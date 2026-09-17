from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-17_COVERAGE_MODERATORS.md"
CONTRACT = ROOT / "manuscript/meta_analysis_coverage_contract.json"
SCHEMA = ROOT / "manuscript/meta_analysis_effect_schema.json"
PAIR_COVERAGE = ROOT / "evidence/meta_extraction/coverage_expansion_pair_coverage_v1.csv"
RECOVERY_PRIORITY = ROOT / "evidence/meta_extraction/coverage_expansion_recovery_priority_v1.csv"
SEED_SOURCES = ROOT / "evidence/meta_extraction/systematic_search_seed_sources_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
REGISTRY_ML020 = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_extension_ml020.csv"
ROBUSTNESS = ROOT / "manuscript/tables/table_s2_covariance_robustness.csv"
PRIMARY_EFFECTS = ROOT / "manuscript/tables/table_s3_primary_marginal_effects.csv"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (
        AMENDMENT,
        CONTRACT,
        SCHEMA,
        PAIR_COVERAGE,
        RECOVERY_PRIORITY,
        SEED_SOURCES,
        REGISTRY,
        REGISTRY_ML020,
        ROBUSTNESS,
        PRIMARY_EFFECTS,
        MANUSCRIPT,
    ):
        assert path.is_file(), path

    amendment = AMENDMENT.read_text(encoding="utf-8")
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    assert contract["schema_version"] == 1
    assert contract["frozen_on"] == "2026-09-17"
    assert contract["purpose"] == "systematic_coverage_and_moderator_expansion_not_significance_repair"

    baseline = contract["baseline"]
    assert baseline["n_primary_clusters"] == 5
    assert baseline["primary_cluster_ids"] == ["ML001", "ML002", "ML003", "ML014", "ML020"]
    assert baseline["n_primary_effects"] == 17
    assert abs(baseline["primary_fisher_p"] - 0.01212432) < 1e-12
    assert abs(baseline["omit_ML001_p"] - 0.18194353) < 1e-12
    assert abs(baseline["zero_covariance_p"] - 0.03860161) < 1e-12
    assert abs(baseline["covariance_free_bound_p"] - 0.28061178) < 1e-12
    assert baseline["gradient_generalisation_cluster"] == "ML015"
    assert baseline["baseline_role"] == "frozen_current_Journal_of_Ecology_result"

    expected_domains = {
        "pollination_and_reproductive_success_fragmentation",
        "adult_plant_genetic_consequences_fragmentation",
        "progeny_genetic_and_biological_quality_fragmentation",
        "fine_scale_spatial_genetic_structure_fragmentation_degradation",
        "updated_land_use_pollination_male_female_fitness",
        "insect_pollinator_fragmentation_abundance_richness",
    }
    search = contract["search_universe"]
    assert search["cutoff_date"] == "2026-09-17"
    assert set(search["seed_domains"]) == expected_domains
    assert len(search["seed_domains"]) == 6
    assert search["rolling_inclusion_after_cutoff"] is False
    assert "terminal_state" in search["completion_rule"]

    seed_rows = rows(SEED_SOURCES)
    assert len(seed_rows) == 6
    assert [r["seed_id"] for r in seed_rows] == ["SS001", "SS002", "SS003", "SS004", "SS005", "SS006"]
    by_seed = {r["seed_id"]: r for r in seed_rows}
    assert by_seed["SS001"]["doi_or_dataset"] == "10.1111/j.1461-0248.2006.00927.x"
    assert by_seed["SS002"]["doi_or_dataset"] == "10.1111/j.1365-294X.2008.03971.x"
    assert by_seed["SS003"]["doi_or_dataset"] == "10.1111/ele.13272"
    assert by_seed["SS004"]["doi_or_dataset"] == "10.1093/aobpla/plad019"
    assert by_seed["SS005"]["doi_or_dataset"] == "10.1093/aob/mcae076"
    assert "10.1111/1365-2664.70161" in by_seed["SS006"]["doi_or_dataset"]
    assert "10.5061/dryad.dz08kps9p" in by_seed["SS006"]["doi_or_dataset"]
    assert all(r["candidate_use"] for r in seed_rows)

    expected_pairs = {"I-F", "C-F", "G_adult-G_offspring", "G_adult-mean(I,F)"}
    assert set(contract["priority_pair_cells"]) == expected_pairs

    expected_moderators = {
        "self_compatibility",
        "autonomous_reproductive_assurance",
        "life_form",
        "longevity_class",
        "fragmentation_age_years",
        "pollination_vector",
        "fragmentation_component",
        "direct_process_measurement",
        "cohort",
    }
    assert set(contract["moderator_fields"]) == expected_moderators

    gates = contract["moderator_opening_gates"]
    assert gates["one_moderator_at_a_time"] is True
    assert gates["pair_specific_categorical_min_independent_systems"] == 10
    assert gates["pair_specific_categorical_min_per_retained_category"] == 4
    assert gates["pair_specific_continuous_min_independent_systems"] == 10
    assert gates["multivariable_min_independent_multilayer_systems"] == 20
    assert gates["failed_gate_label"] == "not_estimable_at_frozen_information_threshold"
    assert gates["thresholds_are_power_guarantees"] is False

    assert set(contract["structural_hard_stops"]) == {"ML009", "ML013"}
    expected_forbidden = {
        "restore_leave_one_out_significance",
        "reduce_global_p_value",
        "replace_null_cluster_after_outcome_inspection",
        "continue_search_because_moderator_is_nonsignificant",
        "stop_search_because_moderator_is_significant",
    }
    assert set(contract["forbidden_expansion_triggers"]) == expected_forbidden

    terminal = set(contract["terminal_candidate_states"])
    assert terminal == {
        "admitted_effect",
        "admitted_multilayer_cluster",
        "admitted_gradient_generalisation",
        "closed_recoverability",
        "closed_structural",
        "awaiting_author_data",
    }

    assert "does not justify searching for a sixth direct cluster" in amendment
    assert "Search-completion stopping rule" in amendment
    assert "not_estimable_at_frozen_information_threshold" in amendment
    assert "ML009" in amendment and "ML013" in amendment
    assert "does not validate the finite NEE operators" in amendment

    assert schema["schema_version"] == 3
    assert schema["coverage_amendment"] == "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-17_COVERAGE_MODERATORS.md"
    assert set(schema["moderator_fields"]) == expected_moderators
    assert schema["moderator_field_rule"] == "moderator_fields_are_nullable_metadata_and_do_not_change_effect_admissibility"
    assert schema["primary_effect_stream"] == "hedges_g_fragmented_minus_reference"
    assert schema["secondary_effect_stream"] == "fisher_z_correlation_with_fragmentation_severity"
    assert {
        "omnibus_layer_heterogeneity",
        "I_minus_F",
        "C_minus_F",
        "G_adult_minus_G_offspring",
        "G_adult_minus_contemporary_interaction_function",
        "process_function_covariance",
    } == set(schema["primary_tests"])

    pair_rows = rows(PAIR_COVERAGE)
    assert {r["pair_id"] for r in pair_rows} == expected_pairs
    by_pair = {r["pair_id"]: r for r in pair_rows}
    assert int(by_pair["I-F"]["current_independent_direct_systems"]) == 1
    assert by_pair["I-F"]["current_system_ids"] == "ML020"
    assert int(by_pair["C-F"]["current_independent_direct_systems"]) == 2
    assert set(by_pair["C-F"]["current_system_ids"].split(";")) == {"ML001", "ML002"}
    assert int(by_pair["G_adult-G_offspring"]["current_independent_direct_systems"]) == 1
    assert by_pair["G_adult-G_offspring"]["current_system_ids"] == "ML003"
    assert int(by_pair["G_adult-mean(I,F)"]["current_independent_direct_systems"]) == 0
    assert all(r["analysis_opening_gate"] == "10_independent_informative_systems" for r in pair_rows)
    assert all("not a significance target" in r["gate_interpretation"] for r in pair_rows)

    priority_rows = rows(RECOVERY_PRIORITY)
    by_cluster = {r["cluster_id"]: r for r in priority_rows}
    assert [r["cluster_id"] for r in priority_rows[:8]] == [
        "ML006", "ML008", "ML007", "ML011", "ML012", "ML010", "ML004", "ML005"
    ]
    assert by_cluster["ML009"]["reopen_allowed"] == "no_without_new_independent_replication"
    assert by_cluster["ML013"]["reopen_allowed"] == "no_without_new_independent_replication"
    assert "I-F" in by_cluster["ML006"]["target_information_cells"]
    assert by_cluster["ML008"]["target_information_cells"] == "I-F"

    registry = rows(REGISTRY) + rows(REGISTRY_ML020)
    assert len({r["cluster_id"] for r in registry}) == len(registry)
    admitted = {
        r["cluster_id"]
        for r in registry
        if r["cluster_status"] == "admissible_multilayer_cluster"
    }
    assert admitted == {"ML001", "ML002", "ML003", "ML014", "ML020"}
    gradient = next(r for r in registry if r["cluster_id"] == "ML015")
    assert gradient["cluster_status"] == "gradient_generalisation_multilayer_cluster"
    ml009 = next(r for r in registry if r["cluster_id"] == "ML009")
    ml013 = next(r for r in registry if r["cluster_id"] == "ML013")
    assert ml009["cluster_status"] == "single_landscape_per_condition_no_replication"
    assert ml013["cluster_status"] == "single_continuous_reference_population_no_replication"

    robustness = {r["regime"]: r for r in rows(ROBUSTNESS)}
    assert abs(float(robustness["frozen_paired_covariance_proxy"]["full_fisher_p"]) - 0.01212432410511315) < 1e-15
    assert abs(float(robustness["frozen_paired_covariance_proxy"]["omit_ML001_p"]) - 0.18194352880824008) < 1e-15
    assert abs(float(robustness["zero_covariance"]["full_fisher_p"]) - 0.038601605823083425) < 1e-15
    assert abs(float(robustness["cauchy_schwarz_certification_bound"]["full_fisher_p"]) - 0.280611779992871) < 1e-15

    primary_effects = rows(PRIMARY_EFFECTS)
    assert len(primary_effects) == 17
    assert {r["cluster_id"] for r in primary_effects} == {"ML001", "ML002", "ML003", "ML014", "ML020"}

    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    assert "five independent direct fragmented-versus-reference clusters comprising 17 Hedges-g marginal effects" in manuscript
    assert "A sixth cluster was not sought merely because removal of ML001 remained non-significant" in manuscript

    print(
        "EGWEE coverage/moderator expansion contract: PASS; "
        "frozen 5-cluster baseline preserved; 6-domain systematic search and moderator gates locked; "
        "significance-repair triggers forbidden"
    )


if __name__ == "__main__":
    main()
