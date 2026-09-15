# ML020 / PS022 Aizen–Feinsinger 1994 recovery result

## Decision

**Admit ML020 as the fifth primary same-effect-family cluster.**

Effect family: `hedges_g_direct`.

Independent primary denominator contribution: **one programme cluster**, not three species.

## Why admission passes

- Source-defined direct habitat contrast is available: small forest fragment (<1 ha) versus continuous forest.
- The source explicitly identifies *Atamisquea emarginata*, *Cercidium australe* and *Prosopis nigra* as the species with the three habitat treatments replicated across four study sites.
- Appendix I exposes one habitat-unit mean per site/condition for pollen tubes and fruit set.
- Primary calculation uses those habitat-unit means as the independent observations (`n=4` small, `n=4` continuous), rather than the nested plant/flower/fruit counts.
- PT and FS are aligned on the same four site IDs; the source states that these reproductive-stage measures generally came from the same sampled individuals for the retained non-herbaceous species.
- A group-centered, site-aligned PT/FS correlation can therefore be used as the within-species covariance proxy.
- All three source-explicit four-site species are retained, preventing selection of one species because it gives a preferred state-separation result.

Discovery was retrospective: the public Appendix I numeric table was visible during candidate recovery. ML020 is therefore an independent external system but not a prospectively outcome-blind discovery.

## Marginal Hedges-g effects

All effects are small-fragment minus continuous-forest and are oriented so negative values indicate reduced support/function under fragmentation.

### *Atamisquea emarginata*

- `I_pollen_tubes`: `g=-0.71203322`, `v=0.53168696`;
- `F_fruit_set`: `g=-1.00369234`, `v=0.56296240`;
- group-centered `rho=-0.19170473`, covariance `-0.10488190`;
- `I-F=+0.29165912`, `SE=1.14210995`, `z=0.25536888`, `p=0.79843820`.

### *Cercidium australe* (1990)

- `I_pollen_tubes`: `g=-0.63664333`, `v=0.52533217`;
- `F_fruit_set`: `g=-1.13729930`, `v=0.58084061`;
- group-centered `rho=+0.08554857`, covariance `+0.04725614`;
- `I-F=+0.50065597`, `SE=1.00581335`, `z=0.49776231`, `p=0.61865159`.

### *Prosopis nigra* (1990)

- `I_pollen_tubes`: `g=-0.48005270`, `v=0.51440316`;
- `F_fruit_set`: `g=-1.13427121`, `v=0.58041070`;
- group-centered `rho=-0.13799123`, covariance `-0.07539994`;
- `I-F=+0.65421850`, `SE=1.11517431`, `z=0.58618018`, `p=0.55775444`.

Each 2x2 working covariance is positive definite and each I-F contrast variance is positive.

## Programme-cluster p-value

The three species share the same four landscapes and are treated as dependent subsystems inside ML020. Per the recovery contract, the programme-level p-value is the Bonferroni gate across the three species-specific I-F tests:

`p_ML020 = min(1, 3 * min(0.79843820, 0.61865159, 0.55775444)) = 1.0`.

This is not a failed admission. It is an admitted cluster with **no evidence that the fragmentation effect differs between I and F** under the frozen within-programme test. Both layers generally deteriorate in the same direction.

## Effect on the primary synthesis

Using the existing canonical cluster p-values plus ML020:

- ML001 Serapias: `0.00354530`;
- ML002 Brosimum: `0.19911670`;
- ML003 Spondias: `0.17406774`;
- ML014 Eucalyptus socialis: `0.09831774`;
- ML020 Chaco programme: `1.0`.

Five-cluster Fisher combination:

- `chi-square(10)=22.64771647`;
- **`p=0.01212432`**;
- the full corpus still rejects primary layer exchangeability at 0.05, but less strongly than the four-cluster corpus because ML020 contributes no Fisher evidence.

Key leave-Serapias-out diagnostic after ML020 admission:

- retain ML002 + ML003 + ML014 + ML020;
- `chi-square(8)=11.36345148`;
- **`p=0.18194353`**;
- **do not reject**.

Other leave-one-cluster-out p-values are:

- omit ML002: `0.01276794`;
- omit ML003: `0.01407214`;
- omit ML014: `0.02116199`;
- omit ML020: `0.00384724` (the previous canonical four-cluster result).

## Scientific conclusion

The fifth same-effect-family cluster gives the requested independent-system test, and the answer is **negative for Serapias-independent robustness**.

Adding a legitimately admitted replicated fragmentation programme does not rescue the conclusion when ML001 is removed; it moves the omit-ML001 Fisher p-value from `0.07777` to `0.18194`. Therefore the current cross-system rejection remains materially dependent on Serapias.

This result should not be repaired by searching for a sixth cluster because ML020 was non-significant. Any sixth-cluster search must be justified as a predeclared expansion of system coverage, not as an attempt to reverse this negative robustness result.