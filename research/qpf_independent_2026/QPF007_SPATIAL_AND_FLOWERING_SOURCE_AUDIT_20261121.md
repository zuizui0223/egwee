# QPF007 — spatial and flowering metadata audit

**21 November 2026; source-coverage conclusion, no new effect estimate.**

## Decision

The released source material inspected here supplies no documented plant-array
coordinates, measured pair distances, or verified identifier-to-position map.
A distance-adjusted contact–parentage estimate cannot currently be justified.
This does not prove that the authors never measured positions or that unreleased
metadata do not exist.

The flowering limitation is more specific than an entirely uncontrolled
phenology difference: the [experimental design](https://doi.org/10.1371/journal.pbio.3003579)
placed ten flowering plants in each cage session, with observations lasting
approximately 30 minutes. Plants came from the same temporal sowing block and
were standardized to 3–4 weeks of age. Existing session conditioning therefore
preserves broad concurrent flowering. Released fields do not supply pairwise
flowering/receptivity intervals within that session.

## Source inspection

| Official file | Header count | Verification in this audit |
|---|---:|---|
| data_ABPOLL_ID_resume.txt | 678 | Existing derivative source-schema receipt, independently reopened |
| data_ABPOLL_ID_level_detID.txt | 169 | Same receipt |
| data_ABPOLL_fix10_paternities.txt | 3 | Same receipt |
| data_ABPOLL_observations.txt | 10 | Live header-only read |
| data_ABPOLL_flower_level_detID.txt | 175 | Live header-only read |
| data_ABPOLL_flower_resume.txt | 658 | Live header-only read |
| data_ABPOLL_ID_level_detflo.txt | 178 | Live header-only read |

The first three schemas come from source-audit run
[44306123175](https://github.com/zuizui0223/egwee/actions/runs/44306123175),
artifact 14427717781, containing `qpf007_original_parentage_ID_receipt.json`.
The four header-only reads do **not** certify those complete files' checksums.
All sources are from the [official Zenodo record](https://doi.org/10.5281/zenodo.21628183).
No original observation or individual identifier values were printed or used.

The observations header is `session, people, time, duration, ID_full, ID,
noHp, flow, id_flow, id_flow_full`. The plant summary includes flower counts,
stem counts and height measurements. None establishes physical interplant
distance. Recorded flower positions in the article are ordinal positions
down a stem.

The [official README](https://zenodo.org/records/21628183/files/README.txt?download=1)
defines `nb_dist_vis` as the number of flowers visited on a plant, not spatial
distance; `mean_nb_dist_flo_out_coXX` also concerns numbers of flowers.
Identifier numbers, source row ordering and flower ranks must not be converted
to plant coordinates.

The README and both R scripts were checked against the official MD5 manifest:

| File | Verified MD5 |
|---|---|
| README.txt | fe32260ef18b1eeef653c2d4c41e8835 |
| script_ABPOLL_main_analyses.R | 52b2bdf6cc591f10b0a145826179370c |
| script_ABPOLL_variance_partition.R | 6500aca492767ecca2449e1fef6e98fd |

No documented spatial mapping or pairwise phenology calculation was identified.
Plot-coordinate settings in an R script are not plant-position measurements.
The text of [S1](https://doi.org/10.1371/journal.pbio.3003579.s001),
[S2](https://doi.org/10.1371/journal.pbio.3003579.s002) and
[S3](https://doi.org/10.1371/journal.pbio.3003579.s003) was also inspected; these
describe pollen counting, genotyping and variance decomposition rather than
an array map or flowering schedule.

## Data needed for a future adjustment

A valid spatial addition would be either a position table keyed by
`session × ID_full`, with spatial units and placement/repositioning rules, or
a pair-distance table keyed by `session × ID_full_foc × ID_full_part`.
Flowering overlap would additionally require documented timing/receptivity
observations aligned to the pollinator session. Existing identifiers permit
such a join; the required measurements are not established.

## Consequence for the current result

PR #92's missing-row sensitivity and its original-source numeric results are
unchanged. The defensible scope is: **contact information under the chosen
carryover rule remains associated with assigned parentage beyond session and
parental sampled-offspring totals, including the stated missing-row sensitivity;
physical distance and finer reproductive availability remain unadjusted.**

This is one experimental programme. Neither a spatially adjusted effect nor a
new replication is claimed. The source-coverage stop closes this adjustment
attempt until additional documented metadata become available. No new model,
raw-data redistribution, main-branch modification or theoretical egwe change.
