#!/usr/bin/env python3
"""AA001 2026 orchard original biological unit / join coverage only.

Outcome-blind: inspect source-key/treatment labels, numeric *eligibility* flags
but never signed visitor/pollen/fruit measurements for inference or outputs.
Styles were excised: same-site P/F is NOT same-flower P/F.
"""
from __future__ import annotations
import argparse
import csv
from collections import Counter, defaultdict
import hashlib
import io
import json
import math
from pathlib import Path

from audit_AA001_zenodo_source_schema import source_metadata,get_bytes

EXPECTED={
 "TransectIN.txt":("9cf85041de39adbb50c881bd3236c7368eeb23f0a20c22e13b2b4c28d8851a09",390),
 "GerminatedPollen.txt":("69c12fd6744dcf5066c7ca08ddfc970f03565faf089721068a05a980d7897312",1061),
 "initial_final_fruitset.txt":("2898dbeab9492d11b6a886373e82ce385d3e16a51c8163c402f8a30adad37ec0",816),
 "apple_weight.txt":("fdfc5b9923dc7047b62ca009875c5d068475cad3381e4baa7c6550d831618942",796),
}
CONTRACT={
 "TransectIN.txt":("Count","Visitors","Temp","Local_temp","Year","Region","Site"),
 "GerminatedPollen.txt":("Nbr_germinated_pollen","Treatment","Temp","Region","Site","Plot","Inflo_ID"),
 "initial_final_fruitset.txt":("Initial_nb_fruit","Nb_Failure_Initial","Final_nb_fruit","Nb_Failure_Final","Treatment","Temp","Year","Region","Site","Plot"),
 "apple_weight.txt":("Weight","Treatment","Temp","Year","Region","Site","Plot","Inflo_ID"),
}
ALLOWED_TREATMENTS={"e","o","oh"}
NA={"","na","nan","none","null","missing","unknown"}

def norm(s):
    return " ".join(str(s or "").strip().casefold().split())

def has(s):
    return norm(s) not in NA

def numeric_nonneg(s):
    if not has(s):return False
    try:
        v=float(s)
        return math.isfinite(v) and v>=0
    except (ValueError,TypeError):return False

def numeric_valid_year(s):
    if not has(s):return None
    try:
        v=float(s)
        if math.isfinite(v) and v==int(v) and 1900<=v<=2100:
            return str(int(v))
    except (ValueError,TypeError):pass
    return None

def rows_from_author_record():
    meta,entries=source_metadata()
    records={}
    for name,(sha,n_expected) in EXPECTED.items():
        entry=entries[name]
        href=(entry.get("links") or {}).get("content") or (entry.get("links") or {}).get("self")
        if not href:
            raise ValueError("no source-advertised raw file link")
        raw=get_bytes(href,512_000)
        if hashlib.sha256(raw).hexdigest()!=sha:
            raise ValueError("original hard-frozen SHA256 drift for "+name)
        reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""),delimiter="\t")
        if tuple(reader.fieldnames or [])!=CONTRACT[name]:
            raise ValueError("original source column header drift for "+name)
        rows=list(reader)
        if len(rows)!=n_expected:
            raise ValueError("original source row count drift for "+name)
        records[name]=rows
    return records

