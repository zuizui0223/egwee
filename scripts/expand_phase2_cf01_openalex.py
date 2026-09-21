from __future__ import annotations

import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOLUTION = ROOT / "evidence/meta_extraction/phase2_cf01_bibliographic_resolution_v1.csv"
SEEDS = ROOT / "evidence/meta_extraction/phase2_cf01_seed_manifest_v1.csv"
EDGES = ROOT / "evidence/meta_extraction/phase2_cf01_citation_edges_v1.csv"
CANDIDATES = ROOT / "evidence/meta_extraction/phase2_cf01_citation_candidate_universe_v1.csv"
SUMMARY = ROOT / "evidence/meta_extraction/phase2_cf01_citation_expansion_summary_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF01_CITATION_EXPANSION_2026-09-21.md"

OPENALEX = "https://api.openalex.org"
USER_AGENT = "EGWEE-Phase2-CF01/1.0"
CUTOFF = date.fromisoformat("2026-09-18")
SLEEP_SECONDS = 0.12
BATCH_SIZE = 100


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def short_id(value: str) -> str:
    return (value or "").rstrip("/").split("/")[-1]


def get_json(url: str, retries: int = 4) -> dict:
    last: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return json.load(resp)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            last = exc
            if attempt + 1 == retries:
                break
            time.sleep(1.5 * (attempt + 1))
    assert last is not None
    raise last


def api_works(params: dict[str, str]) -> dict:
    return get_json(f"{OPENALEX}/works?{urllib.parse.urlencode(params)}")


def work_url(work_id: str, select: str = "") -> str:
    base = f"{OPENALEX}/works/{urllib.parse.quote(short_id(work_id))}"
    return base if not select else f"{base}?{urllib.parse.urlencode({'select': select})}"


SELECT = ",".join([
    "id", "doi", "title", "publication_date", "publication_year", "type",
    "authorships", "primary_location", "is_retracted", "referenced_works",
])


def first_author(work: dict) -> str:
    authorships = work.get("authorships") or []
    if not authorships:
        return ""
    return ((authorships[0].get("author") or {}).get("display_name") or "").strip()


def source_name(work: dict) -> str:
    return (
        (((work.get("primary_location") or {}).get("source") or {}).get("display_name"))
        or ""
    ).strip()


def normalized_doi(work: dict) -> str:
    return (work.get("doi") or "").removeprefix("https://doi.org/").lower()


def cutoff_status(work: dict) -> str:
    raw = (work.get("publication_date") or "").strip()
    if not raw:
        return "unknown_date_requires_adjudication"
    try:
        d = date.fromisoformat(raw)
    except ValueError:
        return "unknown_date_requires_adjudication"
    return "eligible_through_cutoff" if d <= CUTOFF else "excluded_post_cutoff"


def fetch_seed_work(openalex_id: str) -> dict:
    return get_json(work_url(openalex_id, SELECT))


