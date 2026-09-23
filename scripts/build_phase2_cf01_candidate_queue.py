from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "evidence/meta_extraction/phase2_cf01_seed_manifest_v1.csv"
RESOLUTION = ROOT / "evidence/meta_extraction/phase2_cf01_bibliographic_resolution_v1.csv"
CANDIDATES = ROOT / "evidence/meta_extraction/phase2_cf01_citation_candidate_universe_v1.csv"
QUEUE = ROOT / "evidence/meta_extraction/phase2_cf01_candidate_screen_queue_v1.csv"
SUMMARY = ROOT / "evidence/meta_extraction/phase2_cf01_candidate_dedup_summary_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF01_CANDIDATE_QUEUE_2026-09-23.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def short_id(value: str) -> str:
    return (value or "").rstrip("/").split("/")[-1]


def first_author_hint(citation: str) -> str:
    text = citation.strip()
    if not text:
        return ""
    m = re.match(r"^([^,(]+?)(?:\s+et\s+al\.?|\s*&|\s*,|\s*\()", text, re.I)
    raw = m.group(1) if m else text.split(",", 1)[0]
    n = norm(raw)
    return n.split(" ")[0] if n else ""


def candidate_author_hint(name: str) -> str:
    n = norm(name)
    return n.split(" ")[-1] if n else ""


def main() -> None:
    for path in (SEEDS, RESOLUTION, CANDIDATES):
        assert path.is_file(), path

    seeds = rows(SEEDS)
    resolution = rows(RESOLUTION)
    candidates = rows(CANDIDATES)
    assert len(seeds) == len(resolution) == 363
    assert all(r["outcome_opened"] == "no" for r in seeds)
    assert all(r["outcome_opened"] == "no" for r in resolution)
    assert all(r["outcome_opened"] == "no" for r in candidates)

    resolution_by_seed = {r["cf01_seed_id"]: r for r in resolution}
    assert set(resolution_by_seed) == {r["cf01_seed_id"] for r in seeds}

    seed_openalex = {
        short_id(r["openalex_id"])
        for r in resolution
        if r["resolution_status"] == "resolved" and r["openalex_id"]
    }
    seed_dois = {r["doi"].strip().lower() for r in seeds if r["doi"].strip()}
    seed_title_year = {(norm(r["title"]), r["year"].strip()) for r in seeds if norm(r["title"]) and r["year"].strip()}

    unresolved_author_year: dict[tuple[str, str], set[str]] = defaultdict(set)
    for seed in seeds:
        rr = resolution_by_seed[seed["cf01_seed_id"]]
        if rr["resolution_status"] == "resolved":
            continue
        author = first_author_hint(seed["citation"])
        year = seed["year"].strip()
        if author and year:
            unresolved_author_year[(author, year)].add(seed["cf01_seed_id"])

    out = []
    for cand in candidates:
        candidate_id = short_id(cand["candidate_openalex_id"])
        doi = cand["doi"].strip().lower()
        title_key = norm(cand["title"])
        author = candidate_author_hint(cand["first_author"])
        year = cand["publication_year"].strip()

        exact_reasons = []
        if candidate_id and candidate_id in seed_openalex:
            exact_reasons.append("openalex_id")
        if doi and doi in seed_dois:
            exact_reasons.append("doi")
        if title_key and year and (title_key, year) in seed_title_year:
            exact_reasons.append("normalized_title_plus_year")

        unresolved_collision_ids = sorted(unresolved_author_year.get((author, year), set()))

        inherited = cand["screening_status"]
        if inherited != "pending_title_abstract_methods_screen":
            seed_identity_status = "not_applicable_noneligible_candidate"
            screening_status = inherited
        elif exact_reasons:
            seed_identity_status = "existing_seed_exact_identity"
            screening_status = "existing_CF01_seed_no_new_screen"
        elif unresolved_collision_ids:
            seed_identity_status = "possible_unresolved_seed_identity_collision"
            screening_status = "pending_seed_identity_adjudication"
        else:
            seed_identity_status = "no_seed_identity_collision_detected"
            screening_status = "pending_title_abstract_methods_screen"

        out.append({
            "candidate_openalex_id": candidate_id,
            "doi": doi,
            "title": cand["title"],
            "publication_date": cand["publication_date"],
            "publication_year": year,
            "work_type": cand["work_type"],
            "first_author": cand["first_author"],
            "source_name": cand["source_name"],
            "is_retracted_metadata": cand["is_retracted_metadata"],
            "citation_directions": cand["citation_directions"],
            "source_seed_ids": cand["source_seed_ids"],
            "n_source_seeds": cand["n_source_seeds"],
            "cutoff_status": cand["cutoff_status"],
            "seed_identity_status": seed_identity_status,
            "exact_seed_identity_reasons": ";".join(exact_reasons),
            "possible_unresolved_seed_ids": ";".join(unresolved_collision_ids),
            "screening_status": screening_status,
            "outcome_opened": "no",
        })

    assert len(out) == len(candidates)
    assert all(r["outcome_opened"] == "no" for r in out)

    with QUEUE.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    counts: dict[str, int] = defaultdict(int)
    for row in out:
        counts[row["screening_status"]] += 1

    summary = {
        "schema_version": 1,
        "seed_manifest_units": len(seeds),
        "candidate_units": len(candidates),
        "bibliographically_resolved_seed_units": len(seed_openalex),
        "exact_seed_doi_count": len(seed_dois),
        "unresolved_seed_author_year_keys": len(unresolved_author_year),
        "screening_status_counts": dict(sorted(counts.items())),
        "deduplication_rule": (
            "exact OpenAlex ID, DOI, or normalized title + publication year => existing seed; "
            "author-year collision with unresolved seed => adjudicate, never auto-collapse; "
            "only cutoff-eligible candidates with no detected seed collision enter title/abstract/method screening"
        ),
        "effect_outcomes_opened": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    ready = counts.get("pending_title_abstract_methods_screen", 0)
    adjudicate = counts.get("pending_seed_identity_adjudication", 0)
    existing = counts.get("existing_CF01_seed_no_new_screen", 0)

    STATUS.write_text(
        f"""# Phase-2 CF01 candidate deduplication queue — 2026-09-23

## Purpose

The citation graph is deduplicated against the frozen 363-unit CF01 seed manifest before
ecological screening or numerical extraction.

No effect direction, magnitude, variance, p-value or significance field is used.

## Identity firewall

A discovered candidate is treated as an existing seed when it matches a seed by:

- exact OpenAlex work ID;
- exact DOI; or
- exact normalized title plus publication year.

A candidate that only shares first-author surname + publication year with a still-unresolved
seed is not auto-collapsed and is not sent directly to ecological screening. It enters
pending_seed_identity_adjudication.

Only candidates dated on/before the frozen cutoff and with no detected seed identity collision
enter pending_title_abstract_methods_screen.

## Current counts

- seed manifest units: **{len(seeds)}**;
- discovered candidate works: **{len(candidates)}**;
- existing-seed rediscoveries after identity firewall: **{existing}**;
- unresolved-seed identity adjudications: **{adjudicate}**;
- new candidates ready for title/abstract/method screening: **{ready}**.

Other candidates retain their inherited post-cutoff/date/metadata status.

## Next operation

Retrieve outcome-blind bibliographic abstract metadata for the pending_title_abstract_methods_screen
set, then screen for EGWEE habitat-fragmentation relevance and prespecified layer geometry.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF01_CANDIDATE_QUEUE_OK "
        f"candidates={len(candidates)} ready={ready} adjudicate={adjudicate} "
        f"existing={existing} outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
