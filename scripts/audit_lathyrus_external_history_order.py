#!/usr/bin/env python3
"""Independent Lathyrus four-year flowering order test from lefko3 original data.

External Swedish temperate perennial population, not Heliconia, not a frozen
EGWEE effect/programme. RData copied via pinned upstream GitHub commit and Git
blob hash, read with pyreadr; explicit FCODE and observed above-ground volume.
This is a diagnostic of transportability of the order-comparison design.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path
import tempfile
import urllib.request

REPO="dormancy1/lefko3"
UPSTREAM_COMMIT="1ddb6092e5e4f1f401432b594ee49bb7aac2c627"
BLOB_SHA="c014e2728734eb83990f5511669030001a939fb3"
URL=f"https://raw.githubusercontent.com/{REPO}/{UPSTREAM_COMMIT}/data/lathyrus.rda"
YEARS=(1988,1989,1990,1991)

def load_pinned(local_rda: Path | None):
    try:
        import pyreadr
    except ImportError as exc:
        raise RuntimeError("Install pyreadr for reading the pinned RData source") from exc
    if local_rda:
        source=local_rda.read_bytes()
    else:
        request=urllib.request.Request(URL,headers={"User-Agent":"EGWEE-external-Lathyrus-raw/1"})
        with urllib.request.urlopen(request,timeout=45) as response:
            assert response.status==200
            source=response.read()
    git_blob=hashlib.sha1(f"blob {len(source)}\0".encode()+source).hexdigest()
    assert git_blob==BLOB_SHA,(git_blob,BLOB_SHA)
    with tempfile.TemporaryDirectory() as tmp:
        fn=Path(tmp)/"lathyrus.rda"
        fn.write_bytes(source)
        items=pyreadr.read_r(str(fn))
    assert "lathyrus" in items, list(items)
    df=items["lathyrus"]
    assert len(df)==1119, (len(df),list(df.columns))
    fields={"SUBPLOT","GENET"}|{f"FCODE{y%100:02d}" for y in YEARS}|{
        f"Volume{y%100:02d}" for y in YEARS}
    assert fields <= set(df.columns),sorted(fields-set(df.columns))
    return df,{
        "repo":REPO,"upstream_commit":UPSTREAM_COMMIT,
        "original_git_blob_sha":BLOB_SHA,"source_url":URL,
        "source_bytes":len(source),"source_rows":len(df),
        "source_columns":list(df.columns),
    }

def numeric(v):
    if v is None:
        return None
    try:
        x=float(v)
    except (ValueError,TypeError):
        return None
    return x if math.isfinite(x) else None

def year_state(df):
    plants={}
    for _,r in df.iterrows():
        plot,ident=str(r["SUBPLOT"]),str(r["GENET"])
        key=(plot,ident)
        assert key not in plants,key
        vals={}
        for year in YEARS:
            abbrev=year%100
            volume=numeric(r[f"Volume{abbrev:02d}"])
            fl=numeric(r[f"FCODE{abbrev:02d}"])
            alive=volume is not None and volume>0 and fl in (0.,1.)
            vals[year]={"volume":volume,"flowering":int(fl) if fl in (0.,1.) else None,
                        "confirmed_aboveground_and_fcode":alive}
        plants[key]=vals
    return plants

def mh(rows, exposure: str, group_size: int = 2) -> dict:
    cells=defaultdict(lambda:[0,0,0,0])
    one=yes=zero_no=zero_yes=0
    for x in rows:
        a=int(x[exposure])
        y=int(x["next"])
        key=(x["plot"],x["middle_year"],x["size_bin"])
        cells[key][2*a+y]+=1
        if a:
            one+=1;yes+=y
        else:
            zero_no+=1;zero_yes+=y
    num=den=0.
    info=0
    for d,c,b,a in cells.values():
        n=a+b+c+d
        num+=a*d/n
        den+=b*c/n
        info+=int(min(a+b,c+d,a+c,b+d)>0)
    return {
        "n":len(rows),"n_exposed":one,"n_unexposed":zero_no,
        "next_positive_exposed":yes,"next_positive_unexposed":zero_yes,
        "risk_exposed":yes/one if one else None,
        "risk_unexposed":zero_yes/zero_no if zero_no else None,
        "mh_or":num/den if den else None,
        "n_informative_plot_year_volume_strata":info,
        "n_total_strata":len(cells),
    }

def audit(df):
    plants=year_state(df)
    two=[]
    three=[]
    eligible=defaultdict(int)
    for (plot,ident),observations in plants.items():
        for old,now in zip(YEARS,YEARS[1:]):
            a,b=observations[old],observations[now]
            if not(a["confirmed_aboveground_and_fcode"] and
                   b["confirmed_aboveground_and_fcode"]):
                continue
            prior_volume=a["volume"]
            size_bin=min(int(math.log1p(prior_volume)//2),7)
            two.append({"plot":plot,"middle_year":old,
                        "size_bin":size_bin,"prev":a["flowering"],"next":b["flowering"]})
        for t in (1989,1990):
            a,b,c=[observations[z] for z in (t-1,t,t+1)]
            if not all(v["confirmed_aboveground_and_fcode"] for v in (a,b,c)):
                continue
            eligible["observed_three_year"]=eligible["observed_three_year"]+1
            if a["flowering"]+b["flowering"]!=1:
                continue
            size_bin=min(int(math.log1p(b["volume"])//2),7)
            three.append({"plot":plot,"middle_year":t,
                          "size_bin":size_bin,"recent":b["flowering"],
                          "next":c["flowering"]})
    assert len(plants)==1119
    result={
        "status":"EXTERNAL_LATHYRUS_FOUR_YEAR_ORDER_DESCRIPTIVE_NOT_NEW_LAW",
        "n_individuals":len(plants),
        "n_subplots":len({k[0] for k in plants}),
        "n_pair_years_measured":len(two),
        "one_lag_association":mh(two,"prev"),
        "n_three_year_triples":eligible["observed_three_year"],
        "n_unequal_history_triples":len(three),
        "recency_history_order":mh(three,"recent"),
        "one_lag_by_calendar_pair":{
            str(t):mh([r for r in two if r["middle_year"]==t],"prev")
            for t in (1988,1989,1990)
        },
        "order_by_middle_year":{
            str(t):mh([r for r in three if r["middle_year"]==t],"recent")
            for t in (1989,1990)
        },
        "interpretive_limits":[
            "This is a Swedish perennial Lathyrus vernus study (1988-1991), biologically independent of Brazilian Heliconia but not a second Heliconia source.",
            "Only four calendar years and two three-year history windows; no independent future-year training/test series is claimed.",
            "Flowering code 0/1 is explicit in the R package; aboveground positive volume in each relevant year is required; dormancy and missing are excluded.",
            "An above-ground measured plant can have flowering measurement error even when FCODE is numeric.",
            "The analysis reuses an already published perennial study and cannot discover general plant reproductive memory.",
            "Calendar years and subplot/size strata do not randomize reproductive history; latent vigor and resource storage remain possible.",
            "MH odds ratios are descriptive; only an independent study population, not 1119 independent landscape tests.",
            "This external audit is not a fragmentation treatment contrast and does not enter any frozen EGWEE synthesis denominator."
        ]
    }
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--local-rda",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    df,pin=load_pinned(args.local_rda)
    result=audit(df)
    result["source_provenance"]=pin
    if args.output:
        args.output.parent.mkdir(exist_ok=True,parents=True)
        args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("LATHYRUS_EXTERNAL_FLOWERING_HISTORY_ORDER: PASS")
    print(json.dumps({
        k:v for k,v in result.items() if k not in ("source_provenance","interpretive_limits")
    },indent=2))

if __name__=="__main__":
    main()
