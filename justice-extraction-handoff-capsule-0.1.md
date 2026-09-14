# Justice Extraction Handoff Capsule

Version: 0.1.0-draft
Status: Draft

## Purpose

Provide a carrier-independent procedure and evidence package that allows a fresh operator, agent, or reasoning system to extract, harden, validate, and checkpoint the next Operational Archeology Justice from its source authority without relying on conversational memory.

The handoff must preserve Justice identity, lineage, doctrine, declared capabilities, reasoning boundaries, validation evidence, runtime and provider separation, and human authority while allowing the implementation carrier to change.

The same handoff should be usable by different reasoning systems so their conformance to the governed extraction process can be compared.

## Governing Invariants

- Requested state is not observed state. Verify the resulting artifact or runtime state after every material move.
- Preserve source doctrine before hardening it. Extraction and semantic modification are separate lineage events.
- Justice identity remains stable across compatible lineage; Justice version changes when its executable contract changes.
- Parent-framework version and Justice version evolve independently.
- Reasoning packets are assembled only from governed projections, never directly from source artifacts.
- Reasoning output is untrusted until it passes the Justice's declared output contract.
- Contract-valid output is not proof that the reasoning itself is correct.
- Governance determines whether a packet is valid. Runtime determines whether execution is authorized. Provider transport determines whether a carrier path is available.
- Provider identity is observable infrastructure, not Justice doctrine, and does not enter the governed reasoning packet.
- Provider readiness does not confer execution authority.
- Justice-specific capabilities must be declared; do not force one Justice's state model, fixture semantics, or doctrine onto another Justice.
- Telemetry may record what occurred but must not decide whether the Justice was correct.
- Human authority remains outside the Justice and retains final control over execution.
- Preserve what crosses the carrier boundary, not the carrier itself.

## Source Authority

The parent Court artifact is the authoritative source for extracting an unseparated Justice's inherited doctrine and parent lineage binding.

Current source authority:
- `framework-court-1.json`
- framework id: `oa.framework.001.beta`
- framework version: `0.1.0-beta`

The parent Court is required for extraction and provenance comparison, but it is not a runtime dependency of an already-extracted Justice Capsule.

During extraction:
- read the target lane from the parent Court;
- preserve inherited doctrine exactly before hardening;
- add standalone Justice identity, version, status, and explicit `parent_framework` binding;
- mechanically compare inherited fields against the source lane;
- do not modify the parent Court as part of Justice extraction unless separately authorized.

## Portable Core

The portable core is shared infrastructure used by extracted Justices without embedding Justice-specific doctrine.

Current portable core:
- `oa_capsule.py` — governed projection, packet-boundary, identity, fixture-capability, and output-contract validation.
- `oa_runtime.py` — execution-authorization boundary.
- `oa_provider.py` — provider identity/readiness and transport boundary.

Core separation rules:
- `oa_capsule.py` must not know the expected answer for a controlled case.
- `oa_runtime.py` must not validate its own reasoning output and must not decide correctness.
- `oa_provider.py` must not know fixture targets, Justice correctness, drift judgments, synthesis state, or human decision authority.
- A governed reasoning packet must remain provider-independent.
- No provider identity, credentials, model id, or transport metadata may enter Justice doctrine unless explicitly declared as doctrine by a future governed contract.
- Execution authorization and provider readiness remain independently observable states.
- Shared core behavior may be extended only when a capability is proven to be reusable across Justices; do not generalize one Justice's doctrine merely to make another Justice fit.

The implementation carrier may change. The responsibility boundaries above must survive the carrier change.

## Justice Payload

Each extracted Justice carries its own governed payload. The payload may differ by Justice, but it must be sufficient for a fresh reasoning system to understand what the Justice is, what doctrine it owns, what may cross the reasoning boundary, and how its output is validated.

Required Justice payload elements:
- stable Justice identity;
- Justice version and status;
- explicit parent-framework identity/version binding;
- inherited and hardened Justice doctrine;
- declared `capsule_contract`;
- declared reasoning case projection;
- declared reasoning Justice projection;
- declared output schema;
- controlled fixture identity and target-Justice binding;
- Justice-specific harness or equivalent proof surface.

Justice-specific capabilities are optional unless declared by that Justice. Examples include:
- fixture state semantics;
- cross-field consistency enforcement;
- legal-state matrices;
- Justice-specific output self-test vectors;
- additional doctrine fields required by that Justice's jurisdiction.

