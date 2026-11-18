"""CY001 synthetic numerical checks, original 2024 Dryad workbook withheld."""
from __future__ import annotations

from pathlib import Path
import json
import hashlib
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest
import zipfile
from xml.sax.saxutils import escape

import run_cyanus_CY001_plot_holdout as cy

def fixture(path: Path):
    # All IDs, counts, rates and paternity values below are SYNTHETIC, not source.
    headings = {
        0:"Maternal_plant_identifier", 1:"N_alleles_maternal_plant_n",
        3:"rpm_progeny", 4:"Relative_MPA_n_visits_per_15_minutes",
        5:"Conspecific_pollen_donor_density", 6:"Local_floral_richness",
        7:"Local_floral_density", 21:"Plot",22:"Strip_type",
        23:"N_offspring_genotyped_n", 27:"N_seeds_n"
    }
    def address(index,row):
        x=index+1
        letters=""
        while x:
            x,remainder=divmod(x-1,26)
            letters=chr(65+remainder)+letters
        return letters+str(row)
    def cell(c,r,v):
        ref=address(c,r)
        if isinstance(v,str):
            return ('<c r="'+ref+'" t="inlineStr"><is><t>'+
                    escape(v)+'</t></is></c>')
        return '<c r="'+ref+'"><v>'+str(v)+'</v></c>'
    source=['<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>']
    source.append('<row r="1">'+''.join(cell(c,1,v) for c,v in headings.items())+'</row>')
    for i in range(33):
        plot=i//3 if i<27 else 9+(i-27)//2
        site=("F"+str(plot+1) if plot<9 else "G"+str(plot-8))
        vals={
            0:"SYNTHETIC-"+str(i),1:10+i%4,3:.1+.02*(i%8),
            4:.3+.12*(i%7),5:1.2+(i%5),6:2+i%4,7:4+i%8,
            21:site,22:"Wildflower" if plot<9 else "Grass",
            23:16+(i%2),27:40+3*i
        }
        source.append('<row r="'+str(i+2)+'">'+''.join(cell(c,i+2,v) for c,v in vals.items())+'</row>')
    source.append('</sheetData></worksheet>')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr("xl/worksheets/sheet1.xml","".join(source))

class CY001ModelTests(unittest.TestCase):
    def test_original_protocol_and_fixed_model_dimensions(self):
        p=cy.verify_protocol() if hasattr(cy,"verify_protocol") else cy.protocol()
        self.assertEqual(p["published_frame"]["selected_genetic_mother_n"],33)
        self.assertEqual(p["published_frame"]["plots_with_mothers_n"],12)
        self.assertIn("5%",p["primary"]["positive_gate"])
        self.assertEqual(cy.COL["rpm"],3)
        self.assertEqual(cy.COL["seeds"],27)

    def test_xlsx_structural_receipt_precedes_outcomes(self):
        with TemporaryDirectory() as tmp:
            src=Path(tmp)/"synthetic_only.xlsx"
            fixture(src)
            with patch.object(cy,"ORIGINAL_SOURCE_SHA256",hashlib.sha256(src.read_bytes()).hexdigest()):
                receipt=cy.source_schema(src)
            self.assertEqual(receipt["selected_mother_n"],33)
            self.assertEqual(receipt["plot_n"],12)
            self.assertEqual(receipt["strip_n"],2)
            self.assertFalse(receipt["response_values_inspected"])
            self.assertEqual(sum(receipt["plot_sizes_sorted"]),33)
            manifest=Path(tmp)/"locked_schema.json"
            manifest.write_text(json.dumps(receipt))
            with patch.object(cy,"ORIGINAL_SOURCE_SHA256",hashlib.sha256(src.read_bytes()).hexdigest()):
                outcome=cy.analyze(src,manifest)
            self.assertEqual(outcome["mothers"],33)
            self.assertEqual(outcome["nested_original_plots"],12)
            self.assertEqual(sum(f["n_mothers"] for f in outcome["folds"]),33)
            self.assertEqual(len(outcome["folds"]),12)
            self.assertIn("primary_correlated_paternity",outcome)
            self.assertIn("secondary_outcome_selected_seed_number",outcome)
            # Structural lock is binding: mutating source afterward must fail
            src.write_bytes(b"not an original workbook")
            with self.assertRaises(RuntimeError):
                cy.analyze(src,manifest)
            self.assertEqual(
                cy.ORIGINAL_SOURCE_SHA256,
                "18941f666c040c81c5db3f43c661d44fc157e9db636eef07a4aafd49f77b5332",
            )

    def test_train_only_scaling_and_bounded_rpm(self):
        def make(i):
            return {"base":[12+i%3,1+i%4,1+i%5,2+i%6,int(i%2==0)],
                    "visits":.1*i,"rpm":.05+.03*(i%9),
                    "seed_log":3+.2*i}
        train=[make(i) for i in range(1,30)]
        tests=[make(31),make(32)]
        p=cy.ridge_predict(train,tests,"rpm",True)
        q=cy.ridge_predict(train,[{**z,"rpm":999999} for z in tests],"rpm",True)
        self.assertEqual(p,q)
        self.assertTrue(all(0<=z<=1 for z in p))
        self.assertEqual(len(cy.ridge_predict(train,tests,"seed_log",False)),2)

    def test_source_columns_are_explicit_not_guessed_from_outcomes(self):
        self.assertEqual(cy.column_index("AB1"),27)
        self.assertEqual(cy.column_index("V16"),21)
        with self.assertRaises(ValueError):
            cy.column_index("***")

if __name__=="__main__":
    unittest.main()