def audit():
    r=rows_from_author_record()
    Q=r["TransectIN.txt"]
    P=r["GerminatedPollen.txt"]
    F=r["initial_final_fruitset.txt"]
    W=r["apple_weight.txt"]
    cov=Counter()
    q_2023=set()
    q_years=Counter()
    q_region=set()
    q_visitor_categories=set()
    for z in Q:
        yr=numeric_valid_year(z["Year"])
        if not yr:
            cov["q_year_missing"]+=1
            continue
        q_years[yr]+=1
        if not all(has(z[k]) for k in ("Region","Site")):
            cov["q_site_missing"]+=1
            continue
        key=(norm(z["Region"]),norm(z["Site"]))
        q_region.add(key[0])
        if has(z["Visitors"]):q_visitor_categories.add(norm(z["Visitors"]))
        if yr=="2023" and numeric_nonneg(z["Count"]):
            q_2023.add(key)
            cov["q_2023_valid_group_observation_rows"]+=1
        elif yr=="2023":
            cov["q_2023_missing_or_invalid_count"]+=1

    p_keys=defaultdict(set)
    f_keys=defaultdict(set)
    w_keys=defaultdict(set)
    p_orch=set()
    f_orch=set()
    w_orch=set()
    code_p=Counter()
    code_f=Counter()
    code_w=Counter()
    p_inflo_unique=set()
    p_inflo_duplicates=0
    for z in P:
        if not all(has(z[k]) for k in ("Region","Site","Plot")):
            cov["p_key_incomplete"]+=1
            continue
        treatment=norm(z["Treatment"])
        code_p[treatment]+=1
        if treatment not in ALLOWED_TREATMENTS:
            cov["p_unrecognized_treatment"]+=1
            continue
        if not numeric_nonneg(z["Nbr_germinated_pollen"]):
            cov["p_invalid_pollen_measure"]+=1
            continue
        key=(norm(z["Region"]),norm(z["Site"]),norm(z["Plot"]),treatment)
        orchard=key[:2]
        p_keys[treatment].add(key)
        p_orch.add(orchard)
        if has(z["Inflo_ID"]):
            infkey=key+(norm(z["Inflo_ID"]),)
            if infkey in p_inflo_unique:p_inflo_duplicates+=1
            p_inflo_unique.add(infkey)
    for z in F:
        if not all(has(z[k]) for k in ("Region","Site","Plot")):
            cov["f_key_incomplete"]+=1
            continue
        year=numeric_valid_year(z["Year"])
        treatment=norm(z["Treatment"])
        code_f[treatment]+=1
        if year!="2023":continue
        if treatment not in ALLOWED_TREATMENTS:
            cov["f_2023_unrecognized_treatment"]+=1
            continue
        if not all(numeric_nonneg(z[k]) for k in ("Final_nb_fruit","Nb_Failure_Final")):
            cov["f_2023_invalid_final_fraction_components"]+=1
            continue
        successes=float(z["Final_nb_fruit"])
        failed=float(z["Nb_Failure_Final"])
        if successes+failed<=0:
            cov["f_2023_zero_final_denominator"]+=1
            continue
        key=(norm(z["Region"]),norm(z["Site"]),norm(z["Plot"]),treatment)
        f_keys[treatment].add(key)
        f_orch.add(key[:2])
    weight_years=Counter()
    for z in W:
        yr=numeric_valid_year(z["Year"])
        if yr:weight_years[yr]+=1
        if yr!="2023" or not all(has(z[k]) for k in ("Region","Site","Plot")):
            continue
        treatment=norm(z["Treatment"])
        code_w[treatment]+=1
        if treatment not in ALLOWED_TREATMENTS or not numeric_nonneg(z["Weight"]):
            continue
        key=(norm(z["Region"]),norm(z["Site"]),norm(z["Plot"]),treatment)
        w_keys[treatment].add(key)
        w_orch.add(key[:2])

    p_o=p_keys["o"]
    f_o=f_keys["o"]
    plot_o=p_o & f_o
    orch_o_p={x[:2] for x in p_o}
    orch_o_f={x[:2] for x in f_o}
    qpf_orchard=q_2023 & orch_o_p & orch_o_f
    plot_qpf={x for x in plot_o if x[:2] in q_2023}
    region_qpf={x[0] for x in qpf_orchard}
    treatment_plot_overlap={}
    for label in ("e","o","oh"):
        treatment_plot_overlap[label]=len(p_keys[label]&f_keys[label])
    pass_threshold=(len(qpf_orchard)>=12 and len(region_qpf)>=3 and len(plot_qpf)>=20)

    return {
      "status":"AA001_SOURCE_ORCHARD_GRAIN_VERIFIED",
      "source_zenodo_record_id":19403906,
      "source_sha256":{k:v[0] for k,v in EXPECTED.items()},
      "original_row_counts":{k:v[1] for k,v in EXPECTED.items()},
      "q_year_category_row_counts":dict(q_years),
      "fruit_weight_year_category_row_counts":dict(weight_years),
      "n_q_original_regions":len(q_region),
      "n_q_original_visitor_categories":len(q_visitor_categories),
      "n_q_valid_2023_orchards":len(q_2023),
      "n_p_valid_2023_orchards":len(p_orch),
      "n_f_valid_2023_orchards":len(f_orch),
      "n_w_valid_2023_orchards":len(w_orch),
      "original_source_treatment_labels_p":dict(code_p),
      "original_source_treatment_labels_f":dict(code_f),
      "original_source_treatment_labels_w_2023":dict(code_w),
      "source_key_missingness_and_denominator_invalidity":dict(cov),
      "p_with_inflo_label_n_unique":len(p_inflo_unique),
      "p_with_inflo_label_n_duplicate_rows":p_inflo_duplicates,
      "n_qpf_same_orchard_2023_open_context":len(qpf_orchard),
      "n_qpf_distinct_original_regions":len(region_qpf),
      "n_p_and_f_same_orchard_plot_2023_open_treatment_with_q_2023_site":len(plot_qpf),
      "source_plot_treatment_overlap_p_f_2023_by_label":treatment_plot_overlap,
      "new_site_context_coverage_gate_passed":pass_threshold,
      "decision":("MAY_FREEZE_DISTINCT_ORCHARD_CONTEXT_PREDICTIVE_TEST" if pass_threshold
                  else "SOURCE_COHORT_COVERAGE_STOP"),
      "pollen_and_fruit_from_same_sampled_flower":False,
      "q_measured_on_treatment_inflorescence":False,
      "third_same_flower_qpf_programme_admitted":False,
      "original_biological_outcomes_used_for_model":False,
      "source_rows_or_site_ids_redistributed":False,
    }

def self_test():
    assert norm(" R2  Site  1 ")=="r2 site 1"
    assert numeric_valid_year("2023.0")=="2023"
    assert numeric_valid_year("NA") is None
    assert numeric_nonneg("0") and not numeric_nonneg("-1")
    assert ("r","s","p","o")[:2]==("r","s")
    print("AA001_SOURCE_GRAIN_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:self_test();return 0
    if a.output is None:p.error("--output required")
    try:
        result=audit()
    except Exception as exc:
        result={"status":"SOURCE_OR_KEY_STOP","error_type":type(exc).__name__,
                "safe_reason":str(exc)[:280],
                "original_biological_outcomes_used_for_model":False,
                "source_rows_or_site_ids_redistributed":False,
                "third_same_flower_qpf_programme_admitted":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("AA001_ORIGINAL_COHORT_COVERAGE "+json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["status"]=="AA001_SOURCE_ORCHARD_GRAIN_VERIFIED" else 1

if __name__=="__main__":
    raise SystemExit(main())
