#!/usr/bin/env python3
"""QPF006 Penstemon 2026 public-original source/independent-experiment gate.

Only official Dryad DOI/version/file manifest and workbook FIRST-row schema
are accessed when publicly reachable. No original biological signed outcomes,
individual flower/plant IDs, stigma/seed values or untrusted authors' scripts
read or redistributed. Explicit primary paper/README experiment nonjoin is a
design issue and cannot be fixed by matching common Year/Day labels.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"compatibility_function"))
from audit_dryad_joint_state_source_schema import metadata_for_one

DOI="10.5061/dryad.xpnvx0kwt"
PAPER="10.1002/njb.04977"
WORKBOOKS=(
    "Breed_system_data.xlsx",
    "Pollen_tubes_base.xlsx",
    "Pollen_tubes_top.xlsx",
    "Seeds_over_day_and_year.xlsx",
    "Single_visit_pollen_deposition.xlsx",
    "Stigma_pollen_grains.xlsx",
    "Stigma_pollen_over_day_and_year.xlsx",
)
OTHER_EXPECTED="README.md"


def audit()->dict:
    info=metadata_for_one({
      "id":"QPF006",
      "programme":"Penstemon_digitalis_Dieringer_Cabrera_2026",
      "source_doi":DOI,
      "source_url":"https://datadryad.org/dataset/doi%3A10.5061/dryad.xpnvx0kwt",
      "expected_data_files":list(WORKBOOKS)
    })
    schema=info.get("source_workbook_schemas",[])
    accessible=sum(x.get("schema_status")=="verified_first_row_schema_only"
                   for x in schema)
    result={
      "audit_id":"QPF006_original_source_separate_experiments_access",
      "status":"PUBLISHED_README_SOURCE_EXPERIMENTS_NOT_SAME_FLOWER_QPF",
      "source_doi":DOI,"original_paper_doi":PAPER,
      "primary_paper_2026":"Adaptive floral traits that impact stigma pollen load and seed production in Penstemon digitalis",
      "official_dryad_metadata_status":info.get("source_metadata_status"),
      "official_dryad_file_inventory_status":info.get("source_files_status"),
      "original_source_manifest":info.get("public_file_inventory",[]),
      "source_XLSX_required":len(WORKBOOKS),
      "source_XLSX_headers_successfully_retrieved":accessible,
      "source_XLSX_access_receipts":[{
          "file":s.get("source_file"),"status":s.get("schema_status"),
          "error":s.get("reason"),
          "worksheet_headers":s.get("worksheets",[])
      } for s in schema],
      "no_original_biological_source_rows_examined":True,
      "no_individual_flower_or_plant_IDs_joined":True,
      "no_original_mature_seed_P_Q_observations_fitted":True,
      "no_third_party_source_redistributed":True,
      "original_published_cohort_independence":{
        "single_visit_P":"Single bee visit to virgin flower followed by destructive stigma harvest for P; no same-flower fruit response",
        "naturally_pollen_P":"Stigma pollen counts on distinct flowers sampled by year / female receptive day",
        "seeds_F":"Different flower/plant source dataset measuring seeds per fruit by year / female receptive day",
        "pollen_tubes":"Destructive tube growth assays separate from seeds",
        "original_text":"The primary paper explicitly states separate sets of plants were used for pollen deposition versus seed production and no direct individual pollen–seed relationship can be inferred.",
        "calendar_day_aggregation_is_not_same_flower_join":True,
        "source_single_visit_QP_is_not_same_flower_QPF":True,
      },
      "full_original_QPF_same_flower_eligible":False,
      "original_six_candidate_source_count_increment":0,
      "decision":"NOT_A_THIRD_SAME_UNIT_QPF_PROGRAMME_FROM_PUBLISHED_DESIGN",
    }
    return result


def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("--output",required=True,type=Path)
    x=cli.parse_args()
    out=audit()
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({
      "doi":out["source_doi"],
      "species":"Penstemon digitalis",
      "metadata":out["official_dryad_metadata_status"],
      "n_files":len(out["original_source_manifest"]),
      "n_XLSX_headers":out["source_XLSX_headers_successfully_retrieved"],
      "xlsx_failures":[{
          "file":s["file"],"reason":s["error"] or s["status"]
      } for s in out["source_XLSX_access_receipts"]
        if s["status"]!="verified_first_row_schema_only"],
      "decision":out["decision"],
      "new_effects":False
    },indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
