#!/usr/bin/env python3
"""CY002 source-denominator-corrected plot holdout (preserve CY001 v1).

The schema stage verifies the XLSX source/parent/plot structure, writes SHA256,
and does not inspect rpm or seed observations. The fit stage requires the
identical recorded schema receipt. Neither stage exports original maternal IDs
or individual biological source values.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from math import isfinite, log1p
from pathlib import Path
import re
from statistics import fmean
import subprocess
import zipfile
from xml.etree import ElementTree as ET

from run_leavenworthia_LA001 import solve

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL_REL = "research/compatibility_function/CY002_FROZEN_SOURCE_COUNT_CORRECTION_20261118.json"
PROTOCOL = ROOT / PROTOCOL_REL
FREEZE_SHA = "98e2635626515950e7d7c29136b2d4c6c3f17722"
ORIGINAL_CY001_FREEZE_SHA = "a118ab77e71a097b46d264738e34c0428384a304"
# Official Dryad version 2024-09-20 file metadata, SHA-256 original source.
ORIGINAL_SOURCE_SHA256 = "18941f666c040c81c5db3f43c661d44fc157e9db636eef07a4aafd49f77b5332"
MAIN_XML = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
COL = {"id":0,"alleles":1,"rpm":3,"visits":4,"donor":5,"richness":6,
       "density":7,"plot":21,"strip":22,"n_child":23,"seeds":27}

def verify_protocol():
    raw = subprocess.check_output(
        ["git","show",FREEZE_SHA+":"+PROTOCOL_REL],cwd=ROOT)
    if raw != PROTOCOL.read_bytes():
        raise RuntimeError("CY001 frozen protocol changed after outcome disclosure")
    subprocess.run(["git","merge-base","--is-ancestor",FREEZE_SHA,"HEAD"],
                   cwd=ROOT,check=True)
    p = json.loads(raw)
    if p["experiment_id"] != "CY002_cyanus_original_offspring_n_corrected_plot_holdout":
        raise RuntimeError("Incorrect CY002 original protocol family")
    if p["status"] != "source_denominator_corrected_before_full_model_fit_with_limited_preview_disclosure":
        raise RuntimeError("CY002 denominator-correction lock status invalid")
    # Prior CY001 source gate remains historically immutable and an ancestor.
    subprocess.run(["git","merge-base","--is-ancestor",ORIGINAL_CY001_FREEZE_SHA,"HEAD"],
                   cwd=ROOT,check=True)
    return p

def column_index(address):
    prefix = re.match("^[A-Z]+", address or "")
    if prefix is None:
        raise ValueError("Non-A1 source column name")
    val = 0
    for c in prefix.group():
        val = 26*val + ord(c)-64
    return val-1

def rows_from_workbook(path):
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None:
            raise ValueError("Source XLSX CRC failure")
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall(MAIN_XML+"si"):
                shared.append("".join(x.text or "" for x in si.iter(MAIN_XML+"t")))
        candidates = []
        for filename in z.namelist():
            if not re.fullmatch("xl/worksheets/sheet[0-9]+[.]xml",filename):
                continue
            root = ET.fromstring(z.read(filename))
            rows = []
            for row in root.iter(MAIN_XML+"row"):
                cells = {}
                for c in row.findall(MAIN_XML+"c"):
                    v = c.find(MAIN_XML+"v")
                    typ = c.attrib.get("t","n")
                    if typ == "s" and v is not None:
                        item = shared[int(v.text)]
                    elif typ == "inlineStr":
                        item = "".join(t.text or "" for t in c.iter(MAIN_XML+"t"))
                    elif v is None:
                        item = None
                    elif typ in ("str","e"):
                        item = v.text
                    else:
                        item = float(v.text)
                    if item is not None and item != "":
                        cells[column_index(c.attrib.get("r"))] = item
                rows.append(cells)
            for ix,hd in enumerate(rows[:5]):
                if "maternal" in str(hd.get(0,"")).lower() and "rpm" in str(hd.get(3,"")).lower():
                    candidates.append((hd,[r for r in rows[ix+1:] if r]))
                    break
        if len(candidates)!=1:
            raise RuntimeError("Original source must have one mother-rpm worksheet")
        return candidates[0]

def num(x,key):
    if not isinstance(x,(float,int)) or not isfinite(float(x)) or float(x)<0:
        raise ValueError("Missing/invalid original source variable: "+key)
    return float(x)

def source_schema(path):
    verify_protocol()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != ORIGINAL_SOURCE_SHA256:
        raise RuntimeError("Workbook hash is not the original Dryad CY001 publication SHA-256")
    header,rows = rows_from_workbook(path)
    expected = {"id":"maternal","alleles":"alleles","rpm":"rpm",
                "visits":"relative","plot":"plot","strip":"strip",
                "n_child":"offspring","seeds":"seeds"}
    for k,fragment in expected.items():
        if fragment not in str(header.get(COL[k],"")).casefold():
            raise ValueError("Original source header disagrees with Dryad README at "+k)
    if len(rows)!=33:
        raise RuntimeError("Expected 33 selected genotyped mothers")
    mothers = [str(r.get(COL["id"],"")) for r in rows]
    if any(not s for s in mothers) or len(set(mothers))!=33:
        raise RuntimeError("Original maternal keys missing/duplicated")
    plots = Counter(str(r.get(COL["plot"],"")) for r in rows)
    if len(plots)!=12 or any(not x or n>3 for x,n in plots.items()):
        raise RuntimeError("33 mothers do not occupy 12 distinct plots of up to 3")
    strips = sorted(set(str(r.get(COL["strip"],"")) for r in rows))
    if len(strips)!=2 or "" in strips:
        raise RuntimeError("Original strip category unidentified")
    children=[num(r.get(COL["n_child"]),"typed_offspring") for r in rows]
    # The paper/README describe 15-17, but the exact official 27,995-byte
    # workbook contains one mother with 12; correct this SOURCE-ONLY mismatch
    # without dropping her or selecting by mating/seed outcomes.
    typed = Counter(int(n) for n in children if n == int(n))
    expected_typed = Counter({12:1,15:1,16:5,17:26})
    if typed != expected_typed or sum(int(n) for n in children) != 549:
        raise RuntimeError("CY002 original source-only typed-offspring roster drift")
    return {
      "status":"SOURCE_SCHEMA_VERIFIED_NO_RESPONSES_OPENED",
      "dataset_doi":"10.5061/dryad.9p8cz8ws1",
      "source_sha256":digest,
      "selected_mother_n":33,"plot_n":12,
      "plot_sizes_sorted":sorted(plots.values()),
      "strip_n":2,"typed_offspring_n":sum(int(n) for n in children),
      "typed_offspring_histogram":{str(i): typed[i] for i in sorted(typed)},
      "source_only_correction_status":"one_12_typed_mother_retained_no_outcome_filter",
      "response_values_inspected":False,
      "original_source_redistributed":False,
    }

def ridge_predict(train,test,response,added):
    def features(r):
        return r["base"] + ([r["visits"]] if added else [])
    x=[features(r) for r in train]
    p=len(x[0])
    means=[fmean(v[j] for v in x) for j in range(p)]
    scales=[max(1e-10,fmean((v[j]-means[j])**2 for v in x)**.5) for j in range(p)]
    X=[[1]+[(v[j]-means[j])/scales[j] for j in range(p)] for v in x]
    gram=[[sum(row[j]*row[k] for row in X)+(1 if j==k and j>0 else 0)
           for k in range(p+1)] for j in range(p+1)]
    rhs=[sum(row[j]*r[response] for row,r in zip(X,train))
         for j in range(p+1)]
    coef=solve(gram,rhs)
    predict=[coef[0]+sum(coef[j+1]*(features(r)[j]-means[j])/scales[j]
                             for j in range(p)) for r in test]
    return [min(1,max(0,z)) for z in predict] if response=="rpm" else predict

def analyze(path,schema_receipt):
    verify_protocol()
    pinned=json.loads(schema_receipt.read_text())
    if pinned.get("status")!="SOURCE_SCHEMA_VERIFIED_NO_RESPONSES_OPENED":
        raise RuntimeError("Missing prior source-only schema receipt")
    # Verify the frozen ORIGINAL byte hash before opening any workbook member
    # or biological outcome, including when the proposed XLSX is corrupted.
    current_digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if current_digest != pinned.get("source_sha256"):
        raise RuntimeError("Raw original XLSX bytes changed since schema-only freeze")
    verified=source_schema(path)
    for k in ("source_sha256","selected_mother_n","plot_n","plot_sizes_sorted",
              "strip_n","typed_offspring_n","typed_offspring_histogram"):
        if pinned[k]!=verified[k]:
            raise RuntimeError("Source changed since separate schema stage at "+k)
    _,raw=rows_from_workbook(path)
    strips=sorted({str(r[COL["strip"]]) for r in raw})
    data=[]
    for r in raw:
        mother=num(r.get(COL["alleles"]),"mother allele count")
        donor=num(r.get(COL["donor"]),"donor density")
        richness=num(r.get(COL["richness"]),"floral richness")
        density=num(r.get(COL["density"]),"floral density")
        visit=num(r.get(COL["visits"]),"relative visits")
        rpm=num(r.get(COL["rpm"]),"correlated paternity")
        seed=num(r.get(COL["seeds"]),"selected mothers seed count")
        if rpm>1:
            raise ValueError("rpm out of range [0,1]")
        data.append({
          "plot":str(r[COL["plot"]]),
          "base":[mother,log1p(donor),log1p(richness),log1p(density),
                  int(str(r[COL["strip"]])==strips[1])],
          "visits":log1p(visit),
          "rpm":rpm,
          "seed_log":log1p(seed),
        })
    folds=[]
    for plot in sorted({r["plot"] for r in data}):
        train=[r for r in data if r["plot"]!=plot]
        test=[r for r in data if r["plot"]==plot]
        stats={}
        for outcome in ("rpm","seed_log"):
            stats[outcome]={}
            for model, added in (("M0",False),("M1",True)):
                pred=ridge_predict(train,test,outcome,added)
                errors=[r[outcome]-v for r,v in zip(test,pred)]
                stats[outcome][model]={
                  "mse":fmean(e*e for e in errors),
                  "mae":fmean(abs(e) for e in errors),
                }
            stats[outcome]["delta_mse"]=stats[outcome]["M0"]["mse"]-stats[outcome]["M1"]["mse"]
        folds.append({"plot":plot,"n_mothers":len(test),"outcomes":stats})
    if len(folds)!=12 or sum(x["n_mothers"] for x in folds)!=33:
        raise RuntimeError("Whole-plot holdout denominator changed")
    aggregate={}
    for outcome in ("rpm","seed_log"):
        o={}
        for metric in ("mse","mae"):
            for model in ("M0","M1"):
                o[model+"_"+metric]=sum(f["n_mothers"]*f["outcomes"][outcome][model][metric]
                                        for f in folds)/33
        gain=o["M0_mse"]-o["M1_mse"]
        o["M0_minus_M1_mse"]=gain
        o["relative_gain_percent"]=100*gain/o["M0_mse"] if o["M0_mse"]>0 else None
        o["positive_plot_folds"]=sum(f["outcomes"][outcome]["delta_mse"]>0 for f in folds)
        aggregate[outcome]=o
    primary=aggregate["rpm"]
    passed=(primary["M0_minus_M1_mse"]>0 and
            primary["relative_gain_percent"]>=5 and
            primary["positive_plot_folds"]>=8)
    return {
      "status":"ORIGINAL_SOURCE_MATCHED_12_PLOT_TEST_COMPLETE",
      "source_sha256":verified["source_sha256"],
      "source_doi":"10.5061/dryad.9p8cz8ws1",
      "freeze_protocol_commit":FREEZE_SHA,
      "analysis_id":"CY002_cyanus_original_offspring_n_corrected_plot_holdout",
      "mothers":33,"nested_original_plots":12,
      "typed_offspring_original_source_n":549,
      "CY001_prior_source_gate":"STOP_15to17_DOES_NOT_MATCH_ONE_12",
      "initial_four_mother_rows_previewed_before_CY002_freeze":True,
      "fully_outcome_blind":False,
      "primary_correlated_paternity":primary,
      "secondary_outcome_selected_seed_number":aggregate["seed_log"],
      "folds":folds,
      "decision":"BOUNDED_WITHIN_FARM_PLOT_OUT_GAIN" if passed else "NO_PRACTICALLY_PORTABLE_INCREMENT",
      "scope":"Mother-level plot CV; selected 33 mothers in ONE farm, original paper already tested mating associations; CY002 had four earlier source-preview outcome rows so not a fully blinded confirmatory replication.",
      "raw_third_party_source_redistributed":False,
    }

def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("--mode",required=True,choices=("schema","fit"))
    cli.add_argument("--source-xlsx",required=True,type=Path)
    cli.add_argument("--locked-schema",type=Path)
    cli.add_argument("--output",required=True,type=Path)
    a=cli.parse_args()
    if a.mode=="fit":
        if a.locked_schema is None:
            cli.error("fit requires separately frozen --locked-schema")
        result=analyze(a.source_xlsx,a.locked_schema)
    else:
        result=source_schema(a.source_xlsx)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":result["status"],
                      "source_sha256":result["source_sha256"],
                      "decision":result.get("decision","NOT_TESTED"),
                      "n":result.get("mothers",result.get("selected_mother_n"))},indent=2))
if __name__=="__main__":
    main()