Do not copy capability declarations or reasoning fields from another Justice merely for structural similarity. Derive them from the target Justice's actual doctrine and executable contract.

The Justice payload must remain meaningful if the current Python carrier is replaced.

## Extraction Procedure

Use the following sequence for each new Justice. Do not collapse extraction, hardening, validation, and preservation into one uncontrolled change.

1. Start from a clean, known checkpoint on a dedicated Justice branch.
2. Inspect the target lane in the parent Court and record the parent framework identity/version.
3. Search the repository for any pre-existing standalone identity, fixture, harness, or lineage artifact for the target Justice.
4. Create a standalone 0.1 Justice extraction containing:
   - stable Justice identity;
   - version/status;
   - explicit parent-framework binding;
   - inherited source doctrine only.
5. Mechanically prove inherited doctrine matches the parent lane exactly.
6. Fingerprint and checkpoint the pure 0.1 extraction before semantic hardening.
7. Create a 0.2 descendant and prove it differs from 0.1 only by Justice version.
8. Checkpoint the pure 0.2 lineage event.
9. Discover the Justice's actual executable capabilities before adding Capsule semantics.
10. Add the minimum `capsule_contract` required for that Justice's reasoning boundaries.
11. Create controlled fixtures that validate the Justice's own doctrine without importing another Justice's state model.
12. Exercise the persisted Justice, fixture, and Capsule contract against the shared core.
13. Build a Justice-specific harness or equivalent proof surface from reusable scaffolding plus Justice-specific tests.
14. Compile or structurally validate the harness before execution.
15. Run the Justice harness and record every PASS/FAIL gate.
16. Remove generated artifacts such as bytecode caches before checkpointing.
17. Inspect the exact Git delta; stage only intended artifacts.
18. Run staged integrity checks before commit.
19. Commit the proven checkpoint with a scope-specific message.
20. Verify a clean working tree and exact branch HEAD.
21. Preserve the branch remotely only after the local checkpoint is clean.
22. Verify local and remote commit alignment.

At every step:
- one material move at a time;
- inspect observed state before the next move;
- treat interrupted or unobserved tests as NOT RUN;
- do not modify `main` or production as part of Justice extraction unless a separate release/maintenance procedure explicitly authorizes it.

## Capability Discovery

Before hardening a new Justice, determine which capabilities are universal and which belong only to that Justice.

Universal Capsule requirements currently proven across Risk and Advocate:
- stable Justice identity and version binding;
- explicit `reasoning_case_fields`;
- explicit `reasoning_justice_fields`;
- output `schema`;
- exact reasoning case boundary validation;
- exact reasoning Justice boundary validation;
- exact reasoning packet boundary validation;
- Justice identity binding to its controlled fixture;
- shared runtime authorization boundary;
- shared provider readiness and fail-closed transport boundary.

Justice-declared optional capabilities may include:
- `fixture_contract`;
- legal target-state validation;
- fixture consistency validation;
- `consistency_contract`;
- `state_consistency`;
- enum relationships between output fields;
- additional doctrine fields required in the Justice reasoning projection.

Discovery rules:
- inspect the source Justice before defining its Capsule contract;
- derive reasoning fields from doctrine actually required for that Justice;
- do not add fields merely because another Justice uses them;
- do not manufacture target states for a Justice that has no state model;
- do not modify the shared core merely to make one Justice resemble another;
- extend the shared core only when a capability is demonstrated to be genuinely reusable.

Risk proves that richer state-oriented capabilities can be declared.
Advocate proves that a simpler Justice can omit those capabilities while still using the same Capsule engine and outer harness pattern.

## Validation and BATs

Validation must prove both the Justice-specific contract and the shared execution boundaries. A PASS message is evidence only when the resulting artifact or runtime state has also been observed where applicable.

Minimum validation gates for every extracted Justice:
- Justice artifact loads successfully;
- Justice identity matches the fixture target identity;
- reasoning Justice projection contains exactly the declared fields;
- reasoning case projection contains exactly the declared fields;
- reasoning packet contains exactly `justice` and `case`;
- legal synthetic output passes the declared output schema;
- malformed shape, extra fields, or invalid declared types are rejected;
- Justice-specific output self-test vectors pass;
- execution remains blocked when not authorized;
- provider transport remains blocked when no provider is configured;
- provider transport remains blocked when identity is configured but transport implementation is absent;
- temporary BAT changes to runtime authorization or provider configuration are restored after the test.

