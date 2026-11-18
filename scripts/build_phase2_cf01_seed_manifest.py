from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = ROOT / "evidence/meta_extraction/phase2_crossframe_publication_identity_v1.csv"
PRIMARY = ROOT / "manuscript/meta_analysis_primary_study_seed_v1.csv"
OUT = ROOT / "evidence/meta_extraction/phase2_cf01_seed_manifest_v1.csv"
SUMMARY = ROOT / "evidence/meta_extraction/phase2_cf01_seed_manifest_summary_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF01_SEED_MANIFEST_2026-09-21.md"

CUTOFF = "2026-09-18"

# Explicit identity crosswalk. These are known publication-level matches, not fuzzy joins.
PRIMARY_TO_CANONICAL = {
    "PS001": "SF06:SF06P049",
    "PS003": "duplicate:pellegrino|2015",
    "PS009": "SF06:SF06P062",
    "PS012": "SF06:SF06P210",
    "PS013": "SF05:49",
    "PS019": "SF06:SF06P137",
    "PS020": "SF06:SF06P021",
    "PS022": "SF06:SF06P007",
}

CF01_EXTRA = {
    "canonical_search_key": "CF01:P2_CF01_GPAIR_002",
    "source_origins": ["CF01_GPAIR_002"],
    "citation": (
        "Yineger, H., Schmidt, D.J., Hughes, J.M. (2014). Genetic structuring of remnant "
        "forest patches in an endangered medicinal tree in North-western Ethiopia. "
        "BMC Genetics 15:31."
    ),
    "title": (
        "Genetic structuring of remnant forest patches in an endangered medicinal tree "
        "in North-western Ethiopia"
    ),
    "year": "2014",
    "doi": "10.1186/1471-2156-15-31",
    "species": "Prunus africana",
    "existing_egwee_programmes": ["P2_CF01_GPAIR_002"],
    "identity_provenance": "independent CF01 G-pair recovery absent from materialized SF04/SF05/SF06 identities",
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def add_unique(xs: list[str], value: str) -> None:
    value = (value or "").strip()
    if value and value not in xs:
        xs.append(value)


def main() -> None:
    identity = rows(IDENTITY)
    primary = rows(PRIMARY)
    assert len(identity) == 358
    assert len({r["canonical_identity_key"] for r in identity}) == 351
    assert len(primary) == 19

    units: dict[str, dict[str, object]] = {}

    # Start with the deduplicated materialized source-frame identities.
    for r in identity:
        key = r["canonical_identity_key"]
        u = units.setdefault(key, {
            "canonical_search_key": key,
            "source_origins": [],
            "citation": "",
            "title": "",
            "year": r["year"],
            "doi": "",
            "species": [],
            "existing_egwee_programmes": [],
            "identity_provenance": "materialized SF04/SF05/SF06 cross-frame canonical identity",
        })
        add_unique(u["source_origins"], f'{r["source_frame"]}:{r["source_id"]}')
        if not u["citation"]:
            u["citation"] = r["citation"]
        if not u["doi"] and r["doi"]:
            u["doi"] = r["doi"].lower()
        for sp in (r["species"] or "").split(";"):
            add_unique(u["species"], sp)
        add_unique(u["existing_egwee_programmes"], r["existing_egwee_programme"])

    assert len(units) == 351

    crosslinked = 0
    added_primary = 0
    for r in primary:
        sid = r["study_id"]
        if sid in PRIMARY_TO_CANONICAL:
            key = PRIMARY_TO_CANONICAL[sid]
            assert key in units, (sid, key)
            crosslinked += 1
            u = units[key]
            add_unique(u["source_origins"], f"PRIMARY:{sid}")
            if not u["doi"]:
                u["doi"] = r["doi"].lower()
            if not u["title"]:
                u["title"] = r["title"]
            for sp in (r["species"] or "").split(";"):
                add_unique(u["species"], sp)
            continue

        key = f"PRIMARY:{sid}"
        assert key not in units
        units[key] = {
            "canonical_search_key": key,
            "source_origins": [f"PRIMARY:{sid}"],
            "citation": f'{r["title"]} ({r["year"]})',
            "title": r["title"],
            "year": r["year"],
            "doi": r["doi"].lower(),
            "species": [x.strip() for x in (r["species"] or "").split(";") if x.strip()],
            "existing_egwee_programmes": [],
            "identity_provenance": "eligible primary-study seed not represented in materialized SF04/SF05/SF06 identity ledger",
        }
        added_primary += 1

    assert crosslinked == 8
    assert added_primary == 11
    assert len(units) == 362

    # Add one already-declared CF01 programme that is absent from the source-frame ledger.
    key = CF01_EXTRA["canonical_search_key"]
    assert key not in units
    units[key] = {k: (v[:] if isinstance(v, list) else v) for k, v in CF01_EXTRA.items()}
    assert len(units) == 363

    out_rows = []
    for i, key in enumerate(sorted(units), start=1):
        u = units[key]
        doi = str(u["doi"]).strip().lower()
        out_rows.append({
            "cf01_seed_id": f"CF01S{i:04d}",
            "canonical_search_key": key,
            "source_origins": ";".join(u["source_origins"]),
            "citation": u["citation"],
            "title": u["title"],
            "year": u["year"],
            "doi": doi,
            "species": "; ".join(u["species"]),
            "existing_egwee_programmes": ";".join(u["existing_egwee_programmes"]),
            "identity_provenance": u["identity_provenance"],
            "bibliographic_resolution_status": "doi_present" if doi else "citation_resolution_pending",
            "backward_citation_status": "pending",
            "forward_citation_status": "pending",
            "citation_expansion_cutoff": CUTOFF,
            "screening_status": "pending_uniform_CF01_bibliographic_expansion",
            "outcome_opened": "no",
        })

    assert len(out_rows) == 363
    assert len({r["canonical_search_key"] for r in out_rows}) == 363
    assert all(r["outcome_opened"] == "no" for r in out_rows)
    n_doi = sum(bool(r["doi"]) for r in out_rows)

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0]))
        w.writeheader()
        w.writerows(out_rows)

    summary = {
        "schema_version": 1,
        "cutoff": CUTOFF,
        "materialized_crossframe_identity_units": 351,
        "primary_seed_records": 19,
        "primary_seed_crosslinked_to_crossframe": crosslinked,
        "primary_seed_added_search_units": added_primary,
        "declared_cf01_extra_search_units": 1,
        "canonical_search_units": len(out_rows),
        "search_units_with_doi": n_doi,
        "search_units_needing_citation_resolution": len(out_rows) - n_doi,
        "blocked_seed_frames_not_yet_row_materialized": ["SF01", "SF02", "SF03", "SF07"],
        "manifest_status": "partial_CF01_seed_manifest_materialized_frames_plus_declared_primary_seeds",
        "effect_outcomes_opened": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    STATUS.write_text(
        f"""# Phase-2 CF01 seed manifest — 2026-09-21

## What is frozen

A canonical citation-expansion seed manifest has now been built from every currently row-materialized SF04/SF05/SF06 publication identity plus the declared eligible primary-study seed set.

- materialized cross-frame canonical identities: **351**;
- primary-study seed records: **19**;
- primary seeds already represented in those 351 identities: **{crosslinked}**;
- primary seeds added as new search units: **{added_primary}**;
- independently recovered CF01 seed added: **1** (*Prunus africana*, Yineger et al. 2014);
- resulting canonical CF01 search units: **{len(out_rows)}**;
- units already carrying a DOI: **{n_doi}**;
- units requiring bibliographic citation resolution before expansion: **{len(out_rows)-n_doi}**.

Known cross-frame/primary duplicates are linked explicitly rather than rediscovered by fuzzy matching.

## Firewall

The manifest contains publication identity and bibliographic search metadata only.

- backward citation status: pending;
- forward citation status: pending;
- frozen cutoff: **{CUTOFF}**;
- numerical outcome fields opened: **0**.

Every search unit is retained regardless of the direction or significance of any known EGWEE result.

## Partial-frame limitation

This is a **partial CF01 seed manifest**, not a claim that the systematic frame is complete.

SF01, SF02, SF03 and SF07 remain source-verified but row-materialization blocked under the currently tested public object routes. When legitimate row-level source identities become available, they must be added to this same manifest and processed under the same citation-expansion rule.

## Next operation

Resolve the citation-only search units through one reproducible bibliographic route, then run backward/forward citation expansion uniformly for all resolvable units through the frozen 2026-09-18 cutoff. Search ranking or known result direction must not determine which seeds receive expansion.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF01_SEED_MANIFEST_OK "
        f"units={len(out_rows)} doi={n_doi} unresolved={len(out_rows)-n_doi} "
        f"primary_crosslinked={crosslinked} primary_added={added_primary} outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
