from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manuscript/submission_freeze_manifest_v1.json"
STATE_NOTE = ROOT / "manuscript/SUBMISSION_FREEZE_2026-09-27.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
METADATA = ROOT / "manuscript/meta_analysis_submission_metadata.md"

SCALE_ENDPOINTS = ROOT / "evidence/meta_extraction/estimand_scale_sensitivity_v1.csv"
SCALE_ROBUSTNESS = ROOT / "evidence/meta_extraction/estimand_scale_robustness_v1.csv"
SCALE_SUMMARY = ROOT / "evidence/meta_extraction/estimand_scale_cluster_summary_v2.csv"
SCALE_FISHER = ROOT / "evidence/meta_extraction/estimand_scale_fisher_sensitivity_v2.csv"
SCALE_RESULT = ROOT / "manuscript/ESTIMAND_SCALE_ROBUSTNESS_2026-09-29.md"
SCALE_AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-29_EFFECT_SCALE.md"
BOTTLENECK_SCALE_TABLE = ROOT / "evidence/meta_extraction/bottleneck_scale_robustness_v1.csv"
BOTTLENECK_SCALE_NOTE = ROOT / "manuscript/BOTTLENECK_SCALE_ROBUSTNESS_2026-09-29.md"
IF_SIGN_CENSUS = ROOT / "evidence/meta_extraction/if_sign_geometry_census_v1.csv"
IF_SIGN_NOTE = ROOT / "manuscript/IF_SIGN_GEOMETRY_2026-09-29.md"
IF_SIGN_CHECKER = ROOT / "scripts/check_if_sign_geometry.py"

FIGURE_BUILDER = ROOT / "scripts/build_journal_of_ecology_figures.py"
FIGURE_CAPTIONS = ROOT / "manuscript/JOURNAL_OF_ECOLOGY_FIGURE_CAPTIONS.md"
ANON_BUILDER = ROOT / "scripts/build_anonymous_review_package.py"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = f"blob {len(data)}\0".encode("utf-8") + data
    return hashlib.sha1(payload).hexdigest()


