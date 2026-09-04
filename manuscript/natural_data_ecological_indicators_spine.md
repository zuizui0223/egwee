# Test the state before interpreting the residual: four empirical gates for ecological state indicators

**Status:** independent manuscript spine for the natural-data programme. This paper is not an EGWE warning-validity submission, does not validate the genetic warning rules, and does not pool heterogeneous natural systems into one ecological effect.

## Core claim

Ecological analyses often compress biological information into a state, proxy, or indicator and then ask whether geography, habitat, origin, or history explains what remains. That residual interpretation is only licensed if the proposed biological state has first earned endpoint-relevant predictive status and if its analytical representation preserves the information it claims to add. Across seven locked natural-data analyses, these upstream gates lead to different scientific outcomes: residual context can add no detected transferable information, a response-relevant coordinate can remain missing, a plausible proxy can fail measurement adequacy, preprocessing can erase a mechanistic distinction, and cross-study synthesis can remain non-identifiable.

The operational rule is:

> **Test the state before interpreting the residual.**

## Provisional abstract

Ecological indicators and state proxies are often treated as adequate summaries before their endpoint relevance has been demonstrated. Residual effects of habitat, geography, origin or history are then interpreted as evidence for missing ecological context. We argue that this order can invert the inferential burden. A residual-context claim is meaningful only after the biological state supplied first has passed separable tests of endpoint-relevant measurement adequacy and information-preserving representation. We formalise a four-gate workflow: measurement adequacy, representation preservation, residual-context testing, and cross-study identifiability. We apply the workflow to seven previously locked natural-data analyses spanning island and urban pollination systems, mating opportunity, pollinator proxies and interaction representations. The resulting branches are deliberately heterogeneous. In Honshu–Izu, Zurich and Toronto, added contextual variables produced no detected transferable held-out gain after the locked partial states. In *Oenothera harringtonii*, maternal spatial isolation improved held-out prediction, identifying a missing contemporary coordinate. In *Eschscholzia californica* and Mallorca carob, candidate pollinator proxies did not earn general endpoint-relevant state status under the frozen designs. In *Campanula americana*, feature-wise standardisation collapsed an intended effective-transfer distinction onto the simpler visitation representation. A cross-origin synthesis remained non-identifiable because study, origin, taxa, protocol and response construction were confounded. These outcomes do not support one common ecological effect. Instead they show why state measurement, representation and identifiability must be checked before residual context is biologically interpreted.

## 1. Introduction

### 1.1 The residual-context temptation

Ecological studies routinely construct compressed descriptions of a system: a pollinator interaction state, a connectivity index, a trait summary, an abundance proxy, or a functional state. A common next step is to add geography, habitat, urbanisation, origin or history and ask whether prediction improves. When it does, the residual variable is often treated as evidence that the original state was incomplete. When it does not, the original state can be treated—explicitly or implicitly—as sufficient.

Both conclusions can be premature. A residual variable cannot diagnose what the original state failed to measure if the proposed state itself has not earned endpoint-relevant status. Likewise, a biologically richer measurement can become analytically indistinguishable from a simpler proxy after preprocessing. The interpretation problem is therefore ordered: state measurement and representation come before residual context.

### 1.2 What is already known

Environmental and ecological indicator validation is not new. Existing frameworks distinguish design, output and end-use validation; ecological indicator suites are evaluated for relevance, robustness, redundancy and interpretability; predictive validation with held-out data is established; and analytical uncertainty is a recognised component of indicator reliability. Variable standardisation is also a standard statistical tool.

Our contribution is narrower. We connect those concerns in a fail-closed sequence that governs **what may be interpreted next**. The paper does not introduce a universal ecological indicator, a common effect size, or a new cross-validation algorithm.

### 1.3 Study objective

We ask whether seven locked natural-data analyses can be represented as distinct outcomes of one interpretation workflow without pooling incompatible systems. The four gates are:

