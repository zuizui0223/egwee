"""Penstemon QPF006 original README source experiment grain tests.

This tests a strict public source admission decision, not real phenotype
outcomes or a new hypothesis. Original raw XLSX stays outside GitHub.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch
import unittest

import audit_penstemon_QPF006_public_source as q

HERE=Path(__file__).resolve().parent
DECISION=HERE/"QPF006_PENSTEMON_SOURCE_COHORT_GATE_20261118.json"
QPF004=HERE/"QPF004_ORIGINAL_WEEK_HOLDOUT_RESULT_20261118.json"


class PenstemonSeparateAssaysTests(unittest.TestCase):
    def setUp(self):
        self.d=json.loads(DECISION.read_text(encoding="utf-8"))

    def test_original_public_source_doi_and_dataset_file_names(self):
        self.assertEqual(q.DOI,"10.5061/dryad.xpnvx0kwt")
        self.assertEqual(q.PAPER,"10.1002/njb.04977")
        self.assertEqual(len(q.WORKBOOKS),7)
        self.assertEqual(len(set(q.WORKBOOKS)),7)
        self.assertIn("Single_visit_pollen_deposition.xlsx",q.WORKBOOKS)
        self.assertIn("Seeds_over_day_and_year.xlsx",q.WORKBOOKS)
        self.assertIn("Stigma_pollen_over_day_and_year.xlsx",q.WORKBOOKS)
        self.assertEqual(q.OTHER_EXPECTED,"README.md")
        self.assertEqual(self.d["primary"]["paper_doi"],q.PAPER)

    def test_original_flower_recovery_cannot_be_created_by_filename_join(self):
        self.assertEqual(len(self.d["experiment_specific_files"]),7)
        for file in self.d["experiment_specific_files"]:
            self.assertFalse(file["complete_same_flower_QPF"])
        self.assertFalse(self.d["quality_gates"]["direct_P_and_F_on_same_flower"])
        self.assertFalse(self.d["quality_gates"]["source_full_independent_QPF_programme_eligible"])
        self.assertTrue(self.d["quality_gates"]["raw_ID_overlap_of_some_plants_unknown"])
        self.assertIn("separate",self.d["primary"]["README_semantics"])
        self.assertTrue(self.d["quality_gates"]["not_a_negative_biological_result"])

    def test_public_metadata_access_stop_remains_source_gate_not_effect(self):
        mock={
            "source_metadata_status":"verified",
            "source_files_status":"verified_metadata",
            "public_file_inventory":[{"name":name,"bytes_declared":11200}
                for name in q.WORKBOOKS]+[{"name":"README.md","bytes_declared":6670}],
            "source_workbook_schemas":[{
                "source_file":name,"schema_status":"public_download_access_stop",
                "reason":"HTTPError: HTTP Error 401"
            } for name in q.WORKBOOKS],
        }
        with patch.object(q,"metadata_for_one",return_value=mock):
            r=q.audit()
        self.assertEqual(len(r["original_source_manifest"]),8)
        self.assertEqual(r["source_XLSX_headers_successfully_retrieved"],0)
        self.assertEqual(r["decision"],"NOT_A_THIRD_SAME_UNIT_QPF_PROGRAMME_FROM_PUBLISHED_DESIGN")
        self.assertFalse(r["full_original_QPF_same_flower_eligible"])
        self.assertTrue(r["no_original_biological_source_rows_examined"])
        self.assertTrue(r["no_original_mature_seed_P_Q_observations_fitted"])
        self.assertTrue(r["no_third_party_source_redistributed"])

    def test_even_obtaining_headers_does_not_prove_same_flower(self):
        mock={
            "source_metadata_status":"verified",
            "source_files_status":"verified_metadata",
            "public_file_inventory":[],
            "source_workbook_schemas":[{
                "source_file":name,"schema_status":"verified_first_row_schema_only",
                "worksheets":[{"worksheet_xml":"xl/worksheets/sheet1.xml",
                                "physical_rows_including_header":31,
                                "header_cells":["Plant_ID","Pollen"],
                                "data_rows_or_outcome_values_read":False}]
            } for name in q.WORKBOOKS]
        }
        with patch.object(q,"metadata_for_one",return_value=mock):
            x=q.audit()
        self.assertEqual(x["source_XLSX_headers_successfully_retrieved"],7)
        self.assertFalse(x["full_original_QPF_same_flower_eligible"])
        self.assertTrue(x["no_individual_flower_or_plant_IDs_joined"])

    def test_existing_QPF_pilot_count_and_negative_result_unmodified(self):
        source=json.loads(QPF004.read_text(encoding="utf-8"))
        self.assertEqual(source["registered_decision"],"NO_PRACTICALLY_PORTABLE_POLLEN_INCREMENT")
        self.assertEqual(source["source_structure"]["source_2016_P_and_F_joined"],62)
        a=self.d["research_atlas_provenance"]
        self.assertEqual(a["original_eligible_same_unit_direct_P_programmes_before_QPF006_check"],2)
        self.assertEqual(a["original_eligible_same_unit_direct_P_programmes_after_QPF006_check"],2)
        self.assertTrue(a["minimum_3_source_common_estimand_not_met"])
        self.assertTrue(a["original_six_candidate_registry_preserved"])
        self.assertFalse((HERE/"Single_visit_pollen_deposition.xlsx").exists())
        self.assertFalse((HERE/"Seeds_over_day_and_year.xlsx").exists())

if __name__=="__main__":
    unittest.main()