Additional gates are required only when the Justice declares the corresponding capability. Examples:
- legal target-state enforcement;
- fixture consistency;
- selector/constraint consistency;
- state matrix validation;
- Justice-specific prohibited combinations.

Current proof baselines:
- Risk Justice harness: 13/13 PASS.
- Advocate Justice harness: 11/11 PASS.

The gate count is not itself the invariant. A Justice with fewer declared capabilities may legitimately have fewer gates. The invariant is that every declared capability and every shared boundary is mechanically exercised.

No real provider/model traffic is required to prove the extraction or harness layer. Provider execution is a separate authorization and transport milestone.

## Lineage and Versioning

Justice identity and Justice version serve different purposes.

Lineage rules:
- a Justice keeps the same stable identity across compatible descendants;
- the Justice version changes when its executable contract or governed semantics change;
- parent-framework version and Justice version evolve independently;
- an extracted Justice must carry explicit parent-framework identity/version binding;
- a parent framework does not silently inherit a newer child Justice contract;
- parent adoption of a newer Justice version must be explicit;
- do not rewrite a historical Justice artifact in place when creating a hardened descendant;
- preserve the pure extraction baseline before semantic divergence;
- prove lineage transitions mechanically by normalized comparison whenever possible.

Recommended extraction lineage:
- `0.1.x` — pure standalone extraction and provenance baseline;
- `0.2.x` — first hardened descendant where Capsule semantics or executable contract changes may begin.

A version change by itself is a lineage event, not proof of semantic change.
A semantic change without an appropriate version change is a lineage defect.

Historical artifacts are evidence. Preserve them unless an explicit archival or deprecation procedure authorizes otherwise.

## Evidence Required

Every Justice extraction must leave an auditable evidence trail sufficient for another operator or reasoning system to reconstruct what changed and why the checkpoint was accepted.

Required evidence:
- source Court identity/version used for extraction;
- extracted Justice identity/version;
- proof that inherited doctrine matched the source before hardening;
- normalized lineage comparison between extraction baseline and hardened descendant;
- hashes or equivalent fingerprints for important governed artifacts at meaningful checkpoints;
- exact Justice `capsule_contract`;
- exact controlled fixture identity/version and target-Justice binding;
- observed harness/BAT results;
- proof that shared runtime/provider boundaries remained fail-closed where required;
- proof that generated artifacts were removed before checkpointing;
- exact Git delta before staging;
- staged integrity check result;
- commit id and commit message for the accepted checkpoint;
- clean post-commit working-tree evidence;
- branch HEAD evidence;
- remote preservation and local/remote alignment evidence when a remote checkpoint is created.

Evidence must describe observed state, not intended state.

If a command reports success but the resulting artifact is not inspected where inspection is materially relevant, treat the move as incomplete.

If terminal echo, shell rendering, or agent narration conflicts with the resulting artifact, the artifact or runtime state wins.

## Fail-Closed Conditions

Stop the extraction or hardening sequence and do not advance the checkpoint when any required boundary cannot be proven.

Fail closed when:
- the target Justice identity or lineage is ambiguous;
- a pre-existing Justice artifact may conflict with the proposed identity;
- inherited doctrine does not match the source lane during pure extraction;
- a semantic change appears without an appropriate Justice version change;
- a lineage comparison produces an unexplained difference;
- required Capsule projection fields are unknown or inferred from another Justice rather than derived from the target doctrine;
- fixture semantics require assumptions that the Justice does not actually declare;
- reasoning case, Justice, or packet boundaries do not validate exactly;
- output schema validation accepts malformed shape or invalid declared types;
- a declared consistency or state contract is not mechanically enforced;
- execution occurs while authorization is expected to be off;
- provider transport succeeds when provider readiness or transport implementation is expected to be blocked;
- temporary BAT changes are not restored after the test;
- generated artifacts contaminate the intended checkpoint;
- staged integrity checks fail;
- the working tree contains unexplained changes;
- local and remote checkpoint state cannot be reconciled;
- a required test is interrupted, unobserved, or otherwise NOT RUN.

Do not convert a fail-closed condition into a warning merely to preserve schedule.

Production, `main`, provider execution, and real model traffic remain outside this extraction procedure unless separately authorized by an explicit release or maintenance process.

## Checkpoint and Recovery

A checkpoint is accepted only after the relevant artifacts and tests have been observed, the intended Git boundary is clean, and the resulting state can be recovered.

