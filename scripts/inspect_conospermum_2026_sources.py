from __future__ import annotations

import csv
import io
import subprocess
import tempfile
from pathlib import Path

from openpyxl import load_workbook

# File IDs are locked to the source versions qualified by
# probe_conospermum_2026_sources.py:
#   PS011 Dryad version 436023 (v3)
#   2019 exposure-provenance Dryad version 32609 (v1)
PUBLIC_FILES = {
    "paternity_2026": {
        "Paternity_dataset_unformatted.xlsx": 4702034,
        "Seedlings_scoring_unformatted.xlsx": 4702035,
    },
    "reproduction_2019": {
        "fruit_and_seed_set.csv": 155093,
    },
}


def download_bytes(file_id: int) -> bytes:
    url = f"https://datadryad.org/stash/downloads/file_stream/{file_id}"
    # Dryad file_stream redirects to a signed object-store URL. curl preserves
    # that redirect URL faithfully; urllib on hosted runners returned 403 after
    # the redirect even though the public file_stream route itself resolved.
    proc = subprocess.run(
        [
            "curl", "-L", "--fail", "--silent", "--show-error",
            "--retry", "3", "--retry-delay", "2",
            "-A", "Mozilla/5.0 egwee-conospermum-2026-audit/1.0",
            url,
        ],
        check=False,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"Dryad file_stream failed file_id={file_id} rc={proc.returncode} "
            f"stderr={proc.stderr.decode('utf-8', errors='replace')}"
        )
    payload = proc.stdout
    assert payload, url
    print(f"CONO2026_PUBLIC_DOWNLOAD file_id={file_id} bytes={len(payload)}")
    return payload


def inspect_xlsx(label: str, name: str, payload: bytes) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        path.write_bytes(payload)
        wb = load_workbook(path, read_only=True, data_only=True)
        print(f"CONO2026_XLSX label={label!r} name={name!r} sheets={wb.sheetnames!r} bytes={len(payload)}")
        for ws in wb.worksheets:
            print(f"CONO2026_SHEET file={name!r} name={ws.title!r} rows={ws.max_row} cols={ws.max_column}")
            for i, row in enumerate(ws.iter_rows(values_only=True), start=1):
                if i > 12:
                    break
                values = ["" if v is None else str(v) for v in row[:36]]
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

    population_fields = [f for f in fields if "pop" in f.lower()]
    connectivity_fields = [f for f in fields if any(t in f.lower() for t in ("connect", "isolat"))]
    print(
        f"CONO2026_EXPOSURE_SCHEMA population_fields={population_fields!r} "
        f"connectivity_fields={connectivity_fields!r}"
    )
    assert population_fields, fields


def main() -> None:
    for label, files in PUBLIC_FILES.items():
        for name, file_id in files.items():
            payload = download_bytes(file_id)
            if name.lower().endswith(".xlsx"):
                inspect_xlsx(label, name, payload)
            elif name.lower().endswith(".csv"):
                inspect_csv(label, name, payload)
            else:
                raise AssertionError(name)

    print("CONOSPERMUM_2026_SOURCE_INSPECTION PASS")


if __name__ == "__main__":
    main()
