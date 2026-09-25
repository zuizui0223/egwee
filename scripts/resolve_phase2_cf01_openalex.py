from __future__ import annotations

import csv
import json
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evidence/meta_extraction/phase2_cf01_seed_manifest_v1.csv"
OUT = ROOT / "evidence/meta_extraction/phase2_cf01_bibliographic_resolution_v1.csv"
SUMMARY = ROOT / "evidence/meta_extraction/phase2_cf01_bibliographic_resolution_summary_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF01_BIBLIOGRAPHIC_RESOLUTION_2026-09-21.md"

OPENALEX = "https://api.openalex.org"
CROSSREF = "https://api.crossref.org"
USER_AGENT = "EGWEE-Phase2-CF01/1.0"
SLEEP_SECONDS = 0.16


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def tokens(text: str) -> set[str]:
    stop = {
        "the", "and", "of", "in", "a", "an", "to", "for", "on", "with",
        "from", "by", "effects", "effect", "study", "analysis",
    }
    return {x for x in norm(text).split() if len(x) >= 3 and x not in stop}


def first_author_hint(citation: str) -> str:
    text = citation.strip()
    if not text:
        return ""
    m = re.match(r"^([^,(]+?)(?:\s+et\s+al\.?|\s*&|\s*,|\s*\()", text, re.I)
    raw = m.group(1) if m else text.split(",", 1)[0]
    return norm(raw).split(" ")[0] if norm(raw) else ""


def result_first_author(work: dict) -> str:
    authorships = work.get("authorships") or []
    if not authorships:
        return ""
    name = ((authorships[0].get("author") or {}).get("display_name") or "").strip()
    n = norm(name)
    return n.split()[-1] if n else ""


def year_hint(row: dict[str, str]) -> int | None:
    if row["year"].isdigit():
        return int(row["year"])
    m = re.search(r"\b(?:19|20)\d{2}\b", row["citation"])
    return int(m.group(0)) if m else None


def volume_page_hint(citation: str) -> tuple[str, str]:
    # Most SF04/SF06 citations use "volume:firstpage-lastpage".
    matches = re.findall(r"\b(\d{1,4})\s*:\s*(\d{1,6})\b", citation or "")
    return matches[-1] if matches else ("", "")


def title_similarity(a: str, b: str) -> float:
    aa, bb = tokens(a), tokens(b)
    if not aa or not bb:
        return 0.0
    return len(aa & bb) / len(aa | bb)


def get_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def resolve_doi(doi: str) -> tuple[dict | None, str]:
    target = f"https://doi.org/{doi.lower()}"
    url = f"{OPENALEX}/works/{urllib.parse.quote(target, safe=':/')}"
    try:
        return get_json(url), ""
    except urllib.error.HTTPError as exc:
        return None, f"http_{exc.code}"
    except Exception as exc:
        return None, f"{type(exc).__name__}"


def score_candidate(seed: dict[str, str], work: dict) -> tuple[float, dict]:
    y = year_hint(seed)
    author = first_author_hint(seed["citation"])
    volume, page = volume_page_hint(seed["citation"])

    wy = work.get("publication_year")
    wauthor = result_first_author(work)
    biblio = work.get("biblio") or {}
    wvolume = str(biblio.get("volume") or "")
    wpage = str(biblio.get("first_page") or "")

    year_match = y is not None and wy == y
    author_match = bool(author and wauthor and author == wauthor)
    volume_match = bool(volume and wvolume and volume == wvolume)
    page_match = bool(page and wpage and page == wpage)
    tsim = title_similarity(seed["title"], work.get("title") or "") if seed["title"] else 0.0

    score = 0.0
    score += 3.0 if year_match else 0.0
    score += 3.0 if author_match else 0.0
    score += 1.0 if volume_match else 0.0
    score += 2.0 if page_match else 0.0
    score += min(4.0, 4.0 * tsim)

    details = {
        "year_match": year_match,
        "author_match": author_match,
        "volume_match": volume_match,
        "page_match": page_match,
        "title_similarity": round(tsim, 6),
    }
    return score, details


def resolve_citation(seed: dict[str, str]) -> tuple[dict | None, float, float, dict, str]:
    query = seed["citation"] or seed["title"]
    params = urllib.parse.urlencode({"search": query, "per-page": 5})
    url = f"{OPENALEX}/works?{params}"
    try:
        obj = get_json(url)
    except urllib.error.HTTPError as exc:
        return None, 0.0, 0.0, {}, f"http_{exc.code}"
    except Exception as exc:
        return None, 0.0, 0.0, {}, f"{type(exc).__name__}"

    ranked = []
    for work in obj.get("results") or []:
        score, details = score_candidate(seed, work)
        ranked.append((score, work, details))
    ranked.sort(key=lambda x: x[0], reverse=True)
    if not ranked:
        return None, 0.0, 0.0, {}, "no_results"

    top_score, top, details = ranked[0]
    second = ranked[1][0] if len(ranked) > 1 else 0.0
    margin = top_score - second

    # Fail closed. Author + year are mandatory. In addition require either
    # first-page agreement, or strong title agreement, or volume agreement with
    # a clear ranking margin.
    structural_ok = details["author_match"] and details["year_match"]
    evidence_ok = (
        details["page_match"]
        or details["title_similarity"] >= 0.45
        or (details["volume_match"] and margin >= 1.0)
    )
    accepted = structural_ok and evidence_ok and top_score >= 7.0 and margin >= 0.5
    return (top if accepted else None), top_score, margin, details, ("" if accepted else "ambiguous_or_low_confidence")



