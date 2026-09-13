from __future__ import annotations

import csv
import io
import json
import re
import urllib.request

RECORD_ID = 4999157
RECORD_URL = f"https://zenodo.org/api/records/{RECORD_ID}"
EXPECTED = {
    "NatVsRoof_Microsats_FinalData.csv",
    "Parentage_Microsats_FinalData.csv",
}

STRUCTURAL_KEYWORDS = (
    "population",
    "pop",
    "site",
    "roof",
    "sample",
    "individual",
    "offspring",
    "progeny",
    "parent",
    "maternal",
    "mother",
    "father",
    "paternal",
    "paternity",
    "assignment",
    "assigned",
    "lod",
    "confidence",
    "sex",
    "role",
    "locus",
)

ASSIGNMENT_KEYWORDS = (
    "father",
    "paternal",
    "paternity",
    "assignment",
    "assigned",
    "lod",
    "confidence",
    "cervus",
)


def get_bytes(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "egwee-penstemon-2019-schema-audit/1.0",
            "Accept": "application/json,text/csv,*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        payload = response.read()
    assert payload, url
    return payload


def get_json(url: str) -> dict:
    return json.loads(get_bytes(url).decode("utf-8"))


def file_name(item: dict) -> str:
    return str(item.get("key") or item.get("filename") or item.get("name") or "")


def file_content_url(item: dict) -> str:
    links = item.get("links") or {}
    for key in ("content", "download", "self"):
        value = links.get(key)
        if isinstance(value, str) and value.startswith("http"):
            return value
    raise KeyError(f"No downloadable link for {file_name(item)!r}: {links!r}")


def is_number(value: str) -> bool:
    value = value.strip()
    if not value:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def compact_text_cells(row: list[str]) -> list[str]:
    # Schema audit only: expose short nonnumeric labels, never genotype values.
    out: list[str] = []
    for raw in row:
        value = raw.strip()
        if not value or is_number(value):
            continue
        if len(value) > 100:
            value = value[:100]
        out.append(value)
    return out[:30]


def keyword_hits(rows: list[list[str]], keywords: tuple[str, ...]) -> dict[str, list[str]]:
    hits: dict[str, set[str]] = {key: set() for key in keywords}
    for row in rows:
        for raw in row:
            value = raw.strip()
            if not value or is_number(value):
                continue
            low = value.lower()
            for key in keywords:
                if re.search(rf"(^|[^a-z]){re.escape(key)}([^a-z]|$)", low) or key in low:
                    hits[key].add(value[:120])
    return {key: sorted(values)[:20] for key, values in hits.items() if values}


def inspect_csv(name: str, payload: bytes) -> dict[str, object]:
    text = payload.decode("utf-8-sig", errors="replace")
    rows = [row for row in csv.reader(io.StringIO(text))]
    ncols = max((len(row) for row in rows), default=0)
    print(f"PENSTEMON_SCHEMA file={name!r} rows={len(rows)} max_cols={ncols} bytes={len(payload)}")

    # First rows may be GenAlEx metadata rather than ordinary CSV headers.
    for idx, row in enumerate(rows[:8], start=1):
        labels = compact_text_cells(row)
        print(f"PENSTEMON_SCHEMA_LABELS file={name!r} row={idx} labels={labels!r}")

    structural = keyword_hits(rows[:30], STRUCTURAL_KEYWORDS)
    assignments = keyword_hits(rows, ASSIGNMENT_KEYWORDS)
    print(f"PENSTEMON_STRUCTURAL_KEYWORDS file={name!r} hits={structural!r}")
    print(f"PENSTEMON_ASSIGNMENT_KEYWORDS file={name!r} hits={assignments!r}")

    return {
        "rows": len(rows),
        "max_cols": ncols,
        "structural": structural,
        "assignments": assignments,
    }


def main() -> None:
    record = get_json(RECORD_URL)
    files = record.get("files") or []
    by_name = {file_name(item): item for item in files}
    print(
        "PENSTEMON_ZENODO_RECORD "
        f"id={record.get('id')!r} doi={(record.get('metadata') or {}).get('doi')!r} "
        f"files={sorted(by_name)!r}"
    )
    assert EXPECTED <= set(by_name), (EXPECTED - set(by_name), sorted(by_name))

    results: dict[str, dict[str, object]] = {}
    for name in sorted(EXPECTED):
        item = by_name[name]
        size = item.get("size") or (item.get("metadata") or {}).get("size")
        url = file_content_url(item)
        print(f"PENSTEMON_ZENODO_FILE name={name!r} size={size!r} content_url={url!r}")
        payload = get_bytes(url)
        results[name] = inspect_csv(name, payload)

    parentage = results["Parentage_Microsats_FinalData.csv"]
    assignment_hits = parentage["assignments"]
    has_source_assignment_schema = bool(assignment_hits)
    print(
        "PENSTEMON_PARENTAGE_ASSIGNMENT_SCHEMA "
        f"present={has_source_assignment_schema!r} hits={assignment_hits!r}"
    )

    # Do not fail merely because source assignment output is absent. Absence is a
    # legitimate terminal scientific result for the next recovery step.
    assert int(parentage["rows"]) > 0
    assert int(parentage["max_cols"]) > 0
    print("PENSTEMON_2019_ZENODO_SCHEMA_GATE PASS")


if __name__ == "__main__":
    main()
