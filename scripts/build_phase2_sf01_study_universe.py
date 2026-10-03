from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SOURCE_FRAME = "SF01"
SOURCE_ARTICLE_DOI = "10.1111/j.1461-0248.2006.00927.x"
DATAONE_PACKAGE = "doi:10.5063/AA/bowdish.783.5"
DATA_OBJECT = "bowdish.796.1"

REQUIRED = {
    "Species",
    "Family",
    "Hedges_d",
    "Vd",
    "CS",
    "PS",
    "LF",
    "Habitat_type",
    "Geographic_region",
    "Source publication",
}


def clean(text: str) -> str:
    return " ".join((text or "").replace("\u2021", " ").split())


def species_key(text: str) -> str:
    # Table marks pollination-process species with a double dagger.
    return re.sub(r"[‡†*]+", "", clean(text)).strip().casefold()


def publication_key(text: str) -> str:
    return clean(text).casefold()


def read_table(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise AssertionError("unable to decode SF01 source object")

    reader = csv.DictReader(text.splitlines(), delimiter="\t")
    assert reader.fieldnames is not None, "missing header"
    fieldnames = [clean(x) for x in reader.fieldnames]
    reader.fieldnames = fieldnames
    missing = REQUIRED - set(fieldnames)
    assert not missing, (sorted(missing), fieldnames)
    return [{k: clean(v or "") for k, v in row.items()} for row in reader]


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_phase2_sf01_study_universe.py INPUT.tsv OUTPUT_DIR")

    source = Path(sys.argv[1])
    outdir = Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)

    rows = read_table(source)
    assert len(rows) == 93, len(rows)

    species = {species_key(r["Species"]) for r in rows if species_key(r["Species"])}
    assert len(species) == 89, len(species)

    by_pub: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        pub = publication_key(row["Source publication"])
        assert pub, row
        by_pub[pub].append(row)

    # Main article reports 53 published articles/book chapters + one PhD thesis.
    assert len(by_pub) == 54, len(by_pub)

    publication_rows = []
    for i, (_, group) in enumerate(sorted(by_pub.items()), start=1):
        pubs = sorted({r["Source publication"] for r in group})
        assert len(pubs) == 1, pubs
        spp = []
        seen_spp = set()
        for r in group:
            s = re.sub(r"[‡†*]+", "", r["Species"]).strip()
            key = s.casefold()
            if s and key not in seen_spp:
                seen_spp.add(key)
                spp.append(s)
        families = sorted({r["Family"] for r in group if r["Family"]})
        habitats = sorted({r["Habitat_type"] for r in group if r["Habitat_type"]})
        regions = sorted({r["Geographic_region"] for r in group if r["Geographic_region"]})
        compatibility = sorted({r["CS"] for r in group if r["CS"]})
        specialization = sorted({r["PS"] for r in group if r["PS"]})
        life_forms = sorted({r["LF"] for r in group if r["LF"]})
        pollination_marked = any(("‡" in r["Species"] or "†" in r["Species"]) for r in group)

        publication_rows.append({
            "source_frame": SOURCE_FRAME,
            "sf01_publication_id": f"SF01P{i:03d}",
            "source_publication": pubs[0],
            "n_source_rows": str(len(group)),
            "n_species": str(len(spp)),
            "species": "; ".join(spp),
            "families": "; ".join(families),
            "habitat_types": "; ".join(habitats),
            "geographic_regions": "; ".join(regions),
            "compatibility_systems": "; ".join(compatibility),
            "pollination_specialization": "; ".join(specialization),
            "life_forms": "; ".join(life_forms),
            "source_marks_pollination_process_for_any_species": "yes" if pollination_marked else "no",
            "multilayer_screen_status": "pending_title_abstract_methods_screen",
            "screening_note": (
                "Publication/species metadata materialized before new numerical EGWEE effects; "
                "source Hedges_d and Vd were deliberately excluded from this ledger."
            ),
            "outcome_opened": "no",
        })

    out_csv = outdir / "phase2_sf01_publication_universe_v1.csv"
    fieldnames = list(publication_rows[0])
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(publication_rows)

    summary = {
        "source_frame": SOURCE_FRAME,
        "source_article_doi": SOURCE_ARTICLE_DOI,
        "dataone_package": DATAONE_PACKAGE,
        "data_object": DATA_OBJECT,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "source_rows": len(rows),
        "unique_species": len(species),
        "deduplicated_source_publications": len(publication_rows),
        "source_reported_publication_denominator": 54,
        "outcome_fields_materialized": False,
        "excluded_source_columns": ["Hedges_d", "Vd"],
        "publication_universe_file": out_csv.name,
        "completion_status": "publication_rows_materialized_screening_pending",
    }
    (outdir / "phase2_sf01_source_frame_summary_v1.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    status = f"""# Phase-2 SF01 materialization — 2026-09-20

## Result

SF01 (Aguilar et al. 2006) has been row-materialized from the public KNB/DataONE
copy of Supporting Table S1.

The source object contains:

- **{len(rows)}** source rows;
- **{len(species)}** unique plant species;
- **{len(publication_rows)}** deduplicated source publications/programme seeds.

These counts reproduce the article's 93 data points from 89 species and its
53 published articles/book chapters plus one PhD thesis.

## Outcome-blind materialization

The new bibliographic ledger stores:

- source publication;
- species and family identities;
- habitat and geographic metadata;
- compatibility system;
- pollination specialization;
- life form;
- whether the source table marks a species as also assessed for pollination process.

It deliberately excludes the source meta-analysis response columns:

- `Hedges_d`;
- `Vd`.

No new EGWEE effect magnitude is opened by this materialization.

## Files

- `evidence/meta_extraction/phase2_sf01_publication_universe_v1.csv`
- `evidence/meta_extraction/phase2_sf01_source_frame_summary_v1.json`

## Next operation

Screen the 54 source publications by title/abstract/methods for repeated
same-system I/F and other prespecified Phase-2 layers, then crosswalk them against
SF02-SF07 and existing EGWEE programme IDs before numerical extraction.
"""
    (ROOT := outdir.parent.parent)
    (ROOT / "manuscript" / "PHASE2_SF01_MATERIALIZATION_2026-09-20.md").write_text(
        status,
        encoding="utf-8",
    )

    print(
        "PHASE2_SF01_MATERIALIZED "
        f"rows={len(rows)} species={len(species)} publications={len(publication_rows)} "
        "outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
