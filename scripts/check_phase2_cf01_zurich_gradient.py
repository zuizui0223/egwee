from __future__ import annotations

import csv
import json
import math
import statistics as stats
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALUES = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_garden_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_gradient_effects_v1.csv"
COVARIANCE = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_gradient_covariance_v1.json"
SOURCE_MANIFEST = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_source_manifest_v1.json"
CONTRACT = ROOT / "manuscript/CF01_ZURICH_2026_GRADIENT_RECOVERY_CONTRACT.md"
RESULT = ROOT / "manuscript/PHASE2_CF01_ZURICH_GRADIENT_RECOVERY_2026-09-24.md"
REGISTRY = ROOT / "evidence/meta_extraction/phase2_gradient_programme_registry_v1.csv"
REGISTRY_STATUS = ROOT / "manuscript/PHASE2_GRADIENT_PROGRAMME_REGISTRY_2026-09-24.md"
PAIR_COVERAGE = ROOT / "evidence/meta_extraction/coverage_expansion_pair_coverage_v1.csv"

PROGRAMME = "P2_CF01_ZURICH_2026"
PLANTS = ["Daucus_carota", "Raphanus_sativus", "Onobrychis_viciifolia", "Symphytum_officinale"]
EXPECTED_N = {
    "Daucus_carota": 23,
    "Raphanus_sativus": 23,
    "Onobrychis_viciifolia": 20,
    "Symphytum_officinale": 23,
}
TOL = 5e-10


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pearson(x: list[float], y: list[float]) -> float:
    mx, my = stats.mean(x), stats.mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(
        sum(a * a for a in dx) * sum(b * b for b in dy)
    )


def residuals(x: list[float], y: list[float]) -> list[float]:
    mx, my = stats.mean(x), stats.mean(y)
    denom = sum((v - mx) ** 2 for v in x)
    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / denom
    intercept = my - slope * mx
    return [b - (intercept + slope * a) for a, b in zip(x, y)]


