#!/usr/bin/env python3
"""Protocol-locked Arnica 2020 maternal HL -> seed-function association.

Plan committed BEFORE outcomes: ARNICA_HL_SEED_PILOT_FROZEN_20261115.md
plan commit d5eb3b49ef5fb4ca58c9cafd90499681944b3a68.
One source programme; observational within Site x source rank association;
not genetic-rescue causal evidence, not a pooled meta effect.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import random
from audit_dianthus_genome_fitness_ids import source_file, read_whitelisted
from audit_zenodo_genetic_fitness_schema import workbook_sheets

SOURCE_SHA256 = "052fef893ed6bb3dd00fec4882c77b6f4f48ed85767fa2643a4809505d4e8e62"
PROTOCOL_COMMIT = "d5eb3b49ef5fb4ca58c9cafd90499681944b3a68"
FIELDS = {"Code","Site","source","HL mat plant"," Viable seed set","Seed germination"}
NA = {"", "na", "n/a", "nan", "none", "null", "unknown", ".", "-", "missing"}
PERMUTATIONS=10000
SEED=20261115
MIN_STRATUM=5
MIN_TOTAL=30


class GateStop(RuntimeError):
    pass


def number(value, nonnegative=False):
    v=str(value or "").strip().lower()
    if v in NA:
        return None
    try: val=float(v)
    except (ValueError,TypeError):
        return None
    if not math.isfinite(val):
        return None
    if nonnegative and val<0:
        raise GateStop("negative primary endpoint outside prespecified range")
    return val


def ranks(values):
    out=[0.0]*len(values)
    order=sorted(range(len(values)),key=lambda i:values[i])
    i=0
    while i<len(values):
        j=i+1
        while j<len(values) and values[order[j]]==values[order[i]]:
            j+=1
        mid=(i+1+j)/2.0  # 1-based average ranks
        for k in range(i,j):out[order[k]]=mid
        i=j
    return out


def corr(x,y):
    if not x or len(x)!=len(y):return None
    a=sum(x)/len(x)
    b=sum(y)/len(y)
    dx=[i-a for i in x]
    dy=[v-b for v in y]
    vx=sum(v*v for v in dx)
    vy=sum(v*v for v in dy)
    if vx<=0 or vy<=0:return None
    return sum(i*j for i,j in zip(dx,dy))/math.sqrt(vx*vy)


def grouped_rank_data(entries):
    blocks=defaultdict(list)
    for r in entries:
        blocks[(r["Site"],r["source"])].append(r)
    kept={k:v for k,v in blocks.items() if len(v)>=MIN_STRATUM}
    excluded={k:len(v) for k,v in blocks.items() if len(v)<MIN_STRATUM}
    if len(kept)<2 or sum(len(v) for v in kept.values())<MIN_TOTAL:
        raise GateStop("Too few independent maternal records/strata under frozen rule")
    centred=[]
    for key,record in sorted(kept.items()):
        gx=ranks([r["HL"] for r in record])
        gy=ranks([r["F"] for r in record])
        ax=sum(gx)/len(gx)
        ay=sum(gy)/len(gy)
        centred.append((key,[v-ax for v in gx],[v-ay for v in gy],len(record)))
    return centred,excluded


def pooled(blocks):
    x=[v for _,gx,gy,n in blocks for v in gx]
    y=[v for _,gx,gy,n in blocks for v in gy]
    return corr(x,y)


def calculate(records, outcome, prefix):
    entries=[]
    missing_genetic=0
    missing_outcome=0
    for r in records:
        g=number(r.get("HL mat plant"))
        f=number(r.get(outcome),nonnegative=True)
        if g is None:missing_genetic+=1
        elif not 0<=g<=1:raise GateStop("HL outside [0,1] in "+prefix)
        if f is None:missing_outcome+=1
        if g is None or f is None:continue
        entries.append({"Site":r["Site"],"source":r["source"],"HL":g,"F":f})
    blocks,excluded=grouped_rank_data(entries)
    observed=pooled(blocks)
    if observed is None:raise GateStop("No within-stratum variation in genetic proxy or endpoint")
    rng=random.Random(SEED)
    extreme=0
    for _ in range(PERMUTATIONS):
        shuffled=[]
        for k,x,y,n in blocks:
            shuffled_y=y[:]
            rng.shuffle(shuffled_y)
            shuffled.append((k,x,shuffled_y,n))
        rr=pooled(shuffled)
        if rr is not None and abs(rr)>=abs(observed)-1e-12: extreme+=1
    leave_out={}
    for removed,_,_,_ in blocks:
        subset=[b for b in blocks if b[0]!=removed]
        leave_out["site_source_stratum_"+str(len(leave_out)+1)]=pooled(subset)
    stratum_estimates=[]
    for _,x,y,n in blocks:
        stratum_estimates.append({"n_mothers":n,"rho_spearman":corr(x,y)})
    return {
        "role":prefix,
        "observed_pooled_within_site_source_rank_r":observed,
        "two_sided_within_stratum_permutation_p":(1+extreme)/(PERMUTATIONS+1),
        "permutation_draws":PERMUTATIONS,
        "permutation_rng_seed":SEED,
        "complete_matched_maternal_rows_before_min_stratum":len(entries),
        "mothers_in_qualifying_site_source_strata":sum(n for k,x,y,n in blocks),
        "qualifying_site_source_strata":len(blocks),
        "excluded_small_strata_mother_count":sum(excluded.values()),
        "stratum_effects_anonymised":stratum_estimates,
        "leave_one_stratum_out_rank_r_anonymised":leave_out,
        "missing_HL_rows":missing_genetic,
        "missing_target_rows":missing_outcome,
        "effect_direction_opened_only_after_protocol":True,
        "causal_rescue_estimate":False,
        "independent_programme_count":1,
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    # Ensure frozen text exists; it is part of the scientific evidence lock.
    freeze=Path(__file__).resolve().parent/"ARNICA_HL_SEED_PILOT_FROZEN_20261115.md"
    txt=freeze.read_text(encoding="utf-8")
    if "v0.1" not in txt or "seed 20261115" not in txt or "Viable seed set" not in txt:
        raise GateStop("Preregistered estimand/seed/protocol text was changed")
    workbook=source_file(3881439,"VanRossumetal_Arnica_fitness.xlsx")
    digest=hashlib.sha256(workbook).hexdigest()
    if digest!=SOURCE_SHA256:
        raise GateStop("Published source hash does not match preregistered digest")
    sheets=workbook_sheets(workbook)
    first=sheets[0]
    if first["sheet"]!="xl/worksheets/sheet1.xml" or first["xml_nonempty_rows"]!=146:
        raise GateStop("Source worksheet grain changed")
    if not FIELDS<=set(first["first_row_header_fields"]):
        raise GateStop("Target source columns not found")

    rows=read_whitelisted(workbook,first["sheet"],FIELDS)
    if len(rows)!=145:raise GateStop("Prespecified maternal denominator changed")
    valid=[r for r in rows if all(r.get(k) not in NA for k in ("Site","source","Code"))]
    invalid_ids=len(rows)-len(valid)
    motherkeys=Counter((r["Site"],r["source"],r["Code"]) for r in valid)
    duplicates=sum(n>1 for n in motherkeys.values())
    result={
        "status":"SOURCE_ELIGIBILITY_CHECKED",
        "article_doi":"10.1111/mec.15550",
        "dataset_doi":"10.5281/zenodo.3881439",
        "source_sha256":digest,
        "protocol":"research/rescue_coupling/ARNICA_HL_SEED_PILOT_FROZEN_20261115.md",
        "protocol_pre_outcome_commit":PROTOCOL_COMMIT,
        "maternal_source_rows":len(rows),
        "incomplete_maternal_identifier_rows":invalid_ids,
        "duplicated_complete_site_source_mother_keys":duplicates,
        "outcomes_not_inspected_for_protocol_changes":True,
        "no_plant_translocation_causal_contrast":True,
        "independent_meta_study_programmes":1
    }
    if duplicates:
        result["status"]="GRAIN_STOP_DUPLICATE_MOTHER_KEYS"
        result["decision"]="No signed associations computed; resolve duplicate maternal records"
    else:
        try:
            result["primary"]=calculate(valid," Viable seed set","primary_Arnica_maternal_HL_versus_viable_seed")
            result["secondary"]=calculate(valid,"Seed germination","secondary_Arnica_maternal_HL_versus_germination")
            result["status"]="EXPLORATORY_SINGLE_PROGRAMME_ASSOCIATION_COMPUTED_NOT_META"
            result["decision"]="Report only conditional maternal correlations; no causal genetic rescue or partner-service interpretation"
        except GateStop as e:
            result["status"]="SOURCE_QUALITY_OR_COVERAGE_STOP"
            result["decision"]=str(e)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"maternal_source_rows":result["maternal_source_rows"],
                      "decision":result["decision"],"primary":result.get("primary"),
                      "secondary":result.get("secondary")},indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
