from __future__ import annotations

import http.cookiejar
import io
import json
import re
import urllib.parse
import urllib.request

from openpyxl import load_workbook

DOI = "10.5061/dryad.95x69p907"
ROOT = "https://datadryad.org/api/v2"
PUBLIC_ROOT = "https://datadryad.org"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140 Safari/537.36"
TARGETS = {"Seedlings_scoring.xlsx", "Paternity_dataset.xlsx", "README.md"}


def href(obj: dict, *keys: str) -> str | None:
    links = obj.get("_links", {})
    for key in keys:
        v = links.get(key)
        if isinstance(v, dict) and v.get("href"):
            h = v["href"]
            return PUBLIC_ROOT + h if h.startswith("/") else h
    return None


def get_json(opener: urllib.request.OpenerDirector, url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with opener.open(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def file_items(opener: urllib.request.OpenerDirector) -> list[dict]:
    key = urllib.parse.quote(f"doi:{DOI}", safe="")
    ds_url = f"{ROOT}/datasets/{key}"
    ds = get_json(opener, ds_url)
    version_url = href(ds, "stash:version", "version")
    if not version_url:
        versions = get_json(opener, ds_url + "/versions")
        items = versions.get("_embedded", {}).get("stash:versions", [])
        if not items:
            raise RuntimeError("no public Dryad version")
        version_url = href(items[0], "self")
    version = get_json(opener, version_url)
    files_url = href(version, "stash:files", "files") or f"{ROOT}/versions/{version['id']}/files"
    page = get_json(opener, files_url)
    return page.get("_embedded", {}).get("stash:files", page.get("files", []))


def public_file_id(item: dict) -> str:
    self_url = href(item, "self") or ""
    m = re.search(r"/files/(\d+)$", self_url)
    if not m:
        raise RuntimeError(f"cannot derive public file id for {item.get('path')}: {self_url!r}")
    return m.group(1)


def prime_browser_session(opener: urllib.request.OpenerDirector) -> str:
    landing = f"{PUBLIC_ROOT}/dataset/doi%3A10.5061%2Fdryad.95x69p907"
    req = urllib.request.Request(
        landing,
        headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"},
    )
    with opener.open(req, timeout=60) as r:
        r.read(1024)
        return r.geturl()


def download(opener: urllib.request.OpenerDirector, item: dict, referer: str) -> bytes:
    file_id = public_file_id(item)
    url = f"{PUBLIC_ROOT}/downloads/file_stream/{file_id}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Referer": referer,
            "Accept": "application/octet-stream,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*",
        },
    )
    with opener.open(req, timeout=120) as r:
        return r.read()


def main() -> None:
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    items = file_items(opener)
    selected = {}
    for item in items:
        path = item.get("path") or item.get("name")
        if path in TARGETS:
            selected[path] = item
    missing = TARGETS - set(selected)
    if missing:
        raise RuntimeError(f"missing targets: {sorted(missing)}")

    referer = prime_browser_session(opener)
    print(f"CONOSPERMUM_2026_BROWSER_SESSION landing={referer!r} cookies={len(list(jar))}")

    readme = download(opener, selected["README.md"], referer).decode("utf-8", errors="replace")
    print("CONOSPERMUM_2026_README " + json.dumps(readme, ensure_ascii=False))

    for name in ("Seedlings_scoring.xlsx", "Paternity_dataset.xlsx"):
        workbook_bytes = download(opener, selected[name], referer)
        wb = load_workbook(io.BytesIO(workbook_bytes), read_only=True, data_only=True)
        print(f"CONOSPERMUM_2026_WORKBOOK name={name!r} sheets={wb.sheetnames!r} bytes={len(workbook_bytes)}")
        for ws in wb.worksheets:
            rows = ws.iter_rows(values_only=True)
            first = next(rows, tuple())
            second = next(rows, tuple())
            third = next(rows, tuple())
            print(
                "CONOSPERMUM_2026_SHEET "
                f"workbook={name!r} sheet={ws.title!r} rows={ws.max_row} cols={ws.max_column} "
                f"row1={list(first)!r} row2={list(second)!r} row3={list(third)!r}"
            )
    print("CONOSPERMUM_2026_RAW_SCHEMA_GATE PASS only_genalex_schema_rows_printed")


if __name__ == "__main__":
    main()
