from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence/meta_extraction/phase2_cf01_acer_miyabei_table1_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_acer_miyabei_gradient_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/phase2_cf01_acer_miyabei_gradient_covariance_v1.json"
RESULT = ROOT / "manuscript/PHASE2_CF01_ACER_MIYABEI_GRADIENT_RECOVERY_2026-09-24.md"

EXPECTED_IDS = list("abcdefghijklmnopqrstu")
EXPECTED_COMMON = ["c", "d", "f", "i", "l", "m", "o", "p", "q"]
Z975 = 1.959963984540054


def read_rows() -> list[dict[str, str]]:
    with SOURCE.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert [r["forest_id"] for r in rows] == EXPECTED_IDS
    assert len(rows) == 21
    return rows


def f(x: str) -> float | None:
    x = (x or "").strip()
    return None if x == "" else float(x)


def pearson(x: list[float], y: list[float]) -> float:
    assert len(x) == len(y) and len(x) >= 4
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    sx = sum(v * v for v in dx)
    sy = sum(v * v for v in dy)
    assert sx > 0 and sy > 0
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(sx * sy)


def residuals(y: list[float], x: list[float]) -> list[float]:
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    denom = sum((v - mx) ** 2 for v in x)
    assert denom > 0
    beta = sum((a - mx) * (b - my) for a, b in zip(x, y)) / denom
    alpha = my - beta * mx
    return [yy - (alpha + beta * xx) for xx, yy in zip(x, y)]


def fisher_effect(x: list[float], y: list[float]) -> dict[str, float]:
    r = pearson(x, y)
    assert -1 < r < 1
    z = math.atanh(r)
    var = 1.0 / (len(x) - 3)
    return {"r": r, "z": z, "variance": var}


