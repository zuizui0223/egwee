from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "manuscript/meta_analysis_phase2_contract.json"
AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-17_SYSTEMATIC_COVERAGE_MODERATORS.md"
COVERAGE = ROOT / "manuscript/meta_analysis_coverage_frame_v2.csv"
MODERATORS = ROOT / "manuscript/meta_analysis_moderator_schema_v1.csv"
RECOVERY = ROOT / "manuscript/meta_analysis_recovery_priority_v2.csv"
SYNTHESIS = ROOT / "scripts/synthesize_state_separation.py"
COVARIANCE = ROOT / "scripts/check_covariance_robustness.py"

DISPLAY_TOL = 5e-8


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def emitted_json(command: list[str], prefix: str) -> dict:
    proc = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    line = next((x for x in proc.stdout.splitlines() if x.startswith(prefix)), None)
    if line is None:
        raise AssertionError(f"missing emitted record {prefix!r}")
    return json.loads(line.split(" ", 1)[1])


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    amendment = AMENDMENT.read_text(encoding="utf-8")

    assert contract["schema_version"] == 1
    assert contract["frozen_on"] == "2026-09-17"
    assert contract["frozen_scientific_base"] == "16308cf6d6e4aec274504ba81bbf6e71be465099"
    assert contract["phase2_purpose"] == "systematic_coverage_and_moderator_inference_not_significance_repair"

    phase1 = contract["phase1_reference"]
    assert phase1 == {
        "n_primary_clusters": 5,
        "n_primary_marginal_effects": 17,
        "canonical_p": 0.01212432,
        "omit_ML001_p": 0.18194353,
        "zero_covariance_p": 0.03860161,
        "covariance_free_bound_p": 0.28061178,
        "optimization_target": False,
        "search_for_sixth_cluster_to_repair_significance": False,
    }

    canonical = emitted_json([sys.executable, str(SYNTHESIS)], "EGWEE_STATE_SEPARATION ")
    assert canonical["n_primary_independent_clusters"] == phase1["n_primary_clusters"]
    assert canonical["n_primary_effects"] == phase1["n_primary_marginal_effects"]
    assert abs(canonical["primary_combined_p"] - phase1["canonical_p"]) < DISPLAY_TOL
    loo = {x["dropped_cluster"]: x["combined_p"] for x in canonical["primary_leave_one_cluster_out"]}
    assert abs(loo["ML001"] - phase1["omit_ML001_p"]) < DISPLAY_TOL

    covariance = emitted_json([sys.executable, str(COVARIANCE)], "COVARIANCE_ROBUSTNESS ")
    assert abs(covariance["zero_covariance"]["fisher_p"] - phase1["zero_covariance_p"]) < DISPLAY_TOL
    assert abs(
        covariance["cauchy_schwarz_certification_bound"]["fisher_p"]
        - phase1["covariance_free_bound_p"]
    ) < DISPLAY_TOL

    required_estimands = {
        "I_minus_F",
        "C_minus_F",
        "Gadult_minus_Goffspring",
        "Gadult_minus_mean_I_F_when_jointly_estimable",
    }
    assert set(contract["primary_estimands"]) == required_estimands
    assert contract["effect_family_boundaries"]["cross_family_pooling_allowed"] is False

    coverage = rows(COVERAGE)
    assert [r["frame_id"] for r in coverage] == [
        "SF01", "SF02", "SF03", "SF04", "SF05", "SF06", "SF07", "CF01"
    ]
    assert set(contract["source_frames"]) == {r["frame_id"] for r in coverage}
    assert all(r["status"] == "registered_not_executed" for r in coverage)
    assert all("outcome" in r["outcome_blind_rule"].lower() or "effect" in r["outcome_blind_rule"].lower() or "screen" in r["outcome_blind_rule"].lower() for r in coverage)

    moderators = rows(MODERATORS)
    assert [r["moderator_id"] for r in moderators] == [f"M{i:02d}" for i in range(1, 11)]
    moderator_fields = {r["field_name"] for r in moderators}
    assert {
        "mating_system",
        "autonomous_reproductive_assurance",
        "pollination_vector",
        "woodiness",
        "life_form",
        "fragmentation_age_years",
        "fragmentation_component",
        "process_measurement_type",
        "biome_region",
        "study_design",
    } == moderator_fields

    gates = contract["moderator_gates"]
    assert gates == {
        "univariable_min_independent_clusters": 10,
        "categorical_min_clusters_per_level": 4,
        "continuous_min_independent_clusters": 10,
        "multivariable_min_independent_clusters": 20,
        "multivariable_min_clusters_per_df": 10,
    }

    recovery = rows(RECOVERY)
    assert {r["cluster_id"] for r in recovery} == {f"ML{i:03d}" for i in range(4, 14)}
    by_id = {r["cluster_id"]: r for r in recovery}
    assert {cid for cid, r in by_id.items() if r["phase2_priority"] == "P1"} == {
        "ML006", "ML007", "ML008", "ML012"
    }
    assert {cid for cid, r in by_id.items() if r["phase2_priority"] == "HARD_CLOSED"} == {
        "ML009", "ML013"
    }
    assert all(by_id[cid]["phase2_status"] == "structural_closed" for cid in ("ML009", "ML013"))
    assert all("signific" not in r["priority_rationale"].lower() for r in recovery)

    promotion = contract["promotion_gate"]
    assert promotion["requires_systematic_frame_complete"] is True
    assert promotion["depends_on_smaller_phase1_p_value"] is False
    assert len(promotion["qualifying_information_conditions"]) == 3

    required_amendment_tokens = [
        "does **not** reopen the corpus to repair significance",
        "paired within-system layer differences",
        "cohort/history lag",
        "reproductive assurance",
        "Model-opening gates",
        "Search completion and stop rule",
        "Promotion rule for the Journal of Ecology manuscript",
        "search for a sixth direct cluster solely to repair omit-ML001 significance",
    ]
    for token in required_amendment_tokens:
        assert token in amendment, token

    no_rescue = set(contract["hard_no_rescue_rules"])
    assert "no_sixth_cluster_search_for_omit_ML001_significance" in no_rescue
    assert "no_outcome_based_study_retention" in no_rescue
    assert "no_outcome_derived_compensation_moderator" in no_rescue
    assert "no_NEE_operator_validation_claim" in no_rescue

    print(
        "SYSTEMATIC_COVERAGE_EXPANSION_CONTRACT_OK "
        f"frames={len(coverage)} moderators={len(moderators)} "
        f"recovery_targets={sum(r['phase2_status']=='registered_recovery_target' for r in recovery)} "
        f"hard_closed={sum(r['phase2_status']=='structural_closed' for r in recovery)}"
    )


if __name__ == "__main__":
    main()
