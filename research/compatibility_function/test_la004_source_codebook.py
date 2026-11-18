"""LA004 source-withheld originality and measurement-codebook regression contract."""
from __future__ import annotations
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import run_la004_glossary_control_audit as la004

HERE = Path(__file__).resolve().parent
RECEIPT = HERE / "LA004_ORIGINAL_CODEBOOK_CONTROL_RECEIPT_20261118.json"
LA001 = HERE / "LA001_HELDOUT_RESULT_20261117.json"
LA002 = HERE / "LA002_ASSAY_WEIGHTED_SITE_HOLDOUT_RESULT_20261117.json"


class LA004SourceCodebookTests(unittest.TestCase):
    def setUp(self):
        self.rec = json.loads(RECEIPT.read_text(encoding="utf-8"))

    def test_original_literal_glossary_is_not_inferred_from_treatment(self):
        self.assertEqual(self.rec["source_sha256"], la004.SOURCE_SHA)
        self.assertEqual(
            self.rec["source_glossary_literal_labels"],
            list(la004.EXPECTED_GLOSSARY),
        )
        self.assertIn("Bf - Bee Fly", self.rec["source_glossary_literal_labels"])
        self.assertIn("B - Butterfly", self.rec["source_glossary_literal_labels"])
        self.assertIn("Temporal", self.rec["source_glossary_location"])
        self.assertIn("uppercase BF", self.rec["source_explicit_fact"])

    def test_original_case_sensitive_counts_and_denominator(self):
        self.assertEqual(self.rec["completed_periods"]["total"], 121)
        self.assertEqual(self.rec["raw_visitation_record_units"]["insect_event_rows"], 2850)
        self.assertEqual(self.rec["raw_visitation_record_units"]["position_tokens"], 6702)
        self.assertEqual(self.rec["raw_visitation_record_units"]["published_visits"], 3748)
        self.assertEqual(self.rec["source_case_sensitive_counts"]["2014:Bf"],
                         {"insect_rows": 44, "plant_position_tokens": 205})
        self.assertEqual(self.rec["source_case_sensitive_counts"]["2014:BF"],
                         {"insect_rows": 3, "plant_position_tokens": 4})
        self.assertEqual(self.rec["source_case_sensitive_counts"]["2014:B"],
                         {"insect_rows": 7, "plant_position_tokens": 34})
        self.assertEqual(self.rec["source_case_sensitive_counts"]["2015:BF"],
                         {"insect_rows": 85, "plant_position_tokens": 780})
        self.assertEqual(
            sum(x["n_positions"] for x in self.rec["raw_position_share_under_uppercase_merging"]),
            6702,
        )

    def test_neither_case_rule_reconstructs_published_2014_group_rates(self):
        for genotype, pbf, pother in (("SI", .060, .236), ("SC", .080, .297)):
            r = self.rec["source_2014_category_mean_rate_sensitivity"][genotype]
            self.assertGreater(abs(r["bf_casefold"] - pbf), .1)
            self.assertGreater(abs(r["bf_strict_uppercase"] - pbf), .05)
            self.assertGreater(abs(r["other_casefold"] - pother), .1)
            self.assertGreater(abs(r["other_plus_Bf"] - pother), .05)
            self.assertAlmostEqual(r["bf_casefold"], r["bf_strict_uppercase"] +
                                   (r["other_plus_Bf"] - r["other_casefold"]), places=12)

    def test_both_worksheets_have_21_fully_coded_controls(self):
        controls = self.rec["emasculation_controls"]
        for name in ("Final pass", "Fruit set first pass"):
            self.assertEqual(controls[name]["n_source_controls"], 21)
            self.assertEqual(controls[name]["n_fruit_outcomes_present"], 21)
            self.assertEqual(controls[name]["n_fruits"], 1)
        self.assertEqual(controls["Final pass"]["n_with_dates"], 21)
        self.assertEqual(controls["Final pass"]["source_date_serial_counts"],
                         {"42078": 7, "42079": 14})
        self.assertEqual(self.rec["published_bagged_control_n"], 17)

    def test_original_negative_decisions_unchanged(self):
        a = json.loads(LA001.read_text(encoding="utf-8"))
        b = json.loads(LA002.read_text(encoding="utf-8"))
        self.assertEqual(a["decision"], "NO_ROBUST_SINGLE_PROGRAMME_INCREMENT")
        self.assertEqual(b["frozen_decision"],
                         "NO_ROBUST_ASSAY_CALIBRATED_SITE_TRANSFER_INCREMENT")
        self.assertLess(a["pooled"]["M0_minus_M1_mse"], 0)
        self.assertLess(b["primary_M0_minus_M3_mse"], 0)
        self.assertFalse((HERE / "Pollinator+Data+2014.xlsx").exists())
        self.assertFalse((HERE / "Emasculation+experiment.xlsx").exists())

    def test_wrong_zip_hash_fail_closed(self):
        with TemporaryDirectory() as tmp:
            f = Path(tmp) / "incorrect.zip"
            f.write_bytes(b"untrusted synthetic fixture")
            with self.assertRaises(ValueError):
                la004.audit(f)


if __name__ == "__main__":
    unittest.main()
