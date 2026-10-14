#!/usr/bin/env python3
"""Lathyrus reproductive records versus next-year growth and aboveground fate.

Explicit ecological alternative to treating flowering autocorrelation as
evidence of reproductive carry-over: flowering may positively index persistent
vigor while reproductive output has costs in subsequent vegetative performance.
Source-pinned historical Swedish perennial dataset, observational only;
this is NOT a fragmentation experiment or a new EGWEE primary meta-analysis.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path

from audit_lathyrus_external_history_order import (
    YEARS, load_pinned, numeric, year_state
)

def size_bin(v: float, scale: float=1.) -> int:
    assert v>0 and math.isfinite(v)
    return min(int(math.log1p(v)//scale), 15)

def extract(df) -> tuple[list[dict], dict]:
    states=year_state(df)
    source_rows={}
    for _,row in df.iterrows():
        k=(str(row["SUBPLOT"]),str(row["GENET"]))
        assert k not in source_rows
        source_rows[k]=row
    assert len(states)==len(source_rows)==1119
    result=[]
    next_class=Counter()
    next_flag_patterns=Counter()
    for k,years in states.items():
        raw=source_rows[k]
        for t in YEARS[:-1]:
            prior,next_state=years[t],years[t+1]
            if not prior["confirmed_aboveground_and_fcode"]:
                continue
            after=bool(next_state["confirmed_aboveground_and_fcode"])
            flags=next_state["source_status_flags"]
            confirmed=[key for key in ("Dead","Dormant","Missing")
                       if flags[key]==1.]
            # Dormant and Missing are NOT exclusive in the source. Preserve
            # overlaps instead of silently interpreting them as mortality.
            label=("measured_aboveground" if after
                   else "+".join(z.lower() for z in confirmed)
                   if confirmed else "unclassified_not_aboveground")
            next_flag_patterns[",".join(confirmed) if confirmed else "none"]+=1
            next_class[label]+=1
            if after:
                assert next_state["volume"]>0
            flowering=prior["flowering"]
            assert flowering in (0,1)
            seed=numeric(raw[f"Intactseed{t%100:02d}"])
            flower_number=numeric(raw[f"Flow{t%100:02d}"])
            if seed is not None:
                assert seed>=0,(k,t,seed)
            if flower_number is not None:
                assert flower_number>=0,(k,t,flower_number)
            result.append({
                "subplot":k[0],"genet":k[1],"year":t,
                "prior_flowering":flowering,
                "prior_volume":prior["volume"],
                "prior_logvolume":math.log(prior["volume"]),
                "source_intactseed":seed,
                "seed_positive":int(seed>0) if seed is not None else None,
                "source_flower_number":flower_number,
                "next_status":label,
                "next_aboveground":int(after),
                "next_volume":next_state["volume"] if after else None,
                "next_logvolume":math.log(next_state["volume"]) if after else None,
                "log_volume_growth":(math.log(next_state["volume"]/prior["volume"])
                                     if after else None),
            })
    assert len(result)==sum(next_class.values())
    assert len({(r["subplot"],r["genet"],r["year"]) for r in result})==len(result)
    npaired=sum(r["next_aboveground"] for r in result)
    return result,{
        "source_genets":len(states),
        "eligible_prior_aboveground_years":len(result),
        "next_state_classes":dict(next_class),
        "next_status_flag_combinations":dict(next_flag_patterns),
        "next_year_aboveground_observed":npaired,
        "n_source_intact_seed_records":sum(r["source_intactseed"] is not None for r in result),
        "n_positive_flowering_with_zero_seeds":sum(
            r["prior_flowering"]==1 and r["seed_positive"]==0 for r in result
        ),
        "n_positive_flowering_with_positive_seeds":sum(
            r["prior_flowering"]==1 and r["seed_positive"]==1 for r in result
        ),
        "n_positive_flowering_with_intact_seed_record":sum(
            r["prior_flowering"] and r["source_intactseed"] is not None for r in result
        ),
    }

def weighted_contrast(rows: list[dict], outcome: str, scale: float=1.,
                      exposure: str="prior_flowering") -> dict:
    # Matching uses ONLY prior status to define strata. Growth comparisons
    # necessarily condition on the subsequent plant being found aboveground;
    # report unobserved-status contrasts separately, not as deaths.
    strata=defaultdict(lambda:{0:[],1:[]})
    for r in rows:
        v=r[outcome]
        if v is None:
            continue
        key=(r["subplot"],r["year"],size_bin(r["prior_volume"],scale))
        assignment=r[exposure]
        assert assignment in (0,1),(exposure,assignment)
        strata[key][assignment].append(float(v))
    contrast_weighted=weight_total=0.
    informative=0
    p1_total=p0_total=0
    for v in strata.values():
        n0,n1=len(v[0]),len(v[1])
        if not n0 or not n1:
            continue
        effect=(sum(v[1])/n1)-(sum(v[0])/n0)
        weight=n0*n1/(n0+n1)
        assert weight>0
        contrast_weighted+=effect*weight
        weight_total+=weight
        informative+=1
        p1_total+=n1
        p0_total+=n0
    return {
        "outcome":outcome,
        "exposure":exposure,
        "prior_logvolume_bin_width":scale,
        "matched_flowering_minus_nonflowering":(
            contrast_weighted/weight_total if weight_total else None),
        "effective_overlap_weight":weight_total,
        "n_strata_total":len(strata),
        "n_strata_informative":informative,
        "n_flowering_in_informative_strata":p1_total,
        "n_nonflowering_in_informative_strata":p0_total,
        "denominator_warning":(
            "Conditional on next-year aboveground observation"
            if outcome in ("next_logvolume","log_volume_growth")
            else "Prior-observed aboveground plants; next missing/dormant/dead retained as not confirmed aboveground"),
    }

def calculate(rows: list[dict]) -> dict:
    groups={}
    for flowering in (0,1):
        a=[r for r in rows if r["prior_flowering"]==flowering]
        emerged=[r for r in a if r["next_aboveground"]]
        growth=[r["log_volume_growth"] for r in emerged]
        groups[str(flowering)]={
            "n_prior_observed":len(a),
            "n_next_confirmed_aboveground":len(emerged),
            "next_aboveground_fraction":len(emerged)/len(a),
            "mean_prior_logvolume":sum(r["prior_logvolume"] for r in a)/len(a),
            "mean_log_volume_growth_next_observed":(
                sum(growth)/len(growth) if growth else None),
            "mean_next_logvolume_observed":(
                sum(r["next_logvolume"] for r in emerged)/len(emerged)
                if emerged else None),
            "next_state_classes":dict(Counter(r["next_status"] for r in a))
        }
    outcomes={}
    for metric in ("next_aboveground","next_logvolume","log_volume_growth"):
        outcomes[metric]={
            "main":weighted_contrast(rows,metric,1.),
            "finer_size":weighted_contrast(rows,metric,0.5),
            "coarser_size":weighted_contrast(rows,metric,2.),
        }
    fruiters=[r for r in rows if r["prior_flowering"]==1
              and r["seed_positive"] in (0,1)]
    seed_contrasts={}
    for metric in ("next_aboveground","next_logvolume","log_volume_growth"):
        seed_contrasts[metric]={
            "main":weighted_contrast(fruiters,metric,1.,"seed_positive"),
            "finer_size":weighted_contrast(fruiters,metric,0.5,"seed_positive"),
            "coarser_size":weighted_contrast(fruiters,metric,2.,"seed_positive"),
        }
    return {"groups":groups,"matched_prior_state_contrasts":outcomes,
            "among_prior_flowering_seed_produced_vs_zero":seed_contrasts,
            "n_prior_flowering_with_mature_seed_data":len(fruiters)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--local-rda",type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    df,provenance=load_pinned(args.local_rda)
    rows,profile=extract(df)
    assert profile["eligible_prior_aboveground_years"]>2000
    result={
        "status":"EXTERNAL_LATHYRUS_REPRODUCTION_GROWTH_OBSERVATIONAL_NOT_CAUSAL",
        "provenance":provenance,
        "source_demography":profile,
        "all_adjacent_year_pairs":calculate(rows),
        "by_start_year":{
            str(y):calculate([r for r in rows if r["year"]==y])
            for y in YEARS[:-1]
        },
        "leave_one_year_out":{
            str(y):{
                m:weighted_contrast([r for r in rows if r["year"]!=y],m,1.)
                for m in ("next_aboveground","next_logvolume","log_volume_growth")
            }
            for y in YEARS[:-1]
        },
        "leave_one_subplot_out":{
            p:{
                m:weighted_contrast([r for r in rows if r["subplot"]!=p],m,1.)
                for m in ("next_aboveground","next_logvolume","log_volume_growth")
            }
            for p in sorted({r["subplot"] for r in rows})
        },
        "scientific_limits":[
            "Only 1988-1991 within one already published Swedish Lathyrus study; 1119 genets / 6 subplots, repeated year-pairs are not independent.",
            "Flowering was not assigned or randomized; size, condition and climate can jointly determine flowering, growth and next-year appearance.",
            "Conditional next-year growth measures exclude plants dormant, missing or dead and can be subject to selection on future survival/observation.",
            "Next-year not-aboveground is NOT labeled mortality: dormant and missing flags can overlap within original records and are preserved as joint states.",
            "Log volume growth can exhibit regression-to-mean artefacts, so next-year log-volume contrast is also reported.",
            "Source Intactseed counts include model-estimated values and are not automatically independent measured reproductive effort.",
            "Comparison within documented flowering plants of zero versus positive mature seeds selects fruiting versus failure and may reflect poor health or prior pollination rather than any experimentally manipulated investment.",
            "Coarse prior-volume binning leaves within-bin size confounding; fine and coarse alternative bins and leave-one-year/subplot are exploratory.",
            "No formal statistical or causal claim of reproductive cost, no novel ecological law, and no fragmentation treatment contrasts.",
            "Biological history effects and costs are well known in historical Lathyrus research and must not be claimed as new from this analysis.",
            "EGWEE empirical frozen primary/eight/sixteen-programme and SF06 denominator remain unchanged. PR draft submission_ready=false."
        ],
    }
    for k in ("next_aboveground","next_logvolume","log_volume_growth"):
        val=result["all_adjacent_year_pairs"]["matched_prior_state_contrasts"][k]["main"]
        assert val["n_strata_informative"]>0
        assert val["matched_flowering_minus_nonflowering"] is not None
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("LATHYRUS_REPRODUCTIVE_COST_STAGE_FALSIFICATION: PASS")
    print(json.dumps({
        "provenance":{k:provenance[k] for k in ("original_git_blob_sha","source_rows")},
        "sample":profile,
        "all":result["all_adjacent_year_pairs"],
        "yearwise":{
            y:{k:v["matched_prior_state_contrasts"][k]["main"]["matched_flowering_minus_nonflowering"]
               for k in ("next_aboveground","next_logvolume","log_volume_growth")}
            for y,v in result["by_start_year"].items()},
        "omit_year":{
            y:{k:v[k]["matched_flowering_minus_nonflowering"] for k in v}
            for y,v in result["leave_one_year_out"].items()}
    },indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
