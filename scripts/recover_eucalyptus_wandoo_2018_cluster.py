from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_population_table_v1.csv"


def zscore(x: np.ndarray) -> np.ndarray:
    return (x - np.mean(x)) / np.std(x, ddof=1)


def correlation(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(x, y)[0, 1])


def residuals(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    design = np.column_stack((np.ones(len(x)), x))
    beta, *_ = np.linalg.lstsq(design, y, rcond=None)
    return y - design @ beta


def main() -> None:
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 19:
        raise AssertionError(f"expected 19 populations, got {len(rows)}")

    size = np.array([float(r["population_size"]) for r in rows])
    isolation = np.array([float(r["isolation"]) for r in rows])
    shape = np.array([float(r["shape"]) for r in rows])

    exposure = np.column_stack((-np.log10(size), np.sqrt(isolation), np.log10(shape)))
    exposure_z = np.column_stack([zscore(exposure[:, j]) for j in range(3)])
    eigval, eigvec = np.linalg.eigh(np.cov(exposure_z, rowvar=False, ddof=1))
    pc1 = eigvec[:, int(np.argmax(eigval))]
    if float(np.sum(pc1)) < 0:
        pc1 = -pc1
    severity = zscore(exposure_z @ pc1)

    complete_idx = [
        i for i, r in enumerate(rows)
        if r["pollen_tubes"] != "" and r["seeds_per_fruit_y2"] != "" and r["He"] != ""
    ]
    n = len(complete_idx)
    if n < 6:
        print("EUCALYPTUS_WANDOO_RESULT " + json.dumps({
            "terminal_state": "common_population_frame_insufficient",
            "n_common": n,
        }, sort_keys=True))
        return

    names = [rows[i]["population"] for i in complete_idx]
    x = severity[complete_idx]
    endpoints = ["I_pollen_tubes", "F_seeds_per_fruit_y2", "G_adult_He"]
    y = [
        np.array([float(rows[i]["pollen_tubes"]) for i in complete_idx]),
        np.array([float(rows[i]["seeds_per_fruit_y2"]) for i in complete_idx]),
        np.array([float(rows[i]["He"]) for i in complete_idx]),
    ]

    r = np.array([correlation(x, yy) for yy in y])
    if np.any(~np.isfinite(r)) or np.any(np.abs(r) >= 1):
        raise AssertionError(f"invalid correlations: {r}")
    fisher_z = np.arctanh(r)
    marginal_var = np.repeat(1.0 / (n - 3), 3)

    resid = np.vstack([residuals(x, yy) for yy in y])
    residual_corr = np.corrcoef(resid)
    V = residual_corr * np.sqrt(np.outer(marginal_var, marginal_var))
    evals = np.linalg.eigvalsh(V)
    pd = bool(np.all(evals > 0))
    terminal = (
        "ML015_gradient_generalisation_I_F_Gadult_covariance_aware"
        if pd else "gradient_covariance_not_positive_definite"
    )

    out = {
        "terminal_state": terminal,
        "protocol_tier": "separate_fisher_z_gradient_generalisation",
        "counts_toward_primary_hedges_g_denominator": False,
        "n_primary_effects_added": 0,
        "n_source_populations": len(rows),
        "n_common": n,
        "common_populations": names,
        "fragmentation_pc1_loadings": {
            "smallness_minus_log10_size": float(pc1[0]),
            "sqrt_isolation": float(pc1[1]),
            "log10_shape": float(pc1[2]),
        },
        "fragmentation_pc1_eigenvalue": float(np.max(eigval)),
        "pearson_r": {k: float(v) for k, v in zip(endpoints, r)},
        "fisher_z_effects": {k: float(v) for k, v in zip(endpoints, fisher_z)},
        "marginal_variance": {k: float(v) for k, v in zip(endpoints, marginal_var)},
        "residual_correlation_proxy": residual_corr.tolist(),
        "working_covariance": V.tolist(),
        "covariance_eigenvalues": evals.tolist(),
        "interpretation_rule": (
            "severity increases with fragmentation; negative Fisher-z association = lower biological support/function, "
            "positive = increase; analyse separately from Hedges-g primary stream"
        ),
    }
    print("EUCALYPTUS_WANDOO_RESULT " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
