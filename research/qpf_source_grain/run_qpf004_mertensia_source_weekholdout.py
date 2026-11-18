#!/usr/bin/env python3
"""QPF004 source-pinned Mertensia 2016 ramet Q/P/F and 2015 plant test.

Requires the exact original 2020 Dryad four-file ZIP locally. Original third
party source data are NOT stored in this repository and not available in CI.
Reports ONLY aggregate source-denominator and week/site fold metrics.
"""
from __future__ import annotations
import argparse
from collections import Counter
from io import BytesIO
import hashlib
import json
import math
from pathlib import Path
import re
from statistics import mean
import subprocess
from xml.etree import ElementTree as ET
from zipfile import ZipFile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PROTOCOL_REL="research/qpf_source_grain/QPF004_FROZEN_RAMET_POLLEN_SEED_WEEK_HOLDOUT_20261118.json"
PROTOCOL=ROOT/PROTOCOL_REL
FREEZE_SHA="ab174531e7311b3953e7df5daf86da3ffcb4a99f"
ZIP_SHA="635946881e42b2e67b25a3895111089db4d3d99081a7d27cb8be9e4775c1912f"
FILES={
"gallagher&campbell_phenologyExperimentData.xlsx":(96329,"51263c0cabe9dd04dbf716a4594e7d700c5235dd3f85a65ab51f43fcef828411"),
"gallagher&campbell_pollinatorEffectivenessData.xlsx":(77873,"bbfcbbaf43b53b0ef835b891bd8932ae3761a383e4ecb1f38440a4ba9d477c38"),
"gallagher&campbell_nonSpatialData_phenologyExperiment.pdf":(236709,"14d97ecbf68da07252293c751987789d768181bba23da38a9b036dac0cd19972"),
"gallagher&campbell_nonSpatialData_pollinatorEffectiveness.pdf":(206337,"f12e0588619e4a795d7f56a3d42f11cd4b7328716a901041e95f90c67e54ca7f")
}
NS="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def verify_protocol() -> None:
    historic=subprocess.check_output(["git","show",FREEZE_SHA+":"+PROTOCOL_REL],cwd=ROOT)
    if historic!=PROTOCOL.read_bytes():
        raise RuntimeError("Original QPF004 source-only scientific protocol was changed")
    subprocess.run(["git","merge-base","--is-ancestor",FREEZE_SHA,"HEAD"],cwd=ROOT,check=True)
    p=json.loads(historic)
    if (p["experiment_id"]!="QPF004_Mertensia_within_ramet_P_increment_week_holdout_v1"
        or p["status"]!="source_only_structural_gates_locked_before_outcome_covariance_inspection"):
        raise RuntimeError("Wrong QPF004 scientific freeze")


def source_bytes(path:Path)->dict[str,bytes]:
    if hashlib.sha256(path.read_bytes()).hexdigest()!=ZIP_SHA:
        raise ValueError("Unrecognized original 2020 Dryad ZIP SHA")
    with ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError("Original Dryad ZIP CRC failure")
        names={n for n in z.namelist() if not n.endswith("/")}
        if names!=set(FILES):
            raise ValueError("Original Dryad four-file roster drift")
        data={}
        for name,(size,digest) in FILES.items():
            b=z.read(name)
            if len(b)!=size or hashlib.sha256(b).hexdigest()!=digest:
                raise ValueError("Official Dryad original file digest mismatch")
            data[name]=b
    return data


def colnum(ref:str)->int:
    m=re.match(r"^[A-Z]+",ref or "")
    if m is None:
        raise ValueError("Missing cell address")
    n=0
    for c in m.group():
        n=26*n+ord(c)-64
    return n-1


