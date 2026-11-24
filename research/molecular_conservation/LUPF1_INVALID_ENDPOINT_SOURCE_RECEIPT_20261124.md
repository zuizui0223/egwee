# LUPF1 frozen stop and source endpoint validity diagnosis — 2026-11-24

**The original preregistered LUPF1 prediction was NOT carried out to completion. Do not report it as a zero or negative predictive effect.**

## Verified execution sequence
1. Initial [run 45311778662](https://github.com/zuizui0223/egwee/actions/runs/45311778662): source schema `number of seeds` vs internal `number_of_seeds` mismatch; source-only source-header spelling verified independently in run 45328163059, and exact-key decoder repaired with an additional synthetic regression test. No model/outcome result.
2. Rerun [45328288235](https://github.com/zuizui0223/egwee/actions/runs/45328288235) passed the corrected source header; frozen strict "nonnegative integer seeds" endpoint gate stopped as `SOURCE_ENDPOINT_INVALID_STOP` **before fitting**.
3. Post-stop [run 45328462636](https://github.com/zuizui0223/egwee/actions/runs/45328462636), evidence [artifact 14891170399](https://github.com/zuizui0223/egwee/actions/runs/45328462636/artifacts/14891170399), ZIP SHA256 `5dc7ac5bab8dbf8d79ccfae48406098ddd1fe31474c7cb7f1a45526bf5271e61`. Official source article 29606180, 3,024 original data records; **source endpoint validity only**, no individual values released, no genotype samples or regression coefficients.

| Original field category | Count |
|---|---:|
| `number of seeds`: finite nonnegative integer | 1,881 |
| `number of seeds`: finite nonnegative noninteger | 153 |
| `number of seeds`: missing/NA | 990 |
| `number of seeds`: negative | 0 |
| `flowering_onset`: finite nonnegative numeric | 2,042 |
| `flowering_onset`: missing/NA | 982 |
| Both observed with nonnegative **integer** seeds | 1,858 |

`number of seeds` is a **source-stored outcome column**, not a guarantee that numbers are raw counted viable seeds. In the same authors' preceding 2025 programme, the total seeds-per-plant metric was estimated as fruit count × mean seeds per sampled fruit, producing legitimate fractional values (Sacristán-Bajo et al. 2025, `Evolutionary Applications` DOI 10.1111/eva.70087, Methods §2.3). **Whether 2026 used precisely the same measurement protocol is not separately verified** in this receipt.

## Scientific consequence and firewall
- Original LUPF1's prespecified all-source integer-requirement was contradicted by 153 original numerical observations. **Original primary decision stays `SOURCE_ENDPOINT_INVALID_STOP`; no posthoc dropping 153 rows, rounding, or calling the stop a biological null.**
- A **separately recorded exploratory LUPF2** accepts nonnegative *numeric* source reproductive-index values, including fractional recordings, and otherwise retains identical held-out folds, M0/M1, ridge penalty and measurement limitations. Its preread design was committed at `053eca26bc1b527e828cb82cbac9318d20be7621` before any signed predictor association of this new run.
- LUPF2 is **not confirmatory** or a natural G×I×F functional-state test. Seed-data missingness is extensive and its mechanism is unknown. The original group names, genomic pedigree and pollination services remain unverified. Do not interpret seed production conditional on being measured as total population reproductive recovery.
