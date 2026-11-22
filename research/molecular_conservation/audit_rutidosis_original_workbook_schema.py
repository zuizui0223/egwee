#!/usr/bin/env python3
"""Bounded original Dryad Rutidosis XLSX retrieval and source-only schema gate.

Only follows links advertised by official Dryad REST metadata.
Never prints or uploads source bytes, genotype calls, individual IDs or outcomes.
Stop on HTTP 401/403/429 rather than trying alternative credentials/endpoints.
"""
from __future__ import annotations

import hashlib
from io import BytesIO
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen
import zipfile
from xml.etree import ElementTree as ET

DOI = "10.5061/dryad.1qp8v"
BASE = "https://datadryad.org"
LIMIT = 2 * 1024 * 1024
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

def api_url(href: str) -> str:
    url = urljoin(BASE, href)
    p = urlparse(url)
    if p.scheme != "https" or p.hostname != "datadryad.org" or not p.path.startswith("/api/v2/"):
        raise ValueError("Not an official Dryad API endpoint")
    return url

def get_bytes(href: str, limit: int = LIMIT) -> bytes:
    req = Request(api_url(href), headers={
        "User-Agent": "EGWEE-Rutidosis-original-source-gate/1.0",
        "Accept": "application/json,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    })
    with urlopen(req, timeout=30) as response:
        data = response.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Oversize source")
    return data

def get_json(href: str) -> dict:
    doc = json.loads(get_bytes(href))
    if not isinstance(doc, dict):
        raise ValueError("Invalid JSON metadata")
    return doc

def source_link(doc: dict, key: str) -> str | None:
    obj = (doc.get("_links") or {}).get(key) or {}
    return obj.get("href") if isinstance(obj, dict) else None

def schema_only(raw: bytes) -> list[dict]:
    if not zipfile.is_zipfile(BytesIO(raw)):
        raise ValueError("Non-XLSX source")
    out = []
    with zipfile.ZipFile(BytesIO(raw)) as z:
        if z.testzip() is not None:
            raise ValueError("XLSX CRC error")
        # Extract no biological outcome values. Large uncompressed XML is rejected.
        if sum(info.file_size for info in z.infolist()) > 25 * LIMIT:
            raise ValueError("Excessive uncompressed source size")
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.findall(".//m:t", NS))
                      for si in root.findall("m:si", NS)]
        sheets = sorted(
            [n for n in z.namelist()
             if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)],
            key=lambda n: int(re.search(r"sheet(\d+)", n).group(1)))
        if len(sheets) > 30 or not sheets:
            raise ValueError("Unexpected sheet count")
        for name in sheets:
            rows = 0
            headers = []
            with z.open(name) as f:
                for _event, item in ET.iterparse(f, events=("end",)):
                    if item.tag != "{%s}row" % NS["m"]:
                        continue
                    rows += 1
                    if rows == 1:
                        for cell in item.findall("m:c", NS)[:100]:
                            value = cell.find("m:v", NS)
                            kind = cell.get("t")
                            if kind == "s" and value is not None:
                                index = int(value.text)
                                header = shared[index] if 0 <= index < len(shared) else "<invalid_shared_index>"
                            elif kind == "inlineStr":
                                header = "".join(x.text or "" for x in cell.findall(".//m:t", NS))
                            elif kind == "str" and value is not None:
                                header = value.text or ""
                            else:
                                header = "<nontext_header>"
                            headers.append(str(header)[:72])
                    item.clear()
            out.append({"sheet_xml":name,"physical_rows":rows,
                        "first_row_header_cells":headers,
                        "individual_data_values_exported":False})
    return out

def run() -> dict:
    result = {
        "doi": DOI, "status": "pending",
        "original_file_redistributed": False,
        "individual_data_values_exported": False,
        "effect_estimated": False, "source_join_verified": False
    }
    try:
        meta = get_json(BASE + "/api/v2/datasets/" + quote("doi:" + DOI, safe=""))
        if str(meta.get("identifier", "")).casefold() != "doi:" + DOI:
            raise ValueError("Dataset DOI mismatch")
        v = source_link(meta, "stash:version")
        if not v:
            raise ValueError("No source version")
        ver = get_json(v)
        file_url = source_link(ver, "stash:files")
        if not file_url:
            raise ValueError("No source file index")
        files = (get_json(file_url).get("_embedded") or {}).get("stash:files") or []
        if len(files) != 1:
            result.update(status="SOURCE_FILE_NUMBER_MISMATCH",declared_count=len(files))
            return result
        f = files[0]
        name = str(f.get("path","")).split("/")[-1]
        if not name.lower().endswith(".xlsx"):
            result.update(status="SOURCE_NOT_XLSX",filename=name)
            return result
        result.update(filename=name, bytes_declared=f.get("size"))
        link = source_link(f,"stash:download")
        if not link:
            result["status"]="SOURCE_NO_ADVERTISED_DOWNLOAD"
            return result
        raw = get_bytes(link)
        if isinstance(f.get("size"),int) and len(raw)!=f["size"]:
            raise ValueError("Source declared byte size mismatch")
        result.update(status="SOURCE_SCHEMA_VERIFIED_FIRST_ROW_ONLY",
                      bytes_read=len(raw),
                      source_sha256=hashlib.sha256(raw).hexdigest(),
                      worksheet_structure=schema_only(raw))
    except HTTPError as e:
        result.update(status="SOURCE_DOWNLOAD_OR_METADATA_HTTP_STOP", http_status=e.code)
    except (URLError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as e:
        result.update(status="SOURCE_ACCESS_OR_SCHEMA_STOP", error_type=type(e).__name__)
    return result

def main():
    print(json.dumps(run(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
