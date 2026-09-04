# Evidence map

The natural-data paper is organised by **inferential gate outcome**, not by taxon and not as a pooled meta-analysis.

| line | system | gate / outcome | evidence folder |
|---|---|---|---|
| 1 | Honshu–Izu | no detected transferable mainland-distance gain after partial functional state | `honshu_izu/` |
| 1 | Zurich BetterBlooms | 0/6 endpoints with reproducible positive residual urban-context gain | `zurich/` |
| 1 | Toronto gardens | no detected residual urban-context information after partial state | `toronto/` + `shared/` |
| 2 | *Oenothera harringtonii* | missing spatial mating-opportunity coordinate detected | `oenothera/` |
| 3 | *Eschscholzia californica* | primary F endpoint not identifiable; pan-trap state not predictively supported for estimable G/C endpoints | `eschscholzia/` |
| 3 | Mallorca carob | two source pollinator-abundance representations both failed the process-adequacy gate | `mallorca_carob/` + `shared/` |
| 4 | *Campanula americana* | effective-transfer weights erased by feature-wise standardisation | `campanula/` |
| cross-study | urban vs island | `cross_origin_convergence_not_identifiable_from_existing_archives` | `cross_origin/` |

## Reading order

1. Start with `../manuscript/natural_data_gate_registry.json` for locked outcomes and claim ceilings.
2. Read the system preregistration before its result.
3. Use `../background/` only for ecological mechanism/context and prospective design, not as pooled external validation.

## Invariants

- Hold out the declared ecological unit, never rows nested inside it.
- Do not repair or redefine a frozen endpoint/proxy after seeing the outcome.
- Do not interpret a negative residual-context result as state completeness or biological irrelevance.
- Do not treat failed proxy adequacy as evidence that the underlying process is irrelevant.
- Do not infer cross-origin equivalence from within-system results.
