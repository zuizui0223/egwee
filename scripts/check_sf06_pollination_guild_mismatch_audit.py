#!/usr/bin/env python3
"""Exploratory guild stratification of SF06 point-sign I-F mismatch.

This is a post-outcome-visibility diagnostic of a selected publication corpus,
not a confirmatory moderator test. Source publications, not individual rows,
define leave-one-out influence. No frozen EGWEE denominator is modified.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from check_sf06_publication_delete_predictive_influence import OVERLAP

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"


def selected() -> list[dict[str, str]]:
    with PAIRS.open(encoding="utf-8", newline="") as fh:
        source = list(csv.DictReader(fh))
    assert len(source) == 59, len(source)
    rows = [
        r for r in source
        if r["land_use_factor_normalized"] == "habitat fragmentation"
        and r["I_component_consensus_sign"] in {"lower", "nonlower"}
        and r["F_component_consensus_sign"] in {"lower", "nonlower"}
    ]
    assert len(rows) == 54, len(rows)
    for r in rows:
        # Remove an inconsistent semicolon used by the source metadata.
        context = r["pollination_context"].replace(";", " ").strip().lower().split()
        assert context and context[0] in {"vertebrate", "invertebrate"}, (
            r["species"], r["pollination_context"]
        )
        r["guild_audit"] = context[0]
    return rows


def summarize(rows: list[dict[str, str]]) -> dict:
    result = {}
    for guild in ("vertebrate", "invertebrate"):
        part = [r for r in rows if r["guild_audit"] == guild]
        n = len(part)
        assert n, f"empty guild: {guild}"
        false_reassurance = [
            r for r in part
            if r["I_component_consensus_sign"] == "nonlower"
            and r["F_component_consensus_sign"] == "lower"
        ]
        false_warning = [
            r for r in part
            if r["I_component_consensus_sign"] == "lower"
            and r["F_component_consensus_sign"] == "nonlower"
        ]
        assert len(false_reassurance) + len(false_warning) <= n
        # No opposite-sign pair has two separately 95%-resolved endpoints.
        assert not [
            r for r in false_reassurance + false_warning
            if r["I_resolved_consensus_sign"] == r["I_component_consensus_sign"]
            and r["F_resolved_consensus_sign"] == r["F_component_consensus_sign"]
        ]
        result[guild] = {
            "pairs": n,
            "publications": len({r["source_publication_key"] for r in part}),
            "I_nonlower_F_lower_point_sign": len(false_reassurance),
            "I_lower_F_nonlower_point_sign": len(false_warning),
            "I_nonlower_F_lower_fraction_of_selected_pairs": len(false_reassurance) / n,
            "false_reassurance_species": [r["species"] for r in false_reassurance],
        }
    result["vertebrate_minus_invertebrate_false_reassurance_fraction"] = (
        result["vertebrate"]["I_nonlower_F_lower_fraction_of_selected_pairs"]
        - result["invertebrate"]["I_nonlower_F_lower_fraction_of_selected_pairs"]
    )
    return result


def audit(rows: list[dict[str, str]]) -> dict:
    baseline = summarize(rows)
    deletions = {
        pub: summarize([r for r in rows if r["source_publication_key"] != pub])
        for pub in sorted({r["source_publication_key"] for r in rows})
    }
    diffs = {
        p: v["vertebrate_minus_invertebrate_false_reassurance_fraction"]
        for p, v in deletions.items()
    }
    return {
        "baseline": baseline,
        "publication_deleted_comparisons": len(diffs),
        "positive_after_deletion": sum(v > 0 for v in diffs.values()),
        "negative_after_deletion": sum(v < 0 for v in diffs.values()),
        "smallest_contrast": min(diffs.values()),
        "smallest_contrast_publication": min(diffs, key=diffs.get),
        "largest_contrast": max(diffs.values()),
        "largest_contrast_publication": max(diffs, key=diffs.get),
    }


def main() -> None:
    rows = selected()
    disjoint = [r for r in rows if r["source_publication_key"] not in OVERLAP]
    assert len(disjoint) == 31
    assert len({r["source_publication_key"] for r in disjoint}) == 23

    full = audit(rows)
    clean = audit(disjoint)
    f, d = full["baseline"], clean["baseline"]
    assert (f["vertebrate"]["pairs"], f["invertebrate"]["pairs"]) == (8, 46)
    assert (f["vertebrate"]["I_nonlower_F_lower_point_sign"],
            f["invertebrate"]["I_nonlower_F_lower_point_sign"]) == (3, 4)
    assert (f["vertebrate"]["I_lower_F_nonlower_point_sign"],
            f["invertebrate"]["I_lower_F_nonlower_point_sign"]) == (0, 9)
    assert (d["vertebrate"]["pairs"], d["invertebrate"]["pairs"]) == (4, 27)
    assert (d["vertebrate"]["I_nonlower_F_lower_point_sign"],
            d["invertebrate"]["I_nonlower_F_lower_point_sign"]) == (1, 3)
    assert (d["vertebrate"]["I_lower_F_nonlower_point_sign"],
            d["invertebrate"]["I_lower_F_nonlower_point_sign"]) == (0, 6)
    assert (full["positive_after_deletion"], full["negative_after_deletion"]) == (32, 0)
    assert (clean["positive_after_deletion"], clean["negative_after_deletion"]) == (22, 1)
    assert "magrach et al. (2013)" in clean["smallest_contrast_publication"]

    print("SF06_GUILD_MISMATCH_AUDIT: PASS")
    print(json.dumps({
        "status": "post_hoc_selected_public_S1_guild_candidate",
        "new_EGWEE_admissions": 0,
        "no_prevalence_or_causal_inference": True,
        "full": full,
        "source_publication_disjoint": clean,
        "interpretation": (
            "A vertebrate-guild false-reassurance point-sign enrichment appears "
            "in the full selected corpus. It is NOT robust in the source-"
            "publication-disjoint subset to deleting the Tristerix publication. "
            "No discordant pair has two independently resolved endpoint signs."
        ),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
