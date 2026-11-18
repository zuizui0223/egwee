from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

DATASET_ID = "6jw833yrt4"
VERSION = 1
API = f"https://data.mendeley.com/public-api/datasets/{DATASET_ID}/files?folder_id=root&version={VERSION}"
OUT_MANIFEST = Path("evidence/meta_extraction/phase2_cf01_brassica_mendeley_manifest_v1.json")
OUT_STATUS = Path("manuscript/PHASE2_CF01_BRASSICA_MENDELEY_SCHEMA_2026-09-24.md")

INTEREST_TERMS = (
    "site", "plot", "condition", "treatment", "habitat", "forest", "land", "fruit",
    "flower", "visit", "visitor", "bee", "poll", "coordinate", "lat", "lon", "plant",
)


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "EGWEE-CF01/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "EGWEE-CF01/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def sniff_delimited(raw: bytes, filename: str) -> dict:
    text = raw.decode("utf-8-sig", errors="replace")
    sample = text[:8192]
    delimiter = None
    try:
        delimiter = csv.Sniffer().sniff(sample, delimiters=",;\t").delimiter
    except Exception:
        delimiter = "\t" if filename.lower().endswith(".tsv") else ","
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    all_rows = list(reader)
    header = [x.strip() for x in all_rows[0]] if all_rows else []
    data = all_rows[1:] if len(all_rows) > 1 else []
    return {
        "format": "delimited",
        "delimiter": delimiter,
        "columns": header,
        "data_rows": len(data),
        "interest_columns": [c for c in header if any(t in c.lower() for t in INTEREST_TERMS)],
        "first_rows_redacted_to_structure": [
            {header[i]: row[i] if i < len(row) and header[i].lower() in {"site","plot","condition","treatment","habitat"} else "<value>"
             for i in range(len(header))}
            for row in data[:3]
        ],
    }


def xlsx_schema(raw: bytes) -> dict:
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
    sheets = {}
    for ws in wb.worksheets:
        values = ws.iter_rows(values_only=True)
        try:
            first = next(values)
        except StopIteration:
            sheets[ws.title] = {"columns": [], "data_rows": 0, "interest_columns": []}
            continue
        header = ["" if x is None else str(x).strip() for x in first]
        n = sum(1 for _ in values)
        sheets[ws.title] = {
            "columns": header,
            "data_rows": n,
            "interest_columns": [c for c in header if any(t in c.lower() for t in INTEREST_TERMS)],
        }
    return {"format": "xlsx", "sheets": sheets}


def inspect_file(filename: str, raw: bytes) -> dict:
    lower = filename.lower()
    if lower.endswith((".csv", ".tsv", ".txt")):
        return sniff_delimited(raw, filename)
    if lower.endswith((".xlsx", ".xlsm")):
        return xlsx_schema(raw)
    if lower.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            return {
                "format": "zip",
                "members": [{"path": x.filename, "bytes": x.file_size} for x in zf.infolist()],
            }
    return {"format": "other"}


def main() -> None:
    listing = get_json(API)
    assert isinstance(listing, list) and listing, listing

    result = {
        "schema_version": 1,
        "dataset_id": DATASET_ID,
        "version": VERSION,
        "dataset_doi": "10.17632/6jw833yrt4.1",
        "public_api": API,
        "files": [],
        "direct_visitation_file_hint_detected": False,
        "fruit_set_file_hint_detected": False,
        "effect_calculation_opened": False,
    }

    for item in listing:
        filename = item.get("filename") or item.get("name") or ""
        details = item.get("content_details") or {}
        url = details.get("download_url") or item.get("download_url") or ""
        assert filename and url, item
        raw = get_bytes(url)
        entry = {
            "filename": filename,
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "mendeley_file_id": item.get("id") or "",
            "declared_size": details.get("size") or item.get("size"),
            "schema": inspect_file(filename, raw),
        }
        result["files"].append(entry)
        name_lower = filename.lower()
        cols_text = json.dumps(entry["schema"], ensure_ascii=False).lower()
        if ("visit" in name_lower or "visitor" in name_lower or "pollin" in name_lower) or "visit" in cols_text:
            result["direct_visitation_file_hint_detected"] = True
        if "fruit" in name_lower or "fruit" in cols_text:
            result["fruit_set_file_hint_detected"] = True

    OUT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    OUT_STATUS.parent.mkdir(parents=True, exist_ok=True)
    OUT_MANIFEST.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# CFTQ0030 Brassica Mendeley schema audit — 2026-09-24",
        "",
        f"- dataset: **10.17632/{DATASET_ID}.1**",
        f"- public root files: **{len(result['files'])}**",
        f"- direct-visitation file/column hint detected: **{str(result['direct_visitation_file_hint_detected']).lower()}**",
        f"- fruit-set file/column hint detected: **{str(result['fruit_set_file_hint_detected']).lower()}**",
        "- numerical EGWEE effect calculation opened: **false**",
        "",
        "## Files",
        "",
    ]
    for f in result["files"]:
        schema = f["schema"]
        lines.append(f"### {f['filename']}")
        lines.append("")
        lines.append(f"- bytes: {f['bytes']}")
        lines.append(f"- format: {schema.get('format')}")
        if schema.get("format") == "delimited":
            lines.append(f"- rows: {schema.get('data_rows')}")
            lines.append(f"- columns: {', '.join(schema.get('columns') or [])}")
            lines.append(f"- I/F/exposure-related columns: {', '.join(schema.get('interest_columns') or []) or 'none'}")
        elif schema.get("format") == "xlsx":
            for sheet, ss in schema["sheets"].items():
                lines.append(f"- sheet {sheet}: rows={ss['data_rows']}; columns={', '.join(ss['columns'])}")
        elif schema.get("format") == "zip":
            lines.append(f"- archive members: {len(schema.get('members') or [])}")
        lines.append("")
    lines += [
        "## Gate",
        "",
        "This audit is schema-only. If the public files expose direct B. rapa flower-visitation data plus",
        "fruit set and source site/condition identifiers, proceed to the locked six-site I-F reconstruction.",
        "If they expose only surrounding bee diversity and fruit set, do not substitute bee-community",
        "sampling for the frozen direct-visitation endpoint; the direct I-F programme must remain blocked",
        "unless another legitimate public source supplies the visitation rows.",
        "",
    ]
    OUT_STATUS.write_text("\n".join(lines), encoding="utf-8")

    print(
        "PHASE2_CF01_BRASSICA_MENDELEY_SCHEMA_OK "
        f"files={len(result['files'])} visitation_hint={str(result['direct_visitation_file_hint_detected']).lower()} "
        f"fruit_hint={str(result['fruit_set_file_hint_detected']).lower()} effects_opened=false"
    )


if __name__ == "__main__":
    main()
