# UK PoMS 2017–2023: informative-event selection and effort audit result

**2026-11-17 · PR #60 · retrospective exploratory diagnostic, not a new confirmatory test**

## Source and reproducibility

- Frozen original two EIDC datasets and all uncompressed CSV SHA-256 member digests: \`SOURCE_ID_GATE_RESULT_20261117.md\`.
- Analysis specification **written after seeing the original primary result**: \`INFORMATION_GATE_DIAGNOSTIC_SPEC_20261117.md\`; no claim of prospective blindness.
- Implementation: \`audit_poms_information_gate.py\`, with a synthetic fixed-effects and effort-slope identity test.
- **CI PASS**: [run 44035889710](https://github.com/zuizui0223/egwee/actions/runs/44035889710), head \`81283296487553df71a6cc40be17de20d0ea0283\`, 1,000/1,000 successful whole-site bootstrap replicates for **each** of the two diagnostic models. Derivative-only [artifact 14306758491](https://github.com/zuizui0223/egwee/actions/runs/44035889710/artifacts/14306758491), no raw EIDC rows redistributed.
- This audit did **not** change the previously registered FIT−pan composition coefficient, the 972-event primary denominator, or the original 95% site bootstrap interval.

## Strict same-day information gate (95 independent source site keys, 7 years)

Of **1,221** exact site-date matched pan/FIT events, 972 (79.607%) had positive bee-or-hoverfly counts **in both channels** and contributed to the previous ratio-based primary analysis. The other **249** were unsuitable for a two-method log-ratio contrast.

| Mutually exclusive event category | Count |
|---|---:|
| Both methods record bee-or-hoverfly | 972 |
| Only pan channel has zero bee+hoverfly | 45 |
| Only FIT channel has zero bee+hoverfly | 172 |
| Both channels have zero bee+hoverfly | 32 |
| Total exact matches | 1,221 |

The pan-zero total is 77 (45+32), while the FIT-zero total is 204 (172+32). Those nonexclusive totals must **not** be added together as missing-event counts. Source-count field invalidity was zero. FIT records are ten-minute target-flower landing counts and pan records are multi-station passive traps; their different zero patterns are not proof of true insect absence.

## Is inclusion associated with measured pan-station flower incidence?

The same common exposure \`X\` was reconstructed for *all* 1,221 site-dates (mean **1.8403**, SD **1.1904** distinct flowering taxa per pan station, min–max 0–7). Mean \`X\` was **1.8271** among informative events and **1.8916** among zero-excluded events; the exposure mean shifts little.

An **equal-event, site/year/month fixed-effects linear probability diagnostic**, outcome \`R=1\` if both observation channels have positive bee+hoverfly totals, yielded:

| Retrospective R~Xz specification | Slope in probability points per SD | 95% whole-site bootstrap CI |
|---|---:|---:|
| Site/year/month fixed effects | +0.01128 | [−0.01524, +0.03285] |
| Add pan-station sample count and FIT count number | +0.01055 | [−0.01667, +0.03244] |

Neither interval excludes zero. Both fits used the same all-event exposure scale, all 95 sites, 2017–2023, and 1,000/1,000 successful site bootstraps (seed 20261118). **Interpretation:** there is no resolved *linear within-site association* between inclusion and the measured pan-flower incidence at this level of precision. This does **not** imply missing-at-random or exclude nonlinearity, unmeasured weather and target-flower selection, nor does it prove observation-method equivalence.

The proportion of informative matched events changed over calendar years: **0.876 (2017), 0.857 (2018), 0.829 (2019), 0.875 (2020), 0.830 (2021), 0.722 (2022), and 0.718 (2023)**. These are observed coverages, **not population trend estimates**. Counts are clustered, and calendar/site composition and weather or effort could differ.

## Decision for EGWEE

1. **Retain the original pre-registered result as unresolved**: FIT−pan \`delta=-0.05111\` with whole-site bootstrap interval **[−0.17227,+0.09449]**. Negativity in leave-one-site/year-out point estimates does not overrule the uncertainty interval.
2. The 249-event filter has now been made explicit and checked. Selection is **not clearly associated with the measured linear flower-incidence term**. It remains possible that unobserved site-day factors determine who enters the positive-pair frame.
3. The dominant same-day zero-event asymmetry is in the FIT channel (172 FIT-only zeros versus 45 pan-only zeros). This is a property of observation channels (and their unequal sampling protocol), not a mechanistic finding about bee/hoverfly ecological function.
4. Do **not** interpret the measured small and inconclusive differential as a missing gene–function link, biological fragmentation law, partner absence, or monitoring bias correction. Do not promote this exploratory selection result into a new paper lead.

## Literature boundary for the next source-level macro programme

The published 2026 PoMS analysis [doi:10.1002/2688-8319.70327](https://doi.org/10.1002/2688-8319.70327) already fits local flower richness and FIT floral-context covariates in survey-specific environmental models and compares survey-level temporal trends; it is **not safe** to claim that the concept of method-dependent flower effects is unprecedented. The [2024 PoMS annual report](https://ukpoms.org.uk/sites/default/files/PoMS-AR-2024-EN.pdf) already reported positive pan-flower-richness links for some bee groups and a FIT-target-flower patch-context association. [Westerberg et al. 2021](https://doi.org/10.1002/ece3.7252) established flower frequency/color effects on pan-trap catches.

A more general EGWEE paper needs **independent observation programmes**, directly comparable positive ecological functions, or independent source-level plant–pollinator link observations, not statistical significance rescue of a single UK PoMS pilot. The current evidence belongs as a traceable observation-channel calibration/measurement boundary.
