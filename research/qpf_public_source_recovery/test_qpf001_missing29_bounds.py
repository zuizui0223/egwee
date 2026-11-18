"""QPF001 posthoc 29-fruit bounded-score audit: synthetic math, original null.

No real original flower, pollen, visitor or seed rows are accessed by CI.
"""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import bound_qpf001_missing29_fixed_forecasts as audit
from run_qpf001_original_flower_dateholdout import DAYS, FREEZE_SHA, verify_protocol

HERE=Path(__file__).resolve().parent
RECEIPT=HERE/"QPF001_MISSING29_FIXED_FORECAST_BOUNDS_20261118.json"
ORIGINAL=HERE/"QPF001_DATE_HOLDOUT_ORIGINAL_RESULT_20261118.json"
POSTHOC=HERE/"QPF001_POSTHOC_DATE196_MISSINGNESS_RECEIPT_20261118.json"


class Missing29FixedForecastBoundsTests(unittest.TestCase):
    def setUp(self):
        self.r=json.loads(RECEIPT.read_text(encoding="utf-8"))
        self.orig=json.loads(ORIGINAL.read_text(encoding="utf-8"))
        self.previous=json.loads(POSTHOC.read_text(encoding="utf-8"))

    def test_original_protocol_is_ancestral_and_unmodified(self):
        verify_protocol()
        self.assertEqual(self.r["original_protocol_commit"],FREEZE_SHA)
        self.assertEqual(self.r["original_scientific_decision"],
                         "NO_ROBUST_WITHIN_STUDY_DATE_TRANSFER_GAIN")
        self.assertEqual(self.orig["registered_decision"],self.r["original_scientific_decision"])
        self.assertEqual(self.previous["original_scientific_decision"],self.r["original_scientific_decision"])
        self.assertEqual(self.r["status"],"POSTHOC_SHARP_BOUNDS_CONDITIONAL_ON_HYPOTHETICAL_SEEDSET")

    def test_bounded_loss_is_linear_in_unknown_outcome(self):
        for p0,p1 in ((.2,.7),(.8,.4),(0.,1.),(1.,0.),(.5,.5)):
            a=(p0-0.)**2-(p1-0.)**2
            b=(p0-1.)**2-(p1-1.)**2
            lo,hi=audit.bounded_unknown_flower(p0,p1)
            self.assertAlmostEqual(lo,min(a,b))
            self.assertAlmostEqual(hi,max(a,b))
            for y in (.01,.2,.38,.5,.9,.99):
                exact=(p0-y)**2-(p1-y)**2
                self.assertLessEqual(lo-1e-12,exact)
                self.assertLessEqual(exact,hi+1e-12)
        with self.assertRaises(ValueError):
            audit.bounded_unknown_flower(-.2,.4)

    def test_original_recovered_loss_and_missing_date_coverage_exact(self):
        r=self.r
        self.assertEqual(r["filmed_all_flower_n"],122)
        self.assertEqual(r["observed_recovered_fruit_n"],93)
        self.assertEqual(r["unrecovered_fruit_unknown_n"],29)
        self.assertEqual([x["julian_day"] for x in r["date_level_aggregates"]],list(DAYS))
        self.assertEqual([x["n_missing_seedset"] for x in r["date_level_aggregates"]],
                         [15,0,8,2,1,2,0,1])
        self.assertEqual(r["unknown29_M1_prediction_higher_count"],17)
        self.assertEqual(r["unknown29_M1_prediction_lower_count"],12)
        self.assertAlmostEqual(r["original_observed93_mse_gain_M0_minus_M1"],
                               self.orig["pooled"]["M0_minus_M1_mse"],places=13)
        self.assertAlmostEqual(r["original_observed93_summed_squared_loss_gain"],
                               93*self.orig["pooled"]["M0_minus_M1_mse"],places=12)

    def test_each_date_bound_contributes_to_sharp_all122_range(self):
        r=self.r
        date=r["date_level_aggregates"]
        lo=sum(x["min_possible_missing_outcome_error_gain_sse"] for x in date)
        hi=sum(x["max_possible_missing_outcome_error_gain_sse"] for x in date)
        self.assertAlmostEqual(lo,r["unrecovered29_summed_loss_gain_lower"],places=12)
        self.assertAlmostEqual(hi,r["unrecovered29_summed_loss_gain_upper"],places=12)
        self.assertAlmostEqual(
            (r["original_observed93_summed_squared_loss_gain"]+lo)/122,
            r["hypothetical_all122_M0_minus_M1_mse_gain_lower"],places=12)
        self.assertAlmostEqual(
            (r["original_observed93_summed_squared_loss_gain"]+hi)/122,
            r["hypothetical_all122_M0_minus_M1_mse_gain_upper"],places=12)
        self.assertAlmostEqual(r["hypothetical_all122_M0_minus_M1_mse_gain_lower"],
                               -.008424702364987187,delta=1e-12)
        self.assertAlmostEqual(r["hypothetical_all122_M0_minus_M1_mse_gain_upper"],
                               .01051318460870819,delta=1e-12)
        self.assertLess(r["hypothetical_all122_M0_minus_M1_mse_gain_lower"],0)
        self.assertGreater(r["hypothetical_all122_M0_minus_M1_mse_gain_upper"],0)

    def test_scientific_scope_and_source_privacy(self):
        self.assertFalse(self.r["individual_flower_values_exported"])
        self.assertFalse(self.r["third_party_original_workbook_exported"])
        self.assertIn("unrecovered",self.r["condition_on_potential_outcome"])
        self.assertGreater(len(self.r["scope"]),3)
        self.assertLess(self.r["independent_original_data_reproduction"]
                        ["max_absolute_original_8date_model_metric_discrepancy"],1e-12)
        self.assertFalse((HERE/"FIGO_2019_Data_20210523.xlsx").exists())
        with TemporaryDirectory() as t:
            bad=Path(t)/"bad.zip"
            bad.write_bytes(b"not-the-original-source")
            with self.assertRaises(ValueError):
                audit.source_audit(bad)


if __name__=="__main__":
    unittest.main()
