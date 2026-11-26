#!/usr/bin/env python3
"""Synthetic, source-free tests for Lupinus 2026 Figshare provenance and XLSX schema gate."""
import io
import unittest
from zipfile import ZipFile
import audit_lupinus_2026_in_situ_source as source

class SourceGateTests(unittest.TestCase):
    def test_registered_article_doi(self):
        self.assertTrue(source.check_doi("10.6084/m9.figshare.29606180.v1"))
        self.assertFalse(source.check_doi("10.6084/m9.figshare.28304024.v2"))
    def test_only_official_metadata_source(self):
        with self.assertRaises(ValueError):
            source.source_url("https://example.org/v2/articles/29606180",metadata=True)
        self.assertEqual(source.source_url("https://api.figshare.com/v2/articles/29606180",metadata=True),
                         "https://api.figshare.com/v2/articles/29606180")
    def test_headers_not_outcomes(self):
        buf=io.BytesIO()
        with ZipFile(buf,"w") as z:
            z.writestr("xl/worksheets/sheet1.xml",(
                '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                '<sheetData>'
                '<row r="1"><c r="A1" t="inlineStr"><is><t>family</t></is></c>'
                '<c r="B1" t="inlineStr"><is><t>seed_count</t></is></c></row>'
                '<row r="2"><c r="A2" t="inlineStr"><is><t>SENSITIVE_ID</t></is></c>'
                '<c r="B2"><v>999</v></c></row>'
                '</sheetData></worksheet>').encode())
        parsed=source.schema_of_xlsx(buf.getvalue())
        self.assertEqual(parsed[0]["physical_rows"],2)
        self.assertEqual(parsed[0]["first_row_headers"],["family","seed_count"])
        self.assertNotIn("SENSITIVE_ID",str(parsed))
        self.assertNotIn("999",str(parsed))

if __name__=="__main__":
    unittest.main()
