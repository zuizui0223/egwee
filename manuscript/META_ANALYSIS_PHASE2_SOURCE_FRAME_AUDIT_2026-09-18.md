# Phase-2 source-frame audit — updated 2026-09-20

## Current state

The five-cluster Journal of Ecology package remains the frozen Phase-1 submission baseline. Phase 2 is a separate systematic-coverage programme and is not a significance-repair search.

One prespecified repeated layer pair has now crossed its quantitative opening gate:

- `G_adult-G_offspring`: **5 independent programmes / gate met / synthesis completed**;
- pooled adult-minus-offspring contrast: **+0.129**;
- modified Knapp–Hartung 95% CI: **[-0.655, +0.912]**;
- no common directional cohort lag is resolved.

This quantitative result alone does **not** permit Phase-2 supersession. The systematic-frame completion requirement remains active.

## Source-frame state

| frame | source denominator / materialization | current status | next operation |
|---|---|---|---|
| SF01 | Aguilar et al. 2006; 89 species / source publications exposed by Supporting Table S1 metadata | source verified; row materialization blocked because the historical KNB/DataONE object cannot currently be resolved reproducibly | revisit only through a stable publisher/DataONE object route |
| SF02 | Aguilar et al. 2008; 101 publications / 102 unique species | source verified; Appendix S1 row materialization blocked by Wiley download access | revisit only through a stable legitimate Appendix S1 route |
| SF03 | Aguilar et al. 2019; 179 plant species; two public Supporting Information filenames verified | source verified; both Wiley supplement downloads return 403 HTML in reproducible Actions probe | revisit only through a stable legitimate Appendix S1 mirror; do not substitute article aggregate counts |
| SF04 | González et al. 2019 Figshare | **materialized: 92 case rows / 38 publications / 38 species; outcome columns excluded** | screen 38 publications and crosswalk programmes |
| SF05 | Miguel-Peñaloza et al. 2023 Table S1 | **materialized: 177 population rows / 65 source-selected studies / 31 meta subset; 25 multilayer hints fully design-screened** | restore at least 9 outcome-excluded identities and reconstruct broader outcome-blind frame |
| SF06 | Aguilar et al. 2024/2025 Supplementary Table S1 | **materialized: 426 source rows / 255 publications / 261 species; outcome fields excluded** | screen publication rows and crosswalk repeated I/F/C systems |
| SF07 | Olhnuud et al. 2025 Dryad; 80-study source denominator; version 384447 and file IDs verified by public API | source verified; Abundance API download works but Richness returns 401 and UI file routes return HTML; linked Zenodo code contains no data mirror | revisit only through a working official machine-readable Richness route |
| CF01 | backward/forward citation expansion through 2026-09-18 | **partial seed manifest frozen: 363 canonical search units; 83 DOI-bearing + 280 citation-only; OpenAlex fail-closed resolver implemented** | resolve bibliography uniformly, then materialize backward/forward citations for every resolvable seed; blocked source frames remain to be added later |

## Completed quantitative development

### SF05 design and quantitative gates

All 25 SF05 bibliography-level multilayer hints have been design-screened without using candidate effect direction or significance.

- 6 advanced to quantitative full-text screening;
- 4 advanced to exposure/layer verification;
- 15 closed on design geometry;
- 0 remained pending at the design-screen stage.

The six quantitative candidates were then resolved under prespecified pair rules. Parkia and Heliconia yielded admissible Phase-2 genetic-pair information; the other current pair gates closed without changing the frozen Phase-1 result.

### CF01 G-pair expansion

Targeted citation expansion recovered two independent *Prunus africana* programmes:

- Ethiopian forest-patch programme — P2_CF01_GPAIR_002;
- Kakamega fragment/main-forest programme — P2_CF01_GPAIR_003.

Together with Spondias, Parkia and Heliconia, these opened the five-programme `G_adult-G_offspring` synthesis.

The cross-programme result does not resolve a universal directional adult-versus-offspring lag. Moderator models remain closed at K=5.

Brosimum is not used to inflate the pair denominator: its public genotype reconstruction does not reproduce all publication H_O cells under one transparent estimator and remains fail-closed.

## Current pair coverage

- `I-F`: **1/5** independent direct programme; the 32-record outcome-blind SF06 fragmentation screen is complete and yielded 7 design-passing candidates, but all 7 are quantitatively closed/blocked under the current independent-unit/dispersion contract;
- `C-F`: **2/5**; the corrected 16-record SF05 C-enriched screen is complete and all 16 close because no same-programme eligible F and/or admissible fragmentation geometry is present;
- `G_adult-G_offspring`: **5/5 — analysis opened and completed**;
- `G_adult-mean(I,F)`: **0/5**; among the currently materialized unresolved canonical identities, metadata expose **0** records already carrying G_adult + I + F together.

