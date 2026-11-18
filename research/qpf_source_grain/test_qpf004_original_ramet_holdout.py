"""QPF004 original-source-withheld test contracts.

Only SYNTHETIC ramet/plant data, immutable commit ancestry and aggregate
original-source evidence. Original third-party XLSX/PDF/ZIP never in Actions.
"""
from __future__ import annotations
from collections import Counter
import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import run_qpf004_mertensia_source_weekholdout as q

HERE=Path(__file__).resolve().parent
RESULT=HERE/"QPF004_ORIGINAL_WEEK_HOLDOUT_RESULT_20261118.json"
PROTOCOL=HERE/"QPF004_FROZEN_RAMET_POLLEN_SEED_WEEK_HOLDOUT_20261118.json"


def fake_source_2016_and_2015():
    # All rows/values are synthetic. Do not mimic any real mother or flower ID.
    wk=[1]*4+[2]*18+[3]*16+[4]*20+[5]*4
    visitor=["Open"]*15+["Bombus"]*20+["Muscoidea"]*21+["Osmia"]*6
    assert len(wk)==len(visitor)==62
    allrows=[]
    for i,(week,taxon) in enumerate(zip(wk,visitor)):
        treat="O" if taxon=="Open" else "V"
        noflowers=2 if i%2==0 else 1
        seeds=(i%3)*noflowers
        allrows.append({
            "plantID":"SYNTH_R"+str(i),
            "week":float(week),
            "site":"RG" if i<38 else "SP",
            "treat":treat,"visID":taxon,
            "noFlrs":float(noflowers),
            "FlrsAvail":float(2+i%5),
            "flrsVisited":None if treat=="O" else float(noflowers),
            "seedCnt":float(seeds),"seedPerFlr":float(seeds/noflowers),
            "polDepMC":float(1+i%7),
            "polDepNonMC":float(i%3),
        })
    other_treatment=["V"]*47+["O"]*50+["B"]*73
    for j,treat in enumerate(other_treatment):
        i=62+j
        noflowers=1.
        allrows.append({
            "plantID":"SYNTH_R"+str(i),
            "week":float(1+j%5),"site":"RG" if j%2==0 else "SP",
            "treat":treat,
            "visID":"Bombus" if treat=="V" else ("Open" if treat=="O" else "Bagged"),
            "noFlrs":noflowers,"FlrsAvail":5.,
            "flrsVisited":1. if treat=="V" else None,
            "seedCnt":0.,"seedPerFlr":0.,
            "polDepMC":9999999., "polDepNonMC":9999999.,
        })
    p=[{k:r[k] for k in ("plantID","week","site","treat",
                          "polDepMC","polDepNonMC")} for r in allrows[:62]]
    seed=[{k:r[k] for k in ("plantID","week","site","treat",
                            "seedCnt","seedPerFlr","noFlrs")} for r in allrows]
    means=[]
    eligible=[1]*10+[2]*9+[3]*10+[4]*7
    allweeks=eligible+[2]+[4]*3
    for i,week in enumerate(allweeks):
        means.append({
            "plantID":"SYNTH_2015_"+str(i),"tWeek":float(week),
            "mSeed":float(i%4),"mVisRate":float(1+i%4),
            "flrCnt":float(3+i%7),"mVWC":.2+(i%4)*.1,
            "mcPolCnt":float(i%9+1) if i<36 else 9999999.,
            "nonMcPolCnt":float(i%4) if i<36 else 9999999.,
        })
    return p,seed,allrows,means


