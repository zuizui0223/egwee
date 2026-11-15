#!/usr/bin/env python3
"""Apply outcome-blind, literature-frozen endpoint taxonomy to a published schema.

No pre/post heterozygosity, fitness, response signs or effect sizes are read.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
from pathlib import Path


def gate(schema: dict, codebook: dict) -> dict:
    if schema.get("status") != "SCHEMA_ONLY_NO_EFFECT_VALUES_OPENED":
        raise ValueError("Clarke source must be a schema-only receipt")
    if not codebook.get("frozen_before_outcome_sign_inspection"):
        raise ValueError("Endpoint classification not frozen")
    rows = schema["fitness_parameter_levels_complete"]
    classes = codebook["metric_classification"]
    if set(rows) != set(classes):
        raise ValueError("Unclassified published endpoint code")
    domain_counts = defaultdict(int)
    direct = 0
    for k, n in rows.items():
        if n < 1:
            raise ValueError("Nonpositive source category count")
        domain_counts[classes[k]["domain"]] += n
        if classes[k]["direct_interaction_function_confirmed"]:
            direct += n
    if sum(rows.values()) != schema["complete_original_author_slice_rows"]:
        raise ValueError("Author slice counts do not sum")
    ir_studies = schema.get("studies_by_fitness_parameter", {}).get("IR", [])
    if ir_studies != ["Arrendal (2004)", "Gustafson (2017)"]:
        raise ValueError(f"Original reproductive paper list drifted: {ir_studies}")
    lag = schema.get("fitness_measurement_and_heterozygosity_different_generation_rows")
    same = schema.get("fitness_measurement_and_heterozygosity_same_generation_rows")
    if (same, lag) != (19, 8):
        raise ValueError("Original molecular/fitness observation-generation alignment changed")
    return {
        "date": "2026-11-15",
        "status": "ENDPOINT_CLASSIFIED_NO_EFFECT_DIRECTIONS_OPENED",
        "data_doi": schema["data_doi"],
        "source_sha256": schema["source_sha256"],
        "independent_source_studies": schema["unique_original_studies_complete"],
        "paired_population_comparison_rows": schema["complete_original_author_slice_rows"],
        "endpoint_rows_by_original_code": rows,
        "endpoint_rows_by_biological_domain": dict(sorted(domain_counts.items())),
        "direct_ecological_function_confirmed_from_aggregate_source": direct,
        "reproductive_success_rows_for_source_level_screen": rows.get("IR", 0),
        "reproductive_success_unique_source_studies": len(ir_studies),
        "reproductive_success_source_studies": ir_studies,
        "primary_source_audit": "research/rescue_coupling/CLARKE_IR_PRIMARY_SOURCE_AUDIT_20261115.md",
        "same_numeric_post_generation_rows": same,
        "different_numeric_post_generation_rows": lag,
        "numeric_generation_equality_does_not_imply_same_cohort": True,
        "genetic_fitness_same_generation_rows": schema["fitness_measurement_and_heterozygosity_same_generation_rows"],
        "genetic_fitness_different_generation_rows": schema["fitness_measurement_and_heterozygosity_different_generation_rows"],
        "genetic_fitness_timing_unresolved_rows": schema["fitness_measurement_timing_not_resolved_rows"],
        "genetic_measurements_available_as_pre_post_expected_heterozygosity":
            schema["all_complete_rows_share_pair_fields"],
        "primary_causal_rescue_identified_from_pre_post_summary": False,
        "analysis_decision": (
            "The existing 19-study meta dataset cannot by itself identify ecological "
            "interaction-function rescue; 20 rows report population size and seven "
            "report generic survival/reproduction. The three reproduction rows "
            "require original-study endpoint and intervention-control verification. "
            "No new pooled effect sizes are claimed."
        ),
        "unit_warning": "27 paired rows are nested in 19 studies; not 27 independent systems",
        "terminology_warning": "Marker change is not itself causal genetic rescue; functional rescue has independent species-replacement usage"
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--schema", type=Path, required=True)
    p.add_argument("--codebook", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    source = json.loads(a.schema.read_text(encoding="utf-8"))
    book = json.loads(a.codebook.read_text(encoding="utf-8"))
    out = gate(source, book)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
