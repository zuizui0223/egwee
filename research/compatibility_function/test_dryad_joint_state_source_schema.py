"""Offline tests for independent natural SI/function source schema receipt."""
from __future__ import annotations

from io import BytesIO
import json
from pathlib import Path
from unittest.mock import patch
import unittest
from zipfile import ZipFile

import audit_dryad_joint_state_source_schema as audit


class SchemaReceiptTests(unittest.TestCase):
    def test_dataset_identity_exact(self):
        audit.validate_metadata({"identifier": "doi:10.5061/dryad.pnvx0k6zm"}, "10.5061/dryad.pnvx0k6zm")
        with self.assertRaises(ValueError):
            audit.validate_metadata({"identifier": "doi:10.5061/dryad.WRONG"}, "10.5061/dryad.pnvx0k6zm")

    def test_only_official_dryad_api_routes(self):
        self.assertEqual(
            audit.safe_url("/api/v2/files/123/download"),
            "https://datadryad.org/api/v2/files/123/download",
        )
        for url in ("https://unknown.example/api/v2/files/1",
                    "https://datadryad.org/stash/special?id=1"):
            with self.assertRaises(ValueError):
                audit.safe_url(url)

    def test_xlsx_reads_header_only_and_not_second_row(self):
        # No external workbook or actual biological values enter this fixture.
        main = b'''<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
          <sheetData><row r="1"><c r="A1" t="inlineStr"><is><t>Maternal</t></is></c>
          <c r="B1" t="inlineStr"><is><t>Seed count</t></is></c></row>
          <row r="2"><c r="A2" t="inlineStr"><is><t>PRIVATE_FAKE_PLANT_ID</t></is></c>
          <c r="B2"><v>99999</v></c></row></sheetData></worksheet>'''
        buf = BytesIO()
        with ZipFile(buf, "w") as z:
            z.writestr("xl/worksheets/sheet1.xml", main)
        schema = audit.workbook_schema(buf.getvalue())
        self.assertEqual(schema[0]["physical_rows_including_header"], 2)
        self.assertEqual(schema[0]["header_cells"], ["Maternal", "Seed count"])
        self.assertNotIn("PRIVATE_FAKE_PLANT_ID", json.dumps(schema))
        self.assertNotIn("99999", json.dumps(schema))
        self.assertFalse(schema[0]["data_rows_or_outcome_values_read"])

    def test_blocked_download_is_a_stop_not_a_value_zero(self):
        row = {
            "id": "SMF001",
            "programme": "fake_original",
            "source_doi": "10.5061/dryad.pnvx0k6zm",
            "source_url": "https://datadryad.org/dataset/doi%3A10.5061/dryad.pnvx0k6zm",
            "expected_data_files": ["fake.xlsx"],
        }
        with patch.object(audit, "request_json", side_effect=ValueError("access denied")):
            result = audit.metadata_for_one(row)
        self.assertEqual(result["decision"], "SOURCE_ACCESS_STOP_NO_RAW_LINKAGE_INFERENCE")
        self.assertFalse(result["exact_biological_ID_join_verified"])
        self.assertEqual(result["source_workbook_schemas"], [])

    def test_registry_four_programmes_not_four_replications(self):
        registry = json.loads(audit.REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual([x["id"] for x in registry["programmes"]],
                         ["SMF001", "SMF002", "SMF003", "SMF004"])
        self.assertTrue(all(x["independent_programme_count"] == 1
                            for x in registry["programmes"]))
        self.assertTrue(all(x.get("expected_data_files") is not None
                            for x in registry["programmes"]))


if __name__ == "__main__":
    unittest.main()