def crossref_first_author(item: dict) -> str:
    authors = item.get("author") or []
    if not authors:
        return ""
    return norm((authors[0].get("family") or "").strip())


def crossref_year(item: dict) -> int | None:
    for key in ("published-print", "published-online", "published", "issued"):
        parts = ((item.get(key) or {}).get("date-parts") or [])
        if parts and parts[0]:
            try:
                return int(parts[0][0])
            except (TypeError, ValueError):
                pass
    return None


def score_crossref_candidate(seed: dict[str, str], item: dict) -> tuple[float, dict]:
    y = year_hint(seed)
    author = first_author_hint(seed["citation"])
    volume, page = volume_page_hint(seed["citation"])

    cy = crossref_year(item)
    cauthor = crossref_first_author(item)
    cvolume = str(item.get("volume") or "")
    cpage = str(item.get("page") or "").split("-", 1)[0].strip()
    titles = item.get("title") or []
    ctitle = titles[0] if titles else ""

    year_match = y is not None and cy == y
    author_match = bool(author and cauthor and author == cauthor)
    volume_match = bool(volume and cvolume and volume == cvolume)
    page_match = bool(page and cpage and page == cpage)
    tsim = title_similarity(seed["title"], ctitle) if seed["title"] else 0.0

    score = 0.0
    score += 3.0 if year_match else 0.0
    score += 3.0 if author_match else 0.0
    score += 1.0 if volume_match else 0.0
    score += 2.0 if page_match else 0.0
    score += min(4.0, 4.0 * tsim)

    return score, {
        "year_match": year_match,
        "author_match": author_match,
        "volume_match": volume_match,
        "page_match": page_match,
        "title_similarity": round(tsim, 6),
        "crossref_title": ctitle,
        "crossref_doi": (item.get("DOI") or "").lower(),
    }


def resolve_citation_crossref_to_openalex(
    seed: dict[str, str],
) -> tuple[dict | None, float, float, dict, str]:
    query = seed["citation"] or seed["title"]
    params = urllib.parse.urlencode({"query.bibliographic": query, "rows": 5})
    try:
        obj = get_json(f"{CROSSREF}/works?{params}")
    except urllib.error.HTTPError as exc:
        return None, 0.0, 0.0, {}, f"crossref_http_{exc.code}"
    except Exception as exc:
        return None, 0.0, 0.0, {}, f"crossref_{type(exc).__name__}"

    items = (((obj.get("message") or {}).get("items")) or [])
    ranked = []
    for item in items:
        score, details = score_crossref_candidate(seed, item)
        ranked.append((score, item, details))
    ranked.sort(key=lambda x: x[0], reverse=True)
    if not ranked:
        return None, 0.0, 0.0, {}, "crossref_no_results"

    top_score, top, details = ranked[0]
    second = ranked[1][0] if len(ranked) > 1 else 0.0
    margin = top_score - second
    structural_ok = details["author_match"] and details["year_match"]
    evidence_ok = (
        details["page_match"]
        or details["title_similarity"] >= 0.45
        or (details["volume_match"] and margin >= 1.0)
    )
    accepted = structural_ok and evidence_ok and top_score >= 7.0 and margin >= 0.5
    if not accepted:
        return None, top_score, margin, details, "crossref_ambiguous_or_low_confidence"

    doi = (top.get("DOI") or "").strip().lower()
    if not doi:
        return None, top_score, margin, details, "crossref_match_without_doi"

    work, error = resolve_doi(doi)
    if work is None:
        return None, top_score, margin, details, f"crossref_doi_openalex_{error}"

    return work, top_score, margin, details, ""


