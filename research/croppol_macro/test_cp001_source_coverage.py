"""Synthetic source-coverage fixtures; no CropPol source rows are embedded."""
import contextlib
import csv
import io
from http.client import IncompleteRead
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import audit_cp001_source_coverage as source


def fixture(rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=source.EXPECTED_COLUMNS)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return out.getvalue().encode()


def row(study="S1", group="G1", site="P1", year="2001", **extras):
    return {"study_id": study, "study_id2": group, "site_id": site,
            "sampling_year": year, "crop": "synthetic_crop", "country": "synthetic_country",
            **extras}


class CoverageTests(unittest.TestCase):
    def test_frozen_source_pin_and_header_digest_match_independent_contract(self):
        import hashlib
        m = source.MANIFEST
        self.assertEqual((m["release"], m["commit"], m["path"], m["expected_bytes"], m["expected_git_blob_sha1"]),
                         ("v2.1.0", "febec7dcc088ccf1bd721c41ce8dda87a2dcba1a",
                          "Final_Data/CropPol_field_level_data.csv", 2195393,
                          "cd19a354741ac40428e6b94aa1ec2ee596ff0547"))
        self.assertEqual(m["url"], "https://raw.githubusercontent.com/ibartomeus/CropPol/febec7dcc088ccf1bd721c41ce8dda87a2dcba1a/Final_Data/CropPol_field_level_data.csv")
        self.assertEqual(hashlib.sha256(",".join(source.EXPECTED_COLUMNS).encode()).hexdigest(),
                         "f2ee8b3f934bc412f649022c2349f77df18531842f4810983fa60bc721343866")
        result = source.inspect_csv(fixture([row()]))
        self.assertEqual(result.get("schema_sha256"),
                         "f2ee8b3f934bc412f649022c2349f77df18531842f4810983fa60bc721343866")

    def test_categorical_output_uses_bounded_vocabulary_not_arbitrary_cells(self):
        contaminated = ("STUDY_007", "123.45678", "12.34, 56.78", "kg/haXX", "unbounded free text")
        for field in ("yield_units", "use_visits_or_abundance", "taxa_recorded"):
            with self.subTest(field=field):
                result = source.inspect_csv(fixture([row(**{field: v}) for v in contaminated]))
                self.assertEqual(result["categorical_inventory"][field], {"<unreviewed_label>": 5})
                for value in contaminated:
                    self.assertNotIn(value, json.dumps(result))

    def test_verified_bytes_survive_a_schema_stop_in_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "receipt.json"
            with patch.object(source, "fetch_verified_source", return_value=b"hello\n"), \
                 patch.dict(source.MANIFEST, {"expected_bytes": 6,
                      "expected_git_blob_sha1": "ce013625030ba8dba906f756967f9e9ca394464a"}), \
                 patch("sys.argv", ["audit", "--output", str(dest)]), \
                 contextlib.redirect_stdout(io.StringIO()):
                code = source.main()
            result = json.loads(dest.read_text())
            self.assertEqual(code, 2)
            self.assertTrue(result["source_identity_verified"])
            self.assertFalse(result.get("schema_verified", True))
            self.assertEqual(result.get("stop_stage"), "schema")
            self.assertEqual(result.get("source_actual_bytes"), 6)
            self.assertEqual(result.get("source_actual_sha256"),
                         "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03")

    def test_redirect_is_rejected_before_following(self):
        from urllib.request import Request
        handler_type = getattr(source, "PinnedSourceRedirectHandler", None)
        self.assertIsNotNone(handler_type)
        with self.assertRaises(ValueError):
            handler_type().redirect_request(Request(source.MANIFEST["url"]), None,
                302, "Found", {}, "https://raw.githubusercontent.com/other/branch/file.csv")

    def test_zero_is_observed_and_measurement_families_stay_separate(self):
        raw = fixture([
            row(**{
                "yield": "0", "yield_units": "kg/ha", "visitation_rate": "0"}),
            row(site="P2", **{"yield": "2", "yield_units": "kg/ha", "abundance": "3"}),
            row(study="S2", site="P3", **{"yield": "NA", "yield_units": "kg/ha",
                                          "visitation_rate": "4"}),
            row(study="S3", group="G2", site="P4", **{"yield": "5",
                 "yield_units": "", "visitation_rate": "1", "abundance": "1"}),
        ])
        result = source.inspect_csv(raw)
        self.assertEqual(result["keys"]["rows"], 4)
        self.assertEqual(result["keys"]["distinct_study_id"], 3)
        self.assertEqual(result["keys"]["provisional_study_id2_groups"], 2)
        self.assertEqual(result["availability"]["yield"], {"observed_numeric": 3, "missing": 1, "invalid_nonmissing": 0})
        self.assertEqual(result["coverage"]["primary_yield_any_visit_with_units"]["rows"], 1)
        self.assertEqual(result["coverage"]["primary_yield_any_abundance_with_units"]["rows"], 1)
        self.assertEqual(result["coverage"]["primary_yield_any_visit_with_units"]["provisional_study_id2_groups"], 1)
        self.assertFalse(result["model_admission"])

    def test_repeated_source_years_and_duplicate_keys_are_not_independent(self):
        raw = fixture([row(), row(), row(study="S2", site="P2", year="2002"),
                       row(group="G2", site="P3")])
        result = source.inspect_csv(raw)
        self.assertEqual(result["keys"]["distinct_site_year_keys"], 3)
        self.assertEqual(result["keys"]["duplicate_site_year_keys"], 1)
        self.assertEqual(result["keys"]["rows_in_duplicate_site_year_keys"], 2)
        self.assertEqual(result["keys"]["extra_rows_beyond_unique_keys"], 1)
        self.assertEqual(result["keys"]["study_ids_mapping_to_multiple_study_id2"], 1)

    def test_missing_key_and_invalid_numeric_are_counted_without_printing_cells(self):
        raw = fixture([row(group="", site="", **{"yield": "PRIVATE_SENTINEL",
                   "yield_units": "redacted@example.test", "visitation_rate": "NaN"})])
        result = source.inspect_csv(raw)
        self.assertEqual(result["keys"]["rows_missing_candidate_key"], 1)
        self.assertEqual(result["keys"]["rows_missing_study_id2"], 1)
        self.assertEqual(result["availability"]["yield"]["invalid_nonmissing"], 1)
        self.assertNotIn("PRIVATE_SENTINEL", json.dumps(result))
        self.assertNotIn("redacted@example.test", json.dumps(result))

    def test_wrong_header_and_ragged_row_fail_without_echoing_source(self):
        with self.assertRaisesRegex(ValueError, "header"):
            source.inspect_csv(b"private_header\nprivate_value\n")
        raw = fixture([row()]).decode().splitlines()[0] + "\nPRIVATE_SENTINEL\n"
        with self.assertRaisesRegex(ValueError, "width") as caught:
            source.inspect_csv(raw.encode())
        self.assertNotIn("PRIVATE_SENTINEL", str(caught.exception))

    def test_source_identity_uses_git_blob_hash_and_size(self):
        self.assertEqual(source.verify_bytes(b"hello\n", 6,
            "ce013625030ba8dba906f756967f9e9ca394464a"),
            "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03")
        with self.assertRaises(ValueError):
            source.verify_bytes(b"hello\n", 7, "ce013625030ba8dba906f756967f9e9ca394464a")
        with self.assertRaises(ValueError):
            source.verify_bytes(b"hello\n", 6, "0" * 40)

    def test_access_stop_preserves_receipt_and_fails_gate(self):
        failures = [TimeoutError("read timed out"),
                    HTTPError("https://example.test", 503, "unavailable", {}, None),
                    ConnectionResetError("PRIVATE_SENTINEL"),
                    IncompleteRead(b"PRIVATE_SENTINEL", 100)]
        for failure in failures:
            with self.subTest(kind=type(failure).__name__), tempfile.TemporaryDirectory() as tmp:
                dest = Path(tmp) / "receipt.json"
                with patch.object(source, "fetch_verified_source", side_effect=failure), \
                     patch("sys.argv", ["audit", "--output", str(dest)]), \
                     contextlib.redirect_stdout(io.StringIO()):
                    code = source.main()
                self.assertEqual(code, 2)
                result = json.loads(dest.read_text())
                self.assertEqual(result["status"], "SOURCE_ACCESS_OR_SCHEMA_STOP")
                self.assertFalse(result["model_admission"])
                self.assertNotIn("PRIVATE_SENTINEL", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
