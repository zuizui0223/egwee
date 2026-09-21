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
HELICONIA_CHECK = ROOT / "scripts/check_phase2_sf05_71_heliconia.py"
HELICONIA_STATUS = ROOT / "manuscript/PHASE2_SF05_71_HELICONIA_RECOVERY_2026-09-19.md"
HELICONIA_CONTRACT = ROOT / "manuscript/SF05_71_HELICONIA_PHASE2_RECOVERY_CONTRACT.md"
PRUNUS_CHECK = ROOT / "scripts/check_phase2_cf01_prunus_2014.py"
PRUNUS_STATUS = ROOT / "manuscript/PHASE2_CF01_PRUNUS_2014_RECOVERY_2026-09-19.md"
PRUNUS_CONTRACT = ROOT / "manuscript/CF01_GPAIR_002_PRUNUS_2014_PHASE2_RECOVERY_CONTRACT.md"
KAKAMEGA_CHECK = ROOT / "scripts/check_phase2_cf01_prunus_kakamega_2008.py"
KAKAMEGA_STATUS = ROOT / "manuscript/PHASE2_CF01_PRUNUS_KAKAMEGA_2008_RECOVERY_2026-09-19.md"
KAKAMEGA_CONTRACT = ROOT / "manuscript/CF01_GPAIR_003_PRUNUS_KAKAMEGA_2008_PHASE2_RECOVERY_CONTRACT.md"
GPAIR_SYNTHESIS_CHECK = ROOT / "scripts/check_phase2_gpair_synthesis.py"
GPAIR_SYNTHESIS_STATUS = ROOT / "manuscript/PHASE2_GPAIR_SYNTHESIS_2026-09-19.md"
GPAIR_SYNTHESIS_AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-19_GPAIR_SYNTHESIS.md"
QUANT_GATE = ROOT / "evidence/meta_extraction/phase2_sf05_quantitative_gate_v1.csv"
CASTANOPSIS_STATUS = ROOT / "manuscript/PHASE2_SF05_32_CASTANOPSIS_GATE_2026-09-19.md"
OENOCARPUS_STATUS = ROOT / "manuscript/PHASE2_SF05_83_OENOCARPUS_GATE_2026-09-19.md"
PRIMULA_STATUS = ROOT / "manuscript/PHASE2_SF05_42_PRIMULA_GATE_2026-09-19.md"
MILICIA_STATUS = ROOT / "manuscript/PHASE2_SF05_4_MILICIA_GATE_2026-09-19.md"
BROSIMUM_GPAIR_STATUS = ROOT / "manuscript/PHASE2_ML002_BROSIMUM_GPAIR_RECONCILIATION_2026-09-19.md"
CROSSFRAME_IDENTITY = ROOT / "evidence/meta_extraction/phase2_crossframe_publication_identity_v1.csv"
CROSSFRAME_DUPLICATES = ROOT / "evidence/meta_extraction/phase2_crossframe_candidate_duplicates_v1.csv"
CROSSFRAME_SUMMARY = ROOT / "evidence/meta_extraction/phase2_crossframe_identity_summary_v1.json"
CROSSFRAME_STATUS = ROOT / "manuscript/PHASE2_CROSSFRAME_IDENTITY_LEDGER_2026-09-20.md"
SF03_BLOCKER = ROOT / "manuscript/PHASE2_SF03_WILEY_BLOCKER_2026-09-20.md"
METADATA_SCREEN_SUMMARY = ROOT / "evidence/meta_extraction/phase2_metadata_screen_summary_v1.json"
IF_SCREEN_QUEUE = ROOT / "evidence/meta_extraction/phase2_if_fragmentation_screen_queue_v1.csv"
IF_DESIGN_SCREEN = ROOT / "evidence/meta_extraction/phase2_if_design_screen_v1.csv"
IF_WAVE1_STATUS = ROOT / "manuscript/PHASE2_IF_DESIGN_SCREEN_WAVE1_2026-09-20.md"
IF_WAVE2_STATUS = ROOT / "manuscript/PHASE2_IF_DESIGN_SCREEN_WAVE2_2026-09-20.md"
IF_WAVE3_STATUS = ROOT / "manuscript/PHASE2_IF_DESIGN_SCREEN_WAVE3_2026-09-20.md"
IF_WAVE4_STATUS = ROOT / "manuscript/PHASE2_IF_DESIGN_SCREEN_WAVE4_2026-09-20.md"
IF_QUANT_GATE = ROOT / "evidence/meta_extraction/phase2_if_quantitative_gate_v1.csv"
IF_QUANT_STATUS = ROOT / "manuscript/PHASE2_IF_QUANTITATIVE_GATE_2026-09-20.md"

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
    for path in (CONTRACT, AMENDMENT, COVERAGE, PAIR_COVERAGE, MODERATORS, RECOVERY, SF05_SCREEN, SF05_SCREEN_STATUS, PARKIA_CHECK, PARKIA_STATUS, PARKIA_CONTRACT, HELICONIA_CHECK, HELICONIA_STATUS, HELICONIA_CONTRACT, PRUNUS_CHECK, PRUNUS_STATUS, PRUNUS_CONTRACT, KAKAMEGA_CHECK, KAKAMEGA_STATUS, KAKAMEGA_CONTRACT, GPAIR_SYNTHESIS_CHECK, GPAIR_SYNTHESIS_STATUS, GPAIR_SYNTHESIS_AMENDMENT, QUANT_GATE, CASTANOPSIS_STATUS, OENOCARPUS_STATUS, PRIMULA_STATUS, MILICIA_STATUS, BROSIMUM_GPAIR_STATUS, CROSSFRAME_IDENTITY, CROSSFRAME_DUPLICATES, CROSSFRAME_SUMMARY, CROSSFRAME_STATUS, SF03_BLOCKER, METADATA_SCREEN_SUMMARY, IF_SCREEN_QUEUE, IF_DESIGN_SCREEN, IF_WAVE1_STATUS, IF_WAVE2_STATUS, IF_WAVE3_STATUS, IF_WAVE4_STATUS, IF_QUANT_GATE, IF_QUANT_STATUS, SCHEMA):
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
    assert cf01["status"] == "partial_targeted_citation_expansion_executed_full_frame_incomplete"
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
    assert int(by_pair["G_adult-G_offspring"]["current_independent_direct_systems"]) == 5
    assert set(by_pair["G_adult-G_offspring"]["current_system_ids"].split(";")) == {"ML003", "P2_SF05_93", "P2_SF05_71", "P2_CF01_GPAIR_002", "P2_CF01_GPAIR_003"}
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

    heliconia_proc = subprocess.run(
        [sys.executable, str(HELICONIA_CHECK)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "PHASE2_SF05_71_HELICONIA_OK" in heliconia_proc.stdout
    assert "full3_covariance=PD" in heliconia_proc.stdout
    assert "pair_covariance=PD" in heliconia_proc.stdout
    heliconia_status = HELICONIA_STATUS.read_text(encoding="utf-8")
    for token in (
        "full covariance-aware three-layer Phase-2 cluster",
        "increases from 2 to **3 independent programmes**",
        "below the quantitative meta-analysis gate at 3/5",
        "does **not** enter or alter the frozen Phase-1 five-cluster Fisher synthesis",
    ):
        assert token in heliconia_status, token

    prunus_proc = subprocess.run(
        [sys.executable, str(PRUNUS_CHECK)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "PHASE2_CF01_PRUNUS_2014_OK" in prunus_proc.stdout
    assert "pair_covariance=PD" in prunus_proc.stdout
    prunus_status = PRUNUS_STATUS.read_text(encoding="utf-8")
    for token in (
        "pair-specific covariance-aware Phase-2 cluster",
        "4 independent programmes",
        "remains closed at **4/5**",
        "Afrocarpus remains a registered prospective candidate",
    ):
        assert token in prunus_status, token

    kakamega_proc = subprocess.run(
        [sys.executable, str(KAKAMEGA_CHECK)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "PHASE2_CF01_PRUNUS_KAKAMEGA_2008_OK" in kakamega_proc.stdout
    assert "pair_covariance=PD" in kakamega_proc.stdout
    assert "gate=5/5" in kakamega_proc.stdout
    kakamega_status = KAKAMEGA_STATUS.read_text(encoding="utf-8")
    for token in (
        "pair-specific covariance-aware Phase-2 cluster",
        "5 independent programmes",
        "5-programme analysis-opening gate is now met",
        "does **not** enter or alter the frozen Phase-1 five-cluster Fisher synthesis",
    ):
        assert token in kakamega_status, token

    gpair_proc = subprocess.run(
        [sys.executable, str(GPAIR_SYNTHESIS_CHECK)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "PHASE2_GPAIR_SYNTHESIS_OK" in gpair_proc.stdout
    assert "K=5" in gpair_proc.stdout
    assert "directional_lag=false" in gpair_proc.stdout
    gpair_status = GPAIR_SYNTHESIS_STATUS.read_text(encoding="utf-8")
    for token in (
        "mean contrast = +0.129",
        "does **not** resolve a common directional cohort lag",
        "Moderator models remain closed at K=5",
        "systematic search universe is not yet complete",
    ):
        assert token in gpair_status, token

    qrows = rows(QUANT_GATE)
    qby = {r["source_paper_id"]: r for r in qrows}
    assert set(qby) == {"93", "32", "71", "83", "42", "4"}
    assert qby["93"]["gate_status"] == "recovered_pair_admissible"
    assert qby["71"]["gate_status"] == "recovered_full_three_layer_covariance_admissible"
    assert qby["32"]["gate_status"] == "closed_insufficient_fragmentation_unit_replication"
    assert qby["83"]["gate_status"] == "closed_no_prespecified_pair_and_reference_nonindependence"
    assert qby["42"]["gate_status"] == "closed_no_prespecified_pair_common_frame"
    assert qby["4"]["gate_status"] == "closed_exposure_not_common_fragmentation_and_no_prespecified_pair"
    assert {pid for pid, r in qby.items() if r["gate_status"] == "pending_full_text_quantitative_gate"} == set()
    assert sum(r["effect_calculation_opened"] == "yes" for r in qrows) == 2
    cast_status = CASTANOPSIS_STATUS.read_text(encoding="utf-8")
    assert "closed for quantitative Phase-2 admission" in cast_status
    assert "six cohorts cannot" not in cast_status.lower() or "fragmentation-level independent unit remains the site" in cast_status

    oeno_status = OENOCARPUS_STATUS.read_text(encoding="utf-8")
    assert "closed for the current prespecified Phase-2 pair families" in oeno_status
    assert "do not create 10 independent continuous-forest landscapes" not in oeno_status.lower() or "one large continuous-forest reserve" in oeno_status
    assert "No primary Phase-2 pair count changes." in oeno_status

    primula_status = PRIMULA_STATUS.read_text(encoding="utf-8")
    assert "closed for the current prespecified Phase-2 pair families" in primula_status
    assert "G_adult-F" in primula_status
    assert "It does not change any pair-specific programme count." in primula_status

    milicia_status = MILICIA_STATUS.read_text(encoding="utf-8")
    assert "closed for the current prespecified Phase-2 pair families" in milicia_status
    assert "Indirect gene-dispersal distance is estimable only for Mindourou and Djoum" in milicia_status
    assert "no new pair family is created after source inspection" in milicia_status

    brosimum_gpair_status = BROSIMUM_GPAIR_STATUS.read_text(encoding="utf-8")
    for token in (
        "blocked_publication_raw_genotype_reconciliation",
        "current G_adult-G_offspring coverage: **5/5**",
        "programme increment from Brosimum: **0**",
        "0/4 predeclared estimators reproduce all four publication cells",
    ):
        assert token in brosimum_gpair_status, token
    assert "ML002" not in set(by_pair["G_adult-G_offspring"]["current_system_ids"].split(";"))

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

    sf04_summary = ROOT / "evidence/meta_extraction/phase2_sf04_source_frame_summary_v1.json"
    sf04_universe = ROOT / "evidence/meta_extraction/phase2_sf04_publication_universe_v1.csv"
    sf04_status = ROOT / "manuscript/PHASE2_SF04_MATERIALIZATION_2026-09-20.md"
    for p in (sf04_summary, sf04_universe, sf04_status):
        assert p.is_file(), p
    s4 = json.loads(sf04_summary.read_text(encoding="utf-8"))
    assert s4["materialized"]["deduplicated_source_publications"] == 38
    assert s4["materialized"]["unique_species"] == 38
    assert s4["materialized"]["total_source_case_rows"] == 92
    assert s4["materialized"]["allelic_case_rows"] == 42
    assert s4["materialized"]["heterozygosity_case_rows"] == 50
    assert s4["outcome_fields_materialized"] is False
    assert s4["excluded_source_columns"] == ["Xe", "Se", "Ne", "Xc", "Sc", "Nc"]
    s4rows = rows(sf04_universe)
    assert len(s4rows) == 38
    assert all(r["source_frame"] == "SF04" for r in s4rows)
    assert all(r["outcome_opened"] == "no" for r in s4rows)
    assert all(r["multilayer_screen_status"] == "pending_title_abstract_methods_screen" for r in s4rows)

    sf06_summary = ROOT / "evidence/meta_extraction/phase2_sf06_source_frame_summary_v1.json"
    sf06_universe = ROOT / "evidence/meta_extraction/phase2_sf06_publication_universe_v1.csv"
    sf06_status = ROOT / "manuscript/PHASE2_SF06_MATERIALIZATION_2026-09-20.md"
    for p in (sf06_summary, sf06_universe, sf06_status):
        assert p.is_file(), p
    s6 = json.loads(sf06_summary.read_text(encoding="utf-8"))
    assert s6["materialized"]["source_effect_rows"] == 426
    assert s6["materialized"]["deduplicated_source_publications"] == 255
    assert s6["materialized"]["unique_species"] == 261
    assert s6["materialized"]["response_row_counts"] == {
        "Female fitness": 267,
        "Pollination": 71,
        "Male fitness": 88,
    }
    assert s6["outcome_fields_materialized"] is False
    assert s6["excluded_source_fields"] == ["Hedges_d", "V(d)"]
    s6rows = rows(sf06_universe)
    assert len(s6rows) == 255
    assert all(r["source_frame"] == "SF06" for r in s6rows)
    assert all(r["outcome_opened"] == "no" for r in s6rows)
    assert all(r["multilayer_screen_status"] == "pending_title_abstract_methods_screen" for r in s6rows)

    cross_summary = json.loads(CROSSFRAME_SUMMARY.read_text(encoding="utf-8"))
    assert cross_summary["input_rows"] == {"SF04": 38, "SF05": 65, "SF06": 255, "total": 358}
    assert cross_summary["cross_frame_candidate_groups"] == 10
    assert cross_summary["confirmed_same_publication_groups"] == 7
    assert cross_summary["confirmed_distinct_collision_groups"] == 3
    assert cross_summary["unique_screening_identity_units"] == 351
    assert cross_summary["existing_egwee_linked_source_rows"] == 12
    assert cross_summary["existing_egwee_identity_units"] == 10
    assert cross_summary["not_yet_linked_screening_identity_units"] == 341
    assert cross_summary["effect_outcomes_opened"] is False
    assert set(cross_summary["confirmed_duplicate_group_keys"]) == {
        "bartlewicz|2015", "browne|2015", "collevatti|2014", "giombini|2017",
        "lompo|2020", "pellegrino|2015", "zhao|2009",
    }
    assert set(cross_summary["confirmed_distinct_group_keys"]) == {
        "chung|2007", "jacquemyn|2006", "jacquemyn|2009",
    }

    cross_rows = rows(CROSSFRAME_IDENTITY)
    assert len(cross_rows) == 358
    assert len({r["canonical_identity_key"] for r in cross_rows}) == 351
    assert all(r["outcome_opened"] == "no" for r in cross_rows)
    assert len({r["canonical_identity_key"] for r in cross_rows if r["existing_egwee_programme"]}) == 10
    assert all(
        r["identity_action"] == "link_existing_egwee_programme_do_not_recruit_as_new"
        for r in cross_rows if r["existing_egwee_programme"]
    )
    dup_rows = rows(CROSSFRAME_DUPLICATES)
    assert len(dup_rows) == 10
    assert sum(r["group_status"] == "confirmed_same_publication" for r in dup_rows) == 7
    assert sum(r["group_status"] == "confirmed_distinct_publications" for r in dup_rows) == 3

    cross_status = CROSSFRAME_STATUS.read_text(encoding="utf-8")
    for token in (
        "358 source-frame rows to 351 screening identity units",
        "**10** are already linked to known EGWEE programmes",
        "**341** identities not yet linked",
        "Zhao 2009",
    ):
        assert token in cross_status, token

    metadata_summary = json.loads(METADATA_SCREEN_SUMMARY.read_text(encoding="utf-8"))
    assert metadata_summary["counts"] == {
        "canonical_identity_units": 351,
        "existing_egwee_programmes": 10,
        "unresolved_identity_units": 341,
        "unresolved_multilayer_metadata_hints": 61,
        "unresolved_IF_metadata_hints": 36,
        "primary_IF_fragmentation_design_queue": 32,
        "secondary_IF_nonfragmentation": 4,
        "other_multilayer_metadata_hints": 25,
        "single_layer_or_no_pair_hint": 280,
    }
    assert metadata_summary["effect_outcomes_opened"] is False

    if_queue = rows(IF_SCREEN_QUEUE)
    assert len(if_queue) == 32
    assert [r["queue_id"] for r in if_queue] == [f"IFQ{i:03d}" for i in range(1, 33)]
    assert all(r["screening_status"] == "pending_title_abstract_methods_design_screen" for r in if_queue)
    assert all(r["outcome_opened"] == "no" for r in if_queue)

    if_screen = rows(IF_DESIGN_SCREEN)
    assert len(if_screen) == 32
    assert [r["queue_id"] for r in if_screen] == [f"IFQ{i:03d}" for i in range(1, 33)]
    assert {r["screen_wave"] for r in if_screen} == {"1", "2", "3", "4"}
    assert all(sum(r["screen_wave"] == str(wave) for r in if_screen) == 8 for wave in range(1, 5))
    assert all(r["screen_basis"] == "title_abstract_methods_only" for r in if_screen)
    assert all(r["outcome_opened"] == "no" for r in if_screen)
    assert all(r["outcome_blind_confirmation"] == "yes" for r in if_screen)

    if_decisions = {r["queue_id"]: r["screen_decision"] for r in if_screen}
    expected_if_decisions = {
        "IFQ001": "closed_no_source_defined_fragmentation_contrast",
        "IFQ002": "advance_programme_decomposition_screen",
        "IFQ003": "advance_full_text_quantitative_screen",
        "IFQ004": "closed_single_fragment_edge_interior_pseudoreplication",
        "IFQ005": "closed_reference_landscape_nonindependence",
        "IFQ006": "advance_full_text_quantitative_screen",
        "IFQ007": "advance_full_text_quantitative_screen",
        "IFQ008": "advance_full_text_quantitative_screen",
        "IFQ009": "closed_no_source_defined_fragmentation_contrast",
        "IFQ010": "closed_gradient_only_no_reference",
        "IFQ011": "closed_no_source_defined_fragmentation_contrast",
        "IFQ012": "closed_no_source_defined_fragmentation_contrast",
        "IFQ013": "closed_gradient_only_no_reference",
        "IFQ014": "closed_gradient_only_no_reference",
        "IFQ015": "advance_full_text_quantitative_screen",
        "IFQ016": "closed_gradient_only_no_reference",
        "IFQ017": "closed_single_reference_unit",
        "IFQ018": "closed_no_source_defined_fragmentation_contrast",
        "IFQ019": "closed_gradient_only_no_reference",
        "IFQ020": "advance_full_text_quantitative_screen",
        "IFQ021": "closed_no_source_defined_fragmentation_contrast",
        "IFQ022": "advance_full_text_quantitative_screen",
        "IFQ023": "closed_gradient_only_no_reference",
        "IFQ024": "closed_gradient_only_no_reference",
        "IFQ025": "closed_no_source_defined_fragmentation_contrast",
        "IFQ026": "closed_gradient_only_no_reference",
        "IFQ027": "closed_gradient_only_no_reference",
        "IFQ028": "closed_gradient_only_no_reference",
        "IFQ029": "closed_single_fragmented_landscape_no_reference",
        "IFQ030": "closed_gradient_only_no_reference",
        "IFQ031": "closed_no_source_defined_fragmentation_contrast",
        "IFQ032": "closed_no_common_IF_frame_and_no_fragmentation_contrast",
    }
    assert if_decisions == expected_if_decisions
    assert sum(r["screen_decision"] == "advance_full_text_quantitative_screen" for r in if_screen) == 7
    assert sum(r["screen_decision"].startswith("closed_") for r in if_screen) == 24
    assert sum(r["screen_decision"] == "advance_programme_decomposition_screen" for r in if_screen) == 1

    for status_path, tokens in (
        (IF_WAVE1_STATUS, (
            "screened in wave 1: **8**",
            "advance to quantitative full-text screen: **4**",
            "advance to programme decomposition/crosswalk: **1**",
            "closed on design geometry/exposure: **3**",
        )),
        (IF_WAVE2_STATUS, (
            "screened in wave 2: **8**",
            "advance to quantitative full-text screen: **1**",
            "design-screened: **16 / 32**",
        )),
        (IF_WAVE3_STATUS, (
            "screened in wave 3: **8**",
            "advance to quantitative full-text screen: **2**",
            "design-screened: **24 / 32**",
            "pending design screen: **8**",
        )),
        (IF_WAVE4_STATUS, (
            "screened in wave 4: **8**",
            "design-screened: **32 / 32**",
            "pending design screen: **0**",
            "direct/factor-specific quantitative-design candidates: **7**",
            "closed from direct I-F family on exposure/independent-unit/common-frame geometry: **24**",
        )),
    ):
        status_text = status_path.read_text(encoding="utf-8")
        for token in tokens:
            assert token in status_text, (status_path, token)

    if_quant = rows(IF_QUANT_GATE)
    assert [r["queue_id"] for r in if_quant] == ["IFQ003", "IFQ006", "IFQ007", "IFQ008", "IFQ015", "IFQ020", "IFQ022"]
    assert all(r["design_screen_status"] == "design_passed" for r in if_quant)
    assert all(r["effect_calculation_opened"] == "no" for r in if_quant)
    assert all(r["pair_programme_admitted"] == "no" for r in if_quant)
    assert all(int(r["pair_programme_increment"]) == 0 for r in if_quant)
    qstatus = {r["queue_id"]: r["quantitative_gate_status"] for r in if_quant}
    assert qstatus == {
        "IFQ003": "closed_patch_level_IF_values_not_tabulated_no_preregistered_digitization",
        "IFQ006": "blocked_dispersion_unit_not_fragmentation_level_verified",
        "IFQ007": "blocked_dispersion_unit_not_fragmentation_level_verified",
        "IFQ008": "closed_site_level_IF_dispersion_not_recoverable_model_contrast_not_force_standardised",
        "IFQ015": "closed_population_level_F_values_dispersion_not_recoverable_under_current_contract",
        "IFQ020": "blocked_factorial_cell_replication_and_between_population_dispersion_not_recovered_publicly",
        "IFQ022": "blocked_site_allocation_and_site_level_dispersion_not_recovered_publicly",
    }

    if_quant_status = IF_QUANT_STATUS.read_text(encoding="utf-8")
    for token in (
        "Seven records passed",
        "None is yet quantitatively admitted",
        "direct I-F programme coverage: **1/5**",
        "effect calculations opened from unresolved dispersion: **0**",
        "Design screening is complete at 32/32",
        "20 forest patches",
        "Erica, Myrtus, Phyteuma and Psychotria are now fail-closed",
        "All seven design-passing I-F candidates are now quantitatively resolved as closed or blocked",
        "design-passing candidates with unresolved admission status: **0**",
        "3 fragmented forest sites",
        "3 continuous forest sites",
    ):
        assert token in if_quant_status, token

    sf03_blocker = SF03_BLOCKER.read_text(encoding="utf-8")
    for token in (
        "source verified but row-materialization access-blocked",
        "Suppinfo.pdf",
        "AppendixS1.pdf",
        "HTTP 403",
    ):
        assert token in sf03_blocker, token

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
        f"sf05_screened={len(screen_rows)} sf05_advance={sum(r['screen_decision'].startswith('advance_') for r in screen_rows)} "
        f"crossframe_identity_units={cross_summary['unique_screening_identity_units']} "
        f"crossframe_unlinked={cross_summary['not_yet_linked_screening_identity_units']} "
        f"if_screened={len(if_screen)} if_design_pass={sum(r['screen_decision']=='advance_full_text_quantitative_screen' for r in if_screen)} "
        f"if_quant_admitted={sum(r['pair_programme_admitted']=='yes' for r in if_quant)}"
    )


if __name__ == "__main__":
    main()
