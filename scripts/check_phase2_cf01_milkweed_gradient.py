from __future__ import annotations

import csv
import json
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALUES = ROOT / "evidence/meta_extraction/phase2_cf01_milkweed_urban_population_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_milkweed_urban_gradient_effects_v1.csv"
COVARIANCE = ROOT / "evidence/meta_extraction/phase2_cf01_milkweed_urban_gradient_covariance_v1.json"
MANIFEST = ROOT / "evidence/meta_extraction/phase2_cf01_milkweed_urban_source_manifest_v1.json"
CONTRACT = ROOT / "manuscript/CF01_MILKWEED_URBAN_2023_GRADIENT_RECOVERY_CONTRACT.md"
RESULT = ROOT / "manuscript/PHASE2_CF01_MILKWEED_URBAN_GRADIENT_RECOVERY_2026-09-24.md"
REGISTRY = ROOT / "evidence/meta_extraction/phase2_gradient_programme_registry_v1.csv"
REGISTRY_STATUS = ROOT / "manuscript/PHASE2_GRADIENT_PROGRAMME_REGISTRY_2026-09-24.md"
PAIR_COVERAGE = ROOT / "evidence/meta_extraction/coverage_expansion_pair_coverage_v1.csv"

PROGRAMME = "P2_CF01_MILKWEED_URBAN_2023"
SOURCE_COMMIT = "83e56d790410a134fa099425459aefb6f2d07f12"
ZERO_PATCHES = {"MW011", "MW028", "MW040", "MW041", "MW042", "MW061", "MW074"}
TOL = 5e-10
Z95 = 1.959963984540054


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


def calculate(rr: list[dict[str, str]]) -> dict[str, float]:
    x = [float(r["greater_urbanization_negative_city_dist"]) for r in rr]
    i = [float(r["I_pollinator_abundance_per_surveyed_plant"]) for r in rr]
    f = [float(r["F_mean_follicles_per_inflorescence"]) for r in rr]
    n = len(rr)
    ri = pearson(x, i)
    rf = pearson(x, f)
    zi = math.atanh(ri)
    zf = math.atanh(rf)
    variance = 1.0 / (n - 3)
    rho = pearson(residuals(x, i), residuals(x, f))
    covariance = rho * variance
    delta = zi - zf
    dvar = 2 * variance - 2 * covariance
    dse = math.sqrt(dvar)
    z = delta / dse
    p = math.erfc(abs(z) / math.sqrt(2))
    return {
        "n": n,
        "I_r": ri,
        "F_r": rf,
        "I_z": zi,
        "F_z": zf,
        "variance": variance,
        "rho": rho,
        "covariance": covariance,
        "delta": delta,
        "delta_variance": dvar,
        "delta_se": dse,
        "z": z,
        "p": p,
        "ci_low": delta - Z95 * dse,
        "ci_high": delta + Z95 * dse,
    }


