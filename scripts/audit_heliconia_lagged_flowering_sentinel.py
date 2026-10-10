#!/usr/bin/env python3
"""Source-pinned test of lagged flowering as a Heliconia recruitment sentinel.

Exploratory out-of-plot/ranch prediction, not fragmentation causal inference.
The archived flowering indicator is NOT effective mating or pollen delivery.
No observations from this file enter the frozen EGWEE meta-analytic corpus.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path

from analyze_heliconia_census_panel import load_csv

ROOT = Path(__file__).resolve().parents[1]
YEARS = tuple(range(1999, 2006))
PREDICTORS = {
    "year_only": (),
    "habitat": ("fragment",),
    "prior_live_stock": ("stock",),
    "prior_flowering_individuals": ("flowering",),
    "prior_inflorescences": ("inflo",),
    "stock_plus_habitat": ("stock", "fragment"),
    "stock_plus_flowering": ("stock", "flowering"),
    "stock_plus_inflorescences": ("stock", "inflo"),
    "flowering_plus_habitat": ("flowering", "fragment"),
}


def load(local_dir: Path | None) -> tuple[list[dict], dict]:
    plots_raw = load_csv("HDP_plots.csv", local_dir)
    plants_raw = load_csv("HDP_survey.csv", local_dir)
    assert len(plots_raw) == 13 and len(plants_raw) == 66396
    plots = {p["plot_id"]: p for p in plots_raw}
    assert len(plots) == 13
    rec: dict[tuple[str, int], dict[str, float]] = defaultdict(
        lambda: dict(records=0.0, stock=0.0, dead=0.0, missing=0.0, flowering=0.0, inflo=0.0, new=0.0,
                     measured_no_infl=0.0, nonmeasured_infl=0.0)
    )
    keys, new_ids = set(), set()
    trajectory = defaultdict(dict)
    infl_types = Counter()
    for r in plants_raw:
        plot, ident, year = r["plot_id"], r["plant_id"], int(r["year"])
        assert plot in plots and 1998 <= year <= 2009
        key = (plot, ident, year)
        assert key not in keys
        keys.add(key)
        trajectory[(plot, ident)][year] = r["census_status"]
        row = rec[(plot, year)]
        row["records"] += 1
        assert r["census_status"] in {"measured", "dead", "missing"}
        alive = r["census_status"] == "measured"
        if alive:
            row["stock"] += 1
        elif r["census_status"] == "dead":
            row["dead"] += 1
        else:
            row["missing"] += 1
        raw = r["infl"].strip()
        if raw and raw.upper() != "NA":
            value = float(raw)
            assert math.isfinite(value) and value >= 0
            if alive:
                row["inflo"] += value
                if value > 0:
                    row["flowering"] += 1
            else:
                row["nonmeasured_infl"] += 1
            infl_types["reported_numeric"] += 1
        elif alive:
            row["measured_no_infl"] += 1
        if r["recorded_sdlg"] == "TRUE":
            assert alive
            identity = (plot, ident)
            assert identity not in new_ids
            new_ids.add(identity)
            row["new"] += 1
    assert len(keys) == 66396 and len(new_ids) == 3464

    rows = []
    zero_prior_stock = []
    year_profiles = {}
    for year in YEARS:
        prior = [rec[(p, year - 1)] for p in plots]
        year_profiles[str(year - 1)] = {
            "plots_with_documented_flowering": sum(v["flowering"] > 0 for v in prior),
            "flowering_individuals": int(sum(v["flowering"] for v in prior)),
            "inflorescences": int(sum(v["inflo"] for v in prior)),
            "living_individuals": int(sum(v["stock"] for v in prior)),
            "ranches_with_documented_flowering": len({
                plots[p]["ranch"] for p in plots if rec[(p, year - 1)]["flowering"] > 0
            }),
        }
        for p in sorted(plots):
            previous, current = rec[(p, year - 1)], rec[(p, year)]
            assert previous["records"] > 0 and current["records"] > 0, (p, year)
            if previous["stock"] == 0:
                zero_prior_stock.append({"plot": p, "prior_year": year - 1,
                                        "measured": previous["stock"], "dead": previous["dead"],
                                        "missing": previous["missing"], "records": previous["records"]})
            rows.append({
                "plot": p, "ranch": plots[p]["ranch"], "year": year,
                "fragment": float(plots[p]["habitat"] != "forest"),
                "stock": previous["stock"],
                "prior_census_measured": previous["stock"] > 0,
                "outcome_census_measured": current["stock"] > 0,
                "flowering": previous["flowering"],
                "inflo": previous["inflo"], "y": current["new"],
            })
    assert len(rows) == 13 * len(YEARS)
    assert sum(r["y"] for r in rows) == 2590
    # Reject a pooled proxy if entire source-year lacks any documented flowers.
    eligible = [
        y for y in YEARS
        if year_profiles[str(y - 1)]["ranches_with_documented_flowering"] == 3
    ]
    blackouts = []
    for p in sorted(plots):
        for yr in range(1998, 2006):
            cell = rec[(p, yr)]
            if cell["stock"] or not cell["records"]:
                continue
            missing_identities = [identity for (plot, identity), history in trajectory.items()
                                  if plot == p and history.get(yr) == "missing"]
            found_before = sum(trajectory[(p, z)].get(yr - 1) == "measured"
                               for z in missing_identities)
            found_next = sum(trajectory[(p, z)].get(yr + 1) == "measured"
                             for z in missing_identities)
            found_any_later = sum(any(state == "measured" for y, state in trajectory[(p, z)].items()
                                      if y > yr) for z in missing_identities)
            blackouts.append({"plot": p, "year": yr, "all_missing_records": len(missing_identities),
                              "same_id_measured_in_previous_year": found_before,
                              "same_id_measured_next_year": found_next,
                              "same_id_measured_any_later_year": found_any_later})
    assert [(r["plot"], r["year"], r["all_missing_records"],
             r["same_id_measured_next_year"]) for r in blackouts] == [
        ("CF-4", 2000, 116, 111),
        ("CF-5", 2000, 171, 155),
        ("CF-6", 2003, 278, 247),
    ], blackouts
    profile = {
        "source_plant_years": len(plants_raw), "observed_new_seedlings_1999_2005": 2590,
        "years_by_prior_flowering_record": year_profiles,
        "lagged_years_with_all_ranches_reporting_at_least_one_flower": eligible,
        "excluded_prior_flowering_years": sorted(set(YEARS) - set(eligible)),
        "nonmeasured_rows_with_numeric_infl": int(sum(r["nonmeasured_infl"] for r in rec.values())),
        "zero_prior_stock_plot_years": zero_prior_stock,
        "whole_plot_zero_measurement_diagnostic": blackouts,
        "zero_confirmed_live_plot_years_1998_2005": [
            {"plot": p, "year": yr,
             "measured": rec[(p, yr)]["stock"],
             "dead": rec[(p, yr)]["dead"],
             "missing": rec[(p, yr)]["missing"],
             "new": rec[(p, yr)]["new"]}
            for p in sorted(plots) for yr in range(1998, 2006)
            if rec[(p, yr)]["stock"] == 0
        ],
        "status": "DOCUMENTED_FLOWERING_NOT_VERIFIED_ZERO_WHEN_NA",
    }
    return rows, profile


def solve(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    if not n:
        return []
    x = [r[:] + [v] for r, v in zip(a, b)]
    for j in range(n):
        pivot = max(range(j, n), key=lambda i: abs(x[i][j]))
        x[pivot], x[j] = x[j], x[pivot]
        assert abs(x[j][j]) > 1e-10
        scale = x[j][j]
        for k in range(j, n + 1):
            x[j][k] /= scale
        for i in range(n):
            if i == j:
                continue
            z = x[i][j]
            for k in range(j, n + 1):
                x[i][k] -= z * x[j][k]
    return [x[i][-1] for i in range(n)]


def fit_predict(train: list[dict], test: list[dict], predictors: tuple[str, ...]) -> list[float]:
    """Year-intercept ridge: all preprocessing strictly within training folds."""
    years = sorted({r["year"] for r in train})
    assert {r["year"] for r in test} <= set(years)
    mu_y = {y: sum(r["y"] for r in train if r["year"] == y)
                 / sum(r["year"] == y for r in train) for y in years}
    if not predictors:
        return [mu_y[r["year"]] for r in test]
    mean_x = {}
    scales = []
    for j, key in enumerate(predictors):
        mean_x[key] = {
            y: sum(r[key] for r in train if r["year"] == y)
               / sum(r["year"] == y for r in train)
            for y in years
        }
        sdev = math.sqrt(sum(
            (r[key] - mean_x[key][r["year"]]) ** 2 for r in train
        ) / len(train))
        scales.append(max(sdev, 1e-8))
    xx = [[(r[key] - mean_x[key][r["year"]]) / scales[j]
           for j, key in enumerate(predictors)] for r in train]
    yy = [r["y"] - mu_y[r["year"]] for r in train]
    n = len(predictors)
    gram = [[sum(x[i] * x[j] for x in xx) + (1.0 if i == j else 0.0)
             for j in range(n)] for i in range(n)]
    rhs = [sum(x[j] * dy for x, dy in zip(xx, yy)) for j in range(n)]
    beta = solve(gram, rhs)
    return [max(0.0, mu_y[r["year"]] + sum(
        beta[j] * (r[key] - mean_x[key][r["year"]]) / scales[j]
        for j, key in enumerate(predictors)
    )) for r in test]


def grouped_cv(rows: list[dict], pred: tuple[str, ...], unit: str) -> dict:
    keys = sorted({r[unit] for r in rows})
    predictions = []
    for held in keys:
        train, test = [r for r in rows if r[unit] != held], [
            r for r in rows if r[unit] == held
        ]
        for r, v in zip(test, fit_predict(train, test, pred)):
            predictions.append({"plot": r["plot"], "year": r["year"],
                                "obs": r["y"], "pred": v})
    assert len(predictions) == len(rows)
    by_plot = {
        p: [r for r in predictions if r["plot"] == p]
        for p in sorted({r["plot"] for r in rows})
    }
    plot_scores = {
        p: {"mse": sum((r["obs"] - r["pred"])**2 for r in v)/len(v),
            "mae": sum(abs(r["obs"] - r["pred"]) for r in v)/len(v)}
        for p, v in by_plot.items()
    }
    return {
        "mse_equal_plot_year": sum(r["mse"] for r in plot_scores.values()) / len(plot_scores),
        "mae_equal_plot_year": sum(r["mae"] for r in plot_scores.values()) / len(plot_scores),
        "plot_mse": {p: round(v["mse"], 6) for p, v in plot_scores.items()},
        "heldout_units": len(keys),
    }


def analyze(rows: list[dict]) -> dict:
    result = {}
    for name, pred in PREDICTORS.items():
        result[name] = {
            "leave_one_plot_out": grouped_cv(rows, pred, "plot"),
            "leave_one_ranch_out": grouped_cv(rows, pred, "ranch")
        }
    for fold in ("leave_one_plot_out", "leave_one_ranch_out"):
        base = result["year_only"][fold]["mse_equal_plot_year"]
        assert base > 0
        for metrics in result.values():
            metrics[fold]["mse_improvement_vs_year_only"] = (
                (base - metrics[fold]["mse_equal_plot_year"]) / base
            )
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--local-dir", type=Path, default=None)
    ap.add_argument("--output", type=Path, default=None)
    args = ap.parse_args()
    rows, profile = load(args.local_dir)
    valid_years = set(profile["lagged_years_with_all_ranches_reporting_at_least_one_flower"])
    if len(valid_years) < 3:
        final = {"status": "HOLD_INADEQUATE_DOCUMENTED_FLOWERING_COVERAGE",
                 "profile": profile, "models": None}
    else:
        complete = [r for r in rows if r["year"] in valid_years]
        observation_screened = [r for r in complete if r["prior_census_measured"]
                                and r["outcome_census_measured"]]
        assert len(observation_screened) == 85
        def mean_recruits(sample: list[dict]) -> dict:
            outcome = {}
            for group in (0.0, 1.0):
                group_rows = [r for r in sample if r["fragment"] == group]
                by_plot = {r["plot"] for r in group_rows}
                means = [sum(r["y"] for r in group_rows if r["plot"] == p)
                         / sum(r["plot"] == p for r in group_rows) for p in by_plot]
                outcome["continuous" if group == 0 else "fragment"] = {
                    "plot_year_records": len(group_rows),
                    "new_seedlings": int(sum(r["y"] for r in group_rows)),
                    "equal_plot_mean_annual_new_seedlings": sum(means) / len(means),
                }
            return outcome
        final = {
            "status": "POST_HOC_EXPLORATORY_OUT_OF_LANDSCAPE_PREDICTION",
            "profile": profile, "n_rows_all_balanced": len(rows),
            "n_rows_restricted": len(complete),
            "n_rows_observation_screened": len(observation_screened),
            "new_seedling_denominator_sensitivity": {
                "all_archive_plot_years": mean_recruits(rows),
                "observed_outcome_census_only": mean_recruits(
                    [r for r in rows if r["outcome_census_measured"]]),
                "both_outcome_and_predictor_observed": mean_recruits(observation_screened),
            },
            "excluded_plot_year_pairs_due_to_zero_measured": [
                {"plot": r["plot"], "year": r["year"],
                 "prior_measured": r["prior_census_measured"],
                 "outcome_measured": r["outcome_census_measured"]}
                for r in complete if r not in observation_screened
            ],
            "unscreened_models_sensitivity": analyze(rows),
            "observation_screened_models": analyze(observation_screened),
            "interpretation_limit": [
                "A documented flowering record is not confirmed effective pollination or seed production.",
                "NA inflorescence means absent observation/flowering report, not a certified zero.",
                "The lag precedes seedling detection but dispersal/seed bank may introduce longer lags.",
                "Flowering history, living stock and habitat can all encode earlier fragmentation.",
                "New seedlings are first detected seedlings, not total deposited viable seeds.",
                "Entire plot-years with zero confirmed measured individuals and archival missing statuses cannot safely be coded as surveyed biological zero. Screen both exposure and outcome censuses.",
                "Later re-detection of the same IDs can disprove local extinction but cannot by itself establish a precise missing-survey cause.",
                "The screen is conditional on nonzero detected stock and can select against genuine local extinction; compare unscreened sensitivity, never infer true habitat equivalence.",
                "Plot-year counts are nested in 13 plots across only three ranch contexts.",
                "Ridge alpha=1 in within-year standardized feature coordinates was fixed before outcome scoring.",
                "All model comparisons are post hoc and cannot establish causation, field prevalence or novelty.",
                "No frozen EGWEE programme or source denominator was changed."
            ],
        }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
    print("HELICONIA_LAGGED_FLOWERING_AUDIT: " + final["status"])
    print(json.dumps({
        "profile": profile,
        "n_rows_observation_screened": final.get("n_rows_observation_screened"),
        "new_seedling_denominator_sensitivity": final.get("new_seedling_denominator_sensitivity"),
        "plot_mse": {k: round(v["leave_one_plot_out"]["mse_equal_plot_year"], 4)
                     for k, v in (final.get("observation_screened_models") or {}).items()},
        "ranch_mse": {k: round(v["leave_one_ranch_out"]["mse_equal_plot_year"], 4)
                      for k, v in (final.get("observation_screened_models") or {}).items()},
        "unscreened_plot_mse": {k: round(v["leave_one_plot_out"]["mse_equal_plot_year"], 4)
                     for k, v in (final.get("unscreened_models_sensitivity") or {}).items()},
    }, indent=2))


if __name__ == "__main__":
    main()
