from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_table1_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_covariance_v1.json"
RULE = ROOT / "manuscript/CF01_CARDIOPETALUM_2012_GRADIENT_RECOVERY_RULE.md"
RESULT = ROOT / "manuscript/PHASE2_CF01_CARDIOPETALUM_GRADIENT_RECOVERY_2026-09-24.md"
REGISTRY = ROOT / "evidence/meta_extraction/phase2_gradient_programme_registry_v1.csv"
REGISTRY_STATUS = ROOT / "manuscript/PHASE2_GRADIENT_PROGRAMME_REGISTRY_2026-09-24.md"

PROGRAMME = "P2_CF01_CARDIOPETALUM_2012"
TOL = 5e-10


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
    assert [r["fragment_id"] for r in src] == [f"F{i}" for i in range(1, 11)]
    assert len(src) == 10
    assert src[-1]["seed_set_per_flower_mean"] == ""

    x = [-math.log(float(r["area_ha"])) for r in src]
    xi = [math.log(float(r["distance_nearest_fragment_m"])) for r in src]
    i = [float(r["pollinator_abundance_per_flower_mean"]) for r in src]
    f = [float(r["fruit_set_mean"]) for r in src]
    fo = [float(r["follicles_per_flower_mean"]) for r in src]
    seed_rows = [r for r in src if r["seed_set_per_flower_mean"]]
    sx = [-math.log(float(r["area_ha"])) for r in seed_rows]
    seed = [float(r["seed_set_per_flower_mean"]) for r in seed_rows]

    def eff(xx: list[float], yy: list[float]) -> tuple[float, float, float]:
        r = pearson(xx, yy)
        return r, math.atanh(r), 1.0 / (len(xx) - 3)

    ir, iz, iv = eff(x, i)
    fr, fz, fv = eff(x, f)
    forr, foz, fov = eff(x, fo)
    sr, sz, sv = eff(sx, seed)
    iir, iiz, iiv = eff(xi, i)
    fir, fiz, fiv = eff(xi, f)

    rho = pearson(residuals(i, x), residuals(f, x))
    cov = rho * math.sqrt(iv * fv)
    det = iv * fv - cov * cov
    assert det > 0
    delta = iz - fz
    dvar = iv + fv - 2 * cov
    dse = math.sqrt(dvar)
    zstat = delta / dse
    p = math.erfc(abs(zstat) / math.sqrt(2.0))

    effects = {r["endpoint_role"]: r for r in rows(EFFECTS)}
    expected = {
        "I_primary": (ir, iz, iv, 10, "primary"),
        "F_primary": (fr, fz, fv, 10, "primary"),
        "F_sensitivity_follicles": (forr, foz, fov, 10, "sensitivity"),
        "F_sensitivity_seed": (sr, sz, sv, 9, "sensitivity"),
        "I_sensitivity_isolation": (iir, iiz, iiv, 10, "sensitivity"),
        "F_sensitivity_isolation": (fir, fiz, fiv, 10, "sensitivity"),
    }
    assert set(effects) == set(expected)
    for key, (rr, zz, vv, nn, tier) in expected.items():
        row = effects[key]
        assert row["programme_id"] == PROGRAMME
        assert int(row["n_independent"]) == nn
        assert abs(float(row["r"]) - rr) < TOL
        assert abs(float(row["fisher_z"]) - zz) < TOL
        assert abs(float(row["variance"]) - vv) < TOL
        assert row["primary_or_sensitivity"] == tier

    co = json.loads(COV.read_text(encoding="utf-8"))
    assert co["programme_id"] == PROGRAMME
    assert co["status"] == "gradient_generalisation_multilayer_cluster_retrospective"
    assert co["fragment_ids"] == [f"F{i}" for i in range(1, 11)]
    assert co["n_independent_fragments"] == 10
    assert abs(co["I_fisher_z"] - iz) < TOL
    assert abs(co["F_fisher_z"] - fz) < TOL
    assert abs(co["residual_rho_IF"] - rho) < TOL
    assert abs(co["cov_IF"] - cov) < TOL
    assert abs(co["covariance_determinant"] - det) < TOL
    assert abs(co["delta_I_minus_F"] - delta) < TOL
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
        "P2_CF01_ACER_MIYABEI_2014",
        PROGRAMME,
        "P2_CF01_PRITCHARD_2005",
    }
    card = registry[PROGRAMME]
    assert card["independent_unit"] == "forest_fragment"
    assert set(card["layers"].split(";")) == {"I", "F"}
    assert int(card["admissible_gradient_effects"]) == 2
    assert card["covariance_status"] == "proxy_reconstructed_fragment_pair_residual"
    assert card["programme_status"] == "gradient_generalisation_multilayer_cluster_retrospective"
    assert int(card["primary_hedges_increment"]) == 0

    rule = RULE.read_text(encoding="utf-8")
    for token in (
        "retrospective external recovery",
        "negative natural log fragment area",
        "pollinator abundance per flower",
        "fruit set per flower",
        "follicles set per flower",
        "seed set per flower",
        "contributes **zero** primary direct Hedges-g I-F programmes",
    ):
        assert token in rule, token

    result = RESULT.read_text(encoding="utf-8")
    for token in (
        "independent forest fragments: **10**",
        "Fisher z = **−0.245**",
        "Fisher z = **−1.684**",
        "I − F = **+1.439**",
        "95% CI = **[+0.483, +2.394]**",
        "p = **0.00316**",
        "interaction persistence with reproductive collapse",
        "retrospective",
    ):
        assert token in result, token

    status = REGISTRY_STATUS.read_text(encoding="utf-8")
    for token in (
        "**6 gradient/generalisation programmes**",
        "**19 primary Fisher-z admissible marginal effects**",
        "**P2_CF01_CARDIOPETALUM_2012 — Cardiopetalum calophyllum**",
        "I-F contrast is **+1.439**",
        "p=0.00316",
        "retrospective generalisation evidence",
    ):
        assert token in status, token

    print(
        "PHASE2_CF01_CARDIOPETALUM_CHECK_OK "
        f"n=10 I_z={iz:.8f} F_z={fz:.8f} delta={delta:.8f} "
        f"p={p:.8f} gradient_programmes=6 direct_IF_increment=0 retrospective=true"
    )


if __name__ == "__main__":
    main()
