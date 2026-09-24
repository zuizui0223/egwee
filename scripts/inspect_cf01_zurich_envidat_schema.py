from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_envidat_schema_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF01_ZURICH_ENVIDAT_SCHEMA_2026-09-24.md"
EXPOSURE = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_exposure_audit_v1.json"

EXPECTED_SUFFIXES = {
    "data_description.xlsx",
    "protocol_english.pdf",
    "protocol_german.pdf",
    "garden_site_coordinates.csv",
    "taxa_checklist.csv",
    "raw_sampling_data.xlsx",
    "individual_traits.csv",
    "species_temporal_flower_visitation_matrix.csv",
    "daucus_carota_seed_set.csv",
    "onobrychis_viciifolia_fruit_set.csv",
    "raphanus_sativus_fruit_set.csv",
    "raphanus_sativus_seed_set.csv",
    "symphytum_officinale_fruit_set.csv",
    "symphytum_officinale_seed_set.csv",
    "figure_1.R",
    "figure_2.R",
    "figure_3.R",
    "figure_4.R",
    "table_2.R",
    "README.txt",
}


def basename(name: str) -> str:
    return name.rstrip("/").split("/")[-1]


def csv_schema(zf: zipfile.ZipFile, name: str) -> dict:
    raw = zf.read(name)
    text = raw.decode("utf-8-sig", errors="replace")
    reader = csv.reader(io.StringIO(text))
    try:
        header = next(reader)
    except StopIteration:
        header = []
    n_rows = sum(1 for _ in reader)
    return {
        "path": name,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "columns": header,
        "data_rows": n_rows,
    }


def xlsx_schema(zf: zipfile.ZipFile, name: str) -> dict:
    raw = zf.read(name)
    wb = load_workbook(io.BytesIO(raw), read_only=True, data_only=False)
    sheets = []
    for ws in wb.worksheets:
        first = next(ws.iter_rows(min_row=1, max_row=1, values_only=True), ())
        columns = [str(x).strip() if x is not None else "" for x in first]
        sheets.append({
            "sheet": ws.title,
            "max_row": ws.max_row,
            "max_column": ws.max_column,
            "columns": columns,
        })
    return {
        "path": name,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "sheets": sheets,
    }



def workbook_text(zf: zipfile.ZipFile, name: str) -> str:
    raw = zf.read(name)
    wb = load_workbook(io.BytesIO(raw), read_only=True, data_only=False)
    values = []
    for ws in wb.worksheets:
        values.append(f"SHEET {ws.title}")
        for row in ws.iter_rows(values_only=True):
            vals = [str(x) for x in row if x is not None]
            if vals:
                values.append(" | ".join(vals))
    return "\n".join(values)


def text_resource(zf: zipfile.ZipFile, name: str) -> str:
    return zf.read(name).decode("utf-8-sig", errors="replace")


