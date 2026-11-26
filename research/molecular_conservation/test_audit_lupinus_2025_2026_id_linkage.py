#!/usr/bin/env python3
import unittest
from audit_lupinus_2025_2026_id_linkage import summarize

class LineageGateTests(unittest.TestCase):
    def test_label_reuse_not_pedigree(self):
        a={"article_id":28304024,"sha256":"a"*64,"rows":[
           {"population":"P","line":"GFL","id":"X"},
           {"population":"P","line":"CTRL","id":"Y"}]}
        b={"article_id":29606180,"sha256":"b"*64,"rows":[
           {"population":"P","line":"GFL","id":"X"},
           {"population":"P","line":"GFL","id":"Z"}]}
        r=summarize(a,b)
        self.assertEqual(r["exact_id_label_overlap_across_generations"],1)
        self.assertEqual(r["shared_population_line_category_count"],1)
        self.assertFalse(r["direct_maternal_lineage_link_confirmed"])
        self.assertFalse(r["same_individual_cross_year_link_confirmed"])
        self.assertEqual(r["independent_original_programmes_count"],1)
        self.assertFalse(r["outcome_columns_read"])
        self.assertNotIn('"X"',str(r))
        self.assertNotIn('"GFL"',str(r))

    def test_nonmatching_lineage_stops(self):
        a={"article_id":28304024,"sha256":"a"*64,
           "rows":[{"population":"P","line":"A","id":"001"}]}
        b={"article_id":29606180,"sha256":"b"*64,
           "rows":[{"population":"Q","line":"B","id":"900"}]}
        r=summarize(a,b)
        self.assertEqual(r["shared_population_line_category_count"],0)
        self.assertEqual(r["exact_population_id_label_overlap_across_generations"],0)
        self.assertEqual(r["decision"],"SOURCE_PEDIGREE_CROSSWALK_REQUIRED_BEFORE_ANY_CROSS_YEAR_EFFECT")

if __name__=="__main__":
    unittest.main()
