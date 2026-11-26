#!/usr/bin/env python3
"""CAMP01: frozen independent Campanula experimental-site transport test.
Source-only metadata/key gate before model; output aggregate metrics or explicit stop.
No source individual values or identifiers redistributed.
"""
from collections import Counter, defaultdict
import csv, hashlib, io, json, math, re, statistics, subprocess
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT=Path(__file__).resolve().parents[2]
LOCK="03bc79ff02158e73e08138efcb5440130e6f22c0"
DOI="10.5281/zenodo.10814705"
REC="10814705"
FILES={"PLdataindividual.csv":"b84fa5c83513dbe75c0bf7840d1c74aa",
       "pollinator.csv":"81e0deaa78a6a97e1211484cb9d0d3b3"}
BASE_FIELDS={"experimental_population","site","source_population","autonomy","size"}
MISSING={"","na","n/a","nan","null","none","."}
class Stop(Exception): pass

def norm(s): return re.sub(r"[^a-z0-9]+","_",str(s or "").strip().lower()).strip("_")
def clean(s): return str(s if s is not None else "").strip()
def fetch(url, cap):
    p=urlparse(url)
    if p.scheme!="https" or p.hostname not in {"zenodo.org","www.zenodo.org"} or p.username or p.password:
        raise Stop("NONOFFICIAL_SOURCE_URL")
    with urlopen(Request(url,headers={"User-Agent":"EGWEE-CAMP01/1.0 (open research source audit)"}),timeout=45) as r:
        b=r.read(cap+1)
    if len(b)>cap: raise Stop("SOURCE_SIZE_CAP")
    return b
def numeric(v,integer=False):
    s=clean(v)
    if s.lower() in MISSING:return None
    try:x=float(s)
    except ValueError:raise Stop("NONNUMERIC_SOURCE_VALUE")
    if not math.isfinite(x) or x<0 or (integer and abs(x-round(x))>1e-7):
        raise Stop("INVALID_SOURCE_VALUE")
    return x
def csvrows(raw):
    f=csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    heads=[norm(x) for x in (f.fieldnames or [])]
    if len(set(heads))!=len(heads) or not heads:raise Stop("AMBIGUOUS_HEADER")
    rows=[]
    for row in f:
        if None in row:raise Stop("MALFORMED_CSV_ROW")
        rows.append({norm(k):clean(v) for k,v in row.items()})
    return heads,rows
def key(r):
    if any(not r.get(k) for k in ("experimental_population","site","source_population","autonomy","size")):
        raise Stop("MISSING_DESIGN_KEY")
    return (r["site"],r["experimental_population"])
def design(r):
    a=norm(r["autonomy"]); s=norm(r["size"])
    if a not in {"high","low"} or s not in {"single","small"}:
        raise Stop("UNVERIFIED_AUTONOMY_OR_SIZE_CATEGORY")
    return (r["source_population"],a,s)
