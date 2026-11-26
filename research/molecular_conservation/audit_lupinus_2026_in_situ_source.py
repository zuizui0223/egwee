#!/usr/bin/env python3
"""Source-only Figshare gate for the 2026 in-situ Lupinus assisted-gene-flow study.
Only published file metadata, SHA256, XLSX first-row headers and physical row counts
are emitted. No phenotype/genotype values, individual IDs or model effects are emitted.
"""
from __future__ import annotations
from io import BytesIO
import hashlib
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import zipfile
from xml.etree import ElementTree as ET

ARTICLE = 29606180
EXPECTED_DOI = "10.6084/m9.figshare.29606180"
MAX_META = 2*1024*1024
MAX_FILE = 8*1024*1024
NS = {"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

def source_url(url: str, *, metadata: bool = False) -> str:
    u=urlparse(url)
    allowed={"api.figshare.com"} if metadata else {
        "api.figshare.com","figshare.com","ndownloader.figshare.com"}
    if u.scheme!="https" or u.hostname not in allowed or u.username or u.password:
        raise ValueError("Non-public/non-official Figshare source URL")
    if metadata and u.path != f"/v2/articles/{ARTICLE}":
        raise ValueError("Unregistered Figshare article metadata")
    return url

def get_bytes(url, lim):
    req=Request(source_url(url,metadata=("/v2/articles/" in url)),headers={
        "User-Agent":"EGWEE-Lupinus-2026-source-gate/1.0",
        "Accept":"application/json,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*",
    })
    with urlopen(req,timeout=45) as r:
        data=r.read(lim+1)
    if len(data)>lim:
        raise ValueError("File exceeds source-only audit cap")
    return data

def check_doi(value):
    doi=str(value or "").lower().removeprefix("https://doi.org/")
    return doi==EXPECTED_DOI or (doi.startswith(EXPECTED_DOI+".v") and
                                 doi[len(EXPECTED_DOI)+2:].isdigit())

def schema_of_xlsx(data):
    if not zipfile.is_zipfile(BytesIO(data)):
        raise ValueError("Invalid XLSX ZIP container")
    out=[]
    with zipfile.ZipFile(BytesIO(data)) as z:
        if z.testzip() is not None:
            raise ValueError("ZIP CRC mismatch")
        if sum(i.file_size for i in z.infolist())>70*MAX_FILE:
            raise ValueError("Unsafe uncompressed size")
        strings=[]
        if "xl/sharedStrings.xml" in z.namelist():
            r=ET.fromstring(z.read("xl/sharedStrings.xml"))
            strings=["".join(t.text or "" for t in si.findall(".//m:t",NS))
                     for si in r.findall("m:si",NS)]
        sheets=sorted((n for n in z.namelist()
                       if re.fullmatch(r"xl/worksheets/sheet\d+\.xml",n)),
                      key=lambda p:int(re.search(r"sheet(\d+)",p).group(1)))
        if len(sheets)>40:
            raise ValueError("Unexpected XLSX sheet count")
        for name in sheets:
            headers=[]; rows=0
            with z.open(name) as f:
                for event, elem in ET.iterparse(f,events=("end",)):
                    if elem.tag != "{"+NS["m"]+"}row":
                        continue
                    rows+=1
                    if rows==1:
                        for cell in elem.findall("m:c",NS)[:100]:
                            v=cell.find("m:v",NS)
                            typ=cell.get("t")
                            if typ=="s" and v is not None:
                                idx=int(v.text)
                                h=strings[idx] if 0<=idx<len(strings) else "<bad_shared_idx>"
                            elif typ=="inlineStr":
                                h="".join(t.text or "" for t in cell.findall(".//m:t",NS))
                            elif typ=="str" and v is not None:
                                h=v.text or ""
                            else:
                                h="<nontext_first_row>"
                            headers.append(str(h)[:90])
                    elem.clear()
            out.append({"worksheet":name,"physical_rows":rows,
                        "first_row_headers":headers,
                        "all_nonheader_values_read":False})
    return out

def main():
    receipt={"article_id":ARTICLE,"paper_doi":"10.1093/aob/mcag061",
             "status":"METADATA_PENDING","files":[],
             "raw_files_redistributed":False,"nonheader_outcome_values_read":False,
             "genotype_values_read":False,"source_individual_join_verified":False,
             "new_effect_estimated":False,"independent_biological_programmes_added":0}
    try:
        meta=json.loads(get_bytes(f"https://api.figshare.com/v2/articles/{ARTICLE}",MAX_META))
        if not check_doi(meta.get("doi")):
            raise ValueError("Article DOI does not match registered 2026 source")
        receipt["status"]="SOURCE_METADATA_VERIFIED"
        receipt["doi"]=meta["doi"]
        for f in meta.get("files",[]):
            item={"filename":str(f.get("name",""))[:160],
                  "file_id":f.get("id"),"declared_bytes":f.get("size"),
                  "is_link_only":f.get("is_link_only",False)}
            name=item["filename"].lower()
            if name.endswith(".xlsx") and 0< (item["declared_bytes"] or 0) <=MAX_FILE and f.get("download_url"):
                try:
                    raw=get_bytes(f["download_url"],MAX_FILE)
                    item["sha256"]=hashlib.sha256(raw).hexdigest()
                    item["sheets"]=schema_of_xlsx(raw)
                    item["schema_status"]="XLSX_FIRST_ROW_AND_COUNTS_ONLY"
                except (HTTPError,URLError,ValueError,KeyError,zipfile.BadZipFile) as e:
                    item["schema_status"]="DOWNLOAD_OR_SCHEMA_STOP"
                    item["error_type"]=type(e).__name__
                    if isinstance(e,HTTPError):
                        item["http_status"]=e.code
            else:
                item["schema_status"]="METADATA_ONLY_UNSUPPORTED_OR_SIZE_LIMIT"
            receipt["files"].append(item)
        receipt["decision"]="SOURCE_ONLY_SCHEMAS_REQUIRE_COHORT_AND_SAMPLE_KEY_AUDIT"
    except (HTTPError,URLError,ValueError,KeyError,TypeError,json.JSONDecodeError) as e:
        receipt["status"]="SOURCE_METADATA_STOP"
        receipt["error_type"]=type(e).__name__
        if isinstance(e,HTTPError): receipt["http_status"]=e.code
        receipt["decision"]="SOURCE_ACCESS_STOP"
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
