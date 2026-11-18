# Original Q–P–F source recovery — 2026-11-18

**Executed decision: original same-flower source access STOP, not an ecological null or a new validation of a functional-fragmentation regime.** This study deliberately leaves the existing QPF six-source registered denominator (PR #66), the LA005 tiny within-source mating gain, and CY002's failed whole-plot visitation transfer unchanged.

## 1. Most directly matched source: *Oenothera fruticosa* (QPF001)

Smith, Swartz & Spigler (2021), *American Journal of Botany* 108:1612–1624, DOI [10.1002/ajb2.1720](https://doi.org/10.1002/ajb2.1720), source data [Dryad 10.5061/dryad.hqbzkh1g9](https://doi.org/10.5061/dryad.hqbzkh1g9).

This original **single natural-site** study observed pollinator visitation to flowers on video and counted conspecific pollen (CP) and heterospecific pollen (HP) grains on the corresponding stigmas. **122 flowers** were filmed/stigmas sampled, but only **93 mature fruits** were recovered with seed-set counts about three weeks later; others were lost or herbivorized. The paper **already showed** that HP deposition negatively predicts seed set at lower CP loads, and that the negative relationship is mitigated at higher CP loads. It is not a novel discovery of ours.

**Actual original-source GET in GitHub Actions:** the Dryad DOI/version/file metadata were verified, showing exactly **one original XLSX**, `FIGO_2019_Data_20210523.xlsx` (**27,351 bytes**, SHA256 `83790bb7d63222e3e21c0ceed5d729cacf63a2df843e5807836d8e5c853447aa`, original release 2021-06-08). A separately indexed, published **public file stream URL** `https://datadryad.org/stash/downloads/file_stream/736848` returned **HTTP 403 Forbidden** in the Actions environment. The official Dryad file API route also had a previously observed access STOP. No worksheet/header, flower ID, pollen count or fruit value was opened, and **no new Q–P–F statistical effect** was estimated. An access failure alone does **not** prove the dataset is private or biologically unusable.

This is still the strongest data candidate because original *within-flower* Q, CP/HP and F are observable rather than synonyms for different years/groups. But **93/122 outcome ascertainment and any repeated flowers on the same plant or date** need exact source checks before an out-of-sample model. It is one natural study site, not landscape-scale replication.

## 2. Argentina anserina (QPF002) — Zenodo record ambiguity is resolved

Koski & Cisternas-Fuentes / Cisternas-Fuentes & Koski (2024), *Proceedings B*, DOI [10.1098/rspb.2023.1519](https://doi.org/10.1098/rspb.2023.1519), original Dryad dataset [10.5061/dryad.98sf7m0pk](https://doi.org/10.5061/dryad.98sf7m0pk).

The Dryad page links related Zenodo DOIs `10563520` and `10563521`. Official Zenodo API inspection verified:

- **10563520 is a concept-record identifier resolving to versioned record 10563521** (not a second independent ecological observation source).
- The versioned record contains precisely **two public R scripts**, `Visitation_Rate_and_SEM_analyses.R` (3,137 bytes; MD5 `5e543853da269942c5b850b464945c06`) and `Segmented_code.R` (1,599 bytes; MD5 `401e75022ad36b4fc7d39d2225c62438`). **No raw visitation/flower/pollen/seed Excel table is listed.**
- Those are public author software outputs, not two independent natural field datasets and not new independent study programmes. The R scripts were **not executed** in the source gate.

The **original 2024 study itself already established** a genetic–ecological interaction: (N_E) changes how visitation affects pollen quality limitation and reproductive outputs. The source population/year grain is also **not fully synchronized**: flower visitation was measured in 2020–2021, pollen–pistil histology pooled 2019–2021, and fruit/seed set mainly in 2022, with one population M93 retaining a 2021 other-project reproductive dataset. The 13 populations cannot simply be treated as same-year same-mother Q–P–F records. Nor can the companion 2025 13-population paper be counted as an independent biological study.

## 3. Test that remains open

A genuine additional Q→P→F *predictive* result would need a source-identifiable original flower, maternal plant, date, video visit effort, CP/HP pollen deposition, and the subsequent fruit/ovule/seed observation. With **one original natural site**, the narrow question would be whether adding measured pollen **quantity and heterospecific composition** improves **held-out date- or plant-block** seed-set prediction beyond visitation and local floral context. It is not a way to discover the already-published HP × CP seed-set mechanism. The exact endpoints, grouping and missing-outcome handling must be declared after seeing the **source variable/schema definitions but before opening signed seed response relationships**.

**Strict original input still missing:** `FIGO_2019_Data_20210523.xlsx` from the original Dryad record, **27,351 bytes**, SHA256 `83790bb7d63222e3e21c0ceed5d729cacf63a2df843e5807836d8e5c853447aa`. A single correct file is enough to attempt the source-only biological key check; its name alone is insufficient.

No coefficient can be supplied honestly without this source. The result of our executed recovery programme is **verified original-source identity + public URL access STOP + Zenodo related-software deduplication + a stricter biological measurement-gate design**, not a new ecological finding.

## 4. Reproducibility receipts

- GitHub Actions source-only complete run: [44242881984](https://github.com/zuizui0223/egwee/actions/runs/44242881984); artifact [14400148492](https://github.com/zuizui0223/egwee/actions/runs/44242881984/artifacts/14400148492), digest `sha256:76ef4328f82bb900cc01f86e238c72ae3bc2fe14c0945b72233a68ef0bad5d45`.
- Verified source-only protocol commit: `0968b56a86c435a83888d4cac12a3621e8335e5a`.
- Executable original URL gate: `audit_public_qpf_source_links.py`.
- Machine-readable source manifest and biological claim limits: `QPF_SOURCE_RECOVERY_RESULT_20261118.json`.

CI used public original URLs, official dataset metadata, bounded transfers and synthetic tests. No original third-party source file, donor/seed/genotype values, or unknown R code was redistributed or run. The frozen QPF atlas PR #66 remains unaffected and no submitted or review-ready manuscript state was changed.