def term_hits(text: str, terms: tuple[str, ...]) -> dict[str, list[str]]:
    lines = text.splitlines()
    out: dict[str, list[str]] = {}
    for term in terms:
        matches = [line.strip() for line in lines if term.casefold() in line.casefold()]
        if matches:
            out[term] = matches[:25]
    return out


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: inspect_cf01_zurich_envidat_schema.py DATASET.zip")
    path = Path(sys.argv[1])
    assert path.is_file(), path

    with zipfile.ZipFile(path) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        base = {basename(n): n for n in names}
        missing = sorted(EXPECTED_SUFFIXES - set(base))
        assert not missing, missing

        csv_files = {}
        for short in sorted(x for x in EXPECTED_SUFFIXES if x.endswith(".csv")):
            csv_files[short] = csv_schema(zf, base[short])

        xlsx_files = {}
        for short in ("data_description.xlsx", "raw_sampling_data.xlsx"):
            xlsx_files[short] = xlsx_schema(zf, base[short])

        readme = text_resource(zf, base["README.txt"])
        data_description_text = workbook_text(zf, base["data_description.xlsx"])
        raw_workbook_text = workbook_text(zf, base["raw_sampling_data.xlsx"])
        r_script_text = "\n\n".join(
            f"FILE {short}\n" + text_resource(zf, base[short])
            for short in sorted(x for x in EXPECTED_SUFFIXES if x.endswith(".R"))
        )

    response_tokens = ("visit", "pollin", "seed", "fruit")
    schema_text = json.dumps({"csv": csv_files, "xlsx": xlsx_files}, ensure_ascii=False).lower()
    corpus = "\n".join([schema_text, readme, data_description_text, raw_workbook_text, r_script_text])
    exposure_schema_hint = "garden" in corpus.casefold()
    exposure_terms = (
        "impervious", "sealed", "built", "urban intensity", "urbanisation", "urbanization",
        "500 m", "500m", "radius", "land cover", "landcover", "habitat loss",
    )
    exposure_hits = term_hits(corpus, exposure_terms)
    has_impervious_hint = "impervious" in exposure_hits
    response_schema_hint = any(tok in schema_text for tok in response_tokens)

    summary = {
        "schema_version": 1,
        "candidate": "CFTQ0018",
        "dataset_doi": "10.16904/envidat.676",
        "article_doi": "10.1016/j.dib.2025.112013",
        "archive_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "archive_bytes": path.stat().st_size,
        "file_count": len(names),
        "expected_files_present": True,
        "csv_files": csv_files,
        "xlsx_files": xlsx_files,
        "schema_hints": {
            "garden_identifier_or_context_present": exposure_schema_hint,
            "impervious_surface_term_present": has_impervious_hint,
            "pollination_or_reproductive_response_terms_present": response_schema_hint,
        },
        "exposure_term_hits": exposure_hits,
        "numeric_outcome_summaries_calculated": False,
        "effect_outcomes_opened": False,
        "next_gate": (
            "identify exact garden key and 500m impervious-surface field, then verify that visitation "
            "and species seed/fruit records join at garden level before opening response values"
        ),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    raw_sheets = xlsx_files["raw_sampling_data.xlsx"]["sheets"]
    exposure_audit = {
        "candidate": "CFTQ0018",
        "dataset_doi": "10.16904/envidat.676",
        "searched_resources": [
            "README.txt",
            "data_description.xlsx (all cells)",
            "raw_sampling_data.xlsx (all cells)",
            "figure_1.R", "figure_2.R", "figure_3.R", "figure_4.R", "table_2.R",
            "all CSV/XLSX schema field names",
        ],
        "searched_terms": list(exposure_terms),
        "term_hits": exposure_hits,
        "impervious_surface_field_found": has_impervious_hint,
        "effect_outcomes_opened": False,
        "decision": (
            "exposure_present_in_archive_schema_or_code"
            if has_impervious_hint
            else "article_exposure_not_materialized_in_this_archive"
        ),
    }
    EXPOSURE.write_text(
        json.dumps(exposure_audit, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    STATUS.write_text(
        f"""# CFTQ0018 Zurich EnviDat schema gate — 2026-09-24

## Source

Open EnviDat dataset: doi:10.16904/envidat.676, linked to Reji Chacko et al. (2025),
doi:10.1016/j.dib.2025.112013.

The archive is inspected at schema level only before numerical response extraction.

## Archive result

- archive bytes: **{path.stat().st_size}**
- files found: **{len(names)}**
- all expected repository files present: **yes**
- raw field workbook sheets: **{len(raw_sheets)}**
- explicit impervious-surface term found in schema/README: **{"yes" if has_impervious_hint else "no"}**
- pollination/reproductive response terms found in schema: **{"yes" if response_schema_hint else "no"}**

The repository contains separate site, raw field, visitation/trait, and six species-level
seed/fruit-set files. No response means, effect directions, correlations, p-values, or
fragmentation effects were calculated in this gate.

## Admission question

The next gate is structural:

1. identify the exact garden identifier shared across exposure, visitation and reproductive files;
2. identify the source 500-m impervious-surface field;
3. verify that each candidate species has a common garden frame for I and F;
4. keep garden as the independent landscape unit;
5. only then freeze one I endpoint and one F endpoint before calculating a gradient effect.

If impervious exposure cannot be joined at garden level, CFTQ0018 remains descriptive rather than
being rescued with another urbanisation variable.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF01_ZURICH_SCHEMA_OK "
        f"files={len(names)} raw_sheets={len(raw_sheets)} "
        f"impervious_hint={has_impervious_hint} response_hint={response_schema_hint} "
        "outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
