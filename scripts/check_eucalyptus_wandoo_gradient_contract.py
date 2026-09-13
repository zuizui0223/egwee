from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_population_table_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_covariance_v1.csv"
OBSOLETE_COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_primary_covariance_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
RESULT = ROOT / "manuscript/EUCALYPTUS_WANDOO_2018_CLUSTER_RECOVERY_RESULT.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def zscore(x: np.ndarray) -> np.ndarray:
    return (x - np.mean(x)) / np.std(x, ddof=1)


def residuals(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    design = np.column_stack((np.ones(len(x)), x))
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    return y - design @ beta


def main() -> None:
    for path in (DATA, EFFECTS, COV, REGISTRY, RESULT):
        assert path.is_file(), path
    assert not OBSOLETE_COV.exists(), "obsolete ML015 primary covariance must remain deleted"

    data = rows(DATA)
    assert len(data) == 19
    size = np.array([float(r["population_size"]) for r in data])
    isolation = np.array([float(r["isolation"]) for r in data])
    shape = np.array([float(r["shape"]) for r in data])
    exposure = np.column_stack((-np.log10(size), np.sqrt(isolation), np.log10(shape)))
    exposure_z = np.column_stack([zscore(exposure[:, j]) for j in range(3)])
    eigval, eigvec = np.linalg.eigh(np.cov(exposure_z, rowvar=False, ddof=1))
    pc1 = eigvec[:, int(np.argmax(eigval))]
    if float(np.sum(pc1)) < 0:
        pc1 = -pc1
    severity = zscore(exposure_z @ pc1)

    idx = [
        i for i, r in enumerate(data)
        if r["pollen_tubes"] and r["seeds_per_fruit_y2"] and r["He"]
    ]
    assert [data[i]["population"] for i in idx] == ["J", "K", "F", "C", "E", "G", "B", "I", "A", "H", "D"]
    assert len(idx) == 11
    x = severity[idx]
    endpoint_values = {
        "I_pollen_tubes": np.array([float(data[i]["pollen_tubes"]) for i in idx]),
        "F_seeds_per_fruit_y2": np.array([float(data[i]["seeds_per_fruit_y2"]) for i in idx]),
        "G_adult_He": np.array([float(data[i]["He"]) for i in idx]),
    }

    effects = {r["endpoint"]: r for r in rows(EFFECTS)}
    expected_layers = {
        "I_pollen_tubes": "I",
        "F_seeds_per_fruit_y2": "F",
        "G_adult_He": "G_adult",
    }
    var = 1.0 / (len(idx) - 3)
    residual_vectors = []
    for endpoint, y in endpoint_values.items():
        r = float(np.corrcoef(x, y)[0, 1])
        fz = float(np.arctanh(r))
        row = effects[endpoint]
        assert row["layer"] == expected_layers[endpoint]
        assert row["effect_stream"] == "fisher_z_gradient"
        assert row["effect_unit_status"] == "fisher_z_admissible"
        assert abs(float(row["r"]) - r) < 1e-12
        assert abs(float(row["raw_effect_fisher_z"]) - fz) < 1e-12
        assert abs(float(row["oriented_effect"]) - fz) < 1e-12
        assert abs(float(row["raw_variance"]) - var) < 1e-12
        assert abs(float(row["oriented_variance"]) - var) < 1e-12
        residual_vectors.append(residuals(x, y))

    residual_corr = np.corrcoef(np.vstack(residual_vectors))
    V = residual_corr * var
    assert np.all(np.linalg.eigvalsh(V) > 0)
    cov_rows = {(r["endpoint_i"], r["endpoint_j"]): r for r in rows(COV)}
    endpoints = list(endpoint_values)
    assert set(cov_rows) == {(a, b) for a in endpoints for b in endpoints}
    for i, a in enumerate(endpoints):
        for j, b in enumerate(endpoints):
            rr = cov_rows[(a, b)]
            assert rr["covariance_status"] == "proxy_reconstructed_gradient_residual"
            assert abs(float(rr["residual_correlation_proxy"]) - residual_corr[i, j]) < 1e-12
            assert abs(float(rr["sampling_covariance"]) - V[i, j]) < 1e-12

    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    ml015 = registry["ML015"]
    assert ml015["design_stream"] == "fisher_z_gradient_generalisation"
    assert ml015["admissible_primary_layers"] == ""
    assert int(ml015["n_admissible_primary_effects"]) == 0
    assert ml015["cluster_status"] == "gradient_generalisation_multilayer_cluster"
    assert ml015["covariance_status"] == "proxy_reconstructed_gradient_residual"

    primary = [r for r in registry.values() if r["cluster_status"] == "admissible_multilayer_cluster"]
    assert {r["cluster_id"] for r in primary} == {"ML001", "ML002", "ML003"}
    assert sum(int(r["n_admissible_primary_effects"]) for r in primary) == 9

    text = RESULT.read_text(encoding="utf-8")
    assert "zero primary Hedges-g effects" in text
    assert "Fisher-z gradient generalisation cluster" in text
    assert "3 independent clusters / 9 primary effects" in text

    print(
        "ML015 Eucalyptus wandoo gradient contract: PASS; "
        "3 Fisher-z gradient effects retained with positive-definite residual-proxy V; "
        "primary Hedges-g denominator remains 3 clusters / 9 effects"
    )


if __name__ == "__main__":
    main()
