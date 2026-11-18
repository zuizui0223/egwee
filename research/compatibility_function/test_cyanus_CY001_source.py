"""CY001 source/estimand gate. No unpublished maternal rpm/seed outcomes opened."""
import json
from pathlib import Path
from unittest.mock import patch
import subprocess
import unittest

import audit_cyanus_CY001_source as cy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PROTOCOL=HERE/"CY001_FROZEN_PLOT_HOLDOUT_PROTOCOL_20261118.json"
FROZEN="a118ab77e71a097b46d264738e34c0428384a304"

class CY001SourceTests(unittest.TestCase):
    def test_protocol_byte_identical_and_ancestral(self):
        source=subprocess.check_output(
            ["git","show",FROZEN+":research/compatibility_function/CY001_FROZEN_PLOT_HOLDOUT_PROTOCOL_20261118.json"],
            cwd=ROOT)
        self.assertEqual(source,PROTOCOL.read_bytes())
        subprocess.run(["git","merge-base","--is-ancestor",FROZEN,"HEAD"],
                       cwd=ROOT,check=True)
        p=json.loads(source)
        self.assertEqual(p["status"],"prospectively_locked_before_numeric_dataset_access")
        self.assertEqual(p["source"]["doi"],cy.DOI)
        self.assertEqual(p["published_frame"]["selected_genetic_mother_n"],33)
        self.assertEqual(p["published_frame"]["plots_with_mothers_n"],12)
        self.assertEqual(p["published_frame"]["parents_subsampled_from_n"],64)
        self.assertIn(">=20",p["published_frame"]["seed_screen"])
        self.assertIn("MSE",p["primary"]["estimand"])
        self.assertIn("5%",p["primary"]["positive_gate"])

    def test_actual_access_receipt_pins_original_source_without_values(self):
        receipt=json.loads((
            HERE / "CY001_SOURCE_ACCESS_RECEIPT_20261118.json"
        ).read_text(encoding="utf-8"))
        from run_cyanus_CY001_plot_holdout import ORIGINAL_SOURCE_SHA256
        original=next(
            x for x in receipt["source_manifest_from_official_Dryad_API"]
            if x["name"]=="Data_Dryad.xlsx"
        )
        self.assertEqual(original["bytes"],27995)
        self.assertEqual(original["digest_type"],"sha-256")
        self.assertEqual(original["digest"],ORIGINAL_SOURCE_SHA256)
        self.assertEqual(receipt["status"],"SOURCE_ACCESS_STOP_NO_RAW_OUTCOME_TEST")
        self.assertTrue(receipt["source_metadata_verified"])
        self.assertFalse(receipt["new_rpm_prediction_computed"])
        self.assertFalse(receipt["new_seed_prediction_computed"])
        self.assertFalse(receipt["raw_original_files_redistributed"])

    def test_access_denied_is_a_data_stop_not_ecological_null(self):
        fake={
          "source_metadata_status":"verified",
          "source_files_status":"verified_metadata",
          "public_file_inventory":[{"name":"Data_Dryad.xlsx"}],
          "missing_expected_filenames":[],
          "source_workbook_schemas":[{
            "source_file":"Data_Dryad.xlsx",
            "schema_status":"public_download_access_stop",
            "reason":"HTTPError: HTTP Error 401"
          }]
        }
        with patch.object(cy,"metadata_for_one",return_value=fake):
            result=cy.check()
        self.assertEqual(result["status"],"SOURCE_ACCESS_STOP_NO_RAW_OUTCOME_TEST")
        self.assertFalse(result["offspring_rpm_values_read"])
        self.assertFalse(result["seed_outcome_values_read"])
        self.assertFalse(result["same_original_row_join_verified"])
        self.assertEqual(result["file_inventory_count"],1)

    def test_header_receipt_does_not_count_as_33_row_source_join(self):
        fake={
          "source_metadata_status":"verified",
          "source_files_status":"verified_metadata",
          "public_file_inventory":[{"name":"Data_Dryad.xlsx"}],
          "missing_expected_filenames":[],
          "source_workbook_schemas":[{
            "source_file":"Data_Dryad.xlsx",
            "schema_status":"verified_first_row_schema_only",
            "worksheets":[{"worksheet_xml":"xl/worksheets/sheet1.xml",
                           "physical_rows_including_header":34,
                           "first_row_field_count":29,
                           "header_cells":["Maternal_plant_identifier","rpm_progeny"],
                           "data_rows_or_outcome_values_read":False}]
          }]
        }
        with patch.object(cy,"metadata_for_one",return_value=fake):
            result=cy.check()
        self.assertEqual(result["status"],"HEADERS_AVAILABLE_NO_OUTCOME_EXAMINED")
        self.assertEqual(result["decision"],"NEXT_VALIDATE_33_MOTHERS_12_PLOTS_BEFORE_RESPONSE")
        self.assertFalse(result["same_original_row_join_verified"])
        self.assertFalse(result["reproduction_or_paternity_effect_fitted"])

if __name__=="__main__":
    unittest.main()
