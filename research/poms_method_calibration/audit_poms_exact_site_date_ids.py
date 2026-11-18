#!/usr/bin/env python3
"""Outcome-blind exact 1-km-square × date source-ID overlap audit.

Only sample identifiers, site/date strings, year, sampling/station IDs, and
occurrence sample_id foreign keys are inspected. No insect counts, floral
counts, taxon groups or ecological response values are accessed.
"""
from __future__ import annotations
import argparse
import csv
from collections import Counter, defaultdict
import hashlib
import io
import json
from pathlib import Path
import sys
import urllib.request
import zipfile

EXPECTED_MEMBER_SHA = {
    "pan": {
        "ukpoms_1kmpantrapdata_2017-2023_samples.csv": "70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277",
        "ukpoms_1kmpantrapdata_2017-2023_insects.csv": "2423bc370f388a0dafd05c4bd3a7af7491909311ffe6bf4d6607a3697213dcb9",
        "ukpoms_1kmpantrapdata_2017-2023_flowers.csv": "53daa167282092b7081190de00e020b4e2635fa5e7d4fc63d3454f7c338951ba",
    },
    "fit": {
        "ukpoms_1kmfitcountdata_2017-2023.csv": "29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52",
        "ukpoms_publicfitcountdata_2017-2023.csv": "bcd2ef780d3208a5a4aba5c191178900ccef705e5b569dc0160b27d00652dc3c",
    },
}
URLS = {
    "pan": "https://data-package.ceh.ac.uk/data/5841bfae-471b-498c-af89-c30e5140d6c5.zip",
    "fit": "https://data-package.ceh.ac.uk/data/d706088c-9d48-4be5-b156-6ed6ad5e0618.zip",
}
PAN_SAMPLES = "ukpoms_1kmpantrapdata_2017-2023_samples.csv"
PAN_INSECTS = "ukpoms_1kmpantrapdata_2017-2023_insects.csv"
PAN_FLOWERS = "ukpoms_1kmpantrapdata_2017-2023_flowers.csv"
FIT_1KM = "ukpoms_1kmfitcountdata_2017-2023.csv"
FIELDS = ("sample_id", "country", "x1km_square", "sample_projection", "date", "year")
MAX_BYTES = 512 * 1024 * 1024


def load_archive(name: str) -> zipfile.ZipFile:
    req = urllib.request.Request(URLS[name], headers={
        "User-Agent": "EGWEE-PoMS-ID-only-audit/1.0 (+https://github.com/zuizui0223/egwee)",
        "Accept": "application/zip, application/octet-stream",
    })
    with urllib.request.urlopen(req, timeout=120) as response:
        chunks = []
        n = 0
        while True:
            buf = response.read(1024 * 1024)
            if not buf:
                break
            n += len(buf)
            if n > MAX_BYTES:
                raise RuntimeError("SOURCE_STOP: exceeds safety byte limit")
            chunks.append(buf)
    data = b"".join(chunks)
    archive = zipfile.ZipFile(io.BytesIO(data))
    # EIDC regenerates archive packaging, so the wrapper SHA is not stable.
    # Fix identity at uncompressed CSV member bytes instead.
    for suffix, expected in EXPECTED_MEMBER_SHA[name].items():
        found = [m for m in archive.namelist() if m.endswith(suffix)]
        if len(found) != 1 or hashlib.sha256(archive.read(found[0])).hexdigest() != expected:
            raise RuntimeError("SOURCE_STOP: original uncompressed CSV SHA-256 mismatch: " + suffix)
    return archive


def rows_only(z: zipfile.ZipFile, suffix: str, fields: tuple[str, ...]):
    names = [n for n in z.namelist() if n.endswith(suffix)]
    if len(names) != 1:
        raise RuntimeError(f"SCHEMA_STOP: expected exactly one file ending {suffix}")
    with z.open(names[0]) as raw:
        text = io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace", newline="")
        reader = csv.reader(text)
        header = next(reader)
        if len(header) != len(set(header)):
            raise RuntimeError("SCHEMA_STOP: duplicated column names")
        missing = set(fields) - set(header)
        if missing:
            raise RuntimeError(f"SCHEMA_STOP: missing expected columns {sorted(missing)}")
        ids = [header.index(f) for f in fields]
        for row in reader:
            if len(row) != len(header):
                raise RuntimeError("SCHEMA_STOP: malformed CSV record")
            yield {f: row[i].strip() for f, i in zip(fields, ids)}