def main() -> None:
    seeds = rows(MANIFEST)
    assert len(seeds) == 363
    assert all(r["outcome_opened"] == "no" for r in seeds)

    out = []
    for i, seed in enumerate(seeds, start=1):
        method = ""
        work = None
        score = 0.0
        margin = 0.0
        details: dict = {}
        error = ""

        if seed["doi"]:
            work, error = resolve_doi(seed["doi"])
            method = "openalex_doi_exact"
            if work is not None:
                score = 100.0
                margin = 100.0
                details = {"doi_exact": True}
        else:
            work, score, margin, details, error = resolve_citation_crossref_to_openalex(seed)
            method = "crossref_bibliographic_to_openalex_doi"

        if work is None:
            status = "unresolved"
            openalex_id = ""
            resolved_doi = ""
            title = ""
            year = ""
            cited_by_count = ""
            referenced_count = ""
        else:
            status = "resolved"
            openalex_id = work.get("id") or ""
            resolved_doi = (work.get("doi") or "").removeprefix("https://doi.org/").lower()
            title = work.get("title") or ""
            year = str(work.get("publication_year") or "")
            cited_by_count = str(work.get("cited_by_count") or 0)
            referenced_count = str(len(work.get("referenced_works") or []))

        out.append({
            "cf01_seed_id": seed["cf01_seed_id"],
            "canonical_search_key": seed["canonical_search_key"],
            "input_doi": seed["doi"],
            "input_citation": seed["citation"],
            "resolution_status": status,
            "resolution_method": method,
            "openalex_id": openalex_id,
            "resolved_doi": resolved_doi,
            "resolved_title": title,
            "resolved_year": year,
            "match_score": f"{score:.6f}",
            "match_margin": f"{margin:.6f}",
            "match_details_json": json.dumps(details, sort_keys=True),
            "cited_by_count_metadata": cited_by_count,
            "referenced_work_count_metadata": referenced_count,
            "resolution_error": error,
            "citation_expansion_cutoff": seed["citation_expansion_cutoff"],
            "outcome_opened": "no",
        })
        if i < len(seeds):
            time.sleep(SLEEP_SECONDS)

    assert len(out) == 363
    assert all(r["outcome_opened"] == "no" for r in out)

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    resolved = [r for r in out if r["resolution_status"] == "resolved"]
    unresolved = [r for r in out if r["resolution_status"] == "unresolved"]
    doi_seeds = [r for r in seeds if r["doi"]]
    citation_only = [r for r in seeds if not r["doi"]]
    resolved_doi = sum(
        r["resolution_status"] == "resolved" and r["resolution_method"] == "openalex_doi_exact"
        for r in out
    )
    resolved_openalex_citation = sum(
        r["resolution_status"] == "resolved" and r["resolution_method"] == "openalex_citation_search_fail_closed"
        for r in out
    )
    resolved_crossref_citation = sum(
        r["resolution_status"] == "resolved" and r["resolution_method"] == "crossref_bibliographic_to_openalex_doi"
        for r in out
    )
    resolved_citation = resolved_openalex_citation + resolved_crossref_citation

    summary = {
        "schema_version": 1,
        "route": "OpenAlex public API",
        "cutoff": "2026-09-18",
        "seed_units": len(seeds),
        "doi_seed_units": len(doi_seeds),
        "citation_only_seed_units": len(citation_only),
        "resolved_units": len(resolved),
        "resolved_by_exact_doi": resolved_doi,
        "resolved_by_fail_closed_citation_search": resolved_citation,
        "resolved_by_openalex_citation_search": resolved_openalex_citation,
        "resolved_by_crossref_bibliographic_to_openalex_doi": resolved_crossref_citation,
        "unresolved_units": len(unresolved),
        "resolution_rate": round(len(resolved) / len(seeds), 6),
        "acceptance_rule": (
            "citation search requires exact first-author surname + publication year and "
            "page agreement or strong title agreement or volume agreement with ranking margin; "
            "ambiguous matches remain unresolved"
        ),
        "effect_outcomes_opened": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    STATUS.write_text(
        f"""# Phase-2 CF01 bibliographic resolution — 2026-09-21

## Route

The 363-unit partial CF01 seed manifest was resolved through one uniform public bibliographic route: **OpenAlex**.

No effect-size or significance field is queried or used.

- seed units: **{len(seeds)}**;
- exact-DOI seeds: **{len(doi_seeds)}**;
- citation-only seeds: **{len(citation_only)}**;
- resolved total: **{len(resolved)}**;
- resolved by exact DOI: **{resolved_doi}**;
- resolved by fail-closed citation search: **{resolved_citation}**;\n- resolved through Crossref bibliographic match → OpenAlex exact DOI: **{resolved_crossref_citation}**;
- unresolved: **{len(unresolved)}**;
- resolution rate: **{len(resolved)/len(seeds):.1%}**.

## Fail-closed matching rule

DOI-bearing seeds are resolved only through exact DOI lookup.

Citation-only seeds use Crossref bibliographic lookup and then require an exact DOI handoff to OpenAlex. They require:

1. exact first-author surname;
2. exact publication year;
3. plus first-page agreement, strong title agreement, or volume agreement with a clear ranking margin.

Ambiguous results remain unresolved rather than being assigned to the highest search result.

## Next operation

Only resolved units are eligible for automated backward/forward citation materialization. Unresolved units remain in the search denominator and must be resolved through a second bibliographic route or manual bibliographic adjudication; they are not silently dropped.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF01_BIBLIOGRAPHIC_RESOLUTION_OK "
        f"seeds={len(seeds)} resolved={len(resolved)} doi={resolved_doi} "
        f"citation={resolved_citation} crossref={resolved_crossref_citation} unresolved={len(unresolved)} outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
