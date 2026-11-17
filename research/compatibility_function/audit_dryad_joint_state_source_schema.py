#!/usr/bin/env python3
"""Receipt for primary original natural mating/seed datasets, schema only.

Never print raw phenotypes, genotype values, plant IDs, sperm/pollen values or
individual data. No bearer credentials, alternative scraping or bypass on 401.
"""
from __future__ import annotations

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen
import zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "research/compatibility_function/primary_programmes_source_gate_v1.json"
BASE = "https://datadryad.org"
MAX_META = 3 * 1024 * 1024
MAX_FILE = 2 * 1024 * 1024
MAX_BUNDLE = 7 * 1024 * 1024
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def safe_url(href: str) -> str:
    if not isinstance(href, str) or not href:
        raise ValueError("Missing API link")
    url = urljoin(BASE, href)
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "datadryad.org":
        raise ValueError("Unapproved Dryad download location")
    if not parsed.path.startswith("/api/v2/"):
        raise ValueError("Unexpected Dryad link route")
    return url


def request_bytes(url: str, limit: int = MAX_META) -> bytes:
    req = Request(safe_url(url), headers={
        "User-Agent": "EGWEE-source-schema-audit/1.0 (open scholarship; no authentication)",
        "Accept": "application/json,application/zip,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    })
    with urlopen(req, timeout=35) as response:
        body = response.read(limit + 1)
    if len(body) > limit:
        raise ValueError("Response larger than audited limit")
    return body


def request_json(url: str) -> dict:
    raw = request_bytes(url, MAX_META)
    doc = json.loads(raw)
    if not isinstance(doc, dict):
        raise ValueError("Dryad endpoint did not return a JSON object")
    return doc


def validate_metadata(payload: dict, doi: str) -> None:
    expected = "doi:" + doi.casefold()
    actual = str(payload.get("identifier", "")).casefold()
    if actual != expected:
        raise ValueError(f"Wrong dataset identifier: {actual!r}")


def link(doc: dict, rel: str) -> str | None:
    obj = (doc.get("_links") or {}).get(rel) or {}
    return obj.get("href") if isinstance(obj, dict) else None


def version_file_metadata(dataset: dict, dataset_api: str) -> list[dict]:
    version_link = link(dataset, "stash:version")
    if not version_link:
        # No guessed version IDs: use the documented versions collection.
        vlist = request_json(dataset_api + "/versions")
        versions = (vlist.get("_embedded") or {}).get("stash:versions") or []
        if not versions:
            raise ValueError("No version pointer or version metadata")
        version_link = link(versions[-1], "self")
        if not version_link:
            raise ValueError("Cannot follow latest version without a verified link")
    version = request_json(version_link)
    file_link = link(version, "stash:files")
    if not file_link:
        raise ValueError("Version has no source-backed file list")
    files_doc = request_json(file_link)
    files = (files_doc.get("_embedded") or {}).get("stash:files")
    if not isinstance(files, list):
        raise ValueError("Source API file list absent")
    return files


def workbook_schema(raw: bytes) -> list[dict]:
    if not zipfile.is_zipfile(BytesIO(raw)):
        raise ValueError("File is not a valid .xlsx ZIP")
    out = []
    with zipfile.ZipFile(BytesIO(raw)) as z:
        if z.testzip() is not None:
            raise ValueError("Invalid source XLSX CRC")
        sheet_xmls = sorted(
            (n for n in z.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n)),
            key=lambda n: int(re.search(r"sheet(\d+)", n).group(1)),
        )
        if not sheet_xmls:
            raise ValueError("No XLSX worksheets")
        if len(sheet_xmls) > 30:
            raise ValueError("Unexpected number of XLSX sheets")
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.findall(".//m:t", NS))
                      for si in root.findall("m:si", NS)]
        for name in sheet_xmls:
            # Spreadsheet schema only: do not read any column values after
            # the first physical row or any genetic/trait/seed numerical cells.
            root = ET.fromstring(z.read(name))
            rows = root.findall(".//m:sheetData/m:row", NS)
            headings = []
            if rows:
                for cell in rows[0].findall("m:c", NS):
                    val = cell.find("m:v", NS)
                    typ = cell.get("t")
                    if typ == "s" and val is not None:
                        idx = int(val.text)
                        headings.append(shared[idx] if 0 <= idx < len(shared) else "<invalid_shared_text>")
                    elif typ == "inlineStr":
                        headings.append("".join(t.text or "" for t in cell.findall(".//m:t", NS)))
                    elif typ == "str" and val is not None:
                        headings.append(val.text or "")
                    else:
                        headings.append("<nontext_header>")
            # Header strings could include individual IDs if first row is
            # not really a header. Retain strictly bounded schema labels only.
            if len(headings) > 100:
                raise ValueError("Unexpected wide source workbook")
            out.append({
                "worksheet_xml": name,
                "physical_rows_including_header": len(rows),
                "first_row_field_count": len(headings),
                "header_cells": [str(s)[:70] for s in headings[:100]],
                "data_rows_or_outcome_values_read": False,
            })
    return out


