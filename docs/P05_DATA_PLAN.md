# Gate 01 — clean Italian training data plan

Date: 2026-09-03  
Scope: isolated `matrix-understanding-lab`; production Matrix remains frozen.

## Decision

The primary P0.5 Italian POS candidate will be trained only from
**UD Italian MarkIT**, pinned to commit
`e210079df0aea331ec1dcaa90648d815ce94c3ce` and licensed `CC BY 4.0`.
No non-commercial treebank is permitted into the training inputs. The upstream
train/dev/test partitions remain distinct, immutable inputs; the P0.5 semantic
gold is a separate benchmark and is never fed to the POS trainer.

This is a deliberately narrow production-candidate data boundary, not a claim
that MarkIT is sufficient for conversational Italian. Its marked-construction
and student-essay domain is a known limitation that must be attacked by the
expanded semantic gold and by comparison against the original VIT-derived lab
model. If the MarkIT-only variant cannot meet every quality gate, additional
commercially usable sources may be evaluated as separately attributable
variants; they must not be silently merged into the primary artifact.

## Frozen source manifest

| Role | Pinned path | Git blob SHA-1 | Bytes | Use |
|---|---|---:|---:|---|
| train | `it_markit-ud-train.conllu` | `b616889012c62e56e991d14ea3653d798d29b74c` | 1,266,080 | POS training |
| dev | `it_markit-ud-dev.conllu` | `f138df1ee75d0e0b35de5856c4b3f6cebca6bbff` | 665,430 | POS trainer evaluation only |
| test | `it_markit-ud-test.conllu` | `fe41f81cf242a022ed814c3684ecc37f5951cddf` | 658,412 | final POS holdout only |
| license | `LICENSE.txt` | `a7b465577bca288b1eb6f7eed92d83558e038d68` | 188 | attribution evidence |
| card | `README.md` | `87bbd5801727c1de536b1eb57c0e81ac992c5fe3` | 1,968 | provenance/domain evidence |

Canonical repository:
`https://github.com/UniversalDependencies/UD_Italian-MarkIT/tree/e210079df0aea331ec1dcaa90648d815ce94c3ce`

The automated pipeline must download only URLs containing that immutable
commit, verify the Git blob identities (and record content SHA-256), normalize
CoNLL-U deterministically, preserve split membership, and emit a complete
provenance manifest beside the model.

## Classification of examined Italian sources

| Source | License / domain | Classification | P0.5 handling |
|---|---|---|---|
| UD Italian MarkIT | CC BY 4.0; marked constructions / student essays; about 1,300 sentences | `TRAINING_ALLOWED` | Primary clean model. Attribution and source/version manifest mandatory. |
| UD Italian TWITTIRO | CC BY-SA 4.0; ironic social posts; 1,424 posts | `REFERENCE_ONLY_PENDING_SHARE_ALIKE_REVIEW` | Useful robustness reserve. Do not train the production candidate until obligations for the distributed model artifact are explicitly reviewed. |
| UD Italian ParlaMint | CC BY-SA 4.0; parliamentary speech; 701 sentences | `REFERENCE_ONLY_PENDING_SHARE_ALIKE_REVIEW` | Domain-diversity reserve; same share-alike stop condition. |
| UD Italian Valico | CC BY-SA 4.0; learner essays; 398 sentences plus corrected counterparts | `REFERENCE_ONLY_PENDING_SHARE_ALIKE_REVIEW` | Error-analysis reserve, not primary conversational data. |
| UD Italian PUD | CC BY-SA 3.0; translated news/wiki; 1,000 test sentences | `REFERENCE_ONLY_PENDING_SHARE_ALIKE_REVIEW` | Evaluation/reference reserve; upstream itself recommends cross-validation if used for training. |
| UD Italian Old | CC BY-SA 4.0; historical poetry | `REFERENCE_ONLY` | Linguistically useful but materially mismatched to current dialogue scope. |
| UD Italian KIParlaForest | CC BY-NC-SA 4.0; spoken conversation | `REFERENCE_ONLY` | Excellent conversational oracle, but non-commercial restriction excludes training. |
| UD Italian VIT | CC BY-NC-SA 3.0 | `REJECTED_FOR_TRAINING` | Existing Candidate B lab artifact remains comparison-only and license-blocked. |
| UD Italian PoSTWITA | non-commercial terms documented by P0 | `REJECTED_FOR_TRAINING` | Retained only as an Italian social-text error oracle. |
| UD Italian ParTUT | non-commercial terms documented by P0 | `REJECTED_FOR_TRAINING` | Retained only as a reference. |
| UD Italian TrIttok | CC BY-SA 4.0 metadata but incomplete upstream README and future-labelled initial release at the audit date | `REFERENCE_ONLY` | Not admitted while provenance/card maturity is insufficient; no rejection based solely on language coverage. |

Italian-only sources remain reserves as requested. Missing EN/ES coverage alone
is never a rejection reason; all candidates are classified by reusable value.

## License and provenance obligations

- Preserve MarkIT creator names, repository, pinned revision, license notice,
  source file identities and transformation history in the model metadata.
- Ship the CC BY 4.0 notice and attribution with every distributed trained-model
  artifact. The OpenNLP runtime remains under Apache License 2.0; runtime and
  training-data licenses are recorded independently.
- Do not describe this as legal clearance. The technical gate establishes an
  auditable input set without a non-commercial clause; final distribution
  policy remains subject to the project's normal license review.
- Any future CC BY-SA variant must be built and named separately and cannot
  replace the primary artifact without documented treatment of attribution,
  adaptation/share-alike and APK/model redistribution obligations.

## Leakage controls

1. The upstream MarkIT train partition alone updates model parameters.
2. MarkIT dev selects trainer configuration; MarkIT test is reported once for
   POS evidence and never used to alter configuration.
3. The expanded Matrix semantic gold is frozen in Gate 03 before mapper fixes.
4. Semantic train/dev rows may guide implementation; semantic test failures are
   reported and may only trigger a general causal fix accompanied by independent
   non-identical regressions and a new recorded experiment iteration.
5. Every run records source URL, upstream commit, Git blob SHA-1, content
   SHA-256, normalized sample count, seed/configuration, tool versions, model
   SHA-256 and output size.

## Gate 01 status

`PASS`: a commercially usable primary Italian input is selected and pinned;
non-commercial data is excluded from training; share-alike and domain-mismatch
reserves are retained without being silently discarded or promoted.
