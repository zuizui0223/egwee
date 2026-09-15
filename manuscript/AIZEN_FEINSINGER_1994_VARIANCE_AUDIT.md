# ML020 variance-semantics audit

Before interpreting ML020, the recovery formula was checked against the existing primary direct-cluster implementation rather than trusted by inspection.

## Hedges small-sample correction

Canonical EGWEE primary scripts (including the existing Brosimum and Eucalyptus socialis recoveries) use

`J = 1 - 3/(4df - 1)`

and `g = J * d`.

ML020 now uses the same approximation exactly. The earlier branch implementation used the exact gamma-function Hedges correction; that difference was numerically tiny but was removed so ML020 is literally in the same implemented effect family as ML001–ML014.

For ML020, `n_fragmented=n_reference=4`, so `df=6` and `J=20/23`.

## LS sampling variance

For ML014 *Eucalyptus socialis*, `n_fragmented=13`, `n_reference=15`, and `g=-1.02391388`. The large-sample variance used by EGWEE is

`v = (n1+n2)/(n1*n2) + g^2 / (2*(n1+n2))`

which gives `0.1623111656`, matching the canonical stored `0.16231117`.

Using `2*(n1+n2-2)` in the second denominator would give `0.1637512750` and is therefore not the repository's variance semantics.

ML020 uses the same Hedges correction and the same LS sampling-variance expression before any state-separation contrast is interpreted.