def summarize_sample_table(z: zipfile.ZipFile, file_suffix: str):
    sample_ids = set()
    by_event = defaultdict(list)
    missing_keys = Counter()
    for row in rows_only(z, file_suffix, FIELDS):
        rid = row["sample_id"]
        if not rid:
            raise RuntimeError("ID_STOP: missing sample_id")
        if rid in sample_ids:
            raise RuntimeError(f"ID_STOP: duplicate source sample_id in {file_suffix}")
        sample_ids.add(rid)
        site = tuple(row[x] for x in ("country", "sample_projection", "x1km_square"))
        dt = row["date"]
        yr = row["year"]
        if not all(site) or not dt or not yr:
            missing_keys["incomplete_site_date_or_year"] += 1
            continue
        key = (*site, dt)
        by_event[key].append((rid, yr))
    return {"sample_ids": sample_ids, "by_event": by_event, "missing_keys": dict(missing_keys)}


def occurrence_key_coverage(z: zipfile.ZipFile, suffix: str, valid_ids: set[str]) -> dict:
    n = linked = 0
    for row in rows_only(z, suffix, ("sample_id",)):
        n += 1
        if row["sample_id"] in valid_ids:
            linked += 1
    return {"rows": n, "linked_to_source_samples": linked, "unmatched": n - linked}


def summarize(pan, fit):
    pan_keys = set(pan["by_event"])
    fit_keys = set(fit["by_event"])
    matched = sorted(pan_keys & fit_keys)
    by_site = defaultdict(list)
    years = Counter()
    fit_groups = []
    pan_groups = []
    for k in matched:
        site = k[:3]
        by_site[site].append(k)
        py = {r[1] for r in pan["by_event"][k]}
        fy = {r[1] for r in fit["by_event"][k]}
        if py != fy or len(py) != 1:
            raise RuntimeError("ID_STOP: pan/FIT source years disagree on exact site-date")
        y = next(iter(py))
        years[y] += 1
        fit_groups.append(len(fit["by_event"][k]))
        pan_groups.append(len(pan["by_event"][k]))
    eligible = len(by_site) >= 20 and len(matched) >= 80 and len(years) >= 3
    return {
        "pan_sample_id_count": len(pan["sample_ids"]),
        "fit_1km_sample_id_count": len(fit["sample_ids"]),
        "pan_site_dates": len(pan_keys),
        "fit_site_dates": len(fit_keys),
        "unmatched_pan_events": len(pan_keys - fit_keys),
        "unmatched_fit_events": len(fit_keys - pan_keys),
        "exact_match_site_dates": len(matched),
        "exact_match_unique_site_keys": len(by_site),
        "matched_years": dict(sorted(years.items())),
        "pan_samples_in_matched_events": sum(pan_groups),
        "fit_counts_in_matched_events": sum(fit_groups),
        "pan_sample_per_event_min_max": [min(pan_groups), max(pan_groups)] if matched else None,
        "fit_count_per_event_min_max": [min(fit_groups), max(fit_groups)] if matched else None,
        "pan_incomplete_location_date_keys": pan["missing_keys"],
        "fit_incomplete_location_date_keys": fit["missing_keys"],
        "coverage_gate_pass": eligible,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    a = parser.parse_args()
    result = {
        "protocol": "research/poms_method_calibration/PROTOCOL_20261117.md",
        "data_gate": "site_id_only",
        "numeric_flower_or_insect_values_accessed": False,
        "effect_estimated": False,
        "source_uncompressed_csv_shas": EXPECTED_MEMBER_SHA,
    }
    try:
        with load_archive("pan") as pan_z, load_archive("fit") as fit_z:
            pan = summarize_sample_table(pan_z, PAN_SAMPLES)
            fit = summarize_sample_table(fit_z, FIT_1KM)
            result.update(summarize(pan, fit))
            result["pan_insects_id_coverage"] = occurrence_key_coverage(
                pan_z, PAN_INSECTS, pan["sample_ids"])
            result["pan_flowers_id_coverage"] = occurrence_key_coverage(
                pan_z, PAN_FLOWERS, pan["sample_ids"])
            result["status"] = (
                "exact_site_date_coverage_pass" if result["coverage_gate_pass"]
                else "site_date_coverage_STOP")
    except Exception as exc:
        result["status"] = "source_schema_or_id_STOP"
        result["reason"] = f"{type(exc).__name__}: {str(exc)[:220]}"
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PO MS EXACT-MATCH ID GATE " + json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "exact_site_date_coverage_pass" else 1


if __name__ == "__main__":
    sys.exit(main())
