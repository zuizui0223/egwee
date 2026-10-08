#!/usr/bin/env python3
"""Post hoc predictive comparison: Heliconia 1998 population vs habitat category.

Never interpret the 1998 abundance (measured > decade after fragmentation)
as an unexposed confounder; conditioning on it can remove a fragmentation
pathway. Uses only the 13 independent plot summaries and external-holdout
predictions, not nested individual pseudo-replicates.
"""
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "evidence/meta_extraction/heliconia_plot_cohorts_1999_2005_v1.csv"


def load():
    with CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 13
    for r in rows:
        r["x"] = int(r["baseline_live_1998"])
        r["y"] = int(r["new_seedlings_1999_2005"])
    assert sum(r["y"] for r in rows) == 2590
    return rows


def predict(train, test, method):
    if method == "unconditional_mean":
        return sum(r["y"] for r in train) / len(train)
    if method == "habitat_mean":
        same = [r for r in train if r["habitat"] == test["habitat"]]
        assert same
        return sum(r["y"] for r in same) / len(same)
    if method == "initial_population":
        # Zero-intercept one-parameter forecast; not a causal production law.
        coeff = sum(r["x"] * r["y"] for r in train) / sum(
            r["x"] * r["x"] for r in train
        )
        return coeff * test["x"]
    raise ValueError(method)


def crossval(rows, method, holdout):
    preds = []
    for test in rows:
        train = [
            r for r in rows
            if (r["plot_id"] != test["plot_id"] if holdout == "plot"
                else r["ranch"] != test["ranch"])
        ]
        preds.append((test["y"], predict(train, test, method)))
    return {
        "mse": sum((y - p) ** 2 for y, p in preds) / len(preds),
        "mae": sum(abs(y - p) for y, p in preds) / len(preds),
    }


def main():
    rows = load()
    results = {
        method: {
            "LOPO": crossval(rows, method, holdout="plot"),
            "LORO": crossval(rows, method, holdout="ranch"),
        }
        for method in ("unconditional_mean", "habitat_mean", "initial_population")
    }
    assert abs(results["habitat_mean"]["LOPO"]["mse"] - 34938.540854700856) < 1e-8
    assert abs(results["unconditional_mean"]["LOPO"]["mse"] - 32375.26388888888) < 1e-8
    assert abs(results["initial_population"]["LOPO"]["mse"] - 5922.0483580756945) < 1e-8
    assert abs(math.sqrt(results["initial_population"]["LORO"]["mse"]) - 118.87555570411249) < 1e-7
    assert abs(math.sqrt(results["habitat_mean"]["LORO"]["mse"]) - 254.14097352272208) < 1e-7
    print(json.dumps({
        "status": "PASS", "unit": "7-year recruit counts per independent plot",
        "timing": "baseline living abundance 1998 predicts recruits 1999-2005",
        "methods": results,
        "novelty_boundary": (
            "Exploratory, outcome-seen model comparison in one published "
            "system; no external replication, mechanism or causal effect."
        ),
        "causal_boundary": (
            "1998 abundance is post-fragmentation; adjusting for it may "
            "block a real indirect pathway from fragmentation to recruitment."
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
