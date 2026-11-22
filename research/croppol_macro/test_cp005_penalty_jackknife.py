"""CP005 negative-control penalty sensitivity fixture: synthetic sources only."""
import unittest
import json

import audit_cp004_source_heldout_yield_ranks as primary
import audit_cp005_posthoc_penalty_jackknife as stage

def block(source,pairs):
    return {"source_component":("synthetic_private",str(source)),
            "comparison_key":("synthetic_private",str(source)),
            "pairs":pairs}

class PenaltyTests(unittest.TestCase):
    def setUp(self):
        self.pairs=[block(i,[((.5,.5),1),((-.5,-.5),-1),
                             ((.25,.75),1),((-.25,-.75),-1)]) for i in range(10)]
        self.grp={b["source_component"]:[b] for b in self.pairs}

    def test_exact_primary_lambda_point_one_matches_unmodified_primary(self):
        for s in self.grp:
            for two in (False,True):
                a=stage.ridge_lambda(self.grp,s,two,.1)
                b=primary.ridge(self.grp,s,two)
                self.assertEqual(len(a),len(b))
                for v,w in zip(a,b):self.assertAlmostEqual(v,w,places=12)

    def test_all_three_penalty_scenarios_return_all_source_scores(self):
        for lam in stage.PENALTIES:
            vals=stage.score(self.pairs,lam)
            self.assertEqual(len(vals),10)
            agg=stage.aggregated(vals)
            self.assertEqual(agg["positive_source_components"]+
                             agg["negative_source_components"]+
                             agg["zero_source_components"],10)
            self.assertLessEqual(agg["score_M0"],1.)
            self.assertGreaterEqual(agg["score_M1"],0.)

    def test_no_source_identifiers_in_aggregate_metrics(self):
        vals=stage.score(self.pairs,stage.PENALTIES[0])
        msg=json.dumps(stage.aggregated(vals))
        self.assertNotIn("synthetic_private",msg)

    def test_penalty_does_not_change_holdout_cohort_or_pair_count(self):
        source=self.grp
        heldout=("synthetic_private","0")
        beta0=stage.ridge_lambda(source,heldout,False,.01)
        beta1=stage.ridge_lambda(source,heldout,False,1.)
        self.assertLess(abs(beta1[0]),abs(beta0[0]))
        self.assertEqual([len(b["pairs"]) for b in self.pairs],[4]*10)

if __name__=="__main__":unittest.main()