def xlsx_sheet(raw:bytes,number:int)->list[dict]:
    """Decode one original source worksheet using OOXML, no external library."""
    with ZipFile(BytesIO(raw)) as z:
        if z.testzip() is not None:
            raise ValueError("Corrupt original XLSX CRC")
        shared=[]
        if "xl/sharedStrings.xml" in z.namelist():
            root=ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared=["".join(t.text or "" for t in x.iter(NS+"t")) for x in root.findall(NS+"si")]
        root=ET.fromstring(z.read(f"xl/worksheets/sheet{number}.xml"))
        rows=[]
        for row in root.iter(NS+"row"):
            cells={}
            for c in row.findall(NS+"c"):
                k=colnum(c.attrib.get("r",""))
                v=c.find(NS+"v")
                kind=c.get("t","n")
                if kind=="s": val=shared[int(v.text)] if v is not None else None
                elif kind=="inlineStr": val="".join(t.text or "" for t in c.iter(NS+"t"))
                elif kind in ("str","e"): val=v.text if v is not None else None
                elif v is not None: val=float(v.text)
                else: val=None
                if val is not None:
                    cells[k]=val
            if cells:
                rows.append(cells)
    if not rows:
        raise ValueError("No rows in original workbook")
    header=rows[0]
    names={k:str(v) for k,v in header.items()}
    return [{name:r.get(i) for i,name in names.items()} for r in rows[1:]]


def observed(v:object)->bool:
    if v is None: return False
    if isinstance(v,str):
        return v.strip().casefold() not in ("","na","n/a","9999999","nan","none","-")
    return math.isfinite(float(v)) and float(v)!=9999999


def label(v)->str:
    if isinstance(v,(int,float)) and int(v)==v:
        return str(int(v))
    return str(v).strip()


def audit_rows(p2016:list[dict], seed2016:list[dict], all2016:list[dict],
               means2015:list[dict])->tuple[list[dict],list[dict],dict]:
    if (len(all2016),len(p2016),len(seed2016),len(means2015))!=(232,62,232,40):
        raise ValueError("Original QPF004 2016 source row denominators drift")
    def indexed(rows):
        out={label(row["plantID"]):row for row in rows}
        if len(out)!=len(rows):
            raise ValueError("Original source plantID duplicates")
        return out
    a,b,c=indexed(all2016),indexed(p2016),indexed(seed2016)
    if set(a)!=set(c) or len(set(a).intersection(b))!=62:
        raise ValueError("Original 2016 seed and pollen sources do not exact-join")
    for id_,r in c.items():
        v=a[id_]
        if any(v[k]!=r[k] for k in ("week","site","treat","seedCnt","seedPerFlr","noFlrs")):
            raise ValueError("Original 2016 seed-source key or response disagreement")
    for id_,r in b.items():
        v=a[id_]
        if any(v[k]!=r[k] for k in ("week","site","treat","polDepMC","polDepNonMC")):
            raise ValueError("Original 2016 pollen-source key or assay disagreement")
    if Counter(x["treat"] for x in all2016)!=Counter({"V":94,"O":65,"B":73}):
        raise ValueError("Original 2016 three-arm source coverage shifted")
    R16=[]
    for r in all2016:
        if not all(observed(r[k]) for k in ("polDepMC","polDepNonMC","seedPerFlr")):
            continue
        if r["treat"] not in ("V","O") or r["visID"] not in ("Open","Bombus","Muscoidea","Osmia"):
            raise ValueError("Unexpected original source visitor class in matched set")
        if r["noFlrs"]<=0 or abs(r["seedCnt"]/r["noFlrs"]-r["seedPerFlr"])>1e-8:
            raise ValueError("Original 2016 seed/marked-flower denominator mismatch")
        count=0.0 if r["treat"]=="O" else r["flrsVisited"]
        if not observed(count) or count<0 or r["polDepMC"]<0 or r["polDepNonMC"]<0:
            raise ValueError("Invalid original 2016 pollinator/pollen record")
        if not 0<=r["seedPerFlr"]<=4 or r["FlrsAvail"]<0:
            raise ValueError("Original 2016 fitness or exposure outside physical support")
        base=[
            r["week"],int(r["site"]=="SP"),math.log1p(r["FlrsAvail"]),
            math.log1p(r["noFlrs"]),math.log1p(count/r["noFlrs"]),
        ]
        base.extend(int(r["visID"]==group) for group in ("Bombus","Muscoidea","Osmia"))
        cp,hp=math.log1p(r["polDepMC"]),math.log1p(r["polDepNonMC"])
        R16.append({
            "week":int(r["week"]),"site":r["site"],"y":float(r["seedPerFlr"]),
            "M0":base,"M1":base+[cp,hp,cp*hp],
        })
    if (len(R16)!=62 or
        Counter(r["week"] for r in R16)!=Counter({1:4,2:18,3:16,4:20,5:4}) or
        Counter(r["site"] for r in R16)!=Counter({"RG":38,"SP":24})):
        raise ValueError("2016 source matched-pollen support changed")

    R15=[]
    for r in means2015:
        if not observed(r["mcPolCnt"]) or not observed(r["nonMcPolCnt"]):
            continue
        if any(not observed(r[k]) or r[k]<0 for k in (
            "mSeed","mVisRate","mVWC","flrCnt","mcPolCnt","nonMcPolCnt"
        )):
            raise ValueError("2015 source means missing required covariate/outcome")
        if not 0<=r["mSeed"]<=4:
            raise ValueError("2015 seeds per flower outside [0,4]")
        base=[r["tWeek"],math.log1p(r["mVisRate"]),
              math.log1p(r["flrCnt"]),r["mVWC"]]
        cp,hp=math.log1p(r["mcPolCnt"]),math.log1p(r["nonMcPolCnt"])
        R15.append({"week":int(r["tWeek"]),"y":float(r["mSeed"]),
                    "M0":base,"M1":base+[cp,hp,cp*hp]})
    if len(R15)!=36 or Counter(r["week"] for r in R15)!=Counter({1:10,2:9,3:10,4:7}):
        raise ValueError("2015 potted-plant Q/P/F source roster changed")
    receipt={
        "source_all_2016_ramets":232,"source_2016_pollen_assayed_ramets":62,
        "2016_pollen_seed_exact_matched_ramets":len(R16),
        "2016_matched_P_ramets_by_treatment":{"V":47,"O":15,"B":0},
        "2016_site_group":{"RG":38,"SP":24},
        "2016_week_group":{"1":4,"2":18,"3":16,"4":20,"5":4},
        "2016_2015_are_distinct_experiments":True,
        "source_2015_complete_potted_plants":len(R15),
        "2015_treatment_week_group":{"1":10,"2":9,"3":10,"4":7},
        "same_individual_flower_P_F_identified":False,
        "individual_clone_triplet_ID_verified":False,
    }
    return R16,R15,receipt


