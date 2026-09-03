"""Failure-safe helpers shared by Matrix-NLU automation entry points."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    name: str
    command: list[str]


def atomic_json(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        pathlib.Path(temporary).unlink(missing_ok=True)
        raise


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_step(step: Step, root: pathlib.Path, log_dir: pathlib.Path | None = None) -> float:
    """Run one stage while streaming output and retaining a complete stage log."""
    started = time.monotonic()
    print(f"\n[PIPELINE] {step.name}")
    print("$ " + " ".join(step.command))
    log_handle = None
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(character.lower() if character.isalnum() else "-"
                            for character in step.name).strip("-")
        log_handle = (log_dir / f"{safe_name}.log").open("w", encoding="utf-8")
    try:
        process = subprocess.Popen(
            step.command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
        )
        assert process.stdout is not None
        line_count = 0
        for line in process.stdout:
            print(line, end="")
            if log_handle is not None:
                log_handle.write(line)
                log_handle.flush()
            line_count += 1
            if line_count % 100 == 0:
                print(f"[PIPELINE] {step.name}: {line_count} output lines")
        return_code = process.wait()
    finally:
        if log_handle is not None:
            log_handle.close()
    elapsed = time.monotonic() - started
    if return_code != 0:
        raise RuntimeError(f"step '{step.name}' failed with exit code {return_code}")
    return elapsed


def atomic_promote(source: pathlib.Path, destination: pathlib.Path) -> None:
    """Replace a promoted directory only after a complete staging copy exists."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = destination.parent / f".{destination.name}-staging"
    old = destination.parent / f".{destination.name}-old"
    if staging.exists():
        shutil.rmtree(staging)
    shutil.copytree(source, staging)
    if old.exists():
        shutil.rmtree(old)
    if destination.exists():
        destination.replace(old)
    try:
        staging.replace(destination)
    except Exception:
        if old.exists() and not destination.exists():
            old.replace(destination)
        raise
    if old.exists():
        shutil.rmtree(old)


def file_manifest(root: pathlib.Path) -> list[dict]:
    return [
        {"path": str(path.relative_to(root)), "bytes": path.stat().st_size,
         "sha256": sha256(path)}
        for path in sorted(root.rglob("*")) if path.is_file()
    ]
