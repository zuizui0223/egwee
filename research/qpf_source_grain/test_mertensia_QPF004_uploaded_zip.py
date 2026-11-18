"""QPF004 exact-source ZIP identity and XLSX morphology, synthetic only.

No third-party PDF content read, source phenotype values or original files used.
"""
from __future__ import annotations

from io import BytesIO
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import audit_mertensia_QPF004_uploaded_zip_schema as m


def fake_xlsx():
    b=BytesIO()
    with zipfile.ZipFile(b,"w") as z:
        z.writestr(
            "xl/worksheets/sheet1.xml",
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<sheetData>'
            '<row r="1"><c r="A1" t="inlineStr"><is><t>fake</t></is></c></row>'
            '<row r="2"><c r="AB2"><v>742591</v></c></row>'
            '</sheetData></worksheet>'
        )
    return b.getvalue()


class MertensiaOriginalZipGate(unittest.TestCase):
    def test_official_published_file_roster_is_four_not_two_independent_studies(self):
        self.assertEqual(len(m.ORIGINAL_FILES),4)
        self.assertEqual(sum(x.endswith(".xlsx") for x in m.ORIGINAL_FILES),2)
        self.assertEqual(sum(x.endswith(".pdf") for x in m.ORIGINAL_FILES),2)
        self.assertEqual(m.ORIGINAL_FILES[
            "gallagher&campbell_phenologyExperimentData.xlsx"]["bytes"],96329)
        self.assertEqual(m.ORIGINAL_FILES[
            "gallagher&campbell_pollinatorEffectivenessData.xlsx"]["bytes"],77873)
        self.assertEqual(
            m.ORIGINAL_FILES["gallagher&campbell_phenologyExperimentData.xlsx"]["sha256"],
            "51263c0cabe9dd04dbf716a4594e7d700c5235dd3f85a65ab51f43fcef828411"
        )
        self.assertEqual(
            m.ORIGINAL_FILES["gallagher&campbell_pollinatorEffectivenessData.xlsx"]["sha256"],
            "bbfcbbaf43b53b0ef835b891bd8932ae3761a383e4ecb1f38440a4ba9d477c38"
        )

    def test_synthetic_xlsx_exports_only_sheet_structure(self):
        out=m.workbook_shape(fake_xlsx())
        self.assertEqual(len(out),1)
        self.assertEqual(out[0]["physical_source_rows"],2)
        self.assertEqual(out[0]["max_source_column_index"],28)
        self.assertFalse(out[0]["first_row_values_or_biological_data_read"])
        self.assertNotIn("742591",str(out))
        self.assertEqual(m.colindex("AB1"),28)
        with self.assertRaises(ValueError):
            m.colindex("***")

    def test_original_file_sha_crc_and_size_gate_fail_closed(self):
        content=fake_xlsx()
        dummy=b"%PDF-original-not-present-but-synthetic"
        expected={
            "experiment.xlsx":{"bytes":len(content),
                               "sha256":hashlib.sha256(content).hexdigest()},
            "metadata.pdf":{"bytes":len(dummy),
                            "sha256":hashlib.sha256(dummy).hexdigest()}
        }
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"source.zip"
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("subdir/experiment.xlsx",content)
                z.writestr("subdir/metadata.pdf",dummy)
            got=m.verify_original_files(p,expected=expected)
            self.assertEqual(set(got),set(expected))
            self.assertEqual(m.workbook_shape(got["experiment.xlsx"])[0]
                             ["physical_source_rows"],2)
            with zipfile.ZipFile(p,"w") as z:
                z.writestr("experiment.xlsx",content+b"changed")
                z.writestr("metadata.pdf",dummy)
            with self.assertRaises(ValueError):
                m.verify_original_files(p,expected=expected)

    def test_no_original_outcome_data_claimed(self):
        with patch.object(m,"verify_original_files",return_value={
            name:(fake_xlsx() if name.endswith(".xlsx") else b"mock-pdf")
            for name in m.ORIGINAL_FILES
        }):
            with tempfile.TemporaryDirectory() as d:
                source=Path(d)/"synthetic.zip"
                source.write_bytes(b"fake-test-only")
                result=m.audit(source)
        self.assertEqual(result["correct_species"],"Mertensia ciliata")
        self.assertEqual(result["status"],"EXACT_ORIGINAL_ALL4_FILES_VERIFIED_SCHEMA_ONLY")
        self.assertFalse(result["first_row_or_biological_values_read"])
        self.assertFalse(result["pdf_contents_read"])
        self.assertFalse(result["original_field_plant_ramet_flower_ID_joins_verified"])
        self.assertFalse(result["new_original_QPF_effects_fitted"])
        self.assertFalse(result["individual_raw_source_redistributed"])

if __name__=="__main__":
    unittest.main()
