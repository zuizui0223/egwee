"""CP004 source-withheld field-size vs timed visits ranks: synthetic tests only."""
import json
import unittest
from unittest.mock import patch

import audit_cp004_source_heldout_yield_ranks as cp
import audit_cp002_measurement_sources as cp2

def fake(component,pairs,block_id="A"):
    return {"source_component":("original",str(component)),
            "comparison_key":(("original",str(component)),block_id),
            "n_fields":5,"n_nontied_outcome_pairs":len(pairs),
            "n_tied_outcome_pairs":0,
            "visit_predictor_varies":True,"pairs":pairs}
def f(study,site,field_size,visit,output):
    return {"study_id":study,"study_id2":study,"site_id":site,
            "sampling_year":"2001","crop":"synthetic_crop",
            "yield_units":"kg per hectare","visitation_rate_units":"visits per 100 flowers and hour",
            "sampling_visitation":"focal observations","taxa_recorded":"all visitors",
            "field_size":str(field_size),"visitation_rate":str(visit),"yield":str(output)}

class RankTests(unittest.TestCase):
    def test_midrank_ties_and_scale_invariance(self):
        self.assertEqual(cp.midranks([1,1,3,4]),[-1/3,-1/3,1/6,1/2])
        a=cp.midranks([1,2,3,4,5])
        self.assertEqual(a,cp.midranks([100,200,300,400,500]))
        self.assertEqual(a,cp.midranks([0,1,2,3,4]))

    def test_concordance_ties_are_half_not_dropped(self):
        p=[((0,0),1),((1,0),1),((-1,0),-1),((1,0),-1)]
        self.assertAlmostEqual(cp.concordance(p,[1]),(0.5+1+1+0)/4)
        self.assertIsNone(cp.concordance([],[1]))

    def test_source_balancing_is_not_displaced_by_doubling_taxon_pairs(self):
        basic={
           ("original","A"):[fake("A",[((0.5,0),1),((-0.5,0),-1)])],
           ("original","B"):[fake("B",[((0.5,0),-1),((-0.5,0),1)])],
           ("original","C"):[fake("C",[((0.5,0),1),((-0.5,0),-1)])],
           ("original","D"):[fake("D",[((0.5,0),1),((-0.5,0),-1)])],
           ("original","E"):[fake("E",[((0.5,0),1),((-0.5,0),-1)])],
           ("original","F"):[fake("F",[((0.5,0),1),((-0.5,0),-1)])],
           ("original","G"):[fake("G",[((0.5,0),1),((-0.5,0),-1)])],
           ("original","H"):[fake("H",[((0.5,0),1),((-0.5,0),-1)])],
        }
        out1=cp.ridge(basic,("original","H"),False)
        doubled={k:[{**v[0],"pairs":v[0]["pairs"]*10}] if k==("original","A") else v
                 for k,v in basic.items()}
        out2=cp.ridge(doubled,("original","H"),False)
        self.assertAlmostEqual(out1[0],out2[0],places=12)

    def test_test_source_parentage_yields_are_not_ever_in_training(self):
        src={}
        for i in range(8):
            label=1 if i!=7 else -1
            src[("original",str(i))]=[fake(i,[((1,0),label),((-1,0),-label)])]
        a=cp.ridge(src,("original","7"),False)
        b=cp.ridge(src,("original","0"),False)
        self.assertGreater(a[0],b[0])

    def test_exact_six_source_gate_is_not_overridden_by_positive_score(self):
        blocks=[fake(i,[((0.5,0.5),1),((-0.5,-0.5),-1)]) for i in range(7)]
        blocks.append(fake(7,[]))
        out=cp.evaluate(blocks)
        self.assertEqual(out["status"],"SOURCE_HELDOUT_RANK_COVERAGE_STOP")
        self.assertFalse(out["effect_estimated"])

    def test_reduced_baseline_without_visit_increment_remains_negative_not_test_error(self):
        blocks=[fake(i,[((0.5,0.5),1),((-0.5,-0.5),-1)]) for i in range(8)]
        out=cp.evaluate(blocks)
        self.assertEqual(out["status"],"SOURCE_HELDOUT_REDUCED_BASELINE_RANK_TEST_COMPLETE")
        self.assertAlmostEqual(out["source_equal_increment_M1_minus_M0"],0,places=12)
        self.assertFalse(out["predeclared_reduced_baseline_rule_pass"])
        self.assertEqual(out["source_groups_with_zero_increment"],8)

    def test_source_blocks_only_multiply_heterogeneous_within_block_outputs(self):
        rows=[f("SYNTHETIC_STUDY",f"SECRET_SITE_{i}",i+1,i+1,2*i+1) for i in range(5)]
        for r in rows:r["_component"]=("original","SECRET_COMPONENT")
        source=[((r["study_id"],r["site_id"]),r) for r in rows]
        with patch.object(cp.cp003,"field_frames",return_value=({"strict_direct_timed_visit":source},{})):
            blocks,cover=cp.source_blocks(b"unused_synthetic_bytes",expected=(5,1,1))
        self.assertEqual(cover["source_field_size_selection_rows"],5)
        self.assertEqual(cover["outcome_nontied_field_pairs"],10)
        self.assertEqual(cover["source_comparison_blocks"],1)
        out=json.dumps(cover)
        for secret in ("SECRET_SITE","SECRET_COMPONENT","SYNTHETIC_STUDY"):
            self.assertNotIn(secret,out)

    def test_source_tied_output_not_treated_as_negative_pair(self):
        rows=[f("SYNTHETIC_STUDY",f"X{i}",i+1,i+1,100) for i in range(5)]
        for r in rows:r["_component"]=("original","secret")
        source=[((r["study_id"],r["site_id"]),r) for r in rows]
        with patch.object(cp.cp003,"field_frames",return_value=({"strict_direct_timed_visit":source},{})):
            blocks,c=cp.source_blocks(b"unused",expected=(5,1,1))
        self.assertEqual(c["outcome_tied_pairs_excluded_from_pairwise_scores"],10)
        self.assertEqual(len(blocks[0]["pairs"]),0)

if __name__=="__main__":unittest.main()
