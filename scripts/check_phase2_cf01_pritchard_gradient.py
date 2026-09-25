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
REGISTRY = ROOT / "evidence/meta_extraction/phase2_gradient_programme_registry_v1.csv"
REGISTRY_STATUS = ROOT / "manuscript/PHASE2_GRADIENT_PROGRAMME_REGISTRY_2026-09-24.md"
COMPLETION = ROOT / "manuscript/PHASE2_CF01_COVERAGE_COMPLETION_2026-09-25.md"

PROGRAMME = "P2_CF01_PRITCHARD_2005"
TOL = 5e-10
I_R2 = 0.573
I_N = 9
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
    for p in (VALUES, EFFECTS, DEPENDENCE, RULE, RESULT, REGISTRY, REGISTRY_STATUS, COMPLETION):
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
    assert all(r["programme_id"] == PROGRAMME for r in vals)

    r_i = -math.sqrt(I_R2)
    z_i = math.atanh(r_i)
    v_i = 1.0 / (I_N - 3)

    x = [math.log(d) for _, d, _ in got]
    y_log = [math.log(y) for _, _, y in got]
    y_raw = [y for _, _, y in got]
    r_f = pearson(x, y_log)
    z_f = math.atanh(r_f)
    v_f = 1.0 / (len(got) - 3)
    r_f_raw = pearson(x, y_raw)
    z_f_raw = math.atanh(r_f_raw)

    effects = {r["endpoint_role"]: r for r in rows(EFFECTS)}
    assert set(effects) == {"I_primary", "F_primary", "F_sensitivity_raw_proportion"}

    for role, expected in (
        ("I_primary", (I_N, r_i, z_i, v_i, "primary")),
        ("F_primary", (5, r_f, z_f, v_f, "primary")),
        ("F_sensitivity_raw_proportion", (5, r_f_raw, z_f_raw, v_f, "sensitivity")),
    ):
        row = effects[role]
        assert row["programme_id"] == PROGRAMME
        assert row["effect_stream"] == "fisher_z_gradient"
        assert row["exposure"] == "log_distance_to_rainforest_km"
        assert int(row["n_independent"]) == expected[0]
        assert abs(float(row["r"]) - expected[1]) < TOL
        assert abs(float(row["fisher_z"]) - expected[2]) < TOL
        assert abs(float(row["variance"]) - expected[3]) < TOL
        assert row["primary_or_sensitivity"] == expected[4]

    dep = json.loads(DEPENDENCE.read_text(encoding="utf-8"))
    assert dep["programme_id"] == PROGRAMME
    assert dep["status"] == "gradient_generalisation_multilayer_cluster_retrospective_cluster_robust"
    assert dep["independent_unit"] == "orchard_site"
    assert dep["I_frame_n"] == 9
    assert dep["F_frame_n"] == 5
    assert dep["F_is_explicit_subset_of_I"] is True
    assert dep["F_orchards"] == [x[0] for x in EXPECTED_F]
    assert dep["I_numeric_orchard_vector_publicly_recoverable"] is False
    assert dep["paired_covariance_reconstructable"] is False
    assert dep["covariance_status"] == "cluster_robust_fallback_overlap_5_of_9_no_pair_covariance"
    assert dep["within_programme_I_minus_F_test_calculated"] is False
    assert dep["primary_hedges_increment"] == 0
    assert dep["retrospective_recovery"] is True

    registry = {r["programme_id"]: r for r in rows(REGISTRY)}
    assert set(registry) == {
        "ML015",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
        "P2_CF01_ACER_MIYABEI_2014",
        "P2_CF01_CARDIOPETALUM_2012",
        PROGRAMME,
    }
    p = registry[PROGRAMME]
    assert p["design_stream"] == "fisher_z_gradient_generalisation"
    assert p["independent_unit"] == "orchard_site_with_nested_frames"
    assert set(p["layers"].split(";")) == {"I", "F"}
    assert int(p["admissible_gradient_effects"]) == 2
    assert p["covariance_status"] == "cluster_robust_fallback_overlap_5_of_9_no_pair_covariance"
    assert p["programme_status"] == "gradient_generalisation_multilayer_cluster_retrospective_cluster_robust"
    assert int(p["primary_hedges_increment"]) == 0

    rule = RULE.read_text(encoding="utf-8")
    for token in (
        "retrospective external recovery",
        "n = 9 orchards",
        "R² = 0.573",
        "five orchards are an explicit subset",
        "cluster-robust fallback",
        "set unknown covariance to zero",
        "claim causal rainforest-distance effects",
    ):
        assert token in rule, token

    result = RESULT.read_text(encoding="utf-8")
    for token in (
        "Fisher z = **−0.989**",
        "Fisher z = **−1.490**",
        "n = **9 orchards**",
        "n = **5 orchards**",
        "cluster-robust fallback",
        "does not change direct I-F coverage",
    ):
        assert token in result, token

    status = REGISTRY_STATUS.read_text(encoding="utf-8")
    for token in (
        "**6 gradient/generalisation programmes**",
        "**19 primary Fisher-z admissible marginal effects**",
        "**P2_CF01_PRITCHARD_2005 — custard apple**",
        "cluster-robust fallback",
        "19 primary Fisher-z",
    ):
        assert token in status, token

    completion = COMPLETION.read_text(encoding="utf-8")
    for token in (
        "screened: **360 / 360**",
        "6 programmes / 19 primary Fisher-z marginal",
        "Pritchard custard-apple orchard isolation from rainforest",
        "cluster-robust fallback",
        "search-completion stopping rule",
    ):
        assert token in completion, token

    print(
        "PHASE2_CF01_PRITCHARD_CHECK_OK "
        f"I_n=9 I_z={z_i:.8f} F_n=5 F_z={z_f:.8f} "
        "gradient_programmes=6 covariance=cluster_robust_fallback "
        "direct_IF_increment=0 retrospective=true"
    )


if __name__ == "__main__":
    main()
