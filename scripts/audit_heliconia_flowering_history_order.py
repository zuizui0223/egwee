#!/usr/bin/env python3
"""Does the ORDER of a two-year Heliconia flowering history matter?

Compare the outcome after [0,1] vs [1,0], holding number of previous
recorded flowering years (=1) fixed. This separates short-lag recency from
a simple stable-propensity interpretation more sharply than lag-1 OR alone.

Both cleaned archive and ORIGINAL entered numeric 0/positive categories are
audited using pinned blobs. Exploratory post hoc within one published system.
No causal, p-value, ecological memory law or frozen EGWEE corpus admission.
"""
from __future__ import annotations
import argparse
import csv
import io
import json
from collections import Counter, defaultdict
from pathlib import Path

from analyze_heliconia_census_panel import load_csv
from audit_heliconia_raw_inflor_zero_provenance import (
    PLOTS, MAP, get_raw, normalize_tag, subplot, raw_category
)

MIDDLE_YEARS = tuple(range(1999, 2005))
CORE_YEARS = tuple(range(2001, 2005))
RANCH = {"CF-1": "esteio", "CF-2": "esteio", "CF-3": "esteio",
         "FF-1": "dimona", "FF-2": "dimona", "FF-3": "esteio",
         "FF-4": "porto alegre", "FF-5": "dimona", "FF-6": "esteio",
         "FF-7": "porto alegre"}

def categories_from_raw(raw: bytes) -> tuple[dict, dict]:
    text = raw.decode("latin-1")  # source free-text has Latin-1 bytes
    data = list(csv.DictReader(io.StringIO(text)))
    index = defaultdict(list)
    for z in data:
        p = MAP.get(z["PLOT"].strip())
        if p not in PLOTS:
            continue
        tag = normalize_tag(z["Tag_Number"])
        sub = subplot(z["Row"], z["Column"])
        if tag and sub:
            index[(p,tag,sub)].append(z)
    unique = {k:v[0] for k,v in index.items() if len(v)==1}
    return unique, {
        "original_source_rows":len(data),
        "unique_original_plot_tag_subplot_keys":len(unique),
        "ambiguous_original_keys":sum(len(v)>1 for v in index.values()),
    }

