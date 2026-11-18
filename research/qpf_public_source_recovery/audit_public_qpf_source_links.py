#!/usr/bin/env python3
"""Source-only availability probe of independent original Q-P-F natural sources.

QPF001: official Dryad source and public original-file link indexed by NDLI.
QPF002: original Dryad 13-pop paper's Zenodo RELATED WORKS (software, not
independent biological datasets). Strictly does not inspect individual pollen,
seed, outcrossing or visit data, upload third-party files, or compute effects.
"""
from __future__ import annotations

import argparse
from io import BytesIO
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen
import zipfile
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "compatibility_function"))
from audit_dryad_joint_state_source_schema import metadata_for_one

PUBLIC_FIRST_URL = "https://datadryad.org/stash/downloads/file_stream/736848"
FIRST_DOI = "10.5061/dryad.hqbzkh1g9"
RELATED_ZENODO_SOFTWARE_IDS = (10563520,10563521)
MAX_FILE = 1024*1024
MAX_JSON = 2*1024*1024
NS="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def source_get(url: str, limit: int=MAX_FILE) -> tuple[bytes, str]:
    if not (url.startswith("https://zenodo.org/api/records/") or
            url.startswith("https://datadryad.org/stash/downloads/file_stream/")):
        raise ValueError("Source url not in official published public record/known file-stream allowlist")
    r = Request(url, headers={
        "User-Agent":"EGWEE-original-flower-QPF-source-only/1.0",
        "Accept":"application/json,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*",
    })
    with urlopen(r,timeout=25) as out:
        content=out.read(limit+1)
        destination=out.url
    if len(content)>limit:
        raise ValueError("Source file larger than bounded source-gate limit")
    if not destination.startswith("https://"):
        raise ValueError("Insecure source redirect")
    return content,destination


def sheet_structure(data: bytes) -> list[dict]:
    if not zipfile.is_zipfile(BytesIO(data)):
        raise ValueError("Source response was not an original Excel ZIP")
    with zipfile.ZipFile(BytesIO(data)) as z:
        if z.testzip() is not None:
            raise ValueError("Source XLSX member CRC failed")
        result=[]
        for path in sorted(z.namelist()):
            if not re.fullmatch(r"xl/worksheets/sheet[0-9]+\.xml",path):
                continue
            root=ET.fromstring(z.read(path))
            rows=root.findall(".//"+NS+"sheetData/"+NS+"row")
            # Only names of worksheet XML and physical row/cell dimensions:
            # never read a single biological cell, even the header row.
            coords=[c.attrib.get("r","") for row in rows
                    for c in row.findall(NS+"c") if c.attrib.get("r")]
            def colindex(ref):
                letters=re.match("^[A-Z]+",ref)
                n=0
                if letters:
                    for c in letters.group(): n=n*26+(ord(c)-64)
                return n
            result.append({
                "worksheet_xml":path,
                "physical_nonempty_rows":len(rows),
                "max_recorded_column_index":max((colindex(x) for x in coords),default=0),
                "individual_values_or_outcomes_read":False
            })
        if not result:
            raise ValueError("No source worksheets inside reported Excel")
        return result


def qpf001() -> dict:
    entry = {
        "id":"QPF001",
        "programme":"Oenothera_fruticosa_Smith_Swartz_Spigler_2021",
        "source_doi":FIRST_DOI,
        "source_url":"https://datadryad.org/dataset/doi%3A10.5061/dryad.hqbzkh1g9",
        "expected_data_files":["FIGO_2019_Data_20210523.xlsx"],
    }
    out = {
        "programme_id":"QPF001",
        "paper_doi":"10.1002/ajb2.1720",
        "source_doi":FIRST_DOI,
        "source_public_locator":PUBLIC_FIRST_URL,
        "published_design_fruits_recovered":93,
        "published_flowers_filmed":122,
        "source_value_read":False,
        "source_file_redistributed":False,
        "original_file_stream":"not_attempted",
    }
    try:
        metadata = metadata_for_one(entry)
        out["dryad_metadata_status"] = metadata.get("source_metadata_status")
        out["dryad_file_status"] = metadata.get("source_files_status")
        out["dryad_original_file_inventory"] = metadata.get("public_file_inventory",[])
        official = next((x for x in out["dryad_original_file_inventory"]
                         if x.get("name")=="FIGO_2019_Data_20210523.xlsx"),None)
        out["official_xlsx_inventory_match"] = bool(official)
    except Exception as exc:
        out["dryad_metadata_status"] = "SOURCE_METADATA_STOP"
        out["metadata_failure_type"] = type(exc).__name__
        official = None
    try:
        binary,finalurl=source_get(PUBLIC_FIRST_URL, MAX_FILE)
        out["original_file_stream"]="obtained_public_link"
        out["source_redirect_endpoint"]=finalurl.split("?")[0]
        out["source_bytes"]=len(binary)
        out["candidate_source_sha256"]=hashlib.sha256(binary).hexdigest()
        out["worksheet_schema"]=sheet_structure(binary)
        # If original file digest was advertised, corroborate the bytes.
        if official and official.get("digest") and official.get("digest_type")=="sha-256":
            out["matches_official_original_file_sha256"]=(
                official["digest"].casefold()==out["candidate_source_sha256"]
            )
            if not out["matches_official_original_file_sha256"]:
                raise ValueError("Original file SHA differs from official Dryad manifest")
        else:
            out["matches_official_original_file_sha256"]="not_available_in_metadata"
        out["decision"]="ORIGINAL_FILE_SCHEMA_RECOVERED_NO_BIOLOGICAL_OUTCOMES"
    except Exception as exc:
        out["original_file_stream"]="SOURCE_ACCESS_OR_FORMAT_STOP"
        out["stream_failure_type"]=type(exc).__name__
        out["stream_failure_detail"]=str(exc)[:190]
        out["decision"]="SOURCE_ACCESS_STOP_NO_QPF_OUTCOMES"
        out.pop("worksheet_schema",None)
    return out


