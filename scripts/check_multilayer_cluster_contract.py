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
WANDOO_COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_primary_covariance_v1.csv"
WANDOO_RESULT = ROOT / "manuscript/EUCALYPTUS_WANDOO_2018_CLUSTER_RECOVERY_RESULT.md"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
BASE_AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-12_MULTILAYER_CLUSTERS.md"
COHORT_AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-13_COHORT_DEPENDENCE.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pearson(x: list[float], y: list[float]) -> float:
    mx, my = sum(x) / len(x), sum(y) / len(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(sum(a * a for a in dx) * sum(b * b for b in dy))


def centered(values: list[float], groups: list[str]) -> list[float]:
    means = {g: sum(v for v, gg in zip(values, groups) if gg == g) / groups.count(g) for g in set(groups)}
    return [v - means[g] for v, g in zip(values, groups)]


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


def validate_covariance(cov_path: Path, cluster_id: str, study_id: str, endpoint_names: list[str], vectors: dict[str, list[float]], variances: dict[str, float], groups: list[str]) -> None:
    cov_rows = rows(cov_path)
    by_pair = {(r["endpoint_i"], r["endpoint_j"]): r for r in cov_rows}
    assert set(by_pair) == {(a, b) for a in endpoint_names for b in endpoint_names}
    matrix = []
    centered_vectors = {name: centered(v, groups) for name, v in vectors.items()}
    for a in endpoint_names:
        mrow = []
        for b in endpoint_names:
            rr = pearson(centered_vectors[a], centered_vectors[b])
            expected = rr * math.sqrt(variances[a] * variances[b])
            row = by_pair[(a, b)]
            assert row["cluster_id"] == cluster_id and row["study_id"] == study_id
            assert row["covariance_status"] == "proxy_reconstructed"
            assert abs(float(row["correlation_proxy"]) - rr) < 1e-9
            assert abs(float(row["sampling_covariance"]) - expected) < 1e-9
            mrow.append(float(row["sampling_covariance"]))
        matrix.append(mrow)
    assert cholesky_positive_definite(matrix), matrix


def validate_serapias() -> None:
    site = rows(SERA_SITE)
    groups = [r["exposure_group"] for r in site]
    effects = [r for r in rows(SERA_EFFECTS) if r["primary_or_sensitivity"] == "primary"]
    by_effect = {r["endpoint"]: r for r in effects}
    endpoints = ["F_fruit_set", "C_pollen_immigration", "G_adult_Ho"]
    vectors = {
        "F_fruit_set": [float(r["fruit_set_pct"]) for r in site],
        "C_pollen_immigration": [float(r["pollen_immigration_pct"]) for r in site],
        "G_adult_Ho": [float(r["observed_heterozygosity"]) for r in site],
    }
    variances = {
        "F_fruit_set": float(by_effect["fruit_set"]["oriented_variance"]),
        "C_pollen_immigration": float(by_effect["pollen_immigration_rate"]["oriented_variance"]),
        "G_adult_Ho": float(by_effect["observed_heterozygosity"]["oriented_variance"]),
    }
    validate_covariance(SERA_COV, "ML001", "PS003", endpoints, vectors, variances, groups)


def validate_brosimum() -> None:
    site = rows(BROS_SITE)
    groups = [r["habitat"] for r in site]
    by_effect = {r["endpoint_id"]: r for r in rows(BROS_EFFECTS)}
    endpoints = ["C_paternity_rp", "F_TPDW"]
    vectors = {
        "C_paternity_rp": [-float(r["C_paternity_rp"]) for r in site],
        "F_TPDW": [float(r["F_TPDW_site_mean"]) for r in site],
    }
    variances = {
        "C_paternity_rp": float(by_effect["C_paternity_rp"]["oriented_variance"]),
        "F_TPDW": float(by_effect["F_progeny_vigour"]["oriented_variance"]),
    }
    validate_covariance(BROS_COV, "ML002", "PS004", endpoints, vectors, variances, groups)


def validate_wandoo() -> None:
    endpoints = ["I_pollen_tubes", "F_seeds_per_fruit_y2", "G_adult_He"]
    rs = rows(WANDOO_COV)
    by_pair = {(r["endpoint_i"], r["endpoint_j"]): float(r["sampling_covariance"]) for r in rs}
    assert set(by_pair) == {(a, b) for a in endpoints for b in endpoints}
    matrix = [[by_pair[(a, b)] for b in endpoints] for a in endpoints]
    assert cholesky_positive_definite(matrix), matrix
    result = WANDOO_RESULT.read_text(encoding="utf-8")
    assert "ML015_admitted_I_F_Gadult_covariance_aware" in result
    assert "`+0.67475197`" in result
    assert "`-0.79455522`" in result
    assert "`-0.43933127`" in result


def main() -> None:
    for path in (SERA_SITE, SERA_EFFECTS, SERA_COV, BROS_SITE, BROS_EFFECTS, BROS_COV, WANDOO_COV, WANDOO_RESULT, REGISTRY, BASE_AMENDMENT, COHORT_AMENDMENT):
        assert path.is_file(), path
    assert "Do not set covariance to zero" in BASE_AMENDMENT.read_text(encoding="utf-8")
    cohort_text = COHORT_AMENDMENT.read_text(encoding="utf-8")
    assert "proxy_pairwise_low_rank" in cohort_text
    assert "do **not** force the full proxy covariance matrix to be positive definite" in cohort_text

    validate_serapias()
    validate_brosimum()
    validate_wandoo()

    registry = rows(REGISTRY)
    by_cluster = {r["cluster_id"]: r for r in registry}
    assert {r["cluster_id"] for r in registry if r["cluster_status"] == "admissible_multilayer_cluster"} == {"ML001", "ML002", "ML003", "ML015"}
    assert set(by_cluster["ML001"]["admissible_primary_layers"].split(";")) == {"C", "F", "G_adult"}
    assert int(by_cluster["ML001"]["n_admissible_primary_effects"]) == 3
    assert set(by_cluster["ML002"]["admissible_primary_layers"].split(";")) == {"C", "F"}
    assert int(by_cluster["ML002"]["n_admissible_primary_effects"]) == 2
    assert set(by_cluster["ML003"]["admissible_primary_layers"].split(";")) == {"C", "G_adult", "G_offspring"}
    assert int(by_cluster["ML003"]["n_admissible_primary_effects"]) == 4
    assert by_cluster["ML003"]["covariance_status"] == "proxy_pairwise_low_rank_from_five_sites"
    assert set(by_cluster["ML015"]["admissible_primary_layers"].split(";")) == {"I", "F", "G_adult"}
    assert int(by_cluster["ML015"]["n_admissible_primary_effects"]) == 3
    assert by_cluster["ML015"]["covariance_status"] == "paired_population_bootstrap_10000"
    assert by_cluster["ML006"]["cluster_status"] == "common_population_values_not_recoverable"
    assert int(by_cluster["ML006"]["n_admissible_primary_effects"]) == 0

    print(
        "EGWEE multilayer cluster contract: PASS; "
        "4 independent clusters / 12 primary effects; ML015 adds a positive-definite paired-population I/F/G_adult covariance block with discordant fragmentation responses"
    )


if __name__ == "__main__":
    main()
