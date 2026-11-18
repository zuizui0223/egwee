# CY001 independent Cyanus source-gate result — 2026-11-18

**Actual outcome: source file access STOP, not an ecological test or null effect.**

Original article: Labonté et al. (2024), *American Journal of Botany* 111(12):e16440, [10.1002/ajb2.16440](https://doi.org/10.1002/ajb2.16440); [full primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11659934/). Dataset: [Dryad 10.5061/dryad.9p8cz8ws1](https://doi.org/10.5061/dryad.9p8cz8ws1).

## Executed source gate

- Protocol-only frozen at commit **`a118ab77e71a097b46d264738e34c0428384a304`** before any new maternal rpm or seed values were inspected.
- GitHub Actions source-check: [run 44235962169](https://github.com/zuizui0223/egwee/actions/runs/44235962169); metadata-only artifact [14396219408](https://github.com/zuizui0223/egwee/actions/runs/44235962169/artifacts/14396219408) SHA256 `7e314bcc1902eeb22304bcc3ab7aab389743f67c3cf575a7c2e15330c175cbff`.
- Official Dryad dataset DOI/version metadata verified. **Both original published files** and file-level SHA256 digests verified in the version inventory:

| File | Official bytes | Original SHA256 |
|---|---:|---|
| `Data_Dryad.xlsx` | 27,995 | `18941f666c040c81c5db3f43c661d44fc157e9db636eef07a4aafd49f77b5332` |
| `README.md` | 15,811 | `530018a194d6ccdad3bea3b504e48b5c1b0f9f1fe1e9945fe9ca8aa8708fbcb1` |

- The official advertised original XLSX download route returned **HTTP 401 Unauthorized** in the Actions environment. Therefore **zero real worksheets, zero original maternal IDs, zero plot joins and zero numeric mating or seed outcomes were read or estimated**. This is an access-route failure, not evidence that the publicly listed dataset is unavailable to a browser or biologically negative.

## Why this original study remains the strongest next test

The primary article and accompanying public Dryad README describe **33 original mother-level records from 12 plots on one farm**, measured in 2019. The records contain mother-matched **relative visits/15min (E), conspecific pollen donor density (F), floral richness and density (G,H), mother allele number (B), progeny multilocus correlated paternity `rpm` (D), and seed number (AB)**. The original article has *already* reported pollinator functional-group effects on progeny Hs/rpm, so repeating its conclusions is not new.

**Selection limitation:** those 33 genotyped mothers were sampled from **64 plants that produced >=20 viable germinable seeds**, out of 144 transplanted plants. That is a seed-fitness-conditioned subset, not the complete reproductive-success distribution. Any seed-number model can only be descriptive within that selected subset, and cannot identify population-wide failure/recruitment dynamics.

**Frozen test when source is available:** validate original file SHA256 before opening worksheets; source-only schema inspection then separate 12-plot fold analysis of `rpm`, comparing M0 mother alleles + donor density + floral context + strip vs M1 plus mother-specific visitation, fixed λ1 ridge. Practical positive call requires **>=5% MSE gain and >=8/12 positive plot folds**, not a microscopic gain. Original seed count is the conditional secondary comparison, *not* a replacement primary. `rpm` is a different genetic process outcome from LA005's detectable nonmaternal marker fraction; **never pool coefficients or Brier scores directly**.

## Software state and exact missing input

- New source gate: `audit_cyanus_CY001_source.py`.
- New two-step original-data analysis engine: `run_cyanus_CY001_plot_holdout.py`, with **pre-outcome protocol hash and git-ancestor check** and **hardcoded official `Data_Dryad.xlsx` SHA256**.
- Stage 1 `--mode schema`: uses a local source XLSX, confirms 33 unique mothers/12 plots/treatment labels, records only SHA256 and structural counts.
- Stage 2 `--mode fit --locked-schema ...`: requires the same original file hash and a separately stored schema receipt, then tests all 12 held-out plots. It emits only aggregate fold scores and retains the predeclared scientific decision. The source and raw maternal/offspring rows are never committed.
- CI uses only **synthetic XLSX**, not original biological data; a green CI is not a completed original data analysis.

**Next unresolved input:** the exact published `Data_Dryad.xlsx` (27,995 bytes, official SHA256 above). A verified source file, not its name/metadata, is needed before effects can be estimated. A different download location or browser method must still produce the exact official source SHA; no data substitution, 401 bypass or guessing.

The previously locked LA001/LA002 negative seed-prediction results, LA005 small within-study maternal-mating proxy gain and wider EGWEE fragmentation syntheses are unchanged. **No new independent natural replication has been completed yet.**
