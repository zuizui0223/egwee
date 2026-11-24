import unittest
from audit_lupf2_observation_support import aggregate

class SupportTests(unittest.TestCase):
    def test_only_aggregate_completeness_released(self):
        rows=[
            {"population":"FRO","line":"C","genotype":"private1","number_of_seeds":"3.5","flowering_onset":"140"},
            {"population":"FRO","line":"C","genotype":"private1","number_of_seeds":"","flowering_onset":""},
            {"population":"PIC","line":"X","genotype":"private2","number_of_seeds":"0","flowering_onset":"160"},
            {"population":"PIC","line":"X","genotype":"private2","number_of_seeds":"4","flowering_onset":""},
        ]
        d=aggregate(rows,check_denominator=False)
        self.assertEqual(sum(x["n_source_rows"] for x in d["strata"]),4)
        self.assertEqual(sum(x["n_both_present"] for x in d["strata"]),2)
        self.assertEqual(sum(x["n_fractional_numeric_seed"] for x in d["strata"]),1)
        self.assertEqual(sum(x["n_onset_missing_only"] for x in d["strata"]),1)
        self.assertNotIn("private1",str(d))
        self.assertFalse(d["no_new_model_fitted"] is False)
    def test_negative_value_refused(self):
        from run_lupf1_genotype_holdout import SourceStop
        with self.assertRaises(SourceStop):
            aggregate([{"population":"PIC","line":"X","genotype":"g",
                        "number_of_seeds":"-99","flowering_onset":"120"}],
                      check_denominator=False)

if __name__=="__main__":
    unittest.main()
