# ML020 numeric result audit

Independent recomputation from the stored site-mean CSV confirms all six Hedges-g effects, all six LS variances, all three group-centered correlations/covariances, all three contrast z statistics and p-values, and the five-cluster / leave-one-out Fisher results in `AIZEN_FEINSINGER_1994_RECOVERY_RESULT.md`.

Two SE strings in the narrative result file were manually rounded incorrectly while the corresponding variance, z and p values were correct:

- *Atamisquea emarginata*: `sqrt(1.3044131467641615) = 1.1421090783`;
- *Prosopis nigra*: `sqrt(1.2456137412561472) = 1.1160706704`.

*Cercidium australe* is `sqrt(1.0116604975290502) = 1.0058133512`.

Canonical machine-readable values are produced by `scripts/recover_ml020_aizen_feinsinger_v2.py`; downstream checks should compare against those values rather than narrative decimal strings.