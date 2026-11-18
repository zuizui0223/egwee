#!/usr/bin/env python3
"""Post-outcome five-fold aggregate influence check, NO REFITTING.

Only reads GitHub Actions derivative *aggregate* JSON. Cannot read original
source rows, site IDs, pollen, fruit or environmental values.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

EXPECTED=0.08516306718909472

def summarize(result):
    assert result["status"]=="PF_SOURCE_ONE_STUDY_REGION_HOLDOUT_COMPLETE"
    folds=result["heldout_region_folds_anonymized"]
    assert len(folds)==5 and sum(int(x["n_original_orchards"]) for x in folds)==18
    n=sum(int(f["n_original_orchards"]) for f in folds)
    total=sum(f["n_original_orchards"]*f["M0_minus_M1"] for f in folds)
    primary=total/n
    if abs(primary-EXPECTED)>1e-10:
        raise ValueError("Frozen original P-F score drift")
    weighted=[]
    equal=[]
    for ix,f in enumerate(folds,1):
        x=(total-f["n_original_orchards"]*f["M0_minus_M1"])/(n-f["n_original_orchards"])
        y=sum(z["M0_minus_M1"] for i,z in enumerate(folds,1) if i!=ix)/(len(folds)-1)
        weighted.append(x)
        equal.append(y)
    return {
      "status":"POST_OUTCOME_AGGREGATE_ONLY_INFLUENCE_AUDIT",
      "source_model_and_folds_refit":False,
      "orig_frozen_primary_orchard_equal_gain":primary,
      "leave_one_scoring_region_aggregate_only_orchard_weighted_range":[min(weighted),max(weighted)],
      "leave_one_scoring_region_aggregate_only_region_equal_range":[min(equal),max(equal)],
      "n_of_five_deletions_reversing_positive_orchard_weighted_gain":sum(x<=0 for x in weighted),
      "n_of_five_deletions_reversing_positive_region_equal_gain":sum(x<=0 for x in equal),
      "posthoc_exploratory_not_preregistered":True,
      "independent_ecological_studies_added":0,
      "original_source_rows_redistributed":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    x=summarize(json.loads(args.source.read_text(encoding="utf-8")))
    args.output.write_text(json.dumps(x,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("AA001_POST_OUTCOME_INFLUENCE "+json.dumps(x,sort_keys=True))

if __name__=="__main__":
    main()
