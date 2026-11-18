#!/usr/bin/env python3
"""QPF007 Zenodo original same-session directed-pair and paternity ID gate ONLY.

Never interprets reproductive/pollen/visitation values or prints plant IDs,
offspring labels, site labels, genetic assignments or original rows. It cannot
prove a father or mother role from a column name alone.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import shlex

from audit_brassica_rapa_zenodo_source_keys import load_manifest,trusted_binary

FILE_MAIN="data_ABPOLL_ID_resume.txt"
FILE_PAIR="data_ABPOLL_ID_level_detID.txt"
FILE_PATERNITY="data_ABPOLL_fix10_paternities.txt"
EXPECTED_SHA={
    FILE_MAIN:("5033db434dfca909a256df4ed18ae6599fa0afb3c83fa956528b75dda1ef9ffe",160),
    FILE_PAIR:("7f00bbe673eb849c11de5b7fcbeb2d2b60012765cde0f1f6bc25168dd6aedfc5",1363),
    FILE_PATERNITY:("984d60b26e870c58252b39177d923fa0707af6ea62acadfa9bf8f497da1ce6a6",1099),
}
KNOWN_MISSING={"","NA","NaN","NAN","NULL","None","none","null"}
SPEC="research/qpf_independent_2026/QPF007_PARENTAGE_PARTNER_SOURCE_FREEZE_20261118.md"

def valid_name(s):
    return bool(s) and s.strip() not in KNOWN_MISSING

def tabular(data,required):
    try:text=data.decode("utf-8-sig",errors="strict")
    except UnicodeDecodeError:text=data.decode("latin-1",errors="strict")
    first=text.splitlines()[0] if text.splitlines() else ""
    if not first:raise ValueError("Source file has no first header")
    has_delimiters=any(c in first for c in ("\t",",",";","|"))
    if has_delimiters:
        sep=next(k for k in ("\t",",",";","|") if k in first)
        it=csv.reader(io.StringIO(text,newline=""),delimiter=sep)
    else:
        it=(shlex.split(line,posix=True) for line in text.splitlines())
    header=next(it,None)
    if not header:raise ValueError("Source missing header")
    header=[x.strip().strip('"') for x in header]
    if any(header.count(col)!=1 for col in required):
        raise ValueError("Original biological ID headers missing or ambiguous")
    indices={col:header.index(col) for col in required}
    row_n=0
    rows=[]
    shift_source=None
    for row in it:
        if not row or not any(x.strip() for x in row):continue
        shift=len(row)-len(header)
        if shift not in (0,1) or (shift==1 and not row[0].strip().isdigit()):
            raise ValueError("SOURCE_STOP: original text table row/header width disagreement")
        if shift_source is None:shift_source=shift
        if shift!=shift_source:
            raise ValueError("SOURCE_STOP: changing original exported row index layout")
        rows.append(tuple(row[indices[k]+shift].strip() for k in required))
        row_n+=1
        if row_n>2000:raise ValueError("Source exceeds predeclared row bound")
    return {"n_rows":row_n,"header_count":len(header),
            "headers":header,"required_cols":list(required),
            "source_extra_row_index":bool(shift_source)},rows

def author_bytes():
    manifest=load_manifest()
    source={f.get("key") or f.get("filename"):f for f in manifest["files"]}
    out={}
    for name,(expected_sha,n) in EXPECTED_SHA.items():
        if name not in source:
            raise ValueError("Original published file missing (not a phenotype result)")
        raw=trusted_binary(source[name])
        if hashlib.sha256(raw).hexdigest()!=expected_sha:
            raise ValueError("Original verified source SHA256 differs")
        out[name]=raw
    return out

def analyse():
    source=author_bytes()
    h1,main=tabular(source[FILE_MAIN],("session","ID_full"))
    h2,pairs=tabular(source[FILE_PAIR],("session","ID_full_foc","ID_full_part"))
    h3,paternity=tabular(source[FILE_PATERNITY],("offspring_id","known_id","candidate_id"))
    counts=(len(main),len(pairs),len(paternity))
    if counts!=(160,1363,1099):
        raise ValueError("Original original row count drift (main,pair,parentage)")
    if len(set(main))!=160:raise ValueError("Duplicate maternal original session plant key")
    source_sessions={x[0] for x in main}
    pair_sessions={x[0] for x in pairs}
    if (len(source_sessions),len(pair_sessions))!=(16,18):
        raise ValueError("Original 16/18 session enumeration changed")

    id_session=defaultdict(set)
    for ses,plant in main:
        id_session[plant].add(ses)
    globally_unique={p for p,s in id_session.items() if len(s)==1}
    ambiguous={p for p,s in id_session.items() if len(s)>1}
    # Build exact directed focal→partner keys *within original experimental session*.
    original=set(main)
    exact=[]
    exact_both_focal=Counter()
    source_pair_session_cat=Counter()
    for ses,focal,partner in pairs:
        in_session=ses in source_sessions
        foc=(ses,focal) in original
        par=(ses,partner) in original
        if not in_session:
            source_pair_session_cat["rows_outside_original_16_sessions"]+=1
            continue
        if not foc:
            source_pair_session_cat["rows_in_16_sessions_focal_not_in_main"]+=1
        if not par:
            source_pair_session_cat["rows_in_16_sessions_partner_not_in_main"]+=1
        if foc and par:
            exact.append((ses,focal,partner))
            exact_both_focal[(ses,focal)]+=1
    distinct_pairs=set(exact)
    nonself={x for x in distinct_pairs if x[1]!=x[2]}
    # Consistent original parentage file is a candidate only; absent session
    # is NOT filled from ID suffixes or matching row order.
    known=Counter()
    candidate=Counter()
    off=Counter()
    for child,mother,father_candidate in paternity:
        if valid_name(child):off[child]+=1
        for v,counter in ((mother,known),(father_candidate,candidate)):
            if valid_name(v):
                counter[v]+=1
    known_exact=sum(v for k,v in known.items() if k in globally_unique)
    known_ambig=sum(v for k,v in known.items() if k in ambiguous)
    candidate_exact=sum(v for k,v in candidate.items() if k in globally_unique)
    candidate_ambig=sum(v for k,v in candidate.items() if k in ambiguous)
    apparent_mother_ambig=known_ambig+sum(v for k,v in known.items() if k not in id_session)
    apparent_father_ambig=candidate_ambig+sum(v for k,v in candidate.items() if k not in id_session)
    # Name equality != parentage assignment. This gate NEVER opens seed counts.
    source_row_counts={
        "individual_main":len(main),"visit_partner_directed":len(pairs),
        "genotyped_offspring_paternity":len(paternity)
    }
    sess_foc=defaultdict(set)
    for ses,focal,partner in distinct_pairs:
        sess_foc[ses].add(focal)
    eligible_sess=[s for s in source_sessions
                   if len(sess_foc[s])>=3
                   and sum((ses==s and f!=p) for ses,f,p in distinct_pairs)>=10]
    numeric_eligibility=len(eligible_sess)>=12
    # Need correctly certified parentage roles, IDs and 80% assigned offspring
    # before any partner-calibration test, even if structural overlap looks good.
    assay_gate=("PARENTAGE_PARTNER_IDENTITY_STOP"
                if not numeric_eligibility or apparent_mother_ambig or apparent_father_ambig
                else "AUTHOR_ROLE_AND_ASSIGNMENT_SEMANTICS_VERIFICATION_REQUIRED")
    return {
      "status":"ORIGINAL_ID_ONLY_KEY_AUDIT_COMPLETE",
      "postprimary_exploratory_source":True,
      "freeze":SPEC,
      "source_original_paper":"10.1371/journal.pbio.3003579",
      "source_original_zenodo":"10.5281/zenodo.21628183",
      "source_sha256":{k:v[0] for k,v in EXPECTED_SHA.items()},
      "source_rows":source_row_counts,
      "source_headers": {
          "main":h1["headers"],"directed_partner":h2["headers"],
          "raw_parentage":h3["headers"]
      },
      "original_main_mother_session_count":len(source_sessions),
      "directed_partner_source_session_count":len(pair_sessions),
      "extra_pair_source_sessions_not_in_main":len(pair_sessions-source_sessions),
      "source_globally_unique_mother_label_count":len(globally_unique),
      "source_id_labels_reused_across_sessions":len(ambiguous),
      "source_original_mother_session_pairs":len(original),
      "source_exact_valid_directed_partner_rows":len(exact),
      "source_exact_unique_directed_partner_pairs":len(distinct_pairs),
      "source_exact_unique_nonself_directed_pairs":len(nonself),
      "source_duplicate_directed_partner_key_count":len(exact)-len(distinct_pairs),
      "source_partner_rows_self_linked":sum(f==p for s,f,p in exact),
      "source_partner_row_identity_exclusions":dict(source_pair_session_cat),
      "source_exact_focal_mother_keys_with_both_partner_IDs":len(exact_both_focal),
      "source_sessions_with_3plus_focal_mothers_and_10plus_unique_directed_pairs":len(eligible_sess),
      "source_parentage_1099_offspring_rows_with_known_id_literal_unique_mother_ID":known_exact,
      "source_parentage_1099_offspring_rows_with_candidate_id_literal_unique_plant_ID":candidate_exact,
      "source_parentage_1099_known_id_ambiguous_or_unmatched_to_main":apparent_mother_ambig,
      "source_parentage_1099_candidate_id_ambiguous_or_unmatched_to_main":apparent_father_ambig,
      "source_parentage_known_id_unique_tokens":len(known),
      "source_parentage_candidate_id_unique_tokens":len(candidate),
      "source_parentage_offspring_ID_unique_nonmissing":len(off),
      "source_parentage_duplicate_offspring_ID_strings":sum(z>1 for z in off.values()),
      "parentage_role_and_true_father_certified":False,
      "original_pairwise_seed_or_visitation_numeric_values_read":False,
      "original_paternity_genetic_outcomes_read":False,
      "original_source_data_or_plant_IDs_exported":False,
      "independent_original_studies":1,
      "previous_original_QPF007_COVERAGE_STOP_unchanged":True,
      "decision":assay_gate,
      "effect_or_predictive_association_estimated":False,
    }

def synthetic():
    h,rows=tabular(b'"session" "ID_full" "nb_visit"\n"1" "A" "22"\n"2" "B" "16"\n',
                   ("session","ID_full"))
    assert rows==[("1","A"),("2","B")]
    h2,r2=tabular(b'"session" "ID_full"\n1 "S" "P"\n2 "T" "Q"\n',
                  ("session","ID_full"))
    assert r2==[("S","P"),("T","Q")]
    print("QPF007_PARTNER_PARENTAGE_ID_SOURCE_SYNTHETIC_PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",required=True,type=Path)
    ap.add_argument("--self-test",action="store_true")
    args=ap.parse_args()
    if args.self_test:synthetic();return 0
    try:r=analyse()
    except Exception as exc:
        r={"status":"PARENTAGE_SOURCE_OR_ID_STOP",
           "error_type":type(exc).__name__,
           "reason":str(exc)[:160],
           "effect_or_predictive_association_estimated":False,
           "original_source_data_or_plant_IDs_exported":False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    brief={k:v for k,v in r.items() if k in (
        "status","decision","original_main_mother_session_count",
        "directed_partner_source_session_count",
        "source_original_mother_session_pairs",
        "source_exact_valid_directed_partner_rows",
        "source_exact_unique_directed_partner_pairs",
        "source_exact_focal_mother_keys_with_both_partner_IDs",
        "source_globally_unique_mother_label_count",
        "source_id_labels_reused_across_sessions",
        "source_partner_row_identity_exclusions",
        "source_parentage_1099_offspring_rows_with_known_id_literal_unique_mother_ID",
        "source_parentage_1099_offspring_rows_with_candidate_id_literal_unique_plant_ID",
        "source_parentage_1099_known_id_ambiguous_or_unmatched_to_main",
        "source_parentage_1099_candidate_id_ambiguous_or_unmatched_to_main",
        "source_sessions_with_3plus_focal_mothers_and_10plus_unique_directed_pairs",
        "effect_or_predictive_association_estimated","reason")}
    print("QPF007_PARTNER_PARENTAGE_SOURCE "+json.dumps(brief,sort_keys=True),flush=True)
    return 0 if r["status"]=="ORIGINAL_ID_ONLY_KEY_AUDIT_COMPLETE" else 1

if __name__=="__main__":
    raise SystemExit(main())
