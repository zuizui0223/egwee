#!/usr/bin/env python3
"""Schema-only independent audit of Clarke et al. (2024) published XLSX data.

Do NOT inspect pre/post fitness or heterozygosity values at Gate 0.
Reads an Office Open XML archive with Python's standard XML/ZIP facilities,
not with pandas/openpyxl or an alternate spreadsheet library.
The output is a non-redistributive schema and categorical-denominator receipt.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile
from xml.etree import ElementTree as ET

PINNED_GIT_BLOB_SHA1 = "546c93f67ffd67a8776f9a12cfe85af2dd42633d"
PINNED_COMMIT = "61c59003a66580f5ba090de46dd8614008373cb7"
DATA_DOI = "10.5683/SP3/9VKJI6"
PAPER_DOI = "10.1111/mec.17532"
R_CODE_URL = "https://github.com/AdamCSmithCWS/Genetic_rescue_meta/blob/61c59003a66580f5ba090de46dd8614008373cb7/Main_analysis_script.R"

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
EXPECTED = {
    "Study", "Study_n", "Pre_He", "Post_He", "PreHe_SE", "PostHe_SE",
    "Pre_fit", "Post_fit", "Prefit_SE", "Postfit_SE", "tran_R", "fit_par"
}
SENSITIVE_VALUES = {"Pre_He", "Post_He", "Pre_fit", "Post_fit",
                    "PreHe_SE", "PostHe_SE", "Prefit_SE", "Postfit_SE"}


def table_from_xlsx(path: Path) -> tuple[list[str], list[dict[str, str | None]]]:
    with zipfile.ZipFile(path, "r") as zf:
        bad = zf.testzip()
        if bad:
            raise ValueError(f"XLSX CRC failure: {bad}")
        strs = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", NS):
                strs.append("".join((node.text or "") for node in si.findall(".//m:t", NS)))
        sheet_xml = "xl/worksheets/sheet1.xml"
        if sheet_xml not in zf.namelist():
            raise ValueError("First XLSX sheet not found")
        sheet = ET.fromstring(zf.read(sheet_xml))
        grid = []
        for row in sheet.findall(".//m:sheetData/m:row", NS):
            cells = {}
            for cell in row.findall("m:c", NS):
                addr = cell.attrib.get("r", "")
                m = re.match(r"([A-Z]+)\d+", addr)
                if not m:
                    continue
                col = 0
                for ch in m.group(1):
                    col = col * 26 + ord(ch) - ord("A") + 1
                raw = cell.find("m:v", NS)
                typ = cell.attrib.get("t")
                if typ == "s" and raw is not None:
                    value = strs[int(raw.text)]
                elif typ == "inlineStr":
                    value = "".join((node.text or "") for node in cell.findall(".//m:t", NS))
                else:
                    value = raw.text if raw is not None else None
                cells[col - 1] = value
            if cells:
                grid.append(cells)
    if not grid:
        raise ValueError("No nonempty rows")
    max_col = max(grid[0])
    headers = [str(grid[0].get(i, "") or "").strip() for i in range(max_col + 1)]
    if len(set(headers)) != len(headers):
        raise ValueError("Nonunique headers")
    rows = [{name: raw.get(i) for i, name in enumerate(headers)} for raw in grid[1:]]
    return headers, rows


def audit(path: Path) -> dict:
    data = path.read_bytes()
    git_hash = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if git_hash != PINNED_GIT_BLOB_SHA1:
        raise ValueError(f"Source blob moved: expected {PINNED_GIT_BLOB_SHA1}, observed {git_hash}")
    headers, rows = table_from_xlsx(path)
    missing = EXPECTED - set(headers)
    if missing:
        raise ValueError(f"Expected fields absent: {sorted(missing)}")
    if headers.index("Study") > headers.index("fit_par"):
        raise ValueError("Original source analysis slice reversed")
    # Match original published author's select(Study:fit_par) then drop_na().
    selection = headers[headers.index("Study"):headers.index("fit_par") + 1]
    eligible = [r for r in rows if all(r.get(k) not in (None, "") for k in selection)]
    def tally(key: str, subset: list[dict]) -> dict[str,int]:
        return dict(sorted(Counter(str(row.get(key)) for row in subset).items()))
    complete_by_study = Counter(str(r.get("Study")) for r in eligible)
    timed = []
    for row in eligible:
        try:
            a = float(row["gen_post_He"])
            b = float(row["gen_post_fit"])
            timed.append(abs(a - b) < 1e-12)
        except (ValueError, TypeError, KeyError):
            timed.append(None)
    report = {
        "status": "SCHEMA_ONLY_NO_EFFECT_VALUES_OPENED",
        "date": "2026-11-15",
        "article_doi": PAPER_DOI,
        "data_doi": DATA_DOI,
        "source_git_commit": PINNED_COMMIT,
        "source_git_blob_sha1": git_hash,
        "source_sha256": hashlib.sha256(data).hexdigest(),
        "source_code": R_CODE_URL,
        "file_name": path.name,
        "worksheet": "sheet1",
        "columns": headers,
        "original_analysis_selected_columns": selection,
        "raw_table_rows": len(rows),
        "complete_original_author_slice_rows": len(eligible),
        "unique_original_studies_raw": len(set(str(r.get("Study")) for r in rows if r.get("Study"))),
        "unique_original_studies_complete": len(complete_by_study),
        "taxonomic_class_levels_complete": tally("Class", eligible),
        "fitness_measurement_and_heterozygosity_same_generation_rows": sum(v is True for v in timed),
        "fitness_measurement_and_heterozygosity_different_generation_rows": sum(v is False for v in timed),
        "fitness_measurement_timing_not_resolved_rows": sum(v is None for v in timed),
        "fitness_parameter_levels_raw": tally("fit_par", rows),
        "fitness_parameter_levels_complete": tally("fit_par", eligible),
        "translocation_treatment_levels_complete": tally("tran_R", eligible),
        "rows_per_study_complete": dict(sorted(complete_by_study.items())),
        "studies_by_fitness_parameter": {
            code: sorted({str(r["Study"]) for r in eligible if str(r.get("fit_par")) == code})
            for code in sorted({str(r.get("fit_par")) for r in eligible})
        },
        "all_complete_rows_share_pair_fields": all(r.get(x) not in (None, "") for r in eligible for x in SENSITIVE_VALUES),
        "secondary_analysis_permission": "SCHEMA_DISCOVERY_ONLY; separate blind endpoint codebook and estimand must be frozen before outcomes."
    }
    return report


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    report = audit(a.source)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "raw_rows": report["raw_table_rows"],
        "eligible_rows": report["complete_original_author_slice_rows"],
        "unique_studies": report["unique_original_studies_complete"],
        "fitness_categories": report["fitness_parameter_levels_complete"],
        "sha256": report["source_sha256"]
    }, indent=2))


if __name__ == "__main__":
    main()
