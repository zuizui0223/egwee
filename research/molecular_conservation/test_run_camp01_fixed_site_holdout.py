import unittest
from run_camp01_fixed_site_holdout import norm,csvrows,join,evaluate,Stop

class Camp01Tests(unittest.TestCase):
    def test_schema_normalization(self):
        h,r=csvrows(b"experimental.population,source population,seed number\nA,P,0\n")
        self.assertEqual(h,["experimental_population","source_population","seed_number"])
        self.assertEqual(r[0]["seed_number"],"0")
    def test_pairing_and_crossfile_design(self):
        d={"site":"s","experimental_population":"e","source_population":"p","autonomy":"high","size":"single"}
        p=[dict(d,visits_per_flower="1")]
        seed=[dict(d,individual="i",treatment="control",seed_number="0"),
              dict(d,individual="i",treatment="supplemented",seed_number="2"),
              dict(d,individual="j",treatment="control",seed_number="4")]
        receipt={};records=join(seed,p,receipt)
        self.assertEqual(len(records),1)
        self.assertEqual(receipt["paired_plant_records"],1)
        self.assertEqual(receipt["unpaired_plant_records"],1)
        self.assertGreater(records[0][5],0)
        with self.assertRaises(Stop):join(seed,[dict(d,size="small",visits_per_flower="1")],{})
    def test_fixed_site_holdout(self):
        rs=[]
        for i in range(10):
            for j in range(4):
                a="high" if j<2 else "low"
                z="small" if (i+j)%2 else "single"
                v=(i+j*.4)/5
                y=2.+v+float(a=="high")*v*3.
                rs.append((str(i),str(j),a,z,v,y))
        out=evaluate(rs)
        self.assertEqual(out["site_folds"],10)
        self.assertEqual(sum(f["n"] for f in out["folds"]),40)
        self.assertGreater(out["gain"],0)
        with self.assertRaises(Stop):evaluate(rs[:20])
if __name__=="__main__":unittest.main()
