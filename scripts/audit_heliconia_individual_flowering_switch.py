#!/usr/bin/env python3
"""Heliconia repeated-plant documented flowering transitions.

Tests whether a population-wide annual flowering pulse can be accounted for
by mortality/individual turnover alone. Archive infl=NA is NOT independently
verified nonflowering; interpret as no positive record, never true absence.
"""
from __future__ import annotations
from collections import defaultdict
import argparse
import json
from pathlib import Path
from analyze_heliconia_census_panel import load_csv
from audit_heliconia_forward_lag_prediction import archive_rows

YEARS=(2001,2002,2003,2004)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    all_rows,_=archive_rows(None)
    common=set.intersection(*[
        {r["plot"] for r in all_rows if r["year"]==y}
        for y in range(2001,2006)
    ])
    assert len(common)==10
    src=load_csv("HDP_survey.csv",None)
    assert len(src)==66396
    states=defaultdict(dict)
    for r in src:
        p,ident,y=r["plot_id"],r["plant_id"],int(r["year"])
        if p not in common or y not in YEARS:
            continue
        key=(p,ident)
        assert y not in states[key],(key,y)
        status=r["census_status"]
        assert status in ("measured","missing","dead")
        infl=r["infl"].strip()
        pos=(bool(infl) and infl.upper()!="NA" and float(infl)>0)
        if pos:
            assert status=="measured"
        states[key][y]=(status,pos)
    by_plot={}
    for p in sorted(common):
        by_plot[p]={}
        keys=[k for k in states if k[0]==p]
        for old,new in zip(YEARS,YEARS[1:]):
            old_pos={k for k in keys if states[k].get(old,("",False))==("measured",True)}
            new_pos={k for k in keys if states[k].get(new,("",False))==("measured",True)}
            old_alive={k for k in keys if states[k].get(old,("",False))[0]=="measured"}
            new_alive={k for k in keys if states[k].get(new,("",False))[0]=="measured"}
            matched=old_alive & new_alive
            lost=old_pos & matched - new_pos
            gained=new_pos & matched - old_pos
            retained=old_pos & new_pos
            prior_positive_not_measured=old_pos-new_alive
            newly_positive_not_measured_prev=new_pos-old_alive
            assert len(old_pos)==len(retained)+len(lost)+len(prior_positive_not_measured)
            assert len(new_pos)==len(retained)+len(gained)+len(newly_positive_not_measured_prev)
            # Transition identity: total D+ - D- = gained - lost +
            # new flowering outside matched - old flowering outside matched.
            assert len(new_pos)-len(old_pos)==(
                len(gained)-len(lost)+len(newly_positive_not_measured_prev)-
                len(prior_positive_not_measured)
            )
            pos_old_matched=len(old_pos & matched)
            pos_new_matched=len(new_pos & matched)
            n_matched=len(matched)
            new_pos_when_old_pos=len(retained)
            new_pos_when_old_not=len(gained)
            by_plot[p][f"{old}_{new}"]={
                "previous_documented_positive":len(old_pos),
                "next_documented_positive":len(new_pos),
                "previous_living_measured":len(old_alive),
                "next_living_measured":len(new_alive),
                "same_individuals_measured_in_both":n_matched,
                "positive_in_both":len(retained),
                "previous_positive_both_measured_not_positive_next":len(lost),
                "previous_no_positive_both_measured_positive_next":len(gained),
                "previous_positive_not_measured_next":len(prior_positive_not_measured),
                "new_positive_not_measured_prev":len(newly_positive_not_measured_prev),
                "previous_positive_both_measured":pos_old_matched,
                "next_positive_both_measured":pos_new_matched,
                "conditional_next_positive_given_prev_positive":(
                    new_pos_when_old_pos/pos_old_matched if pos_old_matched else None
                ),
                "conditional_next_positive_given_prev_not_positive":(
                    new_pos_when_old_not/(n_matched-pos_old_matched)
                    if n_matched-pos_old_matched else None
                ),
            }
    aggregates={}
    for old,new in zip(YEARS,YEARS[1:]):
        period=f"{old}_{new}"
        records=[by_plot[p][period] for p in sorted(common)]
        keys=[
            "previous_documented_positive","next_documented_positive",
            "previous_living_measured","next_living_measured",
            "same_individuals_measured_in_both","positive_in_both",
            "previous_positive_both_measured_not_positive_next",
            "previous_no_positive_both_measured_positive_next",
            "previous_positive_not_measured_next","new_positive_not_measured_prev",
            "previous_positive_both_measured","next_positive_both_measured"
        ]
        sums={key:sum(rec[key] for rec in records) for key in keys}
        sums["n_plots_with_positive_record_decline"]=sum(
            rec["next_documented_positive"]<rec["previous_documented_positive"]
            for rec in records
        )
        sums["within_individual_net_positive_change"]=(
            sums["previous_no_positive_both_measured_positive_next"]
            -sums["previous_positive_both_measured_not_positive_next"]
        )
        sums["turnover_net_positive_change"]=(
            sums["new_positive_not_measured_prev"]
            -sums["previous_positive_not_measured_next"]
        )
        sums["observed_positive_change"]=(
            sums["next_documented_positive"]-sums["previous_documented_positive"]
        )
        assert sums["within_individual_net_positive_change"]+sums[
            "turnover_net_positive_change"]==sums["observed_positive_change"]
        if sums["previous_positive_both_measured"]:
            sums["next_positive_given_prior_positive"]=(
                sums["positive_in_both"]/sums["previous_positive_both_measured"]
            )
        else:
            sums["next_positive_given_prior_positive"]=None
        denom=(sums["same_individuals_measured_in_both"]-
               sums["previous_positive_both_measured"])
        sums["next_positive_given_prior_nonpositive"]=(
            sums["previous_no_positive_both_measured_positive_next"]/denom
            if denom else None
        )
        aggregates[period]=sums
    assert aggregates["2001_2002"]["previous_documented_positive"]==236
    assert aggregates["2001_2002"]["next_documented_positive"]==116
    assert aggregates["2002_2003"]["next_documented_positive"]==382
    assert aggregates["2003_2004"]["next_documented_positive"]==165
    report={
        "status":"EXPLORATORY_SAME_TAG_FLOWERING_STATUS_CHANGE_NOT_CAUSAL",
        "source_hdp_plant_years":66396,
        "n_fixed_plots":10,
        "n_repeated_plant_IDs":len(states),
        "pooled_transitions":aggregates,
        "by_plot":by_plot,
        "limits":[
            "No positive inflorescence record is not independently certified nonflowering: possible observation effort artefact.",
            "Matched individuals must be measured in both years; selection can bias apparent flowering state changes.",
            "An annual positive-flowering record is neither viable-seed production nor mating success.",
            "Within-individual recording variation cannot be interpreted as cost of reproduction without size/resources/detection controls.",
            "Distinct annual flowering seasons may not map directly onto calendar-year first-marked seedling cohorts.",
            "One study with three ranches, ten plots; demographic transitions are not independent landscape replicates.",
            "This ledger is an identity, not a causal factor attribution; no newly confirmed universal ecological law.",
        ]
    }
    if args.output:
        args.output.parent.mkdir(exist_ok=True,parents=True)
        args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("HELICONIA_INDIVIDUAL_FLOWERING_SWITCH: PASS")
    print(json.dumps({
        "n_fixed_plots":10,
        "n_repeated_plant_IDs":len(states),
        "pooled_transitions":aggregates
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
