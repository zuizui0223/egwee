import unittest
from audit_lupf2_seed_fruit_source_integrity import profile, classify
from run_lupf1_genotype_holdout import SourceStop

class FruitSeedIntegrityTests(unittest.TestCase):
    def test_fractional_seed_does_not_imply_invalid_measure(self):
        self.assertEqual(classify("2.25")[0],"NONNEGATIVE_FRACTION")
        self.assertEqual(classify("0")[0],"NONNEGATIVE_INTEGER")
        self.assertEqual(classify("NA")[0],"MISSING")
        self.assertEqual(classify("-1")[0],"NEGATIVE")
        self.assertEqual(classify("inaccessible")[0],"NONNUMERIC_NONFINITE")

    def test_completeness_and_discordance_without_ids(self):
        rows=[
          {"id":"secretOne","population":"FRO","line":"C","genotype":"secretMother",
           "number of fruits":"2","number of seeds":"8","flowering_onset":"120"},
          {"id":"secretTwo","population":"FRO","line":"C","genotype":"secretMother",
           "number of fruits":"1","number of seeds":"2.5","flowering_onset":"125"},
          {"id":"secretThree","population":"PIC","line":"J","genotype":"otherMother",
           "number of fruits":"0","number of seeds":"0","flowering_onset":""},
          {"id":"secretFour","population":"PIC","line":"J","genotype":"otherMother",
           "number of fruits":"NA","number of seeds":"1","flowering_onset":"135"},
          {"id":"secretFive","population":"PIC","line":"J","genotype":"otherMother",
           "number of fruits":"3","number of seeds":"","flowering_onset":""}
        ]
        out=profile(rows,strict=False)
        self.assertEqual(out["all_original_rows"],5)
        self.assertEqual(out["source_genotype_label_groups"],2)
        self.assertEqual(out["global_seed_categories"]["NONNEGATIVE_FRACTION"],1)
        self.assertEqual(out["by_source_population"]["TOTAL"]["both_seed_and_onset_numeric_nonnegative"],3)
        self.assertEqual(out["by_source_population"]["TOTAL"]["missing_seed_index_with_positive_fruit"],1)
        self.assertEqual(out["by_source_population"]["TOTAL"]["fruit_missing_with_numeric_seed"],1)
        self.assertEqual(out["by_source_population"]["TOTAL"]["fractional_seed_with_fruit_positive"],1)
        self.assertTrue(out["no_new_regression_or_effect_estimated"])
        self.assertNotIn("secretOne",str(out))
        self.assertNotIn("secretMother",str(out))

    def test_unknown_population_or_line_fails_closed(self):
        with self.assertRaises(SourceStop):
            profile([{"population":"FRO","line":"INVALID","genotype":"g1",
                      "number of fruits":"1","number of seeds":"2","flowering_onset":"110"}],
                    strict=False)

if __name__=="__main__":
    unittest.main()
