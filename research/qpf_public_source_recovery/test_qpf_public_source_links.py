"""QPF public-original-source recovery checks without opening real biological rows."""
from __future__ import annotations
from io import BytesIO
import json
import unittest
from unittest.mock import patch
import zipfile

import audit_public_qpf_source_links as testit


def synthetic_xlsx() -> bytes:
    # Synthetic only: structural worksheet with a sensitive-looking fake
    # phenotype value that may never enter the source-only receipt.
    b=BytesIO()
    with zipfile.ZipFile(b,"w") as z:
        z.writestr(
            "xl/worksheets/sheet1.xml",
            """<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
                <sheetData>
                  <row r="1"><c r="A1" t="inlineStr"><is><t>focal flower</t></is></c></row>
                  <row r="2"><c r="B2"><v>999123</v></c></row>
                </sheetData>
              </worksheet>"""
        )
    return b.getvalue()


class SourceGateTests(unittest.TestCase):
    def test_filename_source_is_verified_public_link(self):
        self.assertEqual(testit.FIRST_DOI,"10.5061/dryad.hqbzkh1g9")
        self.assertEqual(testit.RELATED_ZENODO_SOFTWARE_IDS,(10563520,10563521))
        self.assertIn("file_stream/736848",testit.PUBLIC_FIRST_URL)
        for x in ("https://example.com/files/fake.xlsx",
                  "http://zenodo.org/api/records/10563521"):
            with self.assertRaises(ValueError):
                testit.source_get(x)

    def test_xlsx_sheet_structure_does_not_export_outcome_values(self):
        d=testit.sheet_structure(synthetic_xlsx())
        self.assertEqual(len(d),1)
        self.assertEqual(d[0]["physical_nonempty_rows"],2)
        self.assertEqual(d[0]["max_recorded_column_index"],2)
        self.assertFalse(d[0]["individual_values_or_outcomes_read"])
        self.assertNotIn("999123",json.dumps(d))

    def test_unsupported_binary_stops(self):
        with self.assertRaises(ValueError):
            testit.sheet_structure(b"not-excel")

    def test_original_file_available_branch_only_checks_headers(self):
        candidate=synthetic_xlsx()
        meta={
            "source_metadata_status":"verified",
            "source_files_status":"verified_metadata",
            "public_file_inventory":[{
                "name":"FIGO_2019_Data_20210523.xlsx",
                "digest":testit.hashlib.sha256(candidate).hexdigest(),
                "digest_type":"sha-256"
            }],
        }
        with patch.object(testit,"metadata_for_one",return_value=meta), \
             patch.object(testit,"source_get",return_value=(candidate,testit.PUBLIC_FIRST_URL)):
            r=testit.qpf001()
        self.assertEqual(r["decision"],"ORIGINAL_FILE_SCHEMA_RECOVERED_NO_BIOLOGICAL_OUTCOMES")
        self.assertTrue(r["matches_official_original_file_sha256"])
        self.assertFalse(r["source_value_read"])
        self.assertEqual(r["worksheet_schema"][0]["physical_nonempty_rows"],2)
        self.assertNotIn("999123",json.dumps(r))

    def test_source_access_stop_is_not_biological_null(self):
        meta={
            "source_metadata_status":"verified",
            "source_files_status":"verified_metadata",
            "public_file_inventory":[],
        }
        with patch.object(testit,"metadata_for_one",return_value=meta), \
             patch.object(testit,"source_get",side_effect=PermissionError("HTTP 401")):
            r=testit.qpf001()
        self.assertEqual(r["decision"],"SOURCE_ACCESS_STOP_NO_QPF_OUTCOMES")
        self.assertEqual(r["stream_failure_type"],"PermissionError")
        self.assertFalse(r["source_value_read"])

    def test_two_zenodo_related_work_ids_are_not_two_study_programmes(self):
        record={
            "id":10563520,
            "doi":"10.5281/zenodo.10563520",
            "metadata":{"title":"Original source software"},
            "files":[{"key":"Visitation_Rate_and_SEM.R","size":1000,
                      "checksum":"md5:00000000"}]
        }
        with patch.object(testit,"source_get",return_value=(json.dumps(record).encode(),"https://zenodo.org/api/records/10563520")):
            got=testit.software_zenodo_record(10563520)
        self.assertEqual(got["status"],"verified_metadata")
        self.assertFalse(got["original_xlsx_present"])
        self.assertFalse(got["original_biological_outcomes_read"])

if __name__=="__main__":
    unittest.main()
