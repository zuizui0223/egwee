"""Source-withheld LA003 published Table 2 audit contracts, no seed outcomes."""
from __future__ import annotations

import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import run_la003_published_visit_rate_audit as check

DIR = Path(__file__).resolve().parent
RECEIPT = DIR / "LA003_TABLE2_AGGREGATE_RECEIPT_20261118.json"
LA001 = DIR / "LA001_HELDOUT_RESULT_20261117.json"
LA002 = DIR / "LA002_ASSAY_WEIGHTED_SITE_HOLDOUT_RESULT_20261117.json"


class SourceRateAuditTests(unittest.TestCase):
    def setUp(self):
        self.r = json.loads(RECEIPT.read_text(encoding="utf-8"))

    def test_source_is_original_and_raw_not_distributed(self):
        self.assertEqual(self.r["source_zip_sha256"], check.SOURCE_SHA)
        self.assertEqual(self.r["original_paper_doi"], "10.1111/evo.13167")
        self.assertEqual(self.r["original_dataset_doi"], "10.5061/dryad.2pj0j")
        self.assertFalse((DIR / "doi_10_5061_dryad_2pj0j__v20161228.zip").exists())

    def test_counting_units_are_not_conflated(self):
        c = self.r["source_grains"]
        self.assertEqual(c["half_hour_periods"], 121)
        self.assertEqual(c["insect_event_rows"], 2850)
        self.assertEqual(c["position_tokens"], 6702)
        self.assertEqual(c["distinct_positions_per_event_sum"], 5064)
        self.assertEqual(c["in_range_position_tokens"] -
                         c["zero_open_flower_inrange_tokens"], 6663)
        self.assertEqual(c["invalid_position_tokens"], 1)
        self.assertEqual(self.r["reported_paper"]["visits"], 3748)
        self.assertNotIn(3748, (2850, 6702, 5064, 6663))
        self.assertEqual(sum(x["completed_sessions"] for x in
                             self.r["source_by_year"].values()), 121)

    def test_exact_rate_transform_and_rate_boundary(self):
        self.assertEqual(check.source_period_rate(8, 4), 4)
        with self.assertRaises(ValueError):
            check.source_period_rate(0, 0)
        with self.assertRaises(ValueError):
            check.source_period_rate(-1, 5)
        self.assertEqual(check.PUBLISHED_TOTAL_RATES[2014]["SC"], 2.245)
        sc = self.r["observed_rates"]["2014"]["SC"]
        self.assertEqual(sc["n_periods"], 44)
        self.assertAlmostEqual(sc["source_total"], 2.24547416561454, places=12)
        self.assertAlmostEqual(sc["source_AH"], 1.678182729553754, places=12)
        self.assertAlmostEqual(sc["source_F"], .19057333832734902, places=12)
        self.assertLess(abs(sc["source_total"] - 2.245), 0.001)
        for y in ("2014", "2015"):
            for g in ("SI", "SC"):
                rate = self.r["observed_rates"][y][g]
                self.assertAlmostEqual(
                    sum(rate["source_" + k] for k in
                        ("AH", "BF_casefold", "F", "Other")),
                    rate["source_total"], places=10
                )

    def test_taxon_case_is_unresolved_not_automatically_original_paper(self):
        a = self.r["source_case_sensitive_taxon_codes"]
        self.assertEqual(a["2014"]["Bf"]["insect_rows"], 44)
        self.assertEqual(a["2014"]["Bf"]["position_tokens"], 205)
        self.assertEqual(a["2014"]["BF"]["position_tokens"], 4)
        self.assertEqual(a["2015"]["BF"]["position_tokens"], 780)
        self.assertIn("2014 case-sensitive Bf vs BF meaning", " ".join(self.r["unresolved"]))

    def test_no_retuning_of_original_negative_outcomes(self):
        a = json.loads(LA001.read_text(encoding="utf-8"))
        b = json.loads(LA002.read_text(encoding="utf-8"))
        self.assertEqual(a["decision"], "NO_ROBUST_SINGLE_PROGRAMME_INCREMENT")
        self.assertEqual(b["frozen_decision"],
                         "NO_ROBUST_ASSAY_CALIBRATED_SITE_TRANSFER_INCREMENT")
        self.assertLess(a["pooled"]["M0_minus_M1_mse"], 0)
        self.assertLess(b["primary_M0_minus_M3_mse"], 0)

    def test_source_sha_fail_closed_before_opening_zip(self):
        with TemporaryDirectory() as d:
            p = Path(d) / "unrelated.zip"
            p.write_bytes(b"wrong-source")
            with self.assertRaises(ValueError):
                check.audit(p)


if __name__ == "__main__":
    unittest.main()