These are information thresholds, never recruitment targets for statistical significance. Every eligible programme in the completed search universe must remain in the corresponding analysis regardless of direction.

## Pair-specific coverage screens completed

### I-F

The SF06-derived metadata firewall identified 32 unresolved publication identities with pollination/interaction, reproductive fitness and source-labelled habitat fragmentation.

All **32/32** have now completed outcome-blind design screening.

- 7 passed the design geometry gate;
- 24 closed on exposure/independent-unit/common-frame geometry;
- 1 thesis-level source was routed to programme decomposition;
- all 7 design-passing candidates were then audited for quantitative recoverability;
- **0** new I-F programmes were admitted.

The quantitative failures are methodological rather than outcome-based: missing fragmentation-level dispersion, graphical-only patch responses without preregistered digitization, model contrasts without compatible Hedges-g standardisation, or unrecovered site/cell allocation. Direct I-F coverage therefore remains **1/5**.

### C-F

The SF05 C-enriched lane was rebuilt after linking the already-admitted Heliconia programme and fixing a queue-provenance bug. The corrected queue contains **16** unresolved identities.

All **16/16** have completed design screening and **0** advance to quantitative C-F recovery. The dominant reason is biological/evidentiary separation: papers measure pollen/seed movement, mating and genetic state in detail but do not measure an eligible direct reproductive-function endpoint on the same fragmentation exposure.

Direct C-F coverage therefore remains **2/5**.

### G_adult-mean(I,F)

The current materialized SF04/SF05/SF06 cross-frame metadata contain **0 unresolved canonical identities** already tagged with G_adult + I + F together. This is a current-frame observation, not a global absence claim, because SF01/SF02/SF03/SF07 and full citation expansion remain incomplete.

These completed negative screens are stopping evidence, not prompts to relax pair definitions or search until the denominator reaches five.

## Row materialization progress

The systematic-frame bottleneck has moved from model fitting to source-universe completion.

Completed or partially materialized:

1. **SF04** — complete public Figshare publication identity ledger: 38 publications, 38 species, 92 source case rows. Treatment/control means, SDs and sample sizes were intentionally excluded from the Phase-2 bibliography ledger.
2. **SF05** — complete for the published 65-study source-selected subset, but the source itself removed at least nine identities using outcome-related FSGS rules, so its outcome-blind denominator remains incomplete.
3. **SF06** — outcome-blind publication ledger materialized: 426 source rows, 255 deduplicated publications and 261 species. `Hedges_d` and `V(d)` were excluded from the bibliographic ledger.
4. **Cross-frame identity firewall** — SF04+SF05+SF06 collapse to 351 canonical publication identities; **11** are already linked to known EGWEE programmes and **340** remain unresolved. The outcome-blind metadata queue contains **60** unresolved multilayer hints after the Heliconia link.
5. **CF01** — the targeted G-pair recovery is now supplemented by a canonical partial all-seed manifest: 363 search units, of which 83 already carry DOI and 280 require citation resolution. The manifest is outcome-blind and retains blocked-frame incompleteness explicitly.

Access blockers:

- **SF01** — public metadata verified but historical KNB/DataONE object bytes are not reproducibly resolvable.
- **SF02** — Wiley Appendix S1 is source-verified but cannot be downloaded reproducibly in the current execution environment.
- **SF03** — both named Wiley supporting PDFs are source-verified; standard public supplement downloads return 403 HTML, and no complete alternative Appendix S1 mirror was found.
- **SF07** — public Dryad API verifies version/file metadata; Abundance downloads, while Richness is blocked (API 401; UI routes return HTML), and the linked Zenodo code does not mirror the CSV.

## Next executable milestone

The main line is now:

1. complete fail-closed bibliographic resolution of the frozen 363-unit partial CF01 seed manifest through the OpenAlex route;
2. materialize backward/forward citations uniformly for every resolved seed through the frozen 2026-09-18 cutoff;
3. restore the missing SF05 outcome-excluded identities where legitimately recoverable;
4. revisit SF01/SF02/SF03/SF07 only through stable legitimate public object routes rather than repeated blocked-download variants;
5. deduplicate the expanded records to programme identities and complete title/abstract/method screening before numerical extraction;
6. only then evaluate whether the systematic-frame completion gate is satisfied.

Until that is complete, the frozen five-cluster Journal of Ecology manuscript remains the submission-valid baseline even though the adult-versus-offspring pair has reached 5/5 and has a valid Phase-2 estimate.
