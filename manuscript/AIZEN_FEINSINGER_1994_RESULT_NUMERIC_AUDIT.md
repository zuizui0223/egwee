# ML020 numeric result audit

Independent recomputation from the stored site-mean CSV confirms all six Hedges-g effects, all six LS variances, all three group-centered correlations/covariances, all three contrast z statistics and p-values, and the five-cluster / leave-one-out Fisher results in `AIZEN_FEINSINGER_1994_RECOVERY_RESULT.md`.

The recovery now deliberately uses the same small-sample correction as the existing primary EGWEE scripts:

`J = 1 - 3/(4df - 1)`.

For the four-vs-four ML020 effects, `df=6` and `J=20/23`.

Canonical contrast checks after this alignment are:

- *Atamisquea emarginata*: `I-F=0.2919742504`, `SE=1.1422156828`, `z=0.2556209434`, `p=0.7982435451`;
- *Cercidium australe*: `I-F=0.5011969190`, `SE=1.0059179434`, `z=0.4982483137`, `p=0.6183090331`;
- *Prosopis nigra*: `I-F=0.6549253714`, `SE=1.1161746678`, `z=0.5867588562`, `p=0.5573656730`.

The programme Bonferroni p remains exactly `1.0`, so the five-cluster Fisher and omit-ML001 Fisher results are unchanged by this correction-definition alignment.

Canonical machine-readable values are produced by `scripts/recover_ml020_aizen_feinsinger_v2.py`; downstream checks should compare against those values rather than narrative decimal strings.
