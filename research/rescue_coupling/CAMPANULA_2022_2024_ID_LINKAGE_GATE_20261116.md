# Campanula glomerata — outcome-blind natural/translocation molecular–reproduction identifier audit
## 2026-11-16; original published source IDs, separate generations and independent units

**Scope:** identifiers only. The positive ID matches below establish **textual linkage candidates**, not measured genomic contributions to ecological function. Neither HL numerical values, genotype alleles nor reproductive outcomes were opened. No effect size or genetic rescue causality is claimed.

## Publisher sources and pinned original files

Two related but analytically distinct sampling programmes, not four independent biological studies:

1. **Natural source populations (2022):** Van Rossum et al., [Frontiers in Conservation Science, DOI 10.3389/fcosc.2022.829332](https://doi.org/10.3389/fcosc.2022.829332). Natural seed-progeny rosette fitness [Zenodo 5676272](https://doi.org/10.5281/zenodo.5676272), SHA256 `a1c50c74d0bd2c9a00b7a0d42322c31c30c53789e3b5cadbe67b08cee878f6a7`; adult/progeny SSR genotypes [Zenodo 5676286](https://doi.org/10.5281/zenodo.5676286), SHA256 `6fa7f4289236d4deab2151f5a76a2a555ee3513f959821adb5aa8ce5a748df21`.
2. **Translocated populations (2023–2024):** Van Rossum et al., [Global Ecology and Conservation 46:e02548 (2023)](https://doi.org/10.1016/j.gecco.2023.e02548) and Van Rossum & Le Pajolec, [Plant Biology 26:427–436 (2024)](https://doi.org/10.1111/plb.13631). SSR F1 and transplant source [Zenodo 7954368](https://doi.org/10.5281/zenodo.7954368), SHA256 `df204199595f7860b711b52ca49633f3a2339b0d37fa9ab8ae05866df8883636`; maternal/F1 fitness [Zenodo 8217417](https://doi.org/10.5281/zenodo.8217417), SHA256 `8bd38bb15f3fb1734b752d0eedb2a071e8340ee45596cf8e8efd98b871db47bf`.

A source-header-only first pass was reproduced by CI [43698265238](https://github.com/zuizui0223/egwee/actions/runs/43698265238), and the corrected ID-only audit by CI [43876726072](https://github.com/zuizui0223/egwee/actions/runs/43876726072), output artifact [14229702535](https://github.com/zuizui0223/egwee/actions/runs/43876726072/artifacts/14229702535).

## Correct source and identifier denominators

| Published source unit | Full source XLSX rows excluding header | Rows containing any whitelisted identifier cell | Interpretation |
|---|---:|---:|---|
| Natural population seed progeny fitness | **507** | **502** | **5** rows have no readable whitelisted ID fields; these cannot be silently assigned to genomic samples |
| Natural population SSR genotypes | **680** | **680** | **178** records `adult`; **502** `progeny` |
| Translocated SSR genotypes | **716** | **716** | **302** `t` transplants, **247** `p` seed progeny, **166** `r` recruits; **1** generation code absent |
| Translocated maternal seed/flower fitness | **188** | **188** | F0 mothers, not 188 independent landscapes |
| Translocated progeny fitness (repeated/offspring records) | **990** | **990** | offspring records nested within maternal families |

The `t/p/r` interpretation is supported by the 2023 published article's transplants, seed progeny and recruits grouping (https://doi.org/10.1016/j.gecco.2023.e02548). The cohort labels still require same-individual IDs for linkage.

## Exact string matching: natural population sources

| Link contract | Matching unique ID keys | Why it is not automatically a paired genotype–fitness dataset |
|---|---:|---|
| `Ind` alone, all adult+progeny genotypes vs fitness | 126 | 235 fitness records share those keys, reflecting reused individual labels across populations |
| **`Pop×Ind`**, all-genotype generations vs fitness | **30** | Distinct exact keys and no duplicate matches, but some belong to the *adult* genetic generation |
| `Pop×Ind` with genotype = `progeny` | **22** | Candidate **same-generation** genotype-to-rosette association; identity semantics, source study year and population units need checking |
| `Pop×Ind` with genotype = `adult` | **8** | Cannot be treated as the same cohort as the fitness seed progeny merely due to a reused ID |

The natural 507-row fitness workbook *itself* has `HL` and `Rosette diameter (cm)` columns in a common row. That is a separate self-contained **genetic-marker-derived homozygosity × juvenile general fitness** analysis route, not a direct link to a newly genotyped separate SSR table or an interaction-mediated seed/fertilization function. A future HL pilot must be preregistered and kept separate from direct ecological-function rescue.

## Exact string matching: translocated populations

For the **F0 transplant** genetic subset (`Generation=t`, 302 genotypes), only **6** strict `Site×Source×Ind nb` keys match the maternal `Site×sourcEMO pop×maternal code` table. For the **recruit** genetic subset (`r`, 166 records), **38** literal `Site×Ind nb` names match the F0 maternal table but no complete `Site×Source×Ind` keys: those recruit IDs cannot be assigned maternal genotype identity. The **seed progeny** genetic subset (`p`, 247 records) has **zero** matches by the tested keys.

**Within the fitness workbook only**, F0 `Site×source×maternal code` has **144 distinct unique keys** in common with the F1 fitness sheet; they cover **990 F1 rows**. These are **144 candidate maternal families**, NOT 990 independently genotyped plants. The source maternal table has **188** rows, so **44/188** F0 maternal records have no full-key match to the F1 sheet. The identical 144 keys are one-to-one in the F0 table; F1 rows recur within families (maximum **14** offspring records per matched full key). A maternal-to-offspring biological relationship is supported by within-workbook fields but remains subject to original sample/cohort labels.

The 2024 original article already studied maternal origin effects, early biparental inbreeding depression and F1 juvenile fitness (https://doi.org/10.1111/plb.13631). Simply recomputing their associations is not a new ecological-function-rescue discovery.

## Next decision and nonclaims

- **Candidate observational G→W link:** 22 natural progeny SSR–rosette literal keys (not guaranteed actual same-individual records).
- **Direct within-row observational G→W route:** natural fitness workbook's `HL` and rosette diameter; a new fixed analysis can test neutral-marker homozygosity versus growth, but growth alone is not pollination efficiency or seed production.
- **Strong developmental-function unit:** F0 maternal `Site×Source×code` across 144 families and 990 F1 offspring rows, with seed germination / viable seedlings and later growth recorded in compatible source datasets; future analysis must condition on maternal family/plot and identify genetic states without source-guessing.
- **No meta-analysis yet:** original 2022 and 2023/24 studies may share translocation seed-source lineages, investigators and geography. Distinct Zenodo files are not independent meta replicates.
- Do **not** convert the 6 literal F0 genotype matches, 38 unstratified recruit label overlaps, or 990 F1 fitness rows into 6, 38 or 990 independent genetic-rescue experiments.
- **Prior Arnica pilot:** 135 mothers / 6 source-site strata, HL-to-viable seed `r=-0.0185` and permutation `p=0.8341` (separate outcome family, not pooled with Campanula rosette growth).

**Gate:** freeze a genotype/offspring codebook and the correct biological unit before any outcome effect is estimated. Retain source and timing STOPs where needed.