def join(seed,poll,receipt):
    ps={}
    source_classes=defaultdict(set)
    for r in poll:
        k=key(r)
        if k in ps:raise Stop("DUPLICATE_POLLINATOR_EXPERIMENTAL_POPULATION")
        d=design(r)
        source_classes[d[0]].add(d[1])
        ps[k]=(d,numeric(r["visits_per_flower"]))
    if len(ps)>53:raise Stop("PUBLISHED_EXPERIMENTAL_POPULATION_COUNT_EXCEEDED")
    if any(len(v)!=1 for v in source_classes.values()):raise Stop("AUTONOMY_SOURCE_POPULATION_INCONSISTENT")
    groups=defaultdict(lambda:defaultdict(lambda:defaultdict(list)))
    seed_design={}
    nmissing=0
    for r in seed:
        k=key(r);d=design(r)
        if k in seed_design and seed_design[k]!=d:raise Stop("SEED_EXPERIMENTAL_DESIGN_CONFLICT")
        seed_design[k]=d
        if k in ps and ps[k][0]!=d:raise Stop("CROSS_TABLE_DESIGN_MISMATCH")
        if not r.get("individual"):raise Stop("MISSING_INDIVIDUAL_KEY")
        t=norm(r["treatment"])
        if t not in {"control","supplemented"}:raise Stop("UNVERIFIED_TREATMENT_CATEGORY")
        y=numeric(r["seed_number"],integer=True)
        if y is None:nmissing+=1;continue
        groups[k][r["individual"]][t].append(y)
    records=[];paired=0;unpaired=0;no_pairs=0;missing_visits=0
    for k, plants in groups.items():
        ds=[]
        for arms in plants.values():
            if not arms.get("control") or not arms.get("supplemented"):
                unpaired+=1;continue
            ds.append(math.log1p(statistics.mean(arms["supplemented"]))-math.log1p(statistics.mean(arms["control"])))
            paired+=1
        if not ds:no_pairs+=1;continue
        if k not in ps:continue
        d,v=ps[k]
        if v is None:missing_visits+=1;continue
        records.append((k[0],d[0],d[1],d[2],math.log1p(v),statistics.mean(ds)))
    receipt.update(seed_rows=len(seed),pollinator_rows=len(poll),seed_experimental_populations=len(seed_design),
                   pollinator_experimental_populations=len(ps),joined_experimental_populations=len(set(seed_design)&set(ps)),
                   seed_only_experimental_populations=len(set(seed_design)-set(ps)),pollinator_only_experimental_populations=len(set(ps)-set(seed_design)),
                   missing_seed_records=nmissing,paired_plant_records=paired,unpaired_plant_records=unpaired,
                   experimental_populations_without_paired_plant=no_pairs,paired_groups_missing_visits=missing_visits,
                   analysis_experimental_populations=len(records),analysis_sites=len({r[0] for r in records}),
                   source_population_levels=len({r[1] for r in records}))
    return records

def solve(A,b):
    m=[list(x)+[y] for x,y in zip(A,b)];n=len(b)
    for j in range(n):
        k=max(range(j,n),key=lambda i:abs(m[i][j]))
        if abs(m[k][j])<1e-12:raise Stop("SINGULAR_RIDGE_SYSTEM")
        m[j],m[k]=m[k],m[j]
        d=m[j][j];m[j]=[x/d for x in m[j]]
        for i in range(n):
            if i!=j:
                d=m[i][j];m[i]=[x-d*y for x,y in zip(m[i],m[j])]
    return [r[-1] for r in m]
def fit_predict(train,test,levels,interaction):
    mu=statistics.mean(r[4] for r in train)
    sd=statistics.pstdev(r[4] for r in train)
    if sd<=1e-12:raise Stop("NO_TRAINING_VISITATION_VARIATION")
    def x(r):
        a=float(r[2]=="high");s=float(r[3]=="small");v=(r[4]-mu)/sd
        f=[1.]+[float(r[1]==l) for l in levels[1:]]+[a,s,a*s,v]
        if interaction:f.append(a*v)
        return f
    X=[x(r) for r in train]; p=len(X[0]); A=[[0.]*p for _ in range(p)]; b=[0.]*p
    for z,r in zip(X,train):
        for i in range(p):
            b[i]+=z[i]*r[5]
            for j in range(p):A[i][j]+=z[i]*z[j]
    for i in range(1,p):A[i][i]+=1.
    beta=solve(A,b)
    return [sum(v*w for v,w in zip(x(r),beta)) for r in test],beta
