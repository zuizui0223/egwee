#!/usr/bin/env python3
"""ECH03A: frozen within-programme site-heldout test of joint mating opportunity."""
import csv,hashlib,io,json,math,random,statistics,subprocess
from collections import Counter
from pathlib import Path
from audit_echinacea_longterm_sources import get,js
from run_camp01_fixed_site_holdout import solve

ROOT=Path(__file__).resolve().parents[2]
LOCK="f07b86e04cc77c869dc5f28e5a80c684ebe924c0"
SHA="28911e8c2a83bddbb75124dfcb0bf12add21c199b54bc3e308a41c47bf3fa675"
YEAR=(2014,2015,2016,2020,2021,2022)
FIELDS=("census","propFl","meanSync","nn7.hmean","meanOMP","meanSdSet")
MISSING={"","na","nan","n/a","null","none"}
class Stop(Exception):pass
def val(r,k):
    s=str(r.get(k,"")).strip()
    if s.lower() in MISSING:return None
    x=float(s)
    if not math.isfinite(x) or x<0:raise Stop("INVALID_NUMERIC_"+k)
    if k in ("propFl","meanSync","meanOMP","meanSdSet") and x>1:raise Stop("PROPORTION_OUT_OF_RANGE_"+k)
    if k=="census" and x!=int(x):raise Stop("NONINTEGER_CENSUS")
    return x
def prepare(rows):
    seen=set();sites=set();years=set();miss=Counter();nseed=0;records=[]
    for r in rows:
        site=r["burnSite"].strip();year=int(r["year"]);burn=r["burned"].strip()
        if not site or year not in YEAR or burn not in {"Burned","Unburned"}:raise Stop("DESIGN_LABEL_INVALID")
        key=(site,year)
        if key in seen:raise Stop("DUPLICATE_SCENE")
        seen.add(key);sites.add(site);years.add(year)
        v=[val(r,k) for k in FIELDS]
        if v[-1] is not None:nseed+=1
        for k,x in zip(FIELDS,v):
            if x is None:miss[k]+=1
        if any(x is None for x in v):continue
        c,p,s,dist,omp,y=v
        records.append((site,year,float(burn=="Burned"),math.log1p(c),p,s,math.log1p(dist),omp,y))
    if len(rows)!=210 or len(sites)!=35 or years!=set(YEAR) or nseed!=152:raise Stop("PINNED_DESIGN_COUNTS_MISMATCH")
    if len(records)<100 or len({r[0] for r in records})<25 or len({r[-1] for r in records})<2:raise Stop("INSUFFICIENT_FIXED_SUPPORT")
    return records,{"source_rows":len(rows),"source_sites":len(sites),"source_years":len(years),"seed_observed":nseed,
                    "complete_scenes":len(records),"complete_sites":len({r[0] for r in records}),"missing_by_field":dict(miss),
                    "excluded_scene_count":len(rows)-len(records)}
def fit(train,test,add):
    mu=[statistics.mean(r[i] for r in train) for i in range(3,8)]
    sd=[statistics.pstdev(r[i] for r in train) for i in range(3,8)]
    def x(r):
        c,p,s,d,o=[(r[i]-m)/v if v>1e-12 else 0. for i,m,v in zip(range(3,8),mu,sd)]
        z=[1.,r[2],c,r[2]*c,p,s,d,s*d]+[float(r[1]==y) for y in YEAR[1:]]
        if add:z.append(o)
        return z
    X=[x(r) for r in train];dim=len(X[0]);A=[[0.]*dim for _ in range(dim)];b=[0.]*dim
    for z,r in zip(X,train):
        for i in range(dim):
            b[i]+=z[i]*r[-1]
            for j in range(dim):A[i][j]+=z[i]*z[j]
    for i in range(1,dim):A[i][i]+=1.
    beta=solve(A,b)
    return [min(1.,max(0.,sum(v*w for v,w in zip(x(r),beta)))) for r in test]
def evaluate(rs):
    sites=sorted({r[0] for r in rs});folds=[]
    for i,s in enumerate(sites):
        tr=[r for r in rs if r[0]!=s];te=[r for r in rs if r[0]==s]
        p0=fit(tr,te,False);p1=fit(tr,te,True)
        e0=sum((r[-1]-p)**2 for r,p in zip(te,p0));e1=sum((r[-1]-p)**2 for r,p in zip(te,p1))
        n=len(te);folds.append({"fold":i,"n":n,"M0_MSE":e0/n,"M1_MSE":e1/n,"gain":(e0-e1)/n})
    n=sum(f["n"] for f in folds)
    m0=sum(f["M0_MSE"]*f["n"] for f in folds)/n
    m1=sum(f["M1_MSE"]*f["n"] for f in folds)/n
    g=m0-m1;wins=sum(f["gain"]>0 for f in folds);rng=random.Random(20261126);boot=[]
    for _ in range(1000):
        draw=rng.choices(folds,k=len(folds))
        boot.append(sum(f["gain"]*f["n"] for f in draw)/sum(f["n"] for f in draw))
    boot.sort()
    return {"M0_MSE":m0,"M1_MSE":m1,"gain":g,"relative_mse_reduction":g/m0 if m0 else None,"site_folds":len(sites),
            "positive_site_folds":wins,"equal_site_mean_gain":statistics.mean(f["gain"] for f in folds),
            "fixed_residual_site_bootstrap_95pct":[boot[24],boot[975]],"folds":folds,
            "decision":"JOINT_OMP_PREDICTIVE_INCREMENT" if g>0 and wins/len(sites)>=.7 else "NO_SUPPORTED_JOINT_OMP_INCREMENT"}
def run():
    d={"protocol":LOCK,"source_sha256":SHA,"original_individual_rows_exported":False,
       "new_molecular_GxIxF_validation":False,"causal_intervention_claim":False,
       "independent_species_confirmation":False}
    try:
        subprocess.run(["git","merge-base","--is-ancestor",LOCK,"HEAD"],cwd=ROOT,check=True)
        m=js("https://api.figshare.com/v2/articles/23994528")
        if m["id"]!=23994528 or m["doi"]!="10.6084/m9.figshare.23994528.v1":raise Stop("SOURCE_VERSION_MISMATCH")
        f=[f for f in m["files"] if f["name"]=="burnRemsPopData.csv"]
        if len(f)!=1:raise Stop("SOURCE_FILE_NOT_UNIQUE")
        raw,_=get(f[0]["download_url"])
        if hashlib.sha256(raw).hexdigest()!=SHA:raise Stop("ORIGINAL_FILE_SHA_CHANGED")
        rr=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
        rs,info=prepare(rr);d.update(info);d.update(evaluate(rs))
        d["status"]="ECH03A_SITE_HOLDOUT_COMPLETE"
    except Exception as e:
        d.update(status="ECH03A_SOURCE_OR_MODEL_STOP",reason=str(e)[:120] if isinstance(e,Stop) else type(e).__name__,decision="NOT_EVALUATED")
    return d
if __name__=="__main__":print(json.dumps(run(),indent=2))