def linear_solve(A,b):
    n=len(b)
    work=[list(map(float,row))+[float(b[i])] for i,row in enumerate(A)]
    for k in range(n):
        imax=max(range(k,n),key=lambda i:abs(work[i][k]))
        work[k],work[imax]=work[imax],work[k]
        pivot=work[k][k]
        if abs(pivot)<1e-12: raise ValueError("Ridge normal matrix singular")
        for j in range(k,n+1):
            work[k][j]/=pivot
        for i in range(n):
            if i==k:continue
            factor=work[i][k]
            for j in range(k,n+1):
                work[i][j]-=factor*work[k][j]
    return [row[-1] for row in work]


def ridge_prediction(train,test,model):
    X=[r[model] for r in train]
    H=[r[model] for r in test]
    d=len(X[0])
    means=[mean(z[j] for z in X) for j in range(d)]
    scales=[max(1e-10,mean((z[j]-means[j])**2 for z in X)**0.5)
            for j in range(d)]
    normal=[[1.0]+[(z[j]-means[j])/scales[j] for j in range(d)]
            for z in X]
    hold=[[1.0]+[(z[j]-means[j])/scales[j] for j in range(d)]
          for z in H]
    gram=[[sum(z[j]*z[k] for z in normal)+(1 if j==k and j>0 else 0)
           for k in range(d+1)] for j in range(d+1)]
    rhs=[sum(z[j]*r["y"] for z,r in zip(normal,train))
         for j in range(d+1)]
    beta=linear_solve(gram,rhs)
    return [min(4,max(0,sum(z[j]*beta[j] for j in range(d+1))))
            for z in hold]


