#!/usr/bin/env python3
"""Post-outcome source predictor consistency audit on unchanged 591-field frame.

No reselection/refitting and no signed yield values inspected here.
"""
from __future__ import annotations
from collections import Counter
import argparse
import json
import math
from pathlib import Path

from audit_source_field_grain import read_rows,num,norm
import test_frozen_qf_guild_increment as q

ALL_GUILDS=("visit_honeybee","visit_bombus","visit_wildbees",
            "visit_syrphids","visit_humbleflies","visit_other_flies",
            "visit_beetles","visit_lepidoptera",
            "visit_nonbee_hymenoptera","visit_others")

def run():
    selected=q.select_frozen_rows()
    selectkeys={r["site_key"] for panel in selected.values() for r in panel}
    rows=read_rows("field")
    audit=Counter()
    ratios=[]
    for row in rows:
        k=(norm(row["study_id"]),norm(row["site_id"]),norm(row["sampling_year"]),norm(row["crop"]))
        if k not in selectkeys:continue
        audit["source_frozen_selected_fields"]+=1
        total=num(row["visitation_rate"])
        selected_bee_fly=sum(num(row[g]) for g in ("visit_bombus","visit_wildbees","visit_syrphids"))
        if total is None:
            raise ValueError("Source drift: selected row has no total")
        if selected_bee_fly > total+max(.000001,.01*total):
            audit["three_guild_subtotal_exceeds_total_1pct"]+=1
        vals=[num(row[g]) for g in ALL_GUILDS]
        if any(z is None for z in vals):
            audit["full_ten_guild_sum_not_identifiable_due_missing"]=audit["full_ten_guild_sum_not_identifiable_due_missing"]+1
            continue
        full=sum(vals)
        audit["full_ten_guild_sum_evaluable"]+=1
        if abs(full-total)>max(.000001,.01*max(total,1)):
            audit["full_ten_guild_sum_differs_gt_1pct_or_1unit"]+=1
        if total>0:
            ratios.append(full/total)
    if audit["source_frozen_selected_fields"]!=591:
        raise ValueError("Source frozen field count mismatch")
    return {
        "status":"POSTPRIMARY_SOURCE_PREDICTOR_CONSISTENCY_AUDIT_COMPLETE",
        "source_original_author_commit":q.SOURCE_COMMIT,
        "source_original_selected_fields":591,
        "source_guild_sum_labels":list(ALL_GUILDS),
        "aggregate_quality_counts":dict(audit),
        "full_guild_sum_ratio_min":min(ratios) if ratios else None,
        "full_guild_sum_ratio_max":max(ratios) if ratios else None,
        "original_primary_models_refit":False,
        "crop_yield_outcomes_examined":False,
        "source_raw_rows_redistributed":False,
        "post_primary_exploratory":True,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:r=run()
    except Exception as exc:r={"status":"SOURCE_CONSISTENCY_STOP",
                               "reason":type(exc).__name__+": "+str(exc)[:300]}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print("CROPPOL_PREDICTOR_CONSISTENCY "+json.dumps(r,sort_keys=True),flush=True)
    return 0 if r["status"]=="POSTPRIMARY_SOURCE_PREDICTOR_CONSISTENCY_AUDIT_COMPLETE" else 1

if __name__=="__main__":
    raise SystemExit(main())
