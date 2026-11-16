#!/usr/bin/env python3
"""Preregistered population-grain Campanula seed-progeny HL vs rosette pilot.

The analytical protocol, independent unit, endpoint and exact null were frozen
in commit 52ff2c5b2212b6b8d91e802869fb963ebf4973ab BEFORE numerical outcomes
were opened. One programme only, no causal genetic rescue claim or F_direct endpoint.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import permutations
import argparse
import hashlib
import json
import math
from pathlib import Path
import random

from audit_dianthus_genome_fitness_ids import source_file, read_whitelisted

SOURCE_DATA_DOI="10.5281/zenodo.5676272"
SOURCE_PAPER_DOI="10.3389/fcosc.2022.829332"
SOURCE_SHA256="a1c50c74d0bd2c9a00b7a0d42322c31c30c53789e3b5cadbe67b08cee878f6a7"
PROTOCOL_COMMIT="52ff2c5b2212b6b8d91e802869fb963ebf4973ab"
FIELDS={"POP","Ind","HL","Rosette diameter (cm)"}
MISSING={"","na","n/a","null","nan","none","unknown","-",".","missing"}
MIN_POP_N=5
MIN_POPULATIONS=5
SEED=20261116
PERMUTATIONS=10000

class EligibilityStop(Exception):
    pass

def number(s, name, lower=None, upper=None):
    s=str(s or "").strip()
    if s.casefold() in MISSING: return None
    try: v=float(s)
    except (ValueError,TypeError): return None
    if not math.isfinite(v):return None
    if lower is not None and v < lower:raise EligibilityStop(name+" below prespecified lower bound")
    if upper is not None and v > upper:raise EligibilityStop(name+" above prespecified upper bound")
    return v

def avg_rank(vals):
    n=len(vals)
    idx=sorted(range(n),key=lambda i: vals[i])
    out=[0.0]*n
    i=0
    while i<n:
        j=i+1
        while j<n and vals[idx[i]]==vals[idx[j]]:j+=1
        r=(i+1+j)/2.0
        for k in range(i,j):out[idx[k]]=r
        i=j
    return out

def pearson(x,y):
    if len(x)<2 or len(x)!=len(y):return None
    ax=sum(x)/len(x)
    ay=sum(y)/len(y)
    dx=[v-ax for v in x]
    dy=[v-ay for v in y]
    vx=sum(v*v for v in dx)
    vy=sum(v*v for v in dy)
    if vx<=0 or vy<=0:return None
    return sum(a*b for a,b in zip(dx,dy))/math.sqrt(vx*vy)

def spearman(x,y):
    return pearson(avg_rank(x),avg_rank(y))

def exact_or_mc(xs,ys):
    if len(xs)<=8:
        # Under the exchangeability null, count unique assignments of endpoint
        # population ranks. Repeated ties are not separately counted.
        ranks_y=avg_rank(ys)
        unique=set(permutations(ranks_y))
        observed=spearman(xs,ys)
        extreme=sum(abs(pearson(avg_rank(xs),yy)) >= abs(observed)-1e-12 for yy in unique)
        return {"method":"full_unique_permutation_of_population_endpoint_ranks",
                "n_permutations":len(unique),
                "two_sided_permutation_p":extreme/len(unique),
                "extreme_assignments":extreme}, observed
    rng=random.Random(SEED)
    observed=spearman(xs,ys)
    rank_x=avg_rank(xs)
    ry=avg_rank(ys)
    extreme=0
    for _ in range(PERMUTATIONS):
        sample=ry[:]
        rng.shuffle(sample)
        if abs(pearson(rank_x,sample))>=abs(observed)-1e-12:extreme+=1
    return {"method":"monte_carlo_population_rank_permutation",
            "rng_seed":SEED,"n_permutations":PERMUTATIONS,
            "extreme_assignments":extreme,
            "two_sided_permutation_p":(extreme+1)/(PERMUTATIONS+1)}, observed

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()

    protocol=(Path(__file__).resolve().parent/"CAMPANULA_NATURAL_HL_ROSETTE_PROTOCOL_20261116.md").read_text(encoding="utf-8")
    for text in ["Protocol v0.1", "individual-level p-value is allowed", "20261116", "POP", "Rosette diameter (cm)"]:
        if text not in protocol:raise EligibilityStop("Frozen pre-outcome protocol invariant missing: "+text)
    raw=source_file(5676272,"Campanula_fitness.xlsx")
    sha=hashlib.sha256(raw).hexdigest()
    if sha!=SOURCE_SHA256:raise EligibilityStop("Pinned natural Campanula workbook digest changed")
    all_rows=read_whitelisted(raw,"xl/worksheets/sheet1.xml",FIELDS)
    # The preceding identifier-only audit already verified 507 original
    # non-header rows, including 5 without accessible POP or Ind.
    from audit_zenodo_genetic_fitness_schema import workbook_sheets
    source_rows=workbook_sheets(raw)[0]["xml_nonempty_rows"]-1
    if source_rows!=507:raise EligibilityStop("Original source row denominator changed")
    rows=[]
    incomplete_id=missing_hl=missing_outcome=0
    count_valid_ids=Counter()
    seen_keys=Counter()
    for r in all_rows:
        pop=r.get("POP","").strip()
        ind=r.get("Ind","").strip()
        if not pop or not ind or pop in MISSING or ind in MISSING:
            incomplete_id+=1
            continue
        seen_keys[(pop,ind)]+=1
        count_valid_ids[pop]+=1
        h=number(r.get("HL"),"HL",lower=0,upper=1)
        size=number(r.get("Rosette diameter (cm)"),"rosette",lower=0)
        if h is None:missing_hl+=1
        if size is None:missing_outcome+=1
        if h is not None and size is not None:
            rows.append({"pop":pop,"HL":h,"rosette":size})
    n_duplicated_ids=sum(v>1 for v in seen_keys.values())
    report={
        "status":"SOURCE_GRAIN_AUDITED",
        "protocol_commit_frozen_before_data_open":PROTOCOL_COMMIT,
        "source_paper_doi":SOURCE_PAPER_DOI,
        "source_data_doi":SOURCE_DATA_DOI,
        "source_sha256":sha,
        "raw_source_rows":source_rows,
        "source_rows_with_any_whitelisted_cell":len(all_rows),
        "incomplete_population_or_individual_ID_rows_in_whitelist_scan":incomplete_id,
        "distinct_valid_population_and_individual_keys":len(seen_keys),
        "repeated_population_individual_keys":n_duplicated_ids,
        "missing_HL_given_valid_ID":missing_hl,
        "missing_rosette_given_valid_ID":missing_outcome,
        "complete_HL_rosette_rows":len(rows),
        "unique_source_populations_with_complete_rows":len({x["pop"] for x in rows}),
        "causal_genetic_rescue_effect_estimated":False,
        "direct_interaction_function_measured":False,
        "programme_count":1,
        "third_party_raw_values_redistributed":False,
    }
    if n_duplicated_ids:
        report.update(status="DUPLICATE_INDIVIDUAL_ID_STOP",decision="Source identifiers are not unique at POPxInd; no effect computed")
    else:
        pops=defaultdict(list)
        for row in rows:pops[row["pop"]].append(row)
        admitted={k:v for k,v in pops.items() if len(v)>=MIN_POP_N}
        dropped={k:len(v) for k,v in pops.items() if len(v)<MIN_POP_N}
        report["eligible_populations"]=len(admitted)
        report["eligible_seed_progeny_n"]=sum(len(v) for v in admitted.values())
        report["excluded_small_population_rows"]=sum(dropped.values())
        report["population_sample_sizes_anonymous"]=sorted([len(v) for v in admitted.values()])
        if len(admitted)<MIN_POPULATIONS:
            report.update(status="POPULATION_COVERAGE_STOP",
                          decision="Too few independent eligible populations for primary association")
        else:
            pop_means=[]
            centred_x=[]
            centred_y=[]
            for key,dat in sorted(admitted.items()):
                hs=[v["HL"] for v in dat]
                ys=[v["rosette"] for v in dat]
                pop_means.append((key,sum(hs)/len(hs),sum(ys)/len(ys)))
                ranks_h=avg_rank(hs)
                ranks_y=avg_rank(ys)
                centred_x.extend(v-sum(ranks_h)/len(ranks_h) for v in ranks_h)
                centred_y.extend(v-sum(ranks_y)/len(ranks_y) for v in ranks_y)
            x=[v[1] for v in pop_means]
            y=[v[2] for v in pop_means]
            uncertainty,estimate=exact_or_mc(x,y)
            if estimate is None:
                report.update(status="CONSTANT_MARKER_OR_GROWTH_STOP",
                              decision="Cross-population variance missing; no rank association estimable")
            else:
                loo=[]
                for i in range(len(x)):
                    test_x=x[:i]+x[i+1:]
                    test_y=y[:i]+y[i+1:]
                    loo.append(spearman(test_x,test_y))
                report.update(
                  status="SINGLE_PROGRAMME_POPULATION_LEVEL_ASSOCIATION_COMPUTED",
                  primary_endpoint="mean_juvenile_rosette_diameter_cm",
                  molecular_predictor="mean_progeny_HL",
                  independent_population_unit=True,
                  population_level_spearman_rho=estimate,
                  null=uncertainty,
                  leave_one_population_out_rho_anonymous=loo,
                  leave_one_out_min_rho=min(loo),
                  leave_one_out_max_rho=max(loo),
                  descriptive_within_population_rank_r_no_p=pearson(centred_x,centred_y),
                  outcome_values_viewed_only_after_protocol=True,
                  decision="ONE observational G-to-juvenile-growth programme, not direct pollination/seed-function rescue and not a cross-programme meta-analysis"
                )
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:report.get(k) for k in (
        "status","raw_source_rows","complete_HL_rosette_rows","eligible_populations",
        "eligible_seed_progeny_n","population_level_spearman_rho","null",
        "leave_one_out_min_rho","leave_one_out_max_rho","decision")},indent=2))

if __name__=="__main__":
    main()
