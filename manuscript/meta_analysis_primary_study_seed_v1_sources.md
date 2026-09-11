# Primary-study seed corpus v1 — provenance

Status: source-verified screening seed for the active EGWEE multilayer fragmentation meta-analysis. This file is not a fitted meta-analytic result.

## Purpose

`meta_analysis_primary_study_seed_v1.csv` records primary studies for which the publication-level source already supports at least two biological response layers relevant to the locked EGWEE protocol. Inclusion here means **screening priority**, not automatic inclusion in the final effect-size model.

## Verified high-priority direct contrasts

### PS001 — *Spondias purpurea*

Cristóbal-Pérez et al. (2021), *Biological Conservation* 256:109007. DOI `10.1016/j.biocon.2021.109007`.

Direct continuous-versus-fragmented comparison. The same paper reports pollinator visitation, fruit set, paternity-derived pollen flow, correlated paternity/effective sire number, and adult/seed/juvenile genetic responses. This is the strongest synchronized seed for `I + C + F + G_adult + G_offspring`.

### PS004 — *Brosimum alicastrum*

Aguilar-Aguilar et al. (2023), *American Journal of Botany* 110:e16157. DOI `10.1002/ajb2.16157`.

Three continuous and three fragmented forest sites. The paper evaluates population/sex structure, pollen-distance gene flow, genetic diversity and mating, plus early progeny vigour. High-priority `D + C + F + G_adult + G_offspring` seed.

### PS014 — replicated fragmentation experiment

Hulting et al. (2025), *Journal of Ecology*. DOI `10.1111/1365-2745.14452`.

Replicated experimental connectivity/edge design across five planted species, with flowering, pollination rate and seed production. High-priority `D + I + F` seed.

## Verified multilayer gradient studies

### PS002 — *Magnolia stellata*

Suzuki, Nagamitsu & Tomaru (2013), *BMC Ecology* 13:10. DOI `10.1186/1472-6785-13-10`.

Six adjacent fragmented populations. Reports population structure, paternity-derived pollen flow, selfing, female seed-production success and male reproductive success. Because the source is primarily a population-structure gradient, it belongs in the Fisher-z / continuous-exposure stream unless a pre-existing binary contrast is explicitly available.

### PS003 — *Serapias lingua*

Pellegrino, Bellusci & Palermo (2015), *BMC Plant Biology* 15:222. DOI `10.1186/s12870-015-0600-8`.

Nine fragmented subpopulations. Reports microsatellite genetic diversity/differentiation, paternity pollen flow, clonality and fruit production. Treat as a gradient study unless the original design supplies a non-post-hoc categorical contrast.

### PS012 — *Tillandsia intermedia* / *T. makoyana*

DOI `10.1093/aobpla/ply038`.

Continuous-versus-fragmented forest comparison over three years, including floral-visitor composition/visitation and female reproductive success. Useful same-study `I + F (+R)` pair.

### PS015 — *Conospermum undulatum* interaction / pollen-quality gradient

Delnevo et al. (2020), *Biological Conservation*. DOI `10.1016/j.biocon.2020.108824`.

Across eleven remnant populations, specialist native bee visitation increased with floral display/connectivity, while small isolated populations lacked part of the effective pollinator fauna and showed stronger pollen-quality limitation. This is a high-priority same-study `D + I + T + F` gradient and fills the contemporary interaction layer between the 2019 reproductive study and the later adult-genetic / paternity studies.

## Programme-level anchors that must remain split by publication/year

### Miyake *Camellia japonica* programme

- Abe & Hasegawa (2008), DOI `10.1007/s11284-007-0345-4`: local floral support, pollination and reproductive function.
- Abe et al. (2013), DOI `10.1371/journal.pone.0062696`: pollen flow and seed-generation genetics.

These are mechanistically linked but not one synchronized study-year. They may share a programme ID, but their effect sizes must remain separate.

### Montpellier *Crepis sancta* programme

- Cheptou & Avendaño (2006), DOI `10.1111/j.1469-8137.2006.01880.x`: density, pollinator activity, reproductive assurance and seed set.
- Dornier & Cheptou (2013), DOI `10.1038/hdy.2013.3`: contemporary pollen/seed dispersal and immigration.

Do not row-join across campaigns.

### Perth *Conospermum undulatum* programme

- Delnevo et al. (2019), DOI `10.1002/ece3.5653`: population/floral support and reproductive function.
- Delnevo et al. (2020), DOI `10.1016/j.biocon.2020.108824`: pollinator visitation/effectiveness and pollen-quality limitation across eleven remnants.
- Delnevo et al. (2021), DOI `10.1007/s10531-021-02256-x`: adult genetic structure and historical connectivity.
- Delnevo et al. (2026), DOI `10.1002/ece3.73406`: contemporary offspring paternity and pollen flow.

These studies intentionally represent different temporal/cohort/process layers and must not be collapsed into one row-level effect. The 2026 paper's adult-genetic context overlaps the standing adult cohort reported in the programme and is linked rather than counted as a new independent adult-genetic effect.

## Partial comparator seed

### PS013 — *Pistacia lentiscus*

Albaladejo et al. (2012), *PLOS ONE* 7:e49012. DOI `10.1371/journal.pone.0049012`.

The paper measures pollen movement, donor diversity, reproductive variance, adult genetic diversity and spatial genetic structure in a highly fragmented landscape, while some continuous-population comparisons come from an earlier study. It is therefore a valuable multilayer candidate but not yet a clean same-study direct contrast.

## Seed syntheses used for expansion

The primary-study search is seeded from, but does not double-count, existing syntheses:

- Aguilar et al. (2024/2025), DOI `10.1093/aob/mcae076`: pollination + male/female fitness; 235 female-fitness publications, 79 male-fitness publications, with 83 pollination effect sizes from 75 species among reproductive studies.
- Olhnuud et al. (2025), Dryad DOI `10.5061/dryad.dz08kps9p`: pollinator abundance/richness fragmentation dataset; 63 publications for richness and 40 for abundance.
- Aguilar et al. (2019), DOI `10.1111/ele.13272`: progeny genetics and vigour across 179 species.
- González et al. (2019), DOI `10.1111/cobi.13422`: plant genetic-diversity fragmentation/degradation synthesis with public Figshare data.
- global FSGS synthesis (2023, AoB PLANTS `plad019`): supporting Table S1 lists 65 reviewed studies and 31 meta-analysed studies.

Prior syntheses are search frames and data-index sources only. A primary study appearing in multiple syntheses is one sampling unit, with dependence handled at study/species level.

## Screening ceiling

No study in this seed file is declared final-included until the locked protocol checks exposure definition, extractable effect/variance, cohort identity, duplicate reports, compatible directionality, and dependence structure.