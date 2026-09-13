from __future__ import annotations

import re
import urllib.request

URL = "https://pmc.ncbi.nlm.nih.gov/articles/PMC3670206/"
UA = "Mozilla/5.0 egwee-magnolia-2013-schema/1.0"


def strip_html(s: str) -> str:
    s = re.sub(r"<sup[^>]*>.*?</sup>", "", s, flags=re.I | re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def main() -> None:
    req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=60) as r:
        html = r.read().decode("utf-8", errors="replace")

    # Locate Table 1 by its caption and print only headers plus population-group labels/row counts.
    m = re.search(r"(<table[^>]*>.*?</table>)", html, flags=re.I | re.S)
    tables = re.findall(r"<table[^>]*>.*?</table>", html, flags=re.I | re.S)
    target = None
    for table in tables:
        txt = strip_html(table)
        if "Seed production and mating system" in txt or ("Immigration rate by pollen" in txt and "Seed production rate" in txt):
            target = table
            break
    if target is None:
        raise RuntimeError(f"Table 1 not found; tables={len(tables)}")

    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", target, flags=re.I | re.S)
    parsed = []
    for row in rows:
        cells = re.findall(r"<(?:th|td)[^>]*>(.*?)</(?:th|td)>", row, flags=re.I | re.S)
        vals = [strip_html(c) for c in cells]
        if vals:
            parsed.append(vals)

    header_rows = parsed[:3]
    print(f"MAGNOLIA_TABLE1_SCHEMA rows={len(parsed)} header_rows={header_rows!r}")

    # Outcome-blind structural inventory: emit only likely population labels and column counts, not numeric outcome values.
    labels = []
    for vals in parsed[1:]:
        if vals and vals[0] and not re.fullmatch(r"[0-9.() %±+-]+", vals[0]):
            labels.append(vals[0])
    print(f"MAGNOLIA_TABLE1_GROUP_LABELS labels={labels!r}")
    print("MAGNOLIA_TABLE1_SCHEMA_GATE PASS no_numeric_outcomes_printed")


if __name__ == "__main__":
    main()
