from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
EVIDENCE = ROOT / "evidence" / "meta_extraction"

def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def main() -> None:
    contract = json.loads((MANUSCRIPT / "meta_analysis_phase2_contract.json").read_text(encoding="utf-8"))
    assert contract["frozen_scientific_base"] == "16308cf6d6e4aec274504ba81bbf6e71be465099"
    assert contract["phase2_purpose"] == "systematic_coverage_and_moderator_inference_not_significance_repair"
    assert contract["phase1_reference"]["search_for_sixth_cluster_to_repair_significance"] is False
    assert contract["phase1_reference"]["optimization_target"] is False
    assert contract["pair_specific_analysis_gate"]["min_independent_programmes"] == 5
    assert contract["moderator_gates"]["univariable_min_independent_clusters"] == 10
    assert contract["moderator_gates"]["multivariable_min_independent_clusters"] == 20
    assert "no_sixth_cluster_search_for_omit_ML001_significance" in contract["hard_no_rescue_rules"]
    assert "no_outcome_based_study_retention" in contract["hard_no_rescue_rules"]
    assert "no_NEE_operator_validation_claim" in contract["hard_no_rescue_rules"]

    frames = rows(MANUSCRIPT / "meta_analysis_coverage_frame_v2.csv")
    assert {r["frame_id"] for r in frames} == {"SF01","SF02","SF03","SF04","SF05","SF06","SF07","CF01"}
    verified = [r for r in frames if r["frame_id"].startswith("SF")]
    assert all(r["status"].startswith("source_verified_") for r in verified)
    assert next(r for r in frames if r["frame_id"] == "CF01")["status"] == "registered_not_executed"
    assert all("significance" not in r["phase2_use"].lower() for r in frames)

    pair = rows(EVIDENCE / "coverage_expansion_pair_coverage_v1.csv")
    expected = {
        "I-F": 1,
        "G_adult-G_offspring": 1,
        "C-F": 2,
        "G_adult-mean(I,F)": 0,
    }
    assert {r["pair_id"]: int(r["current_independent_direct_systems"]) for r in pair} == expected
    assert all(r["analysis_opening_gate"] == "5_independent_programmes" for r in pair)

    priority = rows(MANUSCRIPT / "meta_analysis_recovery_priority_v2.csv")
    p1 = {r["cluster_id"] for r in priority if r["phase2_priority"] == "P1"}
    hard = {r["cluster_id"] for r in priority if r["phase2_priority"] == "HARD_CLOSED"}
    assert p1 == {"ML006","ML007","ML008","ML012"}
    assert hard == {"ML009","ML013"}
    assert all("significance" not in r["priority_rationale"].lower() for r in priority)

    mods = rows(MANUSCRIPT / "meta_analysis_moderator_schema_v1.csv")
    assert len(mods) == 10
    assert {r["field_name"] for r in mods} >= {
        "mating_system",
        "autonomous_reproductive_assurance",
        "pollination_vector",
        "fragmentation_age_years",
        "fragmentation_component",
        "process_measurement_type",
    }

    schema = json.loads((MANUSCRIPT / "meta_analysis_effect_schema.json").read_text(encoding="utf-8"))
    assert schema["coverage_amendment"] == "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-18_SYSTEMATIC_COVERAGE_MODERATORS.md"

    print("PHASE2_CONTRACT_OK frames=7+CF01 pair_gate=5 moderator_gate=10 no_significance_repair=true")

if __name__ == "__main__":
    main()