def fetch_backward_metadata(ids: set[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    items = sorted({short_id(x) for x in ids if x})
    for i in range(0, len(items), BATCH_SIZE):
        batch = items[i:i+BATCH_SIZE]
        obj = api_works({
            "filter": "openalex:" + "|".join(batch),
            "per-page": str(BATCH_SIZE),
            "select": SELECT,
        })
        for work in obj.get("results") or []:
            out[short_id(work.get("id") or "")] = work
        time.sleep(SLEEP_SECONDS)
    return out


def fetch_forward(seed_openalex_id: str) -> list[dict]:
    seed_short = short_id(seed_openalex_id)
    cursor = "*"
    out: list[dict] = []
    while cursor:
        obj = api_works({
            "filter": f"cites:{seed_short}",
            "per-page": "100",
            "cursor": cursor,
            "select": SELECT,
        })
        out.extend(obj.get("results") or [])
        cursor = (obj.get("meta") or {}).get("next_cursor")
        if cursor:
            time.sleep(SLEEP_SECONDS)
    return out


def main() -> None:
    resolutions = rows(RESOLUTION)
    seeds = rows(SEEDS)
    assert len(resolutions) == len(seeds) == 363
    seed_by_id = {r["cf01_seed_id"]: r for r in seeds}
    assert set(seed_by_id) == {r["cf01_seed_id"] for r in resolutions}
    assert all(r["outcome_opened"] == "no" for r in resolutions)

    resolved = [r for r in resolutions if r["resolution_status"] == "resolved"]
    unresolved = [r for r in resolutions if r["resolution_status"] != "resolved"]
    assert resolved, "bibliographic resolution produced no resolved seeds"

    resolved_seed_openalex = {
        short_id(r["openalex_id"]) for r in resolved if r["openalex_id"]
    }
    assert len(resolved_seed_openalex) == len(resolved), (
        len(resolved_seed_openalex), len(resolved)
    )

    # Fetch each seed once. This gives the complete outgoing reference list.
    seed_work: dict[str, dict] = {}
    all_backward_ids: set[str] = set()
    seed_fetch_failures: list[tuple[str, str]] = []
    for idx, r in enumerate(resolved, start=1):
        sid = r["cf01_seed_id"]
        try:
            work = fetch_seed_work(r["openalex_id"])
        except Exception as exc:
            seed_fetch_failures.append((sid, type(exc).__name__))
            continue
        seed_work[sid] = work
        all_backward_ids.update(work.get("referenced_works") or [])
        if idx < len(resolved):
            time.sleep(SLEEP_SECONDS)

    # Resolve outgoing-reference metadata in batches.
    backward_meta = fetch_backward_metadata(all_backward_ids)

    # Candidate metadata and link provenance are deduplicated separately.
    candidate_meta: dict[str, dict] = {}
    links: set[tuple[str, str, str]] = set()
    forward_query_failures: list[tuple[str, str]] = []

    for sid, work in seed_work.items():
        seed_oa = short_id(work.get("id") or "")
        for ref in work.get("referenced_works") or []:
            cand = short_id(ref)
            if not cand or cand == seed_oa:
                continue
            links.add((sid, "backward_reference", cand))
            if cand in backward_meta:
                candidate_meta[cand] = backward_meta[cand]

    # Forward citations: no ranking-based selection. Cursor through all works
    # OpenAlex reports as citing each resolved seed.
    for idx, r in enumerate(resolved, start=1):
        sid = r["cf01_seed_id"]
        try:
            citing = fetch_forward(r["openalex_id"])
        except Exception as exc:
            forward_query_failures.append((sid, type(exc).__name__))
            continue
        seed_oa = short_id(r["openalex_id"])
        for work in citing:
            cand = short_id(work.get("id") or "")
            if not cand or cand == seed_oa:
                continue
            links.add((sid, "forward_citation", cand))
            candidate_meta[cand] = work
        if idx < len(resolved):
            time.sleep(SLEEP_SECONDS)

    # Keep unresolved metadata edges visible rather than silently dropping them.
    all_candidate_ids = {cand for _, _, cand in links}
    missing_candidate_metadata = sorted(all_candidate_ids - set(candidate_meta))

    edge_rows = []
    by_candidate_seeds: dict[str, set[str]] = defaultdict(set)
    by_candidate_dirs: dict[str, set[str]] = defaultdict(set)

    for sid, direction, cand in sorted(links):
        work = candidate_meta.get(cand)
        status = cutoff_status(work) if work is not None else "metadata_unresolved"
        edge_rows.append({
            "cf01_seed_id": sid,
            "seed_canonical_search_key": seed_by_id[sid]["canonical_search_key"],
            "seed_openalex_id": short_id(
                next(r["openalex_id"] for r in resolved if r["cf01_seed_id"] == sid)
            ),
            "direction": direction,
            "candidate_openalex_id": cand,
            "candidate_cutoff_status": status,
            "candidate_already_seed": "yes" if cand in resolved_seed_openalex else "no",
            "outcome_opened": "no",
        })
        by_candidate_seeds[cand].add(sid)
        by_candidate_dirs[cand].add(direction)

    candidate_rows = []
    for cand in sorted(all_candidate_ids):
        work = candidate_meta.get(cand)
        if work is None:
            cstatus = "metadata_unresolved"
            screening = "pending_bibliographic_metadata_recovery"
            doi = title = pub_date = pub_year = typ = author = venue = retracted = ""
        else:
            cstatus = cutoff_status(work)
            doi = normalized_doi(work)
            title = work.get("title") or ""
            pub_date = work.get("publication_date") or ""
            pub_year = str(work.get("publication_year") or "")
            typ = work.get("type") or ""
            author = first_author(work)
            venue = source_name(work)
            retracted = "yes" if work.get("is_retracted") else "no"
            if cand in resolved_seed_openalex:
                screening = "existing_CF01_seed_no_new_screen"
            elif cstatus == "eligible_through_cutoff":
                screening = "pending_title_abstract_methods_screen"
            elif cstatus == "unknown_date_requires_adjudication":
                screening = "pending_cutoff_date_adjudication"
            else:
                screening = "excluded_post_cutoff"

        candidate_rows.append({
            "candidate_openalex_id": cand,
            "doi": doi,
            "title": title,
            "publication_date": pub_date,
            "publication_year": pub_year,
            "work_type": typ,
            "first_author": author,
            "source_name": venue,
            "is_retracted_metadata": retracted,
            "citation_directions": ";".join(sorted(by_candidate_dirs[cand])),
            "source_seed_ids": ";".join(sorted(by_candidate_seeds[cand])),
            "n_source_seeds": str(len(by_candidate_seeds[cand])),
            "candidate_already_seed": "yes" if cand in resolved_seed_openalex else "no",
            "cutoff_status": cstatus,
            "screening_status": screening,
            "outcome_opened": "no",
        })

    if edge_rows:
        with EDGES.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(edge_rows[0]))
            w.writeheader()
            w.writerows(edge_rows)

    if candidate_rows:
        with CANDIDATES.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(candidate_rows[0]))
            w.writeheader()
            w.writerows(candidate_rows)

    eligible_new = [
        r for r in candidate_rows
        if r["screening_status"] == "pending_title_abstract_methods_screen"
    ]
    existing_seed = [
        r for r in candidate_rows
        if r["screening_status"] == "existing_CF01_seed_no_new_screen"
    ]
    post_cutoff = [
        r for r in candidate_rows if r["screening_status"] == "excluded_post_cutoff"
    ]
    date_pending = [
        r for r in candidate_rows
        if r["screening_status"] == "pending_cutoff_date_adjudication"
    ]
    metadata_pending = [
        r for r in candidate_rows
        if r["screening_status"] == "pending_bibliographic_metadata_recovery"
    ]

    summary = {
        "schema_version": 1,
        "route": "OpenAlex citation graph",
        "cutoff": CUTOFF.isoformat(),
        "seed_manifest_units": len(seeds),
        "resolved_seed_units": len(resolved),
        "unresolved_seed_units_not_expanded": len(unresolved),
        "seed_work_fetch_failures": len(seed_fetch_failures),
        "forward_query_failures": len(forward_query_failures),
        "unique_backward_reference_ids": len({c for _, d, c in links if d == "backward_reference"}),
        "unique_forward_citation_ids": len({c for _, d, c in links if d == "forward_citation"}),
        "citation_edges": len(edge_rows),
        "unique_discovered_candidate_works": len(candidate_rows),
        "existing_CF01_seed_candidates": len(existing_seed),
        "new_candidates_eligible_through_cutoff": len(eligible_new),
        "post_cutoff_candidates": len(post_cutoff),
        "unknown_date_candidates_pending_adjudication": len(date_pending),
        "metadata_unresolved_candidates": len(metadata_pending),
        "missing_candidate_metadata_ids": len(missing_candidate_metadata),
        "selection_rule": (
            "all OpenAlex outgoing references and all incoming citations for every resolved "
            "seed; no rank or outcome-based selection; cutoff applied from publication_date"
        ),
        "effect_outcomes_opened": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    STATUS.write_text(
        f"""# Phase-2 CF01 citation expansion — 2026-09-21

## Expansion rule

Every bibliographically resolved CF01 seed is expanded uniformly through the OpenAlex citation graph.

- backward direction: every ID in the seed work's `referenced_works`;
- forward direction: every work returned by the OpenAlex `cites:<seed>` relation;
- frozen publication cutoff: **{CUTOFF.isoformat()}**;
- search ranking used for inclusion: **no**;
- effect direction or significance used for inclusion: **no**.

## Current materialization

- seed manifest units: **{len(seeds)}**;
- bibliographically resolved seeds expanded: **{len(resolved)}**;
- unresolved seeds retained but not expanded: **{len(unresolved)}**;
- unique discovered candidate works: **{len(candidate_rows)}**;
- citation edges: **{len(edge_rows)}**;
- already-existing CF01 seeds rediscovered: **{len(existing_seed)}**;
- new candidates dated on/before cutoff and ready for title/abstract/method screening: **{len(eligible_new)}**;
- post-cutoff candidates retained as excluded audit records: **{len(post_cutoff)}**;
- candidates with unknown publication date requiring cutoff adjudication: **{len(date_pending)}**;
- candidates whose OpenAlex metadata could not be resolved: **{len(metadata_pending)}**.

Any seed-resolution or forward-query failure remains visible in the summary and does not silently remove the seed from the systematic denominator.

## Next operation

Deduplicate the eligible new candidate works against the current 363-seed manifest by OpenAlex ID/DOI, then run outcome-blind title/abstract/method screening for EGWEE fragmentation relevance and prespecified layer geometry.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF01_CITATION_EXPANSION_OK "
        f"resolved_seeds={len(resolved)} candidates={len(candidate_rows)} "
        f"eligible_new={len(eligible_new)} edges={len(edge_rows)} "
        f"date_pending={len(date_pending)} outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
