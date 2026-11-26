#!/usr/bin/env python3
"""CAMP01A: source-only amended, label-invariant site-held-out predictive comparison."""
from collections import defaultdict
import hashlib,json,math,statistics,subprocess
import run_camp01_fixed_site_holdout as base

LOCK="7d7d8a01ba051f291493f096a6c86d07a28dc428"
SHA={"PLdataindividual.csv":"8a2a38a6552126273a83873e317ee68e1472231e19a8090436006736e30053c3",
     "pollinator.csv":"51101f4705b436cd75d21643910bb1fd611df4e71701918e0dcec24c07b009d5"}
def join(seed,poll,d):
    s=defaultdict(list);p={}
    for r in seed:s[base.key(r)].append(r)
    for r in poll:
        k=base.key(r)
        if k in p:raise base.Stop("DUPLICATE_POLL_KEY")
        p[k]=r
    if len(s)!=53 or len(p)!=56 or len(set(s)&set(p))!=53:raise base.Stop("RECONCILED_SOURCE_COUNTS_CHANGED")
    paired=[];excluded_dates=0;excluded_no_pair=0;excluded_visit=0
    miss_seed=0;npaired=0;unpaired=0;zero_seeds=0
    for k,rows in s.items():
        pr=p[k];des=base.design(pr)
        if any(base.design(r)!=des for r in rows):raise base.Stop("DESIGN_CONFLICT")
        ds={r.get("date_initiated","").strip() for r in rows}
        date=pr.get("start_date","").strip()
        if not date or ds!={date}:excluded_dates+=1;continue
        plants=defaultdict(lambda:defaultdict(list))
        for r in rows:
            i=r.get("individual")
            if not i:raise base.Stop("MISSING_PLANT_ID")
            t=base.norm(r.get("treatment"))
            if t not in {"c","s"}:raise base.Stop("TREATMENT_LABEL_CHANGED")
            arm=plants[i][t]
            y=base.numeric(r["seednumber"],integer=True)
            if y is None:miss_seed+=1;continue
            if y==0:zero_seeds+=1
            arm.append(y)
        ds=[]
        for arm in plants.values():
            if not arm.get("c") or not arm.get("s"):unpaired+=1;continue
            npaired+=1
            ds.append(math.log1p(statistics.mean(arm["s"]))-math.log1p(statistics.mean(arm["c"])))
        if not ds:excluded_no_pair+=1;continue
        v=base.numeric(pr["visits_per_flower"])
        if v is None:excluded_visit+=1;continue
        paired.append((k[0],des[0],des[1],des[2],math.log1p(v),statistics.mean(ds)))
    if excluded_dates!=2:raise base.Stop("DATE_GATE_COUNT_CHANGED")
    d.update(seed_rows=len(seed),pollinator_rows=len(poll),matched_population_keys=53,pollinator_only_keys=3,
             date_unmatched_excluded=excluded_dates,matched_date_population_keys=51,
             no_paired_plant_excluded=excluded_no_pair,missing_visits_excluded=excluded_visit,
             paired_plants_in_date_matched_groups=npaired,unpaired_plants_in_date_matched_groups=unpaired,
             missing_seed_rows_in_date_matched_groups=miss_seed,observed_seed_zero_rows=zero_seeds,
             analysis_experimental_populations=len(paired),analysis_sites=len({r[0] for r in paired}),
             source_population_levels=len({r[1] for r in paired}))
    return paired
def run():
    d={"status":"PENDING","protocol":LOCK,"original_CAMP01_status":"SOURCE_OR_SUPPORT_STOP",
       "treatment_labels_semantically_verified":False,"response_sign_invariant_squared_error_comparison":True,
       "causal_visitation_effect_claimed":False,"molecular_GxIxF_validated":False,
       "raw_rows_redistributed":False,"result_is_independent_cross_species_confirmation":False}
    try:
        subprocess.run(["git","merge-base","--is-ancestor",LOCK,"HEAD"],cwd=base.ROOT,check=True)
        meta=json.loads(base.fetch("https://zenodo.org/api/records/"+base.REC,2_000_000))
        if str(meta.get("id"))!=base.REC or meta.get("doi")!=base.DOI:raise base.Stop("SOURCE_ID_CHANGED")
        mf={f.get("key"):f for f in meta.get("files",[])}
        if set(mf)!=set(SHA):raise base.Stop("SOURCE_FILES_CHANGED")
        tabs={}
        for fn,sha in SHA.items():
            links=mf[fn]["links"];raw=base.fetch(links.get("content") or links.get("self"),2_000_000)
            if hashlib.sha256(raw).hexdigest()!=sha:raise base.Stop("SOURCE_SHA_CHANGED")
            h,tabs[fn]=base.csvrows(raw)
        d["source_sha256"]=SHA
        records=join(tabs["PLdataindividual.csv"],tabs["pollinator.csv"],d)
        v=base.evaluate(records)
        # The sign of the coded S-C outcome is not interpreted biologically.
        for f in v["folds"]:f.pop("descriptive_interaction_coefficient",None)
        d.update(v);d["status"]="CAMP01A_SITE_HOLDOUT_COMPLETE"
    except (base.Stop,ValueError,KeyError,TypeError,IndexError,subprocess.CalledProcessError,base.HTTPError,base.URLError) as e:
        d["status"]="CAMP01A_SOURCE_OR_SUPPORT_STOP"
        d["reason"]=str(e)[:120] if isinstance(e,base.Stop) else type(e).__name__
        d["decision"]="NOT_IDENTIFIABLE_FROM_CURRENT_SOURCE"
    return d
if __name__=="__main__":print(json.dumps(run(),indent=2))
