#!/usr/bin/env python3
"""Frozen ECH01A family holdout. No raw records, coordinates or IDs in outputs."""
import hashlib,json,math,random,re,statistics,subprocess
from pathlib import Path
from collections import Counter
from audit_echinacea_author_semantics import official_drum,pinned,rows
from audit_echinacea_longterm_sources import HANDLES
from run_camp01_fixed_site_holdout import solve

ROOT=Path(__file__).resolve().parents[2]
LOCK="4e495ab61ac5057f02c5578c769975854dbe7b00"
HASHES={"offspring_fitness_data.csv":"7e5bcc2a9fab0b559cae58c2cfeaba11d50cd2d2f445159939bf0f6e54a6c7a6",
        "fitness_predictors.csv":"d3d1d4ab1c95ba872995873af13f10ebcd44a8a2af5dcd4259967f792191b3fd",
        "readme.txt":"553e6bf732740079b3bf43e78ea1837426d779c99730b876ff13d5ebf2d291b8",
        "analysis_code.R":"9dc236bf711ca8868c3e4ec56dcf9e02f090db467b18c66ab28805667608cf6a"}
YRS=tuple(range(2009,2018))+(2019,2020,2021,2022)
CATS=("bot","head","t2","top")
MISS={"","na","nan","n/a","null","none"}
class Stop(Exception):pass
def clean(v):return str(v if v is not None else "").strip()
def ismiss(v):return clean(v).lower() in MISS
def num(v,k):
    if ismiss(v):raise Stop("MISSING_"+k)
    try:x=float(v)
    except ValueError:raise Stop("NONNUMERIC_"+k)
    if not math.isfinite(x):raise Stop("NONFINITE_"+k)
    return x
def prepare(f,p,author_code):
    if len(f)!=3961 or len(p)!=438:raise Stop("SOURCE_ROW_COUNT")
    by={clean(r["cgPlaId"]):r.copy() for r in f}
    if len(by)!=len(f) or len({clean(r["cgPlaId"]) for r in p})!=438:raise Stop("DUPLICATE_SOURCE_KEY")
    if any(clean(r["cgPlaId"]) not in by for r in p):raise Stop("UNMATCHED_OFFSPRING")
    fields=("ld2022","fl2022","hdCt2022")
    # Require the author-published exact, single-record correction, not an assumed zero.
    corrected=[]
    for fld in fields:
        hits=re.findall(r"\b"+fld+r"\s*=\s*case_when\(cgPlaId\s*==\s*(\d+)\s*~\s*0\s*,",author_code)
        if len(hits)!=1:raise Stop("AUTHOR_CORRECTION_NOT_VERIFIED_"+fld)
        corrected.append(hits[0])
    if len(set(corrected))!=1:raise Stop("AUTHOR_CORRECTION_ID_INCONSISTENT")
    corrected_id=corrected[0]
    matchids={clean(r["cgPlaId"]) for r in p}
    if corrected_id not in matchids:raise Stop("AUTHOR_CORRECTION_NOT_IN_MATCHED_COHORT")
    missing_final={i for i in matchids if any(ismiss(by[i][k]) for k in fields)}
    if missing_final!={corrected_id}:raise Stop("FINAL_MISSING_PATTERN_CHANGED")
    for fld in fields:
        if not ismiss(by[corrected_id][fld]) and num(by[corrected_id][fld],fld)!=0:
            raise Stop("AUTHOR_CORRECTION_CONTRADICTS_SOURCE")
        by[corrected_id][fld]="0"
    rec=[];n_no_dist=0;fl_head_discord=0;death_head_discord=0
    for r in p:
        a=by[clean(r["cgPlaId"])]
        if ismiss(r["parentDist"]):
            if not ismiss(r["popCd.sire"]):raise Stop("DISTANCE_MISSING_WITH_KNOWN_SIRE_POP")
            n_no_dist+=1;continue
        dam,sire=clean(r["cgPlaId.dam"]),clean(r["cgPlaId.sire"])
        if ismiss(dam) or ismiss(sire):raise Stop("PARENT_ID_MISSING")
        dist=num(r["parentDist"],"parentDist");delta=num(r["diffStartDir"],"diffStartDir")
        if not 0<=dist<=9014 or not -13<=delta<=12:raise Stop("PUBLISHED_RANGE_MISMATCH")
        fruit=clean(r["ach_pos"])
        if fruit not in CATS:raise Stop("UNKNOWN_FRUIT_POSITION")
        alive=num(a["ld2022"],"ld2022")
        if alive not in (0,1):raise Stop("INVALID_ALIVE")
        counts=[]
        for yr in YRS:
            x=num(a[f"hdCt{yr}"],"hdCt");l=num(a[f"ld{yr}"],"ld");fl=num(a[f"fl{yr}"],"fl")
            if x<0 or x!=int(x) or l not in (0,1) or fl not in (0,1):raise Stop("INVALID_LIFE_HISTORY")
            if x>0 and fl==0:fl_head_discord+=1
            if x>0 and l==0:death_head_discord+=1
            counts.append(x)
        rec.append((dam,sire,num(a["row"],"row"),num(a["pos"],"pos"),dist/1000.,delta,abs(delta),fruit,sum(counts),alive))
    if len(rec)!=436 or n_no_dist!=2:raise Stop("COHORT_MISMATCH")
    if death_head_discord:raise Stop("DEAD_WITH_POSITIVE_HEADS")
    return rec,{"original_offspring_rows":len(f),"matched_predictor_rows":len(p),"excluded_unknown_parent_distance":n_no_dist,
                "author_2022_correction_applied":1,"included_offspring":len(rec),"maternal_groups":len({r[0] for r in rec}),
                "paternal_groups":len({r[1] for r in rec}),"parent_pair_groups":len({(r[0],r[1]) for r in rec}),
                "head_year_count":len(YRS),"head_years":list(YRS),"zero_cumulative_head_count":sum(r[8]==0 for r in rec),
                "dead_2022_without_heads":sum(r[9]==0 and r[8]==0 for r in rec),"alive_2022":sum(r[9] for r in rec),
                "max_observed_cumulative_heads":max(r[8] for r in rec),"positive_heads_but_flowering_zero_cells":fl_head_discord,
                "positive_heads_but_dead_cells":death_head_discord}
