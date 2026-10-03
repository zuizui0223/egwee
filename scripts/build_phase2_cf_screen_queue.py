from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SF05 = ROOT / "evidence/meta_extraction/phase2_sf05_primary_study_universe_v1.csv"
IDENTITY = ROOT / "evidence/meta_extraction/phase2_crossframe_publication_identity_v1.csv"
QUEUE = ROOT / "evidence/meta_extraction/phase2_cf_fragmentation_screen_queue_v1.csv"
SUMMARY = ROOT / "evidence/meta_extraction/phase2_cf_screen_summary_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF_SCREEN_QUEUE_2026-09-21.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    sf05 = rows(SF05)
    identity = rows(IDENTITY)
    idmap = {
        r["source_id"]: r
        for r in identity
        if r["source_frame"] == "SF05"
    }

    candidates = []
    for r in sf05:
        ident = idmap[r["source_paper_id"]]
        hints = r["title_method_screen_hints"] or ""
        if "C_screen" not in hints:
            continue
        if ident["existing_egwee_programme"]:
            continue
        candidates.append((r, ident, hints))

    assert len(candidates) == 16

    out = []
    for i, (r, ident, hints) in enumerate(candidates, start=1):
        out.append({
            "queue_id": f"CFQ{i:03d}",
            "canonical_identity_key": ident["canonical_identity_key"],
            "source_frame": "SF05",
            "source_paper_id": r["source_paper_id"],
            "citation": r["reference"] or r["citation"],
            "doi": r["doi"],
            "species": r["species"],
            "countries": r["countries"],
            "cohorts": r["cohorts"],
            "disturbance_classes": r["disturbance_classes"],
            "C_metadata_basis": hints,
            "F_screen_basis": "title_abstract_methods_only",
            "design_gate": (
                "verify source-defined fragmentation exposure; verify a reproductive-function "
                "endpoint F in the same programme and exposure frame; recover fragmentation-level "
                "independent units; do not promote offspring/trees/loci/paternity events to replicates"
            ),
            "screening_status": "pending_CF_title_abstract_methods_screen",
            "outcome_opened": "no",
        })

    assert all("C_screen" in r["C_metadata_basis"] for r in out)

    with QUEUE.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    summary = {
        "schema_version": 1,
        "source": "SF05 outcome-blind bibliographic/title-method layer hints",
        "candidate_count": len(out),
        "selection_rule": (
            "C_screen present in SF05 metadata and canonical identity not already linked "
            "to an existing EGWEE programme"
        ),
        "current_CF_direct_coverage": 2,
        "pair_gate": 5,
        "forbidden_selection_inputs": [
            "effect_direction", "effect_magnitude", "p_value",
            "reported_significance", "source_meta_analysis_inclusion_result"
        ],
        "effect_outcomes_opened": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    STATUS.write_text(
        """# Phase-2 C-F screening queue — 2026-09-21

## Current state

Direct `C-F` coverage is **2/5** (ML001 + ML002).

The currently materialized cross-frame ledger does not contain an unresolved
identity already tagged with both C and F. Therefore the next outcome-blind
screen starts from SF05 records whose bibliographic/title-method metadata
independently indicate a movement/connectivity (`C`) layer.

After removing records already linked to existing EGWEE programmes, **16
publication identities** remain.

## Screening rule

A candidate can advance only if title/abstract/method information establishes:

1. a source-defined fragmentation exposure;
2. a reproductive-function (`F`) endpoint in the same programme;
3. C and F share the relevant fragmentation exposure;
4. fragmentation-level independent units are recoverable;
5. no lower-level tree, offspring, locus or paternity event is promoted to an
   independent fragmentation replicate.

Effect direction, magnitude, significance and source-meta-analysis result are
not screening inputs.

Machine-readable queue:
`evidence/meta_extraction/phase2_cf_fragmentation_screen_queue_v1.csv`.

## Next operation

Screen the 16 identities for same-programme C + F geometry. Close records that
contain C but no reproductive function before any numerical effect is opened.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF_SCREEN_QUEUE_OK "
        f"candidates={len(out)} current_coverage=2/5 outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