Checkpoint rules:
- checkpoint pure extraction before semantic hardening;
- checkpoint lineage creation before further divergence;
- checkpoint proven Capsule reuse before extending the harness;
- checkpoint the completed Justice harness only after its declared validation gates pass;
- remove generated artifacts before staging;
- inspect the exact Git delta before staging;
- stage only artifacts belonging to the checkpoint;
- run staged integrity checks before commit;
- verify the post-commit working tree is clean;
- verify the branch HEAD points to the expected commit;
- preserve important proof points remotely after the local checkpoint is clean;
- verify local and remote commit alignment after remote preservation.

Recovery rules:
- recover from the most recent known-good checkpoint, not from an assumed intermediate state;
- preserve historical checkpoints rather than rewriting them in place;
- do not use `main` or production as the recovery surface for bench extraction work;
- if an edit partially lands, inspect the artifact before deciding whether to retry, repair, or revert;
- if the observed state differs from the requested change, treat the observed artifact as authoritative and determine the next move from that state;
- do not advance from a checkpoint whose evidence package is incomplete.

A clean checkpoint is both a technical recovery point and an evidentiary boundary.

## Handoff Instructions

Give this Capsule, the parent Court source authority, the portable core, and the relevant worked exemplars to a fresh operator, agent, or reasoning system.

Primary instruction:

> Take the next unextracted Justice. Follow this Handoff Capsule to extract, harden, validate, checkpoint, and preserve that Justice without relying on prior conversational memory. Do not copy Risk or Advocate doctrine. Derive the new Justice's identity, doctrine, capabilities, reasoning projections, fixture semantics, and output contract from the source authority and observed repository state. Stop and report a fail-closed condition whenever a required boundary cannot be proven.

The recipient must:
- begin from a clean dedicated branch;
- identify the next Justice from the parent Court;
- search for pre-existing identity or lineage before creating anything;
- preserve a pure extraction baseline before hardening;
- create a versioned hardened descendant rather than modifying the historical extraction in place;
- discover capabilities from the target Justice itself;
- use the portable core without embedding Justice-specific doctrine into shared infrastructure;
- construct controlled fixtures appropriate to the Justice's own contract;
- construct a Justice-specific harness or equivalent proof surface;
- run and report all required shared and Justice-specific validation gates;
- preserve observed evidence for each accepted checkpoint;
- keep production, `main`, real provider execution, and model traffic out of scope unless separately authorized;
- finish with a clean local checkpoint and, when authorized, aligned remote preservation.

The recipient must not assume that matching Risk or Advocate structure is success. Conformance is measured against this procedure, the target Justice's source doctrine, and the resulting evidence.

A recipient may change the implementation carrier, tooling, or syntax when necessary, but may not silently change the governing invariants or responsibility boundaries.

## FIT Acceptance Criteria

The Justice Extraction Handoff Capsule passes its first transfer FIT only when a fresh operator, agent, or reasoning system can use the handoff package to produce the next governed Justice without relying on the conversation that created this Capsule.

Minimum acceptance criteria:
- the recipient correctly identifies and extracts the next Justice from source authority;
- no pre-existing identity or lineage is overwritten or silently ignored;
- a pure extraction baseline is preserved before hardening;
- inherited doctrine is mechanically proven against the parent source;
- lineage/version transitions are explicit and mechanically evidenced;
- the target Justice's capabilities are derived from its own doctrine rather than copied from Risk or Advocate;
- reasoning case and Justice projections are explicitly declared;
- output validation is derived from the target Justice's own schema and optional capability contracts;
- controlled fixtures test the target Justice without inventing unsupported semantics;
- the shared portable core is reused without Justice-specific contamination;
- any proposed shared-core change is separately justified by demonstrated cross-Justice need;
- the Justice-specific harness or equivalent proof surface exercises every declared capability and every required shared boundary;
- execution and provider transport remain fail-closed unless separately authorized;
- required evidence is preserved at each accepted checkpoint;
- the final working tree is clean;
- the accepted commit and branch state are explicit and recoverable;
- production and `main` remain untouched unless a separate release process authorizes them.

Transferability is strengthened if the same Handoff Capsule is independently given to a second reasoning system and both systems produce materially equivalent governed outcomes while preserving the same invariants and evidence requirements.

A FIT fails if success depends on hidden conversational memory, undocumented operator knowledge, copying a prior Justice's shape, or silently relaxing a governing invariant.

Passing one new Justice proves the handoff process can transfer once.
Independent reproduction across different agents, models, or implementation carriers provides stronger evidence that the process is carrier-independent rather than merely repeatable by its original builders.
