from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SF04 = ROOT / "evidence/meta_extraction/phase2_sf04_publication_universe_v1.csv"
SF05 = ROOT / "evidence/meta_extraction/phase2_sf05_primary_study_universe_v1.csv"
SF06 = ROOT / "evidence/meta_extraction/phase2_sf06_publication_universe_v1.csv"
OUT = ROOT / "evidence/meta_extraction/phase2_crossframe_publication_identity_v1.csv"
DUPS = ROOT / "evidence/meta_extraction/phase2_crossframe_candidate_duplicates_v1.csv"
SUMMARY = ROOT / "evidence/meta_extraction/phase2_crossframe_identity_summary_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CROSSFRAME_IDENTITY_LEDGER_2026-09-20.md"

EXISTING_LINKS = {
    ("SF04", "SF04R06"): "P2_CF01_GPAIR_003",
    ("SF04", "SF04R35"): "ML001",
    ("SF06", "SF06P007"): "ML020",
    ("SF06", "SF06P049"): "ML003",
    ("SF06", "SF06P138"): "P2_SF05_93",
    ("SF06", "SF06P175"): "ML001",
    ("SF05", "93"): "P2_SF05_93",
    ("SF06", "SF06P062"): "PS009_CONOSPERMUM",
    ("SF06", "SF06P210"): "ML008",
    ("SF05", "49"): "ML009_PS013",
    ("SF06", "SF06P137"): "ML015",
    ("SF06", "SF06P021"): "ML014",
}

CONFIRMED_DUPLICATE_KEYS = {
    "bartlewicz|2015",
    "browne|2015",
    "collevatti|2014",
    "giombini|2017",
    "lompo|2020",
    "pellegrino|2015",
    "zhao|2009",
}

