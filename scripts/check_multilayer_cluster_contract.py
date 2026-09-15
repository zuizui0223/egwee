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
SOCIALIS_EFFECTS = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_effects_v1.csv"
SOCIALIS_COV = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_primary_covariance_v1.csv"
ML020_EFFECTS = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_effects_v1.csv"
ML020_COV = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_covariance_v1.csv"
WANDOO_COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_covariance_v1.csv"
WANDOO_EFFECTS = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv"
WANDOO_RESULT = ROOT / "manuscript/EUCALYPTUS_WANDOO_2018_CLUSTER_RECOVERY_RESULT.md"
OBSOLETE_WANDOO_COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_primary_covariance_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
REGISTRY_ML020 = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_extension_ml020.csv"
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


def validate_socialis() -> None:
    effects = {r["endpoint_id"]: r for r in rows(SOCIALIS_EFFECTS)}
    assert set(effects) == {"Gmating_correlated_paternity_rp", "F_family_growth"}
    endpoints = ["Gmating_correlated_paternity_rp", "F_family_growth"]
    cov_rows = rows(SOCIALIS_COV)
    by_pair = {(r["endpoint_i"], r["endpoint_j"]): r for r in cov_rows}
    assert set(by_pair) == {(a, b) for a in endpoints for b in endpoints}
    matrix = [[float(by_pair[(a, b)]["sampling_covariance"]) for b in endpoints] for a in endpoints]
    assert cholesky_positive_definite(matrix), matrix
    assert abs(float(by_pair[(endpoints[0], endpoints[1])]["correlation_proxy"]) - 0.326729868213) < 1e-9
    assert abs(float(by_pair[(endpoints[0], endpoints[1])]["sampling_covariance"]) - 0.050108426040) < 1e-9
    assert effects[endpoints[0]]["layer"] == "G_mating"
    assert effects[endpoints[1]]["layer"] == "F_reproductive_function"
    assert all(r["independent_unit"] == "maternal_family" for r in effects.values())


def validate_ml020() -> None:
    effects = rows(ML020_EFFECTS)
    cov_rows = rows(ML020_COV)
    species = {r["species"] for r in effects}
    assert species == {"Atamisquea emarginata", "Cercidium australe", "Prosopis nigra"}
    assert len(effects) == 6 and len(cov_rows) == 12
    for sp in species:
        sr = [r for r in effects if r["species"] == sp]
        assert {r["endpoint_id"] for r in sr} == {"I_pollen_tubes", "F_fruit_set"}
        assert all(int(r["n_fragmented"]) == 4 and int(r["n_reference"]) == 4 for r in sr)
        endpoints = ["I_pollen_tubes", "F_fruit_set"]
        by_pair = {
            (r["endpoint_i"], r["endpoint_j"]): r
            for r in cov_rows if r["species"] == sp
        }
        assert set(by_pair) == {(a, b) for a in endpoints for b in endpoints}
        matrix = [[float(by_pair[(a, b)]["sampling_covariance"]) for b in endpoints] for a in endpoints]
        assert cholesky_positive_definite(matrix), (sp, matrix)


def validate_wandoo_gradient() -> None:
    effects = rows(WANDOO_EFFECTS)
    assert len(effects) == 3
    assert all(r["effect_stream"] == "fisher_z_gradient" for r in effects)
    assert all(r["effect_unit_status"] == "fisher_z_admissible" for r in effects)
    assert all(abs(float(r["raw_variance"]) - 0.125) < 1e-12 for r in effects)
    endpoints = ["I_pollen_tubes", "F_seeds_per_fruit_y2", "G_adult_He"]
    by_pair = {(r["endpoint_i"], r["endpoint_j"]): r for r in rows(WANDOO_COV)}
    matrix = [[float(by_pair[(a, b)]["sampling_covariance"]) for b in endpoints] for a in endpoints]
    assert cholesky_positive_definite(matrix), matrix
    assert "zero primary Hedges-g effects" in WANDOO_RESULT.read_text(encoding="utf-8")


def main() -> None:
    for path in (
        SERA_SITE, SERA_EFFECTS, SERA_COV, BROS_SITE, BROS_EFFECTS, BROS_COV,
        SOCIALIS_EFFECTS, SOCIALIS_COV, ML020_EFFECTS, ML020_COV,
        WANDOO_COV, WANDOO_EFFECTS, WANDOO_RESULT,
        REGISTRY, REGISTRY_ML020, BASE_AMENDMENT, COHORT_AMENDMENT,
    ):
        assert path.is_file(), path
    assert not OBSOLETE_WANDOO_COV.exists()
    assert "Do not set covariance to zero" in BASE_AMENDMENT.read_text(encoding="utf-8")

    validate_serapias()
    validate_brosimum()
    validate_socialis()
    validate_ml020()
    validate_wandoo_gradient()

    registry = rows(REGISTRY) + rows(REGISTRY_ML020)
    by_cluster = {r["cluster_id"]: r for r in registry}
    assert len(by_cluster) == len(registry)
    primary = [r for r in registry if r["cluster_status"] == "admissible_multilayer_cluster"]
    gradient = [r for r in registry if r["cluster_status"] == "gradient_generalisation_multilayer_cluster"]
    assert {r["cluster_id"] for r in primary} == {"ML001", "ML002", "ML003", "ML014", "ML020"}
    assert {r["cluster_id"] for r in gradient} == {"ML015"}
    assert int(by_cluster["ML001"]["n_admissible_primary_effects"]) == 3
    assert int(by_cluster["ML002"]["n_admissible_primary_effects"]) == 2
    assert int(by_cluster["ML003"]["n_admissible_primary_effects"]) == 4
    assert set(by_cluster["ML014"]["admissible_primary_layers"].split(";")) == {"G_mating", "F"}
    assert int(by_cluster["ML014"]["n_admissible_primary_effects"]) == 2
    assert by_cluster["ML014"]["covariance_status"] == "proxy_reconstructed_from_paired_families"
    assert set(by_cluster["ML020"]["admissible_primary_layers"].split(";")) == {"I", "F"}
    assert int(by_cluster["ML020"]["n_admissible_primary_effects"]) == 6
    assert by_cluster["ML015"]["admissible_primary_layers"] == ""
    assert int(by_cluster["ML015"]["n_admissible_primary_effects"]) == 0
    assert len(primary) == 5
    assert sum(int(r["n_admissible_primary_effects"]) for r in primary) == 17

    print(
        "EGWEE multilayer cluster contract: PASS; primary family = ML001-ML003+ML014+ML020 / 17 marginal effects / 5 clusters; "
        "ML020 counts once despite 3 dependent species; ML015 = separate Fisher-z gradient cluster / 3 effects"
    )


if __name__ == "__main__":
    main()
