# ML020 variance-semantics audit

Before interpreting ML020, the Python recovery formula was checked against an existing canonical direct-cluster value rather than trusted by inspection.

For ML014 *Eucalyptus socialis*, `n_fragmented=13`, `n_reference=15`, and `g=-1.02391388`. The `metafor::escalc(measure="SMD", vtype="LS")` large-sample variance used by EGWEE is reproduced by

`v = (n1+n2)/(n1*n2) + g^2 / (2*(n1+n2))`

which gives `0.1623111656`, matching the canonical stored `0.16231117`.

Using `2*(n1+n2-2)` in the second denominator would give `0.1637512750` and is therefore not the repository's variance semantics.

The ML020 recovery script must use the first formula before any state-separation result is interpreted.