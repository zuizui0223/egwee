from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

SOURCE_FRAME = "SF07"
DATASET_DOI = "10.5061/dryad.dz08kps9p"

REQUIRED = {
    "Publication",
    "Reference",
    "Title",
    "Site",
    "Exp_year",
    "Study",
    "Country",
    "Continent",
    "Climate",
    "Dominant_matrix",
    "Sampling_matrix",
    "Reported_fragment_index",
    "Fragment_index",
    "Reported_pollinators",
    "Taxonomic_group",
}

SAFE_METADATA = [
    "Publication",
    "Reference",
    "Title",
    "Site",
    "Exp_year",
    "Study",
    "Country",
    "Continent",
    "Climate",
    "Dominant_matrix",
    "Sampling_matrix",
    "Reported_fragment_index",
    "Fragment_index",
    "Reported_pollinators",
    "Taxonomic_group",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        assert reader.fieldnames is not None
        missing = REQUIRED - set(reader.fieldnames)
        assert not missing, (path, sorted(missing), reader.fieldnames)
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def norm(text: str) -> str:
    return " ".join(text.split()).casefold()


def pub_key(row: dict[str, str]) -> tuple[str, str, str]:
    publication = norm(row["Publication"])
    title = norm(row["Title"])
    reference = norm(row["Reference"])
    # Prefer stable source Publication identity; title/reference keep duplicates auditable.
    return publication, title, reference


def study_key(row: dict[str, str]) -> str:
    study = row["Study"].strip()
    if study:
        return norm(study)
    return "|".join((norm(row["Publication"]), norm(row["Exp_year"]), norm(row["Site"])))


def merge_values(rows: list[dict[str, str]], field: str) -> str:
    vals = []
    seen = set()
    for row in rows:
        value = row[field].strip()
        if value and value not in seen:
            seen.add(value)
            vals.append(value)
    return "; ".join(vals)


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: build_phase2_sf07_study_universe.py ABUNDANCE.csv RICHNESS.csv OUTPUT_DIR"
        )

    abundance_path = Path(sys.argv[1])
    richness_path = Path(sys.argv[2])
    outdir = Path(sys.argv[3])
    outdir.mkdir(parents=True, exist_ok=True)

    abundance = read_csv(abundance_path)
    richness = read_csv(richness_path)

    # The source README fixes these file-level observation counts.
    assert len(abundance) == 78, len(abundance)
    assert len(richness) == 109, len(richness)

    tagged: list[dict[str, str]] = []
    for stream, rows in (("abundance", abundance), ("richness", richness)):
        for row in rows:
            tagged.append({"stream": stream, **row})

    studies = {study_key(row) for row in tagged}
    # Dryad/source abstract declares 80 studies globally. Fail closed if the
    # materialized files do not reproduce that denominator.
    assert len(studies) == 80, len(studies)

    groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in tagged:
        groups[pub_key(row)].append(row)

    output_rows = []
    for i, (_, rows) in enumerate(sorted(groups.items(), key=lambda kv: kv[0]), start=1):
        streams = sorted({r["stream"] for r in rows})
        source_publication = merge_values(rows, "Publication")
        reference = merge_values(rows, "Reference")
        title = merge_values(rows, "Title")
        output_rows.append(
            {
                "source_frame": SOURCE_FRAME,
                "sf07_publication_id": f"SF07P{i:03d}",
                "source_publication": source_publication,
                "reference": reference,
                "title": title,
                "streams": ";".join(streams),
                "n_source_rows": str(len(rows)),
                "n_unique_studies": str(len({study_key(r) for r in rows})),
                "sites": merge_values(rows, "Site"),
                "study_years": merge_values(rows, "Exp_year"),
                "countries": merge_values(rows, "Country"),
                "continents": merge_values(rows, "Continent"),
                "climates": merge_values(rows, "Climate"),
                "dominant_matrices": merge_values(rows, "Dominant_matrix"),
                "sampling_matrices": merge_values(rows, "Sampling_matrix"),
                "reported_fragment_indices": merge_values(rows, "Reported_fragment_index"),
                "fragment_indices": merge_values(rows, "Fragment_index"),
                "reported_pollinators": merge_values(rows, "Reported_pollinators"),
                "taxonomic_groups": merge_values(rows, "Taxonomic_group"),
                "plant_linkage_screen_status": "pending_title_abstract_methods_screen",
                "plant_linkage_note": (
                    "SF07 is pollinator-only discovery evidence until an eligible flowering-plant "
                    "response is linked independently; effect sizes were not materialized."
                ),
                "outcome_opened": "no",
            }
        )

    fieldnames = list(output_rows[0])
    out_csv = outdir / "phase2_sf07_publication_universe_v1.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    manifest = {
        "source_frame": SOURCE_FRAME,
        "dataset_doi": DATASET_DOI,
        "source_files": {
            abundance_path.name: {
                "sha256": hashlib.sha256(abundance_path.read_bytes()).hexdigest(),
                "source_rows": len(abundance),
                "declared_publications": 40,
            },
            richness_path.name: {
                "sha256": hashlib.sha256(richness_path.read_bytes()).hexdigest(),
                "source_rows": len(richness),
                "declared_publications": 63,
            },
        },
        "materialized": {
            "unique_studies": len(studies),
            "deduplicated_publications": len(output_rows),
            "abundance_rows": len(abundance),
            "richness_rows": len(richness),
        },
        "outcome_fields_materialized": False,
        "excluded_source_columns": ["Sample_size", "r_effect_size"],
        "publication_universe_file": out_csv.name,
        "completion_status": "publication_rows_materialized_plant_linkage_screen_pending",
    }
    (outdir / "phase2_sf07_source_frame_summary_v1.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    status = f"""# Phase-2 SF07 row materialization — 2026-09-20

## Current state

SF07 is the Olhnuud et al. (2025) Dryad dataset
(`{DATASET_DOI}`) on insect-pollinator responses to habitat fragmentation.

The two public source files were materialized into a bibliographic discovery
universe without importing effect sizes.

- abundance source rows: **{len(abundance)}**;
- richness source rows: **{len(richness)}**;
- unique source studies across both files: **{len(studies)}**;
- deduplicated publication identities: **{len(output_rows)}**.

The source files reproduce the declared **80-study** denominator.

## Outcome-blind firewall

The Phase-2 publication universe stores publication identity, title, study site,
year, geography, climate, matrix context, fragmentation-index metadata and
pollinator taxonomy.

It deliberately does **not** materialize:

- `r_effect_size`;
- `Sample_size`.

Every SF07 publication is therefore available for title/abstract/method screening
before any source effect magnitude is used.

## EGWEE use

SF07 remains a **discovery frame**, not direct plant-response evidence.

A record can advance only if a flowering-plant response layer can be linked
independently to the same fragmentation programme without selecting on the
pollinator effect direction or magnitude. Pollinator-only records remain discovery
records and never enter an EGWEE plant layer by themselves.

## Next operation

Screen the deduplicated publication universe for explicit flowering-plant linkage,
assign programme identities, and crosswalk duplicates against SF01-SF06 and the
existing EGWEE candidate registry.
"""
    (outdir.parent.parent / "manuscript" / "PHASE2_SF07_MATERIALIZATION_2026-09-20.md").write_text(
        status,
        encoding="utf-8",
    )

    print(
        "PHASE2_SF07_MATERIALIZED "
        f"studies={len(studies)} publications={len(output_rows)} "
        f"abundance_rows={len(abundance)} richness_rows={len(richness)} outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
