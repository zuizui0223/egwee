from __future__ import annotations

import csv
import io
import tempfile
import urllib.request
from pathlib import Path

from openpyxl import load_workbook

from probe_conospermum_2026_sources import DATASETS, dataset_json, find_file_payload, walk_links

TARGETS = {
    "paternity_2026": ["Paternity_dataset_unformatted.xlsx", "Seedlings_scoring_unformatted.xlsx"],
    "reproduction_2019": ["fruit_and_seed_set.csv"],
}


def item_name(item: dict) -> str:
    return str(item.get("path") or item.get("name") or item.get("fileName") or item.get("filename") or "")


def download_url(item: dict) -> str:
    for path, url in walk_links(item):
        if "download" in f"{path} {url}".lower():
            return url
    for key in ("downloadUrl", "download_url", "url"):
        value = item.get(key)
        if isinstance(value, str) and value.startswith("http") and "api/v2/files" not in value:
            return value
    file_id = item.get("id") or item.get("fileId") or item.get("file_id")
    if file_id is not None:
        return f"https://datadryad.org/api/v2/files/{file_id}/download"
    raise KeyError(f"No download route in file metadata: {item}")


def download_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "egwee-conospermum-2026-audit/1.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        payload = response.read()
    assert payload, url
    return payload


def inspect_xlsx(label: str, name: str, payload: bytes) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        path.write_bytes(payload)
        wb = load_workbook(path, read_only=True, data_only=True)
        print(f"CONO2026_XLSX label={label!r} name={name!r} sheets={wb.sheetnames!r} bytes={len(payload)}")
        for ws in wb.worksheets:
            print(f"CONO2026_SHEET name={ws.title!r} rows={ws.max_row} cols={ws.max_column}")
            for i, row in enumerate(ws.iter_rows(values_only=True), start=1):
                if i > 8:
                    break
                values = ["" if v is None else str(v) for v in row[:24]]
                print(f"CONO2026_PREVIEW file={name!r} sheet={ws.title!r} row={i} values={values!r}")


def inspect_csv(label: str, name: str, payload: bytes) -> None:
    text = payload.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)
    fields = reader.fieldnames or []
    print(f"CONO2026_CSV label={label!r} name={name!r} rows={len(rows)} fields={fields!r}")
    for row in rows[:5]:
        print(f"CONO2026_CSV_PREVIEW name={name!r} row={row!r}")

    exposure_fields = [
        field for field in fields
        if any(token in field.lower() for token in ("connect", "isolat", "area", "size", "population", "display"))
    ]
    print(f"CONO2026_EXPOSURE_FIELDS name={name!r} fields={exposure_fields!r}")
    for field in exposure_fields:
        values = sorted({str(r.get(field, "")).strip() for r in rows if str(r.get(field, "")).strip()})
        print(f"CONO2026_FIELD_VALUES field={field!r} n_unique={len(values)} sample={values[:30]!r}")


def main() -> None:
    for label, targets in TARGETS.items():
        _, dataset = dataset_json(DATASETS[label])
        files = find_file_payload(dataset)
        by_name = {item_name(item): item for item in files}
        for target in targets:
            assert target in by_name, (label, target, sorted(by_name))
            item = by_name[target]
            url = download_url(item)
            payload = download_bytes(url)
            print(f"CONO2026_DOWNLOAD label={label!r} name={target!r} url={url!r} bytes={len(payload)}")
            if target.lower().endswith(".xlsx"):
                inspect_xlsx(label, target, payload)
            elif target.lower().endswith(".csv"):
                inspect_csv(label, target, payload)
            else:
                raise AssertionError(target)

    print("CONOSPERMUM_2026_SOURCE_INSPECTION PASS")


if __name__ == "__main__":
    main()
