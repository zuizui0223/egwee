# CFTQ0350 Pritchard custard-apple gradient recovery — 2026-09-25

## Admission

`P2_CF01_PRITCHARD_2005` is admitted as **one retrospective gradient/generalisation multilayer programme**
using the frozen cluster-robust dependence fallback.

This is not a covariance-aware within-programme I-F test. The F frame is a known five-orchard subset
of the nine-orchard I frame, but the public source does not expose the numeric nine-orchard I vector
needed to reconstruct paired sampling dependence.

## Independent unit and exposure

- independent unit: orchard/site
- exposure: ln distance to nearest naturally occurring rainforest
- larger exposure = greater crop isolation / landscape position
- source I frame: 9 orchards
- source F frame: 5 orchards nested within the I frame

The thesis explicitly cautions that distance is not experimentally replicated and may covary with
rainfall or broad geographic position. EGWEE therefore treats the programme as observational
landscape-position generalisation evidence, not causal proof of a rainforest-distance mechanism.

## Primary marginal effects

### I — total floral visitor abundance

Source Chapter 3 reports R² = 0.573 with a negative slope across nine orchards.

- r = **−0.757**
- Fisher z = **−0.989**
- variance = **0.166667**
- n = **9 orchards**

### F — open-pollinated fruit initiation

Using the five source-explicit orchard means and the source log-log transformation:

- r = **−0.903**
- Fisher z = **−1.490**
- variance = **0.500000**
- n = **5 orchards**

The raw-proportion sensitivity gives Fisher z = **−1.377** and points in the same negative direction.

## Dependence boundary

The exact five F orchards are a subset of the nine I orchards, satisfying the frozen
overlap/nesting rule.

However, the public thesis reports the nine-orchard I relationship as a regression/figure rather than
a numeric site table. EGWEE therefore does **not**:

- digitize Figure 3.2;
- predict I values from the fitted line;
- set I-F covariance to zero;
- calculate a within-programme I-F p-value.

The two valid marginal effects remain in one programme cluster and use the frozen cluster-robust
fallback at the cross-programme stage.

## Scope

This programme:

- contributes **one** gradient/generalisation programme;
- contributes **two primary Fisher-z marginal effects**;
- contributes **zero** primary direct Hedges-g programmes;
- does not change direct I-F coverage;
- does not alter the frozen Phase-1 synthesis;
- must be labelled retrospective and observational;
- does not validate an EGWE/NEE finite operator.
