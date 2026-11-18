#!/usr/bin/env python3
"""Corrected, source-commit-pinned EuPPollNet headers/row counts ONLY.

No pollinator guild / plant identity / interaction values accessed in stage A.
"""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import sys

OWNER="joseblanuza"
REPO="EuPPollNet"
COMMIT="31716d21d5aad8c27c1d91dd0620149ef42e8836"
FILES={
    "Interaction_data.csv.gz": "Data/3_Final_data/Interaction_data.csv.gz",
    "Flower_counts.csv": "Data/3_Final_data/Flower_counts.csv",
    "Metadata.csv": "Data/3_Final_data/Metadata.csv",
}
MAX_DOWNLOAD=40*1024*1024
MAX_EXPANDED=256*1024*1024


def download_original(path):
    url=f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{COMMIT}/{path}"
    req=urllib.request.Request(url,headers={"User-Agent":"EGWEE-EuPPollNet-source-schema/1.0"})
    chunks=[]
    n=0
    with urllib.request.urlopen(req,timeout=120) as response:
        while True:
            block=response.read(1024*1024)
            if not block:
                break
            n+=len(block)
            if n>MAX_DOWNLOAD:
                raise ValueError("SOURCE_STOP: original file exceeds download ceiling")
            chunks.append(block)
    if n==0:
        raise ValueError("SOURCE_STOP: empty original file")
    return b"".join(chunks)


def schema_of(data, compressed=False):
    if compressed:
        data=gzip.decompress(data)
    if len(data)>MAX_EXPANDED:
        raise ValueError("SOURCE_STOP: exceeds uncompressed byte ceiling")
    text=io.TextIOWrapper(io.BytesIO(data),encoding="utf-8-sig",errors="strict",newline="")
    try:
        reader=csv.reader(text)
        head=next(reader,None)
        if not head or len(head)!=len(set(head)) or any(not k.strip() for k in head):
            raise ValueError("SCHEMA_STOP: invalid/duplicate source column names")
        n=0
        for row in reader:
            if len(row)!=len(head):
                raise ValueError("SCHEMA_STOP: ragged CSV source record")
            n+=1
        if n==0:
            raise ValueError("SCHEMA_STOP: original table empty")
        return {"columns":head,"header_column_count":len(head),
                "rows_excluding_header":n,"uncompressed_bytes":len(data),
                "ecological_values_interpreted":False}
    finally:
        text.close()


def audit():
    files={}
    for name,path in FILES.items():
        b=download_original(path)
        files[name]={
            "path":path,"source_commit_sha":COMMIT,
            "bytes_downloaded":len(b),"sha256_original_bytes":hashlib.sha256(b).hexdigest(),
            **schema_of(b,name.endswith(".gz")),
        }
    # Interaction table expected from corrected source paper. Mismatches STOP.
    if files["Interaction_data.csv.gz"]["rows_excluding_header"] != 623476:
        raise ValueError("SOURCE_STOP: corrected interaction count does not match 623476")
    return {
        "status":"SOURCE_SCHEMA_PASS","source":f"{OWNER}/{REPO}",
        "source_commit_sha":COMMIT,
        "correction_doi":"10.1111/geb.70054",
        "files":files,
        "original_rows_redistributed":False,"signed_guild_outcomes_opened":False,
    }


def test():
    data=b"A,B,C\n1,2,3\n4,5,6\n"
    if schema_of(gzip.compress(data),True)["rows_excluding_header"]!=2:
        raise AssertionError("gzip/CSV self test failed")
    try:
        schema_of(b"A,A\n1,2\n")
    except ValueError:
        pass
    else:
        raise AssertionError("duplicate-column input admitted")
    print("EUPPOLLNET_SCHEMA_SYNTHETIC_PASS")


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    if args.self_test:
        test()
        return 0
    if args.output is None:
        p.error("--output required")
    result={
        "phase":"source-schema-outcome-blind","source_commit_sha":COMMIT,
        "protocol":"research/euppollnet_guild_partition/PROTOCOL_20261118.md",
        "signed_guild_outcomes_opened":False,
    }
    try:
        result.update(audit())
    except Exception as exc:
        result["status"]="SOURCE_SCHEMA_STOP"
        result["reason"]=type(exc).__name__+": "+str(exc)[:400]
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("EUPPOLLNET_SOURCE_SCHEMA "+json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["status"]=="SOURCE_SCHEMA_PASS" else 1


if __name__=="__main__":
    sys.exit(main())