def heldout(rows,group_key):
    groups=sorted({r[group_key] for r in rows})
    folds=[]
    for group in groups:
        train=[r for r in rows if r[group_key]!=group]
        test=[r for r in rows if r[group_key]==group]
        item={group_key:group,"n":len(test)}
        for model in ("M0","M1"):
            pred=ridge_prediction(train,test,model)
            errors=[r["y"]-v for r,v in zip(test,pred)]
            item[model+"_MSE"]=mean(v*v for v in errors)
            item[model+"_MAE"]=mean(abs(v) for v in errors)
            item[model+"_mean_pred"]=mean(pred)
        item["delta_M0_minus_M1_MSE"]=item["M0_MSE"]-item["M1_MSE"]
        folds.append(item)
    pooled={k:sum(r["n"]*r[k] for r in folds)/len(rows)
            for k in ("M0_MSE","M1_MSE","M0_MAE","M1_MAE")}
    pooled.update({
        "gain_M0_minus_M1_MSE":pooled["M0_MSE"]-pooled["M1_MSE"],
        "gain_percent":100*(pooled["M0_MSE"]-pooled["M1_MSE"])/pooled["M0_MSE"],
        "positive_folds":sum(x["delta_M0_minus_M1_MSE"]>0 for x in folds),
        "n_folds":len(folds),"n_source_units":len(rows),
    })
    return {"groups":folds,"pooled":pooled}


def analyze(source_zip:Path):
    verify_protocol()
    raw=source_bytes(source_zip)
    p=raw["gallagher&campbell_pollinatorEffectivenessData.xlsx"]
    v=raw["gallagher&campbell_phenologyExperimentData.xlsx"]
    all2016=xlsx_sheet(p,1)
    pollen2016=xlsx_sheet(p,2)
    seed2016=xlsx_sheet(p,3)
    means2015=xlsx_sheet(v,1)
    rows16,rows15,receipt=audit_rows(pollen2016,seed2016,all2016,means2015)
    primary=heldout(rows16,"week")
    site=heldout(rows16,"site")
    other=heldout(rows15,"week")
    success=(
        primary["pooled"]["gain_percent"]>=5
        and primary["pooled"]["positive_folds"]>=4
    )
    return {
      "analysis_id":"QPF004_Mertensia_within_ramet_P_increment_week_holdout_v1",
      "status":"ACTUAL_ORIGINAL_SOURCE_2015_2016_COHORT_RESULTS_COMPLETE",
      "preoutcome_protocol_commit":FREEZE_SHA,
      "original_dryad_doi":"10.7280/D19X0D",
      "original_article_doi":"10.1002/ajb2.1439",
      "original_zip_sha256":ZIP_SHA,
      "source_recovered_structure":receipt,
      "primary_2016_week":primary,
      "secondary_2016_site":site,
      "secondary_2015_week":other,
      "registered_decision":(
         "BOUNDED_WITHIN_STUDY_WEEK_POLLEN_INCREMENT" if success
         else "NO_PRACTICALLY_PORTABLE_POLLEN_INCREMENT"
      ),
      "scientific_scope":[
        "Pollen-to-seed matching is at ramet-level in 2016 and plant-level in 2015, not proven to be identical marked flowers.",
        "2015 and 2016 are different experiments but ONE original study programme; no independent cross-species replication.",
        "2016 matched only 62/232 seed-recovered ramets; pollen assays omit 170 and all 73 bagged controls.",
        "Weeks 1–3 are all RG and weeks 4–5 all SP; 2016 week effects confounded with site.",
        "Open controls have zero observed visits, not proven zero ecological visits.",
        "Original paper already reported Bombus effectiveness and phenological compensation.",
        "Seed-per-flower source is reproductive output, not viable next-generation recruitment.",
        "No genetically compatible pollen or paternal identity identified."
      ],
      "third_party_original_source_redistributed":False,
      "individual_flower_outcomes_exported":False,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source-zip",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    result=analyze(args.source_zip)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",
                          encoding="utf-8")
    print(json.dumps({
        "decision":result["registered_decision"],
        "original_2016_ramets":result["primary_2016_week"]["pooled"]["n_source_units"],
        "primary_M0_MSE":result["primary_2016_week"]["pooled"]["M0_MSE"],
        "primary_M1_MSE":result["primary_2016_week"]["pooled"]["M1_MSE"],
        "primary_positive_weeks":result["primary_2016_week"]["pooled"]["positive_folds"],
        "2015_secondary_n":result["secondary_2015_week"]["pooled"]["n_source_units"],
    },ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
