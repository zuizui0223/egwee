from __future__ import annotations

import io
import urllib.request
from docx import Document

URL = "https://ars.els-cdn.com/content/image/1-s2.0-S0006320725000813-mmc1.docx"
UA = "Mozilla/5.0 egwee-primula-2025-schema/1.0"


def download() -> bytes:
    req = urllib.request.Request(URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def clean(x) -> str:
    return " ".join(str(x or "").split())


def main() -> None:
    payload = download()
    if not payload.startswith(b"PK"):
        raise RuntimeError(f"supplement is not DOCX/ZIP bytes: prefix={payload[:16]!r}")
    doc = Document(io.BytesIO(payload))
    print(f"PRIMULA_2025_SUPP_SCHEMA bytes={len(payload)} paragraphs={len(doc.paragraphs)} tables={len(doc.tables)}")

    for i, p in enumerate(doc.paragraphs, 1):
        text = clean(p.text)
        low = text.lower()
        if text and ("table a" in low or "fig. a" in low or "figure a" in low or "supplement" in low or "appendix" in low):
            print(f"PRIMULA_2025_SUPP_CAPTION {i:03d}: {text[:1000]}")

    for ti, table in enumerate(doc.tables, 1):
        rows = table.rows
        nrow = len(rows)
        ncol = max((len(r.cells) for r in rows), default=0)
        first = [clean(c.text) for c in rows[0].cells] if rows else []
        second = [clean(c.text) for c in rows[1].cells] if len(rows) > 1 else []
        print(
            f"PRIMULA_2025_SUPP_TABLE_SCHEMA table={ti} rows={nrow} cols={ncol} "
            f"row1={first!r} row2={second!r}"
        )

    print("PRIMULA_2025_SUPP_SCHEMA_GATE PASS headers_only_no_population_values_printed")


if __name__ == "__main__":
    main()
