from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "manuscript/meta_analysis_phase2_contract.json"
AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-18_SYSTEMATIC_COVERAGE_MODERATORS.md"
COVERAGE = ROOT / "manuscript/meta_analysis_coverage_frame_v2.csv"
PAIR_COVERAGE = ROOT / "evidence/meta_extraction/coverage_expansion_pair_coverage_v1.csv"
MODERATORS = ROOT / "manuscript/meta_analysis_moderator_schema_v1.csv"
RECOVERY = ROOT / "manuscript/meta_analysis_recovery_priority_v2.csv"
SF05_SCREEN = ROOT / "evidence/meta_extraction/phase2_sf05_multilayer_screen_v1.csv"
SF05_SCREEN_STATUS = ROOT / "manuscript/PHASE2_SF05_MULTILAYER_SCREEN_STATUS_2026-09-19.md"
SCHEMA = ROOT / "manuscript/meta_analysis_effect_schema.json"
SYNTHESIS = ROOT / "scripts/synthesize_state_separation.py"
COVARIANCE = ROOT / "scripts/check_covariance_robustness.py"
PARKIA_CHECK = ROOT / "scripts/check_phase2_sf05_93_parkia.py"
PARKIA_STATUS = ROOT / "manuscript/PHASE2_SF05_93_PARKIA_RECOVERY_2026-09-19.md"
PARKIA_CONTRACT = ROOT / "manuscript/SF05_93_PARKIA_PHASE2_RECOVERY_CONTRACT.md"

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
    for path in (CONTRACT, AMENDMENT, COVERAGE, PAIR_COVERAGE, MODERATORS, RECOVERY, SF05_SCREEN, SF05_SCREEN_STATUS, PARKIA_CHECK, PARKIA_STATUS, PARKIA_CONTRACT, SCHEMA):
        assert path.is_file(), path

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    amendment = AMENDMENT.read_text(encoding="utf-8")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    assert contract["schema_version"] == 2
    assert contract["frozen_on"] == "2026-09-18"
    assert contract["amendment"] == AMENDMENT.relative_to(ROOT).as_posix()
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

    assert set(contract["primary_estimands"]) == {
        "I_minus_F",
        "C_minus_F",
        "Gadult_minus_Goffspring",
        "Gadult_minus_mean_I_F_when_jointly_estimable",
    }
    assert contract["effect_family_boundaries"]["cross_family_pooling_allowed"] is False

    pair_gate = contract["pair_specific_analysis_gate"]
    assert pair_gate["min_independent_programmes"] == 5
    assert "not a significance" in pair_gate["interpretation"]

    coverage = rows(COVERAGE)
    assert [r["frame_id"] for r in coverage] == [
        "SF01", "SF02", "SF03", "SF04", "SF05", "SF06", "SF07", "CF01"
    ]
    assert set(contract["source_frames"]) == {r["frame_id"] for r in coverage}
    seed_frames = [r for r in coverage if r["frame_id"].startswith("SF")]
    assert all(r["status"].startswith("source_verified_") for r in seed_frames)
    sf05 = next(r for r in coverage if r["frame_id"] == "SF05")
    assert sf05["status"] == "source_verified_row_materialized_source_selected_subset_frame_incomplete"
    cf01 = next(r for r in coverage if r["frame_id"] == "CF01")
    assert cf01["status"] == "registered_not_executed"
    assert cf01["doi_or_dataset"] == "cutoff 2026-09-18"

    pair_rows = rows(PAIR_COVERAGE)
    assert {r["pair_id"] for r in pair_rows} == {
        "I-F", "C-F", "G_adult-G_offspring", "G_adult-mean(I,F)"
    }
    by_pair = {r["pair_id"]: r for r in pair_rows}
    assert int(by_pair["I-F"]["current_independent_direct_systems"]) == 1
    assert by_pair["I-F"]["current_system_ids"] == "ML020"
    assert int(by_pair["C-F"]["current_independent_direct_systems"]) == 2
    assert set(by_pair["C-F"]["current_system_ids"].split(";")) == {"ML001", "ML002"}
    assert int(by_pair["G_adult-G_offspring"]["current_independent_direct_systems"]) == 2
    assert set(by_pair["G_adult-G_offspring"]["current_system_ids"].split(";")) == {"ML003", "P2_SF05_93"}
    assert int(by_pair["G_adult-mean(I,F)"]["current_independent_direct_systems"]) == 0
    assert all(r["analysis_opening_gate"] == "5_independent_programmes" for r in pair_rows)
    assert all("not a significance target" in r["gate_interpretation"] for r in pair_rows)

    parkia_proc = subprocess.run(
        [sys.executable, str(PARKIA_CHECK)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "PHASE2_SF05_93_PARKIA_OK" in parkia_proc.stdout
    assert "pair_covariance=PD" in parkia_proc.stdout
    assert "full3=rank_deficient" in parkia_proc.stdout
    parkia_status = PARKIA_STATUS.read_text(encoding="utf-8")
    for token in (
        "pair-specific covariance-aware Phase-2 cluster",
        "**2 independent programmes:** ML003 + P2_SF05_93",
        "analysis-opening gate remains **5 independent programmes**",
        "does **not** enter the frozen Phase-1 five-cluster Fisher synthesis",
    ):
        assert token in parkia_status, token

    moderators = rows(MODERATORS)
    assert [r["moderator_id"] for r in moderators] == [f"M{i:02d}" for i in range(1, 11)]
    gates = contract["moderator_gates"]
    assert gates == {
        "univariable_min_independent_clusters": 10,
        "categorical_min_clusters_per_level": 4,
        "continuous_min_independent_clusters": 10,
        "multivariable_min_independent_clusters": 20,
        "multivariable_min_clusters_per_df": 10,
    }

    recovery = rows(RECOVERY)
    by_id = {r["cluster_id"]: r for r in recovery}
    assert {r["cluster_id"] for r in recovery} == {f"ML{i:03d}" for i in range(4, 14)}
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
    assert promotion["moderator_significance_required"] is False
    assert promotion["depends_on_smaller_phase1_p_value"] is False
    assert "at_least_one_primary_layer_pair_family_has_at_least_5_independent_programmes" in promotion["qualifying_information_conditions"]

    assert schema["schema_version"] == 3
    assert schema["amended_on"] == "2026-09-18"
    assert schema["coverage_amendment"] == AMENDMENT.relative_to(ROOT).as_posix()

    amendment_lower = amendment.lower()
    required_amendment_tokens = [
        "canonical phase-2 protocol amendment",
        "does **not** authorize a sixth-cluster search to restore leave-one-cluster-out significance",
        "does not reduce each cluster to one p-value. it retains effect magnitudes.",
        "cohort/history lag",
        "reproductive assurance",
        "search and extraction stop rules",
        "at least **5 independent programme/study clusters**",
        "at least **10 independent programme/study clusters**",
        "must not use the same natural synthesis as duplicated load-bearing evidence",
    ]
    for token in required_amendment_tokens:
        assert token in amendment_lower, token

    no_rescue = set(contract["hard_no_rescue_rules"])
    assert {
        "no_sixth_cluster_search_for_omit_ML001_significance",
        "no_outcome_based_study_retention",
        "no_outcome_derived_compensation_moderator",
        "no_postoutcome_moderator_gate_relaxation",
        "no_covariance_method_selection_by_p_value",
        "no_NEE_operator_validation_claim",
    } <= no_rescue

    sf05_summary = ROOT / "evidence/meta_extraction/phase2_sf05_source_frame_summary_v1.json"
    sf05_gap = ROOT / "evidence/meta_extraction/phase2_sf05_source_frame_gap_v1.csv"
    sf05_universe = ROOT / "evidence/meta_extraction/phase2_sf05_primary_study_universe_v1.csv"
    for p in (sf05_summary, sf05_gap, sf05_universe):
        assert p.is_file(), p
    s5 = json.loads(sf05_summary.read_text(encoding="utf-8"))
    assert s5["materialized"]["population_rows"] == 177
    assert s5["materialized"]["unique_source_selected_studies"] == 65
    assert s5["materialized"]["unique_source_meta_analysis_studies"] == 31
    assert s5["materialized"]["title_method_multilayer_screen_hints"] == 25
    assert s5["minimum_missing_identity_count"] == 9
    assert s5["denominator_status"] == "incomplete_outcome_blind_source_frame"
    assert s5["effect_outcomes_opened_for_egwee_phase2"] is False

    screen_rows = rows(SF05_SCREEN)
    expected_screen_decisions = {
        "1": "closed_no_fragmentation_reference_contrast",
        "2": "closed_no_fragmentation_reference_contrast",
        "4": "advance_full_text_quantitative_screen",
        "8": "closed_no_fragmentation_reference_contrast",
        "10": "closed_no_fragmentation_reference_contrast",
        "11": "advance_full_text_exposure_screen",
        "15": "closed_no_fragmentation_reference_contrast",
        "20": "advance_full_text_exposure_screen",
        "24": "closed_nonfragmentation_single_population_disturbance",
        "25": "closed_no_fragmentation_reference_contrast",
        "32": "advance_full_text_quantitative_screen",
        "42": "advance_full_text_quantitative_screen",
        "46": "closed_single_fragmented_unit",
        "49": "closed_existing_structural_hard_stop",
        "51": "closed_fragment_only_no_reference",
        "66": "closed_fragment_only_no_reference",
        "68": "closed_fragment_only_no_reference",
        "69": "closed_nonfragmentation_exposure",
        "71": "advance_full_text_quantitative_screen",
        "76": "advance_full_text_exposure_screen",
        "83": "advance_full_text_quantitative_screen",
        "85": "closed_no_fragmentation_reference_contrast",
        "86": "advance_full_text_exposure_screen",
        "93": "advance_full_text_quantitative_screen",
        "96": "closed_nonfragmentation_single_population_disturbance",
    }
    assert len(screen_rows) == s5["materialized"]["title_method_multilayer_screen_hints"] == 25
    assert {r["source_paper_id"] for r in screen_rows} == set(expected_screen_decisions)
    assert all(r["source_frame"] == "SF05" for r in screen_rows)
    assert {r["screen_wave"] for r in screen_rows} == {"1", "2"}
    assert sum(r["screen_wave"] == "1" for r in screen_rows) == 4
    assert sum(r["screen_wave"] == "2" for r in screen_rows) == 21
    assert all(r["screen_basis"] == "design_and_methods_only" for r in screen_rows)
    assert all(r["outcome_opened"] == "no" for r in screen_rows)
    assert all(r["outcome_blind_confirmation"] == "yes" for r in screen_rows)
    decisions = {r["source_paper_id"]: r["screen_decision"] for r in screen_rows}
    assert decisions == expected_screen_decisions
    assert sum(r["screen_decision"] == "advance_full_text_quantitative_screen" for r in screen_rows) == 6
    assert sum(r["screen_decision"] == "advance_full_text_exposure_screen" for r in screen_rows) == 4
    assert sum(r["screen_decision"].startswith("closed_") for r in screen_rows) == 15
    forbidden_reason_tokens = ("significance", "p-value", "effect direction", "effect magnitude")
    assert all(
        not any(token in r["decision_reason"].lower() for token in forbidden_reason_tokens)
        for r in screen_rows
    )

    screen_status = SF05_SCREEN_STATUS.read_text(encoding="utf-8")
    for token in (
        "design-screened: **25**",
        "advance to quantitative full-text screen: **6**",
        "advance to exposure/layer verification: **4**",
        "closed on design geometry: **15**",
        "flagged candidates still pending design screen: **0**",
        "newly admitted Phase-2 effects/clusters: **0**",
        "SF05-93 Parkia biglobosa",
        "SF05-32 Castanopsis sclerophylla",
        "SF05-71 Heliconia acuminata",
        "SF05-83 Oenocarpus bataua",
    ):
        assert token in screen_status, token

    audit = ROOT / "manuscript/META_ANALYSIS_PHASE2_SOURCE_FRAME_AUDIT_2026-09-18.md"
    assert audit.is_file()
    audit_text = audit.read_text(encoding="utf-8")
    for token in ("SF01", "SF02", "SF03", "SF04", "SF05", "SF06", "SF07", "row materialization"):
        assert token in audit_text, token

    print(
        "SYSTEMATIC_COVERAGE_EXPANSION_CONTRACT_OK "
        f"frames={len(coverage)} source_verified={len(seed_frames)} pair_gate={pair_gate['min_independent_programmes']} "
        f"moderators={len(moderators)} "
        f"recovery_targets={sum(r['phase2_status']=='registered_recovery_target' for r in recovery)} "
        f"hard_closed={sum(r['phase2_status']=='structural_closed' for r in recovery)} "
        f"sf05_screened={len(screen_rows)} sf05_advance={sum(r['screen_decision'].startswith('advance_') for r in screen_rows)}"
    )


if __name__ == "__main__":
    main()
