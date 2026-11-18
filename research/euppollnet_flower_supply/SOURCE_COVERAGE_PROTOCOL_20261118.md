# EuPPollNet independently counted flower supply: pre-effect source and biological-unit gate

**Date:** 2026-11-18. **Status:** outcome-blind *with respect to new flower-supply comparisons*, but designed **after** the positive guild JSD main result in PR #72. This is **post-primary exploratory source calibration**, NOT a new original preregistration or evidence of ecological function. This branch stacks on PR #72, not on `main`; it is empirical egwee, not theory egwe.

## Why

The existing wild-bee vs Syrphidae partition used 311 native networks from 39 source programmes, mean within-network hypergeometric-excess JSD +0.2323 nats. The null conditions on the pooled **observed visits**, not on independently observed standing flowers. Day- and shared-visited-host restrictions were also positive, but were post-primary and do not correct resource supply. The corrected author database contains a separate `Flower_counts.csv` (199,692 rows) explicitly connectable to the corrected 623,476 interactions via `Flower_data_merger`. Original article warns that flower measurement units and methods vary greatly across studies.

**First ask:** how often does a source-native bee–hoverfly network have actual independently counted, date-coincident standing flowers for the same identified plant taxa at the SAME study, network, year, and source-merger key, on a comparable flower-count unit?

## Pinned original sources and structural constraints

- `joseblanuza/EuPPollNet` original immutable commit `31716d21d5aad8c27c1d91dd0620149ef42e8836`.
- Interaction original `Data/3_Final_data/Interaction_data.csv.gz`: SHA256 `6e4e5399338d530462d8683b53a5e564d48e287e423be420c07d8046815ef38a`, **623476** rows, 30 source columns.
- Independent flower original `Data/3_Final_data/Flower_counts.csv`: SHA256 `aaf0474d42ca477e20db75205191f9e64fcd19f78c3e75ae3d66df77a1cefb0a`, **199692** rows, source fields `Study_id,Network_id,Day,Month,Year,Site_id,Plant_species,Flower_count,Units,Comments,Flower_data_merger`.
- Source native network: `Study_id × Network_id × calendar year`, with exact `Flower_data_merger` used as extra sampling-episode key. Study IDs 23/24/25 are one original study programme. Never treat plant flowers, visit rows, survey dates or multiple networks of a study as independent study programmes.
- Wild bees = the already frozen PR #72 family whitelist excluding Apis mellifera; hoverflies = Diptera Syrphidae. Structural candidate is >=20 visits from EACH guild, >=3 pooled plant taxa in an unambiguous method network; already 311 networks before new supply eligibility.
- For crosswalk, `Flower_counts.Plant_species` can be mapped to `Interaction.Plant_accepted_name` only through exact case/space normalized accepted match, or a **unique observed** `Plant_original_name → Plant_accepted_name` dictionary within that same network-year. A conflicting original-to-accepted relationship is excluded, never fuzzy-joined. The mapped plant must be in the interaction plant universe; no GBIF heuristic rescue at this stage.
- Required source tuple equality is exact normalized `Study_id,Network_id,Year,Flower_data_merger`. No broadcasting flower counts from one network to another or joining on proximity. Record independently the stricter **same calendar date** subset (interaction `Date` must match flower `Year,Month,Day` exactly); no inventing dates from blank cells.
- Flower_count must parse as finite nonnegative source count; missing, nonnumeric and negative data remain *unknown*, not zero. `Units` must be nonmissing and **identical normalized text within the relevant source network/sampling episode** to be considered homogeneous. This text homogeneity is necessary but not sufficient to establish comparable biological flowers (single flower vs inflorescence vs individual flower-plant counts).
- Multiple original flower observations for a taxon are retained as original sampling records. The **coverage gate** checks eligible source keys and mapped taxon coverage only, without using any cross-guild effect or regression.

## Locked source coverage outputs

Report aggregate counts only: source row and original digest checks; original-network and episode-key cardinalities; source merger missingness; keys overlapping counts and visits, time-matched keys; share of focal guild visit **records** on plant names with counted flowers; original study programmes with >=1 qualifying source network; distinct floral units and ambiguous mappings; valid positive/zero count incidence. No plant names, locations, taxon effects, original rows, visit identifiers or flower values uploaded.

A future *supply-referenced* comparison is **not allowed** unless at least 5 independent original programmes and 20 qualifying network×episode source units exist, with same-day coverage and a single recorded flower-count unit per source unit, >=3 positively counted and taxonomically matched plant taxa, >=20 observed focal-guild visits EACH on positively counted plant taxa, and >=70% of within-episode focal visits represented in the counted-taxonomy match for EACH guild. Only passing units may be considered, and inclusion rules cannot be relaxed after the first eligibility run just to obtain a desired effect.

If coverage passes, first separately lock a source-availability-aware estimand, validation of source sampling-effort and taxonomic rank, and site/programme cross-validation **before** calculating a flower-supply-related effect. The previous hypergeometric null alone is not evidence of supply-corrected floral preference.

## Claim ceiling

An observational use divergence and a flower-count crosswalk cannot identify floral choice, competition, fitness, compatible pollen, pollen quality or fragmentation causality. Sources vary in floral-unit definitions and exact survey hours. Q–P–F remains a separate unmet generalization goal; this gate may show why existing network macroecology can or cannot directly be converted into ecological functioning. This is a legitimate **coverage / comparability** result, not an attempt to force another positive biological effect or source outcome.

## Reproduction and storage

Source verification must fail closed on digest/key mismatch and download errors. Store only small derivative JSON/counts and the analysis script; do not redistribute original author rows or source downloads. No changes to PR #72 primary, historical five-cluster effects, LA005, PR #66, manuscript submission-ready decisions or theoretical egwe.
