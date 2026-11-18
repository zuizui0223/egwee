#!/usr/bin/env python3
"""Original-source Zenodo v2 file inventory + outcome-blind CSV schema receipt.

Only original official record file URLs and bytes; no signed seed outcomes or
network values inspected. Source files never persisted in Git or CI artifacts.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request

RECORD_ID = "20284225"
RECORD_API = f"https://zenodo.org/api/records/{RECORD_ID}"
REQUIRED = {
    "seedset_data.csv": {"Study_id", "Site_id", "Species_long", "fertilized",
                         "unfertilized", "mean_PSI.log", "fc_HL_z.sc"},
    "data_sem.csv": {"Study_id", "Site_id", "mean_PSI.log", "fc_HL_z.sc"},
}
OPTIONAL = {"Overview_data_sets.xlsx"}
MAX_BYTES = 64 * 1024 * 1024
USER_AGENT = "EGWEE-original-source-audit/1.0 (+https://github.com/zuizui0223/egwee)"
PROTOCOL = "research/europe_seed_network_transport/PROTOCOL_SOURCE_FREEZE_20261118.md"


def fetch_bytes(url: str, max_bytes: int) -> bytes:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in {"zenodo.org", "www.zenodo.org"}:
        raise ValueError(f"ACCESS_STOP: not an official Zenodo HTTPS URL: {parsed.hostname}")
    request = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/csv, application/octet-stream",
    })
    chunks, size = [], 0
    with urllib.request.urlopen(request, timeout=100) as response:
        if "html" in str(response.headers.get("Content-Type", "")).lower():
            raise ValueError("ACCESS_STOP: HTML instead of metadata or source bytes")
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            size += len(block)
            if size > max_bytes:
                raise ValueError("ACCESS_STOP: exceeded bounded source file size")
            chunks.append(block)
    if size == 0:
        raise ValueError("ACCESS_STOP: empty official source")
    return b"".join(chunks)


def parse_original_csv_schema(file_data: bytes, expected: set[str]) -> dict:
    text = file_data.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(text, newline=""))
    header = next(reader, None)
    if not header or len(header) != len(set(header)) or any(not h.strip() for h in header):
        raise ValueError("SCHEMA_STOP: missing, blank or duplicate source header")
    columns = [h.strip() for h in header]
    missing = expected.difference(columns)
    if missing:
        raise ValueError("SCHEMA_STOP: preregistered columns unavailable: " + str(sorted(missing)))
    total = 0
    for record in reader:
        if len(record) != len(header):
            raise ValueError("SCHEMA_STOP: irregular CSV column count")
        total += 1  # no biological field values interpreted
    if total == 0:
        raise ValueError("SCHEMA_STOP: zero original data rows")
    return {"rows_excluding_header": total, "columns": columns,
            "header_column_count": len(columns), "outcomes_read": False}


def extract_files(meta: dict) -> dict[str, dict]:
    files = meta.get("files")
    if not isinstance(files, list):
        raise ValueError("SOURCE_STOP: Zenodo metadata lacks record files array")
    found = {}
    for item in files:
        key = item.get("key") or item.get("filename")
        if not key or key in found:
            raise ValueError("SOURCE_STOP: blank or duplicate file key")
        found[key] = item
    return found


def checksum_file(content: bytes, declared: str | None) -> dict:
    digest = hashlib.sha256(content).hexdigest()
    md5 = hashlib.md5(content).hexdigest()  # legacy Zenodo file integrity only
    if declared:
        algo, sep, claimed = declared.partition(":")
        if not sep:
            algo, claimed = "md5", declared
        computed = {"md5": md5, "sha256": digest}.get(algo.lower())
        if computed is None or computed.lower() != claimed.lower():
            raise ValueError("SOURCE_STOP: original file checksum failed")
    return {"sha256_actual": digest, "md5_actual": md5}


def audit() -> dict:
    metadata_bytes = fetch_bytes(RECORD_API, 8 * 1024 * 1024)
    meta = json.loads(metadata_bytes)
    if str(meta.get("id")) != RECORD_ID:
        raise ValueError("SOURCE_STOP: returned Zenodo record ID mismatch")
    files = extract_files(meta)
    receipt = {
        "source_record_id": RECORD_ID, "doi": meta.get("doi"),
        "record_created": meta.get("created"), "record_updated": meta.get("updated"),
        "title": (meta.get("metadata") or {}).get("title"),
        "license": (meta.get("metadata") or {}).get("license"),
        "all_record_filenames": sorted(files),
        "file_inventory": {}, "source_row_values_read": False,
        "original_files_distributed": False, "original_protocol": PROTOCOL,
    }
    for name in sorted(REQUIRED):
        source_file = files.get(name)
        if not source_file:
            raise ValueError("SOURCE_STOP: required original file absent: " + name)
        links = source_file.get("links") or {}
        url = links.get("self") or links.get("download") or links.get("content")
        if not isinstance(url, str):
            raise ValueError("SOURCE_STOP: missing advertised file download: " + name)
        declared_size = source_file.get("size")
        if isinstance(declared_size, int) and declared_size > MAX_BYTES:
            raise ValueError("ACCESS_STOP: source exceeds preset max bytes: " + name)
        data = fetch_bytes(url, MAX_BYTES)
        digests = checksum_file(data, source_file.get("checksum"))
        receipt["file_inventory"][name] = {
            "declared_size": declared_size, "bytes": len(data),
            "declared_checksum": source_file.get("checksum"),
            **digests, **parse_original_csv_schema(data, REQUIRED[name]),
        }
    return receipt


def self_test():
    raw = b"Study_id,Site_id,Species_long,fertilized,unfertilized,mean_PSI.log,fc_HL_z.sc\nA,s1,Plant,3,2,0.5,1.0\n"
    x = parse_original_csv_schema(raw, REQUIRED["seedset_data.csv"])
    if x["rows_excluding_header"] != 1 or x["outcomes_read"] is not False:
        raise AssertionError("Synthetic source schema test failed")
    try:
        parse_original_csv_schema(b"Study_id,Site_id,Study_id\n1,a,2\n", {"Study_id"})
        raise AssertionError("Duplicate header was wrongly admitted")
    except ValueError:
        pass
    print("ZENODO_SCHEMA_SYNTHETIC_TEST_PASS")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.output is None:
        p.error("--output required unless --self-test")
    report = {"protocol": PROTOCOL, "stage": "outcome_blind_file_headers_only",
              "data_record_id": RECORD_ID, "signed_outcomes_inspected": False,
              "primary_effect_estimated": False}
    try:
        report.update(audit())
        report["status"] = "SOURCE_SCHEMA_PASS"
    except Exception as exc:
        report["status"] = "ACCESS_OR_SCHEMA_STOP"
        report["reason"] = type(exc).__name__ + ": " + str(exc)[:280]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("EUROPE_SEED_SOURCE_SCHEMA " + json.dumps(report, sort_keys=True, ensure_ascii=False), flush=True)
    return 0 if report["status"] == "SOURCE_SCHEMA_PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
