import unittest
import run_lupf2_exploratory_continuous_seed as m
import run_lupf1_genotype_holdout as primary

class LUPF2Tests(unittest.TestCase):
    def test_continuous_source_seed_never_rounded(self):
        self.assertEqual(m.continuous_numeric("3.25","SEED"),3.25)
        self.assertEqual(m.continuous_numeric("0","SEED"),0.0)
        self.assertIsNone(m.continuous_numeric("NA","SEED"))
        with self.assertRaises(primary.SourceStop):
            m.continuous_numeric("-1","SEED")
        with self.assertRaises(primary.SourceStop):
            m.continuous_numeric("no","SEED")
    def test_source_rows_keep_fractional_with_predeclared_grouping(self):
        rows=[
         {"population":"FRO","line":"J","genotype":"f1","number_of_seeds":"0.4","flowering_onset":"120"},
         {"population":"FRO","line":"J","genotype":"f1","number_of_seeds":"","flowering_onset":"120"},
         {"population":"PIC","line":"X","genotype":"p1","number_of_seeds":"1","flowering_onset":"121"},
         {"population":"PIC","line":"X","genotype":"p1","number_of_seeds":"2","flowering_onset":""}
        ]
        records,miss,flag,groups=m.source_prepare(rows,check_denominator=False)
        self.assertEqual(len(records),2)
        self.assertEqual(records[0][-1],0.4)
        self.assertEqual(groups,2)
        self.assertEqual(miss["missing_seed_index"],1)
        self.assertEqual(miss["missing_onset"],1)
        self.assertEqual(flag["fractional_nonnegative_seed_index"],1)
        self.assertEqual(flag["seed_numeric_onset_missing"],1)

if __name__=="__main__":
    unittest.main()
