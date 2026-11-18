"""Source-locked exploratory temporal / contextual triangulation in empirical EGWEE.

Population/fragment = independent unit. No results from theoretical EGWE.
No new corpus admissions. CI requires NumPy and SciPy only.

python scripts/audit_reproductive_environment_persistence_20261019.py
python scripts/audit_reproductive_environment_persistence_20261019.py --output result.json
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import numpy as np
from scipy.stats import pearsonr, spearmanr, t

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "meta_extraction"
TABLE1 = EVIDENCE / "wandoo_reproductive_stages_20261019_table1.csv"
TABLE6 = EVIDENCE / "wandoo_reproductive_stages_20261019_table6.csv"
CARDIO = EVIDENCE / "phase2_cf01_cardiopetalum_table1_v1.csv"
COMMON = ["J", "K", "F", "C", "E", "G", "B", "I", "A", "H", "D"]
NATIVE = ["J", "L", *COMMON[1:]]


def rows(path):
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def corr(a, b):
    return float(pearsonr(a, b).statistic)


def fit(x, y, names):
    x, y = np.asarray(x, float), np.asarray(y, float)
    n, k = x.shape
    assert n > k + 1 and np.linalg.matrix_rank(x) == k
    inv = np.linalg.inv(x.T @ x)
    coef = np.linalg.lstsq(x, y, rcond=None)[0]
    residual = y - x @ coef
    df = n - k
    var = float(residual @ residual) / df
    se = np.sqrt(np.maximum(0, np.diag(inv) * var))
    p = 2 * t.sf(abs(coef / se), df)
    h = np.einsum("ij,jk,ik->i", x, inv, x)
    assert np.all(h < 1)
    hc3 = inv @ (x.T * (residual / (1 - h)) ** 2) @ x @ inv
    robust_se = np.sqrt(np.maximum(0, np.diag(hc3)))
    phc3 = 2 * t.sf(abs(coef / robust_se), df)
    predictions, leave_b = [], []
    for i in range(n):
        keep = np.arange(n) != i
        bi = np.linalg.lstsq(x[keep], y[keep], rcond=None)[0]
        predictions.append(float(x[i] @ bi))
        leave_b.append(bi.tolist())
    r2 = 1 - float(residual @ residual) / float(((y - y.mean()) ** 2).sum())
    return {
        "n": n, "df": df, "r2": r2,
        "beta": dict(zip(names, coef.tolist())),
        "p_ols": dict(zip(names, p.tolist())),
        "p_hc3_t_reference": dict(zip(names, phc3.tolist())),
        "loo_rmse": float(np.sqrt(np.mean((np.asarray(predictions) - y) ** 2))),
        "loo_predictions_below_zero": int((np.asarray(predictions) < 0).sum()),
        "loo_beta": [dict(zip(names, b)) for b in leave_b]
    }


def wandoo():
    environment = {r["population"]: r for r in rows(TABLE1)}
    reproduction = {r["population"]: r for r in rows(TABLE6)}
    assert len(environment) == len(reproduction) == 19
    assert reproduction["L"]["fruits_per_branch_y2_mean"] == "0.0"
    assert reproduction["L"]["seeds_per_fruit_y2_mean"] == ""
    assert not any(reproduction[p]["measurement_status"] != "measured" for p in NATIVE)

    data = {}
    for p in NATIVE:
        e, r = environment[p], reproduction[p]
        data[p] = {
            "pollen": float(r["pollen_tubes_y2_mean"]),
            "log_ec": float(np.log10(float(e["ec_ms_per_m"]))),
            "log_size": float(np.log10(float(e["population_size"]))),
            "fruits_y2": float(r["fruits_per_branch_y2_mean"]),
            "fruits_y3": float(r["fruits_per_branch_y3_mean"]),
            "flowers_y2": float(r["flowers_per_branch_y2_mean"]),
            "flowers_y3": float(r["flowers_per_branch_y3_mean"]),
            "seeds_y1": float(r["seeds_per_fruit_y1_mean"]) if p != "L" else None,
            "seeds_y2": float(r["seeds_per_fruit_y2_mean"]) if p != "L" else None,
        }

    def vec(ids, key):
        return np.asarray([data[p][key] for p in ids], dtype=float)

    a, b = vec(COMMON, "fruits_y2"), vec(COMMON, "fruits_y3")
    s1, s2 = vec(COMMON, "seeds_y1"), vec(COMMON, "seeds_y2")
    rf, rs = corr(a, b), corr(s1, s2)
    assert abs(rf - 0.9193298326267294) < 1e-10
    assert abs(rs - 0.31417956212266845) < 1e-10
    assert (b < a).sum() == 11
    assert (vec(COMMON, "flowers_y3") > vec(COMMON, "flowers_y2")).sum() == 2
    assert (s2 > s1).sum() == 7
    omission = []
    for i, p in enumerate(COMMON):
        keep = [q for q in COMMON if q != p]
        omission.append({
            "excluded_population": p,
            "r_fruit": corr(vec(keep, "fruits_y2"), vec(keep, "fruits_y3")),
            "r_seed": corr(vec(keep, "seeds_y1"), vec(keep, "seeds_y2")),
        })
    assert all(z["r_fruit"] > z["r_seed"] for z in omission)

    # Paired-population bootstrap is an influence sensitivity, not a time-
    # or stage-specific mechanism test. The intervals differ for the two outcomes.
    rng = np.random.default_rng(20261019)
    boot = []
    for _ in range(25_000):
        i = rng.integers(0, len(COMMON), len(COMMON))
        if min(np.std(v[i]) for v in (a, b, s1, s2)) < 1e-10:
            continue
        rfb, rsb = corr(a[i], b[i]), corr(s1[i], s2[i])
        boot.append([rfb, rsb, rfb - rsb])
    quantile = np.percentile(np.asarray(boot), [2.5, 50, 97.5], axis=0)
    models = {}
    for label, ids in (
        ("native12", NATIVE), ("common11", COMMON),
        ("omit_G", [p for p in NATIVE if p != "G"]),
        ("omit_L_and_G", [p for p in COMMON if p != "G"]),
    ):
        x = np.column_stack((
            np.ones(len(ids)), vec(ids, "pollen"),
            vec(ids, "log_size"), vec(ids, "log_ec")
        ))
        models[label] = {}
        for y in ("fruits_y2", "fruits_y3"):
            res = fit(x, np.log1p(vec(ids, y)),
                      ["intercept", "pollen_y2", "log10_size", "log10_ec"])
            # Year 3 does not have synchronous pollen; treat as descriptive
            # prior-year context rather than mediation or contemporaneous I-F.
            models[label][y] = {k: v for k, v in res.items() if k != "loo_beta"}
    assert models["native12"]["fruits_y2"]["beta"]["log10_ec"] < 0
    assert models["native12"]["fruits_y3"]["beta"]["log10_ec"] < 0

    return {
        "unit": "population", "n_fruit": 12, "n_same_frame": 11,
        "fruit_year_pair": ["y2", "y3"], "seed_year_pair": ["y1", "y2"],
        "corr_fruit_pearson_common11": rf,
        "corr_fruit_spearman_common11": float(spearmanr(a, b).statistic),
        "corr_seed_pearson_common11": rs,
        "corr_seed_spearman_common11": float(spearmanr(s1, s2).statistic),
        "pearson_delta": rf - rs,
        "bootstrap_quantiles_columns_fruit_seed_delta": quantile.tolist(),
        "fruit_fall_cases": 11,
        "flower_rise_while_fruit_falls": [
            p for p in COMMON if data[p]["flowers_y3"] > data[p]["flowers_y2"]
        ],
        "seeds_per_fruit_rise_cases": 7,
        "median_fruit_y3_over_y2": float(np.median(b / a)),
        "omission": omission, "log1p_context_models": models,
        "mating_system_crosswalk_warning":
            "Table 7 multilocus outcrossing available for F,C,E,B,A, "
            "only 5/11 fruit-producing populations; not a quality mediator test"
    }


def cardiopetalum():
    dataset = sorted(rows(CARDIO), key=lambda x: int(x["fragment_id"][1:]))
    assert len(dataset) == 10
    area = np.asarray([float(r["area_ha"]) for r in dataset])
    beetles = np.asarray([float(r["pollinator_abundance_per_flower_mean"]) for r in dataset])
    isolation = np.asarray([float(r["distance_nearest_fragment_m"]) for r in dataset])
    density = np.asarray([float(r["plant_density_mean"]) for r in dataset])
    fruit = np.asarray([float(r["fruit_set_mean"]) for r in dataset])
    predictors = {
        "beetles": beetles, "log_area": np.log(area),
        "log_distance": np.log(isolation), "log_density": np.log(density)
    }
    specs = [
        ["beetles"], ["beetles", "log_area"], ["beetles", "log_distance"],
        ["beetles", "log_density"], ["beetles", "log_area", "log_distance"],
        ["beetles", "log_area", "log_density"],
        ["beetles", "log_area", "log_distance", "log_density"]
    ]
    models = {}
    for names in specs:
        x = np.column_stack([np.ones(10)] + [predictors[p] for p in names])
        key = "+".join(names)
        raw = fit(x, fruit, ["intercept", *names])
        if "log_area" in names:
            assert raw["beta"]["log_area"] > 0
            assert all(leave["log_area"] > 0 for leave in raw["loo_beta"])
        models[key] = {k: v for k, v in raw.items() if k != "loo_beta"}
    small = fit(np.column_stack([np.ones(7), beetles[:7], np.log(area[:7])]),
                fruit[:7], ["intercept", "beetles", "log_area"])
    assert abs(models["beetles+log_area"]["loo_rmse"] - 0.04654) < 0.0001
    return {
        "unit": "forest_fragment", "n": 10,
        "log_area_log_distance_pearson_r": corr(np.log(area), np.log(isolation)),
        "large_area_gap_fold": float(455 / 33.8),
        "models": models,
        "seven_small_fragments": {k: v for k, v in small.items() if k != "loo_beta"}
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    out = {
        "status": "exploratory_same_source_conditional_stress_test",
        "frozen_corpus_changed": False,
        "wandoo": wandoo(), "cardiopetalum": cardiopetalum()
    }
    content = json.dumps(out, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    print("REPRODUCTIVE_ENVIRONMENT_PERSISTENCE_OK " +
          f"fruit_r={out['wandoo']['corr_fruit_pearson_common11']:.6f} " +
          f"seed_r={out['wandoo']['corr_seed_pearson_common11']:.6f} " +
          f"cardio_area_dist_r={out['cardiopetalum']['log_area_log_distance_pearson_r']:.6f}")


if __name__ == "__main__":
    main()