1. endpoint-relevant measurement adequacy;
2. information-preserving representation;
3. transferable residual context;
4. cross-study identifiability.

A gate failure is not repaired after the result is known. `not_identifiable`, `not_estimable`, unsupported gain and archive STOP are retained as scientific outcomes.

## 2. Methods

### 2.1 General gate logic

The source of truth is `manuscript/natural_data_gate_registry.json`. All systems retain their frozen endpoint, candidate state/proxy, holdout unit, locked result and claim ceiling.

#### Gate 1 — endpoint-relevant measurement adequacy

A proposed biological state or proxy must improve or otherwise earn predictive status for the declared endpoint under the frozen held-out design before it is treated as an adequate state coordinate. Failure does not imply that the underlying biological process is irrelevant; it means the declared measurement has not earned that inferential role.

#### Gate 2 — representation preservation

If a richer biological measurement is intended to encode information absent from a simpler proxy, the analytical representation must preserve that distinction. A representation that maps both onto the same effective coordinate cannot support a claim that the richer state has been analytically supplied.

#### Gate 3 — residual-context testing

Only after the supplied state is interpretable do we ask whether geography, habitat, origin or history adds transferable held-out predictive information. A negative residual-context test is a conditional result. It does not prove complete state measurement and does not establish biological irrelevance of the contextual variable.

#### Gate 4 — cross-study identifiability

Cross-system synthesis requires the design to distinguish the comparison of interest from study, taxa, protocol, state construction and endpoint construction. If these are confounded, the synthesis returns `not_identifiable` or STOP rather than a pooled estimate.

### 2.2 Holdout discipline

The natural systems remain at their native resolution. Holdout units are whole sites, gardens, maternal plants, arrays, orchards or populations as locked in the original analyses. No observation-level random split is substituted after the fact.

### 2.3 No pooled ecological effect

The synthesis is logical, not meta-analytic. Error metrics, endpoints and biological coordinates differ among systems. Numerical results are reported within study on their native scales. Figure 2 encodes branch membership and locked outcome, not a common magnitude or severity ranking.

### 2.4 Fail-closed outcomes

Metadata mismatches, archive failures, `not_identifiable`, `not_estimable`, failed adequacy and unsupported residual gain are retained. No endpoint switching, proxy substitution, source repair, new scaling or post-result threshold search is opened by this manuscript.

## 3. Results

### 3.1 Residual context added no detected transferable information after locked partial states

#### Honshu–Izu

The functional partial state `TM_z + FDQ + FEve` had held-out MSE 1.08774. Adding mainland distance increased held-out MSE to 1.13209, a 4.08% worsening, and improved only 3 of 8 held-out sites. The locked interpretation is no detected transferable mainland-distance gain after the supplied partial state. This does not establish state completeness.

#### Zurich BetterBlooms

Across six fixed reproductive endpoints, none met the preregistered positive residual-context rule after the source-defined function-specific pollinator interaction state was supplied. The result supports no reproducible positive held-out gain from the locked local/urban context terms under the garden-holdout design.

#### Toronto community gardens

After a locked partial pollination/floral state, adding urban cover and green-space edge density increased total held-out NLL by 4932.9195; the garden-bootstrap 95% interval was [603.9654, 10953.6611]. The result supports no detected residual urban-context information under the frozen design, not a general claim of urban irrelevance.

### 3.2 A contemporary response-relevant coordinate remained missing

In *Oenothera harringtonii*, adding maternal spatial isolation after pollinator treatment reduced leave-one-maternal-plant-out MSE from 0.11619 to 0.09187, a 20.93% improvement; the locked permutation test gave p=0.00130. Spatial mating opportunity therefore remained a missing contemporary coordinate for the declared endpoint. The result does not establish a universal isolation law.

### 3.3 Candidate pollinator proxies did not earn general endpoint-relevant state status

#### *Eschscholzia californica*

