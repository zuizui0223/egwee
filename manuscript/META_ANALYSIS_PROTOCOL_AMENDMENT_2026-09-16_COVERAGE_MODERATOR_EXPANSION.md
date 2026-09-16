# Protocol amendment — systematic coverage and moderator expansion

**Frozen development date:** 2026-09-16  
**Parent protocol:** `manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md`  
**Current Stage-A synthesis commit:** `16308cf6d6e4aec274504ba81bbf6e71be465099`

## 1. Purpose

This amendment reopens the **uncompleted coverage and moderator programme already declared in the 2026-09-11 protocol**. It does not reopen the completed five-cluster Fisher result for significance repair.

The current Stage-A paper asks whether the available direct multilayer corpus contains evidence against complete within-system layer exchangeability. It contains five independent direct programme/study clusters, 17 marginal Hedges-g effects, and one separately analysed Fisher-z gradient cluster. That result and its leave-one-cluster-out and covariance-robustness boundaries remain frozen.

The Stage-B question is different:

> **How large are cross-layer fragmentation-response differences in natural plant systems, which layer pairs diverge, and which independently measured biological conditions predict concordant versus decoupled response geometry?**

The scientific target is therefore **coverage and moderator identification**, not a smaller Fisher p-value.

## 2. Firewall from the completed Stage-A result

1. The five-cluster Stage-A Fisher statistic, cluster p-values, leave-one-cluster-out results and covariance-sensitivity results remain historical/frozen estimates.
2. A newly recovered system is **not appended to the Stage-A Fisher test** merely to change its significance.
3. No sixth-cluster search is defined by the criterion "does omit-ML001 become significant?".
4. Stage-B candidates are registered because they expand a predeclared response-layer pair, moderator stratum, taxonomic/life-history stratum, or study-design stratum.
5. All candidates found in a declared search source/window are registered before their cross-layer effect direction or separation p-value is used for prioritisation.
6. Existing outcome-visible closed candidates may be reopened for data recovery, but their inclusion is governed by the same effect-unit and exposure rules as all other candidates. Their known direction cannot be used to define a confirmatory moderator category.

## 3. Systematic candidate universe

Stage B constructs a source-defined candidate universe from the complete primary-study lists or deposited datasets of six seed syntheses, followed by forward/backward citation searching through **2026-09-16**:

1. Aguilar et al. 2006, *Ecology Letters*, `10.1111/j.1461-0248.2006.00927.x` — plant pollination/reproductive response to fragmentation (`I`, `F`).
2. Aguilar et al. 2008, *Molecular Ecology*, `10.1111/j.1365-294X.2008.03971.x` — plant genetic consequences of fragmentation (`G_adult`, mating/genetic endpoints).
3. Aguilar et al. 2019, *Ecology Letters*, `10.1111/ele.13272` — progeny genetic and biological quality across 179 plant species (`G_offspring`, progeny performance/function).
4. Miguel-Peñaloza et al. 2023, *AoB PLANTS*, `10.1093/aobpla/plad019` — systematic FSGS corpus (65 review studies; 31 meta-analysed studies), including pollination/seed-dispersal metadata (`G_adult`, dispersal moderators).
5. Aguilar et al. 2025, *Annals of Botany*, `10.1093/aob/mcae076` — hierarchical synthesis of pollination and male/female fitness under land-use change, mainly habitat loss/fragmentation (`I`, `F`, compatibility system, pollination vector).
6. Olhnuud et al. 2025, *Journal of Applied Ecology*, `10.1111/1365-2664.70161`, Dryad `10.5061/dryad.dz08kps9p` — 80-study insect-pollinator fragmentation corpus with study-level habitat/fragmentation metadata; used as a candidate-discovery source for plant systems with independently recoverable plant response layers, not as automatic plant-study inclusion.

A study appearing in multiple seed syntheses is one candidate record after deduplication by DOI/title/species/system/campaign. A synthesis-level effect is never treated as an independent primary plant system.

## 4. Outcome-blind registration sequence

For every discovered candidate, record before extracting or calculating cross-layer effect values:

- bibliographic identity and source synthesis/source route;
- plant species/system and campaign year;
- fragmentation exposure definition;
- independent fragmentation unit frame;
- response layers apparently available (`D`, `I`, `C`, `F`, `G_adult`, `G_offspring`, `T`);
- direct two-group versus continuous-gradient design stream;
- whether the same exposure/unit frame can support at least two layers;
- public-data/recoverability status;
- predeclared moderator metadata available without using the response outcome.

Only after this registration may numeric outcome extraction begin.

## 5. Stage-B primary estimands

### 5.1 Layer-pair contrasts

For direct two-group effects retain the parent-protocol Hedges-g orientation. For every system with two eligible layers `a` and `b`, define

`Delta_s,ab = g_s,a - g_s,b`

with

`V(Delta_s,ab) = V_s,a + V_s,b - 2 Cov_s,ab`.

These **layer-pair differences**, rather than cluster p-values, are the primary Stage-B effect sizes.

Predeclared layer-pair families are:

- `I - F`;
- `C - F`;
- `C - G_adult`;
- `C - G_offspring`;
- `F - G_adult`;
- `F - G_offspring`;
- `G_adult - G_offspring`;
- `D - I`, `D - F`, and `D - G` when coverage permits.

A mating/genetic endpoint whose biological meaning does not map cleanly to `G_adult` or `G_offspring` remains an explicit subtype (for example `G_mating`) rather than being silently reassigned.

