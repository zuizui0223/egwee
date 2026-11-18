#!/usr/bin/env python3
"""QPF001: sharp bounded-error contrast for 29 unrecovered-fruit outcomes.

POSTHOC PARTIAL IDENTIFICATION, never a new confirmatory Q-P-F test.
Reuses immutable original eight-date M0/M1 design and original fitted
93-fruit training folds. Extends fixed heldout forecasts to 29 missing
outcomes, then analytically bounds the M0−M1 squared-error comparison
for hypothetical y in [0,1]. NO model refitting on unknown outcomes,
no missing-at-random, no raw original flower rows in output.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
from statistics import mean

from run_qpf001_original_flower_dateholdout import (
    DAYS, FREEZE_SHA, _binary_original, _xlsx_data,
    audit_source, numeric, predict, verify_protocol,
)

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / "QPF001_DATE_HOLDOUT_ORIGINAL_RESULT_20261118.json"
EXPECTED_N_MISSING_BY_DAY = {176:15,177:0,178:8,182:2,183:1,190:2,191:0,196:1}


def squared_error_delta_at_boundary(p0:float, p1:float, y:float) -> float:
    """Original M0 squared loss minus original M1 squared loss."""
    if not 0<=p0<=1 or not 0<=p1<=1 or y not in (0.0,1.0):
        raise ValueError("Only bounded predictions and 0/1 endpoint states permitted")
    return (p0-y)**2 - (p1-y)**2


def bounded_unknown_flower(p0:float, p1:float) -> tuple[float,float]:
    """Sharp endpoint extrema: delta(y) affine in unknown y in [0,1]."""
    a = squared_error_delta_at_boundary(p0,p1,0.0)
    b = squared_error_delta_at_boundary(p0,p1,1.0)
    return min(a,b),max(a,b)


def source_audit(source_zip:Path) -> dict:
    verify_protocol()
    old=json.loads(ORIGINAL.read_text(encoding="utf-8"))
    if (old["protocol_commit"]!=FREEZE_SHA or
        old["registered_decision"]!="NO_ROBUST_WITHIN_STUDY_DATE_TRANSFER_GAIN"):
        raise RuntimeError("Original preregistered QPF001 decision changed")
    flowers=_xlsx_data(_binary_original(source_zip))
    observed,receipt=audit_source(flowers)
    if len(flowers)!=122 or len(observed)!=93:
        raise RuntimeError("Original flower and seed-set ascertainment changed")

    grouped=[]
    n_missing=0
    sse_unknown_min=0.0
    sse_unknown_max=0.0
    count_p1_higher=0
    count_p1_lower=0
    sum_known=0.0

    for day in DAYS:
        training=[r for r in observed if int(r["Julian.day"])!=day]
        hold_observed=[r for r in observed if int(r["Julian.day"])==day]
        hold_unseen=[r for r in flowers
                     if int(r["Julian.day"])==day and
                     numeric(r["Seed.set"]) is None]
        if len(hold_unseen)!=EXPECTED_N_MISSING_BY_DAY[day]:
            raise RuntimeError("Original 29-fruit missingness by date drifted")

        original_fold=next(f for f in old["folds"] if f["day"]==day)
        if len(hold_observed)!=original_fold["n"]:
            raise RuntimeError("Original 8-fold recovered-fruit denominator drifted")
        po0=predict(training,hold_observed,False)
        po1=predict(training,hold_observed,True)
        per_day_known=0.0
        for name, forecast in (("M0",po0),("M1",po1)):
            err=[r["Seed.set"]-p for r,p in zip(hold_observed,forecast)]
            mse=mean(v*v for v in err)
            mae=mean(abs(v) for v in err)
            if (abs(mse-original_fold[name+"_mse"])>1e-10 or
                abs(mae-original_fold[name+"_mae"])>1e-10):
                raise RuntimeError("Original fixed model 8-fold predictions not reproduced")
        per_day_known=original_fold["n"]*(original_fold["M0_mse"]-original_fold["M1_mse"])
        sum_known+=per_day_known

        # EXTEND the fixed training-fold predictors to source flowers with
        # unknown fruit outcome. No hypothetical outcome is supplied to fit.
        if hold_unseen:
            pm0=predict(training,hold_unseen,False)
            pm1=predict(training,hold_unseen,True)
            lower=sum(bounded_unknown_flower(a,b)[0] for a,b in zip(pm0,pm1))
            upper=sum(bounded_unknown_flower(a,b)[1] for a,b in zip(pm0,pm1))
            count_p1_higher+=sum(b>a for a,b in zip(pm0,pm1))
            count_p1_lower+=sum(b<a for a,b in zip(pm0,pm1))
            mean0=mean(pm0)
            mean1=mean(pm1)
        else:
            lower=upper=0.0
            mean0=mean1=None
        n_missing+=len(hold_unseen)
        sse_unknown_min+=lower
        sse_unknown_max+=upper
        grouped.append({
            "julian_day":day,
            "n_missing_seedset":len(hold_unseen),
            "mean_frozen_M0_missing_flower_prediction":mean0,
            "mean_frozen_M1_missing_flower_prediction":mean1,
            "min_possible_missing_outcome_error_gain_sse":lower,
            "max_possible_missing_outcome_error_gain_sse":upper,
            "no_individual_source_forecasts_released":True,
        })

    if n_missing!=29 or sum(g["n_missing_seedset"] for g in grouped)!=29:
        raise RuntimeError("Unrecovered-fruit denominator not 29")
    original_known=old["pooled"]["M0_minus_M1_mse"]*93
    if abs(sum_known-original_known)>1e-10:
        raise RuntimeError("Frozen pooled 93-fruit MSE gain not reproducible")
    low=(sum_known+sse_unknown_min)/122
    high=(sum_known+sse_unknown_max)/122
    if not low<=high:
        raise RuntimeError("Bounds not ordered")
    return {
        "analysis_id":"QPF001_missing29_original_fixed_forecast_error_bounds",
        "status":"POSTHOC_SHARP_BOUNDS_CONDITIONAL_ON_HYPOTHETICAL_SEEDSET",
        "original_scientific_decision":old["registered_decision"],
        "original_protocol_commit":old["protocol_commit"],
        "original_source_doi":"10.5061/dryad.hqbzkh1g9",
        "original_source_zip_sha256":old["original_zip_sha256"],
        "original_source_xlsx_sha256":old["original_xlsx_sha256"],
        "observed_recovered_fruit_n":93,
        "unrecovered_fruit_unknown_n":29,
        "filmed_all_flower_n":122,
        "source_genuine_stigma_pollen_and_visits_observed_n":122,
        "original_observed93_mse_gain_M0_minus_M1":old["pooled"]["M0_minus_M1_mse"],
        "original_observed93_summed_squared_loss_gain":sum_known,
        "unrecovered29_summed_loss_gain_lower":sse_unknown_min,
        "unrecovered29_summed_loss_gain_upper":sse_unknown_max,
        "hypothetical_all122_M0_minus_M1_mse_gain_lower":low,
        "hypothetical_all122_M0_minus_M1_mse_gain_upper":high,
        "unknown29_M1_prediction_higher_count":count_p1_higher,
        "unknown29_M1_prediction_lower_count":count_p1_lower,
        "date_level_aggregates":grouped,
        "math":"For missing i, delta_i(y)=(p0_i-y)^2-(p1_i-y)^2=p0_i^2-p1_i^2+2*y*(p1_i-p0_i). This is affine in unknown y in [0,1], so exact unconstrained extrema are attained at y=0 or y=1 independently for each missing flower.",
        "condition_on_potential_outcome":"An original comparable source Seed.set in [0,1] would need to exist for every unrecovered or herbivorized fruit. This cannot be established from the data, and the mathematical interval is NOT an observed all-population fecundity effect.",
        "scope":[
            "Same originally registered M0/M1, same date partitions, 93 observed training outcomes, unchanged ridge lambda and predictor definitions.",
            "Only fixed heldout predictions for missing outcomes are extended; the models are NOT retrained on hypothetical fruit data.",
            "Sharp only conditional on individual missing latent outcomes being unconstrained in [0,1]; if biologically undefined, this target is not identified even by the interval.",
            "No unobserved fruit Seed.set values are imputed. No missing at random or lost fruit equals reproductive failure assumption.",
            "Not a confidence interval, a p-value, a new preregistered hypothesis test or a positive ecological-function discovery.",
            "Original QPF001 8-day negative registered decision remains unchanged; site count remains one.",
        ],
        "individual_flower_values_exported":False,
        "third_party_original_workbook_exported":False,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-zip",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    out=source_audit(a.source_zip)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "result_status":out["status"],
        "n_observed":out["observed_recovered_fruit_n"],
        "n_unknown":out["unrecovered_fruit_unknown_n"],
        "original_decision":out["original_scientific_decision"],
        "all122_fixed_forecast_gain_interval":[
            out["hypothetical_all122_M0_minus_M1_mse_gain_lower"],
            out["hypothetical_all122_M0_minus_M1_mse_gain_upper"]
        ],
    },indent=2))


if __name__=="__main__":
    main()
