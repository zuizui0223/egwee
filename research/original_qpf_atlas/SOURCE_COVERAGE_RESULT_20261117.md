# Original Q–P–F source atlas — independent-unit coverage result (2026-11-17)

**Status:** original-public-source *feasibility/ID-join audit only*, without testing a reproductive or ecological effect. Separate from the frozen EGWEE five-cluster effects, PR #52, PR #63, natural genetic-fitness studies, and theory egwe.

## Research decision

The observed weakness in the current fragmentation evidence is not simply insufficient marginal effect sizes: original data rarely align **visit quantity Q**, **direct transfer/provenance P**, and **seed/fruit function F** at the same site/plant/year with measured observation effort. Our prospective six-source Dryad screen and independent availability follow-up verify this distinction without selecting on outcome direction.

### A. Six pre-outcome registered source programmes

Source list, DOI, context and strict grain constraints were committed before the numeric outcome or raw-data inspection at [source lock](PROTOCOL_SOURCE_LOCK_20261117.md) and [registry](SCHEMA_SOURCE_REGISTRY_20261117.json).

- The six public Dryad DOIs resolved to **6/6 official dataset metadata records** and file inventories for five sources.
- **17 whitelisted files**, **0 successfully downloaded** through the source API advertised file routes in Actions. Five programmes returned **HTTP 401** on original file streams (QPF001–005); QPF006 metadata resolved but a further version/file metadata request returned **HTTP 429**. A 401 on this route is **not** proof that the originally published dataset is private or biologically unusable; a 429 is a rate-limit/access response, **not** a DOI mismatch.
- **0 original sheet headers**, **0 verified same-cohort Q+P+F joins**, **0 new original-observation effects**. All were correctly flagged as access/verification STOP, never invented as negative biology.
- Source candidate semantics still matter: *Argentina anserina* 2024 and the registered 2025 genetic-mating paper share the original 13-population frame; the source paper itself already tested N_E × visitation and pollen quantity vs quality. *Brassica carinata* 2026 measures visits and seed production at 35 sites, but its published Methods explicitly state **direct pollen transfer was not measured**; fields labelled sp/dp cannot be silently treated as genetically compatible pollen provenance.

Evidence: source-only CI [run 44102620895](https://github.com/zuizui0223/egwee/actions/runs/44102620895), [downloadable derivative metadata receipt](https://github.com/zuizui0223/egwee/actions/runs/44102620895/artifacts/14335904403); [original field-compatibility article](https://doi.org/10.1098/rspb.2023.1519); [original carinata article](https://doi.org/10.1111/1365-2664.70495). The 2024 dryad source and its content are independent *data publications*, not independent population samples versus the cited companion field/mating paper.

### B. Direct public GitHub original-observation source follow-up (not in the frozen six)

Because the official Dryad API file streams were unavailable, a **separate access-driven, not outcome-driven** source feasibility audit used the public authors' [urban pollinator metacommunity repository](https://github.com/jensculrich/urban_pollinator_occupancy_model) and immutable commit `4f0b9d53b4901337e441d2d1dae0f2b31c6e8280`. This source is **not counted** toward the frozen initial six, and no outcomes or regressions were inspected.

Three source-matched dimensions:

| Original source component | Source structural audit |
|---|---:|
| Urban landscape sites in published site table | **18** |
| Flower-level *Clarkia amoena* seed/pollen-supplementation experiment entries (2022) | **528 rows**, **11 sites** |
| Structurally complete control+supplement pairs: both flowers opened/applied and capsules recovered | **188 candidate plants**, **11 sites** |
| 2022 original field flower-visitor detection rows (all host plants, not normalized by detection effort) | **3,029** |
| 2022 field floral visitor rows for *Clarkia amoena* (any round) | **0** |
| 2022 field floral visitor rows for **any Clarkia genus** (any round) | **0** |
| Separate *Clarkia* visitation file | **41 records at only one site label: common garden** |
| Exact field site overlap of common-garden visitation records with 11 reproductive sites | **0** |

The seed data have an original paired supplementation experiment that may be useful for testing pollen limitation, but **not** a field-specific, observed *Clarkia* visitor time series at any of the 11 reproductive sites. Other-flower pollinator captures are **community presence proxies**, not visitation to these focal reproductive plants; source counts also have no verified per-plant observation effort denominator. This source therefore does **not** qualify for the preregistered direct Q→F or Q→P→F transfer test.

The **188 is a structural candidate count only**. Source seed values were deliberately unopened; true numeric eligibility (missing seed values, treatment interpretation, zero supplementation) was not checked. Flowers and plants cannot be promoted to 188 independent landscape replications.

Source script [audit_public_clarkia_qf_keys.py](audit_public_clarkia_qf_keys.py) verifies the exact original Git blob SHA for all four public files, counts treatment pairing and field-site/genus cross-coverage, and never reads seed-count values. Run [44102659017](https://github.com/zuizui0223/egwee/actions/runs/44102659017) passed with provenance/quality gates. No third-party source rows are committed to EGWEE.

## What was learned and how it changes the research

1. **Missing transfer information is an independently verified data alignment problem**: recording visit abundance somewhere in a programme does not mean it can be assigned to exactly the same flower, date, or reproducing maternal unit.
2. Even a design with **11 study sites** and **188 paired individual reproductive treatments** provides **0 directly linked focal-flower visits** in the uploaded urban field visitation records. This is *structural infeasibility for this particular published source*, **not** evidence that pollinators are ecologically unimportant or that seed set is unrelated to visits.
3. The external 2024 *Argentina* 13-population paper already identified a genuine positive phenomenon: effective population size modified how visitation was translated into pollen quality and reproductive performance. It cannot count as an EGWEE-discovered replicated mechanism, but helps specify a falsifiable alternative (effective partner provenance and maternal/mating context).
4. The 2026 carinata field work documents pollinator composition/management-dependent yield and per-visit effects, but it does not identify compatible pollen transport. It can supply a context-dependent Q→F replication **if its original plant/site observations become accessible and source effort is verified**, not Q→P→F.

**Next source-selection priority:** seek DOI/Zenodo/author-linked original tables with *simultaneous, same maternal site-year* conspecific/heterospecific stigmatic deposition or tube success and paired natural seed output, plus focal visitation and survey effort. Require at least 3 independent such programmes for a macro prediction. Another site-only pollinator fauna database or generic PL meta table must not be auto-joined by geography. Failure to obtain the qualifying coverage remains a STOP, not reason to switch to an already published effect direction.

## Scientific interpretation ceiling

No new ecological effect or mechanism was statistically confirmed in this source atlas. We have executed and reproduced **a strong source-coverage and false-join falsification**, with two independent validation workflows. This directly protects the earlier three matched I–F mismatches from being reinterpreted as a universal hidden-pollen mechanism without same-unit measurement.

Execution:
- Six-source official Dryad metadata/header gate: [44102620895](https://github.com/zuizui0223/egwee/actions/runs/44102620895).
- Four-file source-hashed original Clarkia structural gate: [44102659017](https://github.com/zuizui0223/egwee/actions/runs/44102659017).
- Frozen six registered source list and protocol are unchanged after source outcomes remained unopened.
- No biological outcome, original genetic or reproductive values, original zipped raw files, 5-cluster effect-size estimands, manuscript conclusions or submission-ready flags changed.
