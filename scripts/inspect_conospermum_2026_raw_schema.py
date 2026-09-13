from __future__ import annotations

import io
import json
import re
import urllib.parse
import urllib.request

from openpyxl import load_workbook

DOI = "10.5061/dryad.95x69p907"
ROOT = "https://datadryad.org/api/v2"
PUBLIC_ROOT = "https://datadryad.org"
UA = "egwee-conospermum-2026-raw-schema/1.1"
TARGETS = {"Seedlings_scoring.xlsx", "Paternity_dataset.xlsx", "README.md"}


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def href(obj: dict, *keys: str) -> str | None:
    links = obj.get("_links", {})
    for key in keys:
        v = links.get(key)
        if isinstance(v, dict) and v.get("href"):
            h = v["href"]
            return PUBLIC_ROOT + h if h.startswith("/") else h
    return None


def file_items() -> list[dict]:
    key = urllib.parse.quote(f"doi:{DOI}", safe="")
    ds_url = f"{ROOT}/datasets/{key}"
    ds = get_json(ds_url)
    version_url = href(ds, "stash:version", "version")
    if not version_url:
        versions = get_json(ds_url + "/versions")
        items = versions.get("_embedded", {}).get("stash:versions", [])
        if not items:
            raise RuntimeError("no public Dryad version")
        version_url = href(items[0], "self")
    version = get_json(version_url)
    files_url = href(version, "stash:files", "files")
    if not files_url:
        files_url = f"{ROOT}/versions/{version['id']}/files"
    page = get_json(files_url)
    return page.get("_embedded", {}).get("stash:files", page.get("files", []))


def public_file_id(item: dict) -> str:
    self_url = href(item, "self") or ""
    m = re.search(r"/files/(\d+)$", self_url)
    if not m:
        raise RuntimeError(f"cannot derive public file id for {item.get('path')}: {self_url!r}")
    return m.group(1)


def download(item: dict) -> bytes:
    file_id = public_file_id(item)
    url = f"{PUBLIC_ROOT}/downloads/file_stream/{file_id}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main() -> None:
    selected = {}
    for item in file_items():
        path = item.get("path") or item.get("name")
        if path in TARGETS:
            selected[path] = item
    missing = TARGETS - set(selected)
    if missing:
        raise RuntimeError(f"missing targets: {sorted(missing)}")

    readme = download(selected["README.md"]).decode("utf-8", errors="replace")
    print("CONOSPERMUM_2026_README " + json.dumps(readme, ensure_ascii=False))

    for name in ("Seedlings_scoring.xlsx", "Paternity_dataset.xlsx"):
        payload = download(selected[name])
        wb = load_workbook(io.BytesIO(payload), read_only=True, data_only=True)
        print(f"CONOSPERMUM_2026_WORKBOOK name={name!r} sheets={wb.sheetnames!r} bytes={len(payload)}")
        for ws in wb.worksheets:
            rows = ws.iter_rows(values_only=True)
            first = next(rows, tuple())
            print(
                "CONOSPERMUM_2026_SHEET "
                f"workbook={name!r} sheet={ws.title!r} rows={ws.max_row} cols={ws.max_column} "
                f"header={list(first)!r}"
            )
    print("CONOSPERMUM_2026_RAW_SCHEMA_GATE PASS values_beyond_headers_not_printed")


if __name__ == "__main__":
    main()
