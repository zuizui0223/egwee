from __future__ import annotations

import csv
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence/meta_extraction/phase2_sf05_parkia_source_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_sf05_parkia_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/phase2_sf05_parkia_pairwise_covariance_v1.csv"
CONTRAST = ROOT / "evidence/meta_extraction/phase2_sf05_parkia_cohort_contrast_v1.csv"
CONTRACT = ROOT / "manuscript/PARKIA_2020_PHASE2_RECOVERY_CONTRACT.md"
RESULT = ROOT / "manuscript/PHASE2_SF05_PARKIA_RECOVERY_RESULT_2026-09-19.md"

ENDPOINTS = ["C_mp", "Gadult_Ho", "Goffspring_Ho"]
POPS = ["Saki", "Cassou", "Walley", "Vouza"]
GROUP = {"Saki": "NCP", "Cassou": "NCP", "Walley": "CP", "Vouza": "CP"}
Z95 = 1.959963984540054


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def hedges_g(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    df = n1 + n2 - 2
    pooled = math.sqrt(
        ((n1 - 1) * stats.stdev(fragmented) ** 2 + (n2 - 1) * stats.stdev(reference) ** 2) / df
    )
    d = (stats.mean(fragmented) - stats.mean(reference)) / pooled
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    variance = 1 / n1 + 1 / n2 + g**2 / (2 * (n1 + n2))
    return g, variance


def pearson(x: list[float], y: list[float]) -> float:
    mx, my = stats.mean(x), stats.mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(
        sum(a * a for a in dx) * sum(b * b for b in dy)
    )


def centered(values: dict[str, float]) -> list[float]:
    means = {
        group: stats.mean(values[p] for p in POPS if GROUP[p] == group)
        for group in {"CP", "NCP"}
    }
    return [values[p] - means[GROUP[p]] for p in POPS]


def matrix_rank(matrix: list[list[float]], tol: float = 1e-10) -> int:
    a = [row[:] for row in matrix]
    m, n = len(a), len(a[0])
    rank = 0
    col = 0
    while rank < m and col < n:
        pivot = max(range(rank, m), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) <= tol:
            col += 1
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pivot_value = a[rank][col]
        for j in range(col, n):
            a[rank][j] /= pivot_value
        for r in range(m):
            if r == rank:
                continue
            factor = a[r][col]
            if abs(factor) <= tol:
                continue
            for j in range(col, n):
                a[r][j] -= factor * a[rank][j]
        rank += 1
        col += 1
    return rank


def main() -> None:
    for path in (SOURCE, EFFECTS, COV, CONTRAST, CONTRACT, RESULT):
        assert path.is_file(), path

    source_rows = rows(SOURCE)
    assert len(source_rows) == 12
    assert {r["population"] for r in source_rows} == set(POPS)
    assert all(r["independent_unit"] == "population" for r in source_rows)
    assert all(int(r["orientation_multiplier"]) == 1 for r in source_rows)

    endpoint_key = {
        ("C", "pollen_immigration_rate_percent"): "C_mp",
        ("G_adult", "large_tree_observed_heterozygosity_Ho"): "Gadult_Ho",
        ("G_offspring", "embryo_observed_heterozygosity_Ho"): "Goffspring_Ho",
    }
    raw: dict[str, dict[str, float]] = {e: {} for e in ENDPOINTS}
    for r in source_rows:
        endpoint = endpoint_key[(r["layer"], r["endpoint"])]
        raw[endpoint][r["population"]] = float(r["value"])

    assert raw == {
        "C_mp": {"Saki": 74.0, "Cassou": 34.0, "Walley": 46.0, "Vouza": 48.0},
        "Gadult_Ho": {"Saki": 0.78, "Cassou": 0.79, "Walley": 0.80, "Vouza": 0.81},
        "Goffspring_Ho": {"Saki": 0.76, "Cassou": 0.79, "Walley": 0.80, "Vouza": 0.80},
    }

    effects = {r["endpoint_id"]: r for r in rows(EFFECTS)}
    assert set(effects) == set(ENDPOINTS)
    variances: dict[str, float] = {}
    effect_values: dict[str, float] = {}
    for endpoint in ENDPOINTS:
        frag = [raw[endpoint][p] for p in POPS if GROUP[p] == "CP"]
        ref = [raw[endpoint][p] for p in POPS if GROUP[p] == "NCP"]
        g, variance = hedges_g(frag, ref)
        row = effects[endpoint]
        assert row["programme_id"] == "PH2_PARKIA_2020"
        assert row["effect_unit_status"] == "g_admissible"
        assert row["independent_unit"] == "population"
        assert int(row["n_independent_fragmented"]) == 2
        assert int(row["n_independent_reference"]) == 2
        assert int(row["orientation_multiplier"]) == 1
        assert abs(float(row["fragmented_mean"]) - stats.mean(frag)) < 1e-12
        assert abs(float(row["fragmented_sd"]) - stats.stdev(frag)) < 1e-12
        assert abs(float(row["reference_mean"]) - stats.mean(ref)) < 1e-12
        assert abs(float(row["reference_sd"]) - stats.stdev(ref)) < 1e-12
        assert abs(float(row["raw_effect"]) - g) < 1e-9
        assert abs(float(row["raw_variance"]) - variance) < 1e-9
        assert abs(float(row["oriented_effect"]) - g) < 1e-9
        assert abs(float(row["oriented_variance"]) - variance) < 1e-9
        effect_values[endpoint] = g
        variances[endpoint] = variance

    cov_rows = rows(COV)
    assert len(cov_rows) == 9
    cov_by_pair = {(r["endpoint_i"], r["endpoint_j"]): r for r in cov_rows}
    assert set(cov_by_pair) == {(a, b) for a in ENDPOINTS for b in ENDPOINTS}
    matrix: list[list[float]] = []
    for a in ENDPOINTS:
        row_values: list[float] = []
        for b in ENDPOINTS:
            rho = pearson(centered(raw[a]), centered(raw[b]))
            covariance = rho * math.sqrt(variances[a] * variances[b])
            row = cov_by_pair[(a, b)]
            assert row["covariance_status"] == "proxy_pairwise_low_rank"
            assert int(row["n_paired_populations"]) == 4
            assert int(row["residual_df"]) == 2
            assert abs(float(row["correlation_proxy"]) - rho) < 1e-9
            assert abs(float(row["sampling_covariance"]) - covariance) < 1e-9
            row_values.append(float(row["sampling_covariance"]))
        matrix.append(row_values)
    assert matrix_rank(matrix) == 2

    contrast_rows = rows(CONTRAST)
    assert len(contrast_rows) == 1
    row = contrast_rows[0]
    assert row["contrast"] == "Gadult_minus_Goffspring"
    covariance = float(cov_by_pair[("Gadult_Ho", "Goffspring_Ho")]["sampling_covariance"])
    delta = effect_values["Gadult_Ho"] - effect_values["Goffspring_Ho"]
    variance = variances["Gadult_Ho"] + variances["Goffspring_Ho"] - 2 * covariance
    se = math.sqrt(variance)
    z = delta / se
    p = math.erfc(abs(z) / math.sqrt(2))
    lo, hi = delta - Z95 * se, delta + Z95 * se
    assert abs(float(row["delta_a_minus_b"]) - delta) < 1e-9
    assert abs(float(row["covariance"]) - covariance) < 1e-9
    assert abs(float(row["delta_variance"]) - variance) < 1e-9
    assert abs(float(row["delta_se"]) - se) < 1e-9
    assert abs(float(row["z"]) - z) < 1e-9
    assert abs(float(row["p_two_sided"]) - p) < 1e-9
    assert abs(float(row["ci95_low"]) - lo) < 1e-9
    assert abs(float(row["ci95_high"]) - hi) < 1e-9
    assert lo < 0 < hi

    contract = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "retrospective external recovery",
        "CP - NCP",
        "population",
        "pollen immigration rate",
        "observed heterozygosity",
        "G_adult - G_offspring",
        "rank-deficient",
    ):
        assert token in contract

    result = RESULT.read_text(encoding="utf-8")
    for token in (
        "g = -0.19975047",
        "g = +1.61624407",
        "g = +0.95238095",
        "p = 0.43438897",
        "increases direct `G_adult-G_offspring` programme coverage from **1 to 2**",
    ):
        assert token in result

    print(
        "PHASE2_SF05_PARKIA_OK "
        f"C={effect_values['C_mp']:.8f} "
        f"Gadult={effect_values['Gadult_Ho']:.8f} "
        f"Goffspring={effect_values['Goffspring_Ho']:.8f} "
        f"Gadult_minus_Goffspring_p={p:.8f} covariance_rank=2"
    )


if __name__ == "__main__":
    main()
