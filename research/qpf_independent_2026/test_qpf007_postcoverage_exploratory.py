"""QPF007 after-coverage exploratory comparison, never a preregistered pass.

All rows synthetic. The actual 2026 source is re-read only in original Actions
workflow and exports aggregate result; no individual original values in repo.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest.mock import patch
import unittest

import run_qpf007_brassica_2026_session_holdout as base
import run_qpf007_postcoverage_all145_exploratory as q

HERE=Path(__file__).resolve().parent
LOCK=HERE/"QPF007_FROZEN_POSTCOVERAGE_EXPLORATORY_20261118.json"


def synthetic_like_original_with_15_NA():
    h=("session","ID_full","poll_treat","nb_visit","nb_flo_all",
       "height_max","pl_mean","nbGr_mean")
    lines=[" ".join('"'+v+'"' for v in h)]
    src=base.full_source_rows if False else None
    for k in range(160):
        missing_seed=k in (set(range(6))|{10,20,30,40,50,60,70})
        missing_pollen=k in {10,80,90}
        row=[
            str(1+k//10),"SYNTHETIC_ID_"+str(k),("low","med","high")[k%3],
            str(k%7+1),str(k%5+3),str(11+k%8),
            "NA" if missing_pollen else str(k%13+1),
            "NA" if missing_seed else str((k*3)%11+1),
        ]
        lines.append(str(k+1)+" "+" ".join('"'+v+'"' for v in row))
    raw=("\n".join(lines)+"\n").encode()
    parsed=base.full_source_rows(raw)
    assert len(parsed)==160
    return raw,parsed


class PostCoverageExploratoryContract(unittest.TestCase):
    def test_commit_history_and_exact_poststop_linguistic_status(self):
        p=q.verify_poststop_provenance()
        self.assertEqual(p,json.loads(LOCK.read_text(encoding="utf-8")))
        self.assertEqual(p["scientific_predecessor"]["original_coverage_result"],
                         "COVERAGE_STOP_NO_ORIGINAL_SOURCE_PREDICTIVE_TEST")
        self.assertFalse(p["scientific_predecessor"]["no_previous_signed_model_fits"] is False)
        self.assertIn("NEVER_CONFIRMATORY",
                      p["exploratory_followup"]["decision_classification"])

    def test_original_coverage_still_fails_and_explicit_exploratory_n145_includes_small_group(self):
        raw,rec=synthetic_like_original_with_15_NA()
        self.assertEqual(len(rec),160)
        no,source_stop=base.materialize_eligibility(rec,160)
        self.assertIsNone(no)
        self.assertEqual(source_stop["status"],
                         "COVERAGE_STOP_NO_ORIGINAL_SOURCE_PREDICTIVE_TEST")
        self.assertEqual(source_stop["source_complete_case_n"],145)
        self.assertEqual(source_stop["source_excluded_rows"],15)
        self.assertEqual(source_stop["n_original_session_groups_with_eligible_mothers"],16)
        self.assertEqual(source_stop["n_source_sessions_below_six_complete_plant_units"],1)
        admitted,rec2=base.materialize_eligibility(rec,160,strict_coverage=False)
        self.assertEqual(len(admitted),145)
        self.assertEqual(rec2["status"],
                         "EXPLORATORY_POSTCOVERAGE_SOURCE_145_WITH_ONE_SMALL_SESSION")
        self.assertTrue(rec2["not_original_registered_confirmation"])
        self.assertEqual(len({r["session"] for r in admitted}),16)
        self.assertEqual(min(rec2["session_group_sizes_sorted"]),4)
        self.assertEqual(max(rec2["session_group_sizes_sorted"]),10)

    def test_original_source_model_whole_programme_exploratory_runs_no_raw_rows_exported(self):
        raw,original=synthetic_like_original_with_15_NA()
        pairs={(r["session"],r["ID_full"]) for r in original}
        manifest={"files":[{"key":base.PLANT_SOURCE_FILE}]}
        with patch.object(q,"load_manifest",return_value=manifest), \
             patch.object(q,"trusted_binary",return_value=raw), \
             patch.object(q,"original_stigma_keys",return_value=pairs), \
             patch.object(q,"PLANT_SOURCE_SHA",hashlib.sha256(raw).hexdigest()):
            result=q.analyze()
        self.assertEqual(result["status"],
                         "ORIGINAL_SOURCE_POSTCOVERAGE_EXPLORATORY_FOLD_SCORES_COMPUTED")
        self.assertEqual(result["confirmation_source_gate_result"],
                         "COVERAGE_STOP_NO_ORIGINAL_SOURCE_PREDICTIVE_TEST")
        self.assertFalse(result["confirmed_original_registered_predictive_result"])
        self.assertEqual(result["source_complete_mother_n"],145)
        self.assertEqual(result["source_excluded_plant_n"],15)
        self.assertEqual(len(result["session_folds"]),16)
        self.assertEqual(sum(f["n_maternal_source_plants"] for f in result["session_folds"]),145)
        self.assertLess(result["independent_numeric_verification"]
                        ["max_absolute_heldout_prediction_discrepancy"],1e-8)
        self.assertFalse(result["source_data_redistributed"])
        self.assertFalse(result["original_source_plant_IDs_disclosed"])
        self.assertEqual(result["no_new_confirmatory_decision"],
                         "EXPLORATORY_POSTSTOP_DIAGNOSTIC_ONLY_NEVER_CONFIRMATORY")

    def test_original_readout_has_no_legacy_prereg_decision_override(self):
        p=q.verify_poststop_provenance()
        self.assertEqual(p["original_protocol_commit"] if "original_protocol_commit" in p else
                         p["scientific_predecessor"]["original_confirmatory_lock_commit"],
                         base.FREEZE_COMMIT)
        self.assertIn("one low-completeness session",p["exploratory_followup"]["changes_from_earlier_model"])
        self.assertFalse((HERE/"data_ABPOLL_ID_resume.txt").exists())
        self.assertFalse((HERE/"data_ABPOLL_flower_resume.txt").exists())


if __name__=="__main__":
    unittest.main()
