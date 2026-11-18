"""QPF004 source-withheld post-outcome ascertainment audit.

No original third-party plant IDs, fruit rows or pollen values used in CI.
"""
from __future__ import annotations
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import diagnose_qpf004_pollen_assay_selection as q
from run_qpf004_mertensia_source_weekholdout import FREEZE_SHA, ZIP_SHA

HERE=Path(__file__).resolve().parent
RECEIPT=HERE/"QPF004_POSTHOC_POLLEN_ASSAY_SELECTION_20261118.json"
PREVIOUS=HERE/"QPF004_ORIGINAL_WEEK_HOLDOUT_RESULT_20261118.json"

class OriginalMertensiaAssayCoverageTests(unittest.TestCase):
    def setUp(self):
        self.r=json.loads(RECEIPT.read_text(encoding="utf-8"))
        self.previous=json.loads(PREVIOUS.read_text(encoding="utf-8"))

    def test_registered_negative_original_stays_intact(self):
        self.assertEqual(self.r["original_primary_protocol_commit"],FREEZE_SHA)
        self.assertEqual(self.r["source_archive_sha256"],ZIP_SHA)
        self.assertEqual(self.r["original_primary_decision"],
                         "NO_PRACTICALLY_PORTABLE_POLLEN_INCREMENT")
        self.assertEqual(self.previous["registered_decision"],
                         self.r["original_primary_decision"])
        self.assertAlmostEqual(self.r["original_2016_primary_pooled_MSE"]["M0"],
                               self.previous["primary_2016_week"]["pooled"]["M0_MSE"])
        self.assertAlmostEqual(self.r["original_2016_primary_pooled_MSE"]["M1"],
                               self.previous["primary_2016_week"]["pooled"]["M1_MSE"])
        self.assertEqual(self.r["original_2016_primary_pooled_MSE"]["positive_weeks"],1)

    def test_original_assay_coverage_unequal_across_treatments(self):
        groups={v["treatment"]:v for v in self.r["source_treatment_coverage_and_F_descriptives"]}
        self.assertEqual((groups["ALL"]["source_n"],groups["ALL"]["pollen_assay_n"]),(232,62))
        self.assertEqual((groups["V"]["source_n"],groups["V"]["pollen_assay_n"]),(94,47))
        self.assertEqual((groups["O"]["source_n"],groups["O"]["pollen_assay_n"]),(65,15))
        self.assertEqual((groups["B"]["source_n"],groups["B"]["pollen_assay_n"]),(73,0))
        self.assertAlmostEqual(groups["V"]["assay_fraction"],.5)
        self.assertAlmostEqual(groups["O"]["assay_fraction"],15/65)
        self.assertAlmostEqual(groups["ALL"]["assay_fraction"],62/232)
        self.assertEqual(groups["B"]["source_P_assayed"]["n"],0)
        self.assertIsNone(groups["B"]["source_P_assayed"]["mean_seed_per_flower"])
        self.assertAlmostEqual(groups["ALL"]["source_P_assayed"]["mean_seed_per_flower"],.7182027649769586,places=12)
        self.assertAlmostEqual(groups["ALL"]["source_P_not_assayed"]["mean_seed_per_flower"],.34067452936378767,places=12)
        # Source composition reverses naive positive pooled comparison inside V
        # (this does not make any within-treatment comparison causal).
        self.assertLess(groups["V"]["source_P_assayed"]["mean_seed_per_flower"],
                        groups["V"]["source_P_not_assayed"]["mean_seed_per_flower"])
        self.assertLess(groups["O"]["source_P_assayed"]["mean_seed_per_flower"],
                        groups["O"]["source_P_not_assayed"]["mean_seed_per_flower"])
        self.assertTrue(self.r["source_support_closure"]["no_bagged_control_assayed_P"])

    def test_site_week_support_disappears_under_measured_P_filter(self):
        ds=self.r["site_by_week_pollen_coverage"]
        self.assertEqual([(x["site"],x["source_week"],x["source_seed_ramets"],x["pollen_measured_ramets"])
                          for x in ds],
                         [("RG",1,23,4),("RG",2,58,18),("RG",3,41,16),
                          ("SP",3,13,0),("SP",4,61,20),("SP",5,36,4)])
        self.assertEqual(sum(x["source_seed_ramets"] for x in ds),232)
        self.assertEqual(sum(x["pollen_measured_ramets"] for x in ds),62)
        self.assertEqual(sum(x["pollen_unmeasured_ramets"] for x in ds),170)
        self.assertFalse(any(x["pollen_measured_ramets"]>0 and x["site"]=="SP" and x["source_week"]<=3 for x in ds))
        self.assertFalse(any(x["pollen_measured_ramets"]>0 and x["site"]=="RG" and x["source_week"]>=4 for x in ds))

    def test_source_auditor_compares_only_synthetic_aggregate_or_source_sha(self):
        rows=[
            {"plantID":11.0,"site":"RG","week":1.0,"seedPerFlr":1.0,"seedCnt":2.0,"noFlrs":2.0},
            {"plantID":12.0,"site":"RG","week":1.0,"seedPerFlr":0.0,"seedCnt":0.0,"noFlrs":1.0},
            {"plantID":13.0,"site":"SP","week":2.0,"seedPerFlr":3.0,"seedCnt":6.0,"noFlrs":2.0}
        ]
        self.assertEqual(q.key(11.0),"11")
        self.assertEqual(q.aggregate([])["n"],0)
        self.assertEqual(q.aggregate(rows)["n"],3)
        self.assertAlmostEqual(q.aggregate(rows)["mean_seed_per_flower"],4/3)
        g=q.siteweek(rows,{"11","13"})
        self.assertEqual([(r["site"],r["source_week"],r["pollen_measured_ramets"]) for r in g],
                         [("RG",1,1),("SP",2,1)])
        with TemporaryDirectory() as tmp:
            p=Path(tmp)/"not-original.zip"
            p.write_bytes(b"source-digest-mismatch")
            with self.assertRaises(ValueError):
                q.audit_source(p)

    def test_only_source_free_diagnostics_and_no_new_pvalues(self):
        self.assertEqual(self.r["classification"],
                         "POSTHOC_ASSAY_SELECTION_AND_SOURCE_SUPPORT_NOT_NEW_ECOLOGICAL_TEST")
        self.assertFalse(self.r["original_individual_flower_ramet_values_exported"])
        self.assertFalse(self.r["third_party_original_source_uploaded"])
        self.assertTrue(self.r["source_support_closure"]["P_missingness_not_randomly_distributed_across_treatments"])
        self.assertFalse(self.r["source_support_closure"]["P_and_seed_same_flower_verified"])
        self.assertFalse((HERE/"gallagher&campbell_pollinatorEffectivenessData.xlsx").exists())

if __name__=="__main__":
    unittest.main()