def main() -> None:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    note = STATE_NOTE.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    metadata = METADATA.read_text(encoding="utf-8")
    scale_result = SCALE_RESULT.read_text(encoding="utf-8")
    amendment = SCALE_AMENDMENT.read_text(encoding="utf-8")
    builder = FIGURE_BUILDER.read_text(encoding="utf-8")
    captions = FIGURE_CAPTIONS.read_text(encoding="utf-8")
    anon = ANON_BUILDER.read_text(encoding="utf-8")

    assert m["schema_version"] == 5
    assert m["updated_on"] == "2026-09-29"
    assert m["status"] == "scientific_validation_pending_after_main_sign_geometry_promotion"
    assert m["submission_ready"] is False
    assert m["supersedes_submission_freeze"] is True
    sv = m["scientific_validation"]
    assert sv["previous_green_full_contract_run_id"] == 36542416391
    assert sv["previous_conclusion"] == "success"
    assert sv["current_revision_status"] == "pending"
    assert sv["current_revision_validated"] is False
    assert "main Figure 3" in sv["reason"]
    assert len(m["remaining_scientific_gate"]) == 1
    assert "current full CI green" in m["remaining_scientific_gate"][0]
    assert m["revision_base_commit"] == "e94722fe99dd40b1bebac42fa311f40d9e412ab4"

    man = m["manuscript"]
    assert git_blob_sha(MANUSCRIPT) == man["blob_sha"]
    assert man["title"] == "Habitat fragmentation across plant reproductive life cycles: species-specific interaction–function translation and scale-sensitive amplitudes"
    assert man["target_journal"] == "Journal of Ecology"
    assert man["main_text_words"] == 7999
    assert man["abstract_words"] == 332
    assert manuscript.startswith("# " + man["title"])

    g = m["historical_primary_g"]
    assert g["independent_clusters"] == 5
    assert g["marginal_effects"] == 17
    assert abs(g["full_fisher_p"] - 0.012124326106346261) < 1e-15
    assert abs(g["omit_ML001_p"] - 0.1819435271114386) < 1e-15

    s = m["authoritative_estimand_scale_audit"]
    assert git_blob_sha(SCALE_ENDPOINTS) == s["endpoint_table_blob_sha"]
    assert git_blob_sha(SCALE_ROBUSTNESS) == s["robustness_table_blob_sha"]
    assert git_blob_sha(SCALE_SUMMARY) == s["cluster_summary_blob_sha"]
    assert git_blob_sha(SCALE_FISHER) == s["fisher_summary_blob_sha"]
    assert git_blob_sha(SCALE_RESULT) == s["result_note_blob_sha"]
    assert git_blob_sha(SCALE_AMENDMENT) == s["protocol_amendment_blob_sha"]

    assert s["primary_direct_negative_g"] == 17
    assert s["primary_direct_negative_lnRR"] == 17
    assert s["sign_discordance"] == 0
    assert s["ML001_g_abs_order"] == ["G", "C", "F"]
    assert s["ML001_lnRR_abs_order"] == ["C", "F", "G"]
    assert abs(s["ML001_CF_g_p"] - 0.0071961841071408175) < 1e-15
    assert abs(s["ML001_CF_lnRR_raw_delta_p"] - 0.6364031922443418) < 1e-15
    assert abs(s["lnRR_raw_delta_full_p"] - 1.19170824745653e-12) < 1e-24
    assert abs(s["lnRR_raw_delta_omit_ML001_p"] - 8.314427075398979e-05) < 1e-16
    assert abs(s["lnRR_zero_omit_ML001_p"] - 0.004344181486257532) < 1e-15
    assert s["lnRR_cauchy_omit_ML001_p"] > 0.05

    sign = m["if_sign_geometry"]
    assert git_blob_sha(IF_SIGN_CENSUS) == sign["census_blob_sha"]
    assert git_blob_sha(IF_SIGN_NOTE) == sign["result_note_blob_sha"]
    assert git_blob_sha(IF_SIGN_CHECKER) == sign["checker_blob_sha"]
    assert sign["primary_panels"] == 18
    assert sign["independent_programmes"] == 8
    assert sign["sign_discordant_panels"] == 6
    assert sign["programmes_with_sign_discordance"] == 5
    assert sign["multi_panel_programmes"] == 4
    assert sign["within_programme_heterogeneous"] == 3

    geom = m["cross_scale_process_function_geometry"]
    assert git_blob_sha(BOTTLENECK_SCALE_TABLE) == geom["scale_table_blob_sha"]
    assert git_blob_sha(BOTTLENECK_SCALE_NOTE) == geom["result_note_blob_sha"]
    assert geom["downstream_identity_stable"] is True
    assert geom["upstream_identity_stable"] is False
    assert geom["both_directions_present_g"] is True
    assert geom["both_directions_present_lnRR"] is True
    assert geom["g_upstream"] == ["ML001"]
    assert geom["lnRR_upstream"] == ["ML002", "ML014"]

    ft = m["figure_table_revision"]
    assert git_blob_sha(FIGURE_BUILDER) == ft["builder_blob_sha"]
    assert git_blob_sha(FIGURE_CAPTIONS) == ft["captions_blob_sha"]
    assert ft["main_figure3"] == "manuscript/figures/figure3_if_sign_geometry.svg"
    assert ft["main_figure4"] == "manuscript/figures/figure4_estimand_scale_sensitivity.svg"
    assert ft["main_table2"] == "manuscript/tables/table2_estimand_scale_sensitivity.csv"
    assert ft["supplementary_table_s4"] == "manuscript/tables/table_s4_process_function_census.csv"
    assert "estimand_scale_cluster_summary_v2.csv" in builder
    assert "lnRR_raw_delta_cov_p" in builder
    assert "p=0.6364" in builder
    assert "figure3_if_sign_geometry.svg" in builder
    assert "Figure 3. Interaction–function sign geometry across matched fragmentation programmes" in captions
    assert "Figure 4. Relative response geometry is estimand-scale dependent" in captions
    assert "raw-unit multivariate delta covariance" in captions

    ap = m["anonymous_package"]
    assert git_blob_sha(ANON_BUILDER) == ap["builder_blob_sha"]
    assert ap["reproduces_authoritative_raw_delta_scale_audit"] is True
    assert ap["reproduces_bottleneck_cross_scale_audit"] is True
    assert "check_estimand_scale_robustness.py" in anon
    assert "check_bottleneck_scale_robustness.py" in anon
    assert "check_if_sign_geometry.py" in anon
    assert "table_s5_if_sign_geometry.csv" in anon
    assert "figure3_if_sign_geometry.svg" in anon
    assert "figure4_estimand_scale_sensitivity.svg" in anon
    assert "table2_estimand_scale_sensitivity.csv" in anon

    for token in (
        "historical Hedges-g synthesis is exactly reproducible",
        "relative response amplitude and omit-Serapias robustness classification are estimand-scale dependent",
        "all 17 primary direct effects are negative on both oriented Hedges g and oriented lnRR",
        "upstream system attribution is scale-sensitive",
    ):
        assert token in json.dumps(m), token

    for token in (
        "scale-invariant global layer-separation syndrome",
        "scale-invariant system-specific bottleneck attribution",
        "claiming lnRR is the uniquely correct effect scale",
        "using ML020 p=1.0 as evidence of equality or coupling",
    ):
        assert token in json.dumps(m), token

    assert "**STATUS: SCIENTIFIC REVALIDATION PENDING.**" in note
    assert "raw-unit multivariate delta covariance" in note
    assert "8.31e-05" in note
    assert "17/17" in note
    assert "Figure 4: estimand-scale sensitivity" in note

    assert "scale_aware_main_sign_geometry_revision_validation_pending" in metadata
    assert "Scientific revalidation pending" in metadata
    assert "p = 0.6364" in metadata
    assert "[ ] ecology-forward title / Methods / main Figure 3 sign-geometry revision revalidated in current full CI and anonymous reviewer package" in metadata

    assert "raw-unit multivariate-delta covariance" in manuscript
    assert "all **17/17 primary direct effects were negative on both oriented g and oriented lnRR**" in manuscript
    assert "p=0.6364" in manuscript
    assert "8.31×10^-5" in manuscript

    assert "SUPERSEDED" not in scale_result
    assert "raw-unit delta covariance" in scale_result
    assert "### 2. Mandatory scale sensitivity" in amendment

    print(
        "SIGN_GEOMETRY_MAIN_REVISION_PENDING_OK "
        "submission_ready=false g_full=0.012124326106 g_drop_ML001=0.181943527111 "
        "lnRR_raw_delta_full=1.191708e-12 lnRR_raw_delta_drop_ML001=8.314427e-05 "
        "primary_negative_g=17 primary_negative_lnRR=17 sign_discordance=0 "
        "ML001_CF_lnRR_p=0.636403 scale_specific_bottleneck_attribution=true"
    )


if __name__ == "__main__":
    main()