def main() -> None:
    for path in (VALUES, EFFECTS, COVARIANCE, SOURCE_MANIFEST, CONTRACT, RESULT, REGISTRY, REGISTRY_STATUS, PAIR_COVERAGE):
        assert path.is_file(), path

    manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["programme_id"] == PROGRAMME
    assert manifest["source_release"] == "jae"
    assert manifest["source_commit"] == "d6361f6874398e797322afe07a8fea85a3c7e927"
    assert manifest["exposure_field"] == "Urban_500"
    assert manifest["source_excluded_garden_ids"] == ["39"]
    assert manifest["effect_outcomes_opened"] is False

    values = rows(VALUES)
    by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in values:
        assert row["programme_id"] == PROGRAMME
        assert row["independent_unit"] == "garden"
        assert row["source_exclusion_status"] == "included_common_frame"
        assert row["garden_id"] != "39"
        by_plant[row["phytometer"]].append(row)

    assert set(by_plant) == set(PLANTS)
    assert {p: len(by_plant[p]) for p in PLANTS} == EXPECTED_N
    for p in PLANTS:
        ids = [r["garden_id"] for r in by_plant[p]]
        assert len(ids) == len(set(ids))

    effects = rows(EFFECTS)
    assert len(effects) == 8
    by_effect = {(r["phytometer"], r["layer"]): r for r in effects}
    assert set(by_effect) == {(p, layer) for p in PLANTS for layer in ("I", "F")}
    assert all(r["programme_id"] == PROGRAMME for r in effects)
    assert all(r["effect_stream"] == "fisher_z_gradient" for r in effects)
    assert all(r["effect_unit_status"] == "fisher_z_admissible" for r in effects)
    assert all(r["independent_unit"] == "garden" for r in effects)
    assert all(r["exposure"] == "Urban_500" for r in effects)

    covariance = json.loads(COVARIANCE.read_text(encoding="utf-8"))
    assert covariance["programme_id"] == PROGRAMME
    assert covariance["exposure"] == "Urban_500"
    assert covariance["source_code_commit"] == manifest["source_commit"]
    blocks = covariance["phytometer_blocks"]
    assert set(blocks) == set(PLANTS)

    for plant in PLANTS:
        rr = sorted(by_plant[plant], key=lambda x: int(x["garden_id"]))
        x = [float(r["Urban_500"]) for r in rr]
        i = [float(r["I_all_pollinator_capture_rate_per_9h"]) for r in rr]
        f = [float(r["F_value"]) for r in rr]
        n = len(rr)

        ri = pearson(x, i)
        rf = pearson(x, f)
        zi = math.atanh(ri)
        zf = math.atanh(rf)
        v = 1.0 / (n - 3)

        ie = by_effect[(plant, "I")]
        fe = by_effect[(plant, "F")]
        assert int(ie["n_independent"]) == int(fe["n_independent"]) == n
        assert abs(float(ie["r"]) - ri) < TOL
        assert abs(float(fe["r"]) - rf) < TOL
        assert abs(float(ie["raw_effect_fisher_z"]) - zi) < TOL
        assert abs(float(fe["raw_effect_fisher_z"]) - zf) < TOL
        assert abs(float(ie["raw_variance"]) - v) < TOL
        assert abs(float(fe["raw_variance"]) - v) < TOL

        ei = residuals(x, i)
        ef = residuals(x, f)
        rho = pearson(ei, ef)
        cov = rho * v

        block = blocks[plant]
        assert block["garden_ids"] == [r["garden_id"] for r in rr]
        assert block["n_independent"] == n
        assert block["positive_definite"] is True
        assert abs(block["I_r"] - ri) < TOL
        assert abs(block["F_r"] - rf) < TOL
        assert abs(block["I_fisher_z"] - zi) < TOL
        assert abs(block["F_fisher_z"] - zf) < TOL
        assert abs(block["residual_correlation_IF"] - rho) < TOL
        assert abs(block["sampling_covariance_proxy_IF"] - cov) < TOL
        assert min(block["eigenvalues_ascending"]) > 0

        delta = zi - zf
        dvar = 2 * v - 2 * cov
        dse = math.sqrt(dvar)
        zstat = delta / dse
        p = math.erfc(abs(zstat) / math.sqrt(2))
        pair = block["I_minus_F"]
        assert abs(pair["delta"] - delta) < TOL
        assert abs(pair["variance"] - dvar) < TOL
        assert abs(pair["se"] - dse) < TOL
        assert abs(pair["z"] - zstat) < TOL
        assert abs(pair["p_two_sided"] - p) < TOL

    registry = {r["programme_id"]: r for r in rows(REGISTRY)}
    assert set(registry) == {"ML015", PROGRAMME, "P2_CF01_MILKWEED_URBAN_2023", "P2_CF01_ACER_MIYABEI_2014", "P2_CF01_CARDIOPETALUM_2012", "P2_CF01_PRITCHARD_2005"}
    z = registry[PROGRAMME]
    assert z["design_stream"] == "fisher_z_gradient_generalisation"
    assert z["independent_unit"] == "garden"
    assert set(z["layers"].split(";")) == {"I", "F"}
    assert int(z["admissible_gradient_effects"]) == 8
    assert z["covariance_status"] == "proxy_reconstructed_phytometer_pair_residual"
    assert z["programme_status"] == "gradient_generalisation_multilayer_cluster"
    assert int(z["primary_hedges_increment"]) == 0

    pair_coverage = {r["pair_id"]: r for r in rows(PAIR_COVERAGE)}
    assert int(pair_coverage["I-F"]["current_independent_direct_systems"]) == 1
    assert pair_coverage["I-F"]["current_system_ids"] == "ML020"
    assert int(pair_coverage["C-F"]["current_independent_direct_systems"]) == 2
    assert int(pair_coverage["G_adult-G_offspring"]["current_independent_direct_systems"]) == 5

    contract = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "retrospective external recovery",
        "Urban_500",
        "all-pollinator capture rate per 9 h",
        "four phytometers are repeated endpoint panels within one programme",
        "does **not** increment the primary Hedges-g I-F programme count",
    ):
        assert token in contract, token

    result = RESULT.read_text(encoding="utf-8")
    for token in (
        "gradient/generalisation multilayer programme",
        "Daucus_carota: n=23",
        "Raphanus_sativus: n=23",
        "Onobrychis_viciifolia: n=20",
        "Symphytum_officinale: n=23",
        "primary Hedges-g programme count increment: **0**",
    ):
        assert token in result, token

    registry_status = REGISTRY_STATUS.read_text(encoding="utf-8")
    for token in (
        "**6 gradient/generalisation programmes**",
        "**19 primary Fisher-z admissible marginal effects**",
        "Zurich contributes **8 Fisher-z admissible marginal effects**",
        "direct I-F coverage remains **1/5**",
    ):
        assert token in registry_status, token

    print(
        "PHASE2_CF01_ZURICH_CHECK_OK "
        "programme=1 phytometers=4 effects=8 covariance_blocks=4 all_PD=true "
        "gradient_programmes=6 primary_Hedges_increment=0"
    )


if __name__ == "__main__":
    main()
