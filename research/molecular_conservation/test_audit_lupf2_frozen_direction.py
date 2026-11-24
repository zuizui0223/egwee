import unittest
import run_lupf1_genotype_holdout as baseline
import audit_lupf2_frozen_direction as audit

class FrozenSlopeTests(unittest.TestCase):
    def test_identical_frozen_predictor_reproduction(self):
        train=[]
        for gi in range(10):
            for j in range(4):
                onset=75+gi+2*j
                y=float(max(0,170-onset))/5.0
                train.append(("FRO" if gi<5 else "PIC",baseline.LINES[gi%6],
                              "group"+str(gi),float(onset),y))
        test=train[:12]
        model=audit.frozen_fit(train,True)
        old=baseline.fit_predict(train,test,True)
        new=audit.predict(test,model,True)
        self.assertTrue(all(abs(x-y)<1e-10 for x,y in zip(old,new)))
        self.assertLess(model[0][-1],0)
    def test_existing_frozen_comparison_reference_unchanged(self):
        self.assertEqual(sum(x[0] for x in audit.EXPECTED_FOLDS),2008)
        self.assertEqual(sum(x[1] for x in audit.EXPECTED_FOLDS),84)
        self.assertEqual(len(audit.EXPECTED_FOLDS),5)
        self.assertEqual(baseline.FOLDS,5)
        self.assertEqual(audit.SOURCE_SHA,
                        "7d0c86d290cf93968cf4f1b155a4ca1647ee399520d9b5ada66f74e892235734")

if __name__=="__main__":
    unittest.main()
