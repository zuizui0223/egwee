from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence/meta_extraction/phase2_cf01_acer_miyabei_table1_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_acer_miyabei_gradient_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/phase2_cf01_acer_miyabei_gradient_covariance_v1.json"
RULE = ROOT / "manuscript/CF01_ACER_MIYABEI_2014_GRADIENT_RECOVERY_RULE.md"
RESULT = ROOT / "manuscript/PHASE2_CF01_ACER_MIYABEI_GRADIENT_RECOVERY_2026-09-24.md"
REGISTRY = ROOT / "evidence/meta_extraction/phase2_gradient_programme_registry_v1.csv"
REGISTRY_STATUS = ROOT / "manuscript/PHASE2_GRADIENT_PROGRAMME_REGISTRY_2026-09-24.md"

PROGRAMME = "P2_CF01_ACER_MIYABEI_2014"
COMMON = ["c", "d", "f", "i", "l", "m", "o", "p", "q"]
TOL = 5e-10


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(x: str) -> float | None:
    x = (x or "").strip()
    return None if not x else float(x)


def pearson(x: list[float], y: list[float]) -> float:
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(
        sum(a * a for a in dx) * sum(b * b for b in dy)
    )


def residuals(y: list[float], x: list[float]) -> list[float]:
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    denom = sum((v - mx) ** 2 for v in x)
    beta = sum((xx - mx) * (yy - my) for xx, yy in zip(x, y)) / denom
    alpha = my - beta * mx
    return [yy - (alpha + beta * xx) for xx, yy in zip(x, y)]


def main() -> None:
    for p in (SOURCE, EFFECTS, COV, RULE, RESULT, REGISTRY, REGISTRY_STATUS):
        assert p.is_file(), p

    src = rows(SOURCE)
    assert len(src) == 21
    assert [r["forest_id"] for r in src] == list("abcdefghijklmnopqrstu")

    common = [
        r for r in src
        if all((r[k] or "").strip() for k in (
            "distance_to_nearest_forest_m",
            "seed_density_m2",
            "viable_seed_proportion",
            "mean_seed_kinship",
        ))
    ]
    assert [r["forest_id"] for r in common] == COMMON

    x = [math.log(float(r["distance_to_nearest_forest_m"])) for r in common]
    c = [-float(r["mean_seed_kinship"]) for r in common]
    seed_density = [float(r["seed_density_m2"]) for r in common]
    viability = [float(r["viable_seed_proportion"]) for r in common]
    f = [a * b for a, b in zip(seed_density, viability)]

    def effect(y: list[float]) -> tuple[float, float, float]:
        r = pearson(x, y)
        return r, math.atanh(r), 1.0 / (len(x) - 3)

    cr, cz, cv = effect(c)
    fr, fz, fv = effect(f)
    dr, dz, dv = effect(seed_density)
    vr, vz, vv = effect(viability)

    rho = pearson(residuals(c, x), residuals(f, x))
    cov = rho * math.sqrt(cv * fv)
    det = cv * fv - cov * cov
    assert det > 0
    delta = cz - fz
    dvar = cv + fv - 2 * cov
    dse = math.sqrt(dvar)
    zstat = delta / dse
    p = math.erfc(abs(zstat) / math.sqrt(2.0))

    effects = {r["endpoint_role"]: r for r in rows(EFFECTS)}
    assert set(effects) == {
        "C_primary", "F_primary", "F_sensitivity_density", "F_sensitivity_viability"
    }
    for role, expected in (
        ("C_primary", (cr, cz, cv, "primary")),
        ("F_primary", (fr, fz, fv, "primary")),
        ("F_sensitivity_density", (dr, dz, dv, "sensitivity")),
        ("F_sensitivity_viability", (vr, vz, vv, "sensitivity")),
    ):
        r = effects[role]
        assert r["programme_id"] == PROGRAMME
        assert int(r["n_independent"]) == 9
        assert r["exposure"] == "log_distance_to_nearest_forest_m"
        assert abs(float(r["r"]) - expected[0]) < TOL
        assert abs(float(r["fisher_z"]) - expected[1]) < TOL
        assert abs(float(r["variance"]) - expected[2]) < TOL
        assert r["primary_or_sensitivity"] == expected[3]

    co = json.loads(COV.read_text(encoding="utf-8"))
    assert co["programme_id"] == PROGRAMME
    assert co["status"] == "gradient_generalisation_multilayer_cluster_retrospective"
    assert co["common_forest_ids"] == COMMON
    assert co["n_independent_forests"] == 9
    assert abs(co["C_fisher_z"] - cz) < TOL
    assert abs(co["F_fisher_z"] - fz) < TOL
    assert abs(co["residual_rho_CF"] - rho) < TOL
    assert abs(co["cov_CF"] - cov) < TOL
    assert abs(co["covariance_determinant"] - det) < TOL
    assert abs(co["delta_C_minus_F"] - delta) < TOL
    assert abs(co["se_delta"] - dse) < TOL
    assert abs(co["z_delta"] - zstat) < TOL
    assert abs(co["p_delta_two_sided"] - p) < TOL
    assert co["retrospective_recovery"] is True
    assert co["primary_hedges_increment"] == 0

    registry = {r["programme_id"]: r for r in rows(REGISTRY)}
    assert set(registry) == {
        "ML015",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
        PROGRAMME,
    }
    a = registry[PROGRAMME]
    assert a["independent_unit"] == "forest_fragment"
    assert set(a["layers"].split(";")) == {"C", "F"}
    assert int(a["admissible_gradient_effects"]) == 2
    assert a["covariance_status"] == "proxy_reconstructed_forest_pair_residual"
    assert a["programme_status"] == "gradient_generalisation_multilayer_cluster_retrospective"
    assert int(a["primary_hedges_increment"]) == 0

    rule = RULE.read_text(encoding="utf-8")
    for token in (
        "retrospective external recovery",
        "log distance to nearest forest",
        "C_support = - mean_kinship",
        "F_viable_seed_density = seed_density_per_m2 * viable_seed_proportion",
        "nine forests",
        "zero** primary direct Hedges-g",
    ):
        assert token in rule, token

    result = RESULT.read_text(encoding="utf-8")
    for token in (
        "9 forests",
        "Fisher z = **+0.181**",
        "Fisher z = **−0.00019**",
        "p = **0.624**",
        "seed density alone",
        "viable-seed proportion alone",
        "retrospective",
    ):
        assert token in result, token

    status = REGISTRY_STATUS.read_text(encoding="utf-8")
    for token in (
        "**4 gradient/generalisation programmes**",
        "**15 primary Fisher-z admissible marginal effects**",
        "**P2_CF01_ACER_MIYABEI_2014 — Acer miyabei**",
        "C-F contrast is `+0.181`",
        "retrospective generalisation evidence",
    ):
        assert token in status, token

    print(
        "PHASE2_CF01_ACER_MIYABEI_CHECK_OK "
        f"n=9 C_z={cz:.8f} F_z={fz:.8f} delta={delta:.8f} "
        f"p={p:.8f} gradient_programmes=4 direct_CF_increment=0 retrospective=true"
    )


if __name__ == "__main__":
    main()