def predict(train,test,add,target):
    mu=[statistics.mean(r[i] for r in train) for i in range(2,7)]
    sd=[statistics.pstdev(r[i] for r in train) for i in range(2,7)]
    def feat(r):
        q=[(r[i]-m)/s if s>1e-12 else 0. for i,m,s in zip(range(2,7),mu,sd)]
        z=[1.]+q+[float(r[7]==c) for c in CATS[1:]]
        if add:z.append(q[2]*q[3])
        return z
    X=[feat(r) for r in train];n=len(X[0]);A=[[0.]*n for _ in range(n)];b=[0.]*n
    for x,r in zip(X,train):
        for i in range(n):
            b[i]+=x[i]*r[target]
            for j in range(n):A[i][j]+=x[i]*x[j]
    for i in range(1,n):A[i][i]+=1.
    beta=solve(A,b)
    raw=[max(0.,sum(v*w for v,w in zip(feat(r),beta))) for r in test]
    return [min(1.,x) for x in raw] if target==9 else raw
def foldplan(rs,disjoint):
    moms=sorted({r[0] for r in rs})
    if len(moms)<25:raise Stop("INSUFFICIENT_MATERNAL_GROUPS")
    folds=[]
    for m in moms:
        te=[r for r in rs if r[0]==m]
        tr=[r for r in rs if r[0]!=m]
        if disjoint:
            heldparents={p for r in te for p in r[:2]}
            tr=[r for r in tr if r[0] not in heldparents and r[1] not in heldparents]
        folds.append((tr,te))
    return folds
def evaluate(rs,disjoint=False):
    plan=foldplan(rs,disjoint)
    supports=[(len(tr),len({r[0] for r in tr})) for tr,te in plan]
    eligible=all(n>=100 and g>=(15 if disjoint else 1) for n,g in supports)
    support={"folds":len(plan),"minimum_training_n":min(n for n,g in supports),
             "minimum_training_mothers":min(g for n,g in supports),"insufficient_folds":sum(n<100 or g<(15 if disjoint else 1) for n,g in supports)}
    if not eligible:return dict(status="FIXED_SUPPORT_STOP",**support)
    out=dict(status="COMPLETE",**support)
    for target,name in [(8,"cumulative_heads"),(9,"alive_2022")]:
        folds=[]
        for i,(tr,te) in enumerate(plan):
            a=predict(tr,te,False,target);b=predict(tr,te,True,target)
            e0=sum((r[target]-p)**2 for r,p in zip(te,a));e1=sum((r[target]-p)**2 for r,p in zip(te,b))
            n=len(te);folds.append({"fold":i,"n":n,"training_n":len(tr),"M0_MSE":e0/n,"M1_MSE":e1/n,"gain":(e0-e1)/n})
        n=sum(f["n"] for f in folds);m0=sum(f["M0_MSE"]*f["n"] for f in folds)/n;m1=sum(f["M1_MSE"]*f["n"] for f in folds)/n
        gain=m0-m1;wins=sum(f["gain"]>0 for f in folds);rng=random.Random(20261126);boot=[]
        for _ in range(1000):
            draw=rng.choices(folds,k=len(folds))
            boot.append(sum(f["gain"]*f["n"] for f in draw)/sum(f["n"] for f in draw))
        boot.sort()
        out[name]={"M0_MSE":m0,"M1_MSE":m1,"gain":gain,"relative_mse_reduction":gain/m0 if m0 else None,
                   "positive_mother_folds":wins,"mother_folds":len(folds),"fixed_residual_mother_bootstrap_95pct":[boot[24],boot[975]],
                   "decision":"INTERACTION_INCREMENT" if gain>0 and wins/len(folds)>=.7 else "NO_SUPPORTED_INCREMENT","fold_results":folds}
    return out
def run():
    d={"protocol":LOCK,"raw_records_exported":False,"author_code_executed":False,
       "molecular_GxIxF_validated":False,"causal_effect_claimed":False,"independent_programme_confirmation":False}
    try:
        subprocess.run(["git","merge-base","--is-ancestor",LOCK,"HEAD"],cwd=ROOT,check=True)
        files=official_drum(HANDLES["ECH01"])
        raws={k:pinned(files,k,v) for k,v in HASHES.items()}
        d["source_sha256"]=HASHES
        rec,info=prepare(rows(raws["offspring_fitness_data.csv"]),rows(raws["fitness_predictors.csv"]),raws["analysis_code.R"].decode("utf-8-sig"))
        d.update(info)
        d["maternal_holdout"]=evaluate(rec)
        d["parent_disjoint_sensitivity"]=evaluate(rec,True)
        d["status"]="ECH01A_COMPLETE" if d["maternal_holdout"]["status"]=="COMPLETE" else "ECH01A_SUPPORT_STOP"
    except Exception as e:
        d.update(status="ECH01A_SOURCE_OR_MODEL_STOP",reason=str(e)[:140] if isinstance(e,Stop) else type(e).__name__)
    return d
if __name__=="__main__":print(json.dumps(run(),indent=2))
