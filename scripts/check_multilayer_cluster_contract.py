from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "evidence/meta_extraction/PS003_serapias_site_table_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/PS003_serapias_primary_covariance_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-12_MULTILAYER_CLUSTERS.md"

ENDPOINTS = ["F_fruit_set", "C_pollen_immigration", "G_adult_Ho"]
SITE_COLUMNS = {
    "F_fruit_set": "fruit_set_pct",
    "C_pollen_immigration": "pollen_immigration_pct",
    "G_adult_Ho": "observed_heterozygosity",
}
EFFECT_ENDPOINTS = {
    "F_fruit_set": "fruit_set",
    "C_pollen_immigration": "pollen_immigration_rate",
    "G_adult_Ho": "observed_heterozygosity",
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pearson(x: list[float], y: list[float]) -> float:
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    num = sum(a * b for a, b in zip(dx, dy))
    den = math.sqrt(sum(a * a for a in dx) * sum(b * b for b in dy))
    return num / den


def group_centered(site_rows: list[dict[str, str]], column: str) -> list[float]:
    means: dict[str, float] = {}
    for group in {r["exposure_group"] for r in site_rows}:
        vals = [float(r[column]) for r in site_rows if r["exposure_group"] == group]
        means[group] = sum(vals) / len(vals)
    return [float(r[column]) - means[r["exposure_group"]] for r in site_rows]


def cholesky_positive_definite(matrix: list[list[float]]) -> bool:
    n = len(matrix)
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                value = matrix[i][i] - s
                if value <= 1e-12:
                    return False
                lower[i][j] = math.sqrt(value)
            else:
                lower[i][j] = (matrix[i][j] - s) / lower[j][j]
    return True


def main() -> None:
    for path in (SITE, EFFECTS, COV, REGISTRY, AMENDMENT):
        assert path.is_file(), path

    amendment = AMENDMENT.read_text(encoding="utf-8")
    assert "one cluster with three correlated outcomes" in amendment
    assert "Do not set covariance to zero" in amendment
    assert "at least two independent admissible multilayer clusters" in amendment

    site = rows(SITE)
    assert len(site) == 9
    assert sum(r["exposure_group"] == "anthropic" for r in site) == 3
    assert sum(r["exposure_group"] == "natural" for r in site) == 6

    effects = rows(EFFECTS)
    primary = [r for r in effects if r["primary_or_sensitivity"] == "primary"]
    assert len(primary) == 3
    assert {r["layer"] for r in primary} == {"C", "F", "G_adult"}
    assert {r["contrast"] for r in primary} == {"predefined_anthropic_vs_natural"}
    assert {r["fragmented_group"] for r in primary} == {"C;F;G"}
    assert {r["reference_group"] for r in primary} == {"A;B;D;E;H;I"}
    assert all(int(r["n_fragmented"]) == 3 and int(r["n_reference"]) == 6 for r in primary)
    assert any(r["endpoint"] == "fixation_index_FIS" and r["primary_or_sensitivity"] == "sensitivity" for r in effects)

    effect_by_endpoint = {r["endpoint"]: r for r in primary}
    variances = {
        key: float(effect_by_endpoint[EFFECT_ENDPOINTS[key]]["oriented_variance"])
        for key in ENDPOINTS
    }

    centered = {
        endpoint: group_centered(site, SITE_COLUMNS[endpoint])
        for endpoint in ENDPOINTS
    }
    correlation = {
        (a, b): pearson(centered[a], centered[b])
        for a in ENDPOINTS
        for b in ENDPOINTS
    }

    cov_rows = rows(COV)
    assert len(cov_rows) == 9
    by_pair = {(r["endpoint_i"], r["endpoint_j"]): r for r in cov_rows}
    assert set(by_pair) == {(a, b) for a in ENDPOINTS for b in ENDPOINTS}

    matrix: list[list[float]] = []
    for a in ENDPOINTS:
        row_values: list[float] = []
        for b in ENDPOINTS:
            r = by_pair[(a, b)]
            expected_r = correlation[(a, b)]
            expected_cov = expected_r * math.sqrt(variances[a] * variances[b])
            assert r["cluster_id"] == "ML001"
            assert r["study_id"] == "PS003"
            assert int(r["n_paired_units"]) == 9
            assert r["covariance_status"] == "proxy_reconstructed"
            assert abs(float(r["correlation_proxy"]) - expected_r) < 1e-9
            assert abs(float(r["sampling_covariance"]) - expected_cov) < 1e-9
            row_values.append(float(r["sampling_covariance"]))
        matrix.append(row_values)

    for i in range(3):
        for j in range(3):
            assert abs(matrix[i][j] - matrix[j][i]) < 1e-12
    assert cholesky_positive_definite(matrix), matrix

    registry = rows(REGISTRY)
    by_cluster = {r["cluster_id"]: r for r in registry}
    assert len(by_cluster) == len(registry)
    assert set(by_cluster) >= {"ML001", "ML002", "ML003", "ML004", "ML005", "ML006"}

    serapias = by_cluster["ML001"]
    assert serapias["cluster_status"] == "admissible_multilayer_cluster"
    assert set(serapias["admissible_primary_layers"].split(";")) == {"C", "F", "G_adult"}
    assert int(serapias["n_admissible_primary_effects"]) == 3
    assert serapias["covariance_status"] == "proxy_reconstructed_from_paired_populations"

    # Candidate rows must not be promoted merely because they are biologically multilayer.
    assert by_cluster["ML002"]["cluster_status"] == "recoverable_raw_reanalysis"
    assert int(by_cluster["ML002"]["n_admissible_primary_effects"]) == 1
    assert by_cluster["ML003"]["cluster_status"] == "blocked_effect_unit_reconstruction"
    assert int(by_cluster["ML003"]["n_admissible_primary_effects"]) == 0
    assert by_cluster["ML006"]["cluster_status"] == "recover_common_landscape_exposure"

    print(
        "EGWEE multilayer cluster contract: PASS; "
        "PS003=1 cluster/3 correlated primary outcomes, V positive definite; "
        "cross-system synthesis gate remains closed at 1 admissible cluster"
    )


if __name__ == "__main__":
    main()
