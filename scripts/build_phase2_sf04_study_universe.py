from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SOURCE_FRAME = "SF04"
SOURCE_ARTICLE_DOI = "10.1111/cobi.13422"
FIGSHARE_DOI = "10.6084/m9.figshare.7520456.v1"

META_FIELDS = [
    "Species",
    "Method",
    "Disturbance",
    "Latitude",
    "Lifeform",
    "Lifespan",
    "Rep_system",
    "Origin",
]
OUTCOME_FIELDS = ["Xe", "Se", "Ne", "Xc", "Sc", "Nc"]


def read_csv(path: Path, ref_field: str) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames is not None
        fields = set(reader.fieldnames)
        required = {"ID", ref_field, *META_FIELDS, *OUTCOME_FIELDS}
        missing = required - fields
        assert not missing, (path, sorted(missing), reader.fieldnames)
        rows = []
        for row in reader:
            clean = {k: (v or "").strip() for k, v in row.items()}
            clean["Ref"] = clean[ref_field]
            rows.append(clean)
        return rows


def parse_references(path: Path) -> dict[int, str]:
    text = path.read_text(encoding="utf-8-sig").replace("\r", "\n")
    # Normalize line breaks to semicolons; some source lines contain several numbered refs.
    flat = re.sub(r"\s*\n\s*", "; ", text)
    matches = list(re.finditer(r"(?<!\d)(\d{1,2})\s*=\s*", flat))
    refs: dict[int, str] = {}
    for i, m in enumerate(matches):
        number = int(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(flat)
        citation = flat[start:end].strip(" ;")
        if citation:
            refs[number] = " ".join(citation.split())
    assert len(refs) == 38, refs
    assert set(refs) == set(range(1, 39)), sorted(refs)
    return refs


def uniq(rows: list[dict[str, str]], field: str) -> str:
    values = []
    seen = set()
    for row in rows:
        v = row[field].strip()
        if v and v not in seen:
            seen.add(v)
            values.append(v)
    return "; ".join(values)


def main() -> None:
    if len(sys.argv) != 6:
        raise SystemExit(
            "usage: build_phase2_sf04_study_universe.py "
            "ALLELIC.csv HE.csv REFERENCES.txt README.txt OUTPUT_DIR"
        )

    allelic_path = Path(sys.argv[1])
    he_path = Path(sys.argv[2])
    refs_path = Path(sys.argv[3])
    readme_path = Path(sys.argv[4])
    outdir = Path(sys.argv[5])
    outdir.mkdir(parents=True, exist_ok=True)

    allelic = read_csv(allelic_path, "Ref")
    he = read_csv(he_path, "Ref_ID")
    refs = parse_references(refs_path)
    assert readme_path.is_file() and readme_path.stat().st_size > 0

    tagged = [
        *[{"stream": "allelic_richness", **r} for r in allelic],
        *[{"stream": "expected_heterozygosity", **r} for r in he],
    ]

    by_ref: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in tagged:
        ref = int(float(row["Ref"]))
        assert ref in refs, (ref, row)
        by_ref[ref].append(row)

    assert set(by_ref) == set(refs), (sorted(by_ref), sorted(refs))

    output = []
    all_species = set()
    for ref in sorted(by_ref):
        rows = by_ref[ref]
        species = []
        seen_species = set()
        for row in rows:
            sp = row["Species"].strip()
            key = sp.casefold()
            if sp and key not in seen_species:
                seen_species.add(key)
                species.append(sp)
                all_species.add(key)
        output.append({
            "source_frame": SOURCE_FRAME,
            "sf04_reference_id": f"SF04R{ref:02d}",
            "source_reference_number": str(ref),
            "source_publication": refs[ref],
            "streams": ";".join(sorted({r["stream"] for r in rows})),
            "n_source_case_rows": str(len(rows)),
            "n_species": str(len(species)),
            "species": "; ".join(species),
            "methods": uniq(rows, "Method"),
            "disturbances": uniq(rows, "Disturbance"),
            "latitudes": uniq(rows, "Latitude"),
            "lifeforms": uniq(rows, "Lifeform"),
            "lifespans": uniq(rows, "Lifespan"),
            "reproductive_systems": uniq(rows, "Rep_system"),
            "origins": uniq(rows, "Origin"),
            "multilayer_screen_status": "pending_title_abstract_methods_screen",
            "screening_note": (
                "Figshare publication/species metadata materialized before new EGWEE numerical "
                "effects; treatment/control means, SDs and sample sizes were excluded."
            ),
            "outcome_opened": "no",
        })

    out_csv = outdir / "phase2_sf04_publication_universe_v1.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)

    summary = {
        "source_frame": SOURCE_FRAME,
        "source_article_doi": SOURCE_ARTICLE_DOI,
        "figshare_doi": FIGSHARE_DOI,
        "source_files": {
            allelic_path.name: {
                "sha256": hashlib.sha256(allelic_path.read_bytes()).hexdigest(),
                "case_rows": len(allelic),
            },
            he_path.name: {
                "sha256": hashlib.sha256(he_path.read_bytes()).hexdigest(),
                "case_rows": len(he),
            },
            refs_path.name: {
                "sha256": hashlib.sha256(refs_path.read_bytes()).hexdigest(),
                "references": len(refs),
            },
            readme_path.name: {
                "sha256": hashlib.sha256(readme_path.read_bytes()).hexdigest(),
            },
        },
        "materialized": {
            "deduplicated_source_publications": len(output),
            "unique_species": len(all_species),
            "total_source_case_rows": len(tagged),
            "allelic_case_rows": len(allelic),
            "heterozygosity_case_rows": len(he),
        },
        "outcome_fields_materialized": False,
        "excluded_source_columns": OUTCOME_FIELDS,
        "publication_universe_file": out_csv.name,
        "completion_status": "publication_rows_materialized_screening_pending",
    }
    (outdir / "phase2_sf04_source_frame_summary_v1.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    status = f"""# Phase-2 SF04 materialization — 2026-09-20

## Result

SF04 (González et al. 2019; doi:{SOURCE_ARTICLE_DOI}) has been row-materialized
from the public Figshare dataset `{FIGSHARE_DOI}`.

The public files contain:

- allelic-richness case rows: **{len(allelic)}**;
- expected-heterozygosity case rows: **{len(he)}**;
- total source case rows: **{len(tagged)}**;
- deduplicated source publications: **{len(output)}**;
- unique plant species represented: **{len(all_species)}**.

All **38** references in `references.txt` are represented in the materialized
case files.

## Outcome-blind firewall

The publication universe retains only source identity and prespecified screening
metadata:

- species;
- molecular method;
- disturbance class;
- latitude;
- life form;
- lifespan;
- reproductive system;
- origin;
- whether the source appears in allelic-richness, expected-heterozygosity, or both streams.

It deliberately excludes all treatment/control outcome columns:

- `Xe`, `Se`, `Ne`;
- `Xc`, `Sc`, `Nc`.

No new EGWEE effect magnitude is opened by this operation.

## Next operation

Screen the 38 source publications by title/abstract/methods for same-system
`G_adult` overlap with contemporary process/function layers, crosswalk duplicates
against SF01-SF07 and existing EGWEE programme IDs, and only then open numerical
effects for candidates that pass the fixed independent-unit and exposure gates.
"""
    root = outdir.parent.parent
    (root / "manuscript" / "PHASE2_SF04_MATERIALIZATION_2026-09-20.md").write_text(
        status,
        encoding="utf-8",
    )

    print(
        "PHASE2_SF04_MATERIALIZED "
        f"publications={len(output)} species={len(all_species)} "
        f"case_rows={len(tagged)} outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
