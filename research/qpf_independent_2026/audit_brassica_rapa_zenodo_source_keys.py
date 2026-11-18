#!/usr/bin/env python3
"""QPF007 external 2026 original Brassica rapa source-only metadata/ID join.

Read trusted original Zenodo record 21628183 and five whitelisted text data
files, with exact original MD5/size checks; emit only source headers, counts,
checksums and anonymous session×plant key overlap counts. No biological
response values, seed/paternity, pollen, or raw individual IDs output.
This is NOT a new fitted ecological effect nor a natural-landscape replication.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import shlex
from urllib.parse import urlparse
from urllib.request import urlopen, Request

ID = 21628183
RECORD_DOI = "10.5281/zenodo.21628183"
ROOT_API = f"https://zenodo.org/api/records/{ID}"
ALLOWED_FILE_NAMES = (
    "README.txt",
    "data_ABPOLL_ID_resume.txt",
    "data_ABPOLL_flower_resume.txt",
    "data_ABPOLL_fix10_paternities.txt",
    "data_ABPOLL_ID_level_detID.txt",
)
LIMIT_BYTES = 7 * 1024 * 1024
MAX_ROWS = 500000
MAX_FILES_IN_RECORD = 150


def trusted_get(url: str, nbytes: int) -> bytes:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != "zenodo.org":
        raise ValueError("Only original Zenodo HTTPS endpoints allowed")
    if not (
        url == ROOT_API or
        url.startswith(ROOT_API + "/files/") or
        url.startswith(f"https://zenodo.org/records/{ID}/files/")
    ):
        raise ValueError("URL not original record metadata/file link")
    request = Request(url, headers={
        "User-Agent":"EGWEE-source-only-original-study-gate/2026-11-18",
        "Accept":"application/json, text/plain, application/octet-stream",
    })
    with urlopen(request, timeout=36) as response:
        payload = response.read(nbytes + 1)
    if len(payload) > nbytes:
        raise ValueError("Source original file exceeds whitelisted bounded size")
    return payload


def load_manifest() -> dict:
    response = json.loads(trusted_get(ROOT_API, 4 * 1024 * 1024))
    if int(response.get("id",-1)) != ID:
        raise ValueError("Wrong original Zenodo record ID")
    if str(response.get("doi","")).lower() != RECORD_DOI:
        raise ValueError("Wrong original Zenodo DOI")
    source = response.get("files")
    if not isinstance(source,list) or len(source)>MAX_FILES_IN_RECORD:
        raise ValueError("Original Zenodo file manifest missing or too large")
    names = [item.get("key") or item.get("filename") for item in source]
    if len(names)!=len(set(names)):
        raise ValueError("Duplicate original source filename")
    if not set(ALLOWED_FILE_NAMES).issubset(names):
        missing=sorted(set(ALLOWED_FILE_NAMES)-set(names))
        raise ValueError(
            "Original record missing whitelisted filenames "
            + repr(missing) + "; official publisher filename roster "
            + repr(sorted(names)[:25])
        )
    return response


def trusted_binary(original_file: dict) -> bytes:
    name = original_file.get("key") or original_file.get("filename")
    if name not in ALLOWED_FILE_NAMES:
        raise ValueError("Original source file not in prospectively bounded whitelist")
    declared = original_file.get("size")
    if not isinstance(declared,int) or declared<=0 or declared>LIMIT_BYTES:
        raise ValueError("Original declared source file size invalid")
    links = original_file.get("links",{})
    # Zenodo records API declares a canonical original file stream URL.
    url = links.get("self") or links.get("content")
    if not url:
        raise ValueError("Original Zenodo record has no advertised download link")
    payload = trusted_get(url, LIMIT_BYTES)
    if len(payload)!=declared:
        raise ValueError("Zenodo original source bytes differ from record manifest")
    digest = original_file.get("checksum","")
    if not digest.startswith("md5:"):
        raise ValueError("Zenodo original file must provide MD5 checksum")
    if hashlib.md5(payload).hexdigest()!=digest[4:]:
        raise ValueError("Original Zenodo file MD5 failed")
    return payload


def decode_table(payload: bytes) -> tuple[list[str], list[tuple[str,str]] | None,
                                           int, set[tuple[str,str]], set[str]]:
    # The first original data row must be a real named header. Safely parse
    # only biological keys, never record pollen, seed or trait numeric values.
    try:
        text = payload.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = payload.decode("latin-1")
    lines = text.splitlines()
    if not lines:
        raise ValueError("Original text dataset is empty")
    first = "\n".join(lines[:5])
    first_line = lines[0].strip()
    # Some author-exported R .txt files use write.table default:
    # quoted names/records separated by SPACE (not TSV/CSV punctuation).
    # This must be decoded without treating the entire biological header
    # as one opaque field or exposing any original signed response.
    whitespace_delimited = (
        not any(mark in first_line for mark in ("\t", ",", ";", "|"))
        and (" " in first_line)
    )
    if whitespace_delimited:
        reader = (shlex.split(line, posix=True) for line in lines)
    else:
        try:
            dialect = csv.Sniffer().sniff(first,delimiters=",;\t|")
            sep = dialect.delimiter
        except csv.Error:
            sep = "\t" if "\t" in lines[0] else ";" if ";" in lines[0] else ","
        reader = csv.reader(io.StringIO(text),delimiter=sep)
    headers = next(reader,None)
    if headers is None:
        raise ValueError("Original source missing header")
    headers = [x.strip().lstrip("\ufeff").strip('"') for x in headers]
    # Author files may include dozens/hundreds of derived analysis columns;
    # repeated non-key names are a disclosed schema ambiguity, not a reason
    # to alter which source plants are present. Key duplicates DO stop.
    if len(headers)==0 or len(headers)>3000:
        raise ValueError("Original source header width unsafe: "+str(len(headers)))
    duplicate_names={n for n,count in Counter(headers).items() if count>1}
    if any(x.casefold() in ("session","id_full","id_full_foc") for x in duplicate_names):
        raise ValueError("Ambiguous duplicated original biological ID header")
    if any(len(x)>120 for x in headers):
        raise ValueError("Unreasonable original single source header")
    # R write.table with row.names=TRUE may have a blank first header
    # followed by data rows one field wider; recognize and name that
    # harmless structural row number without guessing IDs or phenotypes.
    pending_row_index=False
    def findname(*names):
        lower={x.lower():x for x in headers}
        for n in names:
            if n.lower() in lower:return headers.index(lower[n.lower()])
        return None
    session_pos=findname("session")
    person_pos=findname("ID_full","id_full")
    # Partner flow files refer to focal plants via ID_full_foc
    if person_pos is None:
        person_pos=findname("ID_full_foc")
    keyset = set()
    sessions = set()
    n=0
    for cells in reader:
        if not cells or all(not s.strip() for s in cells):
            continue
        if len(cells)==len(headers)+1 and not pending_row_index:
            if not cells[0].strip().isdigit():
                raise ValueError("Source has an extra non-index column not present in header")
            headers=["__source_row_number"]+headers
            session_pos=session_pos+1 if session_pos is not None else None
            person_pos=person_pos+1 if person_pos is not None else None
            pending_row_index=True
        if len(cells)!=len(headers):
            raise ValueError(
                "Inconsistent original TSV/CSV field count: "
                + str(len(cells)) + " data cells vs " + str(len(headers)) + " header fields"
            )
        n+=1
        if n>MAX_ROWS:
            raise ValueError("Original source unexpectedly many records")
        if session_pos is not None:
            session=cells[session_pos].strip()
            if session and session.lower() not in ("na","nan"):
                sessions.add(session)
                if person_pos is not None:
                    plant=cells[person_pos].strip()
                    if plant and plant.lower() not in ("na","nan"):
                        keyset.add((session,plant))
    return headers,None,n,keyset,sessions


def schema_audit() -> dict:
    result={
        "analysis_id":"QPF007_Brassica_rapa_2026_same_plant_original_source_gate",
        "original_paper_doi":"10.1371/journal.pbio.3003579",
        "original_data_doi":RECORD_DOI,
        "zenodo_record_id":ID,
        "source_only":True,
        "raw_numeric_pollen_paternity_seed_or_visitor_values_read":False,
        "original_rows_and_IDs_exported":False,
        "new_ecological_effect_fitted":False,
        "independent_landscapes_claimed":False,
        "frozen_atlas_6_source_denominator_increment":0,
        "status":"SOURCE_ACCESS_STOP_NO_NEW_EFFECTS",
        "original_file_manifest":[],
        "source_schemas":[],
        "biological_ID_join_proven":False,
    }
    try:
        meta=load_manifest()
        result["metadata_verified"]=True
        result["title"]=str((meta.get("metadata") or {}).get("title",""))[:260]
        result["publication_date"]=str((meta.get("metadata") or {}).get("publication_date",""))
        manifest={}
        for item in meta["files"]:
            name=item.get("key") or item.get("filename")
            manifest[name]=item
            result["original_file_manifest"].append({
                "filename":name,"bytes":item.get("size"),
                "checksum":item.get("checksum"),
            })
        source_keys={}
        for name in ALLOWED_FILE_NAMES:
            item=manifest[name]
            try:
                source=trusted_binary(item)
                if name.endswith(".txt") and name=="README.txt":
                    result["source_schemas"].append({
                        "filename":name, "source_bytes":len(source),
                        "verified_sha256":hashlib.sha256(source).hexdigest(),
                        "schema_status":"readme_source_checksum_verified_no_contents_exported",
                    })
                    continue
                headers,_,n,keys,sessions=decode_table(source)
                source_keys[name]=keys
                result["source_schemas"].append({
                    "filename":name,"verified_source_bytes":len(source),
                    "verified_sha256":hashlib.sha256(source).hexdigest(),
                    "schema_status":"original_source_key_and_header_verified",
                    "source_columns":headers,
                    "original_physical_data_rows":n,
                    "unique_session_plant_keys":len(keys),
                    "unique_session_count":len(sessions),
                    "source_ids_not_printed":True,
                    "biological_response_values_not_used":True,
                })
            except Exception as e:
                result["source_schemas"].append({
                    "filename":name,
                    "schema_status":"file_access_or_format_stop",
                    "failure_type":type(e).__name__,
                    "failure_detail":str(e)[:175],
                    "no_raw_source_values_read":True,
                })
        a=source_keys.get("data_ABPOLL_ID_resume.txt")
        b=source_keys.get("data_ABPOLL_flower_resume.txt")
        c=source_keys.get("data_ABPOLL_ID_level_detID.txt")
        if a is not None and b is not None:
            overlap=a.intersection(b)
            result["exact_source_session_plant_key_grain"]={
                "individual_source_plant_keys":len(a),
                "stigma_flower_source_maternal_plant_keys":len(b),
                "observed_ID_level_stigma_overlap":len(overlap),
                "plant_P_coverage_of_individuals":len(overlap)/len(a) if a else None,
                "visit_graph_focal_overlap":len(a.intersection(c)) if c is not None else None,
                "join_grain":"(session, plantID), NOT the identical flower/stigma/seed",
                "individual_IDs_disclosed":False
            }
            result["biological_ID_join_proven"]=bool(overlap)
        if result["biological_ID_join_proven"]:
            result["status"]="ORIGINAL_SAME_PLANT_Q_P_F_STRUCTURAL_GATE_PASSED_NO_OUTCOME_FITTED"
        else:
            result["status"]="SOURCE_ACCESS_OR_EXACT_PLANT_ID_JOIN_STOP_NO_NEW_EFFECTS"
    except Exception as exc:
        result["metadata_verified"]=False
        result["metadata_error_type"]=type(exc).__name__
        result["metadata_error"]=str(exc)[:175]
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    info=schema_audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "result":info["status"],
        "metadata_verified":info.get("metadata_verified"),
        "metadata_access_error_type":info.get("metadata_error_type"),
        "metadata_access_error":info.get("metadata_error"),
        "file_sources":[{"file":x["filename"],"status":x["schema_status"],
                         "source_rows":x.get("original_physical_data_rows"),
                         "source_plant_keys":x.get("unique_session_plant_keys"),
                         "source_sessions":x.get("unique_session_count"),
                         "problem":x.get("failure_detail")}
                         for x in info["source_schemas"]],
        "matched_source_key_grain":info.get("exact_source_session_plant_key_grain"),
        "no_biological_response_fitted":True
    },indent=2))


if __name__=="__main__":
    main()
