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

    out_fields = [
        "source_frame", "source_id", "citation", "doi", "species",
        "author_norm", "year", "author_year_key",
        "cross_frame_group_status", "existing_egwee_programme",
        "identity_action", "outcome_opened",
    ]
    out_rows = []
    for r in source_rows:
        key = r["author_year_key"]
        if key in probable:
            group_status = "probable_same_publication_needs_identity_confirmation"
            action = "review_once_cross_frame_do_not_double_count"
        elif key in ambiguous:
            group_status = "author_year_collision_species_disagree"
            action = "keep_separate_unless_full_citation_or_doi_proves_identity"
        else:
            group_status = "no_cross_frame_author_year_collision"
            action = "screen_as_source_frame_record"
        link = EXISTING_LINKS.get((r["source_frame"], r["source_id"]), "")
        if link:
            action = "link_existing_egwee_programme_do_not_recruit_as_new"
        out_rows.append({
            **r,
            "cross_frame_group_status": group_status,
            "existing_egwee_programme": link,
            "identity_action": action,
        })

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
        status = "probable_same_publication" if key in probable else "ambiguous_author_year_collision"
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
                "confirm by full citation/DOI before collapsing"
                if key in probable
                else "keep separate unless full citation/DOI later proves identity"
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
        "probable_same_publication_groups": len(probable),
        "ambiguous_author_year_collision_groups": len(ambiguous),
        "probable_group_keys": sorted(probable),
        "ambiguous_group_keys": sorted(ambiguous),
        "existing_egwee_linked_rows": sum(bool(EXISTING_LINKS.get((r["source_frame"], r["source_id"]), "")) for r in source_rows),
        "deduplication_policy": "DOI/full-citation confirmation required before collapsing; author-year is candidate discovery only",
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
- probable same-publication groups after species-name agreement/tiny spelling tolerance: **{len(probable)}**;
- ambiguous same-author/year groups with discordant species: **{len(ambiguous)}**.

The six probable duplicate groups are:

- Bartlewicz 2015;
- Collevatti 2014;
- Browne 2015;
- Giombini 2017;
- Pellegrino 2015;
- Lompo 2020.

They are **not yet collapsed automatically**. Full citation/DOI confirmation remains required.

The four ambiguous collisions (Chung 2007, Jacquemyn 2006, Jacquemyn 2009, Zhao 2009) remain separate unless later source metadata proves identity.

## Existing EGWEE firewall

Known records already belonging to an admitted or declared Phase-2 programme are explicitly linked so they cannot be recruited again as independent evidence. Examples include:

- Farwig et al. 2008 → `P2_CF01_GPAIR_003`;
- Pellegrino et al. 2015 → `ML001`;
- Aizen & Feinsinger 1994 → `ML020`;
- Cristóbal-Pérez et al. 2021 → `ML003`;
- Lompo et al. 2020 → `P2_SF05_93`.

The identity ledger therefore advances systematic coverage by separating **new screening records** from **known-programme rediscoveries** before effect extraction.

## Next operation

Resolve the six probable cross-frame duplicate groups by full citation/DOI, then apply the same existing-programme crosswalk to all 358 rows. After identity resolution, title/abstract/method screening can proceed on unique programmes rather than duplicated source-frame rows.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CROSSFRAME_IDENTITY_OK "
        f"rows={len(source_rows)} author_year={len(by_key)} cross_groups={len(candidate_groups)} "
        f"probable={len(probable)} ambiguous={len(ambiguous)} "
        f"existing_links={summary['existing_egwee_linked_rows']} outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
