from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERA_SITE = ROOT / "evidence/meta_extraction/PS003_serapias_site_table_v1.csv"
SERA_EFFECTS = ROOT / "evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv"
SERA_COV = ROOT / "evidence/meta_extraction/PS003_serapias_primary_covariance_v1.csv"
BROS_SITE = ROOT / "evidence/meta_extraction/PS004_brosimum_site_table_v1.csv"
BROS_EFFECTS = ROOT / "evidence/meta_extraction/PS004_brosimum_extraction_v1.csv"
BROS_COV = ROOT / "evidence/meta_extraction/PS004_brosimum_primary_covariance_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-12_MULTILAYER_CLUSTERS.md"


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


def centered(values: list[float], groups: list[str]) -> list[float]:
    means: dict[str, float] = {}
    for group in set(groups):
        selected = [value for value, observed_group in zip(values, groups) if observed_group == group]
        means[group] = sum(selected) / len(selected)
    return [value - means[group] for value, group in zip(values, groups)]


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


def validate_covariance(
    cov_path: Path,
    cluster_id: str,
    study_id: str,
    endpoint_names: list[str],
    centered_vectors: dict[str, list[float]],
    variances: dict[str, float],
    n_units: int,
) -> None:
    cov_rows = rows(cov_path)
    expected_pairs = {(a, b) for a in endpoint_names for b in endpoint_names}
    by_pair = {(r["endpoint_i"], r["endpoint_j"]): r for r in cov_rows}
    assert set(by_pair) == expected_pairs
    assert len(cov_rows) == len(expected_pairs)

    matrix: list[list[float]] = []
    for a in endpoint_names:
        matrix_row: list[float] = []
        for b in endpoint_names:
            row = by_pair[(a, b)]
            r_expected = pearson(centered_vectors[a], centered_vectors[b])
            covariance_expected = r_expected * math.sqrt(variances[a] * variances[b])
            assert row["cluster_id"] == cluster_id
            assert row["study_id"] == study_id
            assert int(row["n_paired_units"]) == n_units
            assert row["covariance_status"] == "proxy_reconstructed"
            assert abs(float(row["correlation_proxy"]) - r_expected) < 1e-9
            assert abs(float(row["sampling_covariance"]) - covariance_expected) < 1e-9
            assert abs(float(row["marginal_variance_i"]) - variances[a]) < 1e-9
            assert abs(float(row["marginal_variance_j"]) - variances[b]) < 1e-9
            matrix_row.append(float(row["sampling_covariance"]))
        matrix.append(matrix_row)

    for i in range(len(endpoint_names)):
        for j in range(len(endpoint_names)):
            assert abs(matrix[i][j] - matrix[j][i]) < 1e-12
    assert cholesky_positive_definite(matrix), matrix


def validate_serapias() -> None:
    site = rows(SERA_SITE)
    assert len(site) == 9
    groups = [r["exposure_group"] for r in site]
    assert groups.count("anthropic") == 3
    assert groups.count("natural") == 6

    effects = rows(SERA_EFFECTS)
    primary = [r for r in effects if r["primary_or_sensitivity"] == "primary"]
    assert len(primary) == 3
    assert {r["layer"] for r in primary} == {"C", "F", "G_adult"}
    assert all(r["effect_unit_status"] == "g_admissible" for r in primary)
    assert any(r["endpoint"] == "fixation_index_FIS" and r["primary_or_sensitivity"] == "sensitivity" for r in effects)

    by_effect = {r["endpoint"]: r for r in primary}
    endpoint_names = ["F_fruit_set", "C_pollen_immigration", "G_adult_Ho"]
    values = {
        "F_fruit_set": [float(r["fruit_set_pct"]) for r in site],
        "C_pollen_immigration": [float(r["pollen_immigration_pct"]) for r in site],
        "G_adult_Ho": [float(r["observed_heterozygosity"]) for r in site],
    }
    centered_vectors = {name: centered(vals, groups) for name, vals in values.items()}
    variances = {
        "F_fruit_set": float(by_effect["fruit_set"]["oriented_variance"]),
        "C_pollen_immigration": float(by_effect["pollen_immigration_rate"]["oriented_variance"]),
        "G_adult_Ho": float(by_effect["observed_heterozygosity"]["oriented_variance"]),
    }
    validate_covariance(SERA_COV, "ML001", "PS003", endpoint_names, centered_vectors, variances, 9)