The primary seed-function endpoint remained `multi_endpoint_not_identifiable` after the exact metadata gate detected `Fallow ground` versus `Fallow graound`. A prospectively permitted one-key sensitivity found the same mismatch at a second array and stopped before model fitting. Independently estimable mating and pollen-movement endpoints did not show reproducible held-out gain from the preregistered pan-trap count/mean-ITD state. The correct outcome is failed or unresolved measurement adequacy, not pollinator irrelevance.

#### Mallorca carob

Two non-identical deposited pollinator-abundance representations were mandatory. Their fruit-production gains were -0.10195 [-3.12202, 3.61919] and -0.09919 [-3.14415, 3.66453]. Neither earned endpoint-relevant process-measurement adequacy, so the residual-context gate was not opened.

### 3.4 Preprocessing erased an intended mechanistic distinction

For *Campanula americana*, none of the fixed interaction representations improved leave-one-population-out prediction of pollen limitation over the mean baseline. A response-firewalled diagnostic showed that the effective-transfer coordinates were constant positive rescalings of their phase-visitation coordinates. After feature-wise standardisation the paired predictors differed by at most 8.88e-16. The declared representation had therefore erased the efficiency multiplier that made the richer biological measurement distinct. No alternative scaling or endpoint rerun was opened.

### 3.5 Cross-origin convergence remained non-identifiable

The available origin comparison confounds origin with study, taxa, protocol, biological coordinate and response construction. A subsequent minimal multi-archive bridge stopped at automated archive access before schema mapping or outcome modelling. The locked result remains `cross_origin_convergence_not_identifiable_from_existing_archives`. This is a design boundary, not evidence for or against a shared urban–island law.

### 3.6 Six system-level branches did not license a stronger downstream inference

Table 1 makes the fail-closed consequence explicit. Here **unreachable under the frozen evidence** means that a stronger interpretation is not licensed by the existing data and analysis contract; it does not mean that the corresponding biological process is impossible. The six rows also did not stop for one common reason. Three reached the residual-context gate but a negative residual cannot certify state completeness; two stopped at measurement adequacy; and one lost its intended distinction at the representation gate.

| System | Furthest gate / locked result | Numerical or exact certificate | Stronger inference not licensed |
| --- | --- | --- | --- |
| Honshu–Izu | Residual context / no detected transferable distance gain | MSE 1.08774 → 1.13209 with distance; 4.08% worsening; 3/8 sites improved | The partial state is complete, or mainland distance is biologically irrelevant. |
| Zurich BetterBlooms | Residual context / no reproducible positive residual-context gain | **0/6** reproductive endpoints passed the preregistered positive rule | The interaction state is complete, or local/urban context is biologically irrelevant. |
| Toronto community gardens | Residual context / no detected residual urban-context information | Added context worsened held-out NLL by **4932.9195**, bootstrap 95% interval [603.9654, 10953.6611] | The supplied partial state is complete, or urban context is biologically irrelevant. |
| *Eschscholzia californica* | Measurement adequacy / primary endpoint not identifiable | Exact metadata mismatch `Fallow ground` versus `Fallow graound`, reproduced at a second array before primary model fitting | The pollinator proxy is an adequate seed-function state, or residual context can be interpreted after it. |
| Mallorca carob | Measurement adequacy / process measurement adequacy not earned | Two mandatory proxy gains: **-0.10195** [-3.12202, 3.61919] and -0.09919 [-3.14415, 3.66453] | Pollinator abundance is an endpoint-relevant state, or the residual-context gate may be opened. |
| *Campanula americana* | Representation preservation / mechanistic distinction erased | Standardised rich/simple coordinates differed by at most **8.88e-16**; no fixed representation beat the mean baseline | The richer effective-transfer state was analytically supplied as a distinct coordinate, or downstream residual context can be interpreted after it. |

*Oenothera harringtonii* is intentionally **not one of these six rows**. Its frozen result is a positive gate diagnosis: adding maternal spatial isolation improved held-out MSE by 20.93% (`0.11619` to `0.09187`; locked permutation `p=0.00130`), identifying a missing contemporary coordinate rather than producing a negative, failed-adequacy or representation-collapse branch. The cross-origin STOP is also kept separate because it is a synthesis-level identifiability boundary, not a seventh system-level row.

