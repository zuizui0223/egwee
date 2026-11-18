from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDENTITY = ROOT / "evidence/meta_extraction/phase2_crossframe_publication_identity_v1.csv"
SF04 = ROOT / "evidence/meta_extraction/phase2_sf04_publication_universe_v1.csv"
SF05 = ROOT / "evidence/meta_extraction/phase2_sf05_primary_study_universe_v1.csv"
SF06 = ROOT / "evidence/meta_extraction/phase2_sf06_publication_universe_v1.csv"

QUEUE = ROOT / "evidence/meta_extraction/phase2_metadata_screen_queue_v1.csv"
IF_QUEUE = ROOT / "evidence/meta_extraction/phase2_if_fragmentation_screen_queue_v1.csv"
SUMMARY = ROOT / "evidence/meta_extraction/phase2_metadata_screen_summary_v1.json"
STATUS = ROOT / "manuscript/PHASE2_METADATA_SCREEN_QUEUE_2026-09-20.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def add_unique(target: list[str], value: str) -> None:
    value = (value or "").strip()
    if value and value not in target:
        target.append(value)


def add_layer(target: set[str], layer: str) -> None:
    if layer:
        target.add(layer)


def main() -> None:
    for path in (IDENTITY, SF04, SF05, SF06):
        assert path.is_file(), path

    identity_rows = rows(IDENTITY)
    assert len(identity_rows) == 358
    assert all(r["outcome_opened"] == "no" for r in identity_rows)

    source_to_identity = {
        (r["source_frame"], r["source_id"]): r for r in identity_rows
    }
    canonical_keys = {r["canonical_identity_key"] for r in identity_rows}
    assert len(canonical_keys) == 351

    aggregate: dict[str, dict[str, object]] = {}
    for r in identity_rows:
        key = r["canonical_identity_key"]
        a = aggregate.setdefault(key, {
            "canonical_identity_key": key,
            "source_frames": [],
            "source_ids": [],
            "citations": [],
            "species": [],
            "layers": set(),
            "land_use_factors": [],
            "sf06_responses": [],
            "sf05_title_method_hints": [],
            "existing_egwee_programmes": [],
            "outcome_opened": "no",
        })
        add_unique(a["source_frames"], r["source_frame"])
        add_unique(a["source_ids"], f'{r["source_frame"]}:{r["source_id"]}')
        add_unique(a["citations"], r["citation"])
        for sp in (r["species"] or "").split(";"):
            add_unique(a["species"], sp)
        add_unique(a["existing_egwee_programmes"], r["existing_egwee_programme"])

    for r in rows(SF04):
        ident = source_to_identity[("SF04", r["sf04_reference_id"])]
        a = aggregate[ident["canonical_identity_key"]]
        add_layer(a["layers"], "G_adult")

    for r in rows(SF05):
        ident = source_to_identity[("SF05", r["source_paper_id"])]
        a = aggregate[ident["canonical_identity_key"]]
        add_layer(a["layers"], "G_adult")
        hints = r["title_method_screen_hints"] or ""
        add_unique(a["sf05_title_method_hints"], hints)
        if "C_screen" in hints:
            add_layer(a["layers"], "C")
        if "D_screen" in hints:
            add_layer(a["layers"], "D")
        if "F_screen" in hints:
            add_layer(a["layers"], "F")
        if "G_offspring_screen" in hints:
            add_layer(a["layers"], "G_offspring")

    for r in rows(SF06):
        ident = source_to_identity[("SF06", r["sf06_publication_id"])]
        a = aggregate[ident["canonical_identity_key"]]
        responses = r["responses"] or ""
        add_unique(a["sf06_responses"], responses)
        add_unique(a["land_use_factors"], r["land_use_factors"])
        if "Pollination" in responses:
            add_layer(a["layers"], "I")
        if "Female fitness" in responses or "Male fitness" in responses:
            add_layer(a["layers"], "F")

    assert len(aggregate) == 351

    output_rows: list[dict[str, str]] = []
    if_rows: list[dict[str, str]] = []

    for key in sorted(aggregate):
        a = aggregate[key]
        layers = sorted(a["layers"])
        existing = sorted(a["existing_egwee_programmes"])
        land = "; ".join(a["land_use_factors"])
        has_if = "I" in layers and "F" in layers
        explicit_fragmentation = has_if and "fragment" in land.lower()
        existing_link = bool(existing)

        if existing_link:
            screen_class = "existing_egwee_programme"
            screen_action = "do_not_recruit_as_new"
        elif explicit_fragmentation:
            screen_class = "primary_if_fragmentation_design_screen"
            screen_action = "screen_title_abstract_methods_same_exposure_and_independent_unit"
        elif has_if:
            screen_class = "secondary_if_nonfragmentation_land_use"
            screen_action = "retain_context_not_primary_if_fragmentation_queue"
        elif len(layers) >= 2:
            screen_class = "other_multilayer_metadata_hint"
            screen_action = "screen_after_primary_if_queue"
        else:
            screen_class = "single_layer_or_no_pair_hint"
            screen_action = "retain_in_systematic_universe_no_immediate_pair_screen"

        row = {
            "canonical_identity_key": key,
            "source_frames": ";".join(a["source_frames"]),
            "source_ids": ";".join(a["source_ids"]),
            "citation": " || ".join(a["citations"]),
            "species": "; ".join(a["species"]),
            "metadata_layers": ";".join(layers),
            "sf06_responses": " || ".join(a["sf06_responses"]),
            "land_use_factors": land,
            "sf05_title_method_hints": " || ".join(a["sf05_title_method_hints"]),
            "existing_egwee_programmes": ";".join(existing),
            "screen_class": screen_class,
            "screen_action": screen_action,
            "screening_status": (
                "linked_existing_no_new_recruitment"
                if existing_link
                else "pending_outcome_blind_design_screen"
                if screen_class in {
                    "primary_if_fragmentation_design_screen",
                    "other_multilayer_metadata_hint",
                }
                else "retained_no_primary_design_screen_yet"
            ),
            "outcome_opened": "no",
        }
        output_rows.append(row)

        if screen_class == "primary_if_fragmentation_design_screen":
            if_rows.append({
                "queue_id": f"IFQ{len(if_rows)+1:03d}",
                "canonical_identity_key": key,
                "source_frames": row["source_frames"],
                "source_ids": row["source_ids"],
                "citation": row["citation"],
                "species": row["species"],
                "metadata_layers": row["metadata_layers"],
                "sf06_responses": row["sf06_responses"],
                "land_use_factors": row["land_use_factors"],
                "screen_basis": "source_metadata_only_no_effect_direction_or_significance",
                "design_gate": (
                    "verify source-defined fragmentation exposure; at least two I/F layers share the "
                    "same exposure; recover fragmentation-level independent unit; no nested-unit promotion"
                ),
                "screening_status": "pending_title_abstract_methods_design_screen",
                "outcome_opened": "no",
            })

    counts = {
        "canonical_identity_units": len(output_rows),
        "existing_egwee_programmes": sum(
            r["screen_class"] == "existing_egwee_programme" for r in output_rows
        ),
        "unresolved_identity_units": sum(
            r["screen_class"] != "existing_egwee_programme" for r in output_rows
        ),
        "unresolved_multilayer_metadata_hints": sum(
            r["screen_class"] != "existing_egwee_programme"
            and len([x for x in r["metadata_layers"].split(";") if x]) >= 2
            for r in output_rows
        ),
        "unresolved_IF_metadata_hints": sum(
            r["screen_class"] in {
                "primary_if_fragmentation_design_screen",
                "secondary_if_nonfragmentation_land_use",
            }
            for r in output_rows
        ),
        "primary_IF_fragmentation_design_queue": len(if_rows),
        "secondary_IF_nonfragmentation": sum(
            r["screen_class"] == "secondary_if_nonfragmentation_land_use"
            for r in output_rows
        ),
        "other_multilayer_metadata_hints": sum(
            r["screen_class"] == "other_multilayer_metadata_hint"
            for r in output_rows
        ),
        "single_layer_or_no_pair_hint": sum(
            r["screen_class"] == "single_layer_or_no_pair_hint"
            for r in output_rows
        ),
    }
    assert counts == {
        "canonical_identity_units": 351,
        "existing_egwee_programmes": 11,
        "unresolved_identity_units": 340,
        "unresolved_multilayer_metadata_hints": 60,
        "unresolved_IF_metadata_hints": 36,
        "primary_IF_fragmentation_design_queue": 32,
        "secondary_IF_nonfragmentation": 4,
        "other_multilayer_metadata_hints": 24,
        "single_layer_or_no_pair_hint": 280,
    }, counts

    assert all(r["outcome_opened"] == "no" for r in output_rows)
    assert all(r["outcome_opened"] == "no" for r in if_rows)
    assert all("fragment" in r["land_use_factors"].lower() for r in if_rows)
    assert all(
        "I" in r["metadata_layers"].split(";") and "F" in r["metadata_layers"].split(";")
        for r in if_rows
    )

    queue_fields = list(output_rows[0])
    with QUEUE.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=queue_fields)
        w.writeheader()
        w.writerows(output_rows)

    if_fields = list(if_rows[0])
    with IF_QUEUE.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=if_fields)
        w.writeheader()
        w.writerows(if_rows)

    summary = {
        "schema_version": 1,
        "built_from": [
            "phase2_crossframe_publication_identity_v1.csv",
            "phase2_sf04_publication_universe_v1.csv",
            "phase2_sf05_primary_study_universe_v1.csv",
            "phase2_sf06_publication_universe_v1.csv",
        ],
        "counts": counts,
        "primary_pair_priority": "I-F because current independent direct coverage is 1/5",
        "IF_queue_rule": (
            "unlinked canonical identity with SF06 Pollination plus Female/Male fitness metadata "
            "and source land-use factor explicitly containing fragmentation"
        ),
        "forbidden_selection_inputs": [
            "effect_direction",
            "Hedges_d",
            "sampling_variance",
            "p_value",
            "reported_significance",
        ],
        "effect_outcomes_opened": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    STATUS.write_text(
        f"""# Phase-2 metadata screening queue — 2026-09-20

## Current denominator

The resolved cross-frame ledger contains **{counts['canonical_identity_units']} canonical publication identities** across the currently materialized SF04/SF05/SF06 frames.

- already linked to existing EGWEE programmes: **{counts['existing_egwee_programmes']}**;
- unresolved identities: **{counts['unresolved_identity_units']}**;
- unresolved identities with at least two metadata-level biological layers: **{counts['unresolved_multilayer_metadata_hints']}**.

No effect direction, Hedges d, variance, p-value or significance field is used in this queue.

## Primary I-F screen

Current direct I-F coverage remains **1/5** (ML020 only), so the first design-screening lane is the prespecified I-F family.

Among unresolved identities:

- metadata indicate both pollination/interaction (I) and reproductive fitness (F): **{counts['unresolved_IF_metadata_hints']}**;
- source land-use metadata explicitly identify habitat fragmentation: **{counts['primary_IF_fragmentation_design_queue']}**;
- I+F records attributed only to agriculture/urbanization rather than fragmentation: **{counts['secondary_IF_nonfragmentation']}** and are not in the primary fragmentation queue.

The 32-record queue is stored in
`evidence/meta_extraction/phase2_if_fragmentation_screen_queue_v1.csv`.

Each record must pass the same design gate before quantitative extraction:

1. fragmentation exposure is source-defined rather than inferred from the response;
2. I and F share the same exposure frame;
3. fragmentation-level independent units are recoverable;
4. nested flowers/plants/visits/fruits are not promoted to independent fragmentation replicates;
5. programme duplication is resolved before effect calculation.

## Other unresolved metadata geometry

- other multilayer hints outside the immediate I-F queue: **{counts['other_multilayer_metadata_hints']}**;
- single-layer/no-pair immediate hints: **{counts['single_layer_or_no_pair_hint']}**.

They remain in the systematic universe and are not discarded. The I-F lane is processed first because its preregistered pair coverage is currently the sparsest opened target, not because any candidate result is favorable.

## Next executable operation

Run title/abstract/method design screening on the 32 I-F fragmentation identities. Close candidates on exposure or independent-unit geometry before opening numerical effects; advance only designs that can support a same-system I-F contrast.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_METADATA_SCREEN_QUEUE_OK "
        f"identity_units={counts['canonical_identity_units']} "
        f"existing={counts['existing_egwee_programmes']} unresolved={counts['unresolved_identity_units']} "
        f"multilayer={counts['unresolved_multilayer_metadata_hints']} "
        f"IF={counts['unresolved_IF_metadata_hints']} primary_IF={len(if_rows)} "
        "outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
