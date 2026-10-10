#!/usr/bin/env python3
"""Chronologically honest reproduction-to-recruitment lead/lag test.

Exploratory one-programme Heliconia archive check, NOT causal mediation,
not a frozen EGWEE meta-analysis admission. For each year >= 2003 predict
first recorded seedlings using only outcomes from EARLIER calendar years.
The 1998-2005 raw census is pinned by the existing source-hash verifier.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

from analyze_heliconia_census_panel import load_csv

YEARS = range(2001, 2006)
FORECAST_YEARS = (2003, 2004, 2005)
FEATURES = {
    "intercept_only": (),
    "linear_calendar_trend": ("trend",),
    "fragmentation_class": ("fragment",),
    "prior_recruits": ("prior_new",),
    "prior_live_stock": ("stock",),
    "lag1_flowering": ("fl1",),
    "lag2_flowering": ("fl2",),
    "lag3_flowering": ("fl3",),
    "lag1_inflorescences": ("inflo1",),
    "lag2_inflorescences": ("inflo2",),
    "stock_plus_prior_recruits": ("stock", "prior_new"),
    "stock_plus_lag1_flowering": ("stock", "fl1"),
    "stock_plus_lag2_flowering": ("stock", "fl2"),
    "stock_plus_lag3_flowering": ("stock", "fl3"),
    "stock_plus_all_flowering_lags": ("stock", "fl1", "fl2", "fl3"),
    "stock_plus_lag1_inflorescences": ("stock", "inflo1"),
    "stock_plus_calendar_trend": ("stock", "trend"),
    "stock_plus_lag1_flowering_and_trend": ("stock", "fl1", "trend"),
}

def archive_rows(local: Path | None) -> tuple[list[dict],dict]:
    plots = {r["plot_id"]: r for r in load_csv("HDP_plots.csv", local)}
    survey = load_csv("HDP_survey.csv", local)
    assert len(plots) == 13 and len(survey) == 66396
    counts = defaultdict(lambda: {"measured": 0, "missing": 0, "dead": 0,
                                   "new": 0, "fl": 0, "inflo": 0, "records": 0})
    ids = set()
    marked = set()
    for rec in survey:
        plot, ident, year = rec["plot_id"], rec["plant_id"], int(rec["year"])
        key = (plot, ident, year)
        assert key not in ids
        ids.add(key)
        assert rec["census_status"] in {"measured", "missing", "dead"}
        r = counts[(plot, year)]
        state = rec["census_status"]
        r["records"] += 1
        r[state] += 1
        if rec["recorded_sdlg"] == "TRUE":
            assert state == "measured" and (plot, ident) not in marked
            marked.add((plot, ident))
            r["new"] += 1
        infl = rec["infl"].strip()
        if infl and infl.upper() != "NA":
            v = float(infl)
            assert math.isfinite(v) and v >= 0 and state == "measured"
            r["inflo"] += v
            r["fl"] += int(v > 0)
    assert len(ids) == 66396 and len(marked) == 3464
    zero_cells = sorted((p, yr, v["missing"]) for (p, yr), v in counts.items()
                        if 1998 <= yr <= 2005 and v["records"] and v["measured"] == 0)
    assert zero_cells == [("CF-4",2000,116), ("CF-5",2000,171), ("CF-6",2003,278)]
    rows, exclusions = [], []
    for year in YEARS:
        for p in sorted(plots):
            current = counts[(p, year)]
            history = [counts[(p, year - lag)] for lag in (1,2,3)]
            assert current["records"] > 0 and all(x["records"] > 0 for x in history)
            if current["measured"] == 0 or any(x["measured"] == 0 for x in history):
                exclusions.append({"plot": p, "year": year,
                                   "missing_census_years": [y for y in range(year-3,year+1)
                                                            if counts[(p,y)]["measured"] == 0]})
                continue
            rows.append({
                "plot": p, "ranch": plots[p]["ranch"], "year": year,
                "fragment": float(plots[p]["habitat"] != "forest"),
                "trend": float(year - 2001),
                "stock": float(history[0]["measured"]),
                "prior_new": float(history[0]["new"]),
                "fl1": float(history[0]["fl"]),
                "fl2": float(history[1]["fl"]),
                "fl3": float(history[2]["fl"]),
                "inflo1": float(history[0]["inflo"]),
                "inflo2": float(history[1]["inflo"]),
                "y": float(current["new"]),
            })
    assert len(rows) + len(exclusions) == 65
    assert len({r["plot"] for r in rows}) == 13
    assert set(r["year"] for r in rows) == set(YEARS)
    return rows, {
        "n_original_plant_year_rows": len(survey),
        "potential_2001_2005_plot_years": 65,
        "n_complete_observation_plot_years": len(rows),
        "n_screened_out": len(exclusions),
        "excluded": exclusions,
        "whole_plot_all_missing_cells": zero_cells,
        "years_for_training_before_prediction": [2001, 2002, 2003, 2004],
        "held_future_years": list(FORECAST_YEARS),
    }


def ridge_predict(train: list[dict], test: list[dict], features: tuple[str,...]) -> list[float]:
    assert train and test and max(r["year"] for r in train) < min(r["year"] for r in test)
    mean_y = sum(r["y"] for r in train) / len(train)
    if not features:
        return [mean_y] * len(test)
    mu = {f: sum(r[f] for r in train) / len(train) for f in features}
    sd = {f: max(1e-8, math.sqrt(sum((r[f]-mu[f])**2 for r in train) / len(train)))
          for f in features}
    X = [[(r[f]-mu[f])/sd[f] for f in features] for r in train]
    Y = [r["y"]-mean_y for r in train]
    d=len(features)
    mat = [[sum(x[i]*x[j] for x in X)+(1.0 if i==j else 0.0)
            for j in range(d)] + [sum(x[i]*y for x,y in zip(X,Y))]
           for i in range(d)]
    for j in range(d):
        best=max(range(j,d),key=lambda i: abs(mat[i][j]))
        mat[j],mat[best]=mat[best],mat[j]
        assert abs(mat[j][j]) > 1e-10
        v=mat[j][j]
        for k in range(j,d+1): mat[j][k]/=v
        for i in range(d):
            if i==j: continue
            a=mat[i][j]
            for k in range(j,d+1): mat[i][k]-=a*mat[j][k]
    beta=[mat[i][d] for i in range(d)]
    return [max(0.,mean_y+sum(beta[i]*(r[f]-mu[f])/sd[f]
                               for i,f in enumerate(features))) for r in test]


def forward_validation(rows: list[dict], features: tuple[str,...]) -> dict:
    preds=[]
    for held in FORECAST_YEARS:
        train=[r for r in rows if r["year"] < held]
        test=[r for r in rows if r["year"] == held]
        assert len(train)>=15 and len(test)>=8 and not(set(id(z) for z in train) & set(id(z) for z in test))
        forecast=ridge_predict(train,test,features)
        preds.extend([{"plot":r["plot"],"ranch":r["ranch"],"year":held,"habitat":r["fragment"],
                       "observed":r["y"],"predicted":v} for r,v in zip(test,forecast)])
    expected=sum(r["year"] in FORECAST_YEARS for r in rows)
    assert len(preds)==expected and len({(r["plot"],r["year"]) for r in preds})==expected
    def mse(a):
        return sum((r["observed"]-r["predicted"])**2 for r in a)/len(a)
    def mae(a):
        return sum(abs(r["observed"]-r["predicted"]) for r in a)/len(a)
    by_year={str(y): mse([r for r in preds if r["year"]==y]) for y in FORECAST_YEARS}
    by_ranch={ranch: mse([r for r in preds if r["ranch"]==ranch])
              for ranch in sorted({r["ranch"] for r in preds})}
    return {
        "n_predictions":len(preds),
        "mse_pooled_plot_years":mse(preds),
        "mae_pooled_plot_years":mae(preds),
        "mse_equal_future_years":sum(by_year.values())/len(by_year),
        "mse_equal_ranches":sum(by_ranch.values())/len(by_ranch),
        "mse_by_future_year":by_year,
        "mse_by_ranch":by_ranch,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--local-dir", type=Path)
    ap.add_argument("--output", type=Path)
    args=ap.parse_args()
    rows,provenance=archive_rows(args.local_dir)
    out={k:forward_validation(rows,v) for k,v in FEATURES.items()}
    base=out["intercept_only"]["mse_pooled_plot_years"]
    for record in out.values():
        record["fraction_mse_improvement_over_intercept"]=1-record["mse_pooled_plot_years"]/base
    assert all(v["n_predictions"]==sum(x["year"] in FORECAST_YEARS for x in rows)
               for v in out.values())
    result={
        "status":"POST_HOC_FORWARD_YEAR_SPLIT_EXPLORATORY_NOT_CAUSAL",
        "source_pin":"BrunaLab/HeliconiaSurveys 0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0",
        "provenance":provenance,
        "candidate_models":out,
        "claim_ceiling":[
            "Only earlier calendar-year outcomes are used; this is temporal transfer, not across-ranch transfer.",
            "The same 2001-2005 fully observed predictor/response cells are used for all lag comparisons.",
            "Lagged flowering and archived inflorescences are recorded reproduction indicators, not viable seed rain.",
            "Source statuses with all plants missing are not biological zero recruitment.",
            "The fixed candidate menu and forward folds were designed after seeing the earlier spatial CV results.",
            "Post-fragmentation stock can be a mediator; controlling it is not a causal effect estimate.",
            "Three forecast years, 13 plots, three ranches from one prior published ecosystem study.",
            "Do not select the winning lag post hoc as a biological seed-bank duration.",
            "No new corpus admission or unapproved manuscript claim.",
        ],
    }
    if args.output:
        args.output.parent.mkdir(exist_ok=True,parents=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("HELICONIA_FORWARD_TEMPORAL_SENTINEL: PASS")
    print(json.dumps({
        "provenance":provenance,
        "scores":{k: {"mse":round(v["mse_pooled_plot_years"],3),
                       "mae":round(v["mae_pooled_plot_years"],3),
                       "equal_year_mse":round(v["mse_equal_future_years"],3),
                       "equal_ranch_mse":round(v["mse_equal_ranches"],3),
                       "year_mse":{yr:round(z,3) for yr,z in v["mse_by_future_year"].items()},
                       "n":v["n_predictions"]}
                  for k,v in out.items()},
    },ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
