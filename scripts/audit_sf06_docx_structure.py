from __future__ import annotations

import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
RESPONSES = ("Female fitness", "Male fitness", "Pollination")


def q(tag: str) -> str:
    return f"{{{NS}}}{tag}"


def cell_text(cell: ET.Element) -> str:
    return " ".join(
        " ".join((t.text or "").split())
        for t in cell.iter(q("t"))
        if (t.text or "").strip()
    ).strip()


def main() -> None:
    source = Path(sys.argv[1])
    with zipfile.ZipFile(source) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    tables = root.findall(".//" + q("tbl"))

    total_response_rows = 0
    print(f"SF06_DOCX_STRUCTURE tables={len(tables)}")
    for ti, table in enumerate(tables):
        shapes = Counter()
        response_rows = Counter()
        nonempty = 0
        first_rows = []
        for ri, row in enumerate(table.findall("./" + q("tr"))):
            cells = [cell_text(c) for c in row.findall("./" + q("tc"))]
            if not any(cells):
                continue
            nonempty += 1
            shapes[len(cells)] += 1
            labels = []
            for candidate in RESPONSES:
                if any(candidate.casefold() in c.casefold() for c in cells[:-2] if c):
                    labels.append(candidate)
            for label in labels:
                response_rows[label] += 1
            if labels:
                total_response_rows += 1
            if len(first_rows) < 4:
                # Structural preview only: redact final two result cells.
                preview = cells[:-2] + ["<RESULT_REDACTED>", "<VAR_SOURCE_REDACTED>"]
                first_rows.append((ri, len(cells), labels, preview))
        print(
            f"TABLE {ti}: nonempty_rows={nonempty} cell_count_hist={dict(shapes)} "
            f"response_rows={dict(response_rows)}"
        )
        for row in first_rows:
            print(f"TABLE {ti} PREVIEW {row}")

    print(f"TOTAL_ROWS_WITH_RESPONSE_LABEL={total_response_rows}")


if __name__ == "__main__":
    main()
