from __future__ import annotations

import io
import re
import urllib.request
import zipfile
import xml.etree.ElementTree as ET

URL = "https://ars.els-cdn.com/content/image/1-s2.0-S0006320721000598-mmc1.docx"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def download() -> bytes:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 egwee-supplement-audit/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = response.read()
    assert payload[:2] == b"PK"
    return payload


def text(node: ET.Element) -> str:
    pieces = [t.text or "" for t in node.iter(f"{W}t")]
    return re.sub(r"\s+", " ", "".join(pieces)).strip()


def main() -> None:
    payload = download()
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        names = set(zf.namelist())
        assert "word/document.xml" in names
        root = ET.fromstring(zf.read("word/document.xml"))

    body = root.find(f"{W}body")
    assert body is not None
    line_no = 0
    table_no = 0
    for child in list(body):
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            value = text(child)
            if value:
                line_no += 1
                print(f"SPONDIAS_SUPP_PARA {line_no:03d} {value}")
        elif tag == "tbl":
            table_no += 1
            print(f"SPONDIAS_SUPP_TABLE_BEGIN {table_no}")
            row_no = 0
            for tr in child.findall(f"{W}tr"):
                row_no += 1
                cells = [text(tc) for tc in tr.findall(f"{W}tc")]
                print(f"SPONDIAS_SUPP_TABLE {table_no} ROW {row_no}: " + " | ".join(cells))
            print(f"SPONDIAS_SUPP_TABLE_END {table_no}")

    print(f"SPONDIAS_SUPP_SUMMARY bytes={len(payload)} paragraphs={line_no} tables={table_no}")


if __name__ == "__main__":
    main()