def evaluate(rs):
    sites=sorted({r[0] for r in rs});levels=sorted({r[1] for r in rs})
    if len(rs)<30 or len(sites)<8 or len(levels)!=4:raise Stop("INSUFFICIENT_FIXED_SITE_SUPPORT")
    if any(sum(r[0]==s for r in rs)<2 for s in sites):raise Stop("INSUFFICIENT_SITE_TEST_GROUPS")
    out=[];e0=e1=0.
    for i,s in enumerate(sites):
        tr=[r for r in rs if r[0]!=s];te=[r for r in rs if r[0]==s]
        if {r[1] for r in tr}!=set(levels) or {r[2] for r in tr}!={"high","low"} or {r[3] for r in tr}!={"single","small"}:
            raise Stop("INSUFFICIENT_TRAINING_LEVELS")
        p0,_=fit_predict(tr,te,levels,False);p1,beta=fit_predict(tr,te,levels,True)
        a=sum((r[5]-p)**2 for r,p in zip(te,p0));b=sum((r[5]-p)**2 for r,p in zip(te,p1))
        e0+=a;e1+=b
        out.append(dict(fold=i,n=len(te),M0_MSE=a/len(te),M1_MSE=b/len(te),
                        gain=(a-b)/len(te),descriptive_interaction_coefficient=beta[-1]))
    wins=sum(x["gain"]>0 for x in out)
    return dict(M0_MSE=e0/len(rs),M1_MSE=e1/len(rs),gain=(e0-e1)/len(rs),
                site_folds=len(sites),positive_site_folds=wins,folds=out,
                decision="WITHIN_PROGRAMME_SITE_TRANSFER_INCREMENT" if e0>e1 and wins/len(sites)>=.7 else "NO_SUPPORTED_SITE_TRANSFER_INCREMENT")
def run():
    d={"status":"SOURCE_GATE_PENDING","protocol":LOCK,"doi":DOI,
       "raw_rows_redistributed":False,"molecular_GxIxF_validated":False,
       "causal_visitation_effect_claimed":False,"new_independent_programmes":0}
    try:
        subprocess.run(["git","merge-base","--is-ancestor",LOCK,"HEAD"],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
        meta=json.loads(fetch("https://zenodo.org/api/records/"+REC,2_000_000))
        if str(meta.get("id"))!=REC or meta.get("doi")!=DOI:raise Stop("ZENODO_RECORD_MISMATCH")
        mf={f.get("key"):f for f in meta.get("files",[])}
        if set(mf)!=set(FILES):raise Stop("FILE_INVENTORY_MISMATCH")
        tabs={};d["source_files"]=[]
        for fn,md5 in FILES.items():
            entry=mf[fn];links=entry.get("links",{})
            url=links.get("content") or links.get("self")
            if not url:raise Stop("NO_OFFICIAL_DOWNLOAD_LINK")
            raw=fetch(url,2_000_000)
            if hashlib.md5(raw).hexdigest()!=md5:raise Stop("ORIGINAL_MD5_MISMATCH")
            h,rows=csvrows(raw);tabs[fn]=rows
            d["source_files"].append({"name":fn,"sha256":hashlib.sha256(raw).hexdigest(),"rows":len(rows),"headers":h})
            required=BASE_FIELDS|({"individual","treatment","seed_number"} if fn.startswith("PL") else {"visits_per_flower"})
            if not required.issubset(h):
                raise Stop("REQUIRED_SOURCE_HEADER_MISSING:"+",".join(sorted(required-set(h))))
        seed=tabs["PLdataindividual.csv"];poll=tabs["pollinator.csv"]
        # Public treatment/design categories only, never seed or visitation values.
        d["source_design_categories"]={name:sorted({norm(r[name]) for r in seed}) for name in ("autonomy","size","treatment")}
        d["source_files_verified"]=True
        records=join(seed,poll,d)
        d.update(evaluate(records))
        d["status"]="CAMP01_FIXED_SITE_HOLDOUT_COMPLETE"
        d["new_independent_programmes"]=1
    except (Stop, HTTPError, URLError, ValueError, KeyError, TypeError, IndexError, subprocess.CalledProcessError) as exc:
        d["status"]="CAMP01_SOURCE_OR_SUPPORT_STOP"
        d["reason"]=str(exc)[:160] if isinstance(exc,Stop) else type(exc).__name__
        if isinstance(exc,HTTPError):d["http_status"]=exc.code
        d["decision"]="NOT_IDENTIFIABLE_FROM_CURRENT_SOURCE"
    return d
if __name__=="__main__":
    print(json.dumps(run(),indent=2,ensure_ascii=False))
