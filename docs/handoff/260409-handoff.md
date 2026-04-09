# Handoff — 2026-04-09

## 1. Objective

**Restructure `my-workflow/IMPLEMENTATION.md` into IMPLEMENTATION.md + `specs/` directory**, then begin P0 implementation of the workflow engine.

The workflow is a 6-phase, 5-profile pluggable state machine for AI agent task execution. The design phase is complete. The next step is splitting the monolithic IMPLEMENTATION.md (1624 lines) into two concerns:

- `IMPLEMENTATION.md` — implementation roadmap (P0-P4 stages, TDD method, vendor references)
- `specs/` — executable specifications (schema definitions, gate parameters, profile matrices)

**Done when**:
1. IMPLEMENTATION.md no longer references 00-09 main docs (self-contained via specs/)
2. specs/ contains all schema fields, gate parameters, profile matrices from current Appendix A
3. A fresh agent can read IMPLEMENTATION.md + specs/ and implement P0 without consulting any other file
4. After restructuring, begin P0.1 (JSON Schema files)

## 2. Progress

### Completed in this session
- [x] Renamed profiles across all main docs: trivial→quick, moderate→standard, harness→orchestrated
- [x] Added ASCII state machine diagrams to `my-workflow/README.md`
- [x] Created `my-workflow/IMPLEMENTATION.md` (1624 lines) — TDD-first roadmap P0-P4
- [x] Added vendor reference index mapping each implementation step to `vendor/` local paths
- [x] Added TDD methodology section (Red→Green→Refactor discipline)
- [x] Added Appendix A (A1-A40) — extracted all precise implementation parameters
- [x] Resolved 6 internal ambiguities found by Codex review (evolution-archive/19)
- [x] Fixed 3 critical schema gaps (delta-log, event-log, protected files)
- [x] All changes committed and pushed to `main`

### Not started
- [ ] Split IMPLEMENTATION.md into IMPLEMENTATION.md + specs/
- [ ] P0.1: Create 14 JSON Schema files
- [ ] P0.2: Create profile fixtures (5 profiles × N artifacts)
- [ ] P0.3: Transition table + validator script
- [ ] P0.4: Hook baseline (never-crash + profile gating)

## 3. Key Context

### User requirements
- **Language**: User communicates in Chinese, code/commits in English
- **Profile names**: quick / simple / standard / complex / orchestrated (finalized, do NOT change)
- **TDD mandatory**: Schema → Fixture → Transition Validator → Gate Test → Profile E2E → Skill/Command/Agent. This order is non-negotiable.
- **Vendor references must be consulted**: All reference frameworks are cloned locally at `vendor/`. Before implementing any subsystem, read the corresponding vendor code first. Do NOT write from scratch.
- **IMPLEMENTATION.md is SSOT**: When it conflicts with 00-09 main docs, IMPLEMENTATION.md wins.

### Architecture decisions
- **State machine is source of truth**, hooks are enforcement adapters (not the other way around)
- **BLOCKED and DELTA are NOT phases** — they are status/completion_status values or gate-triggered re-entry actions
- **simple profile**: requires verify_cmd but verify-evidence is optional (G8 Ralph Loop does NOT apply)
- **standard/semi-auto lane**: only light quality_fit review, no full spec_fit AC analysis (AC coverage checked in reconcile-settlement instead)
- **event-log.jsonl is runtime core**, not optional observability
- **checkpoint = resume-pack (standard) or handoff.md (complex+)** — not a separate protocol

### File structure
```
my-workflow/
├── README.md              ← ASCII diagrams, human overview
├── IMPLEMENTATION.md      ← SSOT for implementation (1624 lines, to be split)
├── 00-overview.md         ← Frozen skeleton v2 (reference, not implementation guide)
├── 01-triage.md ~ 09-schemas.md  ← Phase definitions (reference)
└── evolution-archive/     ← Historical discussion (read-only archive)
    ├── 14-thatall.md      ← Frozen design decisions
    ├── 15~18              ← Progressive refinements (higher number = higher trust)
    └── 19-codex-...       ← Ambiguity resolutions applied to IMPLEMENTATION.md
```

### Version tiers (A40)
- **v1 core**: state/transition, 14 schemas, fixtures, G0-G9, event-log, resume/handoff, routing
- **v1.1**: Deliver Gate, Config system, confidence-gated review pipeline
- **reserved**: multi-layer injection defense, multi-reviewer routing, pass@k

## 4. Key Findings

### Ambiguities resolved (from evolution-archive/19)
1. `state.json.allowed_transitions` used `EXECUTE->DELTA` and `EXECUTE->BLOCKED` — but DELTA and BLOCKED are not phases. Fixed: transitions are only between real phases.
2. P1.4 said "Quick/Simple don't require evidence" but P2.2 said "verify-evidence is collected after VERIFY" for simple. Fixed: simple runs verify_cmd but evidence is optional.
3. P2.3 said semi-auto "verify-review contains spec_fit" but A33 said semi-auto skips spec_fit. Fixed: semi-auto only does quality_fit.

