#!/usr/bin/env python3
"""Empirical EGWEE GloPL complete within-experiment cross-endpoint sign audit.

Source Bennett et al. 2018, GloPL author repository raw data blob pinned by SHA.
No frozen fragmentation-denominator modification and no ecology-agnostic pooling.
Primary: FS (fruit-set proportion) versus SPFR (seeds per EXISTING fruit).
Cases are dependent within publications; a mean effect sign is not confirmed tradeoff.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"evidence/meta_extraction/glopl_2018/GloPL_with_id.csv"
BLOB="0809eaeee54e4375d26bacfe002787241f8ff72e"  # UTF-8-transcoded stored text; upstream legacy byte blob differs
FIELDS=("FS","SO","SPFR","SPFL","SPP")
PAIR=("FS","SPFR")

def load():
    raw=SOURCE.read_bytes()
    h=hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()
    assert h==BLOB,(len(raw),h)
    with SOURCE.open(encoding="utf-8-sig",newline="") as fh:
        records=list(csv.DictReader(fh))
    assert len(records)==2969
    assert len({r["unique_study_number"] for r in records})==927
    assert len({r["Species_accepted_names"] for r in records})==1265
    assert len({r["unique_number"] for r in records})==2969
    return records,h

def value(x):
    if x is None or x.strip() in {"","NA","NaN"}: return None
    try: return float(x)
    except ValueError: return None

def observed(row,endpoint):
    native=value(row[f"Natural_X_{endpoint}"])
    added=value(row[f"Sup_X_{endpoint}"])
    if native is None or added is None or native<0 or added<0:
        return None
    delta=added-native
    return {"natural":native,"supplement":added,"delta":delta,
            "sign":(1 if delta>0 else -1 if delta<0 else 0)}

def approx_z(row,endpoint):
    """Unknown within-plant arm-covariance: NOT a 95% resolved sign test."""
    d=observed(row,endpoint)
    if d is None: return None
    n0,n1,sd0,sd1=(
        value(row[f"{prefix}_{endpoint}"]) for prefix in
        ("Natural_N","Sup_N","Natural_SD","Sup_SD"))
    if any(x is None for x in (n0,n1,sd0,sd1)) or min(n0,n1)<=1 or min(sd0,sd1)<0:
        return None
    se=(sd0**2/n0 + sd1**2/n1)**0.5
    if se==0:
        return None # no support for deterministic sign certainty
    return float(abs(d["delta"])/se)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    parser.add_argument("--publication-csv",type=Path)
    parser.add_argument("--opposite-csv",type=Path)
    args=parser.parse_args()
    source, sha=load()
    endpoints={}
    for e in FIELDS:
        avail=[r for r in source if observed(r,e) is not None]
        endpoints[e]={
            "numeric_eligible":len(avail),
            "positive":sum(observed(r,e)["sign"]>0 for r in avail),
            "negative":sum(observed(r,e)["sign"]<0 for r in avail),
            "exact_zero":sum(observed(r,e)["sign"]==0 for r in avail)
        }
    mult=[r for r in source if sum(observed(r,e) is not None for e in FIELDS)>=2]
    paired=[r for r in source if all(observed(r,e) is not None for e in PAIR)]
    nonzero=[r for r in paired if all(observed(r,e)["sign"]!=0 for e in PAIR)]
    assert len(mult)==560 and len(paired)==344 and len(nonzero)==313
    assert len({r["unique_study_number"] for r in paired})==86

    cross=Counter()
    opposite=[]
    pubrows=defaultdict(list)
    bylevel=defaultdict(list)
    for r in nonzero:
        s1=observed(r,"FS")["sign"]
        s2=observed(r,"SPFR")["sign"]
        key=("+" if s1==1 else "-")+("+" if s2==1 else "-")
        cross[key]+=1
        mis=(s1!=s2)
        pubrows[r["unique_study_number"]].append(int(mis))
        bylevel[r["Level_of_Supplementation"]].append((r["unique_study_number"],int(mis)))
        if mis:
            opposite.append(r)
    assert cross=={ "++":205,"+-":48,"-+":33,"--":27 },cross
    pubs=set(pubrows)
    source_fracs={k:float(np.mean(v)) for k,v in pubrows.items()}
    n_opposite_pubs=len({r["unique_study_number"] for r in opposite})
    assert len(opposite)==81 and n_opposite_pubs==36
    assert len({r["Family"] for r in opposite})==28

    # Publication-balanced inference sensitivity: case fractions nested in studies.
    weights=list(source_fracs.values())
    source_equal_fraction=float(np.mean(weights))
    pub_los={}
    for p in pubs:
        pub_los[p]=float(np.mean([v for k,v in source_fracs.items() if k!=p]))
    # Publication-cluster bootstrap (post hoc uncertainty, not a causal population CI).
    rng=np.random.default_rng(20261019)
    v=np.asarray(weights)
    b=np.mean(v[rng.integers(0,len(v),size=(20000,len(v)))],axis=1)
    bootstrap_95=list(map(float,np.quantile(b,[0.025,0.975])))

    by_level={}
    for level, records in bylevel.items():
        pubslevel=defaultdict(list)
        for pub,mis in records:pubslevel[pub].append(mis)
        by_level[level]={
            "cases":len(records),
            "discordant_cases":sum(j for _,j in records),
            "publications":len(pubslevel),
            "case_weighted_fraction":float(np.mean([j for _,j in records])),
            "publication_equal_fraction":float(np.mean([
                np.mean(t) for t in pubslevel.values()]))
        }

    # Across same-case triples, not a comparison of disjoint response subsets.
    triple=[r for r in source if all(observed(r,e) is not None
             and observed(r,e)["sign"]!=0 for e in ("FS","SPFR","SPFL"))]
    triple_top=Counter("".join("+" if observed(r,e)["sign"]>0 else "-"
                       for e in ("FS","SPFR","SPFL")) for r in triple)
    assert len(triple)==44 and len({r["unique_study_number"] for r in triple})==9
    z_eligible=[r for r in opposite if all(approx_z(r,e) is not None for e in PAIR)]
    z_both=[r for r in z_eligible if all(approx_z(r,e)>=1.96 for e in PAIR)]
    assert len(z_eligible)==78 and len(z_both)==4
    # Detection status is explicitly NOT nominally certified, as treatment
    # groups may be within the same plant and the published N/SD are heterogeneous.

    pubfile=[]
    for pub in sorted(pubs,key=lambda z:int(z)):
        pr=[r for r in nonzero if r["unique_study_number"]==pub]
        mis=[r for r in pr if observed(r,"FS")["sign"]!=observed(r,"SPFR")["sign"]]
        pubfile.append({
            "publication_id":pub,"author":pr[0]["Author"],"publication_year":pr[0]["Year"],
            "n_cases_with_two_nonzero_contrasts":len(pr),
            "n_opposite_point_contrasts":len(mis),
            "fraction_opposite":len(mis)/len(pr),
            "families": ";".join(sorted({r["Family"] for r in pr}))
        })
    oppfile=[]
    for r in opposite:
        oppfile.append({
            "case_id":r["unique_number"],"publication_id":r["unique_study_number"],
            "author":r["Author"],"year":r["Year"],"species":r["Species_accepted_names"],
            "family":r["Family"],"supplementation_level":r["Level_of_Supplementation"],
            "fruit_set_natural":observed(r,"FS")["natural"],
            "fruit_set_supp":observed(r,"FS")["supplement"],
            "seeds_per_existing_fruit_natural":observed(r,"SPFR")["natural"],
            "seeds_per_existing_fruit_supp":observed(r,"SPFR")["supplement"],
            "approx_z_FS":approx_z(r,"FS"),"approx_z_SPFR":approx_z(r,"SPFR")
        })
    if args.publication_csv:
        args.publication_csv.parent.mkdir(parents=True,exist_ok=True)
        with args.publication_csv.open("w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=list(pubfile[0]))
            writer.writeheader();writer.writerows(pubfile)
    if args.opposite_csv:
        args.opposite_csv.parent.mkdir(parents=True,exist_ok=True)
        with args.opposite_csv.open("w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=list(oppfile[0]))
            writer.writeheader();writer.writerows(oppfile)

    result={
        "status":"retrospective_descriptive_point_sign_topology",
        "dataset":"Bennett et al 2018 GloPL",
        "source_blob_sha":sha,
        "case_counts":{"all":len(source),"studies":927,"species":1265,
                       "multi_endpoint":len(mult),"multi_endpoint_sources":
                       len({r["unique_study_number"] for r in mult})},
        "endpoints":endpoints,
        "FS_SPFR":{
            "eligible_with_any_zero":len(paired),
            "publications_with_any_zero":len({r["unique_study_number"] for r in paired}),
            "both_nonzero":len(nonzero),
            "publications_nonzero":len(pubs),
            "table":dict(cross),
            "opposite":len(opposite),
            "opposite_publications":n_opposite_pubs,
            "opposite_families":len({r["Family"] for r in opposite}),
            "case_weighted_fraction":len(opposite)/len(nonzero),
            "publication_equal_fraction":source_equal_fraction,
            "publication_cluster_bootstrap_percentile95":bootstrap_95,
            "leave_one_publication_equal_fraction_range":
                [min(pub_los.values()),max(pub_los.values())],
            "both_marginal_z_approx_available":len(z_eligible),
            "both_marginal_z_approx_atleast196":len(z_both),
            "both_marginal_z_approx_atleast196_publications":
                len({r["unique_study_number"] for r in z_both}),
            "caution":"N and SD are not a covariance-complete design; z >= 1.96 is only a rough screen, not a joint 95%-resolved biological sign reversal"
        },
        "same_case_FS_SPFR_SPFL":{
            "eligible_three_nonzero":len(triple),
            "publications":len({r["unique_study_number"] for r in triple}),
            "direction_table":dict(triple_top)
        },
        "supplementation_level":by_level,
        "interpretation": "multi-stage reproductive output can show opposite source mean changes under one pollen addition experimental frame; GloPL is not a fragmentation experimental replication",
        "frozen_5_8_16_denominators_changed":False,
    }
    assert all(x<=1 for x in bootstrap_95)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",
                               encoding="utf-8")
    print("GLOPL_SOURCE_BLOB_OK",sha,"cases",len(source),"publications",927,
          "species",1265)
    print("GLOPL_MULTILAYER",len(mult),"published_sources",
          result["case_counts"]["multi_endpoint_sources"])
    print("GLOPL_FS_SPFR",len(paired),len(nonzero),dict(cross),
          "opposite",len(opposite),"source",n_opposite_pubs,"family",
          result["FS_SPFR"]["opposite_families"])
    print("GLOPL_STUDY_BALANCED",
          source_equal_fraction,bootstrap_95,
          result["FS_SPFR"]["leave_one_publication_equal_fraction_range"])
    print("GLOPL_Z_SCREEN_UNCERTAIN",len(z_eligible),len(z_both),
          "distinct_sources",result["FS_SPFR"]["both_marginal_z_approx_atleast196_publications"])
    print("GLOPL_TRIPLE",len(triple),dict(triple_top))
    print("GLOPL_LEVEL",json.dumps(by_level,sort_keys=True))


if __name__=="__main__":
    main()
