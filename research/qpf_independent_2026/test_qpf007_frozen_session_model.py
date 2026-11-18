"""QPF007 actual model frozen-before-outcome and synthetic source-grain/solvers.

All synthetic rows below are invented for unit testing. Never commit the
original 2026 source plant/flower/paternity records or individual values.
"""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
import math
from unittest.mock import patch
import unittest

import run_qpf007_brassica_2026_session_holdout as q

HERE = Path(__file__).resolve().parent
LOCK = HERE / "QPF007_FROZEN_SESSION_HELDOUT_MODEL_20261118.json"
GRAIN = HERE / "QPF007_VERIFIED_ORIGINAL_PLANT_GRAIN_20261118.json"


def synth_160(with_rownames=True):
    headers=("session","ID_full","poll_treat","nb_visit","nb_flo_all",
             "height_max","pl_mean","nbGr_mean")
    data=[" ".join('"'+n+'"' for n in headers)]
    for k in range(160):
        session = 1+k//10
        plant = "SYNTHETIC_MAT_"+str(k)
        treatment = ("LOW","MID","HIGH")[k%3]
        values=(str(session),plant,treatment,str(k%7+1),
                str(k%5+4),str(k%13+9),str(k%11),str(k%6+2))
        row=['"'+v+'"' for v in values]
        if with_rownames:row=[str(k+1)]+row
        data.append(" ".join(row))
    return ("\n".join(data)+"\n").encode()


class QPF007PreOutcomeModel(unittest.TestCase):
    def test_protocol_bytes_ancestor_and_exact_original_provenance(self):
        p=q.verify_frozen_science()
        self.assertEqual(p,json.loads(LOCK.read_text(encoding="utf-8")))
        self.assertEqual(p["source_original"]["source_original_sha256"],q.PLANT_SOURCE_SHA)
        self.assertEqual(p["source_original"]["source_stigma_sha256"],q.POLLEN_SOURCE_SHA)
        self.assertEqual(p["primary"]["M1"],"M0 + log1p(pl_mean), one additive original direct source pollen quantity coordinate")
        self.assertIn("12/16",p["primary"]["success_gate"])
        self.assertIn("120",p["primary"]["source_coverage_stop"])
        grain=json.loads(GRAIN.read_text(encoding="utf-8"))
        self.assertEqual(grain["source_only_join"]["matching_original_plant_keys"],160)
        self.assertEqual(grain["files"][3]["offspring_rows"],1099)
        self.assertEqual(grain["files"][4]["session_labels"],18)

    def test_r_quoted_space_tables_with_or_without_row_numbers(self):
        for rownames in (True,False):
            m=q.full_source_rows(synth_160(rownames))
            self.assertEqual(len(m),160)
            self.assertEqual(len({x["session"] for x in m}),16)
            self.assertEqual(len({(x["session"],x["ID_full"]) for x in m}),160)
            self.assertEqual(len({x["poll_treat"] for x in m}),3)

    def test_complete_source_coverage_and_no_missing_outcome_imputation(self):
        records=q.full_source_rows(synth_160())
        valid,receipt=q.materialize_eligibility(records,160)
        self.assertEqual(len(valid),160)
        self.assertEqual(receipt["complete_plant_n"],160)
        self.assertEqual(receipt["n_original_session_groups"],16)
        self.assertEqual(receipt["session_group_sizes_sorted"],[10]*16)
        bad=records.copy()
        bad[0]={**bad[0],"pl_mean":"NA"}
        yes,a=q.materialize_eligibility(bad,160)
        self.assertEqual(len(yes),159)
        self.assertEqual(a["excluded_plant_n"],1)
        for k in range(10):
            bad[k]={**bad[k],"pl_mean":"NA"}
        stopped,diag=q.materialize_eligibility(bad,160)
        self.assertIsNone(stopped)
        self.assertEqual(diag["status"],"COVERAGE_STOP_NO_ORIGINAL_SOURCE_PREDICTIVE_TEST")
        self.assertGreater(diag["n_source_sessions_below_six_complete_plant_units"],0)
        with self.assertRaises(ValueError):
            q.materialize_eligibility(records,159)

    def test_two_numeric_ridge_solves_same_heldout_predictions(self):
        records=q.full_source_rows(synth_160())
        valid,_=q.materialize_eligibility(records,160)
        tr=valid[:150]
        te=valid[150:]
        for model in ("M0","M1"):
            a=q.ridge_predict(tr,te,model,"gaussian")
            b=q.ridge_predict(tr,te,model,"coordinate")
            self.assertEqual(len(a),10)
            self.assertTrue(all(math.isfinite(t) for t in a+b))
            self.assertLess(max(abs(x-y) for x,y in zip(a,b)),1e-8)
            no_peek=q.ridge_predict(
                tr,[{**x,"y":-999999.0} for x in te],model,"gaussian"
            )
            self.assertEqual(a,no_peek)

    def test_full_session_holdout_must_keep_one_treatment_per_session(self):
        records=q.full_source_rows(synth_160())
        valid,_=q.materialize_eligibility(records,160)
        sessions=sorted({r["session"] for r in valid})
        self.assertEqual(len(sessions),16)
        errs=[]
        for session in sessions:
            train=[r for r in valid if r["session"]!=session]
            held=[r for r in valid if r["session"]==session]
            self.assertEqual((len(train),len(held)),(150,10))
            p0=q.ridge_predict(train,held,"M0")
            p1=q.ridge_predict(train,held,"M1")
            errs.append((sum((a["y"]-v)**2 for a,v in zip(held,p0))/10,
                         sum((a["y"]-v)**2 for a,v in zip(held,p1))/10))
        self.assertEqual(len(errs),16)

    def test_wrong_original_publisher_source_sha_stops(self):
        data=b"fake_original_data_not_published"
        with patch.object(q,"load_manifest",return_value={"files":[
            {"key":q.PLANT_SOURCE_FILE},{"key":q.POLLEN_SOURCE_FILE}]}), \
            patch.object(q,"trusted_binary",return_value=data):
            with self.assertRaises(RuntimeError):
                q.source_analysis()
        self.assertFalse((HERE/q.PLANT_SOURCE_FILE).exists())
        self.assertFalse((HERE/q.POLLEN_SOURCE_FILE).exists())


if __name__=="__main__":
    unittest.main()
