#!/usr/bin/env python3
"""QPF004 Mertensia source gate: original Dryad metadata + XLSX header only.

This is a 2020 experimental source architecture feasibility audit, NEVER a
pollinator/pollen/seed outcome test. The published study contains separate
2015 flowering manipulation and 2016 wild single-visit experiments. Unlinked
mother/ramet/flower observations must NOT be combined on taxon identity alone.

Source files are fetched only through the verified official Dryad v2 dataset
metadata -> version -> file download links. On 401, 403, 429 or missing source
links the biological join is STOP, not ecological null. PDFs are inventoried,
not read. Raw original third-party XLSX/PDF never published by this script.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
SRC=HERE.parents[1]/"compatibility_function"
sys.path.insert(0,str(SRC))
from audit_dryad_joint_state_source_schema import metadata_for_one

DOI="10.7280/D19X0D"
EXPECTED_XLSX=(
    "gallagher&campbell_phenologyExperimentData.xlsx",
    "gallagher&campbell_pollinatorEffectivenessData.xlsx",
)
PUBLISHED_SEPARATE_COHORTS={
    "phenology_2015":{
        "flowering_plants":40,
        "phenology_weeks":4,
        "week4_cut_flower_display_intervention":True,
        "joint_id_grain":"plant/array/week, not proof of same flower pollen and seed"
    },
    "single_visit_2016":{
        "single_visit_ramets":95,
        "marked_visited_flowers":235,
        "published_pollen_assays_n":62,
        "published_seed_assays_n":232,
        "open_control_ramets":65,
        "bagged_control_ramets":74,
        "joint_id_grain":"marked flower or ramet/clone/site and pollinator taxon, overlap not yet verified"
    }
}


def source_metadata():
    out={
      "audit_id":"QPF004_Mertensia_original_source_access_and_grain",
      "status":"PUBLISHED_ORIGINAL_GRAIN_VERIFIED_RAW_JOIN_PENDING",
      "correct_source_species":"Mertensia ciliata",
      "incorrect_QPF004_registry_species":"Mimulus/Erythranthe ciliata",
      "paper_doi":"10.1002/ajb2.1439",
      "source_doi":DOI,
      "separate_published_cohorts":PUBLISHED_SEPARATE_COHORTS,
      "source_metadata_checked":False,
      "source_xlsx_structural_headers_verified":False,
      "original_plant_flower_ramet_key_overlap_verified":False,
      "original_experiment_outcomes_read":False,
      "new_original_QPF_effects_estimated":False,
      "original_raw_source_redistributed":False,
    }
    entry={
      "id":"QPF004",
      "programme":"Mertensia_ciliata_Gallagher_Campbell_2020",
      "source_doi":DOI,
      "source_url":"https://datadryad.org/dataset/doi%3A10.7280/D19X0D",
      "expected_data_files":list(EXPECTED_XLSX),
    }
    source=metadata_for_one(entry)
    out["original_metadata_status"]=source["source_metadata_status"]
    out["source_metadata_checked"]=source["source_metadata_status"]=="verified"
    out["source_file_inventory_status"]=source["source_files_status"]
    out["source_manifest"]=source.get("public_file_inventory",[])
    out["missing_expected_files"]=source.get("missing_expected_filenames",list(EXPECTED_XLSX))
    out["expected_xlsx_source_checks"]=source.get("source_workbook_schemas",[])
    out["all_XLSX_schemas_observed"]=(
        len(out["expected_xlsx_source_checks"])==len(EXPECTED_XLSX) and
        all(
            row.get("schema_status")=="verified_first_row_schema_only"
            for row in out["expected_xlsx_source_checks"]
        )
    )
    out["source_xlsx_structural_headers_verified"]=out["all_XLSX_schemas_observed"]
    # Even retrieving both entire XLSX schemas does not establish row-level
    # joins; never promote a source-only header gate to full Q/P/F admission.
    out["decision"]=(
      "NEXT_VALIDATE_EXACT_2016_FLOWER_RAMET_POLLEN_SEED_JOIN"
      if out["all_XLSX_schemas_observed"]
      else "ORIGINAL_EXPERIMENT_XLSX_ACCESS_STOP_NO_JOIN_OR_EFFECT"
    )
    if source.get("source_metadata_reason"):
        out["source_access_metadata_error"]=source["source_metadata_reason"]
    if source.get("source_files_reason"):
        out["source_file_inventory_error"]=source["source_files_reason"]
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    out=source_metadata()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "species":out["correct_source_species"],
        "source_doi":out["source_doi"],
        "original_metadata":out["original_metadata_status"],
        "file_inventory":out["source_file_inventory_status"],
        "files":[{"name":f.get("name"),"bytes":f.get("bytes_declared"),
                  "digest_type":f.get("digest_type"),"digest":f.get("digest")}
                 for f in out["source_manifest"]],
        "xlsx_gates":[{
            "file":r.get("source_file"),
            "status":r.get("schema_status"),
            "reason":r.get("reason"),
            "sheet_count":len(r.get("worksheets",[]))
        } for r in out["expected_xlsx_source_checks"]],
        "decision":out["decision"],
        "no_effect_fitted":True
    },indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
