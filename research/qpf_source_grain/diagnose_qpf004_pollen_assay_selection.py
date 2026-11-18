#!/usr/bin/env python3
"""QPF004 original-ramet pollen-assay coverage and outcome selection audit.

POSTHOC MEASUREMENT PROCESS DIAGNOSTIC ONLY. Reuses the exact four-file
original Dryad source and source-only identities of the frozen QPF004
2016 62-ramet primary. This code does not re-fit, select variables, impute
missing pollen, compute significance tests, or revise scientific decisions.
Raw plant IDs, seed counts, pollen grains and original XLSX/PDF never export.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
from statistics import mean

from run_qpf004_mertensia_source_weekholdout import (
    source_bytes, xlsx_sheet, verify_protocol, ZIP_SHA, FREEZE_SHA
)

HERE = Path(__file__).resolve().parent
OLD_RESULT = HERE / "QPF004_ORIGINAL_WEEK_HOLDOUT_RESULT_20261118.json"
SOURCE_FILE = "gallagher&campbell_pollinatorEffectivenessData.xlsx"
ARMS = ("V", "O", "B")
SITES = ("RG", "SP")


def key(value) -> str:
    if isinstance(value, (int,float)) and int(value) == value:
        return str(int(value))
    return str(value).strip()


def siteweek(source: list[dict], assayed_ids: set[str]) -> list[dict]:
    rows = []
    sites = sorted({r["site"] for r in source})
    groups = sorted({int(r["week"]) for r in source})
    for site in sites:
        for week in groups:
            g = [r for r in source
                 if r["site"] == site and int(r["week"]) == week]
            if not g:
                continue
            n = sum(key(r["plantID"]) in assayed_ids for r in g)
            rows.append({
                "site": site,
                "source_week": week,
                "source_seed_ramets": len(g),
                "pollen_measured_ramets": n,
                "pollen_unmeasured_ramets": len(g)-n,
                "fraction_assayed": n/len(g),
            })
    return rows


def aggregate(rows: list[dict]) -> dict:
    if not rows:
        return {"n":0,"mean_seed_per_flower":None,"zero_seed_fraction":None,
                "mean_marked_flowers":None}
    if any(r["seedPerFlr"] is None or r["seedCnt"] is None or
           r["noFlrs"] is None for r in rows):
        raise ValueError("Original seed output/flower denominator missing")
    return {
        "n": len(rows),
        "mean_seed_per_flower": mean(float(r["seedPerFlr"]) for r in rows),
        "zero_seed_fraction": mean(float(r["seedCnt"] == 0) for r in rows),
        "mean_marked_flowers": mean(float(r["noFlrs"]) for r in rows),
    }


def audit_source(source_zip: Path) -> dict:
    verify_protocol()
    old = json.loads(OLD_RESULT.read_text(encoding="utf-8"))
    if (old["preoutcome_protocol_commit"] != FREEZE_SHA or
        old["registered_decision"] != "NO_PRACTICALLY_PORTABLE_POLLEN_INCREMENT" or
        old["source_structure"]["source_2016_P_and_F_joined"] != 62):
        raise RuntimeError("Original source or frozen primary conclusion was revised")

    original = source_bytes(source_zip)  # ALL 4 original file SHA/size/CRC verified
    source = xlsx_sheet(original[SOURCE_FILE], 1)
    pollen = xlsx_sheet(original[SOURCE_FILE], 2)
    if len(source) != 232 or len(pollen) != 62:
        raise RuntimeError("Original 232/62 source unit roster shifted")
    ids = {key(r["plantID"]) for r in source}
    assayed = {key(r["plantID"]) for r in pollen}
    if len(ids) != 232 or len(assayed) != 62 or not assayed.issubset(ids):
        raise RuntimeError("Source maternal/ramet ID coverage changed")
    counts=Counter(r["treat"] for r in source)
    if counts!=Counter({"V":94,"O":65,"B":73}):
        raise RuntimeError("Original source three treatment groups changed")
    if Counter(r["treat"] for r in source if key(r["plantID"]) in assayed) != Counter({"V":47,"O":15}):
        raise RuntimeError("Original pollen-assayed arm roster changed")

    groups=[]
    for label in ("ALL",) + ARMS:
        source_rows = source if label=="ALL" else [r for r in source if r["treat"] == label]
        yes = [r for r in source_rows if key(r["plantID"]) in assayed]
        no = [r for r in source_rows if key(r["plantID"]) not in assayed]
        row = {
            "treatment":label,
            "source_n":len(source_rows),
            "pollen_assay_n":len(yes),
            "no_pollen_assay_n":len(no),
            "assay_fraction":len(yes)/len(source_rows),
            "source_P_assayed":aggregate(yes),
            "source_P_not_assayed":aggregate(no),
        }
        groups.append(row)
    bydate=siteweek(source,assayed)
    if [(r["site"],r["source_week"],r["source_seed_ramets"],
         r["pollen_measured_ramets"]) for r in bydate] != [
         ("RG",1,23,4), ("RG",2,58,18), ("RG",3,41,16),
         ("SP",3,13,0), ("SP",4,61,20), ("SP",5,36,4)
    ]:
        raise RuntimeError("Original site×week source support differs from audit")
    if sum(x["pollen_measured_ramets"] for x in bydate)!=62:
        raise RuntimeError("Pollen outcome coverage no longer complete")
    matched_source=aggregate([r for r in source if key(r["plantID"]) in assayed])
    nonmatched_source=aggregate([r for r in source if key(r["plantID"]) not in assayed])
    if abs(matched_source["mean_seed_per_flower"]-.7182027649769586)>1e-12:
        raise RuntimeError("P pollen subset seed mean differs from original source")
    if abs(nonmatched_source["mean_seed_per_flower"]-.34067452936378767)>1e-12:
        raise RuntimeError("Unassayed pollen subset seed mean differs from original source")
    return {
      "audit_id":"QPF004_posthoc_2016_pollen_assay_coverage",
      "classification":"POSTHOC_ASSAY_SELECTION_AND_SOURCE_SUPPORT_NOT_NEW_ECOLOGICAL_TEST",
      "source_doi":"10.7280/D19X0D",
      "source_archive_sha256":ZIP_SHA,
      "original_primary_protocol_commit":FREEZE_SHA,
      "original_primary_decision":old["registered_decision"],
      "original_2016_primary_pooled_MSE":{
          "M0":old["primary_2016_week"]["pooled"]["M0_MSE"],
          "M1":old["primary_2016_week"]["pooled"]["M1_MSE"],
          "positive_weeks":old["primary_2016_week"]["pooled"]["positive_folds"],
      },
      "source_all_2016_seed_per_flower_ramets":232,
      "source_ramets_with_measured_stigma_P":62,
      "source_ramets_without_stigma_P":170,
      "source_treatment_coverage_and_F_descriptives":groups,
      "site_by_week_pollen_coverage":bydate,
      "source_support_closure":{
          "site_week_confounding_created_by_pollen_selection":
             "Original seed source includes SP week 3 (13 ramets), while all 13 have missing P. P-complete sample has RG weeks 1–3 only and SP weeks 4–5 only.",
          "no_bagged_control_assayed_P":True,
          "P_missingness_not_randomly_distributed_across_treatments":True,
          "P_and_seed_same_flower_verified":False,
          "clone_triplet_independence_verified":False,
      },
      "interpretation_ceiling":[
          "Source P-assay eligibility differs by original randomized treatment; comparing raw P-observed/unobserved pooled seed means conflates treatment composition and source group.",
          "Within V treatment, source mean seeds/flower in P-measured vs non-assayed is lower, opposite to the all-arms marginal comparison; no causal 'sampling lowered seeds' inference.",
          "Zero measured P on bagged ramets is absence of measurement, not biological zero.",
          "Site×week full support is not preserved after restricting to P-complete 62; no independent site-versus-week causal separation.",
          "No new source pollen/seed regression, alternative fitted QPF model, selective result rescue, conventional p value, or independent-study effect computed.",
          "The original registered QPF004 nonportable pollen predictive decision remains unchanged.",
      ],
      "original_individual_flower_ramet_values_exported":False,
      "third_party_original_source_uploaded":False,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-zip",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    out=audit_source(a.source_zip)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "classification":out["classification"],
        "original_decision":out["original_primary_decision"],
        "all_source_ramets":out["source_all_2016_seed_per_flower_ramets"],
        "assayed_stigma_pollen_ramets":out["source_ramets_with_measured_stigma_P"],
        "experimental_arm_sample_sizes":[{
            "treatment":x["treatment"],"n":x["source_n"],"P_n":x["pollen_assay_n"]
        } for x in out["source_treatment_coverage_and_F_descriptives"]],
        "new_model_fitted":False
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
