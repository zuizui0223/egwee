"""Offline QPF001 original-source, outcome-NA and day-heldout model contracts.

Uses only synthetic flower records and committed aggregate results. The user's
original third-party ZIP is neither committed nor downloaded by GitHub CI.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import math
import unittest

import run_qpf001_original_flower_dateholdout as qpf

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RECEIPT = HERE / "QPF001_DATE_HOLDOUT_ORIGINAL_RESULT_20261118.json"


def synthetic_flower_records():
    full = {176:31,177:18,178:26,182:20,183:8,190:6,191:8,196:5}
    keep = dict(qpf.SEED_COMPLETE_BY_DAY)
    out = []
    seed_seen = 0
    for day, size in full.items():
        for i in range(size):
            seed = i < keep[day]
            if seed:
                seed_seen += 1
            # Ten SYNTHETIC fruit outcomes have immature seeds in denominator
            immature = 1 if seed and seed_seen <= 10 else 0
            weight = 2 + immature
            na_neighbor = (day == 196) or (day == 191 and i == 0)
            out.append({
                "Sample.number":len(out)+1,
                "Julian.day":float(day),
                "Duration.hours":1.0,
                "Large.bee.visits":1.0+i%3,
                "Small.bee.visits":float(i%2),
                "Small.fly.visits":float((i+1)%3),
                "Large.fly.visits":float(i%4),
                "CP.Count":10.0,
                "HP.Count":5.0,
                "Con.abundance":"NA" if na_neighbor else 2.0,
                "Het.abundance":"NA" if na_neighbor else 1.0,
                "Seed.count":1.0 if seed else "NA",
                "Small.seed":float(immature) if seed else "NA",
                "Ovule":1.0 if seed else "NA",
                "Seed.weights":float(weight) if seed else 0.0,
                "Seed.set":1.0/weight if seed else "NA",
            })
    return out


class QPF001Tests(unittest.TestCase):
    def test_original_pre_outcome_protocol_unmodified_and_ancestral(self):
        qpf.verify_protocol()
        frozen = json.loads(qpf.PROTOCOL.read_text(encoding="utf-8"))
        self.assertEqual(frozen["original_source"]["xlsx_official_sha256"],qpf.XLSX_SHA)
        self.assertEqual(frozen["source_metadata_and_outcome_missingness_examined_pre_freeze"]
                         ["n_seed_complete_and_flower_context_complete"],88)
        self.assertEqual(frozen["fixed_model"]["CV"],
                         "leave one whole Julian filming day out (8 folds), all flowers from that day held out including date196; no random flower folds")
        self.assertEqual(frozen["experiment_id"],
                         "QPF001_original_flower_stigma_seed_date_holdout_v1")

    def test_all_source_denominators_and_seedset_formula_are_observed_not_zero_imputed(self):
        raw = synthetic_flower_records()
        admitted, receipt = qpf.audit_source(raw)
        self.assertEqual(len(raw),122)
        self.assertEqual(len(admitted),93)
        self.assertEqual(receipt["n_seedset_missing_NA"],29)
        self.assertEqual(receipt["n_flower_context_missing_any"],6)
        self.assertEqual(receipt["n_context_missing_among_seed_complete"],5)
        self.assertEqual(receipt["source_seedset_arithmetic"]
                         ["match_seed_count_over_seed_weights"],93)
        self.assertEqual(receipt["source_seedset_arithmetic"]
                         ["match_seed_count_over_count_plus_unfertilized_ovules"],83)
        self.assertEqual(Counter(int(x["Julian.day"]) for x in admitted),qpf.SEED_COMPLETE_BY_DAY)

    def test_gaussian_solver_and_train_only_flower_context_imputation(self):
        self.assertEqual([round(z,12) for z in qpf.solve(
            [[2.0,1.0],[1.0,2.0]],[3.0,3.0])], [1.0,1.0])
        train=synthetic_flower_records()
        train=[x for x in train if isinstance(x["Seed.set"],float) and x["Julian.day"]!=196]
        hold=[x for x in synthetic_flower_records()
              if isinstance(x["Seed.set"],float) and x["Julian.day"]==196]
        t0,h0=qpf.make_features(train,hold,False)
        self.assertEqual(len(t0[0]),9)
        self.assertEqual(len(h0[0]),9)
        t1,h1=qpf.make_features(train,hold,True)
        self.assertEqual(len(t1[0]),12)
        self.assertEqual(len(h1[0]),12)
        a=qpf.predict(train,hold,True)
        b=qpf.predict(train,[{**x,"Seed.set":-100000} for x in hold],True)
        self.assertEqual(a,b)
        self.assertTrue(all(0<=v<=1 for v in a))

    def test_original_8_date_results_source_only_boundaries(self):
        z=json.loads(RECEIPT.read_text(encoding="utf-8"))
        self.assertEqual(z["registered_decision"],"NO_ROBUST_WITHIN_STUDY_DATE_TRANSFER_GAIN")
        self.assertEqual(z["protocol_commit"],qpf.FREEZE_SHA)
        self.assertEqual(z["original_source"]["official_original_xlsx_sha256"],qpf.XLSX_SHA)
        self.assertEqual(z["source_grain"]["n_seedset_numeric"],93)
        self.assertEqual(z["source_grain"]["n_missing_seedset_NA"],29)
        self.assertEqual(z["source_variable_reconciliation"]
                         ["n_source_seedset_not_equal_to_paper_formula"],10)
        self.assertEqual(len(z["folds"]),8)
        self.assertEqual(sum(x["n"] for x in z["folds"]),93)
        self.assertEqual(z["pooled"]["positive_date_folds"],4)
        for model in ("M0","M1"):
            for metric in ("mse","mae"):
                key=f"{model}_{metric}"
                self.assertAlmostEqual(
                    sum(x["n"]*x[key] for x in z["folds"])/93,
                    z["pooled"][key],delta=1e-12,
                )
        self.assertLess(z["pooled"]["relative_mse_reduction_pct"],5)
        self.assertEqual(z["independent_numeric_check"]["n_compared_metrics"],32)
        self.assertLess(z["independent_numeric_check"]["max_absolute_discrepancy"],1e-12)
        self.assertFalse(z["raw_source_redistributed"])
        self.assertFalse(z["individual_record_rows_disclosed"])

    def test_wrong_original_archive_stops_before_any_biology(self):
        with TemporaryDirectory() as tmp:
            p=Path(tmp)/"wrong.zip"
            p.write_bytes(b"not source")
            with self.assertRaises(ValueError):
                qpf._binary_original(p)
        self.assertFalse((HERE/"FIGO_2019_Data_20210523.xlsx").exists())


if __name__=="__main__":
    unittest.main()
