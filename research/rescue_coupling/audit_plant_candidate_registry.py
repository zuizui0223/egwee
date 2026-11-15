#!/usr/bin/env python3
"""Validate independent source programme grain and source-backed research coverage.

The registry stores only publication metadata and design/endpoint classifications.
It cannot estimate rescue effect sizes.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

EXPECTED = {"RC001","RC002","RC003","RC004","RC005","RC006","RC007","RC008","RC009","RC010"}
STREAMS = {
    "A_controlled_mating_function",
    "A_assisted_gene_flow_trait_fitness",
    "A_population_rescue_no_direct_F",
    "B_genotype_and_fitness_observational",
    "B_followup_trait",
    "legacy_G_W_D_benchmark_only",
    "C_simulation",
}

def audit(reg: dict, clarke: dict | None) -> dict:
    rows=reg["candidates"]
    ids=[r["id"] for r in rows]
    assert len(ids)==len(set(ids)) and set(ids)==EXPECTED
    assert all(r["publication_doi"] and r["source_evidence"] for r in rows)
    assert set(r["stream"] for r in rows)<=STREAMS
    # Sources are publications, not independent experiments; group by system_cluster.
    groups=defaultdict(list)
    for r in rows:
        groups[r["system_cluster"]].append(r["id"])
        if r["confirmed_direct_F"] and r["confirmed_molecular"] and r["stream"]=="C_simulation":
            raise ValueError("Simulation cannot count as empirical source")
    assert set(groups["Florida_ziziphus_restoration_programme"])=={"RC002","RC003"}
    assert set(groups["Lupinus_angustifolius_Spain_AGF_programme"])=={"RC004","RC005"}
    # The eight candidate cluster keys include an existing 19-study REVIEW
    # and one SIMULATION; they are not eight primary empirical replicates.
    primary_empirical = [r for r in rows if r["id"] not in ("RC008", "RC010")]
    primary_clusters = {r["system_cluster"] for r in primary_empirical}
    assert len(primary_empirical) == 8
    assert len(primary_clusters) == 6
    both=[r["id"] for r in rows if r["confirmed_direct_F"] and r["confirmed_molecular"] and r["stream"]!="C_simulation"]
    assert both==["RC001"], both
    direct=[r["id"] for r in rows if r["confirmed_direct_F"]]
    if clarke is not None:
        assert clarke["status"]=="ENDPOINT_CLASSIFIED_NO_EFFECT_DIRECTIONS_OPENED"
        assert clarke["independent_source_studies"]==19
        assert clarke["reproductive_success_rows_for_source_level_screen"]==3
        assert clarke["direct_ecological_function_confirmed_from_aggregate_source"]==0
    return {
        "status":"SCREENED_CANDIDATE_EVIDENCE_MAP_NO_POOLED_META",
        "registered_on":reg["registered_on"],
        "publication_records_total":len(rows),
        "independent_study_programme_keys_total":len(groups),
        "candidate_group_keys_including_review_and_simulation":len(groups),
        "primary_empirical_publications_in_candidate_registry":len(primary_empirical),
        "potentially_independent_primary_empirical_programmes":len(primary_clusters),
        "aggregated_existing_review_records":1,
        "simulation_records_excluded_from_empirical_meta":1,
        "currently_meta_ready_programmes_with_matched_raw_G_F_effects":0,
        "programmes_grouping_publications":{k:v for k,v in sorted(groups.items()) if len(v)>1},
        "design_classes":dict(sorted(Counter(r["stream"] for r in rows).items())),
        "public_datasets_reported":sum(bool(r["raw_dataset_reported"]) for r in rows),
        "sources_with_direct_function_outcome_confirmed":direct,
        "sources_with_molecular_and_direct_function_at_published_design_level":both,
        "molecular_and_direct_function_n_published_programmes":len({r["system_cluster"] for r in rows if r["id"] in both}),
        "raw_same_unit_linkage_verified_and_effects_estimated":0,
        "original_clarke_pre_post_rows_in_prior_meta_not_new_independent_experiments":27,
        "note":"Eight grouping keys include one 19-study literature review and one simulated model; six are candidate primary empirical programmes, not six confirmed independent eligible contrasts. Published direct endpoints do not certify recoverable same-unit molecular/functional raw data, comparable intervention contrasts, or independent cohorts. No effect signs were examined.",
        "decision":"Proceed with RC001 Dryad exact data-sheet schema and linked trial identifiers; do not pool confirmed 1 programme. Screen RC002/003 and RC004/005 as potentially overlapping programme components."
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--registry",type=Path,required=True)
    ap.add_argument("--clarke",type=Path)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    reg=json.loads(a.registry.read_text(encoding="utf-8"))
    clarke=json.loads(a.clarke.read_text(encoding="utf-8")) if a.clarke else None
    result=audit(reg,clarke)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
