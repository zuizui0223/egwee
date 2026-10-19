"""Retrospective two-programme context audit for empirical EGWEE.

Equal independent-population (Wandoo) and forest-fragment (Cardiopetalum)
models. No theoretical EGWE outputs, no extra corpus admissions.

Usage: python scripts/audit_if_environment_conditional_20261019.py
       python scripts/audit_if_environment_conditional_20261019.py --output out.json
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/meta_extraction"
T1 = EVIDENCE / "wandoo_reproductive_stages_20261019_table1.csv"
T6 = EVIDENCE / "wandoo_reproductive_stages_20261019_table6.csv"
CARDIO = EVIDENCE / "phase2_cf01_cardiopetalum_table1_v1.csv"
COMMON = ("J", "K", "F", "C", "E", "G", "B", "I", "A", "H", "D")
NATIVE = ("J", "L", *COMMON[1:])
ENDPOINTS = (
    "fruits_per_branch_y2",
    "fruit_flower_ratio_y2",
    "seeds_per_fruit_y2",
)

def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))

def f(v: str) -> float:
    return float(v) if v != "" else float("nan")

def model(X: np.ndarray, y: np.ndarray, names: list[str], with_loo: bool = True) -> dict:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, k = X.shape
    assert n > k + 1 and len(names) == k and np.linalg.matrix_rank(X) == k
    inv = np.linalg.inv(X.T @ X)
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    df = n - k
    rss = float(e @ e)
    s2 = rss / df
    v = inv * s2
    se = np.sqrt(np.diag(v))
    tval = b / se
    p = 2 * stats.t.sf(np.abs(tval), df)
    h = np.einsum("ij,jk,ik->i", X, inv, X)
    assert np.all(h < 1)
    w = (e / (1 - h)) ** 2
    hcov = inv @ (X.T * w) @ X @ inv
    se_hc3 = np.sqrt(np.maximum(0, np.diag(hcov)))
    p_hc3 = 2 * stats.t.sf(np.abs(b / se_hc3), df)
    tcrit = float(stats.t.ppf(.975, df))
    r2 = 1.0 - rss / float(((y - y.mean()) ** 2).sum())
    out = {
        "n_independent": n, "df_residual": df, "r_squared": float(r2),
        "beta": dict(zip(names, [float(x) for x in b])),
        "p_ols": dict(zip(names, [float(x) for x in p])),
        "p_hc3_t_reference": dict(zip(names, [float(x) for x in p_hc3])),
        "ci95_nominal": {
            name: [float(b[j] - tcrit * se[j]), float(b[j] + tcrit * se[j])]
            for j, name in enumerate(names)
        },
    }
    if with_loo:
        pred, slopes, cases = [], [], []
        for i in range(n):
            keep = np.arange(n) != i
            sub = model(X[keep], y[keep], names, with_loo=False)
            bi = np.array([sub["beta"][name] for name in names])
            pred.append(float(X[i] @ bi))
            slopes.append({
                "excluded_row_index_zero_based": i,
                "coefficients": sub["beta"],
                "p_ols": sub["p_ols"],
            })
            cases.append(i)
        out["loo_rmse"] = float(np.sqrt(np.mean((np.array(pred) - y) ** 2)))
        out["loo_pred_below_zero"] = sum(q < 0 for q in pred)
        out["loo_predictions"] = pred
        out["loo_refits"] = slopes
    return out

def holm(pvalues: list[float]) -> list[float]:
    n = len(pvalues)
    order = sorted(range(n), key=lambda i: pvalues[i])
    out = [0.0] * n
    sofar = 0.0
    for rank, j in enumerate(order):
        sofar = max(sofar, min(1.0, pvalues[j] * (n - rank)))
        out[j] = sofar
    return out

def wandoo() -> dict:
    env = {r["population"]: r for r in read(T1)}
    repro = {r["population"]: r for r in read(T6)}
    assert len(env) == len(repro) == 19
    assert set(COMMON).issubset(env) and set(NATIVE).issubset(env)
    assert repro["L"]["fruits_per_branch_y2_mean"] == "0.0"
    assert repro["L"]["seeds_per_fruit_y2_mean"] == ""
    out = {}
    for frame, populations in (("common11", COMMON), ("native12", NATIVE)):
        out[frame] = {}
        for endpoint in ENDPOINTS:
            ids = [a for a in populations if repro[a][endpoint + "_mean"] != ""]
            if frame == "native12" and endpoint == "seeds_per_fruit_y2":
                assert ids == list(COMMON)
            y = np.array([f(repro[a][endpoint + "_mean"]) for a in ids])
            x_i = np.array([f(repro[a]["pollen_tubes_y2_mean"]) for a in ids])
            x_ec = np.log10([f(env[a]["ec_ms_per_m"]) for a in ids])
            x_size = np.log10([f(env[a]["population_size"]) for a in ids])
            X0 = np.column_stack((np.ones(len(ids)), x_i))
            X1 = np.column_stack((np.ones(len(ids)), x_i, x_ec, x_size))
            m0 = model(X0, y, ["intercept", "pollen_tubes"])
            m1 = model(X1, y, ["intercept", "pollen_tubes", "log10_EC", "log10_population_size"])
            m1["loo_population_ids"] = ids
            m1["loo_excluded_EC_slope"] = {
                a: s["coefficients"]["log10_EC"]
                for a, s in zip(ids, m1["loo_refits"])
            }
            m1["loo_excluded_EC_p"] = {
                a: s["p_ols"]["log10_EC"]
                for a, s in zip(ids, m1["loo_refits"])
            }
            m1.pop("loo_refits")
            m1.pop("loo_predictions")
            m1["loo_mse_gain_vs_pollen_only"] = 1 - (m1["loo_rmse"] / m0["loo_rmse"]) ** 2
            out[frame][endpoint] = {
                "pollen_only": {"r_squared": m0["r_squared"], "loo_rmse": m0["loo_rmse"]},
                "joint_EC_population_size": m1,
            }
    tests = []
    for endpoint in ENDPOINTS:
        m = out["common11"][endpoint]["joint_EC_population_size"]
        for var in ("log10_EC", "log10_population_size"):
            tests.append((endpoint, var, m["p_ols"][var]))
    corrected = holm([x[2] for x in tests])
    out["common11_six_joint_tests_holm"] = [
        {"endpoint": e, "predictor": v, "p_ols": p, "holm_p": q}
        for (e, v, p), q in zip(tests, corrected)
    ]
    high_ec = {
        "observed_12": sum(float(env[a]["ec_ms_per_m"]) >= 20 for a in NATIVE),
        "not_reproductively_measured_7": sum(
            float(r["ec_ms_per_m"]) >= 20
            for a, r in env.items() if a not in NATIVE
        ),
        "threshold_is_descriptive_not_pre_registered": 20,
    }
    out["observed_EC_range_selection"] = high_ec
    out["restricted_N_ge_10"] = {}
    for frame, populations in (("common11", COMMON), ("native12", NATIVE)):
        out["restricted_N_ge_10"][frame] = {}
        for endpoint in ENDPOINTS:
            ids = [a for a in populations
                   if int(repro[a]["n_reproductive"]) >= 10
                   and repro[a][endpoint + "_mean"]]
            y = np.array([f(repro[a][endpoint + "_mean"]) for a in ids])
            X = np.column_stack((
                np.ones(len(ids)),
                [f(repro[a]["pollen_tubes_y2_mean"]) for a in ids],
                np.log10([f(env[a]["ec_ms_per_m"]) for a in ids]),
                np.log10([f(env[a]["population_size"]) for a in ids]),
            ))
            m = model(X, y, ["intercept", "pollen_tubes", "log10_EC", "log10_population_size"],
                      with_loo=False)
            out["restricted_N_ge_10"][frame][endpoint] = {
                "ids": ids, "n": len(ids), "beta_log10_EC": m["beta"]["log10_EC"],
                "p_log10_EC": m["p_ols"]["log10_EC"],
                "p_hc3_log10_EC": m["p_hc3_t_reference"]["log10_EC"],
            }
    assert abs(out["common11"]["fruits_per_branch_y2"]["joint_EC_population_size"]["beta"]["log10_EC"] + 129.05152075441623) < 1e-7
    assert abs(out["common11"]["fruit_flower_ratio_y2"]["joint_EC_population_size"]["p_ols"]["log10_EC"] - .009817810959752588) < 1e-9
    return out

def cardiopetalum() -> dict:
    rows = read(CARDIO)
    assert [r["fragment_id"] for r in rows] == [f"F{i}" for i in range(1, 11)]
    area = np.array([f(r["area_ha"]) for r in rows])
    poll = np.array([f(r["pollinator_abundance_per_flower_mean"]) for r in rows])
    fruit = np.array([f(r["fruit_set_mean"]) for r in rows])
    density = np.array([f(r["plant_density_mean"]) for r in rows])
    severity = -np.log(area)
    log_density = np.log(density)
    models = {}
    for key, cols, names in (
        ("pollinator_only", [poll], ["pollinator_abundance_per_flower"]),
        ("pollinator_plus_severity", [poll, severity],
         ["pollinator_abundance_per_flower", "negative_ln_fragment_area"]),
        ("pollinator_plus_log_density", [poll, log_density],
         ["pollinator_abundance_per_flower", "ln_plant_density"]),
        ("pollinator_plus_severity_plus_density", [poll, severity, log_density],
         ["pollinator_abundance_per_flower", "negative_ln_fragment_area", "ln_plant_density"]),
    ):
        X = np.column_stack([np.ones(10), *cols])
        m = model(X, fruit, ["intercept", *names])
        m.pop("loo_refits")
        m.pop("loo_predictions")
        models[key] = m
    small = area <= 33.8
    rho = stats.pearsonr(np.log(area[small]), fruit[small])
    gap = float(455 / 33.8)
    assert abs(models["pollinator_plus_severity"]["beta"]["negative_ln_fragment_area"] + .0435118043109858) < 1e-10
    return {
        "independent_units": 10,
        "models": models,
        "area_gap_ha": [33.8, 455.0],
        "gap_factor": gap,
        "smaller_seven_log_area_fruit_r": float(rho.statistic),
        "smaller_seven_log_area_fruit_descriptive_p": float(rho.pvalue),
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "status": "posthoc_cross_programme_context_stress_test_no_causal_identification",
        "wandoo": wandoo(),
        "cardiopetalum": cardiopetalum(),
        "no_added_meta_programmes": True,
        "separate_theoretical_egwe": True,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    w = result["wandoo"]["common11"]
    c = result["cardiopetalum"]["models"]
    print(
        "CONDITIONAL_CONTEXT_AUDIT_OK"
        f" wandoo_n=11 EC_fruit={w['fruits_per_branch_y2']['joint_EC_population_size']['beta']['log10_EC']:.6f}"
        f" EC_ratio_p={w['fruit_flower_ratio_y2']['joint_EC_population_size']['p_ols']['log10_EC']:.6f}"
        f" cardio_n=10 severity_b={c['pollinator_plus_severity']['beta']['negative_ln_fragment_area']:.6f}"
    )

if __name__ == "__main__":
    main()