def validate_brosimum() -> None:
    site = rows(BROS_SITE)
    assert len(site) == 6
    groups = [r["habitat"] for r in site]
    assert groups.count("FRA") == 3
    assert groups.count("CON") == 3

    effects = rows(BROS_EFFECTS)
    by_effect = {r["endpoint_id"]: r for r in effects}
    assert by_effect["C_paternity_rp"]["effect_unit_status"] == "g_admissible"
    assert by_effect["F_progeny_vigour"]["effect_unit_status"] == "g_admissible"
    for endpoint in ("Gadult_Ho", "Goffspring_Ho", "Goffspring_F"):
        assert by_effect[endpoint]["effect_unit_status"] == "raw_reanalysis_required"

    # C is oriented so larger biological support = lower source rp.
    values = {
        "C_paternity_rp": [-float(r["C_paternity_rp"]) for r in site],
        "F_TPDW": [float(r["F_TPDW_site_mean"]) for r in site],
    }
    centered_vectors = {name: centered(vals, groups) for name, vals in values.items()}
    variances = {
        "C_paternity_rp": float(by_effect["C_paternity_rp"]["oriented_variance"]),
        "F_TPDW": float(by_effect["F_progeny_vigour"]["oriented_variance"]),
    }
    validate_covariance(BROS_COV, "ML002", "PS004", ["C_paternity_rp", "F_TPDW"], centered_vectors, variances, 6)


def main() -> None:
    for path in (SERA_SITE, SERA_EFFECTS, SERA_COV, BROS_SITE, BROS_EFFECTS, BROS_COV, REGISTRY, AMENDMENT):
        assert path.is_file(), path

    amendment = AMENDMENT.read_text(encoding="utf-8")
    assert "one cluster with three correlated outcomes" in amendment
    assert "Do not set covariance to zero" in amendment
    assert "at least two independent admissible multilayer clusters" in amendment
    assert "metafor::escalc" in amendment and 'vtype="LS"' in amendment

    validate_serapias()
    validate_brosimum()

    registry = rows(REGISTRY)
    by_cluster = {r["cluster_id"]: r for r in registry}
    assert len(by_cluster) == len(registry)
    assert set(by_cluster) >= {"ML001", "ML002", "ML003", "ML004", "ML005", "ML006"}

    serapias = by_cluster["ML001"]
    assert serapias["cluster_status"] == "admissible_multilayer_cluster"
    assert set(serapias["admissible_primary_layers"].split(";")) == {"C", "F", "G_adult"}
    assert int(serapias["n_admissible_primary_effects"]) == 3

    brosimum = by_cluster["ML002"]
    assert brosimum["cluster_status"] == "admissible_multilayer_cluster"
    assert set(brosimum["admissible_primary_layers"].split(";")) == {"C", "F"}
    assert int(brosimum["n_admissible_primary_effects"]) == 2
    assert brosimum["covariance_status"] == "proxy_reconstructed_from_six_sites"

    assert by_cluster["ML003"]["cluster_status"] == "blocked_effect_unit_reconstruction"
    assert int(by_cluster["ML003"]["n_admissible_primary_effects"]) == 0
    assert by_cluster["ML006"]["cluster_status"] == "recover_common_landscape_exposure"

    admissible = [r for r in registry if r["cluster_status"] == "admissible_multilayer_cluster"]
    assert {r["cluster_id"] for r in admissible} == {"ML001", "ML002"}

    print(
        "EGWEE multilayer cluster contract: PASS; "
        "ML001 Serapias=3 correlated layers, ML002 Brosimum=2 correlated layers; "
        "both V blocks positive definite; cross-system comparison gate OPEN at 2 independent clusters"
    )


if __name__ == "__main__":
    main()
