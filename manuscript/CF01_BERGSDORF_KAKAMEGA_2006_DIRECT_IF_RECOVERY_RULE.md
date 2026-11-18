# CFTQ0349 / Bergsdorf Kakamega retrospective direct I-F recovery rule — 2026-09-27

## Programme

Programme identity: `P2_CF01_BERGSDORF_KAKAMEGA_2006`.

Primary source: Thomas Bergsdorf (2006), *Forest fragmentation and plant-pollinator interactions in Western Kenya*, PhD dissertation, Rheinische Friedrich-Wilhelms-Universität Bonn.

This is an explicitly **retrospective external recovery**. The dissertation's site tables and qualitative directions were visible before this rule was written. The purpose of the rule is therefore to make panel inclusion, endpoint definition, dependence and programme counting deterministic rather than to claim outcome-blind confirmation.

## Source design and claim ceiling

The dissertation samples named study sites distributed through the Kakamega main forest block and surrounding forest fragments.

Primary source condition:

- reference = source-labelled **main forest** study site;
- fragmented = source-labelled **surrounding forest fragment** study site.

Independent observational unit = **study site / locality**.

The reference sites are spatially separated localities inside one broad main forest block, whereas fragment sites occur in separate surrounding forest patches. This is therefore a **site/local-context observational contrast**, not a replicated experiment with multiple independent continuous-forest blocks. Later BIOTA work in the same Kakamega observatory network explicitly treated multiple main-block BDOs as reasonable site replicates because the main forest is structurally heterogeneous and split among management regimes, but the present recovery retains the narrower claim ceiling above.

Flowers, observation units, plants, stigmas, fruits and seeds are nested below site and never increase fragmentation n.

## Deterministic panel rule

The dissertation contains four focal plant species, with *Acanthus eminens* sampled in two campaigns.

A species×campaign panel is admitted to numerical recovery only when the public dissertation text exposes, for the same named sites:

1. a complete site-level standardized visitation-occurrence table;
2. a complete site-level mean fruit-set table;
3. at least two main-forest and two fragment sites in their intersection.

Every panel meeting those criteria is retained regardless of effect direction or significance.

Under the currently indexed dissertation tables this mechanically retains:

- *Acanthopale pubescens* — 2001;
- *Acanthus eminens* — 2002;
- *Acanthus eminens* — 2003;
- *Heinsenia diervilleoides* — 2002–2003.

*Dracaena fragrans* is not silently dropped because of its result. Its public indexed surface exposes grouped pollination levels but not the common site-level visitation and fruit-set vectors needed by this rule, so it remains **blocked/unrecovered** and contributes no numerical panel.

The four recovered panels are dependent outcomes inside **one Kakamega programme**. They can increase pair-specific direct I-F programme coverage by at most one.

## Locked I endpoint

Primary I = **standardized visitation-occurrence support at site level**:

`I_visit_occurrence = 1 - (source observation units with zero accepted-pollinator visits / all standardized observation units)`.

The accepted pollinator set follows the source's own biological filtering before this deterministic transformation:

- *Acanthopale pubescens*: honey bees (*Apis mellifera*), identified by the source as the most probable effective pollinator;
- *Acanthus eminens*: *Xylocopa* carpenter bees, identified by the source effectiveness tests as the pollinator group used in its visitation analysis;
- *Heinsenia diervilleoides*: all recorded visitor groups, because the source explicitly treats all groups as potential pollinators.

This endpoint uses the full source observation-unit denominator at each site. No visitor guild is changed after the fragmentation result is inspected.

## Locked F endpoint

Primary F = **source table mean natural fruit set at site level**.

The reported within-site SD and individual counts are provenance only. EGWEE constructs the fragmented/reference marginal effect from the set of site means, so the Hedges-g dispersion is the **between-site SD**, not the within-site plant SD printed in the dissertation table.

Seed set and pollen-on-stigma responses remain secondary biological context and cannot replace fruit set after seeing their directions.

## Common-frame rule

For each panel, use the intersection of named sites with both I and F.

The 2002 *Acanthus eminens* source fruit-set table includes Yala, but its 2002 source visitation table does not. Yala is therefore retained in the transcription as F-only provenance and excluded mechanically from the primary 2002 common frame.

No missing site is imputed.

## Direct effect representation

For each recovered panel:

1. form fragmented-site I values and main-forest-site I values;
2. form F values on the exact same sites;
3. calculate canonical EGWEE Hedges `g` for fragmented minus main forest;
4. use the frozen large-sample standardized-effect variance:
   `V(g)=1/n_fragment + 1/n_main + g^2/[2(n_fragment+n_main)]`;
5. higher I and F mean greater biological support/function, so no orientation sign reversal is needed.

## Within-panel dependence

For each common site frame:

1. group-center I and F within fragmented and main-forest conditions;
2. calculate Pearson `rho_IF` across the paired site observations;
3. set `Cov(g_I,g_F)=rho_IF*sqrt(V_I*V_F)`;
4. require finite positive marginal variances;
5. require the 2×2 working covariance block to be positive definite;
6. require positive `Var(g_I-g_F)`.

The covariance is a transparent paired-site working proxy, not an exact sampling covariance.

## Programme-level internal gate

The four species×campaign panels are dependent panels inside one programme and cannot increase K separately.

For descriptive within-programme layer separation:

- calculate one covariance-aware I-F p-value per recovered panel;
- set `p_programme=min(1, 4*min(p_panel))`.

This Bonferroni gate protects against selecting the strongest of the four visible recovered panels.

A successful programme admission increments **pair-specific direct I-F coverage by one** only. It does **not** modify the frozen Phase-1 five-cluster Fisher synthesis.

## Admission

Admit `P2_CF01_BERGSDORF_KAKAMEGA_2006` as one retrospective direct I-F programme only if:

- the source-transcribed site table reproduces the deterministic panel list above;
- every primary panel has at least two sites per habitat condition;
- all panel marginal Hedges-g effects are finite;
- every paired-site 2×2 covariance block is positive definite;
- site, not plant/flower/observation unit, remains the independent observational unit;
- *Dracaena* remains explicitly blocked rather than treated as a zero result.

## No-rescue rules

Do not:

- select only the panel with the smallest p-value;
- count species or years as independent programmes;
- use within-site plant SD as if it were among-site fragmentation variance;
- use flowers, observation units, plants, stigmas, fruits or seeds as fragmentation n;
- impute the missing 2002 Yala visitation value;
- substitute seed set or pollen deposition for fruit set after inspection;
- change source-defined pollinator groups after seeing results;
- claim independent replication of multiple continuous-forest blocks;
- add this programme to the frozen Phase-1 five-cluster Fisher synthesis;
- describe the recovery as prospective or outcome-blind;
- relabel the result as validation of an EGWE/NEE finite operator.

## Terminal outcomes

- `bergsdorf_direct_IF_four_panel_covariance_aware_retrospective`;
- `bergsdorf_panel_common_frame_not_reproducible`;
- `bergsdorf_panel_covariance_not_positive_definite`;
- `bergsdorf_site_unit_not_defensible`;
- `bergsdorf_Dracaena_site_frame_not_recoverable`.

All outcomes are retained.
