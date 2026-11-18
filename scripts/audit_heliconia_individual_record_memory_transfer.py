#!/usr/bin/env python3
"""Same-plant reproductive-record persistence versus future-year predictive utility.

Exploratory external Heliconia archive, not an EGWEE primary study admission.
Two separate questions:
  A. Does past recorded flowering associate with next year's recorded flowering
     within plot, calendar transition, prior measured size and shoots?
  B. Does *adding* past recorded flowering actually improve future-calendar-
     year prediction over observed morphology alone?

Source-pinned via analyze_heliconia_census_panel.load_csv. No causal or
independent landscape claim; positive records may have imperfect detection.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path

from analyze_heliconia_census_panel import load_csv

PANEL_PLOTS = ("CF-1", "CF-2", "CF-3", "FF-1", "FF-2", "FF-3", "FF-4",
               "FF-5", "FF-6", "FF-7")
START_YEARS = tuple(range(1998, 2005))
FORECAST_STARTS = (2002, 2003, 2004)
YEAR_CORE = (2001, 2002, 2003, 2004)

def hbin(v: float, fine: bool = False) -> int:
    assert math.isfinite(v) and v >= 0
    if fine:
        return min(int(v // 10), 20)
    return min(int(v // 25), 5)

def sbin(v: float) -> int:
    assert math.isfinite(v) and v >= 0
    return 0 if v < 3 else 1 if v < 5 else 2 if v < 8 else 3

def build_rows(local_dir: Path | None) -> tuple[list[dict], dict]:
    source = load_csv("HDP_survey.csv", local_dir)
    plots = {z["plot_id"]: z for z in load_csv("HDP_plots.csv", local_dir)}
    assert len(source) == 66396 and len(plots) == 13
    assert set(PANEL_PLOTS) <= set(plots)
    plants: dict[tuple[str, str], dict[int, dict]] = defaultdict(dict)
    for z in source:
        p, year = z["plot_id"], int(z["year"])
        if p not in PANEL_PLOTS or not 1998 <= year <= 2005:
            continue
        ident = (p, z["plant_id"])
        assert year not in plants[ident], (p, ident, year)
        stat = z["census_status"]
        assert stat in {"measured", "dead", "missing"}
        infl = z["infl"].strip()
        positive = False
        if infl and infl != "NA":
            value = float(infl)
            assert math.isfinite(value) and value >= 0 and stat == "measured"
            positive = value > 0
        h, shoots = z["ht"].strip(), z["shts"].strip()
        plants[ident][year] = {
            "alive": stat == "measured",
            "positive": int(positive),
            "height": None if h in {"", "NA"} else float(h),
            "shoots": None if shoots in {"", "NA"} else float(shoots),
        }
    rows=[]
    missing_height_or_shoot=0
    for (p, _), history in plants.items():
        for year in START_YEARS:
            prev, nxt = history.get(year), history.get(year + 1)
            if not prev or not nxt or not prev["alive"] or not nxt["alive"]:
                continue
            height, shoots = prev["height"], prev["shoots"]
            if height is None or shoots is None:
                missing_height_or_shoot += 1
                continue
            assert math.isfinite(height) and math.isfinite(shoots)
            next_height, next_shoots = nxt["height"], nxt["shoots"]
            rows.append({
                "plot": p, "ranch": plots[p]["ranch"], "year": year,
                "prev": prev["positive"], "next": nxt["positive"],
                "height": hbin(height), "height10": hbin(height, True),
                "shoot": sbin(shoots),
                "next_height": None if next_height is None else hbin(next_height),
                "next_shoot": None if next_shoots is None else sbin(next_shoots),
            })
    rows.sort(key=lambda r:(r["year"],r["plot"],r["height"],r["shoot"],r["prev"],r["next"]))
    assert len(rows)==28247, len(rows)
    assert sum(r["year"] in FORECAST_STARTS for r in rows)==13542
    assert sum(r["next"] for r in rows if r["year"] in FORECAST_STARTS)==648
    assert all(z["plot"] in PANEL_PLOTS and 1998 <= z["year"] <= 2004 for z in rows)
    return rows, {
        "n_source_plant_years":len(source),
        "n_source_plots":len(plots),
        "n_plot_panels":len(PANEL_PLOTS),
        "n_morphology_complete_alive_to_alive_transitions":len(rows),
        "n_excluded_measured_both_but_no_prior_height_or_shoot":missing_height_or_shoot,
        "n_forward_year_predictions":13542,
        "observed_flowering_records_in_forward_years":648,
    }

def mh_odds(rows: list[dict], include_next: str = "none",
            fine: bool = False) -> dict:
    groups = defaultdict(lambda: [0,0,0,0])
    eligible=0
    for x in rows:
        parts=[x["plot"], x["year"], x["height10"] if fine else x["height"], x["shoot"]]
        if include_next in ("height","both"):
            if x["next_height"] is None:
                continue
            parts.append(x["next_height"])
        if include_next in ("shoots","both"):
            if x["next_shoot"] is None:
                continue
            parts.append(x["next_shoot"])
        index=2*x["prev"]+x["next"]
        # 0=none/none(d), 1=no/yes(c), 2=yes/no(b), 3=yes/yes(a)
        groups[tuple(parts)][index]+=1
        eligible+=1
    numerator=denominator=0.0
    informative=0
    for d,c,b,a in groups.values():
        n=a+b+c+d
        assert n>0
        numerator+=a*d/n
        denominator+=b*c/n
        if min(a+b,c+d,a+c,b+d)>0:
            informative+=1
    assert denominator>0
    return {
        "odds_ratio":numerator/denominator,
        "n_individual_year_transitions":eligible,
        "n_strata":len(groups),
        "n_informative_strata":informative,
        "strata":"plot × calendar transition × prior height × prior shoots"
                 + (" × current "+include_next if include_next!="none" else ""),
    }

def score_cases(predictions: list[dict]) -> dict:
    assert predictions
    n=len(predictions)
    sq0=sq1=ll0=ll1=0.
    for z in predictions:
        y,p0,p1=z["y"],z["size_only"],z["size_plus_past_flower"]
        assert y in (0,1) and 0 < p0 < 1 and 0 < p1 < 1
        sq0+=(y-p0)**2
        sq1+=(y-p1)**2
        ll0-=y*math.log(p0)+(1-y)*math.log1p(-p0)
        ll1-=y*math.log(p1)+(1-y)*math.log1p(-p1)
    return {
        "n":n,"positive_next_records":sum(z["y"] for z in predictions),
        "brier_size_only":sq0/n,"brier_size_plus_past_flower":sq1/n,
        "brier_gain_from_past_flower":(sq0-sq1)/n,
        "logloss_size_only":ll0/n,"logloss_size_plus_past_flower":ll1/n,
        "logloss_gain_from_past_flower":(ll0-ll1)/n,
    }

def train_predict(train: list[dict], test: list[dict],
                  past_record_shrinkage: float = 20.) -> list[dict]:
    # All global means and cell probabilities are trained from past years only.
    global_n=len(train)
    global_y=sum(r["next"] for r in train)
    assert global_n and 0<global_y<global_n
    global_risk=(global_y+0.5)/(global_n+1)
    joint=defaultdict(lambda:[0,0])
    observed_state=defaultdict(lambda:[0,0])
    for z in train:
        key=(z["height"],z["shoot"])
        joint[key][0]+=z["next"]
        joint[key][1]+=1
        key2=(*key,z["prev"])
        observed_state[key2][0]+=z["next"]
        observed_state[key2][1]+=1
    predictions=[]
    for z in test:
        key=(z["height"],z["shoot"])
        succ,n=joint[key]
        baseline=(succ+25*global_risk)/(n+25)
        succ2,n2=observed_state[(*key,z["prev"])]
        extended=(succ2+past_record_shrinkage*baseline)/(n2+past_record_shrinkage)
        predictions.append({
            "year":z["year"],"plot":z["plot"],"ranch":z["ranch"],
            "prev":z["prev"],"y":z["next"],
            "size_only":baseline,"size_plus_past_flower":extended,
        })
    return predictions

def forward_comparison(rows: list[dict], shrinkage: float = 20.) -> dict:
    all_predictions=[]
    by_year={}
    for y in FORECAST_STARTS:
        train=[z for z in rows if z["year"]<y]
        test=[z for z in rows if z["year"]==y]
        assert train and test and max(z["year"] for z in train)<min(z["year"] for z in test)
        fitted=train_predict(train,test,shrinkage)
        all_predictions.extend(fitted)
        by_year[str(y)+"_to_"+str(y+1)]=score_cases(fitted)
    by_ranch={r:score_cases([z for z in all_predictions if z["ranch"]==r])
              for r in sorted({z["ranch"] for z in all_predictions})}
    by_prev={str(p):score_cases([z for z in all_predictions if z["prev"]==p])
             for p in (0,1)}
    by_plot={p:score_cases([z for z in all_predictions if z["plot"]==p])
             for p in sorted({z["plot"] for z in all_predictions})}
    return {
        "pooled_all_three_future_years":score_cases(all_predictions),
        "by_held_future_year":by_year,
        "by_ranch":by_ranch,
        "by_prior_flowering_record":by_prev,
        "by_plot":by_plot,
        "fraction_heldout_plots_improved_brier":sum(
            z["brier_gain_from_past_flower"]>0 for z in by_plot.values()
        )/len(by_plot),
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--local-dir",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    rows,provenance=build_rows(args.local_dir)
    core=[x for x in rows if x["year"] in YEAR_CORE]
    result={
        "status":"EXPLORATORY_REPRODUCTIVE_RECORD_ASSOCIATION_VS_PROSPECTIVE_PREDICTION",
        "provenance":provenance,
        "marginal_contingency":{},
        "size_shoot_plot_year_odds":{
            "all_1998_2004":mh_odds(rows),
            "core_2001_2004":mh_odds(core),
            "core_with_next_height":mh_odds(core,include_next="height"),
            "core_with_next_shoots":mh_odds(core,include_next="shoots"),
            "core_with_next_height_and_shoots":mh_odds(core,include_next="both"),
            "core_finer_prior_height_bins":mh_odds(core,fine=True),
            "by_year":{str(y):mh_odds([r for r in rows if r["year"]==y])
                       for y in START_YEARS},
            "leave_one_year_out_core":{
                str(yr):mh_odds([z for z in core if z["year"]!=yr])
                for yr in YEAR_CORE
            },
            "leave_one_ranch_out_core":{
                ranch:mh_odds([z for z in core if z["ranch"]!=ranch])
                for ranch in sorted({z["ranch"] for z in core})
            },
            "leave_one_plot_out_core":{
                plot:mh_odds([z for z in core if z["plot"]!=plot])
                for plot in PANEL_PLOTS
            },
        },
        "chronological_predictions":{
            "primary_shrinkage_20":forward_comparison(rows,20.),
            "shrinkage_sensitivity":{
                str(k):forward_comparison(rows,k)["pooled_all_three_future_years"]
                for k in (5.,100.,300.)
            },
            "model_and_time_rule":"For each transition start 2002, 2003, 2004, train only earlier annual transitions. Compare smoothed height-and-shoot cell probability vs the same plus previous recorded flowering. Bayesian cell shrinkage was explored post hoc, not preregistered. Held years mean outcome records 2003, 2004, 2005.",
        },
        "scientific_limits":[
            "All data come from one published Heliconia programme spanning 10 selected plots and three ranch blocks.",
            "Same plant can contribute several year-pairs: 28,247 pairs are not independent biological experiments.",
            "No-positive inflorescence record is not certified absence of flowering: visit effort and phenology can vary by year.",
            "Stratifying on prior height and shoot number cannot eliminate unmeasured stable plant health or resources.",
            "Adding current-year height/shoot status is a post-response conditional sensitivity and not a causal adjustment.",
            "The Mantel-Haenszel odds ratio is a descriptive common-odds summary; no population p-value or calibrated uncertainty is inferred from thousands of correlated plant-year records.",
            "Future-year prediction comparisons are within the same landscape/individual population, not species-level replication.",
            "Brier/logloss gains are tiny if the independent-year performance remains similar, even for a sizable adjusted odds ratio.",
            "This is an observed flowering-record persistence analysis, not true physiological memory or reproductive success.",
            "Prior work already established size-dependent flowering, temporal climate responses, and stage-limited recruitment in this taxon.",
            "This is empirical egwee, not the theoretical egwe framework. Frozen five/eight/sixteen-programme and SF06 denominators remain unchanged.",
        ],
    }
    for subset_name,items in (("core_2001_2004",core),("all_1998_2004",rows)):
        a=b=c=d=0
        for z in items:
            if z["prev"] and z["next"]:a+=1
            elif z["prev"]:b+=1
            elif z["next"]:c+=1
            else:d+=1
        result["marginal_contingency"][subset_name]={"a":a,"b":b,"c":c,"d":d,
                                                     "naive_odds_ratio":a*d/(b*c)}
    assert abs(result["size_shoot_plot_year_odds"]["core_2001_2004"]["odds_ratio"]-
               2.7768080308056233)<1e-10
    assert abs(result["size_shoot_plot_year_odds"]["all_1998_2004"]["odds_ratio"]-
               2.5908084543060723)<1e-10
    assert result["chronological_predictions"]["primary_shrinkage_20"][
        "pooled_all_three_future_years"]["n"]==13542
    if args.output:
        args.output.parent.mkdir(exist_ok=True,parents=True)
        args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    main_scores=result["chronological_predictions"]["primary_shrinkage_20"]
    print("HELICONIA_RECORD_MEMORY_TRANSFER: PASS")
    print(json.dumps({
        "source":provenance,
        "core_adj_OR":result["size_shoot_plot_year_odds"]["core_2001_2004"],
        "full_adj_OR":result["size_shoot_plot_year_odds"]["all_1998_2004"],
        "core_next_height_OR":result["size_shoot_plot_year_odds"]["core_with_next_height"],
        "core_finer_height_OR":result["size_shoot_plot_year_odds"]["core_finer_prior_height_bins"],
        "core_delete_year":{k:round(v["odds_ratio"],4)
                            for k,v in result["size_shoot_plot_year_odds"]["leave_one_year_out_core"].items()},
        "core_next_both_OR":result["size_shoot_plot_year_odds"]["core_with_next_height_and_shoots"],
        "yearwise":{k:round(v["odds_ratio"],4)
                   for k,v in result["size_shoot_plot_year_odds"]["by_year"].items()},
        "delete_ranch":{k:round(v["odds_ratio"],4)
                        for k,v in result["size_shoot_plot_year_odds"]["leave_one_ranch_out_core"].items()},
        "forward_primary":main_scores["pooled_all_three_future_years"],
        "forward_by_previous_record":main_scores["by_prior_flowering_record"],
        "forward_ranches":main_scores["by_ranch"],
        "n_heldout_plots_where_memory_improves_brier":sum(
            z["brier_gain_from_past_flower"]>0 for z in main_scores["by_plot"].values()
        ),
        "n_heldout_plots":len(main_scores["by_plot"]),
        "forward_years":main_scores["by_held_future_year"],
        "forward_shrinkage":result["chronological_predictions"]["shrinkage_sensitivity"],
    },indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
