from __future__ import annotations

import csv
import io
import tempfile
import urllib.request
import zipfile
from pathlib import Path

from openpyxl import load_workbook

from probe_conospermum_2026_sources import DATASETS, dataset_url

TARGETS = {
    "paternity_2026": ["Paternity_dataset_unformatted.xlsx", "Seedlings_scoring_unformatted.xlsx"],
    "reproduction_2019": ["fruit_and_seed_set.csv"],
}


def download_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "egwee-conospermum-2026-audit/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response:
        payload = response.read()
    assert payload, url
    return payload


def archive_members(doi: str) -> dict[str, bytes]:
    # The Dryad public full-dataset relation returns a ZIP. This avoids a second
    # API metadata walk and avoids the authenticated per-file API download route.
    url = dataset_url(doi) + "/download"
    payload = download_bytes(url)
    assert payload[:2] == b"PK", (url, payload[:16])
    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        names = zf.namelist()
        print(f"CONO2026_ARCHIVE doi={doi!r} url={url!r} bytes={len(payload)} members={names!r}")
        out: dict[str, bytes] = {}
        for member in names:
            base = Path(member).name
            if base:
                out[base] = zf.read(member)
        return out


def inspect_xlsx(label: str, name: str, payload: bytes) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        path.write_bytes(payload)
        wb = load_workbook(path, read_only=True, data_only=True)
        print(f"CONO2026_XLSX label={label!r} name={name!r} sheets={wb.sheetnames!r} bytes={len(payload)}")
        for ws in wb.worksheets:
            print(f"CONO2026_SHEET file={name!r} name={ws.title!r} rows={ws.max_row} cols={ws.max_column}")
            for i, row in enumerate(ws.iter_rows(values_only=True), start=1):
                if i > 10:
                    break
                values = ["" if v is None else str(v) for v in row[:32]]
                print(f"CONO2026_PREVIEW file={name!r} sheet={ws.title!r} row={i} values={values!r}")


def inspect_csv(label: str, name: str, payload: bytes) -> None:
    text = payload.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)
    fields = reader.fieldnames or []
    print(f"CONO2026_CSV label={label!r} name={name!r} rows={len(rows)} fields={fields!r}")
    for row in rows[:8]:
        print(f"CONO2026_CSV_PREVIEW name={name!r} row={row!r}")

    exposure_fields = [
        field for field in fields
        if any(token in field.lower() for token in ("connect", "isolat", "area", "size", "population", "display"))
    ]
    print(f"CONO2026_EXPOSURE_FIELDS name={name!r} fields={exposure_fields!r}")
    for field in exposure_fields:
        values = sorted({str(r.get(field, "")).strip() for r in rows if str(r.get(field, "")).strip()})
        print(f"CONO2026_FIELD_VALUES field={field!r} n_unique={len(values)} sample={values[:40]!r}")

    # The earlier study must expose a population identity plus a non-outcome
    # fragmentation/connectivity field to qualify as an exposure provenance route.
    population_fields = [f for f in fields if "pop" in f.lower()]
    connectivity_fields = [f for f in fields if any(t in f.lower() for t in ("connect", "isolat"))]
    print(
        f"CONO2026_EXPOSURE_SCHEMA population_fields={population_fields!r} "
        f"connectivity_fields={connectivity_fields!r}"
    )
    assert population_fields, fields
    assert connectivity_fields, fields


def main() -> None:
    for label, doi in DATASETS.items():
        members = archive_members(doi)
        targets = TARGETS[label]
        for target in targets:
            assert target in members, (label, target, sorted(members))
            payload = members[target]
            print(f"CONO2026_ARCHIVE_FILE label={label!r} name={target!r} bytes={len(payload)}")
            if target.lower().endswith(".xlsx"):
                inspect_xlsx(label, target, payload)
            elif target.lower().endswith(".csv"):
                inspect_csv(label, target, payload)
            else:
                raise AssertionError(target)

    print("CONOSPERMUM_2026_SOURCE_INSPECTION PASS")


if __name__ == "__main__":
    main()
