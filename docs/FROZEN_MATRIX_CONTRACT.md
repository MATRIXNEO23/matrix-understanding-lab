# Frozen Matrix Understanding contract

Source runtime: `MATRIXNEO23/8.10.9evo3-solo-gpt` at commit
`ae82d5cf843d52b3d60caadd161e4a5516fc5d0d`.

Only the semantic contract is reproduced in this lab. No UI, gameplay, memory
store, prompt, GGUF, personality, or production dependency is copied.

## Claim contract

Every interpreted claim carries:

- stable claim and observation IDs;
- speaker, subject, optional target, owner and perspective/belief holder;
- dialogue act (`ASSERT`, `CORRECT`, `QUESTION`, `REQUEST`, `HYPOTHESIS`, `UNKNOWN`);
- typed predicate and object value;
- polarity and optional bounded negation scope;
- temporal relation/expression/validity;
- zero or more entity mentions with type/link/method/confidence/source span;
- claim kind (`EXPLICIT` or `HYPOTHESIS`), confidence and provenance;
- one or more source spans and source IDs.

`PLAYER`, `SELF`, `OTHER:<id>`, `LOCATION:<id>` and `UNKNOWN:<id>` are the
portable subject encodings used by the lab. The lab must never promote a
reported location or a belief to World Truth.

## Predicate taxonomy frozen for P0

`identity.name`, `identity.age`, `attribute.is`, `work.role`,
`residence.place`, `presence.reported`, `possession.has`, `preference.like`,
`family.relation`, `fear.object`, `goal.object`, `opinion.claim`,
`speech.unresolved`.

P0 may report a missing taxonomy item, but must not silently create a new
production predicate.

## Semantic invariants

1. Speaker is derived from the Observation source, not from grammar.
2. Owner follows the claim subject unless an explicit perspective construction
   establishes a different belief holder.
3. Questions and requests are not asserted facts.
4. Hypotheses stay hypotheses.
5. `presence.reported` is an Observation/Belief candidate, never World Truth.
6. Entity resolution prefers the world registry and discourse context; casing
   alone is not sufficient.
7. Unknown is observable and preferable to an invented structured claim.
8. Source text and IDs remain attached to every claim.

## Frozen baseline behavior

Candidate A ports the bounded deterministic engine's behavior, including its
Italian lexicon and conservative unresolved result outside supported grammar.
It is a reproducibility control, not a trilingual redesign.

