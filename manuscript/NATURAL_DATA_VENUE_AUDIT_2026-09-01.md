# Natural-data four-gate venue audit — 2026-09-01

## Publication recommendation

### Primary target — Ecological Indicators

Best current fit for the manuscript in its present scientific form.

Reasoning:

- the paper evaluates whether proposed biological state measurements earn endpoint-relevant indicator/state status before residual context is interpreted;
- the central contribution is measurement/indicator validity and monitoring-assessment logic, not a new ecological effect shared across taxa;
- the natural datasets provide direct ecological/environmental observations rather than only simulations;
- negative, unsupported, `not_identifiable`, `not_estimable`, and STOP outcomes can be treated as outcomes of indicator-evaluation gates rather than forced into one pooled effect size;
- the paper can end with a reusable evaluation workflow for ecological state indicators while retaining the heterogeneous empirical demonstrations at native resolution.

Recommended framing:

> **Test the state before interpreting the residual: four empirical gates for ecological state indicators**

Alternative:

> **When does an ecological state proxy earn interpretation? Four empirical gates for measurement adequacy, representation, and residual context**

The word `indicator` should be used only where the candidate state/proxy is genuinely being evaluated as an endpoint-relevant compressed ecological measure; do not retrofit indicator terminology onto every raw biological variable.

### Stretch target — Methods in Ecology and Evolution, conditional only

MEE becomes defensible only if the four-gate logic is promoted from a synthesis of existing analyses into a genuinely reusable methodological object.

Minimum upgrade required before considering MEE:

1. define a general algorithm/checklist with explicit inputs, outcomes, and fail-closed transitions;
2. implement it as reusable code rather than only manuscript prose;
3. benchmark the workflow on simulated cases where the truth is known, including at least:
   - complete state + redundant context;
   - incomplete state + missing process coordinate;
   - inadequate proxy;
   - representation collapse;
   - non-identifiable study/origin design;
4. show that the workflow controls a failure that plausible existing analysis workflows do not;
5. demonstrate portability across the existing natural systems after the simulation benchmark;
6. package code with an author-approved open-source license.

Without those additions, MEE is not the recommended target because the current contribution is an empirical methodological synthesis rather than a clearly new method.

### Alternative target — Ecological Informatics, conditional

Consider only if the manuscript is recentered on representation/information preservation and data-pipeline failure, especially the distinction between biological measurement and analytical representation illustrated by *Campanula americana*.

This would require a stronger computational/informatics contribution across multiple systems. In the current four-gate form, the indicator-validity framing is broader and more coherent than an informatics-only framing.

### Not preferred — Ecological Modelling

The current paper is not primarily a new ecological model, systems-analysis theory, or model-development paper. Model/state language is present, but the empirical contribution concerns whether measurements/proxies and representations license interpretation. Ecological Modelling would become more natural only if the paper were rebuilt around a formal state-space modelling framework, which is unnecessary for the current evidence package.

## Submission strategy

1. Build the independent manuscript for **Ecological Indicators** first.
2. Keep all frozen natural-data outcomes unchanged.
3. Add one machine-readable gate table and deterministic figures.
4. Perform a nearest-neighbour literature audit on ecological indicator validation, construct validity/measurement error, proxy validation, preprocessing information loss, and residual-confounding interpretation.
5. Reassess MEE only after that audit. If the nearest-neighbour review shows that the four-gate decision logic is itself methodologically novel and broadly reusable, open a deliberate method-development branch with simulation benchmarks. Otherwise submit the empirical synthesis without inflating it into a new-method claim.

## Current go/no-go

**GO** for development as one independent Ecological Indicators-oriented empirical methodological paper.

**NO-GO** for four separate natural-data papers at present.

**NO-GO** for pooled cross-origin ecological-effect modelling with the existing archives.

**CONDITIONAL** for MEE; requires a separate method-development gate rather than prose reframing alone.
