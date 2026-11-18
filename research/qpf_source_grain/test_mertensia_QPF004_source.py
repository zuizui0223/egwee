"""QPF004 primary-source identity + independent biological grain, source withheld.

Synthetic mock source metadata. No original flowers, pollen, fruits, plants, or
experimental Excel/PDF contents downloaded or imported into public CI tests.
"""
from __future__ import annotations
import json
from pathlib import Path
from unittest.mock import patch
import unittest
import audit_mertensia_QPF004_public_source as study

HERE=Path(__file__).resolve().parent
LOCK=HERE/"QPF004_MERTENSIA_SOURCE_ARCHITECTURE_LOCK_20261118.json"


class MertensiaQPF004SourceTests(unittest.TestCase):
    def test_identification_correction_and_original_design_preserved(self):
        p=json.loads(LOCK.read_text(encoding="utf-8"))
        self.assertEqual(p["source"]["corrected_species"],"Mertensia ciliata (James ex Torr.) G.Don")
        self.assertEqual(p["original_atlas_error"]["incorrect_label"],"Mimulus/Erythranthe ciliata")
        self.assertEqual(p["source"]["source_paper_doi"],"10.1002/ajb2.1439")
        self.assertEqual(p["source"]["source_doi"],study.DOI)
        self.assertEqual(study.PUBLISHED_SEPARATE_COHORTS["phenology_2015"]["flowering_plants"],40)
        self.assertTrue(study.PUBLISHED_SEPARATE_COHORTS["phenology_2015"]["week4_cut_flower_display_intervention"])
        self.assertEqual(study.PUBLISHED_SEPARATE_COHORTS["single_visit_2016"]["single_visit_ramets"],95)
        self.assertEqual(study.PUBLISHED_SEPARATE_COHORTS["single_visit_2016"]["marked_visited_flowers"],235)
        self.assertNotEqual(study.PUBLISHED_SEPARATE_COHORTS["single_visit_2016"]["published_pollen_assays_n"],235)
        self.assertEqual(study.PUBLISHED_SEPARATE_COHORTS["single_visit_2016"]["published_seed_assays_n"],232)

    def test_missing_original_xlsx_stops_before_biological_effect(self):
        fake={
          "source_metadata_status":"verified",
          "source_files_status":"verified_metadata",
          "public_file_inventory":[
            {"name":study.EXPECTED_XLSX[0],"bytes_declared":96330,
             "digest":"sha256-placeholder","digest_type":"sha-256"},
            {"name":study.EXPECTED_XLSX[1],"bytes_declared":77870,
             "digest":"sha256-placeholder","digest_type":"sha-256"},
          ],
          "missing_expected_filenames":[],
          "source_workbook_schemas":[
            {"source_file":name,"schema_status":"public_download_access_stop",
             "reason":"HTTPError: HTTP Error 401: Unauthorized"}
            for name in study.EXPECTED_XLSX
          ]
        }
        with patch.object(study,"metadata_for_one",return_value=fake):
            result=study.source_metadata()
        self.assertTrue(result["source_metadata_checked"])
        self.assertFalse(result["source_xlsx_structural_headers_verified"])
        self.assertFalse(result["original_plant_flower_ramet_key_overlap_verified"])
        self.assertFalse(result["original_experiment_outcomes_read"])
        self.assertFalse(result["new_original_QPF_effects_estimated"])
        self.assertEqual(result["decision"],"ORIGINAL_EXPERIMENT_XLSX_ACCESS_STOP_NO_JOIN_OR_EFFECT")

    def test_schema_only_headers_do_not_establish_matched_ramet(self):
        fake={
          "source_metadata_status":"verified",
          "source_files_status":"verified_metadata",
          "public_file_inventory":[],
          "missing_expected_filenames":[],
          "source_workbook_schemas":[
            {"source_file":name,"schema_status":"verified_first_row_schema_only",
             "worksheets":[{"worksheet_xml":"xl/worksheets/sheet1.xml",
                            "physical_rows_including_header":300,
                            "first_row_field_count":14,
                            "header_cells":["site","treatment","Plant_ID"],
                            "data_rows_or_outcome_values_read":False}]}
            for name in study.EXPECTED_XLSX
          ]
        }
        with patch.object(study,"metadata_for_one",return_value=fake):
            result=study.source_metadata()
        self.assertTrue(result["source_xlsx_structural_headers_verified"])
        self.assertEqual(result["decision"],"NEXT_VALIDATE_EXACT_2016_FLOWER_RAMET_POLLEN_SEED_JOIN")
        self.assertFalse(result["original_plant_flower_ramet_key_overlap_verified"])
        self.assertFalse(result["original_experiment_outcomes_read"])

    def test_year_cohorts_are_not_falsely_linked_by_species(self):
        p=json.loads(LOCK.read_text(encoding="utf-8"))
        a=p["two_separate_experimental_frames"]["phenology_2015"]
        b=p["two_separate_experimental_frames"]["single_visit_2016"]
        self.assertIn("plant",a["candidate_join_grain"])
        self.assertIn("ramet",b["candidate_join_grain"])
        self.assertFalse(p["schema_only_decision"]["biological_source_XLSX_downloaded"])
        self.assertEqual(p["schema_only_decision"]["original_programmes_added_to_atlas"],0)
        self.assertFalse((HERE/study.EXPECTED_XLSX[0]).exists())
        self.assertFalse((HERE/study.EXPECTED_XLSX[1]).exists())

if __name__=="__main__":
    unittest.main()
