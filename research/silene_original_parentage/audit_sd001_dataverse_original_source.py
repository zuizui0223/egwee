#!/usr/bin/env python3
"""Dataverse original source-only Silene 2026 mother/sire vs pollen assay receipt.

Only Dataverse publisher metadata, SHA/digest, original filename, file size,
field label first line, physical row count are emitted. Genotypes, stigma
pollen numbers, mother/sire/offspring IDs and source outcomes are NOT parsed.
Two assays on different flowers NEVER joined by positions or matching labels.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from io import StringIO
import json
from pathlib import Path
from urllib.parse import quote,urljoin,urlparse
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
import re

BASE="https://entrepot.recherche.data.gouv.fr"
DOI="doi:10.57745/CF1VNW"
META_MAX=3_000_000
SOURCE_MAX=300_000
FILE_EXPECTED={
    "paternity_assignment_results.tab":1150,
    "pollen_counts_on_stigmas.tab":186,
}
LABEL_RE=re.compile(r"^[A-Za-z][A-Za-z0-9_ /()%:,.+#?-]{0,95}$")

def approved_url(url):
    if not url or not isinstance(url,str):raise ValueError("No publisher source URL")
    full=urljoin(BASE,url)
    p=urlparse(full)
    if p.scheme!="https" or p.hostname!="entrepot.recherche.data.gouv.fr":
        raise ValueError("Third-party or non-HTTPS source forbidden")
    if not p.path.startswith("/api/"):
        raise ValueError("Publisher Dataverse only API path required")
    return full

def official_bytes(url,max_n):
    target=approved_url(url)
    req=Request(target,headers={
        "User-Agent":"egwee-source-only-Silene-2026/1.0",
        "Accept":"application/json,text/tab-separated-values,application/octet-stream,*/*"})
    with urlopen(req,timeout=40) as resp:
        if urlparse(resp.geturl()).hostname!="entrepot.recherche.data.gouv.fr":
            raise ValueError("Publisher redirected source to unverified domain: "+str(urlparse(resp.geturl()).hostname))
        raw=resp.read(max_n+1)
        if len(raw)>max_n:raise ValueError("Publisher file size over bounded source audit")
        content_type=resp.headers.get("Content-Type","")
    return raw,content_type

def one_file(item,name):
    file=item["dataFile"]
    id_=file.get("id")
    if not isinstance(id_,int) or id_<=0:
        raise ValueError("No original Dataverse integer file ID")
    out={
       "original_published_file_name":name,
       "original_dataverse_file_id":id_,
       "publisher_declared_bytes":file.get("filesize"),
       "publisher_data_file_content_type":file.get("contentType"),
       "publisher_declared_md5":file.get("md5"),
       "publisher_original_file_name":file.get("originalFileName"),
       "publisher_original_file_bytes":file.get("originalFileSize"),
       "publisher_original_file_format":file.get("originalFileFormat"),
       "publisher_checksum":file.get("checksum"),
       "original_dataset_rows_expected":FILE_EXPECTED[name],
       "source_numeric_outcomes_not_examined":True,
       "source_original_ID_or_genotype_rows_redistributed":False,
       "status":"SOURCE_FILE_NOT_YET_RETRIEVED",
    }
    try:
        raw,typ=official_bytes(BASE+"/api/access/datafile/"+str(id_)+"?format=original",SOURCE_MAX)
        if out["publisher_declared_bytes"] is not None and len(raw)!=out["publisher_declared_bytes"]:
            raise ValueError("Dataverse original published file size does not match")
        expected_md5=out["publisher_declared_md5"]
        if expected_md5 and hashlib.md5(raw).hexdigest().lower()!=str(expected_md5).lower():
            raise ValueError("Original source MD5 does not match publisher file checksum")
        # Original source is text tabular, not an automatic recreation of
        # genotype/paternity semantics.
        try:txt=raw.decode("utf-8-sig","strict")
        except UnicodeDecodeError:txt=raw.decode("latin-1","strict")
        lines=[x for x in txt.splitlines() if x.strip()]
        if len(lines)<2:raise ValueError("Original source tabular file lacks data rows")
        first=lines[0]
        delim="\t" if first.count("\t")>=max(first.count(","),first.count(";")) else (
               "," if first.count(",")>=first.count(";") else ";")
        headers=next(csv.reader([first],delimiter=delim))
        plausible=len(headers)>=2 and len(headers)<=40 and all(
            LABEL_RE.fullmatch(x.strip()) for x in headers)
        if not plausible:raise ValueError("No source-safe first-row column header")
        if len(lines)!=FILE_EXPECTED[name]+1:
            raise ValueError("Original source expected physical row count mismatch")
        out.update({
            "actual_source_sha256":hashlib.sha256(raw).hexdigest(),
            "actual_source_bytes":len(raw),
            "actual_download_content_type":typ,
            "first_line_field_count":len(headers),
            "original_field_labels":[x.strip() for x in headers],
            "verified_nonempty_original_data_rows":len(lines)-1,
            "metadata_source_parent_child_names_only": {
               kind:any(kind in x.lower() for x in headers) for kind in (
                   "mother","maternal","father","paternal","sire",
                   "offspring","seed","flower","visit","pollen",
                   "sequence","position","order","bout","plant","trial","replicate")
            },
            "original_source_MD5_pass":bool(expected_md5),
            "status":"PUBLISHED_SOURCE_ORIGINAL_HEADER_AND_LINE_COUNT_VERIFIED",
        })
    except (HTTPError,URLError,ValueError,KeyError,TypeError,UnicodeError) as ex:
        out["status"]="ORIGINAL_SOURCE_ACCESS_OR_SEMANTICS_STOP"
        out["source_stop_type"]=type(ex).__name__
        if isinstance(ex,HTTPError):out["source_stop_http"]=ex.code
        else:out["source_stop_bounded_reason"]=str(ex)[:190]
    return out

def audit():
    result={
       "source_programme":"SD001_2026_Silene_dioica",
       "source_original_repository":"Recherche Data Gouv Dataverse",
       "source_doi":DOI,
       "author_preprint_doi":"10.1101/2025.07.19.665651",
       "source_official_persistent_id":"10.57745/CF1VNW",
       "source_expected_file_count":2,
       "original_source_rows_or_genotypes_redistributed":False,
       "one_original_experimental_study_not_1150_replicate_programmes":True,
       "same_flower_Q_P_F_joins_verified":False,
       "assigned_father_linked_to_sequential_stigma_visit_verified":False,
       "biological_effect_estimated":False,
       "status":"SOURCE_METADATA_NOT_ACCESSED",
    }
    api=BASE+"/api/datasets/:persistentId/?persistentId="+quote(DOI,safe="")
    try:
        raw,_=official_bytes(api,META_MAX)
        doc=json.loads(raw)
        if str(doc.get("status","")).upper()!="OK":
            raise ValueError("Official Dataverse API status not OK")
        data=doc.get("data") or {}
        version=data.get("latestVersion") or {}
        supplied=str(version.get("datasetPersistentId") or data.get("persistentId") or "")
        if supplied.casefold()!=DOI.casefold():
            raise ValueError("Published Dataverse source DOI does not match")
        items=version.get("files")
        if not isinstance(items,list):raise ValueError("No original Dataverse public file metadata")
        names={str(x.get("label","")):x for x in items}
        result.update({
            "original_repository_API_metadata_verified":True,
            "publisher_dataset_id":data.get("id"),
            "publisher_current_version":version.get("versionNumber"),
            "publisher_version_minor":version.get("versionMinorNumber"),
            "publisher_version_state":version.get("versionState"),
            "original_record_file_metadata_count":len(items),
            "original_expected_files_present":{k:k in names for k in FILE_EXPECTED},
        })
        if any(k not in names for k in FILE_EXPECTED):
            raise ValueError("One or both official source file name labels are absent")
        result["status"]="SOURCE_OFFICIAL_METADATA_VERIFIED"
    except (HTTPError,URLError,ValueError,KeyError,TypeError,json.JSONDecodeError) as ex:
        result["status"]="SOURCE_METADATA_OR_OFFICIAL_ID_STOP"
        result["source_stop_type"]=type(ex).__name__
        if isinstance(ex,HTTPError):result["source_stop_http"]=ex.code
        else:result["source_stop_bounded_reason"]=str(ex)[:200]
        return result
    result["source_files"]=[one_file(names[k],k) for k in FILE_EXPECTED]
    if all(x["status"]=="PUBLISHED_SOURCE_ORIGINAL_HEADER_AND_LINE_COUNT_VERIFIED"
           for x in result["source_files"]):
        result["status"]="TWO_ORIGINAL_SOURCE_SCHEMAS_VERIFIED_NO_BIOLOGICAL_JOIN"
        result["decision"]="FREEZE_DISTINCT_POLLEN_AND_PATERNITY_STAGE_ESTIMANDS_SEPARATELY"
    else:
        result["status"]="PUBLIC_ORIGINAL_SOURCE_ACCESS_OR_SCHEMA_STOP"
        result["decision"]="DO_NOT_INFER_DIRECT_MOTHER_FATHER_VISIT_CAUSATION"
    return result

def self_test():
    assert approved_url(BASE+"/api/datasets/1")=="https://entrepot.recherche.data.gouv.fr/api/datasets/1"
    assert approved_url("/api/access/datafile/100?format=original").startswith(BASE+"/api/access")
    try:approved_url("https://example.net/api/data")
    except ValueError:pass
    else:raise AssertionError("External file URL not rejected")
    assert FILE_EXPECTED["paternity_assignment_results.tab"]==1150
    assert FILE_EXPECTED["pollen_counts_on_stigmas.tab"]==186
    print("SD001_DATAVERSE_SOURCE_AND_TWO_ASSAYS_SYNTHETIC_PASS")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:self_test();return 0
    if a.output is None:p.error("--output required")
    result=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    brief={"status":result["status"],"stop_type":result.get("source_stop_type"),
           "stop_http":result.get("source_stop_http"),
           "stop_reason":result.get("source_stop_bounded_reason"),
           "metadata_files":result.get("original_record_file_metadata_count"),
           "sources":[{
              "name":x["original_published_file_name"],"status":x["status"],
              "rows":x.get("verified_nonempty_original_data_rows"),
              "fields":x.get("original_field_labels"),
              "md5_pass":x.get("original_source_MD5_pass"),
              "publisher_original_name":x.get("publisher_original_file_name"),
              "publisher_original_bytes":x.get("publisher_original_file_bytes"),
              "publisher_original_format":x.get("publisher_original_file_format"),
              "publisher_bytes":x.get("publisher_declared_bytes"),
              "publisher_md5":x.get("publisher_declared_md5"),
              "publisher_checksum":x.get("publisher_checksum"),
              "stop_type":x.get("source_stop_type"),
              "stop_http":x.get("source_stop_http"),
              "stop_reason":x.get("source_stop_bounded_reason")
           } for x in result.get("source_files",[])],
           "effect_estimated":False}
    print("SD001_ORIGINAL_DATAVERSE_SOURCE_AUDIT "+json.dumps(brief,sort_keys=True,ensure_ascii=False),flush=True)
    return 0

if __name__=="__main__":raise SystemExit(main())