def software_zenodo_record(record_id:int) -> dict:
    url=f"https://zenodo.org/api/records/{record_id}"
    out={"id":record_id,"public_api_url":url,
         "source_relationship":"Dryad QPF002 related work; presumed software unless original file inventory proves otherwise"}
    try:
        raw,_=source_get(url,MAX_JSON)
        doc=json.loads(raw)
        if not isinstance(doc,dict) or int(doc.get("id",-1))!=record_id:
            raise ValueError("Zenodo result ID mismatched pinned record")
        out["status"]="verified_metadata"
        out["doi"]=doc.get("doi")
        out["title"]=str((doc.get("metadata") or {}).get("title",doc.get("title","")))[:250]
        files=doc.get("files",[])
        out["files"]=[{
            "name":f.get("key") or f.get("filename"),
            "bytes":f.get("size"),
            "checksum":f.get("checksum"),
        } for f in files if isinstance(f,dict)]
        out["original_xlsx_present"]=any(
            str(x.get("name","")).casefold().endswith((".xlsx",".csv"))
            for x in out["files"]
        )
        out["file_bodies_downloaded"]=False
        out["original_biological_outcomes_read"]=False
    except Exception as exc:
        out["status"]="ZENODO_METADATA_ACCESS_STOP"
        out["failure_type"]=type(exc).__name__
        out["failure_detail"]=str(exc)[:190]
    return out


def audit() -> dict:
    one = qpf001()
    mirrors=[software_zenodo_record(x) for x in RELATED_ZENODO_SOFTWARE_IDS]
    return {
        "analysis_id":"qpf_original_public_source_recovery_v1",
        "scope":"source metadata/headers, no fitted Q-P-F association",
        "original_paper_programmes_count":2,
        "QPF001":one,
        "QPF002_zenodo_related_software":mirrors,
        "original_numeric_pollen_seed_or_visit_values_read":False,
        "third_party_raw_source_uploaded":False,
        "independent_new_QPF_empirical_tests_completed":0,
        "claim_limitations":[
            "Zenodo related software records are not independent original population samples.",
            "One Oenothera site has 122 filmed flowers but only 93 mature fruit outcomes; no outcome-missingness ignorability inferred.",
            "The published Smith et al. paper already demonstrated pollen composition x seed-set associations.",
            "Original new hypothesis/test is not executed without verified same-flower source IDs and pre-outcome fixed analysis."
        ]
    }


def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    info=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(info,indent=2,ensure_ascii=False)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "QPF001_file_status":info["QPF001"]["original_file_stream"],
        "QPF001_decision":info["QPF001"]["decision"],
        "QPF001_source_metadata":info["QPF001"].get("dryad_metadata_status"),
        "QPF001_original_file_inventory":info["QPF001"].get("dryad_original_file_inventory",[]),
        "QPF001_failure":info["QPF001"].get("stream_failure_detail"),
        "QPF001_file_schema":info["QPF001"].get("worksheet_schema",[]),
        "QPF002_zenodo": [{
            "id":x["id"],"status":x["status"],
            "title":x.get("title"),"failure":x.get("failure_detail"),
            "file_manifest":x.get("files",[])
        } for x in info["QPF002_zenodo_related_software"]],
        "no_new_effects":True,
    },indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
