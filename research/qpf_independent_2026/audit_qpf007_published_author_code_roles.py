#!/usr/bin/env python3
"""Source-verifiable, nonexecuting original author R source parentage role audit.

Reads only official original source code and original checksum; no source
genotypes, father/seed assignment rows or pollen values. Short source-code
context in GitHub Actions logs is only for human scientific-source review,
never automatically claims parentage semantics.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from audit_brassica_rapa_zenodo_source_keys import load_manifest,trusted_get

SOURCE_NAME="script_ABPOLL_main_analyses.R"
MAX_SIZE=600_000
NEEDLES=("known_id","candidate_id","offspring_id","fix10_paternities",
         "ID_level_detID","ID_level_ID","ID_full_foc","ID_full_part")
SPEC="research/qpf_independent_2026/QPF007_AUTHOR_CODE_PARENTAGE_ROLE_FREEZE_20261118.md"
MAX_PRINT_LINES=24

def code_source():
    doc=load_manifest()
    matches=[r for r in doc["files"]
             if (r.get("key") or r.get("filename"))==SOURCE_NAME]
    if len(matches)!=1:
        raise ValueError("SOURCE_STOP: original author script missing/ambiguous in Zenodo")
    entry=matches[0]
    expected_bytes=entry.get("size")
    if not isinstance(expected_bytes,int) or not 1000<=expected_bytes<=MAX_SIZE:
        raise ValueError("SOURCE_STOP: advertised script size invalid")
    rawurl=(entry.get("links") or {}).get("self") or (entry.get("links") or {}).get("content")
    if not rawurl:raise ValueError("SOURCE_STOP: no author-advertised source script URL")
    data=trusted_get(rawurl,MAX_SIZE)
    if len(data)!=expected_bytes:
        raise ValueError("Original R script bytes differ from published size")
    declared=str(entry.get("checksum") or "")
    if not declared.startswith("md5:") or hashlib.md5(data).hexdigest()!=declared[4:]:
        raise ValueError("Published original author script checksum mismatch")
    try:txt=data.decode("utf-8-sig","strict")
    except UnicodeDecodeError:txt=data.decode("latin-1","strict")
    return txt,hashlib.sha256(data).hexdigest(),len(data)

def analyze():
    text,sha,size=code_source()
    lines=text.splitlines()
    hits={term:[i+1 for i,s in enumerate(lines) if term.casefold() in s.casefold()]
          for term in NEEDLES}
    counts={term:len(p) for term,p in hits.items()}
    # Source code is not itself a semantic proof until we inspect the roles in
    # context; never automatically promote a shared string to a true father.
    annotated=[]
    printed=set()
    for needle in ("fix10_paternities","candidate_id","known_id",
                   "ID_level_detID","ID_level_ID","offspring_id"):
        for line_no in hits[needle][:4]:
            if len(annotated)>=MAX_PRINT_LINES:break
            if line_no in printed:continue
            original=lines[line_no-1]
            sanitized=original.rstrip()[:220]
            annotated.append({"source_line_number":line_no,
                              "source_code_excerpt_for_review":sanitized})
            printed.add(line_no)
    return {
        "status":"PUBLISHED_ORIGINAL_AUTHOR_SCRIPT_CHECKSUM_VERIFIED",
        "original_public_data_doi":"10.5281/zenodo.21628183",
        "original_author_script":SOURCE_NAME,
        "original_R_script_sha256":sha,
        "original_R_script_bytes":size,
        "original_R_script_line_count":len(lines),
        "searched_terms_code_line_counts":counts,
        "bounded_author_code_evidence_for_review":annotated,
        "source_code_executed":False,
        "paternity_roles_certified_by_this_automated_source_gate":False,
        "assigned_father_vs_candidate_semantics_human_review_required":True,
        "source_raw_individual_genotypes_or_paternities_opened":False,
        "source_genetic_effect_estimated":False,
        "original_author_R_source_code_redistributed":False,
        "scientific_status":"CODEBOOK_SOURCE_ROLE_REVIEW_REQUIRED",
        "frozen_source_only_spec":SPEC,
    }

def synthetic():
    assert "known_id".casefold() in "known_ID".casefold()
    assert MAX_PRINT_LINES<=25
    assert "candidate_id" in NEEDLES
    print("QPF007_AUTHOR_SCRIPT_ROLE_GATE_SYNTHETIC_PASS")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    if args.self_test:synthetic();return 0
    if args.output is None:parser.error("--output required")
    try:r=analyze()
    except Exception as e:
        r={"status":"ORIGINAL_AUTHOR_CODEBOOK_ACCESS_STOP",
           "error_type":type(e).__name__,
           "reason":str(e)[:180],
           "paternity_roles_certified_by_this_automated_source_gate":False,
           "source_genetic_effect_estimated":False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    brief={k:v for k,v in r.items() if k in
           ("status","original_author_script","original_R_script_sha256",
            "original_R_script_bytes","searched_terms_code_line_counts",
            "bounded_author_code_evidence_for_review","paternity_roles_certified_by_this_automated_source_gate",
            "scientific_status","reason")}
    print("QPF007_AUTHOR_SCRIPT_ROLE_SOURCE "+json.dumps(brief,sort_keys=True),flush=True)
    return 0 if r["status"]=="PUBLISHED_ORIGINAL_AUTHOR_SCRIPT_CHECKSUM_VERIFIED" else 1

if __name__=="__main__":
    raise SystemExit(main())