The table therefore does not count six replications of one effect. It records six distinct reasons why a stronger state or residual-context claim is not warranted. The machine-readable source is `manuscript/unreachable_six_systems.json` and is checked directly against `natural_data_gate_registry.json`.

## 4. Discussion

### 4.1 A negative residual is conditional evidence

The three line-1 systems do not show that distance, urbanisation or local habitat are generally unimportant. They show that, after the particular locked partial states and under their own held-out designs, the added contextual variables did not provide transferable predictive gain. This is a much narrower and more defensible inference.

### 4.2 State incompleteness and proxy inadequacy are different failures

The *Oenothera* result shows a missing coordinate that improves the declared endpoint. The *Eschscholzia* and carob results show something different: the candidate process proxy itself did not earn the right to stand in for the relevant state. Combining these as generic “context matters” or “pollinators matter” results would erase the inferential distinction.

### 4.3 Biological measurement is not the same as analytical representation

The *Campanula* case isolates a frequently overlooked step. A richer biological measurement can exist in the raw data yet disappear as a distinct predictor after transformation. The lesson is not to avoid standardisation. It is to verify that preprocessing preserves the biological distinction on which the state claim depends.

### 4.4 STOP is an outcome, not missing prose

The cross-origin result illustrates why a synthesis should sometimes terminate. If origin is inseparable from study and protocol, a pooled coefficient would answer an unidentified question. Preserving STOP keeps the inferential boundary visible and prevents heterogeneous archives from being converted into apparent replication by model specification alone.

### 4.5 Relation to ecological indicator validation

This paper does not replace established indicator-validation frameworks. It adds an ordered interpretation problem particularly relevant when a biological state proxy is followed by residual-context modelling. The four-gate workflow can be used as a reporting checklist: before interpreting residual context, state what biological measure was supplied, what endpoint it earned, whether its representation preserved the intended information, what holdout unit was used, and whether the requested synthesis was identifiable.

## 5. Claim ceiling

Supported:

- the four gate outcomes are empirically distinguishable in the locked natural-data analyses;
- residual-context interpretation is conditional on upstream state measurement and representation;
- fail-closed outcomes can determine what inference is authorised next;
- preprocessing can make a biologically richer raw measurement analytically non-distinct;
- six system-level branches identify specific stronger inferences that remain unreachable under the frozen evidence, for four different blocking reasons rather than one pooled failure mode.

Not supported:

- one pooled cross-system ecological effect;
- a universal urban, island, pollination or mating law;
- state completeness from a negative residual-context test;
- general irrelevance of distance, urbanisation, habitat or pollinators;
- predictive validity of the separate EGWE genetic warning statistic;
- a common origin effect from the existing archives;
- treating the six rows in Table 1 as exchangeable replications or as a severity ranking.

## Figure and table plan

**Figure 1.** Ordered four-gate interpretation diagram from `natural_data_figure_spec.json`.

**Figure 2.** Seven-system branch map showing candidate state, endpoint, holdout unit, gate reached and locked outcome. No pooled effect-size axis.

**Table 1.** Six system-level downstream-inference boundaries: furthest gate reached, exact/numerical certificate, and the stronger inference not licensed by the frozen evidence.

**Figure 3.** Optional within-study held-out contrasts, faceted by system and retained on native scales.

**Figure 4.** Optional *Campanula americana* representation-collapse diagnostic before and after standardisation.

## Literature anchors for the full draft

The complete draft should explicitly position itself relative to environmental/ecological indicator validation, rigorous proxy selection, predictive validation, indicator uncertainty, redundancy/contradiction among indicator suites, and standardisation. The current novelty firewall is recorded in `NATURAL_DATA_NEAREST_NEIGHBOR_AUDIT_2026-09-01.md`.
