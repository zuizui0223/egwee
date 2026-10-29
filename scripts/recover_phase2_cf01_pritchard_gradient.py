from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALUES = ROOT / "evidence/meta_extraction/phase2_cf01_pritchard_openfruit_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_pritchard_gradient_effects_v1.csv"
DEPENDENCE = ROOT / "evidence/meta_extraction/phase2_cf01_pritchard_gradient_dependence_v1.json"
RULE = ROOT / "manuscript/CF01_PRITCHARD_2005_GRADIENT_RECOVERY_RULE.md"
RESULT = ROOT / "manuscript/PHASE2_CF01_PRITCHARD_GRADIENT_RECOVERY_2026-09-25.md"

PROGRAMME = "P2_CF01_PRITCHARD_2005"
I_R2 = 0.573
I_N = 9
I_SLOPE_SIGN = -1
EXPECTED_F = [
    ("Briggs Lease", 0.1, 0.11),
    ("Cummings", 0.5, 0.04),
    ("Kilpatrick", 5.5, 0.02),
    ("Lavers", 9.0, 0.02),
    ("Samanes", 12.0, 0.03),
]


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pearson(x: list[float], y: list[float]) -> float:
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(
        sum(a * a for a in dx) * sum(b * b for b in dy)
    )


def main() -> None:
    for p in (VALUES, RULE):
        assert p.is_file(), p

    vals = rows(VALUES)
    assert len(vals) == 5
    got = [
        (
            r["orchard"],
            float(r["distance_to_rainforest_km"]),
            float(r["open_fruit_initiation_mean"]),
        )
        for r in vals
    ]
    assert got == EXPECTED_F

    # Source Chapter 3: nine-orchard log abundance ~ log distance regression.
    r_i = I_SLOPE_SIGN * math.sqrt(I_R2)
    z_i = math.atanh(r_i)
    v_i = 1.0 / (I_N - 3)

    # Source Chapter 4: five source-explicit orchard means; source uses log-log distance analysis.
    log_d = [math.log(d) for _, d, _ in got]
    log_f = [math.log(y) for _, _, y in got]
    raw_f = [y for _, _, y in got]

    r_f = pearson(log_d, log_f)
    z_f = math.atanh(r_f)
    v_f = 1.0 / (len(got) - 3)

    r_f_raw = pearson(log_d, raw_f)
    z_f_raw = math.atanh(r_f_raw)

    EFFECTS.parent.mkdir(parents=True, exist_ok=True)
    with EFFECTS.open("w", newline="", encoding="utf-8") as fh:
        fields = [
            "programme_id", "endpoint_role", "layer", "endpoint", "effect_stream",
            "n_independent", "exposure", "r", "fisher_z", "variance",
            "primary_or_sensitivity", "source_location",
        ]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for role, layer, endpoint, n, r, z, var, tier, loc in (
            (
                "I_primary", "I_interaction", "total_floral_visitor_abundance",
                I_N, r_i, z_i, v_i, "primary",
                "Chapter 3 source regression R2=0.573, negative slope, n=9 orchards",
            ),
            (
                "F_primary", "F_reproductive_function", "open_fruit_initiation_log",
                len(got), r_f, z_f, v_f, "primary",
                "Chapter 4 five source orchard means; ln fruit initiation versus ln distance",
            ),
            (
                "F_sensitivity_raw_proportion", "F_reproductive_function",
                "open_fruit_initiation_raw_proportion",
                len(got), r_f_raw, z_f_raw, v_f, "sensitivity",
                "Chapter 4 five source orchard means; raw proportion versus ln distance",
            ),
        ):
            w.writerow(
                {
                    "programme_id": PROGRAMME,
                    "endpoint_role": role,
                    "layer": layer,
                    "endpoint": endpoint,
                    "effect_stream": "fisher_z_gradient",
                    "n_independent": n,
                    "exposure": "log_distance_to_rainforest_km",
                    "r": f"{r:.12f}",
                    "fisher_z": f"{z:.12f}",
                    "variance": f"{var:.12f}",
                    "primary_or_sensitivity": tier,
                    "source_location": loc,
                }
            )

    dependence = {
        "programme_id": PROGRAMME,
        "status": "gradient_generalisation_multilayer_cluster_retrospective_cluster_robust",
        "independent_unit": "orchard_site",
        "I_frame_n": 9,
        "F_frame_n": 5,
        "F_is_explicit_subset_of_I": True,
        "F_orchards": [name for name, _, _ in got],
        "I_numeric_orchard_vector_publicly_recoverable": False,
        "paired_covariance_reconstructable": False,
        "covariance_status": "cluster_robust_fallback_overlap_5_of_9_no_pair_covariance",
        "within_programme_I_minus_F_test_calculated": False,
        "primary_hedges_increment": 0,
        "retrospective_recovery": True,
        "claim_ceiling": (
            "observational landscape-position generalisation; source warns distance is not "
            "experimentally replicated and may covary with rainfall/geographic position"
        ),
    }
    DEPENDENCE.write_text(json.dumps(dependence, indent=2) + "\n", encoding="utf-8")

    RESULT.write_text(
        f"""# CFTQ0350 Pritchard custard-apple gradient recovery — 2026-09-25

## Admission

`{PROGRAMME}` is admitted as **one retrospective gradient/generalisation multilayer programme**
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

- r = **{r_i:+.3f}**
- Fisher z = **{z_i:+.3f}**
- variance = **{v_i:.6f}**
- n = **9 orchards**

### F — open-pollinated fruit initiation

Using the five source-explicit orchard means and the source log-log transformation:

- r = **{r_f:+.3f}**
- Fisher z = **{z_f:+.3f}**
- variance = **{v_f:.6f}**
- n = **5 orchards**

The raw-proportion sensitivity gives Fisher z = **{z_f_raw:+.3f}** and points in the same negative
direction.

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
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF01_PRITCHARD_OK "
        f"I_n={I_N} I_z={z_i:.8f} F_n={len(got)} F_z={z_f:.8f} "
        "covariance=cluster_robust_fallback direct_IF_increment=0 retrospective=true"
    )


if __name__ == "__main__":
    main()
