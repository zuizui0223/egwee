#!/usr/bin/env python3
"""Inspect <=24 exact R lines documenting parentage roles and session parsing.

This prints ONLY published author-script excerpts, never original paternity
rows or genotypes. All role claims remain source-code-review STOP pending
manual interpretation of original paper, README and code contexts.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from audit_qpf007_published_author_code_roles import code_source

EXPECTED_SHA="a8e47abb7b2b4e7d6f85574fa6444eddd35a2bf0537592eccb4354fabb2402e9"
LINE_NUMBERS=list(range(85,95))+list(range(99,110))+[113,117,119] # 24 source lines

def audit():
    src,sha,n=code_source()
    if sha!=EXPECTED_SHA or n!=297463:
        raise ValueError("Original author R source fingerprint drift")
    assert len(LINE_NUMBERS)==24 and len(set(LINE_NUMBERS))==24
    lines=src.splitlines()
    if len(lines)<6037:
        raise ValueError("Unexpected original author R script length")
    excerpts=[{"line":i,"source_code":lines[i-1].strip()[:240]}
              for i in LINE_NUMBERS]
    # Author methodological provenance is not an inferred new scientific
    # result. The operator must inspect these and original source methods.
    return {
        "status":"AUTHOR_R_SOURCE_ROLE_CODE_CONTEXT_VERIFIED",
        "source_original_doi":"10.5281/zenodo.21628183",
        "source_sha256":sha,
        "source_script_bytes":n,
        "bounded_source_code_line_count":len(excerpts),
        "bounded_exact_lines":excerpts,
        "source_known_id_session_derivation_seen":any(
            "session = substr(known_id,1,5)" in lines[i-1] for i in LINE_NUMBERS),
        "original_genotype_or_phenotype_rows_opened":False,
        "actual_genetic_assignment_estimated":False,
        "parentage_father_role_automatic_certification":False,
        "new_biological_effect_estimated":False,
        "conclusion":"REVIEW_SOURCE_FATHER_ROLE_BEFORE_GENETIC_EDGE_LINK"
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    r=audit()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print("QPF007_ORIGINAL_AUTHOR_CODE_CONTEXT "+json.dumps(r,ensure_ascii=False,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
