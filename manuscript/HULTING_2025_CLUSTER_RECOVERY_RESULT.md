# ML007 / PS014 Hulting 2025 recovery result

## Terminal state

`source_access_blocked`

No covariance-aware I/F effect was calculated.

## Prospectively locked design

Before raw outcomes were opened, the recovery contract fixed:

- one study-level experimental cluster, not five independent species studies;
- common exposure `edge_severity = -z(distance_from_edge)`;
- species-specific `I` = pollination rate;
- species-specific `F` = non-zero conditional total seed production per reproductive plant;
- original block > patch > patch-corner hierarchy;
- shared species/block dependence must be retained rather than assigning zero covariance.

## Public source structure

The Dryad record `10.5061/dryad.bnzs7h4mb` exposes two files:

- `archive_SRS_2009_seeds.csv` (664,907 bytes);
- `README.md` (8,434 bytes).

The public README documents one row per flowering structure (up to three structures per plant) and the fields needed for source-equivalent reconstruction: block, patch, patch corner, categorical distance from edge, species, structure/stalk number, viable and nonviable seed counts, patch type, reproductive state, plant dimensions, flowering-stalk counts, pre-dispersal seed predation and quality flags.

The paper states that one individual of each focal species was planted at each experimental location defined by block, patch/corner and edge-distance treatment. This makes a plant-level reconstruction structurally plausible while preserving the nested experimental hierarchy.

## Why the quantitative recovery stopped

The public raw CSV could not be retrieved from the CI environment. Dryad returned an Anubis JavaScript proof-of-work challenge at the file-stream boundary. No attempt was made to bypass that access control.

A second route through the Wiley supporting-information download endpoint returned HTTP 403 from CI. The article/search representation nevertheless identifies the supporting tables:

- Table S3 = Type III Wald-test results for species-specific pollination GLMMs;
- Table S4 = Type III Wald-test results for the species-specific seed-production hurdle models.

These tables test the edge term but do not, from the accessible representation, supply the signed edge coefficient plus SE/covariance needed for the locked meta-effect. Published nonsignificance of I therefore cannot be converted to effect = 0.

The main article does report exact percentage changes in non-zero seed production from 0 to 36.10 m for four species (Anthaenantia +135%, Aristida +240%, Sorghastrum +113%, Carphephorus +128%), with Liatris lacking the edge response. Those F summaries alone do not solve the missing quantitative I effect or cross-layer covariance.

## Biological information retained without promotion

The synchronized experimental study supports a qualitative state-separation pattern: edge proximity reduces reproductive output via flowering/seed production while pollination rate shows no detected edge response across all five species. This is useful biological evidence, but it is not promoted to the covariance-aware quantitative synthesis.

## Reopen condition

Reopen ML007 when the Dryad CSV is available through an ordinary browser/authorized download or an author-supplied copy. On reopening, preserve the already-frozen edge exposure, species set, I/F endpoints, hierarchy and dependence rules. Do not switch to patch type/connectivity or remove Liatris after seeing the raw effects.