### Coverage audit results
Two agent-based audits were performed (one against evolution-archive 14-18, one against 00-09). Found 50 gaps total, all resolved:
- 34 items added to Appendix A (A1-A34)
- 3 critical schema gaps fixed (A35 delta-log, A36 protected files, A37 handoff triggers)
- 3 structural items added (A38 routing 3-tier, A39 evidence ladder, A40 version tiers)

### Profile rename scope
Changed in 00-09 main docs + README.md. NOT changed in evolution-archive/ (intentionally frozen). "Anthropic harness" (paper name) and "Harness engineering" (concept) were protected from rename.

## 5. Remaining Work

### Priority 1: Split IMPLEMENTATION.md into specs/

**What**: Extract Appendix A (A1-A40) into `my-workflow/specs/` directory. Each spec becomes its own file.

**Suggested split**:
```
my-workflow/specs/
├── schemas.md        ← A1 (tasks.json fields), A3 (reconcile fields), A4 (verify-review), A5 (context.jsonl), A6 (completion markers), A35 (delta-log), A28 (event-log)
├── gates.md          ← A7 (gate taxonomy), A8 (G5 failure sequence), A9 (G9 three-way), A26 (stall 4-mode mapping), A27 (3-strike semantics)
├── profiles.md       ← A2 (closure matrix), A10 (enforcement matrix), A11 (scope guard), A12 (context thresholds), A31 (deliver gate), A33 (light quality gate), A39 (evidence ladder)
├── routing.md        ← A21 (priority + templates), A19 (continuation 6-check), A20 (semi-auto exit), A38 (3-tier interface)
├── execution.md      ← A13 (resume bootstrap), A14 (orchestrator/worker do-don't), A15 (anti-rationalization), A16 (DONE_WITH_CONCERNS semantics), A17 (backflow triggers), A18 (session reset), A22 (diagnostic routing), A23 (background-alignment order), A37 (handoff triggers)
├── templates.md      ← A24 (spec templates), A25 (ADR template), A34 (review confidence)
├── infrastructure.md ← A29 (.workflow/ layout), A30 (hook 5s timeout), A32 (config 3-tier), A36 (protected files)
└── version-tiers.md  ← A40
```

**After split**: IMPLEMENTATION.md P0-P4 sections reference `specs/*.md` instead of "附录 A*". Remove Appendix A entirely.

**Files involved**: `my-workflow/IMPLEMENTATION.md`, new `my-workflow/specs/*.md`

### Priority 2: Begin P0.1 (JSON Schema files)

After split, create 14 JSON Schema files in `.workflow/schemas/`. Use specs/schemas.md as authority. Consult `vendor/flowspec/` for schema validation patterns.

### Priority 3: P0.2-P0.4

See IMPLEMENTATION.md P0.2 (fixtures), P0.3 (transition validator), P0.4 (hook baseline).

## 6. Recommended Approach

### Files to read first (ordered)
1. `my-workflow/IMPLEMENTATION.md` — the SSOT, read completely
2. `my-workflow/README.md` — ASCII diagrams for visual orientation
3. `my-workflow/09-schemas.md` — current schema definitions (will become specs/schemas.md source)
4. `vendor/flowspec/` — first vendor reference for state machine + schema validation

### Suggested sequence
1. Read IMPLEMENTATION.md end-to-end
2. Create `my-workflow/specs/` directory
3. Extract Appendix A into spec files per the split above
4. Update IMPLEMENTATION.md P0-P4 references from "附录 A*" to "specs/*.md"
5. Remove Appendix A from IMPLEMENTATION.md
6. Verify: IMPLEMENTATION.md no longer contains any "来源：XX§Y" references to 00-09
7. Begin P0.1: create `.workflow/schemas/` with 14 JSON Schema files

### Validation
- After split: grep IMPLEMENTATION.md for "附录" and "来源：0" — both should return 0 hits
- After P0.1: all fixtures in IMPLEMENTATION.md P0.2 should validate against their schemas

## 7. Risks & Anti-Patterns

### Do NOT retry
- **Do not re-read evolution-archive 09-13** — these are superseded. Only 14-18 (and now 19) matter, and their content is already extracted into IMPLEMENTATION.md.
- **Do not modify 00-09 main docs** during implementation. They are reference documents. If you find errors, note them but don't fix during P0.
- **Do not rename profiles again** — quick/simple/standard/complex/orchestrated is final.

### Traps
- `1st-cc-plugin` submodule shows as "dirty" in git status. Ignore it — it has internal uncommitted content unrelated to this work.
- The word "harness" still appears in main docs as "Anthropic harness" (paper title) and "Harness engineering" (concept). These are NOT profile names — do not replace them.
- IMPLEMENTATION.md has "12 个 JSON Schema" in some prose but "14 个" in P0 验收. The correct number is **14** (12 original + delta-log + event-log).

### Edge cases
- `standard/semi-auto` and `standard/full` share the same profile but different lanes. Specs must distinguish their gate behavior (semi-auto skips spec_fit, full does both).
- `simple` is the only profile where verify-evidence is produced but NOT hard-gated. The fixture should include an optional evidence file.

---

## First Step

Read `my-workflow/IMPLEMENTATION.md` completely. Then create `my-workflow/specs/` and extract Appendix A (A1-A40) into the 7-8 spec files listed in Priority 1 above. This restructuring must be done before any P0 implementation begins.
