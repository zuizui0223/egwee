#!/usr/bin/env python3
"""CY001: original Dryad public metadata and header-only feasibility receipt.

Never read maternal rpm, visits, seed values or genotype values in this gate.
Only official DOI/version/file API links; HTTP 401/429 => SOURCE_ACCESS_STOP.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from audit_dryad_joint_state_source_schema import metadata_for_one

DOI = "10.5061/dryad.9p8cz8ws1"

def check() -> dict:
    entry = {
        "id": "CY001",
        "programme": "Cyanus_segetum_Labonte_2024_CA_SYS_farm",
        "source_doi": DOI,
        "source_url": "https://datadryad.org/dataset/doi%3A10.5061/dryad.9p8cz8ws1",
        "expected_data_files": ["Data_Dryad.xlsx"],
    }
    info = metadata_for_one(entry)
    inventory = info.get("public_file_inventory", [])
    match = [x for x in info.get("source_workbook_schemas", [])
             if x["source_file"].casefold() == "data_dryad.xlsx"]
    ready = any(x.get("schema_status") == "verified_first_row_schema_only"
                for x in match)
    return {
        "analysis_id": "CY001_cyanus_original_source_gate",
        "status": ("HEADERS_AVAILABLE_NO_OUTCOME_EXAMINED" if ready
                   else "SOURCE_ACCESS_STOP_NO_RAW_OUTCOME_TEST"),
        "original_doi": DOI,
        "paper_doi": "10.1002/ajb2.16440",
        "programme_count": 1,
        "published_n_mothers": 33,
        "published_n_plots_with_mothers": 12,
        "published_design": "33 mothers from 64 plants with >=20 viable germinable seeds; 1 farm",
        "doi_metadata_status": info["source_metadata_status"],
        "file_inventory_status": info["source_files_status"],
        "file_inventory_count": len(inventory),
        "all_expected_filenames_found": not bool(info.get("missing_expected_filenames")),
        "source_workbook_schemas": match,
        "public_download_failed_reason": [
            {"source_file": z["source_file"], "error": z.get("reason", z.get("schema_status"))}
            for z in match if z.get("schema_status") != "verified_first_row_schema_only"
        ],
        "original_mother_rows_examined": False,
        "offspring_rpm_values_read": False,
        "seed_outcome_values_read": False,
        "same_original_row_join_verified": False,
        "reproduction_or_paternity_effect_fitted": False,
        "original_raw_workbook_redistributed": False,
        "decision": (
            "NEXT_VALIDATE_33_MOTHERS_12_PLOTS_BEFORE_RESPONSE"
            if ready else "STOP_AT_RAW_DATA_ACCESS_AND_DO_NOT_INVENT_OUTCOMES"
        ),
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    result=check()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({
        "decision":result["decision"],
        "metadata":result["doi_metadata_status"],
        "file_inventory":result["file_inventory_count"],
        "source_sheet_count":sum(len(x.get("worksheets",[]))
                                 for x in result["source_workbook_schemas"]
                                 if x.get("schema_status")=="verified_first_row_schema_only"),
        "source_errors": result["public_download_failed_reason"],
    },indent=2,ensure_ascii=False))
if __name__=="__main__":
    main()
