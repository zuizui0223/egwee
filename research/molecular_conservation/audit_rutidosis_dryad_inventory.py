#!/usr/bin/env python3
"""Metadata-only audit for the published Rutidosis Dryad source, no biological values."""
import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen

DOI = "10.5061/dryad.1qp8v"
BASE = "https://datadryad.org"

def safe(href):
    url=urljoin(BASE,href)
    p=urlparse(url)
    if p.scheme!="https" or p.hostname!="datadryad.org" or not p.path.startswith("/api/v2/"):
        raise ValueError("non-official API URL")
    return url

def get(href):
    with urlopen(Request(safe(href),headers={"Accept":"application/json","User-Agent":"EGWEE-Rutidosis-source-gate/1.0"}),timeout=30) as r:
        return json.load(r)

def href(doc,rel):
    x=(doc.get("_links") or {}).get(rel) or {}
    return x.get("href")

def main():
    result={"doi":DOI,"status":"pending","no_original_data_downloaded":True,"no_effect_estimated":True}
    try:
        d=get(BASE+"/api/v2/datasets/"+quote("doi:"+DOI,safe=""))
        if str(d.get("identifier","")).casefold()!="doi:"+DOI:
            raise ValueError("DOI mismatch")
        v=href(d,"stash:version")
        if not v:
            raise ValueError("No version link; no guessing")
        version=get(v)
        files_link=href(version,"stash:files")
        if not files_link:
            raise ValueError("No files link")
        files=(get(files_link).get("_embedded") or {}).get("stash:files") or []
        result.update({"status":"OFFICIAL_FILE_INVENTORY_VERIFIED",
                       "file_count":len(files),
                       "files":[{"filename":str(f.get("path","")).split("/")[-1][:150],
                                 "declared_bytes":f.get("size"),
                                 "has_official_download_link":bool(href(f,"stash:download"))}
                                for f in files[:100]]})
    except HTTPError as e:
        result.update({"status":"SOURCE_ACCESS_STOP","http_status":e.code})
    except (URLError,ValueError,KeyError,TypeError) as e:
        result.update({"status":"SOURCE_ACCESS_STOP","reason_type":type(e).__name__})
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
