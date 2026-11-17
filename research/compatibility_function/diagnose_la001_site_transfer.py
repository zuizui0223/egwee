#!/usr/bin/env python3
"""Post-hoc, source-hashed diagnostic for the already frozen LA001 site holdout.

Requires original Layman et al. (2017) Dryad ZIP as a local input. Does not
redistribute plant IDs, visits, raw phenotypes, genotype calls, or ZIP contents.
No alternative model, parameter tuning, p-values, or replacement primary test.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import fmean

from run_leavenworthia_LA001 import (
    SITES, draw_source, features, ridge_predict, solve,
)

DIR = Path(__file__).resolve().parent
LOCKED_PATH = DIR / "LA001_HELDOUT_RESULT_20261117.json"
POSTHOC_PATH = DIR / "LA001_POSTHOC_EXPOSURE_TRANSPORT_20261117.json"


def linear_percentile(values: list[float], q: float) -> float:
    if not values or not 0 <= q <= 1:
        raise ValueError("Empty values or invalid quantile")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    return ordered[lo] + (pos - lo) * (ordered[hi] - ordered[lo])


def m1_visitation_coefficient(train: list[dict]) -> float:
    """Original M1 ridge coefficient for unscaled log(1+effective visits/hour)."""
    raw = [features(r, "M1_effective_visits") for r in train]
    p = len(raw[0])
    mean = [fmean(row[j] for row in raw) for j in range(p)]
    scale = []
    for j in range(p):
        val = math.sqrt(fmean((row[j] - mean[j]) ** 2 for row in raw))
        scale.append(val if val > 1e-10 else 1.0)
    x = [[1.0] + [(row[j] - mean[j]) / scale[j] for j in range(p)] for row in raw]
    gram = [[sum(row[j] * row[k] for row in x) + (1.0 if j == k and j > 0 else 0.0)
             for k in range(p + 1)] for j in range(p + 1)]
    rhs = [sum(row[j] * r["y"] for row, r in zip(x, train)) for j in range(p + 1)]
    return solve(gram, rhs)[-1] / scale[-1]


def run(source: Path) -> dict:
    locked = json.loads(LOCKED_PATH.read_text(encoding="utf-8"))
    expected = json.loads(POSTHOC_PATH.read_text(encoding="utf-8"))
    meta, rows = draw_source(source)  # checks original SHA, CRC, IDs, 121 sessions
    if (len(rows) != 252 or meta["completed_sessions"] != 121 or
        locked["decision"] != "NO_ROBUST_SINGLE_PROGRAMME_INCREMENT"):
        raise RuntimeError("Source changed or original negative decision not preserved")
    report = []
    for ix, name in enumerate(SITES, 1):
        training = [r for r in rows if r["site"] != ix]
        test = [r for r in rows if r["site"] == ix]
        archived = next(x for x in locked["folds"] if x["site"] == name)
        benchmark = next(x for x in expected["sites"] if x["site"] == name)
        preds = {
            model: ridge_predict(training, test, label)
            for model, label in (
                ("M0", "M0_baseline"),
                ("M1", "M1_effective_visits"),
                ("M2", "M2_all_visits"),
            )
        }
        for model, values in preds.items():
            mse = fmean((r["y"] - yhat) ** 2 for r, yhat in zip(test, values))
            if abs(mse - archived[f"{model}_mse"]) > 1e-9:
                raise RuntimeError(f"Original site holdout not reproducible: {name}/{model}")
        upper = linear_percentile([math.expm1(x["effective"]) for x in training], .95)
        unusual = [x for x in test if math.expm1(x["effective"]) > upper]
        beta = m1_visitation_coefficient(training)
        cell = {
            "site": name, "n": len(test),
            "training_effective_visit_rate_q95": upper,
            "n_above_train_rate_q95": len(unusual),
            "n_above_q95_2014": sum(x["year"] == 2014 for x in unusual),
            "unstandardized_log_visit_coefficient": beta,
            "m0_minus_m1_mse": archived["M0_mse"] - archived["M1_mse"],
            "site_year_SC_descriptive": [],
        }
        for year in (2014, 2015):
            for sc in (0, 1):
                indices = [j for j, x in enumerate(test) if x["year"] == year and x["SC"] == sc]
                if len(indices) < 10:
                    raise RuntimeError("Site-year-SC stratum too sparse")
                scores0 = [(test[j]["y"] - preds["M0"][j]) ** 2 for j in indices]
                scores1 = [(test[j]["y"] - preds["M1"][j]) ** 2 for j in indices]
                cell["site_year_SC_descriptive"].append({
                    "year": year, "genotype": "SC" if sc else "SI", "n": len(indices),
                    "mean_effective_visits_per_flower_hour":
                        fmean(math.expm1(test[j]["effective"]) for j in indices),
                    "m0_minus_m1_mse": fmean(scores0) - fmean(scores1),
                    "m1_minus_m0_mean_pred": fmean(
                        preds["M1"][j] - preds["M0"][j] for j in indices
                    ),
                })
        gain = [
            (row["y"] - a) ** 2 - (row["y"] - b) ** 2
            for row, a, b in zip(test, preds["M0"], preds["M1"])
        ]
        cell["five_most_negative_predictions_contribution_to_site_mean_mse_gain"] = (
            sum(sorted(gain)[:5]) / len(gain)
        )
        # The locked aggregate receipt uses human-readable key names; keep
        # that document immutable and explicitly map only display aliases.
        receipt_keys = {
            "training_effective_visit_rate_q95": "training_visitation_rate_p95",
            "n_above_train_rate_q95": "n_holdout_above_training_p95",
            "n_above_q95_2014": "n_above_in_2014",
            "unstandardized_log_visit_coefficient": "unstandardized_log_visit_coefficient",
            "m0_minus_m1_mse": "m0_minus_m1_mse",
        }
        for key, receipt_key in receipt_keys.items():
            if abs(cell[key] - benchmark[receipt_key]) > 1e-9:
                raise RuntimeError(f"Posthoc source summary drift: {name}/{key}")
        for current, recorded in zip(
            cell["site_year_SC_descriptive"], benchmark.get("subgroup", []),
        ):
            if current["year"] != recorded["year"] or current["genotype"] != recorded["genotype"]:
                raise RuntimeError("Site-year-SC classification changed")
            for key in ("n", "mean_effective_visits_per_flower_hour",
                        "m0_minus_m1_mse", "m1_minus_m0_mean_pred"):
                if abs(current[key] - recorded[key]) > 1e-9:
                    raise RuntimeError(f"Posthoc subgroup summary drift: {name}/{key}")
        report.append(cell)
    return {
        "status": "POSTHOC_SOURCE_REPRODUCED_NO_NEW_HYPOTHESIS_TEST",
        "original_decision": locked["decision"],
        "original_source_sha256": expected["original_source_sha256"],
        "n_plants": 252,
        "source_completed_observation_periods": 121,
        "four_site_diagnostics": report,
        "claim_boundary": [
            "Training/extrapolation diagnostic; not a causal mechanism",
            "No model refit or outcome-based removal of high-visit individuals",
            "No raw plant-level values or original third-party source copied into report",
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-zip", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    result = run(args.source_zip)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "decision": result["original_decision"],
        "out_of_training_range_counts": {
            x["site"]: x["n_above_train_rate_q95"]
            for x in result["four_site_diagnostics"]
        },
    }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
