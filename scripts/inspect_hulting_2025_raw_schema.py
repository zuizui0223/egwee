from __future__ import annotations

import csv
import http.cookiejar
import io
import os
import urllib.error
import urllib.request
from collections import Counter

LANDING = "https://datadryad.org/dataset/doi%3A10.5061%2Fdryad.bnzs7h4mb"
FILE_ID = "3628536"
ROUTES = (
    ("file_stream", f"https://datadryad.org/downloads/file_stream/{FILE_ID}"),
    ("api_v2_download", f"https://datadryad.org/api/v2/files/{FILE_ID}/download"),
    ("stash_file_stream", f"https://datadryad.org/stash/downloads/file_stream/{FILE_ID}"),
)
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140 Safari/537.36"
OUT_ENV = "HULTING_2025_RAW_OUT"


def is_html(payload: bytes) -> bool:
    head = payload[:4096].lstrip().lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html") or b"<html" in head[:512]


def is_anubis(payload: bytes) -> bool:
    head = payload[:16384].decode("utf-8", errors="ignore").lower()
    return (
        "anubis_challenge" in head
        or "proof-of-work" in head
        or ("anubis" in head and "protected" in head)
    )


def open_landing() -> tuple[urllib.request.OpenerDirector, str]:
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    req = urllib.request.Request(
        LANDING,
        headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"},
    )
    with opener.open(req, timeout=60) as r:
        r.read(2048)
        return opener, r.geturl()


def try_route(
    opener: urllib.request.OpenerDirector,
    referer: str,
    label: str,
    url: str,
) -> tuple[bytes | None, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Referer": referer,
            "Accept": "text/csv,text/plain,application/octet-stream,*/*",
        },
    )
    try:
        with opener.open(req, timeout=120) as r:
            payload = r.read()
            status = getattr(r, "status", 200)
            ctype = r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        print(
            f"HULTING_2025_RAW_ROUTE label={label} status={exc.code} "
            f"bytes=0 content_type='' result=http_error"
        )
        return None, f"http_{exc.code}"
    except Exception as exc:
        print(
            f"HULTING_2025_RAW_ROUTE label={label} status=NA "
            f"bytes=0 content_type='' result={type(exc).__name__}"
        )
        return None, type(exc).__name__

    if is_anubis(payload):
        result = "anubis_challenge_no_bypass"
    elif is_html(payload):
        result = "html_not_csv"
    else:
        result = "candidate_bytes"

    print(
        f"HULTING_2025_RAW_ROUTE label={label} status={status} "
        f"bytes={len(payload)} content_type={ctype!r} result={result}"
    )
    return (payload if result == "candidate_bytes" else None), result


def validate_csv(payload: bytes) -> tuple[list[dict[str, str]], list[str]]:
    text = payload.decode("utf-8-sig", errors="strict")
    rows = list(csv.DictReader(io.StringIO(text)))
    header = list(rows[0].keys()) if rows else []
    required = {
        "block", "patch", "corner", "distance", "species", "stalk",
        "no.viable_seeds", "no.nonviable_seeds", "ptype", "reproductive",
        "length", "width", "height", "no_basal_fl", "no_axil_fl",
        "predisp_seedpred", "flags",
    }
    missing = required - set(header)
    if missing:
        raise RuntimeError(f"missing required columns: {sorted(missing)}")
    return rows, header


def main() -> None:
    opener, referer = open_landing()

    payload = None
    successful_route = ""
    route_results = []
    for label, url in ROUTES:
        candidate, result = try_route(opener, referer, label, url)
        route_results.append((label, result))
        if candidate is None:
            continue
        try:
            rows, header = validate_csv(candidate)
        except Exception as exc:
            print(
                f"HULTING_2025_RAW_ROUTE_VALIDATION label={label} "
                f"result=invalid_csv error={type(exc).__name__}:{exc}"
            )
            continue
        payload = candidate
        successful_route = label
        break

    if payload is None:
        print(
            "HULTING_2025_RAW_SCHEMA_GATE SOURCE_ACCESS_BLOCKED "
            f"routes={route_results!r}; no_access_control_bypass_attempted"
        )
        return

    rows, header = validate_csv(payload)
    plant_key_cols = ["block", "patch", "corner", "distance", "species"]
    structure_key_cols = plant_key_cols + ["stalk"]
    plant_counts = Counter(tuple(r[c] for c in plant_key_cols) for r in rows)
    structure_counts = Counter(tuple(r[c] for c in structure_key_cols) for r in rows)
    bad_structure_keys = sum(1 for n in structure_counts.values() if n != 1)
    plant_structure_hist = Counter(plant_counts.values())

    invariant_cols = [
        "ptype", "reproductive", "length", "width", "height",
        "no_basal_fl", "no_axil_fl", "flags",
    ]
    invariant_violations = 0
    by_plant: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for r in rows:
        key = tuple(r[c] for c in plant_key_cols)
        by_plant.setdefault(key, []).append(r)
    for rr in by_plant.values():
        for col in invariant_cols:
            vals = {r[col] for r in rr}
            if len(vals) > 1:
                invariant_violations += 1

    out_path = os.environ.get(OUT_ENV, "").strip()
    if out_path:
        with open(out_path, "wb") as fh:
            fh.write(payload)

    print(
        "HULTING_2025_RAW_SCHEMA "
        f"route={successful_route} bytes={len(payload)} rows={len(rows)} "
        f"cols={len(header)} header={header!r} n_plants={len(plant_counts)} "
        f"n_structure_keys={len(structure_counts)} bad_structure_keys={bad_structure_keys} "
        f"plant_structure_hist={dict(sorted(plant_structure_hist.items()))!r} "
        f"invariant_violations={invariant_violations} raw_out={out_path!r}"
    )
    print("HULTING_2025_RAW_SCHEMA_GATE PASS no_effects_calculated")


if __name__ == "__main__":
    main()
