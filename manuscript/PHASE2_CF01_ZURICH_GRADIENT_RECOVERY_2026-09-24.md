# CFTQ0018 Zurich gradient recovery — 2026-09-24

## Decision

The Zurich BetterBlooms programme passes the registered continuous-gradient effect-unit gate as one
**gradient/generalisation multilayer programme**.

- source-defined severity: `Urban_500`, proportion impervious surface within 500 m;
- independent unit: garden;
- source gardens: 24;
- source-wide low-effort exclusion: garden 39;
- phytometer-specific source exclusions are preserved;
- effect representation: Fisher z of Pearson r;
- primary Hedges-g programme count increment: **0**.

The four phytometer species are repeated endpoint panels within the same experimental programme and
are not four independent studies.

## Recovered phytometer pairs

- Daucus_carota: n=23, I z=-0.449, F z=-0.399, I-F=-0.050, 95% CI [-0.737, +0.637]
- Raphanus_sativus: n=23, I z=-0.578, F z=-0.565, I-F=-0.013, 95% CI [-0.550, +0.524]
- Onobrychis_viciifolia: n=20, I z=-0.262, F z=+0.119, I-F=-0.381, 95% CI [-0.908, +0.147]
- Symphytum_officinale: n=23, I z=-0.450, F z=-0.571, I-F=+0.121, 95% CI [-0.409, +0.651]

Negative Fisher z means lower biological support/function with increasing densification/habitat
loss. No pair is selected or discarded based on its direction or interval.

## Dependence

For each phytometer, I and F share the same common garden frame. The working I/F covariance is
reconstructed from residual correlations after separate linear fits on `Urban_500`. All four 2x2
working covariance blocks are positive definite.

This covariance is an approximate reconstructed proxy, not an exact analytic sampling covariance.

## Scope

This programme enters only the separately analysed Fisher-z gradient/generalisation stream.

It does not:

- convert the urban gradient into a binary fragmented/reference contrast;
- increment direct I-F Hedges-g coverage;
- treat four phytometers as four independent programmes;
- alter the frozen Phase-1 five-cluster Fisher synthesis.