def build_rows(archive: list[dict], unique_raw: dict) -> tuple[dict,dict]:
    records = defaultdict(dict)
    keys = set()
    tallies = Counter()
    for x in archive:
        p = x["plot_id"]
        year = int(x["year"])
        if p not in PLOTS or not 1998 <= year <= 2005:
            continue
        ident = (p,x["plant_id"])
        assert (p,x["plant_id"],year) not in keys
        keys.add((p,x["plant_id"],year))
        if x["census_status"] not in {"measured","dead","missing"}:
            raise AssertionError(x["census_status"])
        raw_tag = normalize_tag(x["tag_number"])
        src_key = (p,raw_tag,x["subplot"].strip().upper())
        src = unique_raw.get(src_key)
        kind = raw_category(src.get(f"INFL_{year}")) if src else "unlinked"
        original_binary = (int(kind=="positive") if kind in {"zero","positive"} else None)
        clean_positive = x["infl"].strip() not in {"NA",""}
        if clean_positive:
            assert float(x["infl"])>0
        agreement = original_binary is not None and original_binary==int(clean_positive)
        if x["census_status"]=="measured" and original_binary is not None:
            tallies["direct_raw_numeric"]=tallies["direct_raw_numeric"]+1
            if not agreement:
                tallies["raw_clean_conflict"]+=1
        height = x["ht"].strip()
        shoot = x["shts"].strip()
        records[ident][year] = {
            "alive": x["census_status"]=="measured",
            "clean_positive":int(clean_positive),
            "raw_numeric_positive":original_binary if agreement else None,
            "raw_source_key":src_key if agreement else None,
            "height": None if height in {"NA",""} else float(height),
            "shoots": None if shoot in {"NA",""} else float(shoot),
        }
    out={}
    for source in ("clean", "raw_confirmed", "raw_stable_key"):
        rows=[]
        for (p, ident), byyear in records.items():
            for t in MIDDLE_YEARS:
                a,b,c=(byyear.get(t-1),byyear.get(t),byyear.get(t+1))
                if not a or not b or not c or not all(z["alive"] for z in (a,b,c)):
                    continue
                if b["height"] is None or b["shoots"] is None:
                    continue
                assert b["height"] >= 0 and b["shoots"] >= 0
                if source=="clean":
                    bits=[a["clean_positive"],b["clean_positive"],c["clean_positive"]]
                else:
                    bits=[a["raw_numeric_positive"],b["raw_numeric_positive"],
                          c["raw_numeric_positive"]]
                    if any(z is None for z in bits):
                        continue
                    if source=="raw_stable_key":
                        if len({a["raw_source_key"],b["raw_source_key"],
                                c["raw_source_key"]})!=1:
                            continue
                if bits[0]+bits[1]!=1:
                    continue
                rows.append({
                    "plot":p,"ranch":RANCH[p],"year":t,
                    "height25":min(int(b["height"]//25),5),
                    "height10":min(int(b["height"]//10),20),
                    "shoot":0 if b["shoots"]<3 else 1 if b["shoots"]<5 else 2 if b["shoots"]<8 else 3,
                    "recent":bits[1], "old":bits[0], "next":bits[2],
                })
        out[source]=rows
        assert len({(x["plot"],x["year"]) for x in rows}) > 35, source
    return out,{
        "verified_clean_source_plant_years":len(archive),
        "n_archive_plant_years_in_restricted_plots":len(keys),
        "raw_original_matching_counters":dict(tallies),
    }

def summarize(rows: list[dict], fine_height: bool=False) -> dict:
    if not rows:
        return {"n":0, "common_odds_ratio":None}
    cells=defaultdict(lambda: [0,0,0,0])  # d,c,b,a
    n_recent=n_distant=pos_recent=pos_distant=0
    for r in rows:
        label = (r["plot"],r["year"],r["height10" if fine_height else "height25"],r["shoot"])
        cell=cells[label]
        cell[2*r["recent"]+r["next"]]+=1
        if r["recent"]:
            n_recent+=1
            pos_recent+=r["next"]
        else:
            n_distant+=1
            pos_distant+=r["next"]
    numerator=denominator=0.
    informative=0
    for d,c,b,a in cells.values():
        n=a+b+c+d
        numerator+=a*d/n
        denominator+=b*c/n
        informative+=int(min(a+b,c+d,a+c,b+d)>0)
    return {
        "n":len(rows),
        "recent_sequence_01_n":n_recent,
        "recent_sequence_01_next_positive":pos_recent,
        "distant_sequence_10_n":n_distant,
        "distant_sequence_10_next_positive":pos_distant,
        "next_positive_risk_recent_01":pos_recent/n_recent if n_recent else None,
        "next_positive_risk_distant_10":pos_distant/n_distant if n_distant else None,
        "common_odds_ratio":numerator/denominator if denominator else None,
        "n_plot_year_size_shoot_strata":len(cells),
        "n_informative_strata":informative,
    }

def analyze(rows: list[dict]) -> dict:
    core=[r for r in rows if r["year"] in CORE_YEARS]
    ret={
        "all_middle_years_1999_2004":summarize(rows),
        "core_middle_years_2001_2004":summarize(core),
        "core_height_10cm":summarize(core,fine_height=True),
        "per_middle_year":{str(y):summarize([r for r in rows if r["year"]==y])
                           for y in MIDDLE_YEARS},
        "core_leave_one_middle_year_out":{
            str(y):summarize([r for r in core if r["year"]!=y]) for y in CORE_YEARS
        },
        "core_leave_one_ranch_out":{
            ranch:summarize([r for r in core if r["ranch"]!=ranch])
            for ranch in sorted({r["ranch"] for r in core})
        },
        "core_by_ranch":{
            ranch:summarize([r for r in core if r["ranch"]==ranch])
            for ranch in sorted({r["ranch"] for r in core})
        },
    }
    return ret

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--local-raw",type=Path)
    parser.add_argument("--local-archive",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    archive=load_csv("HDP_survey.csv",args.local_archive)
    assert len(archive)==66396
    index,raw_profile=categories_from_raw(get_raw(args.local_raw))
    rows,counts=build_rows(archive,index)
    result={
        "status":"EXPLORATORY_TRIPLE_YEAR_ORDER_NOT_A_CAUSAL_MEMORY_IDENTIFICATION",
        "source_raw_linkage":raw_profile,"source_archive":counts,
        "analysis":{name:analyze(v) for name,v in rows.items()},
        "interpretation_ceiling":[
            "Only plants alive/measured in all three years are included; selection on survival can bias the pattern.",
            "Previous two-year history is fixed to exactly ONE recorded positive: [0,1] vs [1,0].",
            "Under conditionally independent Bernoulli flowering with a time-invariant individual logistic intercept and additive calendar-year intercept, history order among exactly-one-positive histories has no selection on the individual intercept. This is a sharp null under restrictive assumptions, not a proof of physiology.",
            "Year, plot, prior size and shoot are stratified; time-varying unmeasured plant resources and observation effort remain possible.",
            "The post hoc Mantel-Haenszel odds ratio is descriptive; none of the multiple overlapping individual-year contrasts are independent landscape replicates.",
            "Original entered numeric 0 is stronger record provenance than cleaned NA but still cannot certify inflorescence detection completeness.",
            "Unique raw plot/tag/subplot matches and raw-stable-key sensitivities are selected provenance samples, not independent confirmations.",
            "No lag can be selected as a true physiological memory duration without external prospective data.",
            "No frozen EGWEE effect study/programme/corpus denominator is altered.",
        ]
    }
    # Source-identity fingerprints and algebraic tested cohort size.
    assert len(rows["clean"]) > 800
    assert len(rows["raw_confirmed"]) > 500
    assert all(v["n"] == (v["recent_sequence_01_n"]+v["distant_sequence_10_n"])
               for obj in result["analysis"].values()
               for k,v in obj.items() if k in {
                   "all_middle_years_1999_2004","core_middle_years_2001_2004"
               })
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("HELICONIA_FLOWERING_HISTORY_ORDER: PASS")
    print(json.dumps({
        "source":{**raw_profile,**counts},
        "results":{k:{
            "all":v["all_middle_years_1999_2004"],
            "core":v["core_middle_years_2001_2004"],
            "fine_height_core":v["core_height_10cm"],
            "by_year":{yr:{"n":z["n"],"OR":z["common_odds_ratio"]}
                       for yr,z in v["per_middle_year"].items()},
            "leave_year_core":{yr:z["common_odds_ratio"]
                               for yr,z in v["core_leave_one_middle_year_out"].items()},
            "leave_ranch_core":{r:z["common_odds_ratio"]
                                for r,z in v["core_leave_one_ranch_out"].items()},
        } for k,v in result["analysis"].items()}
    },indent=2,ensure_ascii=False))

if __name__ == "__main__":
    main()
