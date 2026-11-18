#!/usr/bin/env python3
"""QPF007 POSTCOVERAGE exploratory prediction using all 145 source-valid plants.

The original QPF007 confirmation STOP remains untouched; one of 16 study
sessions has <6 complete plants, so the original preregistered 16-session
success gate was NOT met. This is an EXPLORATORY model using exactly the same
predictors, standardization, lambdas, folds and original source, permitting
that one small session for a sensitivity diagnosis only. No p-values, no
new confirmatory positive status, no dropping or merging sessions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from statistics import mean

from audit_brassica_rapa_zenodo_source_keys import load_manifest, trusted_binary
from run_qpf007_brassica_2026_session_holdout import (
    PLANT_SOURCE_FILE,POLLEN_SOURCE_FILE,PLANT_SOURCE_SHA,
    full_source_rows, original_stigma_keys, materialize_eligibility,
    ridge_predict, verify_frozen_science
)

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
POSTSTOP_REL="research/qpf_independent_2026/QPF007_FROZEN_POSTCOVERAGE_EXPLORATORY_20261118.json"
POSTSTOP_PATH=ROOT/POSTSTOP_REL
POSTSTOP_COMMIT="0933180d563150885968ee4d2eceb3f8fbb0245b"


def verify_poststop_provenance():
    verify_frozen_science()
    historic=subprocess.check_output(
        ["git","show",POSTSTOP_COMMIT+":"+POSTSTOP_REL],cwd=ROOT
    )
    if historic!=POSTSTOP_PATH.read_bytes():
        raise RuntimeError("Original QPF007 post-coverage exploratory rule changed")
    subprocess.run(["git","merge-base","--is-ancestor",POSTSTOP_COMMIT,"HEAD"],
                   cwd=ROOT,check=True)
    p=json.loads(historic)
    if p["experiment_id"]!="QPF007_Brassica_rapa_postcoverage_full145_session_exploratory_v1":
        raise RuntimeError("Wrong post-stop independent trial source protocol")
    return p


def analyze():
    rule=verify_poststop_provenance()
    meta=load_manifest()
    filemap={f.get("key") or f.get("filename"):f for f in meta["files"]}
    if PLANT_SOURCE_FILE not in filemap:
        raise RuntimeError("Published original 2026 plant data file missing")
    raw=trusted_binary(filemap[PLANT_SOURCE_FILE])
    if hashlib.sha256(raw).hexdigest()!=PLANT_SOURCE_SHA:
        raise RuntimeError("Original plant source SHA was not matched")
    stigma_keys=original_stigma_keys(meta)
    original=full_source_rows(raw)
    keys={(r["session"],r["ID_full"]) for r in original}
    if len(keys)!=160 or keys!=stigma_keys:
        raise RuntimeError("Original 160 source plant-stigma IDs no longer exactly match")
    # Demonstrate original strict first-stage source gate still FAILS.
    none, prior=materialize_eligibility(original,160,strict_coverage=True)
    if none is not None or prior.get("status")!="COVERAGE_STOP_NO_ORIGINAL_SOURCE_PREDICTIVE_TEST":
        raise RuntimeError("Original confirmation did not retain preregistered coverage STOP")
    admitted,coverage=materialize_eligibility(original,160,strict_coverage=False)
    if admitted is None or coverage["status"]!="EXPLORATORY_POSTCOVERAGE_SOURCE_145_WITH_ONE_SMALL_SESSION":
        raise RuntimeError("Postcoverage source conditions no longer match frozen 145 source plants")
    if (len(admitted)!=145 or coverage["source_excluded_rows"]!=15 or
        coverage["n_original_session_groups_with_eligible_mothers"]!=16 or
        coverage["n_source_sessions_below_six_complete_plant_units"]!=1):
        raise RuntimeError("145 complete plants / one small session source-gate discrepancy")
    groups=sorted({r["session"] for r in admitted})
    if len(groups)!=16:
        raise ValueError("Wrong original experimental session count")
    folds=[]
    maximum_numerical_difference=0
    for k,session in enumerate(groups,1):
        training=[r for r in admitted if r["session"]!=session]
        heldout=[r for r in admitted if r["session"]==session]
        if not 2<=len(heldout)<=10:
            raise RuntimeError("Unexpected source group size for original postcoverage trial")
        fold={"session_fold_index":k,"n_maternal_source_plants":len(heldout)}
        for model in ("M0","M1"):
            p_gauss=ridge_predict(training,heldout,model,"gaussian")
            p_cd=ridge_predict(training,heldout,model,"coordinate")
            dif=max(abs(a-b) for a,b in zip(p_gauss,p_cd))
            maximum_numerical_difference=max(maximum_numerical_difference,dif)
            if dif>1e-8:
                raise RuntimeError("Independently fitted ridge models disagree")
            errors=[y-r["y"] for r,y in zip(heldout,p_gauss)]
            fold[model+"_MSE"]=mean(v*v for v in errors)
            fold[model+"_MAE"]=mean(abs(v) for v in errors)
        fold["delta_M0_minus_M1_MSE"]=fold["M0_MSE"]-fold["M1_MSE"]
        folds.append(fold)
    if sum(f["n_maternal_source_plants"] for f in folds)!=145:
        raise ValueError("Original plant denominator lost in CV")
    def average(metric):
        return sum(f["n_maternal_source_plants"]*f[metric] for f in folds)/145
    m0,m1=average("M0_MSE"),average("M1_MSE")
    gain=m0-m1
    wins=sum(f["delta_M0_minus_M1_MSE"]>0 for f in folds)
    return {
      "analysis_id":rule["experiment_id"],
      "status":"ORIGINAL_SOURCE_POSTCOVERAGE_EXPLORATORY_FOLD_SCORES_COMPUTED",
      "confirmation_source_gate_result":"COVERAGE_STOP_NO_ORIGINAL_SOURCE_PREDICTIVE_TEST",
      "confirmed_original_registered_predictive_result":False,
      "postcoverage_freeze_commit":POSTSTOP_COMMIT,
      "original_predictive_protocol_commit":rule["scientific_predecessor"]["original_confirmatory_lock_commit"],
      "source_original_Zenodo_doi":"10.5281/zenodo.21628183",
      "source_original_individual_sha256":PLANT_SOURCE_SHA,
      "source_all_plant_n":160,
      "source_stigma_pollen_plant_keys":160,
      "source_complete_mother_n":145,
      "source_excluded_plant_n":15,
      "source_exclusion_reason_counts":coverage["missing_required_field_counts"],
      "n_experimental_session_groups":16,
      "n_group_below_original_six_plant_minimum":1,
      "session_folds":folds,
      "pooled":{
          "eligible_plant_n":145,"n_sessions":16,
          "M0_MSE":m0,"M1_MSE":m1,
          "M0_MAE":average("M0_MAE"),
          "M1_MAE":average("M1_MAE"),
          "M0_minus_M1_MSE":gain,
          "relative_mse_gain_percent":100*gain/m0 if m0>0 else None,
          "number_of_positive_session_folds":wins,
      },
      "no_new_confirmatory_decision":"EXPLORATORY_POSTSTOP_DIAGNOSTIC_ONLY_NEVER_CONFIRMATORY",
      "preexisting_model_5percent_12of16_gate_passed_DESCRIPTIVE_ONLY":
          bool(m0>0 and gain/m0>=.05 and wins>=12),
      "independent_numeric_verification":{
          "method_one":"train-only standardized ridge normal equations / Gauss Jordan",
          "method_two":"separate coordinate descent of penalized least-squares loss",
          "max_absolute_heldout_prediction_discrepancy":maximum_numerical_difference,
          "all_16_folds_both_source_models_verified":True
      },
      "scope":[
          "One experimentally manipulated Brassica rapa original research programme, not 16 independent natural landscapes.",
          "Primary registered test did not run: one 16-session group had <6 complete source plants.",
          "This postcoverage observation model retains all 145 eligible plants and one underpowered source session, with prior model architecture unchanged.",
          "Result sign and raw MSE difference cannot restore the registered confirmatory decision, nor count as independent QPF natural fragmented landscape replication.",
          "Original published paper already studied pollinator abundance, mate contact and sexual selection.",
          "Seed count per sampled fruit is not compatible pollen gene flow, viable cohort recruitment or functional loss.",
          "Raw original plant/flower genetic data not redistributed."
      ],
      "original_source_plant_IDs_disclosed":False,
      "original_raw_phenotype_or_genotype_values_disclosed":False,
      "source_data_redistributed":False
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    out=analyze()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":out["status"],
        "pre_registered_confirmation":out["confirmation_source_gate_result"],
        "n_complete_source_plants":out["source_complete_mother_n"],
        "M0_MSE":out["pooled"]["M0_MSE"],
        "M1_MSE":out["pooled"]["M1_MSE"],
        "relative_gain_percent":out["pooled"]["relative_mse_gain_percent"],
        "n_positive_sessions":out["pooled"]["number_of_positive_session_folds"],
        "exploratory_not_confirmation":True,
    },indent=2))


if __name__=="__main__":
    main()
