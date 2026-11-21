"""Offline regressions for evidence status; fixtures contain no empirical rows."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import audit_sd001_dataverse_original_source as source


class SourceGateTests(unittest.TestCase):
    @staticmethod
    def synthetic_file():
        # 186 artificial lines; no source response, identity, or genotype values.
        raw = b"ColumnA,ColumnB\n" + b"1,2\n" * 186
        return raw, {"dataFile": {"id": 765423, "filesize": len(raw),
                     "contentType": "text/tab-separated-values",
                     "md5": hashlib.md5(raw).hexdigest()}}

    def test_missing_publisher_digest_cannot_certify_source(self):
        raw, item = self.synthetic_file()
        item["dataFile"].pop("md5")
        with patch.object(source, "official_bytes", return_value=(raw, "text/csv")):
            result = source.one_file(item, "pollen_counts_on_stigmas.tab")
        self.assertEqual(result["status"], "ORIGINAL_SOURCE_ACCESS_OR_SEMANTICS_STOP")
        self.assertNotIn("original_field_labels", result)

    def test_original_download_uses_original_representation_size(self):
        raw, item = self.synthetic_file()
        item["dataFile"].update({"filesize": len(raw) + 100,
                                "originalFileSize": len(raw),
                                "originalFileName": "synthetic.csv",
                                "originalFileFormat": "text/csv"})
        with patch.object(source, "official_bytes", return_value=(raw, "text/csv")):
            result = source.one_file(item, "pollen_counts_on_stigmas.tab")
        self.assertEqual(result["status"], "PUBLISHED_SOURCE_ORIGINAL_HEADER_AND_LINE_COUNT_VERIFIED")
        self.assertTrue(result["original_source_MD5_pass"])
        self.assertEqual(result["verified_nonempty_original_data_rows"], 186)

    def test_unreleased_version_cannot_certify_published_source(self):
        version = {"datasetPersistentId": "doi:10.57745/CF1VNW", "versionState": "DRAFT",
                   "files": [{"label": name} for name in source.FILE_EXPECTED]}
        raw = json.dumps({"status": "OK", "data": {"latestVersion": version}}).encode()
        with patch.object(source, "official_bytes", return_value=(raw, "application/json")), \
             patch.object(source, "one_file", return_value={
                 "status": "PUBLISHED_SOURCE_ORIGINAL_HEADER_AND_LINE_COUNT_VERIFIED"}):
            result = source.audit()
        self.assertEqual(result["status"], "SOURCE_METADATA_OR_OFFICIAL_ID_STOP")

    def test_network_timeout_still_writes_stop_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "receipt.json"
            with patch.object(source, "official_bytes", side_effect=TimeoutError("read timed out")), \
                 patch("sys.argv", ["audit", "--output", str(dest)]), \
                 contextlib.redirect_stdout(io.StringIO()):
                code = source.main()
            self.assertEqual(code, 2)
            result = json.loads(dest.read_text())
            self.assertEqual(result["status"], "SOURCE_METADATA_OR_OFFICIAL_ID_STOP")
            self.assertEqual(result["source_stop_type"], "TimeoutError")

    def test_file_timeout_returns_source_stop(self):
        _, item = self.synthetic_file()
        with patch.object(source, "official_bytes", side_effect=TimeoutError("read timed out")):
            result = source.one_file(item, "pollen_counts_on_stigmas.tab")
        self.assertEqual(result["status"], "ORIGINAL_SOURCE_ACCESS_OR_SEMANTICS_STOP")
        self.assertEqual(result["source_stop_type"], "TimeoutError")

    def test_source_stop_preserves_receipt_but_fails_cli(self):
        # Regression: a successful audit execution must not certify failed access.
        for status in ("SOURCE_METADATA_OR_OFFICIAL_ID_STOP",
                       "PUBLIC_ORIGINAL_SOURCE_ACCESS_OR_SCHEMA_STOP"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as tmp:
                dest = Path(tmp) / "receipt.json"
                result = {"status": status, "source_stop_http": 503}
                with patch.object(source, "audit", return_value=result), \
                     patch("sys.argv", ["audit", "--output", str(dest)]), \
                     contextlib.redirect_stdout(io.StringIO()):
                    code = source.main()
                self.assertEqual(code, 2)
                self.assertEqual(json.loads(dest.read_text()), result)

    def test_verified_status_succeeds_without_changing_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "receipt.json"
            result = {"status": "TWO_ORIGINAL_SOURCE_SCHEMAS_VERIFIED_NO_BIOLOGICAL_JOIN"}
            with patch.object(source, "audit", return_value=result), \
                 patch("sys.argv", ["audit", "--output", str(dest)]), \
                 contextlib.redirect_stdout(io.StringIO()):
                code = source.main()
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(dest.read_text()), result)


if __name__ == "__main__":
    unittest.main()
