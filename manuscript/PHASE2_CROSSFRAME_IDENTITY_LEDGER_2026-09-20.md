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
- probable same-publication groups after species-name agreement/tiny spelling tolerance: **6**;
- ambiguous same-author/year groups with discordant species: **4**.

The six probable duplicate groups are:

- Bartlewicz 2015;
- Collevatti 2014;
- Browne 2015;
- Giombini 2017;
- Pellegrino 2015;
- Lompo 2020.

They are **not yet collapsed automatically**. Full citation/DOI confirmation remains required.

The four ambiguous collisions (Chung 2007, Jacquemyn 2006, Jacquemyn 2009, Zhao 2009) remain separate unless later source metadata proves identity.

## Existing EGWEE firewall

Known records already belonging to an admitted or declared Phase-2 programme are explicitly linked so they cannot be recruited again as independent evidence. Examples include:

- Farwig et al. 2008 → `P2_CF01_GPAIR_003`;
- Pellegrino et al. 2015 → `ML001`;
- Aizen & Feinsinger 1994 → `ML020`;
- Cristóbal-Pérez et al. 2021 → `ML003`;
- Lompo et al. 2020 → `P2_SF05_93`.

The identity ledger therefore advances systematic coverage by separating **new screening records** from **known-programme rediscoveries** before effect extraction.

## Next operation

Resolve the six probable cross-frame duplicate groups by full citation/DOI, then apply the same existing-programme crosswalk to all 358 rows. After identity resolution, title/abstract/method screening can proceed on unique programmes rather than duplicated source-frame rows.
