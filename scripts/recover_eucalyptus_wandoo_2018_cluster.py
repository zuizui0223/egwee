from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_population_table_v1.csv"
SEED = 20260913
B = 10_000


def z(x: np.ndarray) -> np.ndarray:
    return (x - np.mean(x)) / np.std(x, ddof=1)


def slope(x: np.ndarray, y: np.ndarray) -> float:
    xc = x - np.mean(x)
    yc = y - np.mean(y)
    den = float(xc @ xc)
    if den <= 0:
        return float("nan")
    return float((xc @ yc) / den)


def main() -> None:
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 19:
        raise AssertionError(f"expected 19 populations, got {len(rows)}")

    size = np.array([float(r["population_size"]) for r in rows])
    isolation = np.array([float(r["isolation"]) for r in rows])
    shape = np.array([float(r["shape"]) for r in rows])

    # Source-compatible transforms, all oriented so larger = stronger fragmentation severity.
    X = np.column_stack((-np.log10(size), np.sqrt(isolation), np.log10(shape)))
    Xz = np.column_stack([z(X[:, j]) for j in range(3)])
    eigval, eigvec = np.linalg.eigh(np.cov(Xz, rowvar=False, ddof=1))
    pc1 = eigvec[:, int(np.argmax(eigval))]
    if float(np.sum(pc1)) < 0:
        pc1 = -pc1
    severity = z(Xz @ pc1)

    complete_idx = [
        i for i, r in enumerate(rows)
        if r["pollen_tubes"] != "" and r["seeds_per_fruit_y2"] != "" and r["He"] != ""
    ]
    if len(complete_idx) < 6:
        print("EUCALYPTUS_WANDOO_RESULT " + json.dumps({
            "terminal_state": "common_population_frame_insufficient",
            "n_common": len(complete_idx),
        }, sort_keys=True))
        return

    names = [rows[i]["population"] for i in complete_idx]
    x = severity[complete_idx]
    Yraw = np.column_stack([
        [float(rows[i]["pollen_tubes"]) for i in complete_idx],
        [float(rows[i]["seeds_per_fruit_y2"]) for i in complete_idx],
        [float(rows[i]["He"]) for i in complete_idx],
    ])
    Yz = np.column_stack([z(Yraw[:, j]) for j in range(3)])
    effects = np.array([slope(x, Yz[:, j]) for j in range(3)])

    rng = np.random.default_rng(SEED)
    boot = np.empty((B, 3), dtype=float)
    for b in range(B):
        ix = rng.integers(0, len(complete_idx), size=len(complete_idx))
        xb = x[ix]
        for j in range(3):
            boot[b, j] = slope(xb, Yz[ix, j])
    valid = np.all(np.isfinite(boot), axis=1)
    boot = boot[valid]
    if len(boot) < int(B * 0.99):
        raise AssertionError(f"too many invalid bootstrap draws: {B-len(boot)}")

    V = np.cov(boot, rowvar=False, ddof=1)
    ci = np.percentile(boot, [2.5, 97.5], axis=0).T
    evals = np.linalg.eigvalsh(V)
    pd = bool(np.all(evals > 0))
    terminal = "ML015_admitted_I_F_Gadult_covariance_aware" if pd else "covariance_not_positive_definite"

    out = {
        "terminal_state": terminal,
        "n_source_populations": len(rows),
        "n_common": len(complete_idx),
        "common_populations": names,
        "fragmentation_pc1_loadings": {
            "smallness_minus_log10_size": float(pc1[0]),
            "sqrt_isolation": float(pc1[1]),
            "log10_shape": float(pc1[2]),
        },
        "fragmentation_pc1_eigenvalue": float(np.max(eigval)),
        "effects": {
            "I_pollen_tubes": float(effects[0]),
            "F_seeds_per_fruit_y2": float(effects[1]),
            "G_adult_He": float(effects[2]),
        },
        "percentile_95_ci": {
            "I_pollen_tubes": [float(ci[0, 0]), float(ci[0, 1])],
            "F_seeds_per_fruit_y2": [float(ci[1, 0]), float(ci[1, 1])],
            "G_adult_He": [float(ci[2, 0]), float(ci[2, 1])],
        },
        "bootstrap_covariance": V.tolist(),
        "covariance_eigenvalues": evals.tolist(),
        "bootstrap_draws_requested": B,
        "bootstrap_draws_valid": int(len(boot)),
        "rng_seed": SEED,
        "interpretation_rule": "severity increases with fragmentation; negative slope=deterioration, positive slope=increase/improvement",
    }
    print("EUCALYPTUS_WANDOO_RESULT " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
