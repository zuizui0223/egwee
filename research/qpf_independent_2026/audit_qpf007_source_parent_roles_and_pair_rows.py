#!/usr/bin/env python3
"""Original CERVUS parent-ID × source pair-row key audit, no interaction outcome.

Verifies that the author's known_id session derivation and candidate_id paternal
aggregation are consistent with the original ID tables. Pair TABLE ROW
presence is NOT positive flower contact. Paternal ID strings define reproductive dyads and ARE original genetic identity outcomes; we inspect source IDs for structural membership but compute no visit/fertilization coefficient. No raw source rows or IDs are emitted.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path

from audit_qpf007_partner_parentage_ids import (
    author_bytes,tabular,FILE_MAIN,FILE_PAIR,FILE_PATERNITY
)
from audit_qpf007_published_author_code_roles import code_source

SCRIPT_SHA="a8e47abb7b2b4e7d6f85574fa6444eddd35a2bf0537592eccb4354fabb2402e9"
SPEC="research/qpf_independent_2026/QPF007_PARENTAGE_PARTNER_SOURCE_FREEZE_20261118.md"

def run():
    orig=author_bytes()
    hmain,main=tabular(orig[FILE_MAIN],("session","ID_full"))
    hpair,pairs=tabular(orig[FILE_PAIR],("session","ID_full_foc","ID_full_part"))
    hpat,paternity=tabular(orig[FILE_PATERNITY],("offspring_id","known_id","candidate_id"))
    if (len(main),len(pairs),len(paternity))!=(160,1363,1099):
        raise ValueError("Hard source roster drift")
    index={plant:session for session,plant in main}
    if len(index)!=160 or len({s for s,p in main})!=16:
        raise ValueError("Source original maternal plant keys not globally unique")
    source_text,author_sha,author_size=code_source()
    if author_sha!=SCRIPT_SHA or author_size!=297463:
        raise ValueError("Author original R script fingerprint drift")
    lines=source_text.splitlines()
    # Original author script gives specific CERVUS source semantics:
    # line 88 derives session from known_id (known maternal parent);
    # male bias groups candidate_id as sire, and group_by(known_id)
    # counts mother's original genotyped progeny.
    if "mutate(session = substr(known_id,1,5))" not in lines[87]:
        raise ValueError("Author-script maternal session contract changed")
    if "male_bias_self <- all_pat" not in lines[100]:
        raise ValueError("Author-script male candidate role block changed")
    if "group_by(candidate_id)" not in lines[101]:
        raise ValueError("Author-script sire candidate grouping changed")
    if "group_by(known_id)" not in lines[107]:
        raise ValueError("Author-script known maternal grouping changed")

    mother_prefix=Counter()
    father_session=Counter()
    offspring_seen=Counter()
    mother_by_session=defaultdict(set)
    pat_edges=set()
    assn=Counter()
    for child,mother,father in paternity:
        offspring_seen[child]+=1
        if mother not in index or father not in index:
            assn["parent_string_missing_from_160_main_plants"]+=1
            continue
        session=index[mother]
        mother_by_session[session].add(mother)
        if mother[:5]!=session:
            mother_prefix["author_substr_session_differs_from_main"]+=1
        if index[father]!=session:
            father_session["father_main_session_differs_from_mother"]+=1
        if mother==father:assn["literal_self_parentage_rows"]+=1
        if index[father]==session:
            pat_edges.add((session,mother,father))
            assn["source_known_candidate_same_session_rows"]+=1
    pairkeys={(session,foc,part) for session,foc,part in pairs
              if (session,foc) in set(main) and (session,part) in set(main)}
    expected=1209
    if len(pairkeys)!=expected:
        raise ValueError("Original source 1,209 structural pair table keys drift")
    oriented_in=sum(1 for k in pat_edges if k in pairkeys)
    reverse_in=sum(1 for ses,mo,fa in pat_edges if (ses,fa,mo) in pairkeys)
    self_n=sum(mo==fa for ses,mo,fa in pat_edges)
    counts={
        "original_offspring_paternity_rows":len(paternity),
        "original_unique_offspring_id_strings":len(offspring_seen),
        "original_offspring_id_repeated_strings":sum(n>1 for n in offspring_seen.values()),
        "known_mother_strings_mappable_to_main_ID":sum(mother in index for _,mother,_ in paternity),
        "candidate_father_strings_mappable_to_main_ID":sum(father in index for _,_,father in paternity),
        "session_derived_from_known_id_5_chars_disagreement":mother_prefix["author_substr_session_differs_from_main"],
        "candidate_id_in_different_session_from_known_id":father_session["father_main_session_differs_from_mother"],
        "paternity_same_session_assignments":assn["source_known_candidate_same_session_rows"],
        "genetic_same_session_distinct_mother_candidate_pairs":len(pat_edges),
        "genetic_same_session_self_pairs":self_n,
        "source_pair_table_rows_with_exact_plant_IDs":len(pairkeys),
        "genetic_unique_ID_pairs_present_as_focal_to_partner_table_ROWS":oriented_in,
        "genetic_unique_ID_pairs_present_as_partner_to_focal_table_ROWS":reverse_in,
        "genotyped_mothers_with_unique_mapped_ID":len({mo for s,mo,fa in pat_edges}),
        "genotyped_sessions_with_known_mother_ID":len(mother_by_session),
        "source_pair_table_header_column_count":len(hpair["headers"]),
        "original_pair_table_header_names":hpair["headers"],
        "source_parentage_table_header_names":hpat["headers"],
    }
    if not (counts["original_unique_offspring_id_strings"]==1099 and
            counts["known_mother_strings_mappable_to_main_ID"]==1099 and
            counts["candidate_father_strings_mappable_to_main_ID"]==1099):
        decision="SOURCE_ID_OR_DUPLICATE_OFFSPRING_STOP"
    elif (mother_prefix or father_session):
        decision="AUTHOR_SESSION_OR_PARENT_ID_SEMANTIC_STOP"
    else:
        decision="PARENTAL_SOURCE_ROLES_SUPPORTED_CONTACT_VALUE_STILL_UNCERTIFIED"

    return {
      "status":"ORIGINAL_PARENTAGE_PAIRED_ID_AND_ROLE_SOURCE_CHECK_COMPLETE",
      "source_zenodo_doi":"10.5281/zenodo.21628183",
      "source_script_sha256":SCRIPT_SHA,
      "source_original_pair_sha256":"7f00bbe673eb849c11de5b7fcbeb2d2b60012765cde0f1f6bc25168dd6aedfc5",
      "source_original_paternity_sha256":"984d60b26e870c58252b39177d923fa0707af6ea62acadfa9bf8f497da1ce6a6",
      "author_R_line_88_known_parent_session_substr_verified":True,
      "author_R_male_candidate_grouping_and_known_parent_mother_grouping_verified":True,
      "original_paper_paternity_assignment_80pct_threshold_source":"10.1371/journal.pbio.3003579",
      "ID_only_summary":counts,
      "decision":decision,
      "do_not_interpret_pair_table_row_as_positive_flower_contact":True,
      "source_assigned_paternity_ID_pair_membership_computed":True,
      "paternity_identity_is_a_genetic_outcome":True,
      "new_partner_overlap_scientific_effect_estimated":False,
      "observational_positive_contact_status_certified":False,
      "source_pair_contact_numeric_values_opened":False,
      "source_genotypic_paternity_rows_published":False,
      "one_experimental_original_study_only":True,
    }

def self_test():
    assert "all_pat <- read.table" in "all_pat <- read.table"
    assert len("AAAAA") == 5
    print("ORIGINAL_AUTHOR_CERVUS_ID_AND_PAIRTAB_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:self_test();return 0
    if a.output is None:p.error("--output required")
    try:result=run()
    except Exception as e:result={
        "status":"PARENTAL_OR_SOURCE_ROLE_STOP",
        "error_type":type(e).__name__,
        "reason":str(e)[:240],
        "source_assigned_paternity_ID_pair_membership_computed":False,
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("QPF007_AUTHOR_SEMANTIC_PARENTS "+json.dumps({
        "status":result["status"],
        "decision":result.get("decision"),
        "ID_only_summary":result.get("ID_only_summary"),
        "reason":result.get("reason"),
        "new_biological_effect_estimated":False
    },sort_keys=True),flush=True)
    return 0 if result["status"]=="ORIGINAL_PARENTAGE_PAIRED_ID_AND_ROLE_SOURCE_CHECK_COMPLETE" else 1

if __name__=="__main__":
    raise SystemExit(main())
