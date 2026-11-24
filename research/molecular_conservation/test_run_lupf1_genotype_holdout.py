#!/usr/bin/env python3
"""Offline synthetic tests for frozen Lupinus genotype-cluster holdout engine."""
import unittest
import run_lupf1_genotype_holdout as m

class LUPF1Tests(unittest.TestCase):
    def test_ridge_linear_solver(self):
        self.assertEqual(m.solve([[2,0],[0,4]],[4,8]),[2,2])
    def test_fold_never_splits_genotype_key(self):
        self.assertEqual(m.fold_of("FRO|maternal-01"),m.fold_of("FRO|maternal-01"))
        self.assertTrue(0<=m.fold_of("PIC|maternal-22")<5)
    def test_source_denominators_and_group_level_engine(self):
        lengths={"C":20,"J":18,"L":20,"R":4,"T":20,"X":2}
        rows=[]
        gi=0
        for code,n in lengths.items():
            for _ in range(n):
                pop="FRO" if gi<44 else "PIC"
                genotype="g"+str(gi)
                for plant in range(36):
                    rows.append({"id":str(plant),"genotype":genotype,
                                 "population":pop,"line":code,
                                 "flowering_onset":str(42+plant%7+gi%3),
                                 "number_of_seeds":str(15+plant%7+gi%3)})
                gi+=1
        r,missing,flags,ng=m.prepare(rows)
        self.assertEqual(len(r),3024)
        self.assertEqual(ng,84)
        self.assertEqual(sum(missing.values()),0)
        self.assertEqual(sum(flags.values()),0)
        out=m.evaluate(r)
        self.assertEqual(sum(x["n_records"] for x in out["fold_results"]),3024)
        self.assertEqual(sum(x["n_genotype_groups"] for x in out["fold_results"]),84)
        self.assertFalse(out["bootstrap_is_not_full_model_refit"] is False)
    def test_negative_or_noninteger_seed_stops(self):
        import math
        self.assertIsNone(m.numeric("NA"))
        self.assertIsNone(m.numeric("inf"))
        self.assertEqual(m.numeric("0"),0.0)
    def test_phenology_feature_only_changes_M1(self):
        row=("FRO","C","FRO|g1",80.0,5.0)
        self.assertEqual(len(m.features(row,False,80,1)),7)
        self.assertEqual(len(m.features(row,True,80,1)),8)

if __name__=="__main__":
    unittest.main()