def metadata_for_one(entry: dict) -> dict:
    doi = entry["source_doi"]
    api = BASE + "/api/v2/datasets/" + quote("doi:" + doi, safe="")
    result = {
        "programme_id": entry["id"], "source_doi": doi,
        "programme_cluster": entry["programme"], "url": entry["source_url"],
        "source_metadata_status": "pending",
        "source_files_status": "pending",
        "source_workbook_schemas": [],
        "expected_file_names": entry["expected_data_files"],
        "source_data_redistributed": False,
        "phenotype_values_examined": False,
        "molecular_genotypes_examined": False,
        "exact_biological_ID_join_verified": False,
    }
    try:
        metadata = request_json(api)
        validate_metadata(metadata, doi)
        result["source_metadata_status"] = "verified"
        result["source_title"] = str(metadata.get("title", ""))[:260]
        result["publication_date"] = metadata.get("publicationDate")
    except (HTTPError, URLError, ValueError, KeyError, json.JSONDecodeError) as exc:
        result["source_metadata_status"] = "access_or_identifier_stop"
        result["source_metadata_reason"] = type(exc).__name__ + ": " + str(exc)[:170]
        result["source_files_status"] = "not_checked_metadata_stop"
        result["decision"] = "SOURCE_ACCESS_STOP_NO_RAW_LINKAGE_INFERENCE"
        return result

    try:
        files = version_file_metadata(metadata, api)
        result["source_files_status"] = "verified_metadata"
        declared = []
        for item in files:
            name = str(item.get("path", "")).split("/")[-1]
            if not name:
                raise ValueError("File without path in source metadata")
            declared.append({"name": name, "bytes_declared": item.get("size"),
                             "digest": item.get("digest"), "digest_type": item.get("digestType")})
        result["public_file_inventory"] = declared
        expected = {x.casefold() for x in entry["expected_data_files"]}
        observed = {x["name"].casefold() for x in declared}
        result["missing_expected_filenames"] = sorted(expected - observed)
        selected = [f for f in files if str(f.get("path", "")).split("/")[-1].casefold() in expected]
        if not selected:
            result["decision"] = "SOURCE_SCHEMA_STOP_NO_EXPECTED_FILE_MATCH"
            return result
        for f in selected:
            name = str(f["path"]).split("/")[-1]
            size = f.get("size")
            r = {"source_file": name, "bytes_declared": size, "schema_status": "pending"}
            if not isinstance(size, int) or not 0 < size <= MAX_FILE:
                r["schema_status"] = "skipped_declared_size"
            else:
                href = link(f, "stash:download")
                if not href:
                    r["schema_status"] = "no_verified_download_link"
                else:
                    try:
                        raw = request_bytes(href, limit=MAX_FILE)
                        r["source_sha256"] = hashlib.sha256(raw).hexdigest()
                        r["worksheets"] = workbook_schema(raw)
                        r["schema_status"] = "verified_first_row_schema_only"
                    except (HTTPError, URLError, ValueError, KeyError, zipfile.BadZipFile) as exc:
                        r["schema_status"] = "public_download_access_stop"
                        r["reason"] = type(exc).__name__ + ": " + str(exc)[:150]
            result["source_workbook_schemas"].append(r)
        if any(x["schema_status"] == "verified_first_row_schema_only" for x in result["source_workbook_schemas"]):
            result["decision"] = "SCHEMA_AVAILABLE_JOIN_GRAIN_NOT_YET_VERIFIED"
        else:
            result["decision"] = "PUBLIC_DOWNLOAD_STOP_METADATA_ONLY"
    except (HTTPError, URLError, ValueError, KeyError, json.JSONDecodeError) as exc:
        result["source_files_status"] = "metadata_access_stop"
        result["source_files_reason"] = type(exc).__name__ + ": " + str(exc)[:170]
        result["decision"] = "SOURCE_ACCESS_STOP_NO_RAW_LINKAGE_INFERENCE"
    return result


def audit(registry: dict) -> dict:
    entries = registry.get("programmes") or []
    assert registry["schema_version"] == 1
    assert [x["id"] for x in entries] == ["SMF001", "SMF002", "SMF003", "SMF004"]
    two = entries[:2]
    rows = [metadata_for_one(x) for x in two]
    return {
        "status": "PUBLISHED_PROGRAMME_METADATA_AND_SCHEMA_ONLY",
        "doi_inventory_source_count": 2,
        "distinct_original_published_programmes": 4,
        "raw_same_cohort_joint_state_verified_programmes": 0,
        "source_results": rows,
        "raw_alleles_or_fitness_values_read": False,
        "published_raw_files_redistributed": False,
        "no_empirical_function_effect_estimated": True,
        "decision": "REVIEW_SOURCE_SCHEMAS_THEN_FREEZE_JOIN_GRAIN_BEFORE_ANY_EFFECT",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", type=Path, default=REGISTRY)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    result = audit(registry)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"], "sources": [
            {"id": x["programme_id"], "metadata": x["source_metadata_status"],
             "files": x["source_files_status"], "decision": x["decision"],
             "matched_schemas": sum(y["schema_status"] == "verified_first_row_schema_only"
                                    for y in x["source_workbook_schemas"])}
            for x in result["source_results"]],
        "raw_same_cohort_joint_state_verified_programmes": 0,
        "no_outcome_analysis": True,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
