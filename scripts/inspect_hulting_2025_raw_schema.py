from __future__ import annotations

import csv
import http.cookiejar
import io
import urllib.request
from collections import Counter

LANDING = "https://datadryad.org/dataset/doi%3A10.5061%2Fdryad.bnzs7h4mb"
CSV_URL = "https://datadryad.org/downloads/file_stream/3628536"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140 Safari/537.36"


def is_anubis(payload: bytes) -> bool:
    head = payload[:16384].decode("utf-8", errors="ignore").lower()
    return "anubis_challenge" in head or "proof-of-work" in head or ("anubis" in head and "protected" in head)


def main() -> None:
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    req = urllib.request.Request(LANDING, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    with opener.open(req, timeout=60) as r:
        r.read(2048)
        referer = r.geturl()

    req = urllib.request.Request(
        CSV_URL,
        headers={"User-Agent": UA, "Referer": referer, "Accept": "text/csv,text/plain,*/*"},
    )
    with opener.open(req, timeout=120) as r:
        payload = r.read()

    if is_anubis(payload):
        print("HULTING_2025_RAW_SCHEMA_GATE SOURCE_ACCESS_BLOCKED anubis_javascript_proof_of_work; no_bypass_attempted")
        return

    text = payload.decode("utf-8-sig", errors="strict")
    rows = list(csv.DictReader(io.StringIO(text)))
    header = list(rows[0].keys()) if rows else []
    required = {"block", "patch", "corner", "distance", "species", "stalk", "no.viable_seeds", "no.nonviable_seeds", "ptype", "reproductive", "length", "width", "height", "no_basal_fl", "no_axil_fl", "predisp_seedpred", "flags"}
    missing = required - set(header)
    if missing:
        raise RuntimeError(f"missing required columns: {sorted(missing)}")

    plant_key_cols = ["block", "patch", "corner", "distance", "species"]
    structure_key_cols = plant_key_cols + ["stalk"]
    plant_counts = Counter(tuple(r[c] for c in plant_key_cols) for r in rows)
    structure_counts = Counter(tuple(r[c] for c in structure_key_cols) for r in rows)
    bad_structure_keys = sum(1 for n in structure_counts.values() if n != 1)
    plant_structure_hist = Counter(plant_counts.values())

    invariant_cols = ["ptype", "reproductive", "length", "width", "height", "no_basal_fl", "no_axil_fl", "flags"]
    invariant_violations = 0
    by_plant: dict[tuple[str, ...], list[dict[str, str]]] = {}
    for r in rows:
        key = tuple(r[c] for c in plant_key_cols)
        by_plant.setdefault(key, []).append(r)
    for rr in by_plant.values():
        for c in invariant_cols:
            vals = {r[c] for r in rr}
            if len(vals) > 1:
                invariant_violations += 1

    print(
        "HULTING_2025_RAW_SCHEMA "
        f"bytes={len(payload)} rows={len(rows)} cols={len(header)} header={header!r} "
        f"n_plants={len(plant_counts)} n_structure_keys={len(structure_counts)} "
        f"bad_structure_keys={bad_structure_keys} plant_structure_hist={dict(sorted(plant_structure_hist.items()))!r} "
        f"invariant_violations={invariant_violations}"
    )
    print("HULTING_2025_RAW_SCHEMA_GATE PASS no_effects_calculated")


if __name__ == "__main__":
    main()
