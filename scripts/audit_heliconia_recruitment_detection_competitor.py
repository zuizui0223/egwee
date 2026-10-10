#!/usr/bin/env python3
"""2002->2003 same-plant ascertainment, flowering and recruitment accounting.

One published Heliconia programme, post hoc descriptive diagnostic only.
Use source-pinned upstream HDP archive; no new admissions to EGWEE synthesis.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from analyze_heliconia_census_panel import load_csv
from audit_heliconia_forward_lag_prediction import archive_rows

def audit(local_dir: Path | None) -> dict:
    rows, provenance = archive_rows(local_dir)
    plots = {r["plot_id"]:r for r in load_csv("HDP_plots.csv",local_dir)}
    data = load_csv("HDP_survey.csv",local_dir)
    assert len(data)==66396 and len(plots)==13
    counts=defaultdict(lambda: {"measured":0,"missing":0,"dead":0,"fl":0,"infl":0,"new":0})
    by_plant=defaultdict(dict)
    for r in data:
        p,i,y=r["plot_id"],r["plant_id"],int(r["year"])
        state=r["census_status"]
        assert state in ("measured","missing","dead")
        by_plant[(p,i)][y]=state
        counts[(p,y)][state]+=1
        if r["recorded_sdlg"]=="TRUE":
            assert state=="measured"
            counts[(p,y)]["new"]+=1
        raw=r["infl"].strip()
        if raw and raw.upper()!="NA":
            assert state=="measured"
            val=float(raw)
            assert math.isfinite(val) and val>=0
            counts[(p,y)]["infl"]+=val
            counts[(p,y)]["fl"]+=int(val>0)
    assert sum(v["new"] for v in counts.values())==3464
    common=set.intersection(*[
        {r["plot"] for r in rows if r["year"]==y}
        for y in range(2001,2006)
    ])
    assert len(common)==10
    expected={"CF-4","CF-5","CF-6"}
    assert common.isdisjoint(expected),common
    pairs=[]
    for p in sorted(common):
        d={"plot":p,"ranch":plots[p]["ranch"],"habitat":plots[p]["habitat"]}
        for y in (2002,2003):
            earlier=counts[(p,y-1)]
            now=counts[(p,y)]
            prior_measured={
                ident for (plot,ident),states in by_plant.items()
                if plot==p and states.get(y-1)=="measured"
            }
            next_states=[
                by_plant[(p,i)].get(y,"NOT_PRESENT") for i in prior_measured
            ]
            assert all(s!="NOT_PRESENT" for s in next_states),(
                p,y,{x:next_states.count(x) for x in set(next_states)}
            )
            total=len(next_states)
            verified=sum(s in ("measured","dead") for s in next_states)
            missing=sum(s=="missing" for s in next_states)
            assert verified+missing==total
            assert total==earlier["measured"]>0
            assert now["measured"]>0
            d[str(y)]={
                "prior_alive_count":total,
                "prior_alive_next_census_verified":verified,
                "prior_alive_next_census_missing":missing,
                "prior_alive_verification_fraction":verified/total,
                "prior_alive_next_dead":sum(s=="dead" for s in next_states),
                "new_seedling_records":now["new"],
                "prior_flowering_individuals":earlier["fl"],
                "prior_inflorescences":earlier["infl"],
                "year_census_measured_count":now["measured"],
                "year_census_missing_count":now["missing"],
                "year_census_dead_count":now["dead"],
            }
        d["seedling_change"]=d["2003"]["new_seedling_records"]-d["2002"]["new_seedling_records"]
        d["verification_fraction_change"]=(
            d["2003"]["prior_alive_verification_fraction"]
            -d["2002"]["prior_alive_verification_fraction"]
        )
        d["flowering_change"]=(
            d["2003"]["prior_flowering_individuals"]
            -d["2002"]["prior_flowering_individuals"]
        )
        pairs.append(d)
    def summarise(rows: list[dict]) -> dict:
        assert rows
        n=len(rows)
        out={"n_plots":n}
        for y in ("2002","2003"):
            totprev=sum(r[y]["prior_alive_count"] for r in rows)
            found=sum(r[y]["prior_alive_next_census_verified"] for r in rows)
            out[y]={
                "mean_recruits":sum(r[y]["new_seedling_records"] for r in rows)/n,
                "mean_prior_stock":sum(r[y]["prior_alive_count"] for r in rows)/n,
                "mean_prior_flowering":sum(r[y]["prior_flowering_individuals"] for r in rows)/n,
                "mean_prior_inflorescences":sum(r[y]["prior_inflorescences"] for r in rows)/n,
                "verified_prior_live_plants":found,
                "previously_measured_plants":totprev,
                "pooled_previous_alive_fate_verification":found/totprev,
                "equal_plot_fate_verification":sum(r[y]["prior_alive_verification_fraction"] for r in rows)/n,
                "new_per_prior_flowering":(
                    sum(r[y]["new_seedling_records"] for r in rows)
                    / sum(r[y]["prior_flowering_individuals"] for r in rows)
                ),
                "new_per_prior_all_alive":(
                    sum(r[y]["new_seedling_records"] for r in rows)/totprev
                )
            }
        out["recruits_declined_in_plots"]=sum(r["seedling_change"]<0 for r in rows)
        out["prior_flowering_declined_in_plots"]=sum(r["flowering_change"]<0 for r in rows)
        out["fate_verification_declined_in_plots"]=sum(r["verification_fraction_change"]<0 for r in rows)
        out["recruit_ratio_2003_to_2002"]=out["2003"]["mean_recruits"]/out["2002"]["mean_recruits"]
        out["flowering_ratio_2003_to_2002"]=out["2003"]["mean_prior_flowering"]/out["2002"]["mean_prior_flowering"]
        out["conversion_ratio_2003_to_2002"]=out["2003"]["new_per_prior_flowering"]/out["2002"]["new_per_prior_flowering"]
        assert math.isclose(out["recruit_ratio_2003_to_2002"],
                            out["flowering_ratio_2003_to_2002"]*out["conversion_ratio_2003_to_2002"],
                            abs_tol=1e-10)
        return out
    full=summarise(pairs)
    ranches={k:summarise([r for r in pairs if r["ranch"]==k])
             for k in sorted({r["ranch"] for r in pairs})}
    habitats={"continuous":summarise([r for r in pairs if r["habitat"]=="forest"]),
              "fragmented":summarise([r for r in pairs if r["habitat"]!="forest"])}
    return {
        "status":"EXPLORATORY_INDIVIDUAL_FATE_OBSERVABILITY_AND_REPRODUCTIVE_ACCOUNTING",
        "source_years":"2001-2003 observation; 2002 and 2003 recruitment",
        "eligible_fixed_plots":sorted(common),
        "source_hashes_pinned":True,
        "full":full,"by_ranch":ranches,"by_habitat":habitats,"by_plot":pairs,
        "interpretation_guards":[
            "A tracked prior adult/juvenile fate is NOT directly the detection probability of new seedlings.",
            "First record of a seedling is not all biological germination or establishment.",
            "Annual census records and flowering surveys may have different effort and timing.",
            "Ratios new recruits per documented flowering individual mix distinct maternal cohorts, dispersal and seed banks.",
            "A multiplicative decline decomposition is algebraic, not a causal contribution.",
            "Three ranch groups are not independent climate replicates; one species landscape only.",
            "No confirmed climate, mating, or restoration mechanism; do not promote a new law.",
        ]
    }

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--local-dir",type=Path)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    result=audit(args.local_dir)
    assert result["full"]["n_plots"]==10
    assert result["full"]["2002"]["mean_recruits"]==44.5
    assert result["full"]["2003"]["mean_recruits"]==14.1
    if args.output:
        args.output.parent.mkdir(exist_ok=True,parents=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("HELICONIA_FATE_COVERAGE_REPRODUCTIVE_ACCOUNTING: PASS")
    print(json.dumps({k:v for k,v in result.items() if k!="by_plot"},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
