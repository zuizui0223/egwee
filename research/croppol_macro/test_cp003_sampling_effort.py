"""CP003 strict cross-table effort fixture tests, synthetic original-shaped rows only."""
import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import audit_cp001_source_coverage as old
import audit_cp003_sampling_effort as cp

def raw(header,rows):
    buf=io.StringIO(newline="")
    writer=csv.DictWriter(buf,fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue().encode()

def f(study="STUDY_A",group="A",site="S1",year="2001",**fields):
    return {
       "study_id":study,"study_id2":group,"site_id":site,"sampling_year":year,
       "crop":"synthetic_crop","country":"synthetic_country",
       "yield":"0","yield_units":"kg per hectare",
       "visitation_rate":"0","visitation_rate_units":"visits per 100 flowers and hour",
       "sampling_visitation":"focal observations","taxa_recorded":"all visitors",
       "use_visits_or_abundance":"use visits",
       **fields,
    }

def s(study="STUDY_A",site="S1",method="focal observations",time="60",flowers="100",area="10",**fields):
    return {
       "study_id":study,"site_id":site,
       "sampling_method":method,"pollinator":"PRIVATE_TAXON",
       "guild":"PRIVATE_GUILD","abundance":"2",
       "total_sampled_time":time,"total_sampled_area":area,
       "total_sampled_flowers":flowers,**fields,
    }

class EffortTests(unittest.TestCase):
    def test_pinned_two_original_source_contracts(self):
        self.assertEqual(cp.SAMPLE_PIN["commit"],old.MANIFEST["commit"])
        self.assertEqual(cp.SAMPLE_PIN["size"],22084522)
        self.assertEqual(cp.SAMPLE_PIN["blob"],"b7ab3fd92da0be5e8ec41b6ada50c2da7d4756c2")
        self.assertEqual(cp.SAMPLE_PIN["url"],"https://raw.githubusercontent.com/ibartomeus/CropPol/febec7dcc088ccf1bd721c41ce8dda87a2dcba1a/Final_Data/CropPol_sampling_data.csv")
        self.assertEqual(len(cp.SAMPLING_HEADER),12)

    def test_source_timed_effort_repeated_taxa_is_once_not_sum(self):
        tbl=[s(),s(pollinator="DIFFERENT_PRIVATE_TAXON")]
        items,summary=cp.sampling_summary(raw(cp.SAMPLING_HEADER,tbl),expected_rows=2)
        o=items[("STUDY_A","S1")]
        self.assertEqual(o.n,2)
        self.assertEqual(o.tier("total_sampled_time"),"unique_complete")
        self.assertEqual(o.unique_number("total_sampled_time"),60)
        self.assertEqual(len(o.status["total_sampled_time"]["positive"]),1)
        self.assertEqual(summary["distinct_complete_sampling_site_keys"],1)
        self.assertEqual(cp.global_sampling_quality(items,{("STUDY_A","S1"):1})["keys"]["keys_with_repeated_taxon_or_method_rows"],1)

    def test_multi_method_source_and_multiple_different_efforts_do_not_recover(self):
        tbl=[s(),s(method="transect",time="120")]
        items,_=cp.sampling_summary(raw(cp.SAMPLING_HEADER,tbl),expected_rows=2)
        self.assertEqual(items[("STUDY_A","S1")].tier("total_sampled_time"),"not_unique_positive")
        self.assertEqual(len(items[("STUDY_A","S1")].status["total_sampled_time"]["positive"]),2)

    def test_method_ambiguity_not_silently_discarded(self):
        x=cp.SampleSummary()
        x.add(s(method="focal observations"))
        x.add(s(method="transects"))
        self.assertEqual(x.tier("total_sampled_time"),"method_ambiguous")
        self.assertEqual(x.unique_number("total_sampled_time"),60)

    def test_missing_zero_invalid_vs_recoverable(self):
        x=cp.SampleSummary()
        x.add(s(time="60"));x.add(s(time="NA"))
        self.assertEqual(x.tier("total_sampled_time"),"possible_partial_only")
        x.add(s(time="0"))
        self.assertEqual(x.tier("total_sampled_time"),"not_unique_positive")
        self.assertEqual(x.status["total_sampled_time"]["n_missing"],1)
        self.assertEqual(x.status["total_sampled_time"]["n_zero"],1)
        x.add(s(time="-3"))
        self.assertEqual(x.status["total_sampled_time"]["n_negative"],1)
        x.add(s(time="BAD_PRIVATE"))
        self.assertEqual(x.status["total_sampled_time"]["n_invalid"],1)

    def test_sampling_year_absent_cannot_claim_field_year(self):
        fields=[
          f(study="STUDY_A",site="S1",year="2001"),
          f(study="STUDY_A",site="S1",year="2002"),
          f(study="STUDY_B",group="B",site="S2",year="2001"),
        ]
        group,keys=cp.field_frames(raw(old.EXPECTED_COLUMNS,fields),expected=(3,3,3))
        sample_rows=[s(study="STUDY_A",site="S1"),
                     s(study="STUDY_B",site="S2"),
                     s(study="STUDY_B",site="S2",pollinator="PRIVATE_TAXON_2")]
        sample,_=cp.sampling_summary(raw(cp.SAMPLING_HEADER,sample_rows),expected_rows=3)
        res=cp.source_frame_summary(group["strict_direct_timed_visit"],keys,sample)
        n=res["metadata_and_effort_counts"]
        self.assertEqual(n["field_rows_with_shared_study_site_multiple_year_or_other_field"],2)
        self.assertEqual(n["field_rows_unique_study_site_across_full_source"],1)
        self.assertEqual(n["total_sampled_time_possible_new_field_effort_without_overwrite"],1)
        self.assertEqual(n["total_sampled_flowers_unique_complete_sampling_effort"],1)

    def test_cross_file_disagreement_is_not_overwritten(self):
        rows=[f(study="STUDY_B",group="B",site="S2",
                total_sampled_time="33",total_sampled_area="NA")]
        fr,keys=cp.field_frames(raw(old.EXPECTED_COLUMNS,rows),expected=(1,1,1))
        sample,_=cp.sampling_summary(raw(cp.SAMPLING_HEADER,[s(study="STUDY_B",site="S2",time="60")]),expected_rows=1)
        res=cp.source_frame_summary(fr["strict_direct_timed_visit"],keys,sample)
        self.assertEqual(res["metadata_and_effort_counts"]["total_sampled_time_cross_table_disagreement"],1)
        self.assertEqual(res["metadata_and_effort_counts"]["total_sampled_area_possible_new_field_effort_without_overwrite"],1)

    def test_original_file_headers_must_match(self):
        with self.assertRaises(ValueError):
            list(cp.tabular_rows(b"study_id,site_id\nA,one\n",cp.SAMPLING_HEADER))
        with self.assertRaises(ValueError):
            list(cp.tabular_rows(b"study_id,site_id\nA,one\n",tuple(old.EXPECTED_COLUMNS)))

    def test_source_labels_and_private_fields_do_not_leak(self):
        field=[f(study="PRIVATE_STUDY",group="PRIVATE_GROUP",site="PRIVATE_SITE")]
        sample=[s(study="PRIVATE_STUDY",site="PRIVATE_SITE",
                  method="PRIVATE_METHOD",pollinator="PRIVATE_TAXON")]
        fs,k=cp.field_frames(raw(old.EXPECTED_COLUMNS,field),expected=(1,1,1))
        sc,_=cp.sampling_summary(raw(cp.SAMPLING_HEADER,sample),expected_rows=1)
        out=json.dumps({"q":cp.global_sampling_quality(sc,k),
                        "f":cp.source_frame_summary(fs["strict_direct_timed_visit"],k,sc)})
        for word in ("PRIVATE_STUDY","PRIVATE_SITE","PRIVATE_GROUP","PRIVATE_METHOD","PRIVATE_TAXON"):
            self.assertNotIn(word,out)

    def test_source_access_stop_returns_nonzero_and_sanitized_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            file=Path(tmp)/"out.json"
            with patch.object(cp.cp001,"fetch_verified_source",side_effect=TimeoutError("PRIVATE_DETAIL")),\
                 patch("sys.argv",["audit","--output",str(file)]),contextlib.redirect_stdout(io.StringIO()):
                rc=cp.main()
            x=json.loads(file.read_text())
            self.assertEqual(rc,2)
            self.assertEqual(x["status"],"ORIGINAL_SOURCE_OR_GRAIN_STOP")
            self.assertNotIn("PRIVATE_DETAIL",json.dumps(x))

if __name__=="__main__":unittest.main()
