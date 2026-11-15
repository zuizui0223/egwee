#!/usr/bin/env python3
"""Read published Dryad Pyrus programme metadata and raw workbook SHEET SCHEMA only.

Uses documented public Dryad REST GET endpoints.
No phenotypic value, treatment effect, genotype value or signed outcome is read.
Never uploads the workbook or Dryad's full ZIP.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
from io import BytesIO
import json
from pathlib import Path
import urllib.error
import urllib.request
import zipfile
from xml.etree import ElementTree as ET

DOI="doi:10.5061/dryad.6t72p3j"
ENCODED="doi%3A10.5061%2Fdryad.6t72p3j"
API="https://datadryad.org/api/v2/datasets/" + ENCODED
NS={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
MAX_BUNDLE=15*1024*1024

def public_get(url: str, limit: int=MAX_BUNDLE) -> bytes:
    req=urllib.request.Request(url, headers={"User-Agent":"EGWEE-published-source-schema-audit/0.1 (research)", "Accept":"application/json,application/zip"})
    with urllib.request.urlopen(req,timeout=35) as r:
        raw=r.read(limit+1)
        if len(raw)>limit:
            raise ValueError("Document exceeds source-audit size limit")
        return raw

def workbook_sheet_headers(workbook: bytes) -> list[dict]:
    sheets=[]
    with zipfile.ZipFile(BytesIO(workbook)) as z:
        assert z.testzip() is None
        ss=[]
        if "xl/sharedStrings.xml" in z.namelist():
            root=ET.fromstring(z.read("xl/sharedStrings.xml"))
            for v in root.findall("m:si",NS):
                ss.append("".join(t.text or "" for t in v.findall(".//m:t",NS)))
        for name in sorted(n for n in z.namelist() if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")):
            # Read only the leading row's cell TEXT and count row/column coordinates.
            root=ET.fromstring(z.read(name))
            rows=root.findall(".//m:sheetData/m:row",NS)
            header=[]
            for row in rows[:1]:
                for cell in row.findall("m:c",NS):
                    v=cell.find("m:v",NS)
                    if cell.attrib.get("t")=="s" and v is not None:
                        header.append(ss[int(v.text)])
                    elif cell.attrib.get("t")=="inlineStr":
                        header.append("".join(t.text or "" for t in cell.findall(".//m:t",NS)))
                    elif cell.attrib.get("t")=="str" and v is not None:
                        header.append(v.text or "")
                    else:
                        # Numeric first-row fields are not interpreted as phenotypes.
                        header.append("<nontext_first_row_cell>")
            sheets.append({
                "xml_sheet":name,
                "nonempty_xml_row_count":len(rows),
                "first_row_fields":header[:80],
                "first_row_field_count":len(header),
                "phenotype_values_examined":False
            })
    return sheets

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    result={
        "doi":DOI,"publication_doi":"10.1111/mec.15233",
        "source_page":"https://datadryad.org/dataset/doi%3A10.5061/dryad.6t72p3j",
        "published_files_from_landing_page":[
            "Pyrus bourgaeana genetic rescue_07_15_19.xlsx",
            "README_for_Pyrus bourgaeana genetic rescue_07_15_19.txt"
        ],
        "outcome_values_opened":False,
        "uncontrolled_effect_estimated":False,
        "data_redistributed":False,
        "metadata_status":"not_requested",
        "bundle_status":"not_requested",
        "schema_status":"pending",
    }
    try:
        dataset=json.loads(public_get(API,limit=3*1024*1024).decode("utf-8"))
        if DOI.lower() not in str(dataset.get("identifier","")).lower():
            raise ValueError("Dryad metadata identifier does not match pinned DOI")
        result["metadata_status"]="verified"
        result["title"]=dataset.get("title")
        result["dataset_publication_date"]=dataset.get("publicationDate")
    except Exception as e:
        result["metadata_status"]="access_stop"
        result["metadata_error"]=str(e)[:220]
    try:
        bundle=public_get(API+"/download",limit=MAX_BUNDLE)
        if not zipfile.is_zipfile(BytesIO(bundle)):
            raise ValueError("Dryad dataset export was not a ZIP archive")
        with zipfile.ZipFile(BytesIO(bundle)) as z:
            names=[n for n in z.namelist() if not n.endswith("/")]
            xlsx=[n for n in names if n.lower().endswith(".xlsx") and not n.startswith("__MACOSX")]
            result["downloaded_bundle_sha256"]=hashlib.sha256(bundle).hexdigest()
            result["bundle_status"]="verified"
            result["files"]=[{"name":n,"bytes":z.getinfo(n).file_size} for n in names]
            result["workbook_sheets"]=[]
            for name in xlsx[:3]:
                result["workbook_sheets"].append({
                    "source_file":name,
                    "sha256":hashlib.sha256(z.read(name)).hexdigest(),
                    "worksheets":workbook_sheet_headers(z.read(name))
                })
            result["schema_status"]="verified" if xlsx else "no_xlsx_in_bundle"
    except Exception as e:
        result["bundle_status"]="access_stop"
        result["bundle_error"]=str(e)[:220]
        result["schema_status"]="not_verified_access_stop"
    result["decision"]={
        "verified":"SHEET_SCHEMA_ONLY_REVIEW_TREATMENT_GRAIN_BEFORE_OUTCOME",
        "not_verified_access_stop":"ACCESS_STOP_NO_RAW_COHORT_LINKAGE_CLAIM",
        "no_xlsx_in_bundle":"DATA_FORMAT_STOP_REVIEW_FILE_METADATA"
    }[result["schema_status"]]
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "metadata_status":result["metadata_status"],
        "bundle_status":result["bundle_status"],
        "schema_status":result["schema_status"],
        "decision":result["decision"],
        "workbooks":len(result.get("workbook_sheets",[]))
    },ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
