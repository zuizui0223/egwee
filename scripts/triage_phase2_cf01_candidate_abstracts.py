from __future__ import annotations

import csv
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "evidence/meta_extraction/phase2_cf01_candidate_screen_queue_v1.csv"
OUT = ROOT / "evidence/meta_extraction/phase2_cf01_candidate_abstract_triage_v1.csv"
SUMMARY = ROOT / "evidence/meta_extraction/phase2_cf01_candidate_abstract_triage_summary_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF01_ABSTRACT_TRIAGE_2026-09-23.md"

OPENALEX = "https://api.openalex.org"
USER_AGENT = "EGWEE-Phase2-CF01/1.0"
BATCH_SIZE = 40
SLEEP_SECONDS = 0.15

FRAGMENT_TERMS = (
    "fragment", "habitat loss", "patch size", "forest patch", "landscape connectivity",
    "landscape isolation", "isolated population", "isolated populations", "edge effect",
    "habitat connectivity", "remnant", "habitat amount",
)
I_TERMS = (
    "pollinator", "pollination", "flower visitor", "floral visitor", "visitation",
    "visit rate", "pollen limitation",
)
C_TERMS = (
    "gene flow", "pollen flow", "pollen dispers", "seed dispers", "paternity",
    "parentage", "immigration", "migration", "dispersal distance", "mating system",
)
F_TERMS = (
    "fruit set", "seed set", "seed production", "fruit production", "reproductive success",
    "fecundity", "seed number", "fruit number", "offspring performance", "progeny performance",
    "recruitment",
)
G_TERMS = (
    "genetic diversity", "heterozygos", "allelic", "genetic structure", "inbreeding",
    "fst", "f st", "microsatellite", "genomic diversity", "genetic differentiation",
)
OFFSPRING_TERMS = ("seedling", "seedlings", "progeny", "offspring", "embryo", "juvenile")


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


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


def reconstruct_abstract(index: dict | None) -> str:
    if not index:
        return ""
    positions: list[tuple[int, str]] = []
    for token, locs in index.items():
        for pos in locs or []:
            positions.append((int(pos), token))
    positions.sort()
    return " ".join(token for _, token in positions)


