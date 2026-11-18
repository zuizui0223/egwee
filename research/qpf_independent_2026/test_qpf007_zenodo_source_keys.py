"""QPF007 original Zenodo source-only gate contracts, with MOCK data only."""
from __future__ import annotations

from unittest.mock import patch
import hashlib
import json
from pathlib import Path
import unittest

import audit_brassica_rapa_zenodo_source_keys as q

HERE=Path(__file__).resolve().parent
FROZEN=HERE/"QPF007_SOURCE_ONLY_FREEZE_20261118.json"


def tsv(s):
    return s.encode("utf-8")


class SourceGate(unittest.TestCase):
    def test_original_freeze_is_fully_source_only(self):
        p=json.loads(FROZEN.read_text(encoding="utf-8"))
        self.assertEqual(p["original_public_data"]["zenodo_record"],q.ID)
        self.assertEqual(p["status"],"SOURCE_DISCOVERY_FREEZE_NO_BIOLOGICAL_OUTCOMES_ACCESSED")
        self.assertEqual(len(p["original_public_data"]["whitelist"]),5)
        self.assertIn("session+ID_full",p["source_only_gate"]["exact_joint_grain"])
        self.assertIn("NOT",p["next_outcome_test_if_verified"]["status"])

    def test_host_rejects_external_and_unrelated_records(self):
        for url in (
            "https://example.com/api/records/21628183",
            "http://zenodo.org/api/records/21628183",
            "https://zenodo.org/api/records/21628184",
            "https://zenodo.org/records/21628183/malware",
        ):
            with self.assertRaises(ValueError):
                q.trusted_get(url, 1000)

    def test_parse_source_bio_keys_but_never_numeric_response(self):
        data=tsv(
            "session\tID_full\tpoll_treat_factor\tSR_all\tnb_visit\n"
            "1.A\tPlantX\tlow\t500\t999999\n"
            "1.A\tPlantY\tlow\t99999\t3\n"
            "2.A\tPlantX\thigh\t99999\t1\n"
        )
        headers,_,n,keys,sessions=q.decode_table(data)
        self.assertEqual(n,3)
        self.assertEqual(len(keys),3)
        self.assertEqual(len(sessions),2)
        self.assertIn("SR_all",headers)
        self.assertNotIn("99999",str(n)+str(len(keys)))
        pollen=tsv(
            "session;ID_full;id_flow;pl\n"
            "1.A;PlantX;FlowerA;999998\n"
            "1.A;PlantX;FlowerB;999997\n"
            "2.A;PlantX;FlowerC;999996\n"
        )
        _,_,n2,k2,ss2=q.decode_table(pollen)
        self.assertEqual(n2,3)
        self.assertEqual(len(k2),2)
        self.assertEqual(len(keys.intersection(k2)),2)

    def test_invalid_source_file_metadata_rejected(self):
        original={
            "key":"data_ABPOLL_ID_resume.txt","size":5,
            "checksum":"md5:00000000000000000000000000000000",
            "links":{"self":"https://zenodo.org/api/records/21628183/files/data_ABPOLL_ID_resume.txt/content"}
        }
        with patch.object(q,"trusted_get",return_value=b"hello"):
            with self.assertRaises(ValueError):
                q.trusted_binary(original)
        x={**original,"checksum":"md5:"+hashlib.md5(b"hello").hexdigest()}
        with patch.object(q,"trusted_get",return_value=b"hello"):
            self.assertEqual(q.trusted_binary(x),b"hello")
        with patch.object(q,"trusted_get",return_value=b"hell"):
            with self.assertRaises(ValueError):
                q.trusted_binary(x)

    def test_aggregate_receipt_never_opens_signed_effect(self):
        record={"id":q.ID,"doi":q.RECORD_DOI,
                "metadata":{"title":"Original field-data study"},
                "files":[]}
        file_data={
          "README.txt":b"original author README\n",
          "data_ABPOLL_ID_resume.txt":tsv("session\tID_full\tSR_all\n1.A\tA\t4\n1.A\tB\t6\n"),
          "data_ABPOLL_flower_resume.txt":tsv("session\tID_full\tid_flow\tpl\n1.A\tA\tf1\t350\n"),
          "data_ABPOLL_fix10_paternities.txt":tsv("session\tID_full\tparent\n1.A\tA\tX\n"),
          "data_ABPOLL_ID_level_ID.txt":tsv("session\tID_full_foc\tID_full_part\tseed_couple_on_foc\n1.A\tA\tB\t9999\n"),
        }
        record["files"]=[
          {"key":name,"size":len(body),
           "checksum":"md5:"+hashlib.md5(body).hexdigest(),
           "links":{"self":f"https://zenodo.org/api/records/{q.ID}/files/{name}/content"}}
          for name,body in file_data.items()
        ]
        with patch.object(q,"load_manifest",return_value=record), \
             patch.object(q,"trusted_binary",side_effect=lambda f:file_data[f["key"]]):
            x=q.schema_audit()
        self.assertTrue(x["biological_ID_join_proven"])
        self.assertEqual(x["status"],"ORIGINAL_SAME_PLANT_Q_P_F_STRUCTURAL_GATE_PASSED_NO_OUTCOME_FITTED")
        self.assertEqual(x["exact_source_session_plant_key_grain"]["observed_ID_level_stigma_overlap"],1)
        self.assertEqual(x["frozen_atlas_6_source_denominator_increment"],0)
        self.assertFalse(x["raw_numeric_pollen_paternity_seed_or_visitor_values_read"])
        self.assertFalse(x["original_rows_and_IDs_exported"])
        self.assertFalse(x["new_ecological_effect_fitted"])
        self.assertNotIn("9999",json.dumps(x))

    def test_mock_invalid_doi_fails(self):
        with patch.object(q,"trusted_get",return_value=json.dumps({
            "id":q.ID,"doi":"10.5281/zenodo.999","files":[]}).encode()):
            with self.assertRaises(ValueError):
                q.load_manifest()


if __name__=="__main__":
    unittest.main()
