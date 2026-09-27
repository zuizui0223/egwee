from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manuscript/submission_freeze_manifest_v1.json"
FREEZE_NOTE = ROOT / "manuscript/SUBMISSION_FREEZE_2026-09-27.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
IF_CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
BOTTLENECK_CENSUS = ROOT / "evidence/meta_extraction/ecological_mating_function_programme_census_v1.csv"
PROCESS_FUNCTION_CENSUS = ROOT / "evidence/meta_extraction/ecological_process_function_programme_census_v1.csv"
CANONICAL_CENSUS_NOTE = ROOT / "manuscript/ECOLOGICAL_PROCESS_FUNCTION_CENSUS_2026-09-27.md"
METADATA = ROOT / "manuscript/meta_analysis_submission_metadata.md"
README = ROOT / "README.md"
FIGURE_BUILDER = ROOT / "scripts/build_journal_of_ecology_figures.py"
FIGURE_CAPTIONS = ROOT / "manuscript/JOURNAL_OF_ECOLOGY_FIGURE_CAPTIONS.md"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = f"blob {len(data)}\0".encode("utf-8") + data
    return hashlib.sha1(payload).hexdigest()


def main() -> None:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    note = FREEZE_NOTE.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    if_census = IF_CENSUS.read_text(encoding="utf-8")
    bottleneck = BOTTLENECK_CENSUS.read_text(encoding="utf-8")
    process_function = PROCESS_FUNCTION_CENSUS.read_text(encoding="utf-8")
    canonical_note = CANONICAL_CENSUS_NOTE.read_text(encoding="utf-8")
    metadata = METADATA.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    builder = FIGURE_BUILDER.read_text(encoding="utf-8")
    captions = FIGURE_CAPTIONS.read_text(encoding="utf-8")

    assert m["schema_version"] == 3
    assert m["frozen_on"] == "2026-09-27"
    assert m["scientific_base_commit"] == "d2c5c37acf005c10341c4f7ee6551ea52eaa463f"

    assert git_blob_sha(MANUSCRIPT) == m["manuscript"]["blob_sha"]
    assert git_blob_sha(IF_CENSUS) == m["ecological_IF_census"]["blob_sha"]
    assert git_blob_sha(BOTTLENECK_CENSUS) == m["bottleneck_position_audit"]["blob_sha"]
    assert git_blob_sha(PROCESS_FUNCTION_CENSUS) == m["unified_process_function_census"]["blob_sha"]

    assert m["manuscript"]["title"] == "Variable life-cycle bottlenecks under habitat fragmentation: a cross-system synthesis of plant interaction, mating and reproduction"
    assert m["manuscript"]["target_journal"] == "Journal of Ecology"
    assert m["manuscript"]["main_text_words_at_freeze"] == 6619
    assert m["manuscript"]["abstract_words_at_freeze"] == 293
    assert manuscript.startswith("# " + m["manuscript"]["title"])

    direct = m["primary_direct"]
    assert direct["independent_clusters"] == 5
    assert direct["marginal_effects"] == 17
    assert direct["canonical_p"] == 0.01212432
    assert direct["omit_ML001_p"] == 0.18194353
    assert direct["zero_covariance_p"] == 0.03860161
    assert direct["covariance_free_bound_p"] == 0.28061178

    phase2 = m["phase2"]
    assert phase2["target_pair_candidates_screened"] == 360
    assert phase2["target_pair_candidates_total"] == 360
    assert phase2["pending_screens"] == 0
    assert phase2["direct_IF_programmes"] == 3
    assert phase2["direct_IF_gate"] == 5
    assert phase2["direct_CF_programmes"] == 2
    assert phase2["direct_CF_gate"] == 5
    assert phase2["gradient_programmes"] == 6
    assert phase2["gradient_primary_effects"] == 19

    unified = m["unified_process_function_census"]
    assert unified["independent_programmes"] == 12
    assert unified["pair_testable"] == 11
    assert unified["resolved"] == 4
    assert unified["unresolved"] == 7
    assert unified["not_testable"] == 1
    assert unified["resolved_downstream_F_dominant"] == 3
    assert unified["resolved_upstream_process_dominant"] == 1
    assert unified["interaction_quantity_programmes"] == 8
    assert unified["movement_or_mating_support_programmes"] == 4

    ec = m["ecological_IF_census"]
    assert ec["independent_programmes"] == 8
    assert ec["pair_testable"] == 7
    assert ec["resolved"] == 3
    assert ec["unresolved"] == 4
    assert ec["not_testable"] == 1
    assert ec["resolved_F_more_negative_than_I"] == 3
    assert ec["resolved_I_more_negative_than_F"] == 0
    assert ec["quantity_only_I"] == 8
    assert ec["effective_mating_quality_I"] == 0

    bp = m["bottleneck_position_audit"]
    assert bp["independent_programmes"] == 4
    assert bp["resolved"] == 1
    assert bp["unresolved"] == 3
    assert bp["resolved_process_more_negative_than_F"] == 1
    assert bp["resolved_F_more_negative_than_process"] == 0

    for token in (
        "programmes=12",
        "resolved_downstream_F=3",
        "resolved_upstream_process=1",
    ):
        assert token not in process_function  # machine output belongs in checker, not CSV

    for token in (
        "downstream_function_dominant",
        "upstream_process_dominant",
        "unresolved_process_function_difference",
        "not_testable",
    ):
        assert token in process_function, token

    assert "12 independent programmes" in canonical_note
    assert "3 are downstream function-dominant" in canonical_note
    assert "1 is upstream process-dominant" in canonical_note
    assert "Delta_QE = Q - E" in canonical_note

    claims = json.dumps(m)
    for token in (
        "12 independent programmes",
        "3 downstream F-dominant and 1 upstream process-dominant",
        "one universal life-cycle bottleneck position",
        "cross-family pooling of Hedges-g and Fisher-z effects",
        "direct validation of finite EGWE or NEE operators",
    ):
        assert token in claims, token

    fresh = m["fresh_validation"]
    assert fresh["current_IF_programmes_burned"] == 8
    assert fresh["burned_auxiliary_process_function_programmes"] == 4
    assert fresh["min_fresh_programmes_per_effect_family"] == 5
    assert fresh["h2_v2_primary_contrast"] == "Delta_QE=Q-E"
    assert fresh["h2_v2_primary_direction"] == "Delta_QE>0"

    ft = m["figures_tables"]
    assert ft["main_figures"] == 4
    assert ft["main_tables"] == 2
    assert ft["figure4"] == "manuscript/figures/figure4_lifecycle_bottleneck_synthesis.svg"
    assert ft["table2"] == "manuscript/tables/table2_process_function_census.csv"
    assert "figure4_lifecycle_bottleneck_synthesis.svg" in builder
    assert "table2_process_function_census.csv" in builder
    assert "Figure 4. Fragmentation can shift the position" in captions
    assert "Table 2. Complete paired process–function bottleneck census" in captions

    ready = m["automated_readiness"]
    assert ready["validation_mode"] == "self_validating_current_ci"
    assert ready["submission_shape"] is True
    assert ready["double_anonymous"] is True
    assert ready["figures_tables_reproduced"] is True
    assert ready["anonymous_review_package_reproduced"] is True

    assert len(m["remaining_human_blockers"]) == 7
    assert "[ ] author/declaration metadata approved." in metadata
    assert "[x] double-anonymous submission package checked" in metadata
    assert "[x] final figure/table package completed" in metadata
    assert "Figures 1–4" in metadata
    assert "results_bearing_variable_lifecycle_bottleneck_synthesis" in metadata

    for token in (
        "12 independent programmes",
        "Bottleneck position is not fixed",
        "ΔQE",
    ):
        assert token.casefold() in (readme + "\n" + note).casefold(), token

    assert "Figure 4" in manuscript
    assert "unified 12-programme process–function census" in manuscript
    assert "three were downstream function-dominant and one" in manuscript

    print(
        "SUBMISSION_FREEZE_V3_OK "
        "direct=5 effects=17 phase2=360/360 process_function=12 testable=11 "
        "resolved=4 downstream=3 upstream=1 IF=8 quantity_only=8 effective=0 "
        "figures=4 tables=2 H2v2=Delta_QE_positive human_admin_pending=7"
    )


if __name__ == "__main__":
    main()
