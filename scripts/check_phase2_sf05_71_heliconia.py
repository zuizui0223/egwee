from __future__ import annotations

import csv
import json
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POP = ROOT / "evidence/meta_extraction/phase2_sf05_71_heliconia_population_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_sf05_71_heliconia_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/phase2_sf05_71_heliconia_covariance_v1.json"

TOL = 1e-9


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def hedges_g(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    assert n1 >= 2 and n2 >= 2
    m1, m2 = stats.mean(fragmented), stats.mean(reference)
    s1, s2 = stats.stdev(fragmented), stats.stdev(reference)
    df = n1 + n2 - 2
    pooled = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / df)
    d = (m1 - m2) / pooled
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    variance = 1 / n1 + 1 / n2 + g**2 / (2 * (n1 + n2))
    return g, variance


def group_residuals(values: list[float], groups: list[str]) -> list[float]:
    means = {
        group: stats.mean(v for v, g in zip(values, groups) if g == group)
        for group in set(groups)
    }
    return [v - means[g] for v, g in zip(values, groups)]


def correlation(x: list[float], y: list[float]) -> float:
    mx, my = stats.mean(x), stats.mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(
        sum(a * a for a in dx) * sum(b * b for b in dy)
    )


def det3(m: list[list[float]]) -> float:
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def main() -> None:
    pop = rows(POP)
    assert [r["site"] for r in pop] == ["CF1", "CF2", "F1", "F2", "F3"]
    assert [r["exposure_group"] for r in pop] == [
        "reference", "reference", "fragmented", "fragmented", "fragmented"
    ]
    assert all(r["cluster_id"] == "P2_SF05_71" for r in pop)
    assert all(r["independent_unit_note"] == "site_is_independent_fragmentation_unit" for r in pop)

    endpoint_columns = {
        "C": "C_father_outside_pct",
        "G_adult": "G_adult_reproductive_UHe",
        "G_offspring": "G_offspring_seedling_UHe",
    }
    effect_rows = {r["layer"]: r for r in rows(EFFECTS)}
    assert set(effect_rows) == set(endpoint_columns)

    groups = [r["exposure_group"] for r in pop]
    effects: dict[str, tuple[float, float]] = {}
    residuals: dict[str, list[float]] = {}

    for layer, column in endpoint_columns.items():
        values = [float(r[column]) for r in pop]
        fragmented = [v for v, group in zip(values, groups) if group == "fragmented"]
        reference = [v for v, group in zip(values, groups) if group == "reference"]
        g, variance = hedges_g(fragmented, reference)
        effects[layer] = (g, variance)
        residuals[layer] = group_residuals(values, groups)

        row = effect_rows[layer]
        assert row["effect_stream"] == "hedges_g_fragmented_minus_reference"
        assert row["effect_unit_status"] == "g_admissible"
        assert row["independent_unit"] == "site"
        assert int(row["n_fragmented"]) == 3
        assert int(row["n_reference"]) == 2
        assert row["fragmented_group"] == "F1;F2;F3"
        assert row["reference_group"] == "CF1;CF2"
        assert int(row["orientation_multiplier"]) == 1
        assert abs(float(row["raw_effect"]) - g) < TOL
        assert abs(float(row["raw_variance"]) - variance) < TOL
        assert abs(float(row["oriented_effect"]) - g) < TOL
        assert abs(float(row["oriented_variance"]) - variance) < TOL

    cov = json.loads(COV.read_text(encoding="utf-8"))
    labels = cov["endpoints"]
    assert labels == ["C", "G_adult", "G_offspring"]

    reconstructed_r = [
        [correlation(residuals[a], residuals[b]) for b in labels]
        for a in labels
    ]
    stored_r = cov["residual_correlation_matrix"]
    for i in range(3):
        for j in range(3):
            assert abs(reconstructed_r[i][j] - stored_r[i][j]) < TOL

    variances = [effects[layer][1] for layer in labels]
    reconstructed_v = [
        [
            reconstructed_r[i][j] * math.sqrt(variances[i] * variances[j])
            for j in range(3)
        ]
        for i in range(3)
    ]
    stored_v = cov["working_covariance_matrix"]
    for i in range(3):
        for j in range(3):
            assert abs(reconstructed_v[i][j] - stored_v[i][j]) < TOL

    full_det = det3(reconstructed_v)
    assert full_det > 0
    assert reconstructed_v[0][0] > 0
    assert reconstructed_v[0][0] * reconstructed_v[1][1] - reconstructed_v[0][1] ** 2 > 0
    assert cov["full_three_layer"]["positive_definite"] is True
    assert cov["full_three_layer"]["status"] == "full_three_layer_covariance_admissible"
    assert abs(cov["full_three_layer"]["determinant"] - full_det) < TOL

    pair = cov["primary_pair"]
    assert pair["pair_id"] == "G_adult-G_offspring"
    pair_v = pair["covariance_matrix"]
    expected_pair_cov = reconstructed_r[1][2] * math.sqrt(
        effects["G_adult"][1] * effects["G_offspring"][1]
    )
    assert abs(pair_v[0][1] - expected_pair_cov) < TOL
    pair_det = pair_v[0][0] * pair_v[1][1] - pair_v[0][1] ** 2
    assert pair_det > 0
    assert pair["positive_definite"] is True
    assert pair["status"] == "pair_covariance_admissible"

    admission = cov["admission"]
    assert admission["pair_specific_admissible"] == ["G_adult-G_offspring"]
    assert admission["full_three_layer_joint_cluster_admissible"] is True
    assert admission["phase1_baseline_changed"] is False

    print(
        "PHASE2_SF05_71_HELICONIA_OK "
        "effects=3 full3_covariance=PD pair=G_adult-G_offspring "
        "pair_covariance=PD phase1_unchanged=true"
    )


if __name__ == "__main__":
    main()
