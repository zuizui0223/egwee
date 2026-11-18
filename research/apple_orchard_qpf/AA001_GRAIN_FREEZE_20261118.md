# AA001 original apple cohort/experimental-grain freeze — before response inspection

2026-11-18. Stage A original Zenodo source validated by [workflow 44290503422](https://github.com/zuizui0223/egwee/actions/runs/44290503422), **before any numerical Q/P/F relationship was tested**.

Source original files and immutable SHA256:

| Source file | Raw rows | SHA256 |
|---|---:|---|
| TransectIN.txt | 390 | `9cf85041de39adbb50c881bd3236c7368eeb23f0a20c22e13b2b4c28d8851a09` |
| GerminatedPollen.txt | 1,061 | `69c12fd6744dcf5066c7ca08ddfc970f03565faf089721068a05a980d7897312` |
| initial_final_fruitset.txt | 816 | `2898dbeab9492d11b6a886373e82ce385d3e16a51c8163c402f8a30adad37ec0` |
| apple_weight.txt | 796 | `fdfc5b9923dc7047b62ca009875c5d068475cad3381e4baa7c6550d831618942` |

Original source: Riva et al. 2026, DOI 10.1016/j.scitotenv.2026.181767; Zenodo 10.5281/zenodo.19403906. Files are tab-delimited.

## Source-specific immutable column contracts

- Q: `Count, Visitors, Temp, Local_temp, Year, Region, Site`. This is *orchard/year visitor survey*, not treatment-inflorescence or individual flower visitors.
- P: `Nbr_germinated_pollen, Treatment, Temp, Region, Site, Plot, Inflo_ID`. **Year column absent**. Original primary Methods explicitly state the sampled styles were collected only **in 2023**. Year=2023 is a source-verified property of this P component, not an inferred year for any other file.
- F: `Initial_nb_fruit, Nb_Failure_Initial, Final_nb_fruit, Nb_Failure_Final, Treatment, Temp, Year, Region, Site, Plot`. Treat source numerator/denominator columns as separate source quantities. Valid final-fruit denominator requires a numeric, nonnegative pair with sum>0; do not interpret missing as zero.
- Secondary apple fruit weight: `Weight, Treatment, Temp, Year, Region, Site, Plot, Inflo_ID`. Different `Inflo_ID` entries in P versus apple weight DO NOT license same-inflorescence pair matching, because styles were excised, and source outcomes were measured on independently sampled floral material.

## Source grain and coverage rules before inspecting signed effects

1. Normalize `Region`, `Site`, `Plot`, `Treatment` by case/whitespace only. Orchard key is exactly **Region×Site**, not Site alone. Plot key includes original Region×Site×Plot.
2. Q key is **Region×Site×Year**. Only original source 2023 Q is an eligible stage-matched visitor summary for P 2023. No 2022 visits substituted.
3. P key is **Region×Site×Plot×Treatment×2023**. F key is **Region×Site×Plot×Treatment×Year**. The common experimental context is orchard-year-treatment, possibly same orchard-plot-year-treatment. A P style is destructively sampled and does NOT become a F-bearing inflorescence, so even if IDs coincide, P and F are independent flowers.
4. Allowed experimental treatment labels are source-authored `E, O, OH` (case-insensitive literal), meaning pollinator-excluded, natural open, open+supplemented cross-pollen. **Do not harmonize undocumented treatment synonyms post outcome**, or use excluded E flowers as observed visitor Q.
5. Stage B may examine categorical keys, treatment distributions, numeric validity/missingness flags and unique counts ONLY, not response magnitudes, signed group differences, correlations, or model coefficients. Never copy original row-level data, place IDs or treatment-level outcomes into GitHub.
6. Gate for a *later separately frozen*, orchard-context study: at least **12 distinct 2023 orchard keys** with Q, P and F in the same `O` treatment context, from >=3 original `Region` keys, at least **20 combined source orchard×plot×treatment overlaps** across those orchards, and valid source F final-fruit denominators. Otherwise STOP and document source grain.
7. A measured Q-P-F site-year correlation under this gate is observational and uses *distinct inflorescences*, even where matched orchard plots exist; it cannot be declared a third same-flower programme, estimate causal mediation, or infer a universal pollen-quality mechanism.

This is **Stage B source-only**; no signed ecological results are being claimed. Source original paper published climate×pollination associations already. No change to frozen egwee 5-cluster meta, QPF001/004, CropPol PR #78, EuPPollNet PR #72/#74 or theory egwe.
