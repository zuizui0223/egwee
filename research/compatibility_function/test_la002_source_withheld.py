"""Offline scientific contract for source-withheld LA002 per-visit calibration.

The user's original Dryad ZIP is NOT committed or run in GitHub Actions.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
from unittest.mock import patch
import unittest

import run_leavenworthia_LA002 as la2
from run_leavenworthia_LA001 import ridge_predict


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RESULT = HERE / "LA002_ASSAY_WEIGHTED_SITE_HOLDOUT_RESULT_20261117.json"
OLD = HERE / "LA001_HELDOUT_RESULT_20261117.json"


class LA002ContractTests(unittest.TestCase):
    def setUp(self):
        self.out = json.loads(RESULT.read_text(encoding="utf-8"))
        self.old = json.loads(OLD.read_text(encoding="utf-8"))

    def test_protocol_precedes_outcome_and_remains_byte_identical(self):
        la2.verify_original_protocol_freeze()
        self.assertEqual(self.out["protocol_frozen_commit"], la2.FROZEN_SHA)
        self.assertEqual(self.out["original_source_SHA256"], la2.SOURCE_SHA)
        self.assertEqual(self.out["original_source_SHA256"],
                         self.old["provenance"]["archive_sha256"])

    def test_assay_contrast_uses_independent_single_visits(self):
        expected = {
            "Solitary": (22, 14, 57), "BeeFly": (9, 6, 23),
            "Fly": (17, 2, 7), "Honeybee": (2, 1, 4),
            "Ant": (1, 0, 0), "Control": (21, 1, 1),
        }
        # Synthetic sheet fixture contains only group counts and overall sums,
        # not original individual pollen/seed data.
        sheet = {1: {0: "Pollinator", 2: "Fruit", 3: "Seed/fruit"}}
        rno = 2
        for group, (n, fruits, total_seeds) in expected.items():
            for i in range(n):
                row = {0: group, 2: float(i < fruits)}
                if i == 0 and fruits:
                    row[3] = float(total_seeds)
                elif i < fruits:
                    row[3] = 0.0
                sheet[rno] = row
                rno += 1
        self.assertEqual(len(sheet), 73)
        with patch.object(la2, "sheets", return_value={"Final pass": sheet}):
            got = la2.calibrate_single_visit(None)
        self.assertEqual(len(got), 6)
        for k, (n, fruits, seed) in expected.items():
            self.assertEqual((got[k]["n"], got[k]["n_fruits"],
                              got[k]["total_seeds"]), (n, fruits, seed))
            self.assertAlmostEqual(got[k]["mean_seeds_per_assigned_visit"], seed/n)

    def test_weighted_ridge_matches_M1_if_fixed_feature_is_identical(self):
        # Synthetic independent rows, no original phenotype observation.
        def row(k):
            return {
                "baseline": [int(k % 2), int(k % 3 == 0),
                             int(k % 2 and k % 3 == 0),
                             math.log1p(1 + k), k / 30.0],
                "effective": math.log1p(k / 4),
                "quality": math.log1p(k / 4),
                "y": math.log1p(6 + (k * k) % 21),
            }
        train = [row(i) for i in range(1, 45)]
        hold = [row(i) for i in (46, 47, 50)]
        old = ridge_predict(train, hold, "M1_effective_visits")
        new = la2.weighted_ridge(train, hold)
        self.assertEqual(len(new), 3)
        for a, b in zip(old, new):
            self.assertAlmostEqual(a, b, places=11)

    def test_original_four_site_fold_values_still_frozen(self):
        self.assertEqual(self.old["decision"], "NO_ROBUST_SINGLE_PROGRAMME_INCREMENT")
        self.assertEqual(self.out["eligible_field_plants"], 252)
        self.assertEqual(self.out["whole_site_fold_count"], 4)
        self.assertEqual(
            [f["site"] for f in self.out["folds"]],
            ["Waco", "Quarry", "24-43", "Landersville"],
        )
        self.assertEqual(sum(f["n"] for f in self.out["folds"]), 252)
        for f in self.out["folds"]:
            prior = next(x for x in self.old["folds"] if x["site"] == f["site"])
            for m in ("M0", "M1", "M2"):
                self.assertAlmostEqual(f["models"][m]["mse"], prior[f"{m}_mse"],
                                       delta=1e-9)
            self.assertAlmostEqual(
                f["M0_minus_M3_mse"],
                f["models"]["M0"]["mse"] - f["models"]["M3"]["mse"],
                places=11,
            )
        for m in ("M0", "M1", "M2", "M3"):
            expected = sum(
                f["n"] * f["models"][m]["mse"] for f in self.out["folds"]
            ) / 252
            self.assertAlmostEqual(self.out["pooled"][m]["mse"], expected,
                                   places=11)

    def test_negative_result_not_rescued_by_secondary(self):
        self.assertEqual(self.out["positive_folds"], 3)
        self.assertLess(self.out["primary_M0_minus_M3_mse"], 0)
        self.assertEqual(
            self.out["frozen_decision"],
            "NO_ROBUST_ASSAY_CALIBRATED_SITE_TRANSFER_INCREMENT",
        )
        self.assertAlmostEqual(self.out["primary_M0_minus_M3_mse"],
                               self.out["pooled"]["M0"]["mse"] -
                               self.out["pooled"]["M3"]["mse"])
        self.assertAlmostEqual(self.out["secondary_M1_minus_M3_mse"],
                               self.out["pooled"]["M1"]["mse"] -
                               self.out["pooled"]["M3"]["mse"])
        self.assertTrue(self.out["provenance"]["original_source_not_redistributed"])
        self.assertFalse((ROOT / "doi_10_5061_dryad_2pj0j__v20161228.zip").exists())

    def test_published_rate_and_control_numerators_not_falsely_reconciled(self):
        source = self.out["source_visit_QC"]
        pub = self.out["publisher_source_reconciliation"]
        self.assertEqual(source["complete_sessions"], 121)
        self.assertEqual(source["insect_event_rows"], 2850)
        self.assertEqual(source["position_tokens_all"], 6702)
        self.assertEqual(source["valid_position_visits"] -
                         source["zero_open_flower_visits"], 6663)
        self.assertEqual(pub["reported_paper_visits"], 3748)
        self.assertNotEqual(pub["reported_paper_visits"],
                            pub["source_raw_position_tokens"])
        self.assertNotEqual(pub["reported_paper_visits"],
                            pub["source_insect_event_rows"])
        self.assertEqual(pub["reported_paper_control_flowers"], 17)
        self.assertEqual(pub["source_control_rows"], 21)
        self.assertTrue(pub["not_a_reconciled_paper_table_2_reproduction"])

    def test_source_sha_fail_closed(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            p = Path(tmp) / "fake-source.zip"
            p.write_bytes(b"wrong-source")
            with self.assertRaises(ValueError):
                la2.prepare_original_252(p)


if __name__ == "__main__":
    unittest.main()