class OriginalSourceMertensiaTests(unittest.TestCase):
    def setUp(self):
        self.r=json.loads(RESULT.read_text(encoding="utf-8"))

    def test_frozen_protocol_commit_before_original_outcome_fits(self):
        q.verify_protocol()
        p=json.loads(PROTOCOL.read_text(encoding="utf-8"))
        self.assertEqual(p["experiment_id"],self.r["analysis_id"])
        self.assertEqual(self.r["preoutcome_protocol_commit"],q.FREEZE_SHA)
        self.assertEqual(p["original_sources"]["source_zip_sha256"],q.ZIP_SHA)
        self.assertEqual(p["primary_2016"]["success_gate"],
            "pooled ramet-weighted M0-M1 MSE strictly positive and >=5% M0 relative improvement and >=4/5 observation week folds strictly positive")

    def test_synthetic_exact_ramet_join_and_original_week_grain(self):
        p,s,a,m=fake_source_2016_and_2015()
        self.assertEqual((len(p),len(s),len(a),len(m)),(62,232,232,40))
        r16,r15,receipt=q.audit_rows(p,s,a,m)
        self.assertEqual(len(r16),62)
        self.assertEqual(len(r15),36)
        self.assertEqual(receipt["2016_matched_P_ramets_by_visitor"],
            {"Bombus":20,"Muscoidea":21,"Osmia":6,"Open":15})
        self.assertEqual(receipt["2016_matched_P_ramets_by_treatment"],
            {"V":47,"O":15,"B":0})
        self.assertEqual(Counter(r["week"] for r in r16),
                         Counter({1:4,2:18,3:16,4:20,5:4}))
        self.assertEqual(Counter(r["week"] for r in r15),
                         Counter({1:10,2:9,3:10,4:7}))
        self.assertTrue(all(0<=r["y"]<=4 for r in r16+r15))

    def test_synthetic_ridge_is_train_only_bounded_and_all_fold_groups(self):
        p,s,a,m=fake_source_2016_and_2015()
        r16,r15,_=q.audit_rows(p,s,a,m)
        self.assertEqual(len(q.heldout(r16,"week")["groups"]),5)
        self.assertEqual(len(q.heldout(r16,"site")["groups"]),2)
        self.assertEqual(len(q.heldout(r15,"week")["groups"]),4)
        train=[r for r in r16 if r["week"]!=1]
        test=[r for r in r16 if r["week"]==1]
        baseline=q.ridge_prediction(train,test,"M1")
        changed=[{**r,"y":-1000000} for r in test]
        self.assertEqual(baseline,q.ridge_prediction(train,changed,"M1"))
        self.assertTrue(all(0<=x<=4 and math.isfinite(x) for x in baseline))
        self.assertEqual(q.linear_solve([[2.,1.],[1.,2.]],[3.,3.]),[1.,1.])

    def test_original_11_fold_aggregate_mses_and_negative_decision(self):
        r=self.r
        self.assertEqual(r["registered_decision"],
                         "NO_PRACTICALLY_PORTABLE_POLLEN_INCREMENT")
        nfolds=0
        nmetrics=0
        for name,N,F in (
            ("primary_2016_week",62,5),
            ("secondary_2016_site",62,2),
            ("secondary_2015_week",36,4),
        ):
            section=r[name]
            folds=section["groups"]
            pool=section["pooled"]
            self.assertEqual(len(folds),F)
            self.assertEqual(sum(f["n"] for f in folds),N)
            self.assertEqual(pool["n_source_units"],N)
            for key in ("M0_MSE","M1_MSE","M0_MAE","M1_MAE"):
                got=sum(f["n"]*f[key] for f in folds)/N
                self.assertAlmostEqual(got,pool[key],delta=1e-11)
            self.assertAlmostEqual(pool["M0_MSE"]-pool["M1_MSE"],
                                   pool["gain_M0_minus_M1_MSE"],places=11)
            self.assertEqual(pool["positive_folds"],
                             sum(f["delta_M0_minus_M1_MSE"]>0 for f in folds))
            self.assertLess(pool["gain_percent"],0)
            nfolds+=F
            nmetrics+=F*6+6
        self.assertEqual((nfolds,nmetrics),(11,84))
        self.assertAlmostEqual(r["primary_2016_week"]["pooled"]["M0_MSE"],
                               .7815361133641171,places=12)
        self.assertAlmostEqual(r["primary_2016_week"]["pooled"]["M1_MSE"],
                               .8928460165385343,places=12)
        self.assertEqual(r["primary_2016_week"]["pooled"]["positive_folds"],1)
        self.assertEqual(r["secondary_2016_site"]["pooled"]["positive_folds"],0)
        self.assertEqual(r["secondary_2015_week"]["pooled"]["positive_folds"],1)

    def test_real_source_sha_and_no_raw_original_republished(self):
        self.assertEqual(self.r["original_source_zip_sha256"],q.ZIP_SHA)
        self.assertEqual(self.r["independent_numeric_verification"]
                         ["n_independent_fold_level_metrics"],84)
        self.assertLess(self.r["independent_numeric_verification"]["max_abs_difference"],1e-12)
        self.assertEqual(self.r["source_structure"]["original_2016_pollen_source_ID_matches"],62)
        self.assertFalse(self.r["original_raw_source_redistributed"])
        self.assertFalse(self.r["individual_plant_ramet_source_values_exported"])
        self.assertFalse((HERE/"doi_10_7280_D19X0D__v20200619.zip").exists())
        self.assertFalse((HERE/"gallagher&campbell_pollinatorEffectivenessData.xlsx").exists())
        with TemporaryDirectory() as t:
            s=Path(t)/"incorrect_original.zip"
            s.write_bytes(b"wrong-source")
            with self.assertRaises(ValueError):
                q.source_bytes(s)


if __name__=="__main__":
    unittest.main()
