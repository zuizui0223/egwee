# Migration manifest — EGWE natural-data four-gate programme

Migration date: **2026-09-04**

Source repository: `zuizui0223/eco-genetic-warning-extensions` (`main`)

Destination repository: `zuizui0223/egwee` (`main`)

## Ownership decision

`egwee` is the authoritative development home for the independent natural-data four-gate empirical paper. The source EGWE repository retains historical copies and provenance because its integrated archive, validators, and prior publication-router history depend on them. This migration does **not** rewrite or delete frozen results in EGWE.

The natural-data paper is independent of:

- EGWE warning validity;
- EGWE model state-validity / process-portability claims;
- EGC finite-model mechanism and state-separation claims.

Natural datasets are not external validation of the synthetic simulator closure or of the frozen warning statistic.

## Migrated manuscript core

| destination | source path in EGWE | source blob SHA | role |
|---|---|---|---|
| `manuscript/natural_data_four_gate_program.md` | same | `d0809c7...` | four-line programme |
| `manuscript/natural_data_ecological_indicators_spine.md` | same | `362bb7c...` | independent manuscript spine |
| `manuscript/natural_data_gate_registry.json` | same | `644bdb3...` | machine-readable locked registry |
| `manuscript/natural_data_figure_spec.json` | same | `67394e6...` | deterministic figure contract |
| `manuscript/NATURAL_DATA_PUBLICATION_AUDIT_2026-09-01.md` | same | `d1b253d...` | one-paper publication decision |
| `manuscript/NATURAL_DATA_VENUE_AUDIT_2026-09-01.md` | same | `a9b640d...` | venue decision |
| `manuscript/NATURAL_DATA_NEAREST_NEIGHBOR_AUDIT_2026-09-01.md` | same | `b465a50...` | novelty firewall |

Ellipses in this human-readable manifest abbreviate Git blob SHAs; the source repository remains the immutable lookup location for the full identifiers.

## Migrated locked evidence

### Line 1 — no detected transferable residual-context gain after locked partial states

- Honshu–Izu: preregistration + locked result (`evidence/honshu_izu/`)
- Zurich BetterBlooms: preregistration + locked result (`evidence/zurich/`)
- Toronto community gardens: preregistration (`evidence/toronto/`) + shared Toronto/carob locked result (`evidence/shared/`)

### Line 2 — missing contemporary coordinate

- *Oenothera harringtonii*: preregistration + locked result (`evidence/oenothera/`)

### Line 3 — process proxy did not earn endpoint-relevant adequacy / endpoint not identifiable

- *Eschscholzia californica*: discovery preregistration, exact-model preregistration, locked multi-process result (`evidence/eschscholzia/`)
- Mallorca carob: predictive preregistration (`evidence/mallorca_carob/`) + shared Toronto/carob locked result (`evidence/shared/`)

### Line 4 — analytical representation erased mechanistic information

- *Campanula americana*: exact-model preregistration, locked predictive result, response-firewalled rescaling diagnostic (`evidence/campanula/`)

### Cross-study identifiability

- urban–island cross-origin preregistration + locked `cross_origin_convergence_not_identifiable_from_existing_archives` result (`evidence/cross_origin/`)

## Migrated natural mechanism / design background

`background/` contains the material used to connect the four-gate workflow to ecological mechanism without treating those published case studies as prospective validation:

- `empirical_condition_map.md`
- `empirical_measurement_crosswalk.md`
- `natural_state_field_protocol.md`
- `empirical_e3_crepis_audit.md`
- `empirical_e4_miyake_audit.md`
- `empirical_e5_conospermum_audit.md`
- `empirical_e6_spondias_audit.md`

These preserve four particularly useful natural anchors:

- *Crepis sancta* — uncompensated interaction limitation;
- Miyake-jima *Camellia–Zosterops* — movement-mediated compensation;
- *Conospermum undulatum* — cohort/history lag;
- *Spondias purpurea* — near-synchronized interaction–connectivity–function–genetic deterioration.

## Scientific invariants retained through migration

1. No frozen endpoint, holdout unit, seed, bootstrap rule, proxy or claim ceiling is changed by relocation.
2. Heterogeneous systems are not pooled into a common ecological effect size.
3. `not_identifiable`, `not_estimable`, unsupported predictive gain, metadata STOP and access STOP remain legitimate outcomes.
4. A plausible biological proxy is not granted state status without endpoint-relevant predictive evidence.
5. Residual geography/origin/history is interpreted only after upstream measurement and representation gates.
6. Cross-origin convergence remains not identifiable from the existing unmatched archives.
7. Future reader-facing development of this empirical paper belongs in `egwee`; historical EGWE copies are provenance only.
