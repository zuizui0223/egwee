"""LA001 post-outcome diagnostic source-withheld contract and regression tests."""
from __future__ import annotations

import json
from pathlib import Path
import math
import unittest

import diagnose_la001_site_transfer as audit

ROOT = Path(__file__).resolve().parent
RECORD = ROOT / "LA001_POSTHOC_EXPOSURE_TRANSPORT_20261117.json"
ORIGINAL = ROOT / "LA001_HELDOUT_RESULT_20261117.json"


class LA001ExposureTransportTests(unittest.TestCase):
    def test_linear_percentile_without_looking_at_real_outcomes(self):
        self.assertAlmostEqual(audit.linear_percentile([0, 10], .95), 9.5)
        self.assertAlmostEqual(audit.linear_percentile([1, 2, 3, 4, 5], .5), 3)
        for data, fraction in (([], .5), ([1], 1.1)):
            with self.assertRaises(ValueError):
                audit.linear_percentile(data, fraction)

    def test_original_negative_decision_unchanged(self):
        x = json.loads(RECORD.read_text(encoding="utf-8"))
        old = json.loads(ORIGINAL.read_text(encoding="utf-8"))
        self.assertEqual(x["status"], "POSTHOC_DESCRIPTIVE_NOT_CONFIRMATORY")
        self.assertEqual(x["original_decision"], old["decision"])
        self.assertEqual(x["original_frozen_protocol_commit"],
                         old["provenance"]["frozen_protocol_commit"])
        self.assertEqual(x["original_source_sha256"],
                         old["provenance"]["archive_sha256"])
        self.assertEqual(x["eligible_plants"], old["pooled"]["n"])
        self.assertEqual(x["original_pooled_m0_minus_m1_mse"],
                         old["pooled"]["M0_minus_M1_mse"])
        self.assertLess(x["original_pooled_m0_minus_m1_mse"], 0)

    def test_all_four_fold_mse_values_preserved(self):
        x = json.loads(RECORD.read_text(encoding="utf-8"))
        old = json.loads(ORIGINAL.read_text(encoding="utf-8"))
        self.assertEqual(len(x["sites"]), 4)
        self.assertEqual(set(row["site"] for row in x["sites"]),
                         set(row["site"] for row in old["folds"]))
        for row in x["sites"]:
            source = next(f for f in old["folds"] if f["site"] == row["site"])
            self.assertAlmostEqual(row["m0_minus_m1_mse"],
                                   source["M0_mse"] - source["M1_mse"],
                                   delta=1e-9)
            self.assertGreater(row["n"], 0)
            self.assertGreaterEqual(row["n_holdout_above_training_p95"], 0)
            self.assertLessEqual(row["n_holdout_above_training_p95"], row["n"])

    def test_24_43_distribution_shift_is_not_predeclared_significance(self):
        x = json.loads(RECORD.read_text(encoding="utf-8"))
        one = next(s for s in x["sites"] if s["site"] == "24-43")
        self.assertEqual(one["n"], 64)
        self.assertEqual(one["n_holdout_above_training_p95"], 22)
        self.assertEqual(one["n_above_in_2014"], 22)
        self.assertEqual([r["n"] for r in one["subgroup"]], [16, 16, 16, 16])
        self.assertLess(one["unstandardized_log_visit_coefficient"], 0)
        self.assertLess(one["m0_minus_m1_mse"], 0)
        self.assertTrue(x["no_new_inferential_test"])
        self.assertTrue(x["intervention_no_retraining"])

    def test_source_not_committed_and_reproduction_contract(self):
        x = json.loads(RECORD.read_text(encoding="utf-8"))
        self.assertTrue(x["no_original_individual_rows_or_genotypes_redistributed"])
        self.assertFalse((ROOT / "doi_10_5061_dryad_2pj0j__v20161228.zip").exists())
        self.assertEqual(audit.LOCKED_PATH, ORIGINAL)
        self.assertEqual(audit.POSTHOC_PATH, RECORD)


if __name__ == "__main__":
    unittest.main()
