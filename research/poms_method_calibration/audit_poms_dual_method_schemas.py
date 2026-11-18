#!/usr/bin/env python3
"""Source-exact *schema-only* PoMS dual-method audit.

Reads archive structure, column headers and row counts. NEVER reads or reports
insect response values, flower counts, covariate values, coordinate values or
identifier tokens. Source files are not written to the repository or artifacts.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import urllib.request
import zipfile

SOURCES = {
    "pan": {
        "doi": "10.5285/5841bfae-471b-498c-af89-c30e5140d6c5",
        "url": "https://data-package.ceh.ac.uk/data/5841bfae-471b-498c-af89-c30e5140d6c5.zip",
    },
    "fit": {
        "doi": "10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618",
        "url": "https://data-package.ceh.ac.uk/data/d706088c-9d48-4be5-b156-6ed6ad5e0618.zip",
    },
}
MAX_ARCHIVE_BYTES = 512 * 1024 * 1024
MAX_MEMBER_BYTES = 256 * 1024 * 1024
MAX_CSV_MEMBERS = 60
USER_AGENT = "EGWEE-public-research-schema-only/1.0 (+https://github.com/zuizui0223/egwee)"


def download_to_temp(url: str, dest: Path) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/zip, application/octet-stream"},
    )
    sha = hashlib.sha256()
    total = 0
    with urllib.request.urlopen(req, timeout=120) as response:
        ctype = str(response.headers.get("Content-Type", "")).lower()
        if "text/html" in ctype:
            raise ValueError("Access STOP: URL returned HTML instead of original archive")
        with dest.open("wb") as fileobj:
            while True:
                buf = response.read(1024 * 1024)
                if not buf:
                    break
                total += len(buf)
                if total > MAX_ARCHIVE_BYTES:
                    raise ValueError("Access STOP: archive exceeds preset 512-MiB safety ceiling")
                sha.update(buf)
                fileobj.write(buf)
    if total == 0:
        raise ValueError("Access STOP: empty original source")
    return {"bytes": total, "sha256": sha.hexdigest()}


def inspect_archive(path: Path) -> list[dict]:
    if not zipfile.is_zipfile(path):
        raise ValueError("Access STOP: downloaded body is not a genuine ZIP")
    tables: list[dict] = []
    with zipfile.ZipFile(path) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not names:
            raise ValueError("Schema STOP: archive contains no CSV files")
        if len(names) > MAX_CSV_MEMBERS:
            raise ValueError("Schema STOP: too many CSV members for schema gate")
        for member in names:
            info = zf.getinfo(member)
            if info.file_size > MAX_MEMBER_BYTES:
                raise ValueError("Schema STOP: single CSV exceeds 256-MiB safety ceiling")
            # Hash the uncompressed CSV; EIDC ZIP wrappers may be regenerated.
            # No biological values are interpreted in this hash operation.
            csv_sha256 = hashlib.sha256(zf.read(member)).hexdigest()
            with zf.open(member) as infile:
                wrapped = io.TextIOWrapper(infile, encoding="utf-8-sig", errors="replace", newline="")
                reader = csv.reader(wrapped)
                header = next(reader, None)
                if not header:
                    raise ValueError(f"Schema STOP: empty/missing CSV header in {member}")
                if len(header) > 300:
                    raise ValueError(f"Schema STOP: unexpectedly wide CSV in {member}")
                # Row values are deliberately discarded, without interpretation.
                rows = sum(1 for _ in reader)
            tables.append({
                "member": member,
                "sha256_uncompressed_csv": csv_sha256,
                "bytes_uncompressed": info.file_size,
                "rows_excluding_header": rows,
                "header_fields": [str(v)[:180] for v in header],
            })
    return tables


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    report: dict = {
        "audit_version": "1.0.0",
        "protocol": "research/poms_method_calibration/PROTOCOL_20261117.md",
        "signed_outcomes_read": False,
        "ecological_effect_estimated": False,
        "sources": {},
        "status": "not_identifiable_pending_source",
    }
    all_ok = True
    for name, src in SOURCES.items():
        print(f"Auditing original-source metadata for {name} ({src['doi']})", flush=True)
        item = {"doi": src["doi"], "url": src["url"]}
        try:
            with tempfile.TemporaryDirectory() as scratch:
                local = Path(scratch) / "source_archive.zip"
                item.update(download_to_temp(src["url"], local))
                item["csv_tables"] = inspect_archive(local)
                item["status"] = "schema_pass"
        except Exception as exc:
            item["status"] = "source_or_schema_STOP"
            item["reason"] = f"{type(exc).__name__}: {str(exc)[:220]}"
            all_ok = False
        report["sources"][name] = item
        print(
            "SOURCE_SCHEMA_RECEIPT " +
            json.dumps({"name": name, **item}, sort_keys=True, ensure_ascii=False)[:13000],
            flush=True,
        )
    report["status"] = "schema_gate_pass" if all_ok else "source_or_schema_STOP"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("FINAL_GATE_STATUS=" + report["status"], flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
