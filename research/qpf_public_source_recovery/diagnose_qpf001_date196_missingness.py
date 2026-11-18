#!/usr/bin/env python3
"""POSTHOC audit: original QPF001 date-heldout prediction support + fruit recovery.

This script may ONLY describe the original frozen QPF001 model predictions and
original response ascertainment. No new model, p-value, outcome, hyperparameter,
date selection for confirmatory claims, or reinterpretation of a primary null.
Requires the exact original source ZIP held privately by the researcher.
Outputs ONLY date-group / recovered-vs-unrecovered group aggregates, no flowers.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
from statistics import mean

from run_qpf001_original_flower_dateholdout import (
    DAYS, FREEZE_SHA, _binary_original, _xlsx_data,
    audit_source, numeric, predict, verify_protocol,
)

HERE = Path(__file__).resolve().parent
LOCKED = HERE / "QPF001_DATE_HOLDOUT_ORIGINAL_RESULT_20261118.json"


def decompose_frozen_folds(original: dict) -> dict:
    folds = original["folds"]
    if [x["day"] for x in folds] != list(DAYS):
        raise ValueError("The original 8 held-out date folds changed")
    if sum(x["n"] for x in folds) != 93:
        raise ValueError("Original 93 scored flowers changed")
    source = original["pooled"]
    contributions = [{
        "day": x["day"],
        "n_scored": x["n"],
        "M0_minus_M1_date_mse": x["M0_minus_M1_mse"],
        "contribution_to_93flower_M0minusM1_mse":
            x["n"] * x["M0_minus_M1_mse"] / 93,
    } for x in folds]
    pooled = sum(r["contribution_to_93flower_M0minusM1_mse"]     for r in contributions)
    if abs(pooled - source["M0_minus_M1_mse"]) > 1e-11:
        raise ValueError("Original MSE gain cannot be reconstructed")
    remainder = [r for r in contributions if r["day"] != 196]
    n_remaining = sum(r["n_scored"] for r in remainder)
    return {
        "original_complete_case_mse_gain": pooled,
        "all_frozen_date_score_contributions": contributions,
        "day196_score_contribution_to_93flower_mse_gain": next(
            r["contribution_to_93flower_M0minusM1_mse"]
            for r in contributions if r["day"] == 196
        ),
        "other7_dates_n": n_remaining,
        "other7_dates_original_prediction_mse_gain_without_refit": (
            sum(r["contribution_to_93flower_M0minusM1_mse"] for r in remainder)
            * 93 / n_remaining
        ),
        "diagnostic_not_an_alternative_registered_estimator": True,
    }


def mean_or_none(rows: list[dict], getter):
    a = [getter(row) for row in rows]
    a = [v for v in a if v is not None and math.isfinite(v)]
    return mean(a) if a else None


def original_visits_hour(row: dict) -> float:
    return sum(numeric(row[c]) for c in (
        "Large.bee.visits", "Small.bee.visits",
        "Small.fly.visits", "Large.fly.visits",
    )) / numeric(row["Duration.hours"])


def source_diagnostic(source_zip: Path) -> dict:
    verify_protocol()  # historic preregistered protocol unchanged in Git
    old = json.loads(LOCKED.read_text(encoding="utf-8"))
    if (old["protocol_commit"] != FREEZE_SHA or
        old["registered_decision"] != "NO_ROBUST_WITHIN_STUDY_DATE_TRANSFER_GAIN"):
        raise ValueError("Original registered result was unexpectedly modified")
    records = _xlsx_data(_binary_original(source_zip))  # exact SHA & source CRC
    scored, receipt = audit_source(records)
    if len(records) != 122 or len(scored) != 93:
        raise ValueError("Original fruit complete-case denominator changed")
    source_dates = []
    for day in DAYS:
        all_ = [row for row in records if int(row["Julian.day"]) == day]
        held = [row for row in scored if int(row["Julian.day"]) == day]
        missing = [row for row in all_ if numeric(row["Seed.set"]) is None]
        train = [row for row in scored if int(row["Julian.day"]) != day]
        old_fold = next(x for x in old["folds"] if x["day"] == day)
        if len(held) != old_fold["n"]:
            raise ValueError("Original date fruit-ascertainment count changed")
        p0 = predict(train, held, False)
        p1 = predict(train, held, True)
        for name, values in (("M0", p0), ("M1", p1)):
            mse = mean((p - row["Seed.set"])**2           for p, row in zip(values, held))
            mae = mean(abs(p - row["Seed.set"])           for p, row in zip(values, held))
            if (abs(mse - old_fold[name+"_mse"]) > 1e-10 or    abs(mae - old_fold[name+"_mae"]) > 1e-10):    raise RuntimeError(        "Original date heldout forecasts no longer reproduce"    )
        missing_context = lambda row: (
            numeric(row["Con.abundance"]) is None or
            numeric(row["Het.abundance"]) is None
        )
        source_dates.append({
            "day": day,
            "n_filmed": len(all_),
            "n_recovered_fruit_seedset": len(held),
            "n_unrecovered_seedset": len(missing),
            "unrecovered_fraction": len(missing) / len(all_),
            "n_context_missing_among_recovered": sum(missing_context(r) for r in held),
            "n_context_missing_among_unrecovered": sum(missing_context(r) for r in missing),
            "mean_recorded_seedset_in_recovered": mean(    numeric(r["Seed.set"]) for r in held
            ),
            "mean_locked_M0_prediction": mean(p0),
            "mean_locked_M1_prediction": mean(p1),
            "predictions_reused_without_model_selection": True,
        })
    by_group = {}
    groups = {
        "recovered_fruit_seedset": scored,
        "unrecovered_no_seedset": [
            r for r in records if numeric(r["Seed.set"]) is None
        ],
    }
    for name, group in groups.items():
        by_group[name] = {
            "n": len(group),
            "mean_stigmatic_conspecific_pollen_grains": mean_or_none(    group, lambda r: numeric(r["CP.Count"])
            ),
            "mean_stigmatic_heterospecific_pollen_grains": mean_or_none(    group, lambda r: numeric(r["HP.Count"])
            ),
            "mean_eligible_visitor_contacts_per_film_hour": mean_or_none(    group, original_visits_hour
            ),
        }
    if [r["n_filmed"] for r in source_dates] != [31,18,26,20,8,6,8,5]:
        raise ValueError("Original filmed-date sample counts changed")
    if sum(r["n_unrecovered_seedset"] for r in source_dates) != 29:
        raise ValueError("Missing 29 fruit outcomes not accounted for")
    if sum(r["n_context_missing_among_recovered"] for r in source_dates) != 5:
        raise ValueError("Five recovered-fruit context NA rows not accounted for")
    day196 = next(r for r in source_dates if r["day"]==196)
    if day196["n_context_missing_among_recovered"] != 4:
        raise ValueError("Late day-196 four missing context rows changed")
    if abs(day196["mean_recorded_seedset_in_recovered"] - .005) > 1e-12:
        raise ValueError("Late-day observed seed-set magnitude changed")
    mismatch_by_day = Counter()
    for r in scored:
        seed = numeric(r["Seed.count"])
        ovule = numeric(r["Ovule"])
        weight = numeric(r["Seed.weights"])
        if seed+ovule>0 and weight>0:
            if abs(seed/weight - seed/(seed+ovule)) > 1e-9:    mismatch_by_day[int(r["Julian.day"])] += 1
    if sum(mismatch_by_day.values()) != 10:
        raise ValueError("Original source Seed.set denominator audit changed")
    return {
        "analysis_id": "QPF001_posthoc_date196_support_and_fruit_recovery",
        "classification": "POST_OUTCOME_SOURCE_DIAGNOSTIC_NOT_A_NEW_HYPOTHESIS_TEST",
        "original_protocol_commit": old["protocol_commit"],
        "original_scientific_decision": old["registered_decision"],
        "original_source_zip_sha256": old["original_zip_sha256"],
        "original_source_xlsx_sha256": old["original_xlsx_sha256"],
        "n_filmed_flowers": len(records),
        "n_source_seedset_recorded":len(scored),
        "n_source_seedset_unrecovered":len(records)-len(scored),
        "date_source_ascertainment_and_original_model_predictions":source_dates,
        "original_frozen_model_score_decomposition":decompose_frozen_folds(old),
        "recovered_vs_unrecovered_upstream_measurement_means":by_group,
        "source_vs_published_seedset_denominator_disagreement_by_date":{
            str(k):v for k,v in sorted(mismatch_by_day.items())
        },
        "evidence_ceiling": [
            "The primary date CV and negative registered decision are NOT changed.",
            "Omitting day196 from existing loss sums is descriptive source decomposition, NOT retraining, preregistered sensitivity, or permission to select favourable dates.",
            "The final filming day is outside training dates and all four recovered flowers lack floral-neighborhood measurements.",
            "The four late flowers have near-zero source seed set, but this does not determine whether pollen, resources, seed abortion or observation/fruit ascertainment caused it.",
            "Mean upstream CP/HP/visitor contrasts between recovered and unrecovered fruits do not identify the unobserved seed-set outcomes, missingness mechanism, or causality.",
            "Only one site and eight dates; not an independent cross ecosystem test or a generalized eco-genetic mechanism.",
            "Original raw flower/seed/visitor rows were not redistributed."
        ],
        "individual_source_flower_records_exported": False,
        "new_fit_or_inferential_test_conducted": False,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source-zip",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    a=parser.parse_args()
    result=source_diagnostic(a.source_zip)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",            encoding="utf-8")
    score=result["original_frozen_model_score_decomposition"]
    print(json.dumps({
        "classification":result["classification"],
        "main_decision":result["original_scientific_decision"],
        "n_original_source":result["n_filmed_flowers"],
        "n_source_seedset":result["n_source_seedset_recorded"],
        "full_MSE_gain":score["original_complete_case_mse_gain"],
        "day196_gain_contribution":score["day196_score_contribution_to_93flower_mse_gain"],
        "other7_gain_existing_predictions":score["other7_dates_original_prediction_mse_gain_without_refit"],
        "new_model_fit":False,
    },indent=2))


if __name__=="__main__":
    main()