def main() -> None:
    for path in (VALUES, EFFECTS, COVARIANCE, MANIFEST, CONTRACT, RESULT, REGISTRY, REGISTRY_STATUS, PAIR_COVERAGE):
        assert path.is_file(), path

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["programme_id"] == PROGRAMME
    assert manifest["source_repository"] == "sbreitbart/observ_study_phenotype"
    assert manifest["source_commit"] == SOURCE_COMMIT
    assert manifest["article_doi"] == "10.1007/s11252-022-01278-9"
    assert manifest["archive_doi"] == "10.5281/zenodo.6985410"
    assert manifest["primary_year"] == 2019
    assert manifest["independent_unit"] == "population_patch"
    assert manifest["primary_common_populations"] == 31
    assert manifest["zero_retaining_sensitivity_populations"] == 38
    assert set(manifest["zero_pollinator_common_patches"]) == ZERO_PATCHES
    assert manifest["primary_direct_Hedges_increment"] == 0
    assert manifest["effect_outcomes_opened"] is True

    values = rows(VALUES)
    assert len(values) == 38
    assert all(r["programme_id"] == PROGRAMME for r in values)
    assert all(r["year"] == "2019" for r in values)
    assert all(r["independent_unit"] == "population_patch" for r in values)
    assert len({r["patch_id"] for r in values}) == 38
    primary_rows = [r for r in values if r["primary_source_code_frame"] == "yes"]
    zero_rows = [r for r in values if r["I_pollinator_abundance_per_surveyed_plant"] == "0.000000000000"]
    assert len(primary_rows) == 31
    assert {r["patch_id"] for r in zero_rows} == ZERO_PATCHES
    assert all(r["zero_pollinator_sensitivity_only"] == "yes" for r in zero_rows)
    assert all(int(r["n_F_plants"]) > 0 for r in values)

    primary = calculate(primary_rows)
    sensitivity = calculate(values)
    assert primary["n"] == 31
    assert sensitivity["n"] == 38

    effects = {(r["analysis_frame"], r["layer"]): r for r in rows(EFFECTS)}
    assert set(effects) == {
        ("primary_source_code_nonzero", "I"),
        ("primary_source_code_nonzero", "F"),
        ("zero_pollinator_retaining_sensitivity", "I"),
        ("zero_pollinator_retaining_sensitivity", "F"),
    }

    for frame, calc, expected_status in (
        ("primary_source_code_nonzero", primary, "fisher_z_admissible"),
        ("zero_pollinator_retaining_sensitivity", sensitivity, "sensitivity_only"),
    ):
        for layer, rkey, zkey in (("I", "I_r", "I_z"), ("F", "F_r", "F_z")):
            row = effects[(frame, layer)]
            assert row["programme_id"] == PROGRAMME
            assert int(row["n_independent"]) == calc["n"]
            assert row["independent_unit"] == "population_patch"
            assert row["effect_unit_status"] == expected_status
            assert abs(float(row["r"]) - calc[rkey]) < TOL
            assert abs(float(row["raw_effect_fisher_z"]) - calc[zkey]) < TOL
            assert abs(float(row["raw_variance"]) - calc["variance"]) < TOL
            assert abs(float(row["oriented_effect"]) - calc[zkey]) < TOL
            assert abs(float(row["oriented_variance"]) - calc["variance"]) < TOL

    cov = json.loads(COVARIANCE.read_text(encoding="utf-8"))
    assert cov["programme_id"] == PROGRAMME
    for block_name, calc in (
        ("primary_source_code_nonzero", primary),
        ("zero_pollinator_retaining_sensitivity", sensitivity),
    ):
        block = cov[block_name]
        assert block["n_independent"] == calc["n"]
        assert block["positive_definite"] is True
        assert min(block["eigenvalues_ascending"]) > 0
        assert abs(block["I_r"] - calc["I_r"]) < TOL
        assert abs(block["F_r"] - calc["F_r"]) < TOL
        assert abs(block["I_fisher_z"] - calc["I_z"]) < TOL
        assert abs(block["F_fisher_z"] - calc["F_z"]) < TOL
        assert abs(block["residual_correlation_IF"] - calc["rho"]) < TOL
        assert abs(block["sampling_covariance_proxy_IF"] - calc["covariance"]) < TOL
        pair = block["I_minus_F"]
        assert abs(pair["delta"] - calc["delta"]) < TOL
        assert abs(pair["variance"] - calc["delta_variance"]) < TOL
        assert abs(pair["se"] - calc["delta_se"]) < TOL
        assert abs(pair["z"] - calc["z"]) < TOL
        assert abs(pair["ci95"][0] - calc["ci_low"]) < TOL
        assert abs(pair["ci95"][1] - calc["ci_high"]) < TOL
        assert calc["ci_low"] < 0 < calc["ci_high"]

    registry = {r["programme_id"]: r for r in rows(REGISTRY)}
    assert set(registry) == {"ML015", "P2_CF01_ZURICH_2026", PROGRAMME, "P2_CF01_ACER_MIYABEI_2014"}
    milk = registry[PROGRAMME]
    assert milk["design_stream"] == "fisher_z_gradient_generalisation"
    assert milk["independent_unit"] == "population_patch"
    assert set(milk["layers"].split(";")) == {"I", "F"}
    assert int(milk["admissible_gradient_effects"]) == 2
    assert milk["covariance_status"] == "proxy_reconstructed_population_pair_residual"
    assert milk["programme_status"] == "gradient_generalisation_multilayer_cluster"
    assert int(milk["primary_hedges_increment"]) == 0

    pair = {r["pair_id"]: r for r in rows(PAIR_COVERAGE)}
    assert int(pair["I-F"]["current_independent_direct_systems"]) == 1
    assert pair["I-F"]["current_system_ids"] == "ML020"
    assert int(pair["C-F"]["current_independent_direct_systems"]) == 2
    assert int(pair["G_adult-G_offspring"]["current_independent_direct_systems"]) == 5

    contract = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "retrospective external recovery",
        "greater_urbanization = - City_dist_km",
        "population-level total pollinator abundance per surveyed plant in 2019",
        "fruit set, mean follicles per inflorescence",
        "retaining surveyed populations with zero pollinator abundance",
        "does **not** increment the primary fragmented-versus-reference Hedges-g I-F denominator",
    ):
        assert token in contract, token

    result = RESULT.read_text(encoding="utf-8")
    for token in (
        "31 common populations",
        "38 common populations",
        "third",
        "primary direct I-F denominator remains **1/5",
        "interval crosses zero",
    ):
        assert token in result, token

    status = REGISTRY_STATUS.read_text(encoding="utf-8")
    for token in (
        "**4 gradient/generalisation programmes**",
        "**15 primary Fisher-z admissible marginal effects**",
        "**31 populations**",
        "**38 populations**",
        "direct I-F coverage remains **1/5**",
    ):
        assert token in status, token

    print(
        "PHASE2_CF01_MILKWEED_CHECK_OK "
        f"primary_n={primary['n']} sensitivity_n={sensitivity['n']} "
        f"I_z={primary['I_z']:.8f} F_z={primary['F_z']:.8f} "
        f"delta={primary['delta']:.8f} p={primary['p']:.8f} "
        f"sensitivity_delta={sensitivity['delta']:.8f} sensitivity_p={sensitivity['p']:.8f} "
        "gradient_programmes=4 direct_IF=1/5"
    )


if __name__ == "__main__":
    main()