CONFIRMED_FALSE_COLLISION_KEYS = {
    "chung|2007",
    "jacquemyn|2006",
    "jacquemyn|2009",
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def citation_author_year(citation: str, author: str = "", year: str = "") -> tuple[str, str]:
    y = year.strip()
    if not y:
        m = re.search(r"\b(?:19|20)\d{2}\b", citation or "")
        y = m.group(0) if m else ""
    a = author.strip()
    if not a:
        m = re.match(r"^([^,(]+?)(?:\s+et\s+al\.?|\s*&|\s*\()", citation or "", re.I)
        a = m.group(1) if m else ""
    a = norm(a).split(" ")[0] if norm(a) else ""
    return a, y


def species_list(text: str) -> list[str]:
    out = []
    for item in re.split(r";", text or ""):
        n = norm(item.replace("_", " "))
        if n:
            out.append(n)
    return out


def edit_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i]
        for j, cb in enumerate(b, start=1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def species_overlap(a: str, b: str) -> bool:
    aa, bb = species_list(a), species_list(b)
    for x in aa:
        for y in bb:
            if x == y or edit_distance(x, y) <= 2:
                return True
    return False


def main() -> None:
    source_rows: list[dict[str, str]] = []

    for r in rows(SF04):
        a, y = citation_author_year(r["source_publication"])
        source_rows.append({
            "source_frame": "SF04",
            "source_id": r["sf04_reference_id"],
            "citation": r["source_publication"],
            "doi": "",
            "species": r["species"],
            "author_norm": a,
            "year": y,
            "author_year_key": f"{a}|{y}" if a and y else "",
            "outcome_opened": r["outcome_opened"],
        })

    for r in rows(SF05):
        a, y = citation_author_year(r["citation"], r["first_author"], r["year"])
        source_rows.append({
            "source_frame": "SF05",
            "source_id": r["source_paper_id"],
            "citation": r["reference"] or r["citation"],
            "doi": (r["doi"] or "").strip().lower(),
            "species": r["species"],
            "author_norm": a,
            "year": y,
            "author_year_key": f"{a}|{y}" if a and y else "",
            "outcome_opened": "no",
        })

    for r in rows(SF06):
        a, y = citation_author_year(r["source_publication"])
        source_rows.append({
            "source_frame": "SF06",
            "source_id": r["sf06_publication_id"],
            "citation": r["source_publication"],
            "doi": "",
            "species": r["species"],
            "author_norm": a,
            "year": y,
            "author_year_key": f"{a}|{y}" if a and y else "",
            "outcome_opened": r["outcome_opened"],
        })

    assert len(source_rows) == 358
    assert all(r["outcome_opened"] == "no" for r in source_rows)

    by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in source_rows:
        if r["author_year_key"]:
            by_key[r["author_year_key"]].append(r)

    candidate_groups: dict[str, list[dict[str, str]]] = {}
    for key, rr in by_key.items():
        if len({r["source_frame"] for r in rr}) > 1:
            candidate_groups[key] = rr

    assert len(candidate_groups) == 10
    assert sum(len(v) for v in candidate_groups.values()) == 20

    probable: set[str] = set()
    ambiguous: set[str] = set()
    for key, rr in candidate_groups.items():
        cross_pairs = [
            (a, b)
            for i, a in enumerate(rr)
            for b in rr[i + 1:]
            if a["source_frame"] != b["source_frame"]
        ]
        if any(species_overlap(a["species"], b["species"]) for a, b in cross_pairs):
            probable.add(key)
        else:
            ambiguous.add(key)

    assert probable == {
        "bartlewicz|2015",
        "collevatti|2014",
        "browne|2015",
        "giombini|2017",
        "pellegrino|2015",
        "lompo|2020",
    }
    assert ambiguous == {"chung|2007", "jacquemyn|2006", "jacquemyn|2009", "zhao|2009"}
    assert CONFIRMED_DUPLICATE_KEYS | CONFIRMED_FALSE_COLLISION_KEYS == set(candidate_groups)
    assert not (CONFIRMED_DUPLICATE_KEYS & CONFIRMED_FALSE_COLLISION_KEYS)

    group_existing_links: dict[str, str] = {}
    for key, rr in candidate_groups.items():
        links = {
            EXISTING_LINKS.get((r["source_frame"], r["source_id"]), "")
            for r in rr
            if EXISTING_LINKS.get((r["source_frame"], r["source_id"]), "")
        }
        assert len(links) <= 1, (key, links)
        if links:
            group_existing_links[key] = next(iter(links))

    out_fields = [
        "source_frame", "source_id", "citation", "doi", "species",
        "author_norm", "year", "author_year_key",
        "cross_frame_group_status", "identity_resolution", "canonical_identity_key",
        "existing_egwee_programme", "identity_action", "outcome_opened",
    ]
    out_rows = []
    for r in source_rows:
        key = r["author_year_key"]
        if key in CONFIRMED_DUPLICATE_KEYS:
            group_status = "cross_frame_candidate_resolved"
            resolution = "confirmed_same_publication"
            canonical_key = f"duplicate:{key}"
            action = "collapse_for_screening_do_not_double_count"
            link = group_existing_links.get(key, "") or EXISTING_LINKS.get((r["source_frame"], r["source_id"]), "")
        elif key in CONFIRMED_FALSE_COLLISION_KEYS:
            group_status = "cross_frame_candidate_resolved"
            resolution = "confirmed_distinct_publications"
            canonical_key = f"{r['source_frame']}:{r['source_id']}"
            action = "keep_separate_publications"
            link = EXISTING_LINKS.get((r["source_frame"], r["source_id"]), "")
        else:
            group_status = "no_cross_frame_author_year_collision"
            resolution = "unique_within_current_materialized_frames"
            canonical_key = f"{r['source_frame']}:{r['source_id']}"
            action = "screen_as_source_frame_record"
            link = EXISTING_LINKS.get((r["source_frame"], r["source_id"]), "")
        if link:
            action = "link_existing_egwee_programme_do_not_recruit_as_new"
        out_rows.append({
            **r,
            "cross_frame_group_status": group_status,
            "identity_resolution": resolution,
            "canonical_identity_key": canonical_key,
            "existing_egwee_programme": link,
            "identity_action": action,
        })

    unique_identity_units = len({r["canonical_identity_key"] for r in out_rows})
    existing_identity_units = len({
        r["canonical_identity_key"] for r in out_rows if r["existing_egwee_programme"]
    })
    assert unique_identity_units == 351
    assert existing_identity_units == 10

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=out_fields)
        w.writeheader()
        w.writerows(out_rows)

    dup_fields = [
        "author_year_key", "group_status", "source_frames", "source_ids",
        "citations", "species", "existing_egwee_programmes", "resolution_rule",
    ]
    dup_rows = []
    for key in sorted(candidate_groups):
        rr = candidate_groups[key]
        status = "confirmed_same_publication" if key in CONFIRMED_DUPLICATE_KEYS else "confirmed_distinct_publications"
        dup_rows.append({
            "author_year_key": key,
            "group_status": status,
            "source_frames": ";".join(r["source_frame"] for r in rr),
            "source_ids": ";".join(r["source_id"] for r in rr),
            "citations": " || ".join(r["citation"] for r in rr),
            "species": " || ".join(r["species"] for r in rr),
            "existing_egwee_programmes": ";".join(sorted({
                EXISTING_LINKS.get((r["source_frame"], r["source_id"]), "")
                for r in rr
                if EXISTING_LINKS.get((r["source_frame"], r["source_id"]), "")
            })),
            "resolution_rule": (
                "collapse to one screening identity; preserve both source-frame provenance rows"
                if key in CONFIRMED_DUPLICATE_KEYS
                else "keep as separate screening identities"
            ),
        })

    with DUPS.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=dup_fields)
        w.writeheader()
        w.writerows(dup_rows)

    summary = {
        "schema_version": 1,
        "materialized_frames": ["SF04", "SF05", "SF06"],
        "input_rows": {"SF04": 38, "SF05": 65, "SF06": 255, "total": 358},
        "unique_author_year_keys": len(by_key),
        "cross_frame_candidate_groups": len(candidate_groups),
        "cross_frame_candidate_rows": sum(len(v) for v in candidate_groups.values()),
        "heuristic_probable_same_publication_groups": len(probable),
        "heuristic_ambiguous_author_year_collision_groups": len(ambiguous),
        "confirmed_same_publication_groups": len(CONFIRMED_DUPLICATE_KEYS),
        "confirmed_distinct_collision_groups": len(CONFIRMED_FALSE_COLLISION_KEYS),
        "confirmed_duplicate_group_keys": sorted(CONFIRMED_DUPLICATE_KEYS),
        "confirmed_distinct_group_keys": sorted(CONFIRMED_FALSE_COLLISION_KEYS),
        "unique_screening_identity_units": unique_identity_units,
        "existing_egwee_linked_source_rows": sum(bool(r["existing_egwee_programme"]) for r in out_rows),
        "existing_egwee_identity_units": existing_identity_units,
        "not_yet_linked_screening_identity_units": unique_identity_units - existing_identity_units,
        "deduplication_policy": "author-year discovers candidates; full citation/journal-volume-pages/DOI and species metadata resolve identity before collapsing",
        "effect_outcomes_opened": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    STATUS.write_text(
        f"""# Phase-2 cross-frame publication identity ledger — 2026-09-20

## Scope

This ledger combines the currently row-materialized, outcome-blind publication identities from **SF04, SF05 and SF06** before any additional numerical effect extraction.

- SF04: **38** publication rows;
- SF05: **65** source-selected study rows;
- SF06: **255** publication rows;
- combined source-frame rows: **358**.

No treatment/control outcome value is added by this crosswalk.

## Duplicate discovery

A conservative two-stage identity rule is used.

1. DOI/full-citation identity is required before records are collapsed.
2. First-author + year is used only to find records requiring review.

Across the 358 rows:

- unique first-author/year keys: **{len(by_key)}**;
- cross-frame author/year candidate groups: **{len(candidate_groups)}** containing **{sum(len(v) for v in candidate_groups.values())}** rows;
- heuristic same-publication candidates from species agreement: **{len(probable)}**;
- heuristic ambiguous author/year collisions: **{len(ambiguous)}**;
- after full source-citation resolution: **{len(CONFIRMED_DUPLICATE_KEYS)} confirmed duplicate groups** and **{len(CONFIRMED_FALSE_COLLISION_KEYS)} confirmed distinct collisions**.

Confirmed cross-frame duplicates are:

- Bartlewicz 2015;
- Collevatti 2014;
- Browne 2015;
- Giombini 2017;
- Pellegrino 2015;
- Lompo 2020;
- Zhao 2009.

Zhao 2009 is important: the source-frame species labels disagree (`Glycine soja` versus `Glycine_max`), but both records identify the same *American Journal of Botany* 96:1138–1147 publication. Citation identity therefore overrides the species-field discrepancy.

The three confirmed distinct same-author/year collisions are Chung 2007, Jacquemyn 2006 and Jacquemyn 2009; their journals/species/source citations differ and they remain separate.

Collapsing only the seven confirmed duplicate pairs reduces **358 source-frame rows to {unique_identity_units} screening identity units**. Of those, **{existing_identity_units}** are already linked to known EGWEE programmes, leaving **{unique_identity_units-existing_identity_units}** identities not yet linked under the current firewall.

## Existing EGWEE firewall

Known records already belonging to an admitted or declared Phase-2 programme are explicitly linked so they cannot be recruited again as independent evidence. Examples include:

- Farwig et al. 2008 → `P2_CF01_GPAIR_003`;
- Pellegrino et al. 2015 → `ML001`;
- Aizen & Feinsinger 1994 → `ML020`;
- Cristóbal-Pérez et al. 2021 → `ML003`;
- Lompo et al. 2020 → `P2_SF05_93`;
- Delnevo et al. 2019 → existing Conospermum programme (`PS009`);
- Sáyago et al. 2018 → `ML008`;
- Albaladejo et al. 2012 → structurally closed `ML009/PS013`;
- Llorens et al. 2018 → gradient `ML015`;
- Breed et al. 2012 (*Eucalyptus socialis*) → `ML014`.

The identity ledger therefore advances systematic coverage by separating **new screening records** from **known-programme rediscoveries** before effect extraction.

## Next operation

Use the {unique_identity_units} canonical identity units—not 358 source-frame rows—as the denominator for the next title/abstract/method screen. Expand the existing-programme crosswalk before any new effect extraction, then screen unresolved identities for prespecified multilayer geometry.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CROSSFRAME_IDENTITY_OK "
        f"rows={len(source_rows)} author_year={len(by_key)} cross_groups={len(candidate_groups)} "
        f"confirmed_duplicates={len(CONFIRMED_DUPLICATE_KEYS)} false_collisions={len(CONFIRMED_FALSE_COLLISION_KEYS)} "
        f"identity_units={unique_identity_units} existing_units={existing_identity_units} outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