### 5.2 Model hierarchy

The intended Stage-B model is the multilevel random-effects structure already declared in the parent protocol, with study/programme/species clustering and reconstructed sampling covariance where defensible. Cluster-robust inference is the fallback when sampling covariance cannot be reconstructed.

The direct and continuous-gradient effect families remain separate. No Hedges-g/Fisher-z conversion is introduced by this amendment.

## 6. Moderator hypotheses

The following hypotheses are frozen before Stage-B outcome synthesis.

### H-B1 — cohort/history lag

Adult standing genetic state should be more weakly coupled to contemporary `I/C/F` responses than offspring/juvenile genetic or mating state when fragmentation is recent relative to generation time. Primary moderator variables are life form/longevity, time since fragmentation, and cohort.

### H-B2 — reproductive assurance buffers `I -> F` coupling

Where autonomous reproductive assurance is independently demonstrated, or where a pre-outcome compatibility category indicates reduced dependence on pollinator-mediated outcrossing, a decline in interaction support may translate less directly into reproductive-function decline. `Compensated` is **not** defined from the observed `F` response.

### H-B3 — movement/vector biology alters cross-layer coupling

Pollination vector (invertebrate / vertebrate / abiotic / mixed), process-specific movement measurement, and fragmentation component (area / isolation-connectivity / composite) may alter `I-F`, `C-F`, and `C-G` coupling. Pollination-vector classes are assigned from source biology, never from the observed effect size.

### H-B4 — direct process measures are more informative than proxies

Direct pollen movement, realised visitation/pollen receipt, or explicitly measured propagule movement may show different coupling to downstream function/genetics than habitat-distance or structural proxies. `direct_process_measurement` is fixed from methods, not from predictive performance.

## 7. Model-activation gates

These are **identifiability/precision gates**, not significance thresholds.

- A layer-pair pooled Stage-B estimate may be promoted from descriptive to model-based when at least **5 independent systems/programmes** provide that pair.
- A one-variable categorical moderator test requires at least **10 independent systems/programmes** with non-missing moderator data and at least **4 systems in each compared category**. Categories failing this gate are reported descriptively or collapsed only according to a pre-outcome biological rule.
- A one-variable continuous moderator test requires at least **10 independent systems/programmes** with non-missing values and non-degenerate support.
- A model containing more than one substantive moderator requires at least **20 independent systems/programmes** and at least 5 independent systems per estimated categorical parameter level; otherwise moderators are analysed one at a time.
- A phylogenetic random-effect analysis requires at least **20 independently represented species** with reproducible phylogenetic placement and remains a sensitivity analysis unless this gate is met before fitting.

No model is activated because a smaller dataset happens to produce a favourable p-value.

## 8. Existing closed-candidate recovery lane

Recovery priorities are based on **missing layer-pair coverage and structural recoverability**, not known outcome direction.

### Tier A — high coverage value if source data become recoverable

- `ML006 Primula elatior`: `I/F/G_adult` on the frozen common 15-population frame; potentially adds `I-F`, `I-G_adult`, `F-G_adult`.
- `ML007 Hulting fragmentation experiment`: `D/I/F`; potentially adds the first replicated `D` pair geometry and another `I-F` system.
- `ML008 Tillandsia`: `I/F`; potentially independently replicates the currently sparse direct `I-F` family.
- `ML012 Dieffenbachia seguine`: `C/G_mating`; potentially expands movement-to-genetic/mating coupling.
- `ML010 Penstemon hirsutus`: `C/G_offspring`; potentially expands movement-to-offspring-genetic coupling.
- `ML005 Conospermum 2026`: `C/G_offspring`; reopen only with the exact locked exposure and legitimate genotype bytes.
- `ML011 Magnolia stellata`: `C/F`; expands process-function coupling.
- `ML004 Conospermum 2020`: `I/T/F`; adds `I-F` plus partner-trait context if the same 2020 frame is recovered.

### Tier B — within-cluster layer completion

These do not increase the number of independent systems but improve response geometry within an already admitted system:

- `ML002 Brosimum`: recover `G` only if genotype summaries reconcile under the existing QA contract.
- `ML003 Spondias`: recover `I/F` only with author/raw-data release under the same five-site frame; do not digitise figures or substitute published significance for effects.

### Structural closures

`ML009 Pistacia` and `ML013 Swietenia` remain structurally non-identifiable for the binary fragmentation estimand unless genuinely additional independent landscapes/reference populations become available. Lower-level mothers, progeny or loci may not be promoted to fragmentation replicates.

## 9. Stage-B search stop

Stage-B search stops when all declared seed-source primary lists plus forward/backward searches through 2026-09-16 have been screened and every candidate has a terminal registration state. It does **not** stop when a desired moderator or layer-pair p-value crosses 0.05.

A future extension beyond this date requires a new dated amendment specifying the added bibliographic window or biological coverage target before new outcomes are inspected.

## 10. Reporting contract

The completed Stage-A Journal of Ecology package remains a valid frozen analysis snapshot. Stage B may ultimately produce a revised/expanded manuscript only if the systematic candidate universe materially increases the inferential target from global exchangeability testing to layer-pair estimation and moderator analysis.

If Stage-B coverage gates are not met, the current five-cluster **conditional state-separation** paper remains the publication endpoint; failed expansion is reported as an evidence-availability boundary rather than repaired by lowering model-activation thresholds.
