from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

SOURCE_FRAME = "SF06"
SOURCE_ARTICLE_DOI = "10.1093/aob/mcae076"
NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
RESPONSES = ("Female fitness", "Male fitness", "Pollination")


def q(tag: str) -> str:
    return f"{{{NS}}}{tag}"


def cell_text(cell: ET.Element) -> str:
    text = " ".join(
        (t.text or "").strip()
        for t in cell.iter(q("t"))
        if (t.text or "").strip()
    )
    return " ".join(text.split())


def strip_variance_from_source(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^(?:NA|N/?A)\s+", "", text, flags=re.I)
    text = re.sub(r"^[−–-]?\s*\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?\s+", "", text)
    return text.strip()


def parse_row(cells: list[str]) -> dict[str, str]:
    assert len(cells) >= 11, cells
    metadata = cells[:-2]
    species = metadata[0].strip()
    country = metadata[-1].strip()
    source = strip_variance_from_source(cells[-1])
    assert species and source, cells

    response = None
    response_idx = None
    family = ""
    for idx, value in enumerate(metadata[1:-1], start=1):
        for candidate in RESPONSES:
            if candidate.casefold() in value.casefold():
                response = candidate
                response_idx = idx
                lower = value.casefold()
                pos = lower.find(candidate.casefold())
                prefix = value[:pos].strip()
                if prefix:
                    family = prefix
                elif idx > 1:
                    family = metadata[idx - 1].strip()
                break
        if response is not None:
            break
    assert response is not None and response_idx is not None, cells

    land_use_idx = response_idx + 1
    land_use = metadata[land_use_idx].strip()
    trait_cells = [x.strip() for x in metadata[land_use_idx + 1 : -1] if x.strip()]
    assert len(trait_cells) >= 4, (cells, trait_cells)

    compatibility = trait_cells[0]
    sexual_expression = trait_cells[1]
    life_form = trait_cells[-2]
    ecosystem_type = trait_cells[-1]
    pollination_context = "; ".join(trait_cells[2:-2])

    # When Family and response are separate cells, keep the preceding family cell.
    if not family and response_idx >= 2:
        family = metadata[response_idx - 1].strip()
    assert family, cells

    return {
        "species": species,
        "family": family,
        "response": response,
        "land_use_factor": land_use,
        "compatibility": compatibility,
        "sexual_expression": sexual_expression,
        "pollination_context": pollination_context,
        "life_form": life_form,
        "ecosystem_type": ecosystem_type,
        "country": country,
        "source_publication": source,
    }


def uniq(rows: list[dict[str, str]], field: str) -> str:
    out = []
    seen = set()
    for row in rows:
        value = row[field].strip()
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return "; ".join(out)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_phase2_sf06_study_universe.py INPUT.docx OUTPUT_DIR")
    source = Path(sys.argv[1])
    outdir = Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(source) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    tables = root.findall(".//" + q("tbl"))
    assert len(tables) == 7, len(tables)

    parsed = []
    for table in tables[1:]:
        for row in table.findall("./" + q("tr")):
            cells = [cell_text(c) for c in row.findall("./" + q("tc"))]
            if not any(cells):
                continue
            parsed.append(parse_row(cells))

    assert len(parsed) == 426, len(parsed)
    response_counts = Counter(r["response"] for r in parsed)

    by_pub: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in parsed:
        key = " ".join(row["source_publication"].casefold().split())
        by_pub[key].append(row)

    output = []
    species_all = set()
    for i, (_, rows) in enumerate(sorted(by_pub.items(), key=lambda kv: kv[0]), start=1):
        for row in rows:
            species_all.add(row["species"].casefold())
        output.append({
            "source_frame": SOURCE_FRAME,
            "sf06_publication_id": f"SF06P{i:03d}",
            "source_publication": rows[0]["source_publication"],
            "n_source_rows": str(len(rows)),
            "responses": "; ".join(sorted({r["response"] for r in rows})),
            "n_species": str(len({r["species"].casefold() for r in rows})),
            "species": uniq(rows, "species"),
            "families": uniq(rows, "family"),
            "land_use_factors": uniq(rows, "land_use_factor"),
            "compatibility_systems": uniq(rows, "compatibility"),
            "sexual_expressions": uniq(rows, "sexual_expression"),
            "pollination_contexts": uniq(rows, "pollination_context"),
            "life_forms": uniq(rows, "life_form"),
            "ecosystem_types": uniq(rows, "ecosystem_type"),
            "countries": uniq(rows, "country"),
            "multilayer_screen_status": "pending_title_abstract_methods_screen",
            "screening_note": (
                "DOCX source identity/trait metadata materialized before new numerical EGWEE effects; "
                "Hedges-d and V(d) cells were parsed only as excluded positions and are not stored."
            ),
            "outcome_opened": "no",
        })

    out_csv = outdir / "phase2_sf06_publication_universe_v1.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)

    summary = {
        "source_frame": SOURCE_FRAME,
        "source_article_doi": SOURCE_ARTICLE_DOI,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "docx_tables": len(tables),
        "materialized": {
            "source_effect_rows": len(parsed),
            "deduplicated_source_publications": len(output),
            "unique_species": len(species_all),
            "response_row_counts": dict(response_counts),
        },
        "outcome_fields_materialized": False,
        "excluded_source_fields": ["Hedges_d", "V(d)"],
        "publication_universe_file": out_csv.name,
        "completion_status": "publication_rows_materialized_screening_pending",
    }
    (outdir / "phase2_sf06_source_frame_summary_v1.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    status = f"""# Phase-2 SF06 materialization — 2026-09-20

## Result

SF06 (Aguilar et al. 2024 online / 2025 volume; doi:{SOURCE_ARTICLE_DOI}) has
been row-materialized from public Supplementary Table S1.

The source DOCX contains:

- source effect rows: **{len(parsed)}**;
- deduplicated source publications: **{len(output)}**;
- unique plant species represented: **{len(species_all)}**;
- female-fitness rows: **{response_counts.get('Female fitness', 0)}**;
- male-fitness rows: **{response_counts.get('Male fitness', 0)}**;
- pollination rows: **{response_counts.get('Pollination', 0)}**.

## Outcome-blind firewall

The Phase-2 publication universe retains publication identity, species, family,
response family, land-use factor and ecological/life-history metadata.

The numerical source-result cells `Hedges' d` and `V(d)` are deliberately
excluded from the materialized ledger. No new EGWEE effect magnitude is opened.

## Next operation

Screen and crosswalk the source publications for repeated same-system I/F/C
programmes and duplicates with SF01-SF05, SF07 and the existing EGWEE registry
before any new numerical extraction.
"""
    rootdir = outdir.parent.parent
    (rootdir / "manuscript" / "PHASE2_SF06_MATERIALIZATION_2026-09-20.md").write_text(
        status, encoding="utf-8"
    )

    print(
        "PHASE2_SF06_MATERIALIZED "
        f"rows={len(parsed)} publications={len(output)} species={len(species_all)} "
        f"female={response_counts.get('Female fitness',0)} "
        f"male={response_counts.get('Male fitness',0)} "
        f"pollination={response_counts.get('Pollination',0)} outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
