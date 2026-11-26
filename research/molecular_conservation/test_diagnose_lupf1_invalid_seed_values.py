import unittest
from diagnose_lupf1_invalid_seed_values import classify_seed, classify_onset, diagnose

class InvalidEndpointTests(unittest.TestCase):
    def test_noninteger_not_silently_rounded(self):
        self.assertEqual(classify_seed("1.5"),"NONINTEGER")
        self.assertEqual(classify_seed("0.0"),"VALID_INTEGER")
        self.assertEqual(classify_seed("-1"),"NEGATIVE")
        self.assertEqual(classify_seed("NA"),"MISSING_OR_NA")
        self.assertEqual(classify_seed("not measured"),"NONNUMERIC_OR_NONFINITE")
    def test_no_model_and_all_denominators(self):
        rows=[
            {"population":"FRO","line":"C","genotype":"g1","flowering_onset":"120","number_of_seeds":"12"},
            {"population":"FRO","line":"C","genotype":"g1","flowering_onset":"","number_of_seeds":"1.2"},
            {"population":"PIC","line":"X","genotype":"g2","flowering_onset":"-1","number_of_seeds":"-99"},
            {"population":"PIC","line":"X","genotype":"g2","flowering_onset":"118","number_of_seeds":""},
        ]
        r=diagnose(rows)
        self.assertEqual(r["original_rows"],4)
        self.assertEqual(r["seed_and_onset_both_valid_rows"],1)
        self.assertEqual(r["seed_value_categories"]["NONINTEGER"],1)
        self.assertEqual(r["seed_value_categories"]["NEGATIVE"],1)
        self.assertEqual(r["seed_value_categories"]["MISSING_OR_NA"],1)
        self.assertFalse(r["new_predictive_model_ran"])
        self.assertFalse(r["source_values_or_individual_ids_exported"])
        self.assertNotIn("-99",str(r))
if __name__=="__main__":
    unittest.main()
