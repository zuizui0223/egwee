"""LA001 source-withheld reproducibility tests.

No original Dryad workbook is accessed in GitHub CI. Source-level model must be
run by a researcher with the SHA-pinned original archive as an explicit input.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
import tempfile
import unittest

import run_leavenworthia_LA001 as la


ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "research/compatibility_function/LA001_HELDOUT_RESULT_20261117.json"
PROTOCOL = ROOT / "research/compatibility_function/LA001_FROZEN_VISIT_SEED_PROTOCOL_20261117.json"


class LA001ContractTests(unittest.TestCase):
    def setUp(self):
        self.result = json.loads(RESULT.read_text(encoding="utf-8"))
        self.protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))

    def test_archive_and_original_paper_provenance(self):
        self.assertEqual(la.SOURCE_SHA, self.protocol["original_source"]["archive_sha256"])
        self.assertEqual(la.SOURCE_SHA, self.result["provenance"]["archive_sha256"])
        self.assertEqual(la.PROTOCOL_COMMIT, self.result["provenance"]["frozen_protocol_commit"])
        self.assertEqual(self.protocol["original_source"]["article_doi"], "10.1111/evo.13167")
        self.assertTrue(self.result["provenance"]["original_zip_not_committed"])

    def test_ooxml_position_columns(self):
        self.assertEqual(la.colnum("A1"), 0)
        self.assertEqual(la.colnum("H4"), 7)
        self.assertEqual(la.colnum("AM4"), 38)
        self.assertEqual(la.colnum("EH4"), 137)
        with self.assertRaises(ValueError):
            la.colnum("??")

    def test_normal_equations_solver(self):
        a = [[2.0, 1.0], [1.0, 2.0]]
        b = [3.0, 3.0]
        self.assertEqual([round(v, 12) for v in la.solve(a, b)], [1.0, 1.0])
        with self.assertRaises(ValueError):
            la.solve([[0.0, 0.0], [0.0, 0.0]], [0, 0])

    def test_source_digest_blocks_any_other_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            wrong = Path(tmp) / "not-actual-data.zip"
            wrong.write_bytes(b"not-the-source")
            with self.assertRaises(ValueError):
                la.draw_source(wrong)

    def test_ridge_training_only_standardization(self):
        # Synthetic rows; NOT data from the source study.
        def make(x, y):
            return {
                "baseline": [1 if x>2 else 0, 1 if x%2 else 0, 0, float(x), 0.3],
                "effective": math.log1p(x),
                "total": math.log1p(x+1),
                "y": float(y),
            }
        train = [make(i, 2 + 0.5 * i) for i in range(1, 10)]
        test = [make(12, 99999)]  # should not affect prediction
        a = la.ridge_predict(train, test, "M0_baseline")[0]
        b = la.ridge_predict(train, [{**test[0], "y": -99999}], "M0_baseline")[0]
        self.assertAlmostEqual(a, b, places=10)
        self.assertTrue(math.isfinite(a))
        with self.assertRaises(ValueError):
            la.ridge_predict(train, test, "unregistered_model")

    def test_all_four_sites_and_primary_outcome_locked(self):
        r = self.result
        self.assertEqual(r["quality"]["source_field_n"], 256)
        self.assertEqual(r["quality"]["source_field_with_seed_total"], 252)
        self.assertEqual(r["quality"]["source_plant_observation_periods"], 121)
        self.assertEqual(r["quality"]["source_visits_to_positions_1to32"], 6701)
        self.assertEqual(r["quality"]["source_visits_with_zero_open_flower"], 38)
        self.assertEqual(r["quality"]["one_out_of_range_position_token"], 34)
        self.assertEqual([s["site"] for s in r["folds"]], list(la.SITES))
        self.assertEqual([s["n"] for s in r["folds"]], [62, 63, 64, 63])
        self.assertEqual(r["pooled"]["n"], 252)
        for m in la.MODELS:
            label = m.split("_")[0]
            expected = sum(f["n"] * f[f"{label}_mse"] for f in r["folds"]) / 252
            self.assertAlmostEqual(expected, r["pooled"][f"{label}_mse"], places=11)
        self.assertAlmostEqual(
            r["pooled"]["M0_mse"] - r["pooled"]["M1_mse"],
            r["pooled"]["M0_minus_M1_mse"], places=11,
        )
        self.assertEqual(r["pooled"]["sites_with_positive_primary_gain"], 3)
        self.assertLess(r["pooled"]["M0_minus_M1_mse"], 0)
        self.assertEqual(r["decision"], "NO_ROBUST_SINGLE_PROGRAMME_INCREMENT")

    def test_source_absent_from_repository_is_not_successful_rerun(self):
        self.assertTrue(self.result["provenance"]["original_zip_not_committed"])
        self.assertFalse((ROOT / self.protocol["original_source"]["archive_name"]).exists())


if __name__ == "__main__":
    unittest.main()
