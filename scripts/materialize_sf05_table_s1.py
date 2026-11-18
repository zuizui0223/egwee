from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"


def col_index(cell_ref: str) -> int:
    letters = re.match(r"[A-Z]+", cell_ref)
    if not letters:
        raise ValueError(cell_ref)
    n = 0
    for ch in letters.group(0):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def shared_strings(zf: zipfile.ZipFile) -> list[str]:
    name = "xl/sharedStrings.xml"
    if name not in zf.namelist():
        return []
    root = ET.fromstring(zf.read(name))
    out = []
    for si in root.findall(f"{{{NS_MAIN}}}si"):
        parts = [t.text or "" for t in si.iter(f"{{{NS_MAIN}}}t")]
        out.append("".join(parts))
    return out


def workbook_sheets(zf: zipfile.ZipFile) -> list[tuple[str, str]]:
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    relmap = {
        r.attrib["Id"]: r.attrib["Target"]
        for r in rels.findall(f"{{{NS_PKG_REL}}}Relationship")
    }
    sheets = []
    for sheet in wb.find(f"{{{NS_MAIN}}}sheets"):
        rid = sheet.attrib[f"{{{NS_REL}}}id"]
        target = relmap[rid].lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        sheets.append((sheet.attrib["name"], target))
    return sheets


def cell_value(cell: ET.Element, shared: list[str]) -> str:
    ctype = cell.attrib.get("t")
    if ctype == "inlineStr":
        return "".join(t.text or "" for t in cell.iter(f"{{{NS_MAIN}}}t"))
    v = cell.find(f"{{{NS_MAIN}}}v")
    if v is None or v.text is None:
        return ""
    raw = v.text
    if ctype == "s":
        return shared[int(raw)]
    if ctype == "b":
        return "TRUE" if raw == "1" else "FALSE"
    return raw


def sheet_matrix(zf: zipfile.ZipFile, path: str, shared: list[str]) -> list[list[str]]:
    root = ET.fromstring(zf.read(path))
    result: list[list[str]] = []
    for row in root.iter(f"{{{NS_MAIN}}}row"):
        vals: dict[int, str] = {}
        max_col = -1
        for cell in row.findall(f"{{{NS_MAIN}}}c"):
            idx = col_index(cell.attrib["r"])
            vals[idx] = cell_value(cell, shared)
            max_col = max(max_col, idx)
        if max_col < 0:
            result.append([])
        else:
            result.append([vals.get(i, "") for i in range(max_col + 1)])
    width = max((len(r) for r in result), default=0)
    return [r + [""] * (width - len(r)) for r in result]


def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower() or "sheet"


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: materialize_sf05_table_s1.py INPUT.xlsx OUTPUT_DIR")
    src = Path(sys.argv[1])
    outdir = Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)

    digest = hashlib.sha256(src.read_bytes()).hexdigest()
    manifest = {
        "source_frame": "SF05",
        "source_article_doi": "10.1093/aobpla/plad019",
        "source_file": "plad019_suppl_supplementary_table_s1.xlsx",
        "source_sha256": digest,
        "parser": "stdlib_zipfile_xml_no_spreadsheet_recalculation",
        "sheets": [],
    }

    with zipfile.ZipFile(src) as zf:
        shared = shared_strings(zf)
        for i, (name, path) in enumerate(workbook_sheets(zf), start=1):
            matrix = sheet_matrix(zf, path, shared)
            outfile = outdir / f"phase2_sf05_table_s1_sheet{i:02d}_{safe_name(name)}.csv"
            with outfile.open("w", newline="", encoding="utf-8") as fh:
                csv.writer(fh).writerows(matrix)
            manifest["sheets"].append({
                "index": i,
                "name": name,
                "xml_path": path,
                "rows": len(matrix),
                "columns": max((len(r) for r in matrix), default=0),
                "csv": outfile.name,
            })

    (outdir / "phase2_sf05_table_s1_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