def has_any(text: str, terms: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(term in lower for term in terms)


def layer_flags(text: str) -> list[str]:
    out = []
    if has_any(text, I_TERMS):
        out.append("I")
    if has_any(text, C_TERMS):
        out.append("C")
    if has_any(text, F_TERMS):
        out.append("F")
    if has_any(text, G_TERMS):
        out.append("G_offspring" if has_any(text, OFFSPRING_TERMS) else "G_adult")
    return out


def main() -> None:
    assert QUEUE.is_file(), QUEUE
    queue = rows(QUEUE)
    assert queue
    assert all(r["outcome_opened"] == "no" for r in queue)

    ready = [
        r for r in queue
        if r["screening_status"] == "pending_title_abstract_methods_screen"
    ]
    ids = sorted({r["candidate_openalex_id"] for r in ready if r["candidate_openalex_id"]})
    metadata: dict[str, dict] = {}
    failed_batches: list[str] = []

    select = "id,title,abstract_inverted_index"
    for i in range(0, len(ids), BATCH_SIZE):
        batch = ids[i:i+BATCH_SIZE]
        params = urllib.parse.urlencode({
            "filter": "openalex:" + "|".join(batch),
            "per-page": str(BATCH_SIZE),
            "select": select,
        })
        try:
            obj = get_json(f"{OPENALEX}/works?{params}")
        except Exception as exc:
            failed_batches.append(f"{i}:{type(exc).__name__}")
            continue
        for work in obj.get("results") or []:
            wid = (work.get("id") or "").rstrip("/").split("/")[-1]
            if wid:
                metadata[wid] = work
        if i + BATCH_SIZE < len(ids):
            time.sleep(SLEEP_SECONDS)

    out = []
    for r in queue:
        wid = r["candidate_openalex_id"]
        work = metadata.get(wid)
        abstract = reconstruct_abstract((work or {}).get("abstract_inverted_index"))
        combined = " ".join([r["title"], abstract]).strip()
        frag = has_any(combined, FRAGMENT_TERMS)
        layers = layer_flags(combined)

        if r["screening_status"] != "pending_title_abstract_methods_screen":
            triage = "not_in_ecological_screening_set"
        elif work is None:
            triage = "abstract_metadata_unresolved"
        elif frag and len(layers) >= 2:
            triage = "priority_multilayer_fragmentation"
        elif frag and len(layers) == 1:
            triage = "priority_single_layer_fragmentation"
        elif frag:
            triage = "fragmentation_no_registered_layer_hint"
        elif layers:
            triage = "layer_hint_no_fragmentation_term"
        else:
            triage = "low_metadata_relevance_needs_screen"

        out.append({
            "candidate_openalex_id": wid,
            "doi": r["doi"],
            "title": r["title"],
            "publication_year": r["publication_year"],
            "first_author": r["first_author"],
            "source_name": r["source_name"],
            "seed_identity_status": r["seed_identity_status"],
            "screening_status": r["screening_status"],
            "abstract_available": "yes" if abstract else "no",
            "fragmentation_term_hint": "yes" if frag else "no",
            "layer_hints": ";".join(layers),
            "triage_class": triage,
            "triage_rule": "title_and_openalex_abstract_metadata_only_no_effect_outcome",
            "abstract_text": abstract,
            "outcome_opened": "no",
        })

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    counts = Counter(r["triage_class"] for r in out)
    ready_rows = [r for r in out if r["screening_status"] == "pending_title_abstract_methods_screen"]
    summary = {
        "schema_version": 1,
        "candidate_queue_units": len(queue),
        "ready_for_ecological_screen": len(ready),
        "requested_openalex_abstract_units": len(ids),
        "openalex_metadata_resolved_units": len(metadata),
        "failed_batches": failed_batches,
        "abstract_available_ready_units": sum(r["abstract_available"] == "yes" for r in ready_rows),
        "triage_counts": dict(sorted(counts.items())),
        "triage_is_priority_not_inclusion": True,
        "all_ready_candidates_must_eventually_be_screened": True,
        "forbidden_inputs": [
            "effect_direction", "effect_magnitude", "variance", "p_value", "reported_significance"
        ],
        "effect_outcomes_opened": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    STATUS.write_text(
        f"""# Phase-2 CF01 outcome-blind abstract triage — 2026-09-23

## Purpose

This is a workload-ordering layer, not an inclusion filter.

For candidates already cleared by the CF01 seed-identity firewall, OpenAlex title/abstract
metadata are scanned for habitat-fragmentation terms and prespecified EGWEE layer terms.

No effect magnitude, direction, variance, p-value or significance field is queried.

## Current materialization

- candidate queue units: **{len(queue)}**;
- candidates ready for ecological title/abstract/method screening: **{len(ready)}**;
- OpenAlex abstract metadata resolved: **{len(metadata)}**;
- ready candidates with abstract text available: **{sum(r['abstract_available'] == 'yes' for r in ready_rows)}**;
- metadata batch failures retained: **{len(failed_batches)}**.

Triage counts:

{chr(10).join(f"- {k}: **{v}**" for k, v in sorted(counts.items()))}

## Interpretation

priority_multilayer_fragmentation is screened first because its metadata contain both a
fragmentation term and at least two prespecified layer hints. It is not automatically included.

Likewise, low_metadata_relevance_needs_screen is not automatically excluded. Every candidate in
the ecological screening set remains part of the search denominator until title/abstract/method
screening assigns a documented decision.

## Next operation

Process the priority_multilayer_fragmentation group first, then the remaining ready candidates,
recording explicit exposure, layer, independent-unit and duplicate-programme decisions.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF01_ABSTRACT_TRIAGE_OK "
        f"queue={len(queue)} ready={len(ready)} metadata={len(metadata)} "
        f"abstracts={sum(r['abstract_available']=='yes' for r in ready_rows)} "
        f"failed_batches={len(failed_batches)} outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
