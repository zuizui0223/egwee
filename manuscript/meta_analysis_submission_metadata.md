# EGWEE multilayer meta-analysis publication metadata

## Manuscript identity

- **Working title:** Evidence for variable life-cycle bottleneck positions under habitat fragmentation: a cross-system synthesis of plant interaction, mating and reproduction
- **Source manuscript:** `manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md`
- **Protocol:** `manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md`
- **Submission state:** `revision_required_estimand_scale_sensitivity`
- **Article type:** Research Article / empirical research synthesis
- **Primary target journal:** **Journal of Ecology**
- **Fallback venues:** Ecology (Article or Concepts & Synthesis, if reframed for broader ecological generality); Oikos (Meta-analysis)

## Venue rationale

Journal of Ecology is the best current fit because plants and plant–animal interactions are central, while the manuscript asks a general plant-ecology question rather than claiming a universal cross-taxon law. The current evidence is a results-bearing quantitative synthesis with substantial empirical data, which fits the journal's Research Article route better than a Review.

Current Journal of Ecology shaping constraints:

- research articles are typically about 8000 words;
- initial-submission abstract <=350 words;
- abstract uses clear numbered statements;
- the final abstract statement is headed **Synthesis** and states the general ecological advance;
- research-article main sections ultimately need Introduction, Materials and Methods, Results and Discussion;
- up to eight keywords/short phrases.

The manuscript abstract and keywords have been reformatted to these requirements, and the main text has been converted to Introduction, Materials and Methods, Results and Discussion. Automated word-count and submission-shape checks are used before the remaining figure and anonymous-submission package work.

## Ecological research position

EGWEE is a plant-fragmentation ecology synthesis. Its primary objects are natural biological processes and their coupling across fragmented systems:

- pollinator interaction / pollen receipt;
- movement and mating connectivity;
- reproductive function;
- adult and offspring genetic responses.

The paper asks whether these processes remain coupled under fragmentation or become decoupled because they operate over different spatial scales, demographic pathways and response times.

Finite-model NEE/EGWE work is not the framing, estimand, admission rule or inferential target of this paper. It may be cited only as downstream comparative theory where useful.

> **Submission hold:** the historical Hedges-g synthesis is reproducible, but its biological separation/robustness interpretation is estimand-scale dependent. Journal of Ecology submission is reopened pending the mandatory g-versus-lnRR revision.

## Current quantitative state

Primary direct Hedges-g synthesis:

- independent programme/study clusters: **5**;
- admissible marginal effects: **17**;
- full Fisher synthesis: `chi-square(10)=22.64771647`, **`p = 0.01212432`**;
- omit-ML001 *Serapias lingua*: `chi-square(8)=11.36345148`, **`p = 0.18194353`**;
- therefore the pooled rejection is not Serapias-independent.

The fifth cluster, ML020 Aizen–Feinsinger Chaco, is retained despite its non-significant programme gate (`p_ML020=1.0`). It provides the independent negative robustness result: interaction and reproductive-function layers can deteriorate together without detectable separation in effect magnitude.

ML015 *Eucalyptus wandoo* remains separate Fisher-z gradient generalisation evidence and is never pooled into the primary Hedges-g Fisher statistic.

## Current claim ceiling

Authorised manuscript-level ecological claims:

- natural fragmented plant systems include both coupled and decoupled process responses;
- the five-cluster direct corpus contains evidence against complete equality of process-specific fragmentation responses, but that evidence is materially dependent on ML001 *Serapias* and is not leave-one-system-out robust;
- ML020 independently shows coupled deterioration of interaction and reproductive function across a replicated fragmentation programme;
- *Eucalyptus wandoo*, *Cardiopetalum calophyllum* and the Kakamega *Acanthopale pubescens* panel each show a quantity–function mismatch in which interaction/pollen quantity is maintained or changes less strongly while reproductive function declines;
- the repeated quantity–function geometry is a descriptive ecological motif across heterogeneous registered effect families, not a pooled universal effect;
- the complete paired process–function census contains 12 independent programmes; 11 are pair-testable, 4 resolve a mismatch, 7 are unresolved and 1 is not pair-testable; among resolved mismatches, 3 are downstream F-dominant and 1 is upstream process-dominant;
- the two-direction resolved bottleneck result is not leave-one-programme-out robust: omitting ML001 *Serapias* removes the only resolved upstream process-dominant case and leaves 3 downstream F-dominant resolved programmes;
- the complete registered I–F census contains 8 programmes; 7 are pair-testable, 3 resolve a mismatch, all 3 are F-more-negative-than-I, 4 are unresolved, and 1 is not pair-testable;
- all 8 registered I endpoints quantify interaction/pollen quantity; none directly quantify compatible mating quality, realised paternity or effective pollen-donor diversity on the same I–F frame;
- a secondary four-programme movement/mating-support versus F audit contains one resolved upstream process-dominant mismatch (*Serapias*) and three unresolved contrasts, showing that the dominant fragmentation bottleneck is not fixed at reproductive function;
- the current evidence does not resolve a common directional adult-versus-offspring genetic lag.

Not authorised:

- one universal fragmentation response trajectory;
- a universal ordering of I/C/F/G responses;
- a general causal explanation for quantity–function decoupling;
- a confirmed cross-system cohort/history lag;
- treating pollinator abundance, reproductive output or genetic diversity alone as a sufficient proxy for whole-system condition;
- one universal life-cycle bottleneck position across fragmented plant systems;
- claiming that upstream and downstream bottleneck directions are both leave-one-programme-out robust or recurrent across independent systems;
- converting the descriptive 3 downstream : 1 upstream resolved split into a sign/binomial test or a global regime-prevalence estimate;
- a universal claim that effective mating quality is the missing mechanism in every fragmented system;
- direct empirical validation of finite EGWE/NEE operators;
- searching for additional systems merely to restore a preferred p-value or force a pair family to K=5.

## Completion gates

- [x] ecological response-coupling question defined independently from theory;
- [x] primary and secondary effect-size streams declared;
- [x] response-layer coding declared;
- [x] dependence/duplicate rules declared;
- [x] seed meta-analysis literature identified;
- [x] candidate-system ledger created;
- [x] primary same-effect-family cluster denominator materialized for the current claim;
- [x] five-cluster primary synthesis computed;
- [x] leave-one-primary-cluster-out influence analysis computed;
- [x] fifth independent same-effect-family robustness test completed;
- [x] quantitative manuscript conclusion rewritten to match the canonical synthesis;
- [x] primary venue selected: Journal of Ecology;
- [x] journal-specific abstract and keywords shaped;
- [x] main text converted to Journal of Ecology IMRaD structure;
- [x] main-text word count audited against the ~8000-word research-article target (current automated count: 7031 words from Introduction onward);
- [x] pre-scale-audit figure/table package completed and CI-reproduced (Figures 1–4, Table 1, complete paired process–function bottleneck census Table 2, Supplementary Tables S1–S3, Supplementary Figure S1);
- [x] pre-scale-audit double-anonymous package checked and anonymously reproduced in CI;
- [x] estimand-scale audit completed: Hedges-g and lnRR yield materially different response geometry / robustness classifications;
- [ ] manuscript headline revised so no scale-dependent separation/bottleneck claim is presented as scale-invariant;
- [ ] g and lnRR sensitivity reported in Methods, Results, Limitations and figure/table package;
- [ ] submission freeze renewed after scale-aware manuscript revision;
- [ ] author/declaration metadata approved.

Secondary cohort-lag and interaction/function-coupling analyses remain optional future ecological extensions only if independently justified coverage becomes sufficient; they are not submission blockers for the present cross-system fragmentation synthesis.
