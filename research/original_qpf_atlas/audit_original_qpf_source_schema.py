#!/usr/bin/env python3
"""Original Q/P/F source atlas: official Dryad metadata and first-row schema only.

No seed, visit, pollen, genotype, individual ID or other outcome values are
printed, saved or fitted. Unavailable files are explicit SOURCE_ACCESS_STOP.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from io import StringIO
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research/compatibility_function"))
from audit_dryad_joint_state_source_schema import (  # type: ignore
    BASE,
    link,
    request_bytes,
    request_json,
    validate_metadata,
    version_file_metadata,
    workbook_schema,
)

REGISTRY = ROOT / "research/original_qpf_atlas/SCHEMA_SOURCE_REGISTRY_20261117.json"
MAX_FILE = 2 * 1024 * 1024
MAX_TOTAL_FILES = 18
SAFE_HEAD = re.compile(r"^[A-Za-z][A-Za-z0-9 _./%():+-]{0,69}$")

def csv_schema(blob: bytes) -> dict:
    text = blob.decode("utf-8-sig")
    reader = csv.reader(StringIO(text, newline=""))
    try:
        first = next(reader)
    except StopIteration:
        raise ValueError("Empty CSV")
    if not 0 < len(first) <= 100:
        raise ValueError("Unsupported CSV header width")
    n = sum(1 for _ in reader)
    if n < 1:
        raise ValueError("CSV header without rows")
    return {
        "physical_rows_including_header": n + 1,
        "first_row_field_count": len(first),
        "first_row_header_labels_provisional": [
            x.strip() if SAFE_HEAD.fullmatch(x.strip()) else "<unverified_header>"
            for x in first
        ],
        "data_values_read_or_saved": False,
    }

def one_source(s: dict) -> dict:
    doi = s["doi"]
    api = BASE + "/api/v2/datasets/" + quote("doi:" + doi, safe="")
    out = {
        "id": s["id"], "doi": doi, "programme": s["name"],
        "source_status": "not_checked",
        "expected_files": s["expected_files"],
        "source_overlap_warning": s["known_overlap"],
        "P_measurement_intent": s["p_intent"],
        "file_results": [],
        "any_outcomes_opened": False,
        "cross_source_IDs_joined": False,
        "reproductive_effect_tested": False,
    }
    try:
        meta = request_json(api)
        validate_metadata(meta, doi)
        out["source_status"] = "original_doi_metadata_verified"
        out["official_title"] = str(meta.get("title", ""))[:180]
        files = version_file_metadata(meta, api)
    except (HTTPError, URLError, ValueError, KeyError, json.JSONDecodeError) as exc:
        out["decision"] = "DOI_OR_SOURCE_FILE_METADATA_STOP"
        out["error_class"] = type(exc).__name__
        if isinstance(exc, HTTPError):
            out["http_status"] = exc.code
        return out
    declared = [str(f.get("path", "")).rsplit("/", 1)[-1] for f in files]
    out["official_file_inventory_count"] = len(files)
    out["official_file_inventory_names"] = declared
    expected = set(x.lower() for x in s["expected_files"])
    observed = {x.lower() for x in declared}
    out["expected_file_missing"] = sorted(expected - observed)
    inspected = 0
    for f in files:
        name = str(f.get("path", "")).rsplit("/", 1)[-1]
        if name.lower() not in expected:
            continue
        inspected += 1
        rec = {"official_file_name": name, "schema_status": "not_checked",
               "official_declared_bytes": f.get("size")}
        size = f.get("size")
        if not isinstance(size, int) or not 0 < size <= MAX_FILE:
            rec["schema_status"] = "DECLARED_FILE_SIZE_GATE_STOP"
        else:
            href = link(f, "stash:download")
            if not href:
                rec["schema_status"] = "NO_API_ADVERTISED_DOWNLOAD_LINK"
            else:
                try:
                    raw = request_bytes(href, MAX_FILE)
                    if len(raw) != size:
                        raise ValueError("Downloaded file byte length differs from official metadata")
                    rec["original_file_sha256"] = hashlib.sha256(raw).hexdigest()
                    if name.lower().endswith(".xlsx"):
                        rec["sheets"] = workbook_schema(raw)
                    elif name.lower().endswith(".csv"):
                        rec["csv"] = csv_schema(raw)
                    else:
                        raise ValueError("Unapproved whitelist file extension")
                    rec["schema_status"] = "SOURCE_FIRST_ROW_SCHEMA_ONLY_VERIFIED"
                except (HTTPError, URLError, ValueError, UnicodeError, KeyError, zipfile.BadZipFile) as exc:
                    rec["schema_status"] = "PUBLIC_SOURCE_DOWNLOAD_STOP"
                    rec["error_class"] = type(exc).__name__
                    if isinstance(exc, HTTPError):
                        rec["http_status"] = exc.code
        out["file_results"].append(rec)
    n_ok = sum(rec["schema_status"] == "SOURCE_FIRST_ROW_SCHEMA_ONLY_VERIFIED"
               for rec in out["file_results"])
    out["files_with_headers_verified"] = n_ok
    if out["expected_file_missing"]:
        out["decision"] = "SOURCE_EXPECTED_FILE_INVENTORY_MISMATCH"
    elif n_ok == len(expected):
        out["decision"] = "ALL_EXPECTED_HEADERS_VERIFIED_NO_BIOLOGICAL_ID_JOIN"
    elif n_ok:
        out["decision"] = "PARTIAL_SOURCE_SCHEMA_NO_BIOLOGICAL_ID_JOIN"
    else:
        out["decision"] = "SOURCE_ACCESS_STOP_OFFICIAL_FILE_METADATA_ONLY"
    return out

def audit(registry: dict) -> dict:
    if registry.get("schema_version") != 1:
        raise ValueError("Unknown source atlas registry")
    src = registry.get("sources")
    if not isinstance(src, list) or [x["id"] for x in src] != [
        "QPF001", "QPF002", "QPF003", "QPF004", "QPF005", "QPF006"
    ]:
        raise ValueError("Pre-outcome six-programme registration changed")
    file_n = sum(len(x["expected_files"]) for x in src)
    if file_n > MAX_TOTAL_FILES or file_n != 17:
        raise ValueError("File whitelist count invalid")
    results = [one_source(x) for x in src]
    return {
        "analysis_status": "SOURCE_SCHEMA_ONLY_NO_EFFECTS",
        "source_programmes_screened": len(src),
        "selected_original_source_file_targets": file_n,
        "metadata_dois_verified": sum(r["source_status"] == "original_doi_metadata_verified"
                                      for r in results),
        "source_files_with_headers_verified": sum(r.get("files_with_headers_verified", 0)
                                                   for r in results),
        "programmes_complete_first_row_schema": sum(
            r["decision"] == "ALL_EXPECTED_HEADERS_VERIFIED_NO_BIOLOGICAL_ID_JOIN"
            for r in results),
        "same_unit_verified_QPF_programmes": 0,
        "global_macro_effect_estimated": False,
        "outcome_values_or_genotypes_examined": False,
        "original_source_rows_redistributed": False,
        "source_programmes": results,
        "decision": "REVIEW_STRUCTURAL_GRAINS_BEFORE_FREEZING_ANY_OUTCOME_TEST",
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", type=Path, default=REGISTRY)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    r = audit(json.loads(args.registry.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(r, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "analysis_status": r["analysis_status"],
        "metadata_dois_verified": r["metadata_dois_verified"],
        "selected_original_source_file_targets": r["selected_original_source_file_targets"],
        "source_files_with_headers_verified": r["source_files_with_headers_verified"],
        "source_programmes": [
            {"id": x["id"], "decision": x["decision"],
             "metadata_status": x["source_status"],
             "metadata_error_class": x.get("error_class"),
             "metadata_http_status": x.get("http_status"),
             "headers": x.get("files_with_headers_verified", 0),
             "source_http_statuses": sorted({y.get("http_status") for y in x.get("file_results", []) if y.get("http_status") is not None}),
             "error_types": sorted({y.get("error_class", y["schema_status"])
                                    for y in x.get("file_results", [])
                                    if y["schema_status"] != "SOURCE_FIRST_ROW_SCHEMA_ONLY_VERIFIED"})}
            for x in r["source_programmes"]
        ],
        "same_unit_verified_QPF_programmes": 0,
        "outcomes_opened": False,
    }, indent=2))

if __name__ == "__main__":
    main()
