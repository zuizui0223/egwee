import unittest
from validate_joint_state_schema import audit

def base():
    cols=["population_id","mother_id","year","cohort_id","value"]
    return {"schema_version":1,
            "layers":{x:{"columns":cols,"original_sha256":"synthetic-fixture-only"} for x in ("genetics","interaction","function")},
            "source_declares_key_semantics":True,"source_declares_temporal_order":True,
            "outcome_observation_denominator_declared":True}

class GateTests(unittest.TestCase):
    def test_complete_synthetic_schema_only(self):
        self.assertEqual(audit(base())["decision"],"SCHEMA_ONLY_ELIGIBLE_FOR_ID_AUDIT")
    def test_row_order_not_key(self):
        x=base()
        for k in x["layers"]: x["layers"][k]["columns"]=["row_number","value"]
        self.assertEqual(audit(x)["decision"],"STOP_NO_SAME_POPULATION_YEAR")
    def test_unverified_semantics(self):
        x=base();x["source_declares_key_semantics"]=False
        self.assertEqual(audit(x)["decision"],"STOP_UNVERIFIED_KEY_SEMANTICS")
    def test_no_denominator(self):
        x=base();x["outcome_observation_denominator_declared"]=False
        self.assertEqual(audit(x)["decision"],"STOP_MISSING_OUTCOME_DENOMINATOR")
    def test_missing_provenance(self):
        x=base();x["layers"]["genetics"]["original_sha256"]=""
        self.assertEqual(audit(x)["decision"],"STOP_UNVERIFIED_SOURCE_PROVENANCE")

if __name__=="__main__":
    unittest.main()
