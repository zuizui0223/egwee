"""CY002 source-withheld exact denominators, original-preregistered model and reported score QA."""
from __future__ import annotations
from pathlib import Path
import json
import math
import unittest

import run_cyanus_CY002_plot_holdout as cy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT = HERE / "CY002_ORIGINAL_PLOT_HOLDOUT_RESULT_20261118.json"
PROTOCOL = HERE / "CY002_FROZEN_SOURCE_COUNT_CORRECTION_20261118.json"
RECEIPT = HERE / "CY002_ORIGINAL_SOURCE_STRUCTURAL_RECEIPT_20261118.json"

class CY002SourceWithheldQA(unittest.TestCase):
    def setUp(self):
        self.r = json.loads(RESULT.read_text(encoding="utf-8"))
        self.p = json.loads(PROTOCOL.read_text(encoding="utf-8"))
        self.e = json.loads(RECEIPT.read_text(encoding="utf-8"))

    def test_unchanged_original_design_and_disclosed_preview(self):
        p = cy.verify_protocol()  # Git SHA, byte-identical lock, prior CY001 ancestor
        self.assertEqual(p, self.p)
        self.assertEqual(p["original_protocol_commit"], cy.ORIGINAL_CY001_FREEZE_SHA)
        self.assertFalse(p["blinding_and_analysis_disclosure"]["strictly_outcome_blind"])
        self.assertEqual(p["analysis_retained_verbatim_from_CY001"]["primary"]["positive_gate"],
                         "delta>0 AND relative reduction >=5% of M0 MSE AND positive delta in >=8 of 12 plot folds")
        self.assertEqual(self.r["source_corrected_CY002_frozen_protocol_commit"], cy.FREEZE_SHA)
        self.assertEqual(self.r["original_CY001_protocol_commit"], cy.ORIGINAL_CY001_FREEZE_SHA)

    def test_source_original_archive_and_typed_offspring(self):
        self.assertEqual(self.r["original_xlsx_sha256"], cy.ORIGINAL_SOURCE_SHA256)
        self.assertEqual(self.e["original_archive"]["original_data_xlsx_sha256"],
                         cy.ORIGINAL_SOURCE_SHA256)
        self.assertEqual(self.r["sampling"]["offspring_typed_total"], 549)
        self.assertEqual(self.e["source_structural_data"]["source_typed_offspring_total"], 549)
        self.assertEqual(self.r["sampling"]["offspring_typed_histogram"],
                         {"12":1,"15":1,"16":5,"17":26})
        self.assertEqual(self.e["source_structural_data"]["source_plot_size_histogram"],
                         {"1":1,"2":1,"3":10})
        self.assertEqual(self.r["sampling"]["source_mothers"],33)
        self.assertEqual(self.r["sampling"]["plot_folds"],12)

    def test_model_numerical_coherence_all_original_plot_cells(self):
        fs=self.r["folds"]
        self.assertEqual(len(fs),12)
        self.assertEqual(sum(x["n_mothers"] for x in fs),33)
        self.assertEqual(len({x["plot"] for x in fs}),12)
        for outcome,overall in (
            ("primary_rpm",self.r["primary_correlated_paternity"]),
            ("secondary_seed_log",self.r["secondary_selected_mother_seed_count"]),
        ):
            for model in ("M0","M1"):
                expected=sum(x["n_mothers"]*x[outcome][model+"_mse"]
                             for x in fs)/33
                self.assertAlmostEqual(overall[model+"_mse"], expected,delta=1e-11)
            self.assertAlmostEqual(overall["delta_mse_M0_minus_M1"],
                                   overall["M0_mse"]-overall["M1_mse"],places=12)
            self.assertEqual(overall["positive_plot_folds"],
                             sum(x[outcome]["delta_mse"]>0 for x in fs))
        self.assertAlmostEqual(self.r["primary_correlated_paternity"]["M0_mse"],
                               .010832423420456901,places=12)
        self.assertAlmostEqual(self.r["primary_correlated_paternity"]["M1_mse"],
                               .011468827191568344,places=12)

    def test_no_primary_reversal_or_secondary_rescue(self):
        a=self.r["primary_correlated_paternity"]
        s=self.r["secondary_selected_mother_seed_count"]
        self.assertLess(a["delta_mse_M0_minus_M1"],0)
        self.assertEqual(a["positive_plot_folds"],3)
        self.assertLess(s["delta_mse_M0_minus_M1"],0)
        self.assertEqual(s["positive_plot_folds"],4)
        self.assertEqual(self.r["primary_decision"],"NO_PRACTICALLY_PORTABLE_INCREMENT")
        self.assertIn("preview",self.r["source_blinding"].lower())

    def test_original_raw_source_not_added_to_public_branch(self):
        self.assertFalse((HERE/"Data_Dryad.xlsx").exists())
        self.assertFalse((HERE/"README.md").exists())
        self.assertFalse((HERE/"doi_10_5061_dryad_9p8cz8ws1__v20240920.zip").exists())
        self.assertIn("original third-party", " ".join(self.r["scientific_limitations"]))

if __name__ == "__main__":
    unittest.main()