def normal_p(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def main() -> None:
    rows = read_rows()
    parsed = []
    for r in rows:
        dist = f(r["distance_to_nearest_forest_m"])
        seed_density = f(r["seed_density_m2"])
        viable = f(r["viable_seed_proportion"])
        kinship = f(r["mean_seed_kinship"])
        parsed.append(
            {
                "forest_id": r["forest_id"],
                "distance": dist,
                "seed_density": seed_density,
                "viable": viable,
                "kinship": kinship,
            }
        )

    common = [
        r for r in parsed
        if all(r[k] is not None for k in ("distance", "seed_density", "viable", "kinship"))
    ]
    assert [r["forest_id"] for r in common] == EXPECTED_COMMON
    assert len(common) == 9

    x = [math.log(r["distance"]) for r in common]
    c_support = [-r["kinship"] for r in common]
    f_primary = [r["seed_density"] * r["viable"] for r in common]
    f_density = [r["seed_density"] for r in common]
    f_viable = [r["viable"] for r in common]

    c_eff = fisher_effect(x, c_support)
    f_eff = fisher_effect(x, f_primary)
    density_eff = fisher_effect(x, f_density)
    viable_eff = fisher_effect(x, f_viable)

    rho = pearson(residuals(c_support, x), residuals(f_primary, x))
    cov = rho * math.sqrt(c_eff["variance"] * f_eff["variance"])
    det = c_eff["variance"] * f_eff["variance"] - cov * cov
    assert det > 0

    delta = c_eff["z"] - f_eff["z"]
    var_delta = c_eff["variance"] + f_eff["variance"] - 2 * cov
    assert var_delta > 0
    se_delta = math.sqrt(var_delta)
    z_stat = delta / se_delta
    p = normal_p(z_stat)
    ci_low = delta - Z975 * se_delta
    ci_high = delta + Z975 * se_delta

    EFFECTS.parent.mkdir(parents=True, exist_ok=True)
    with EFFECTS.open("w", newline="", encoding="utf-8") as fh:
        fields = [
            "programme_id", "endpoint_role", "layer", "endpoint", "effect_stream",
            "n_independent", "exposure", "r", "fisher_z", "variance",
            "primary_or_sensitivity", "orientation_note", "source_location",
        ]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for role, layer, endpoint, eff, tier, note in (
            (
                "C_primary", "C_movement_connectivity", "negative_mean_seed_kinship",
                c_eff, "primary",
                "Higher endpoint = lower kinship = greater gene-flow support; higher exposure = greater forest isolation.",
            ),
            (
                "F_primary", "F_reproductive_function", "viable_seed_density_m2",
                f_eff, "primary",
                "EGWEE-derived deterministic product seed_density_m2 * viable_seed_proportion; higher = more viable dispersed seed output.",
            ),
            (
                "F_sensitivity_density", "F_reproductive_function", "seed_density_m2",
                density_eff, "sensitivity",
                "Source-reported seed density retained as endpoint-definition sensitivity only.",
            ),
            (
                "F_sensitivity_viability", "F_reproductive_function", "viable_seed_proportion",
                viable_eff, "sensitivity",
                "Source-reported viable-seed proportion retained as endpoint-definition sensitivity only.",
            ),
        ):
            w.writerow(
                {
                    "programme_id": "P2_CF01_ACER_MIYABEI_2014",
                    "endpoint_role": role,
                    "layer": layer,
                    "endpoint": endpoint,
                    "effect_stream": "fisher_z_gradient",
                    "n_independent": len(common),
                    "exposure": "log_distance_to_nearest_forest_m",
                    "r": f"{eff['r']:.12f}",
                    "fisher_z": f"{eff['z']:.12f}",
                    "variance": f"{eff['variance']:.12f}",
                    "primary_or_sensitivity": tier,
                    "orientation_note": note,
                    "source_location": "Nagamitsu et al. 2014 Table 1",
                }
            )

    cov_result = {
        "programme_id": "P2_CF01_ACER_MIYABEI_2014",
        "status": "gradient_generalisation_multilayer_cluster_retrospective",
        "source_table": "Nagamitsu et al. 2014 Table 1",
        "common_forest_ids": EXPECTED_COMMON,
        "n_independent_forests": len(common),
        "primary_exposure": "log_distance_to_nearest_forest_m",
        "C_endpoint": "negative_mean_seed_kinship",
        "F_endpoint": "viable_seed_density_m2",
        "C_fisher_z": c_eff["z"],
        "F_fisher_z": f_eff["z"],
        "C_variance": c_eff["variance"],
        "F_variance": f_eff["variance"],
        "residual_rho_CF": rho,
        "cov_CF": cov,
        "covariance_determinant": det,
        "delta_C_minus_F": delta,
        "se_delta": se_delta,
        "z_delta": z_stat,
        "p_delta_two_sided": p,
        "ci95_delta": [ci_low, ci_high],
        "sensitivities": {
            "seed_density": density_eff,
            "viable_seed_proportion": viable_eff,
        },
        "primary_hedges_increment": 0,
        "retrospective_recovery": True,
        "effect_outcomes_opened_after_source_table_visible": True,
    }
    COV.write_text(json.dumps(cov_result, indent=2) + "\n", encoding="utf-8")

    RESULT.write_text(
        f"""# CFTQ0142 Acer miyabei retrospective gradient recovery — 2026-09-24

## Admission

`P2_CF01_ACER_MIYABEI_2014` is admitted as **one retrospective
gradient/generalisation multilayer programme**.

This is not outcome-blind: Table 1 values and the published qualitative conclusions were visible
before the deterministic recovery rule was written. The result is therefore generalisation evidence,
not prospective confirmation.

## Effect unit

- source forest fragments: **21**
- primary C-F common frame after source missingness: **{len(common)} forests**
- common forest IDs: **{', '.join(EXPECTED_COMMON)}**
- independent unit: **forest fragment**
- target trees / quadrats / seeds: nested below forest and not counted as n

## Locked variables

- exposure: log distance to nearest forest; higher = greater isolation
- C: negative mean seed kinship; higher = greater gene-flow support
- F: viable seed density = source seed density × source viable-seed proportion

## Primary gradient effects

- C: r = **{c_eff['r']:+.3f}**, Fisher z = **{c_eff['z']:+.3f}**
- F: r = **{f_eff['r']:+.3f}**, Fisher z = **{f_eff['z']:+.3f}**
- marginal Fisher-z variance: **{c_eff['variance']:.6f}** for each endpoint

The source-table isolation gradient therefore shows little resolved change in the derived viable-seed
output and a weak positive C-support correlation on the nine-forest common frame.

## C-F response geometry

The residual dependence reconstruction gives:

- residual rho(C,F) = **{rho:+.3f}**
- working Cov(z_C,z_F) = **{cov:+.6f}**
- covariance determinant = **{det:.6f}**
- C - F = **{delta:+.3f}**
- SE = **{se_delta:.3f}**
- 95% CI = **[{ci_low:+.3f}, {ci_high:+.3f}]**
- two-sided p = **{p:.3f}**

The interval crosses zero. This programme therefore does **not** resolve a precise C-F separation
under the frozen retrospective recovery.

## Endpoint-definition sensitivities

On the same nine forests:

- source seed density alone: r = **{density_eff['r']:+.3f}**, Fisher z = **{density_eff['z']:+.3f}**
- source viable-seed proportion alone: r = **{viable_eff['r']:+.3f}**, Fisher z = **{viable_eff['z']:+.3f}**

These two source components point in different directions with isolation. That divergence is exactly
why neither visible component is promoted post hoc to replace the deterministic primary viable-seed
density. The sensitivity pattern should be reported as endpoint-definition heterogeneity, not used
as a significance rescue.

## Scope

This programme:

- contributes **one** gradient/generalisation programme;
- contributes **zero** primary direct Hedges-g programmes;
- does not alter the frozen Phase-1 five-cluster synthesis;
- does not validate an EGWE/NEE finite operator;
- should be labelled retrospective wherever used.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF01_ACER_MIYABEI_OK "
        f"n={len(common)} C_z={c_eff['z']:.8f} F_z={f_eff['z']:.8f} "
        f"delta={delta:.8f} p={p:.8f} cov_pd=true retrospective=true"
    )


if __name__ == "__main__":
    main()
