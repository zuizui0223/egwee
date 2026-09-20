# Phase-2 cross-frame publication identity ledger — 2026-09-20

## Scope

This ledger combines the currently row-materialized, outcome-blind publication identities from **SF04, SF05 and SF06** before any additional numerical effect extraction.

- SF04: **38** publication rows;
- SF05: **65** source-selected study rows;
- SF06: **255** publication rows;
- combined source-frame rows: **358**.

No treatment/control outcome value is added by this crosswalk.

## Duplicate discovery

A conservative two-stage identity rule is used.

1. DOI/full-citation identity is required before records are collapsed.
2. First-author + year is used only to find records requiring review.

Across the 358 rows:

- unique first-author/year keys: **336**;
- cross-frame author/year candidate groups: **10** containing **20** rows;
- heuristic same-publication candidates from species agreement: **6**;
- heuristic ambiguous author/year collisions: **4**;
- after full source-citation resolution: **7 confirmed duplicate groups** and **3 confirmed distinct collisions**.

Confirmed cross-frame duplicates are:

- Bartlewicz 2015;
- Collevatti 2014;
- Browne 2015;
- Giombini 2017;
- Pellegrino 2015;
- Lompo 2020;
- Zhao 2009.

Zhao 2009 is important: the source-frame species labels disagree (`Glycine soja` versus `Glycine_max`), but both records identify the same *American Journal of Botany* 96:1138–1147 publication. Citation identity therefore overrides the species-field discrepancy.

The three confirmed distinct same-author/year collisions are Chung 2007, Jacquemyn 2006 and Jacquemyn 2009; their journals/species/source citations differ and they remain separate.

Collapsing only the seven confirmed duplicate pairs reduces **358 source-frame rows to 351 screening identity units**. Of those, **5** are already linked to known EGWEE programmes, leaving **346** identities not yet linked under the current firewall.

## Existing EGWEE firewall

Known records already belonging to an admitted or declared Phase-2 programme are explicitly linked so they cannot be recruited again as independent evidence. Examples include:

- Farwig et al. 2008 → `P2_CF01_GPAIR_003`;
- Pellegrino et al. 2015 → `ML001`;
- Aizen & Feinsinger 1994 → `ML020`;
- Cristóbal-Pérez et al. 2021 → `ML003`;
- Lompo et al. 2020 → `P2_SF05_93`.

The identity ledger therefore advances systematic coverage by separating **new screening records** from **known-programme rediscoveries** before effect extraction.

## Next operation

Use the 351 canonical identity units—not 358 source-frame rows—as the denominator for the next title/abstract/method screen. Expand the existing-programme crosswalk before any new effect extraction, then screen unresolved identities for prespecified multilayer geometry.
