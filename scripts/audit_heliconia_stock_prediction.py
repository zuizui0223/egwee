#!/usr/bin/env python3
"""Exploratory held-out-plot/ranch prediction from independently reconstructed data.

Predicts 1999-2005 *observed* annual new seedlings using 1998 standing
population size; this is NOT an estimate of fragmentation's direct effect.
Run after audit_heliconia_recruitment_denominators.py.
"""
from __future__ import annotations

import csv
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).parents[1]
HERE = ROOT / "build" / "heliconia_external_audit"
DATA = HERE / "per_plot.csv"


def read_data():
    with DATA.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == 13
    ans = []
    for r in rows:
        ans.append({
            "plot": r["plot"], "habitat": r["habitat"],
            "fragment": float(r["habitat"] != "forest"), "ranch": r["ranch"],
            "stock": float(r["initial_measured_1998"]),
            "new": float(r["mean_new_per_year"]),
            "new_rate": float(r["new_per_measured_stock"]),
        })
    assert len(set(r["plot"] for r in ans)) == 13
    assert sorted(set(r["ranch"] for r in ans)) == ["dimona", "esteio", "porto alegre"]
    assert sum(r["fragment"] for r in ans) == 7
    return ans


def xvec(r, model):
    if model == "mean":
        return [1.0]
    if model == "habitat":
        return [1.0, r["fragment"]]
    if model == "stock":
        return [1.0, r["stock"]]
    if model == "stock+habitat":
        return [1.0, r["stock"], r["fragment"]]
    raise ValueError(model)


def fit(rows, model):
    x = [xvec(r, model) for r in rows]
    m = len(x[0])
    a = [[sum(v[i] * v[j] for v in x) for j in range(m)] +
         [sum(v[i] * r["new"] for v, r in zip(x, rows))]
         for i in range(m)]
    for j in range(m):
        best = max(range(j, m), key=lambda i: abs(a[i][j]))
        a[j], a[best] = a[best], a[j]
        assert abs(a[j][j]) > 1e-9
        pivot = a[j][j]
        for k in range(j, m + 1):
            a[j][k] /= pivot
        for i in range(m):
            if i != j:
                v = a[i][j]
                for k in range(j, m + 1):
                    a[i][k] -= v * a[j][k]
    return [a[i][m] for i in range(m)]


def heldout_prediction(rows, model, heldout):
    sq = []
    ab = []
    for group in sorted(set(heldout(r) for r in rows)):
        test = [r for r in rows if heldout(r) == group]
        train = [r for r in rows if heldout(r) != group]
        b = fit(train, model)
        for row in test:
            yhat = sum(v * c for v, c in zip(xvec(row, model), b))
            err = row["new"] - yhat
            sq.append(err * err)
            ab.append(abs(err))
    return {"mse": sum(sq) / len(sq), "mae": sum(ab) / len(ab)}


def within_ranch_permutation(rows, field):
    """Exploratory permutation respecting fragment labels per ranch, not causal."""
    strata = []
    for ranch in sorted(set(r["ranch"] for r in rows)):
        inds = [i for i, r in enumerate(rows) if r["ranch"] == ranch]
        n = sum(rows[i]["fragment"] for i in inds)
        strata.append(list(itertools.combinations(inds, int(n))))
    frag = [i for i, r in enumerate(rows) if r["fragment"]]
    all_sum = sum(r[field] for r in rows)
    actual_sum = sum(rows[i][field] for i in frag)
    observed = actual_sum / 7 - (all_sum - actual_sum) / 6
    tested = extreme = 0
    for choices in itertools.product(*strata):
        selected = tuple(itertools.chain.from_iterable(choices))
        value = sum(rows[i][field] for i in selected)
        delta = value / 7 - (all_sum - value) / 6
        tested += 1
        extreme += abs(delta) >= abs(observed) - 1e-12
    assert tested == 240
    return {"fragment_minus_continuous": observed, "two_sided_p": extreme / tested, "partitions": tested}


def main():
    rows = read_data()
    mx = sum(r["stock"] for r in rows) / 13
    my = sum(r["new"] for r in rows) / 13
    cross = sum((r["stock"] - mx) * (r["new"] - my) for r in rows)
    vx = sum((r["stock"] - mx)**2 for r in rows)
    vy = sum((r["new"] - my)**2 for r in rows)
    rvalue = cross / math.sqrt(vx * vy)
    models = {}
    for model in ["mean", "habitat", "stock", "stock+habitat"]:
        models[model] = {
            "leave_one_plot_out": heldout_prediction(rows, model, lambda r: r["plot"]),
            "leave_one_ranch_out": heldout_prediction(rows, model, lambda r: r["ranch"]),
        }
    pvals = {
        "annual_new_count": within_ranch_permutation(rows, "new"),
        "new_per_measured_stock": within_ranch_permutation(rows, "new_rate"),
    }
    assert abs(rvalue - 0.9047118469047212) < 1e-10
    assert abs(models["stock"]["leave_one_plot_out"]["mse"] - 131.36016895210207) < 1e-8
    assert abs(models["stock"]["leave_one_ranch_out"]["mse"] - 248.89169178562298) < 1e-8
    assert abs(models["stock+habitat"]["leave_one_ranch_out"]["mse"] - 280.36369871855953) < 1e-8
    assert abs(pvals["annual_new_count"]["two_sided_p"] - 0.2375) < 1e-12
    assert abs(pvals["new_per_measured_stock"]["two_sided_p"] - (191 / 240)) < 1e-12

    result = {
        "status": "POST_HOC_EXPLORATORY_PREDICTION_NOT_CAUSAL",
        "n_plots": len(rows),
        "n_spatial_blocks": 3,
        "correlation_initial_stock_1998_vs_annual_new_1999_2005": rvalue,
        "models": models,
        "within_ranch_label_partitions": pvals,
        "cautions": [
            "Initial 1998 population size is measured AFTER historical fragmentation",
            "Baseline stock can mediate or encode historical fragmentation effects",
            "Measured recruits are not a controlled seed or maternal fecundity outcome",
            "Ranch-held-out predictions cover only three geographic blocks",
            "A lower predictive MSE is not evidence for no habitat effect",
            "Blockwise label exchangeability is unverified; permutation probabilities are descriptive",
        ],
    }
    (HERE / "stock_prediction.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("HELICONIA_STOCK_PREDICTION: PASS " + json.dumps({
        "stock_recruit_r": round(rvalue, 6),
        "plot_mse_stock": round(models["stock"]["leave_one_plot_out"]["mse"], 3),
        "plot_mse_stock_plus_habitat": round(models["stock+habitat"]["leave_one_plot_out"]["mse"], 3),
        "ranch_mse_stock": round(models["stock"]["leave_one_ranch_out"]["mse"], 3),
        "ranch_mse_stock_plus_habitat": round(models["stock+habitat"]["leave_one_ranch_out"]["mse"], 3),
        "blocked_permutation_p": pvals["annual_new_count"]["two_sided_p"],
    }))


if __name__ == "__main__":
    main()
