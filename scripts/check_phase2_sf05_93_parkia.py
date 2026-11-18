from __future__ import annotations

import csv
import json
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POP = ROOT / "evidence/meta_extraction/phase2_sf05_93_parkia_population_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_sf05_93_parkia_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/phase2_sf05_93_parkia_covariance_v1.json"

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


def correlation(x: list[float], y: list[float]) -> float:
    mx, my = stats.mean(x), stats.mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    num = sum(a * b for a, b in zip(dx, dy))
    den = math.sqrt(sum(a * a for a in dx) * sum(b * b for b in dy))
    return num / den


def group_residuals(values: list[float], groups: list[str]) -> list[float]:
    means = {
        group: stats.mean(v for v, g in zip(values, groups) if g == group)
        for group in set(groups)
    }
    return [v - means[g] for v, g in zip(values, groups)]


def det3(m: list[list[float]]) -> float:
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def main() -> None:
    pop = rows(POP)
    assert [r["population"] for r in pop] == ["Saki", "Cassou", "Walley", "Vouza"]
    assert [r["exposure_group"] for r in pop] == ["reference", "reference", "fragmented", "fragmented"]
    assert all(r["cluster_id"] == "P2_SF05_93" for r in pop)
    assert all(r["independent_unit_note"] == "population_is_independent_fragmentation_unit" for r in pop)

    endpoint_columns = {
        "C": "C_pollen_immigration_pct",
        "G_adult": "G_adult_large_HE",
        "G_offspring": "G_offspring_embryo_HE",
    }
    effect_rows = {r["layer"]: r for r in rows(EFFECTS)}
    assert set(effect_rows) == set(endpoint_columns)

    groups = [r["exposure_group"] for r in pop]
    effects: dict[str, tuple[float, float]] = {}
    residuals: dict[str, list[float]] = {}

    for layer, column in endpoint_columns.items():
        values = [float(r[column]) for r in pop]
        fragmented = [v for v, g in zip(values, groups) if g == "fragmented"]
        reference = [v for v, g in zip(values, groups) if g == "reference"]
        g, variance = hedges_g(fragmented, reference)
        effects[layer] = (g, variance)
        residuals[layer] = group_residuals(values, groups)

        row = effect_rows[layer]
        assert row["effect_stream"] == "hedges_g_fragmented_minus_reference"
        assert row["effect_unit_status"] == "g_admissible"
        assert row["independent_unit"] == "population"
        assert int(row["n_fragmented"]) == 2
        assert int(row["n_reference"]) == 2
        assert row["fragmented_group"] == "Walley;Vouza"
        assert row["reference_group"] == "Saki;Cassou"
        assert int(row["orientation_multiplier"]) == 1
        assert abs(float(row["raw_effect"]) - g) < TOL
        assert abs(float(row["raw_variance"]) - variance) < TOL
        assert abs(float(row["oriented_effect"]) - g) < TOL
        assert abs(float(row["oriented_variance"]) - variance) < TOL

    cov = json.loads(COV.read_text(encoding="utf-8"))
    assert cov["cluster_id"] == "P2_SF05_93"
    assert cov["endpoints"] == ["C", "G_adult", "G_offspring"]

    labels = cov["endpoints"]
    reconstructed_r = []
    for a in labels:
        reconstructed_r.append([correlation(residuals[a], residuals[b]) for b in labels])

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
    assert abs(full_det) < 1e-10
    assert cov["full_three_layer"]["numerical_rank"] == 2
    assert cov["full_three_layer"]["status"] == "rank_deficient_not_used_for_joint_inversion"

    pair = cov["primary_pair"]
    assert pair["pair_id"] == "G_adult-G_offspring"
    pair_v = pair["covariance_matrix"]
    assert abs(pair_v[0][0] - effects["G_adult"][1]) < TOL
    assert abs(pair_v[1][1] - effects["G_offspring"][1]) < TOL
    expected_pair_cov = reconstructed_r[1][2] * math.sqrt(
        effects["G_adult"][1] * effects["G_offspring"][1]
    )
    assert abs(pair_v[0][1] - expected_pair_cov) < TOL
    assert abs(pair_v[1][0] - expected_pair_cov) < TOL
    pair_det = pair_v[0][0] * pair_v[1][1] - pair_v[0][1] ** 2
    assert pair_v[0][0] > 0 and pair_det > 0
    assert pair["positive_definite"] is True
    assert pair["status"] == "pair_covariance_admissible"

    diff = effects["G_adult"][0] - effects["G_offspring"][0]
    diff_var = effects["G_adult"][1] + effects["G_offspring"][1] - 2 * expected_pair_cov
    assert abs(pair["effect_difference_Gadult_minus_Goffspring"] - diff) < TOL
    assert abs(pair["difference_variance"] - diff_var) < TOL

    admission = cov["admission"]
    assert admission["pair_specific_admissible"] == ["G_adult-G_offspring"]
    assert admission["full_three_layer_joint_cluster_admissible"] is False
    assert admission["phase1_baseline_changed"] is False

    print(
        "PHASE2_SF05_93_PARKIA_OK "
        f"effects={len(effect_rows)} pair=G_adult-G_offspring "
        "pair_covariance=PD full3=rank_deficient phase1_unchanged=true"
    )


if __name__ == "__main__":
    main()
