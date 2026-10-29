# EGWEE Systematic Coverage and Moderator Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a preregistered coverage/moderator expansion lane that turns EGWEE from a frozen five-cluster global-exchangeability test into a systematic multilayer response-geometry meta-analysis without significance-driven corpus expansion.

**Architecture:** Preserve the current Journal of Ecology analysis as a frozen baseline. Add a separate dated amendment and machine-readable contract for systematic search, pair-specific coverage, moderator gates, and closed-candidate reopening rules. CI validates that the new phase cannot mutate the frozen five-cluster numerical baseline or reopen structurally invalid systems for significance repair.

**Tech Stack:** Markdown protocol/specification files, JSON schemas/contracts, CSV ledgers, Python 3.11 contract checker, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-17-egwee-systematic-coverage-moderator-expansion-design.md`

## Global Constraints

- The frozen direct baseline remains 5 independent clusters / 17 marginal effects.
- Frozen canonical Fisher p is `0.01212432`; omit-ML001 p is `0.18194353`; zero-covariance p is `0.03860161`; covariance-free bound p is `0.28061178`.
- No sixth direct cluster may be sought merely to repair leave-one-cluster-out significance.
- Hedges-g and Fisher-z remain separate effect families.
- Lower-level plants, flowers, fruits, progeny or loci cannot be promoted to fragmentation replicates.
- `ML009` and `ML013` remain structurally closed unless genuinely new independent landscape/reference replication appears.
- Moderator categories must be defined independently of the response they explain.
- Search completion, not statistical significance, is the expansion stopping rule.
- No expansion result enters the Journal of Ecology manuscript until the declared search universe is fully screened and the expansion contract passes.

---

### Task 1: Freeze the coverage/moderator protocol amendment

**Files:**
- Create: `manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-17_COVERAGE_MODERATORS.md`

**Interfaces:**
- Consumes: `manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md`, current five-cluster result, existing search-stop rule.
- Produces: authoritative prose contract for search universe, estimands, moderator gates, reopening and stopping rules.

- [ ] **Step 1: Write the amendment**

Include verbatim numerical baseline values and explicitly label the expansion as coverage/moderator-driven rather than a sixth-cluster robustness search.

- [ ] **Step 2: Check internal consistency**

Verify the amendment preserves the original `g ~ 0 + layer`, `I-F`, `C-F`, `G_adult-G_offspring`, `G_adult-mean(I,F)` and process-function coupling estimands.

- [ ] **Step 3: Commit**

```bash
git add manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-17_COVERAGE_MODERATORS.md
git commit -m "Freeze EGWEE coverage and moderator expansion"
```

### Task 2: Add machine-readable expansion and moderator contracts

**Files:**
- Create: `manuscript/meta_analysis_coverage_contract.json`
- Modify: `manuscript/meta_analysis_effect_schema.json`

**Interfaces:**
- Consumes: Task 1 amendment.
- Produces: keys consumed by `scripts/check_coverage_expansion_contract.py`.

- [ ] **Step 1: Write `meta_analysis_coverage_contract.json`**

Required top-level keys:

```json
{
  "schema_version": 1,
  "frozen_on": "2026-09-17",
  "baseline": {},
  "search_universe": {},
  "priority_pair_cells": [],
  "moderator_opening_gates": {},
  "structural_hard_stops": [],
  "terminal_candidate_states": [],
  "forbidden_expansion_triggers": []
}
```

The baseline block must carry the exact five frozen p-values/counts from Global Constraints. `forbidden_expansion_triggers` must include `restore_leave_one_out_significance`, `reduce_global_p_value`, and `replace_null_cluster_after_outcome_inspection`.

- [ ] **Step 2: Amend the effect schema to version 3**

Preserve all existing `required_fields`, `primary_tests`, and `forbidden_shortcuts`. Add:

```json
"coverage_amendment": "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-17_COVERAGE_MODERATORS.md",
"moderator_fields": [
  "self_compatibility",
  "autonomous_reproductive_assurance",
  "life_form",
  "longevity_class",
  "fragmentation_age_years",
  "pollination_vector",
  "fragmentation_component",
  "direct_process_measurement",
  "cohort"
]
```

Moderator fields are nullable metadata and do not change effect admissibility.

- [ ] **Step 3: Commit**

```bash
git add manuscript/meta_analysis_coverage_contract.json manuscript/meta_analysis_effect_schema.json
git commit -m "Add machine-readable EGWEE expansion contract"
```

### Task 3: Freeze current information geometry and recovery priorities

**Files:**
- Create: `evidence/meta_extraction/coverage_expansion_pair_coverage_v1.csv`
- Create: `evidence/meta_extraction/coverage_expansion_recovery_priority_v1.csv`

**Interfaces:**
- Consumes: `multilayer_cluster_registry_v1.csv`, `multilayer_cluster_registry_extension_ml020.csv`.
- Produces: auditable coverage snapshot and outcome-independent reopening queue.

- [ ] **Step 1: Record pair coverage at the expansion freeze**

Rows must include at least `I-F`, `C-F`, `G_adult-G_offspring`, and `G_adult-mean(I,F)` with current independent-system counts and a note that target information thresholds are analysis-opening gates, not significance goals.

- [ ] **Step 2: Record recovery priorities**

Prioritize already registered candidates by missing information geometry:

1. `ML006` Primula — high-value `I/F/G_adult` common-frame recovery;
2. `ML008` Tillandsia — direct `I-F` replication;
3. `ML007` replicated fragmentation experiment — `D/I/F`;
4. `ML011` Magnolia — `C-F`;
5. `ML012` Dieffenbachia — `C-G_mating`;
6. `ML010` Penstemon — `C-G_offspring`;
7. `ML004` Conospermum 2020 — gradient `I/F/T` generalisation;
8. `ML005` Conospermum 2026 — `C-G_offspring`.

Include `ML009` and `ML013` with `reopen_allowed=no_without_new_independent_replication`.

- [ ] **Step 3: Commit**

```bash
git add evidence/meta_extraction/coverage_expansion_pair_coverage_v1.csv evidence/meta_extraction/coverage_expansion_recovery_priority_v1.csv
git commit -m "Freeze EGWEE coverage gaps and recovery priorities"
```

### Task 4: Add fail-closed expansion checker

**Files:**
- Create: `scripts/check_coverage_expansion_contract.py`
- Modify: `scripts/check_meta_analysis_contract.py`

**Interfaces:**
- Consumes: amendment, coverage JSON, schema v3, pair coverage CSV, recovery priority CSV, existing cluster registries and current manuscript metadata.
- Produces: zero-exit validation used by GitHub Actions.

- [ ] **Step 1: Write the checker assertions**

The checker must assert:

```python
assert contract["baseline"]["n_primary_clusters"] == 5
assert contract["baseline"]["n_primary_effects"] == 17
assert abs(contract["baseline"]["primary_fisher_p"] - 0.01212432) < 1e-12
assert abs(contract["baseline"]["omit_ML001_p"] - 0.18194353) < 1e-12
assert abs(contract["baseline"]["zero_covariance_p"] - 0.03860161) < 1e-12
assert abs(contract["baseline"]["covariance_free_bound_p"] - 0.28061178) < 1e-12
```

It must also assert schema version 3, all nine moderator fields, `K>=10` one-moderator gates, `K>=20` multivariable gate, structural hard stops `ML009` and `ML013`, all four priority pair cells, all six seed domains, and the three forbidden significance-repair triggers.

- [ ] **Step 2: Cross-check the existing registry**

Assert direct admitted IDs remain exactly `ML001`, `ML002`, `ML003`, `ML014`, `ML020`; ML015 remains gradient-only; ML009/ML013 are still non-identifiable.

- [ ] **Step 3: Update `check_meta_analysis_contract.py`**

Require the new amendment, coverage contract and schema version 3 while retaining every existing numerical/manuscript assertion.

- [ ] **Step 4: Commit**

```bash
git add scripts/check_coverage_expansion_contract.py scripts/check_meta_analysis_contract.py
git commit -m "Enforce EGWEE coverage expansion firewall"
```

### Task 5: Wire expansion validation into CI

**Files:**
- Modify: `.github/workflows/meta-analysis-contract.yml`

**Interfaces:**
- Consumes: Task 4 checker.
- Produces: PR/main validation of the new expansion contract.

- [ ] **Step 1: Add paths**

Add the new amendment, coverage contract, pair coverage CSV, recovery priority CSV, checker, and design/plan files to pull-request and main path filters.

- [ ] **Step 2: Add validation step**

After `Validate protocol-first meta-analysis state`, add:

```yaml
- name: Validate systematic coverage and moderator expansion
  run: python scripts/check_coverage_expansion_contract.py
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/meta-analysis-contract.yml
git commit -m "Run EGWEE expansion contract in CI"
```

### Task 6: Verify without changing the current Journal of Ecology claim

**Files:**
- Read-only verification: `manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md`, `manuscript/meta_analysis_submission_metadata.md`.

**Interfaces:**
- Consumes: all previous tasks.
- Produces: merge-ready PR evidence.

- [ ] **Step 1: Run the new checker**

```bash
python scripts/check_coverage_expansion_contract.py
```

Expected: `EGWEE coverage/moderator expansion contract: PASS`.

- [ ] **Step 2: Run existing meta-analysis contract**

```bash
python scripts/check_meta_analysis_contract.py
```

Expected: existing results-bearing five-cluster contract still passes.

- [ ] **Step 3: Run the full workflow or PR CI**

Expected: `Multilayer meta-analysis contract` succeeds, including anonymous package construction.

- [ ] **Step 4: Inspect diff**

Confirm no numerical result paragraph in `MULTILAYER_FRAGMENTATION_META_ANALYSIS.md` changed and no sixth cluster was admitted.

- [ ] **Step 5: Open PR**

PR title: `Freeze systematic coverage and moderator expansion for EGWEE`.

The PR body must state that this is a coverage/moderator expansion, not significance repair, and that the current Journal of Ecology numerical package remains frozen until the new search universe is completed.