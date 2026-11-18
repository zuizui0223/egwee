"""Source-withheld QPF001 posthoc date/fruit-ascertainment QA, no new model tests."""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import diagnose_qpf001_date196_missingness as audit
from run_qpf001_original_flower_dateholdout import DAYS, FREEZE_SHA

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / "QPF001_DATE_HOLDOUT_ORIGINAL_RESULT_20261118.json"
RECEIPT = HERE / "QPF001_POSTHOC_DATE196_MISSINGNESS_RECEIPT_20261118.json"


class QPF001PosthocSourceWithheldTests(unittest.TestCase):
    def setUp(self):
        self.old = json.loads(ORIGINAL.read_text(encoding="utf-8"))
        self.r = json.loads(RECEIPT.read_text(encoding="utf-8"))

    def test_original_frozen_primary_invariant(self):
        self.assertEqual(self.old["protocol_commit"], FREEZE_SHA)
        self.assertEqual(self.old["registered_decision"],
                         "NO_ROBUST_WITHIN_STUDY_DATE_TRANSFER_GAIN")
        self.assertEqual(self.r["original_scientific_decision"],
                         self.old["registered_decision"])
        self.assertEqual(self.r["original_source"]["original_protocol_commit"], FREEZE_SHA)
        self.assertFalse(self.r["current_results_modified"])
        self.assertEqual(
            self.r["status"], "POSTHOC_DESCRIPTIVE_NOT_A_NEW_CONFIRMATORY_TEST"
        )

    def test_exact_mse_contribution_identity_not_a_refit(self):
        meta = audit.decompose_frozen_folds(self.old)
        stored = self.r["original_model_score_accounting"]
        self.assertEqual(meta["other7_dates_n"], 89)
        self.assertEqual([r["day"] for r in meta["all_frozen_date_score_contributions"]],
                         list(DAYS))
        self.assertAlmostEqual(
            stored["day196_contribution_to_original_all93_mse_gain"],
            meta["day196_score_contribution_to_93flower_mse_gain"], places=13
        )
        self.assertAlmostEqual(
            stored["other7days_original_predictions_mean_M0_minus_M1_mse_gain_NO_REFIT"],
            meta["other7_dates_original_prediction_mse_gain_without_refit"],
            places=13
        )
        self.assertAlmostEqual(
            stored["original_all93_M0_minus_M1_mse_gain"],
            self.old["pooled"]["M0_minus_M1_mse"],places=13
        )
        self.assertGreater(
            stored["day196_contribution_to_original_all93_mse_gain"],
            stored["original_all93_M0_minus_M1_mse_gain"]
        )
        self.assertLess(
            stored["other7days_original_predictions_mean_M0_minus_M1_mse_gain_NO_REFIT"],0
        )

    def test_original_flower_and_missing_fruit_grain(self):
        rows = self.r["film_day_ascertainment_and_original_predictions"]
        self.assertEqual([r["day"] for r in rows], list(DAYS))
        self.assertEqual([r["n_filmed"] for r in rows], [31,18,26,20,8,6,8,5])
        self.assertEqual([r["n_seedset_observed"] for r in rows], [16,18,18,18,7,4,8,4])
        self.assertEqual(sum(r["n_seedset_missing"] for r in rows), 29)
        self.assertEqual(sum(r["n_neighborhood_missing_among_recovered"] for r in rows),5)
        self.assertEqual(sum(r["n_neighborhood_missing_among_unrecovered"] for r in rows),1)
        d196 = rows[-1]
        self.assertEqual(d196["n_seedset_observed"], 4)
        self.assertEqual(d196["n_neighborhood_missing_among_recovered"],4)
        self.assertAlmostEqual(d196["mean_recorded_seedset"], .005, places=13)
        self.assertAlmostEqual(d196["mean_original_M0_day_heldout_prediction"],
                               .7739837606244953, places=12)
        self.assertAlmostEqual(d196["mean_original_M1_day_heldout_prediction"],
                               .7530552589601156, places=12)
        self.assertEqual(self.r["recovery_selection_descriptives"]
                         ["n_missing_on_days_176_and_178"],23)

    def test_partial_identification_bounds_not_zero_imputation(self):
        r = self.r["partial_identification_of_hypothetical_all122_seedset_mean"]
        self.assertTrue(r["no_missing_at_random_assumption"])
        self.assertTrue(r["no_zero_imputation_in_original_QPF001_predictive_analysis"])
        known = sum(x["n_seedset_observed"] * x["mean_recorded_seedset"]
                    for x in self.r["film_day_ascertainment_and_original_predictions"])
        self.assertAlmostEqual(known,r["known_seedset_sum_from_93"], places=11)
        self.assertAlmostEqual(known/122,
                               r["worst_case_zero_for_all_unrecovered_lower_bound"],places=12)
        self.assertAlmostEqual((known+29)/122,
                               r["worst_case_one_for_all_unrecovered_upper_bound"],places=12)
        self.assertAlmostEqual(r["identification_interval_width"],29/122,places=12)

    def test_source_outcome_mismatch_and_no_new_effects(self):
        d=self.r["source_seedset_definition_mismatch_10_fruits_by_date"]
        self.assertEqual(sum(d.values()),10)
        self.assertEqual(d,{"176":1,"177":4,"178":1,"182":1,"183":2,"191":1})
        self.assertEqual(self.r["recovery_selection_descriptives"]["recovered"]["n"],93)
        self.assertEqual(self.r["recovery_selection_descriptives"]["unrecovered"]["n"],29)
        self.assertGreater(
            self.r["recovery_selection_descriptives"]["unrecovered"]["mean_CP_grains"],
            self.r["recovery_selection_descriptives"]["recovered"]["mean_CP_grains"]
        )
        self.assertFalse(self.r["source_raw_individual_flowers_disclosed"])
        self.assertIn("No p-values", self.r["inferential_status"])
        self.assertFalse((HERE/"FIGO_2019_Data_20210523.xlsx").exists())

    def test_synthetic_source_function_and_wrong_archive_stops(self):
        fake = {
            "Duration.hours": 2.0, "Large.bee.visits":2.0,
            "Small.bee.visits":2.0,"Small.fly.visits":1.0,
            "Large.fly.visits":1.0,
        }
        self.assertEqual(audit.original_visits_hour(fake), 3.0)
        self.assertIsNone(audit.mean_or_none([],lambda x:x))
        with TemporaryDirectory() as tmp:
            bad = Path(tmp)/"fake-original.zip"
            bad.write_bytes(b"wrong-archive-content")
            with self.assertRaises(ValueError):
                audit.source_diagnostic(bad)


if __name__=="__main__":
    unittest.main()
