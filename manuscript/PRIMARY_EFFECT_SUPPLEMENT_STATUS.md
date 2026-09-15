# Full primary-effect supplement status

The reviewer-facing supplement exposes all 17 admitted primary Hedges-g marginal effects without changing the five-cluster primary estimand or treating the 17 rows as independent replicates.

- Supplementary Table S3 contains exactly 17 rows across ML001, ML002, ML003, ML014 and ML020.
- `scripts/check_primary_effect_supplement.py` reconstructs each row from the canonical source effect files and verifies the effect, sampling variance, independent-unit counts, SE and marginal 95% CI.
- Supplementary Figure S1 is generated from S3 by `scripts/build_primary_effect_forest.py`.
- ML001 *Serapias lingua* uses an explicitly separate horizontal display scale because its standardized magnitudes would otherwise compress the remaining 14 effects. The split scale does not alter any value or inference.
- Marginal confidence intervals are descriptive endpoint intervals and are not the covariance-aware layer-separation tests used for the primary result.

No marginal effect, covariance proxy, cluster-level p-value, Fisher statistic or claim ceiling is changed by this supplement.