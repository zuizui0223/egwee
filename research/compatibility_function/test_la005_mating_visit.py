"""LA005 source-withheld contract, never opens original genetic marker values."""
from __future__ import annotations

import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import run_la005_mating_visit as la

DIR = Path(__file__).resolve().parent
RECORD = DIR / "LA005_DETECTABLE_OUTCROSSING_SITE_HOLDOUT_RESULT_20261118.json"
LA001 = DIR / "LA001_HELDOUT_RESULT_20261117.json"
LA002 = DIR / "LA002_ASSAY_WEIGHTED_SITE_HOLDOUT_RESULT_20261117.json"


class LA005ContractTests(unittest.TestCase):
    def setUp(self):
        self.x = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_original_commit_ancestor_and_exact_protocol(self):
        p = la.verify_original_freeze()
        self.assertEqual(p["experiment_id"], self.x["analysis_id"])
        self.assertEqual(p["source"]["archive_sha256"], la.SOURCE_SHA)
        self.assertEqual(self.x["protocol_freeze_commit"], la.FROZEN_PROTOCOL_COMMIT)

    def test_source_mother_suffix_rules_are_no_fuzzy_match(self):
        self.assertEqual(la.normalized_label("24_10-12", 2014), "10-12")
        self.assertEqual(la.normalized_label("W_10-13", 2014), "10-13")
        self.assertEqual(la.normalized_label("8-1M", 2015), "8-1")
        self.assertEqual(la.normalized_label("8-1", 2015), "8-1")

    def test_allele_rule_detects_only_directly_observed_nonmaternal(self):
        m = {i: (100 + i, 100 + i) for i in range(6)}
        matched = dict(m)
        foreign = dict(m)
        foreign[3] = (103, 200)
        self.assertEqual(la.detected_nonmaternal(matched, m), 0)
        self.assertEqual(la.detected_nonmaternal(foreign, m), 1)
        self.assertIsNone(la.detected_nonmaternal({0:m[0],1:m[1],2:m[2]}, m))
        self.assertEqual(la.detected_nonmaternal(
            {0:(1,1),1:(2,2),2:(3,3),3:(4,4)},m,min_shared=4), 1)

    def test_positive_only_allele_call_and_half_count_logit(self):
        row = {
            2:88.0,3:90.0,4:132.0,5:132.0,6:0.0,7:200.0,
            8:220.0,9:222.0,10:101.0,11:101.0,12:190.0,13:196.0
        }
        got = la.typed_loci(row)
        self.assertEqual(set(got), {0,1,3,4,5})
        self.assertEqual(got[0], (88,90))
        self.assertAlmostEqual(la.logit_rate(0, 8), -la.logit_rate(8,8))
        self.assertAlmostEqual(la.sigmoid(la.logit_rate(0,8)), .5/9)
        with self.assertRaises(ValueError):
            la.logit_rate(-1,8)

    def test_training_only_prediction_and_probabilities(self):
        # Synthetic data, no source maternal genotype or phenotype exposed.
        def make(k):
            return {
              "baseline":[int(k%2==0),int(k%3==0),int(k%2==0 and k%3==0),
                          math.log1p(k+1),k/30, .4 if k%2 else .6],
              "effective":math.log1p(k/4),
              "y":la.logit_rate((k*3)%8,8)
            }
        training = [make(i) for i in range(1,48)]
        test = [make(55),make(56),make(57)]
        pred0 = la.ridge_prediction(training,test,False)
        pred1 = la.ridge_prediction(training,test,True)
        for v in pred0+pred1:
            self.assertTrue(math.isfinite(v))
            self.assertTrue(0 < v < 1)
        # Prediction does not access heldout outcome values.
        future = [{**row,"y":-10000} for row in test]
        self.assertEqual(pred1,la.ridge_prediction(training,future,True))

    def test_original_data_and_site_folds(self):
        x=self.x
        g=x["source_grain"]
        for name,expected in {
            "field_plants":256,"source_maternal_rows":249,
            "source_unique_maternal_labels":248,
            "exact_field_matched_unique_source_mothers":246,
            "duplicate_source_mother_id":1,
            "offspring_source_rows":1796,
            "offspring_rows_with_unmatched_mother_label":7,
            "max_unambiguous_field_linked_mother_keys":245,
            "eligible_mothers_min_four_children":233,
            "eligible_offspring_in_admitted_mothers":1742,
        }.items():
            self.assertEqual(g[name],expected,name)
        self.assertEqual(len(x["holdout_folds"]),4)
        self.assertEqual(sum(r["n_mothers"] for r in x["holdout_folds"]),233)
        self.assertEqual(sum(r["genotyped_children"] for r in x["holdout_folds"]),1742)
        for key in ("M0_brier","M1_brier","M0_mae","M1_mae"):
            model,metric=key.split("_",1)
            n=sum(f["n_mothers"]*f[key] for f in x["holdout_folds"])/233
            self.assertAlmostEqual(n,x["pooled"][key],places=12)
        self.assertAlmostEqual(
            x["pooled"]["M0_brier"]-x["pooled"]["M1_brier"],
            x["pooled"]["M0_minus_M1_brier"],places=12
        )
        self.assertEqual(x["pooled"]["positive_site_folds"],3)
        self.assertGreater(x["pooled"]["M0_minus_M1_brier"],0)
        self.assertLess(x["pooled"]["relative_brier_improvement_percent"],1)
        self.assertEqual(x["frozen_decision"],
                         "BOUNDED_WITHIN_STUDY_VISIT_TO_DETECTABLE_OUTCROSSING_INCREMENT")

    def test_old_seed_count_failure_remains(self):
        la1=json.loads(LA001.read_text(encoding="utf-8"))
        la2=json.loads(LA002.read_text(encoding="utf-8"))
        self.assertEqual(la1["decision"],"NO_ROBUST_SINGLE_PROGRAMME_INCREMENT")
        self.assertEqual(la2["frozen_decision"],
                         "NO_ROBUST_ASSAY_CALIBRATED_SITE_TRANSFER_INCREMENT")
        self.assertLess(la1["pooled"]["M0_minus_M1_mse"],0)
        self.assertLess(la2["primary_M0_minus_M3_mse"],0)

    def test_no_raw_archive_or_marker_values_committed(self):
        self.assertTrue(self.x["source_definitions"]["no_raw_source_redistributed"])
        self.assertFalse((DIR/"doi_10_5061_dryad_2pj0j__v20161228.zip").exists())
        with TemporaryDirectory() as tmp:
            p=Path(tmp)/"invalid.zip"
            p.write_bytes(b"not original dryad")
            with self.assertRaises(ValueError):
                la.load_maternal_records(p)


if __name__ == "__main__":
    unittest.main()
