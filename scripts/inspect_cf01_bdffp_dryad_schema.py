from __future__ import annotations

import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "evidence/meta_extraction/phase2_cf01_bdffp_dryad_schema_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF01_BDFFP_DRYAD_SCHEMA_2026-09-24.md"

EXPECTED = {
    "density.rich.data.xlsx",
    "dispersed.matrix.xlsx",
    "functional.diversity.xlsx",
    "undispersed.matrix.xlsx",
}

STRUCTURAL_TERMS = (
    "plot", "site", "fragment", "size", "ranch", "forest", "treatment",
    "habitat", "class", "area", "control",
)
RESPONSE_TERMS = (
    "dispers", "undispers", "density", "seed", "rich", "divers", "abund",
)


def basename(name: str) -> str:
    return name.rstrip("/").split("/")[-1]


def workbook_schema(raw: bytes) -> dict:
    wb = load_workbook(io.BytesIO(raw), read_only=True, data_only=False)
    sheets = []
    for ws in wb.worksheets:
        first = next(ws.iter_rows(min_row=1, max_row=1, values_only=True), ())
        columns = ["" if x is None else str(x).strip() for x in first]
        structural = [
            c for c in columns if c and any(t in c.casefold() for t in STRUCTURAL_TERMS)
        ]
        response = [
            c for c in columns if c and any(t in c.casefold() for t in RESPONSE_TERMS)
        ]

        # Exposure/unit values are structural metadata, not biological outcomes.
        # Record only unique values from structural columns and never inspect
        # response cells in this schema gate.
        structural_values: dict[str, list[str]] = {}
        col_index = {c: i for i, c in enumerate(columns)}
        if structural:
            found = {c: set() for c in structural}
            for row in ws.iter_rows(min_row=2, values_only=True):
                for c in structural:
                    i = col_index[c]
                    if i < len(row) and row[i] is not None:
                        found[c].add(str(row[i]).strip())
            structural_values = {
                c: sorted(vals)[:100] for c, vals in found.items()
            }

        sheets.append(
            {
                "sheet": ws.title,
                "max_row": ws.max_row,
                "max_column": ws.max_column,
                "columns": columns,
                "structural_columns": structural,
                "response_columns": response,
                "structural_values": structural_values,
            }
        )
    return {"sheets": sheets}


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: inspect_cf01_bdffp_dryad_schema.py DATASET.zip")
    archive = Path(sys.argv[1])
    assert archive.is_file(), archive

    with zipfile.ZipFile(archive) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        by_base = {basename(n): n for n in names}
        missing = sorted(EXPECTED - set(by_base))
        assert not missing, missing

        files = {}
        for short in sorted(EXPECTED):
            raw = zf.read(by_base[short])
            files[short] = {
                "path": by_base[short],
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "schema": workbook_schema(raw),
            }

    schema_text = json.dumps(files, ensure_ascii=False).casefold()
    dispersed_hint = "dispers" in schema_text
    undispersed_hint = "undispers" in schema_text
    plot_hint = "plot" in schema_text
    fragment_hint = "fragment" in schema_text or "size" in schema_text

    result = {
        "schema_version": 1,
        "candidate": "CFTQ0065",
        "programme_id": "P2_CF01_BDFFP_SEED_RAIN_2020",
        "dataset_doi": "10.5061/dryad.612jm640h",
        "article_doi": "10.1002/eap.2093",
        "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
        "archive_bytes": archive.stat().st_size,
        "archive_file_count": len(names),
        "expected_files_present": True,
        "files": files,
        "schema_hints": {
            "plot_identifier_present": plot_hint,
            "fragment_exposure_present": fragment_hint,
            "dispersed_seed_endpoint_present": dispersed_hint,
            "undispersed_seed_endpoint_present": undispersed_hint,
        },
        "effect_outcomes_opened": False,
        "numeric_effects_calculated": False,
        "next_gate": (
            "verify the eleven source plots and common dispersed/undispersed density frame, "
            "then execute the frozen direct C-F recovery contract"
        ),
    }

    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# CFTQ0065 BDFFP Dryad schema gate — 2026-09-24",
        "",
        "## Source",
        "",
        "- article: doi:10.1002/eap.2093",
        "- public data: doi:10.5061/dryad.612jm640h",
        "- recovery contract: `CF01_BDFFP_SEED_RAIN_2020_RECOVERY_CONTRACT.md`",
        "",
        "This gate inspects workbook structure and exposure/unit identifiers only. It does not",
        "calculate or summarize biological response values.",
        "",
        "## Archive result",
        "",
        f"- archive bytes: **{archive.stat().st_size}**",
        f"- files found: **{len(names)}**",
        "- all four declared Dryad workbooks present: **yes**",
        f"- plot identifier hint present: **{'yes' if plot_hint else 'no'}**",
        f"- fragment exposure hint present: **{'yes' if fragment_hint else 'no'}**",
        f"- dispersed-seed endpoint hint present: **{'yes' if dispersed_hint else 'no'}**",
        f"- undispersed-seed endpoint hint present: **{'yes' if undispersed_hint else 'no'}**",
        "- numerical EGWEE effect calculation opened: **false**",
        "",
        "## Workbook schemas",
        "",
    ]
    for short in sorted(files):
        lines.append(f"### {short}")
        lines.append("")
        for sheet in files[short]["schema"]["sheets"]:
            lines.append(
                f"- sheet `{sheet['sheet']}`: rows={sheet['max_row']}; "
                f"columns={', '.join(sheet['columns'])}"
            )
            if sheet["structural_columns"]:
                lines.append(
                    "- structural columns: " + ", ".join(sheet["structural_columns"])
                )
        lines.append("")

    lines += [
        "## Gate",
        "",
        "Proceed to numerical recovery only if the public workbooks support all of:",
        "",
        "1. exactly the source plot frame can be reconstructed without using traps as n;",
        "2. fragment/control status is joined before opening endpoint values;",
        "3. dispersed and undispersed density are available on the same plot frame;",
        "4. the frozen all-fragment-versus-continuous contrast can be calculated without",
        "   selecting fragment sizes or response subsets from outcomes.",
        "",
        "Otherwise retain the programme as design-valid but quantitatively blocked.",
        "",
    ]
    STATUS.write_text("\n".join(lines), encoding="utf-8")

    print(
        "PHASE2_CF01_BDFFP_DRYAD_SCHEMA_OK "
        f"files={len(names)} plot_hint={str(plot_hint).lower()} "
        f"fragment_hint={str(fragment_hint).lower()} "
        f"dispersed_hint={str(dispersed_hint).lower()} "
        f"undispersed_hint={str(undispersed_hint).lower()} "
        "effects_opened=false"
    )


if __name__ == "__main__":
    main()
