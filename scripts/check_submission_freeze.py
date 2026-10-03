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
IF_UNCERTAINTY = ROOT / "evidence/meta_extraction/if_sign_uncertainty_v1.csv"
IF_UNCERTAINTY_CHECKER = ROOT / "scripts/check_if_sign_uncertainty.py"
PROXY_TABLE = ROOT / "evidence/meta_extraction/scale_stable_quantity_function_proxy_failure_v1.csv"
PROXY_CHECKER = ROOT / "scripts/check_scale_stable_quantity_function_proxy_failure.py"
PROXY_NOTE = ROOT / "manuscript/SCALE_STABLE_QUANTITY_FUNCTION_PROXY_FAILURE_2026-09-29.md"
NOVELTY_AUDIT = ROOT / "manuscript/IF_PROXY_FAILURE_NOVELTY_AUDIT_2026-10-01.md"

FIGURE_BUILDER = ROOT / "scripts/build_journal_of_ecology_figures.py"
FIGURE_CAPTIONS = ROOT / "manuscript/JOURNAL_OF_ECOLOGY_FIGURE_CAPTIONS.md"
ANON_BUILDER = ROOT / "scripts/build_anonymous_review_package.py"
SOCIALIS_SNAPSHOT = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_sufficient_stats_v1.json"


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

    assert m["schema_version"] == 6
    assert m["updated_on"] == "2026-10-01"
    assert m["status"] == "scientific_validation_green_human_admin_pending"
    assert m["submission_ready"] is False
    assert m["supersedes_submission_freeze"] is True
    sv = m["scientific_validation"]
    assert sv["conclusion"] == "success"
    assert sv["current_revision_status"] == "validated"
    assert sv["current_revision_validated"] is True
    assert sv["full_contract_run_id"] == 37089505747
    assert sv["proxy_failure_audit"] is True
    assert sv["sign_uncertainty_audit"] is True
    assert len(m["remaining_scientific_gate"]) == 0

    man = m["manuscript"]
    assert git_blob_sha(MANUSCRIPT) == man["blob_sha"]
    assert man["title"] == "Habitat fragmentation across plant reproductive life cycles: scale-stable deterioration and recurrent interaction–function proxy failure"
    assert man["target_journal"] == "Journal of Ecology"
    assert man["main_text_words"] == 7811
    assert man["abstract_words"] == 334
    assert manuscript.startswith("# " + man["title"])

    g = m["historical_primary_g"]
    assert g["independent_clusters"] == 5
    assert g["marginal_effects"] == 17
    assert abs(g["full_fisher_p"] - 0.012124326106346261) < 1e-15
    assert abs(g["omit_ML001_p"] - 0.1819435271114386) < 1e-15

    s = m["authoritative_estimand_scale_audit"]
    assert git_blob_sha(SOCIALIS_SNAPSHOT) == s["ml014_sufficient_stats_snapshot_blob_sha"]
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
    assert abs(s["ML001_CF_lnRR_raw_delta_p"] - 0.6364031922443418) < 1e-15
    assert abs(s["lnRR_raw_delta_omit_ML001_p"] - 8.314427075398979e-05) < 1e-16
    assert s["lnRR_cauchy_omit_ML001_p"] > 0.05

    sign = m["if_sign_geometry"]
    assert git_blob_sha(IF_SIGN_CENSUS) == sign["census_blob_sha"]
    assert git_blob_sha(IF_SIGN_NOTE) == sign["result_note_blob_sha"]
    assert git_blob_sha(IF_SIGN_CHECKER) == sign["checker_blob_sha"]
    assert sign["primary_panels"] == 18
    assert sign["independent_programmes"] == 8
    assert sign["sign_discordant_panels"] == 6
    assert sign["programmes_with_sign_discordance"] == 5

    uncertainty = m["if_sign_uncertainty"]
    assert git_blob_sha(IF_UNCERTAINTY) == uncertainty["table_blob_sha"]
    assert git_blob_sha(IF_UNCERTAINTY_CHECKER) == uncertainty["checker_blob_sha"]
    assert uncertainty["primary_panels"] == 18
    assert uncertainty["opposite_point_panels"] == 6
    assert uncertainty["programmes_with_opposite_point_signs"] == 5
    assert uncertainty["both_endpoint_directions_resolved_opposite"] == 0
    assert uncertainty["one_endpoint_resolved_opposite"] == 2
    assert uncertainty["both_endpoints_unresolved_opposite"] == 4

    proxy = m["ecological_leads"]["scale_stable_quantity_function_proxy_failure"]
    assert git_blob_sha(PROXY_TABLE) == proxy["evidence_table_blob_sha"]
    assert git_blob_sha(PROXY_CHECKER) == proxy["checker_blob_sha"]
    assert git_blob_sha(PROXY_NOTE) == proxy["note_blob_sha"]
    assert proxy["independent_programmes"] == 3
    assert proxy["stable_upstream_programmes"] == 0
    assert set(proxy["programmes"]) == {"ML015", "P2_CF01_CARDIOPETALUM_2012", "P2_CF01_BERGSDORF_KAKAMEGA_2006"}
    assert len(proxy["regions"]) == 3
    assert len(proxy["plant_families"]) == 3
    assert git_blob_sha(NOVELTY_AUDIT) == m["proxy_failure_novelty_audit"]["blob_sha"]

    geom = m["cross_scale_process_function_geometry"]
    assert git_blob_sha(BOTTLENECK_SCALE_TABLE) == geom["scale_table_blob_sha"]
    assert git_blob_sha(BOTTLENECK_SCALE_NOTE) == geom["result_note_blob_sha"]
    assert geom["downstream_identity_stable"] is True
    assert geom["upstream_identity_stable"] is False

    ft = m["figure_table_revision"]
    assert git_blob_sha(FIGURE_BUILDER) == ft["builder_blob_sha"]
    assert git_blob_sha(FIGURE_CAPTIONS) == ft["captions_blob_sha"]
    assert ft["main_figure3"] == "manuscript/figures/figure3_if_sign_geometry.svg"
    assert ft["main_figure4"] == "manuscript/figures/figure4_estimand_scale_sensitivity.svg"
    assert ft["main_table2"] == "manuscript/tables/table2_estimand_scale_sensitivity.csv"
    assert "IF_SIGN_UNCERTAINTY" in builder
    assert "PROXY_FAILURE" in builder
    assert "Figure 3. Scale-stable interaction–function proxy failure and sign uncertainty" in captions
    assert "Figure 4. Relative response geometry is estimand-scale dependent" in captions

    ap = m["anonymous_package"]
    assert git_blob_sha(ANON_BUILDER) == ap["builder_blob_sha"]
    assert ap["reproduces_authoritative_raw_delta_scale_audit"] is True
    assert ap["reproduces_bottleneck_cross_scale_audit"] is True
    assert "check_estimand_scale_robustness.py" in anon
    assert "check_bottleneck_scale_robustness.py" in anon
    assert "check_if_sign_geometry.py" in anon
    assert "check_if_sign_uncertainty.py" in anon
    assert "scale_stable_quantity_function_proxy_failure_v1.csv" in anon
    assert "figure3_if_sign_geometry.svg" in anon

    claims = json.dumps(m)
    for token in (
        "all 17 primary direct effects are negative on both oriented Hedges g and oriented lnRR",
        "three independent I-F programmes provide representation-stable downstream function-dominant mismatches",
        "no audited I-F programme provides an equally representation-stable resolved upstream mismatch",
        "zero of those six have both marginal endpoint directions individually resolved at 95 percent",
    ):
        assert token in claims, token

    for token in (
        "claiming the six opposite-sign point estimates are six resolved sign reversals",
        "claiming species-specific visitation or reproductive responses to fragmentation are newly discovered",
        "claiming flower visitation being an imperfect proxy for pollination effectiveness is newly discovered",
    ):
        assert token in claims, token

    assert "**STATUS: SCIENTIFICALLY VALIDATED, HUMAN ADMINISTRATION PENDING.**" in note
    assert "Scale-stable interaction–function proxy failure" in note
    assert "0/6 have both marginal endpoint directions individually resolved" in note

    assert "scale_aware_proxy_failure_scientific_validation_green_human_admin_pending" in metadata
    assert "Scientific validation complete" in metadata
    assert "current automated count: 7811 words" in metadata

    assert "scale-stable deterioration and recurrent interaction–function proxy failure" in manuscript
    assert "all **17/17 primary direct effects were negative on both oriented g and oriented lnRR**" in manuscript
    assert "three programme-level I–F mismatches that remain stable" in manuscript
    assert "none has both marginal endpoint directions individually resolved at 95%" in manuscript

    assert "SUPERSEDED" not in scale_result
    assert "raw-unit delta covariance" in scale_result
    assert "### 2. Mandatory scale sensitivity" in amendment

    print(
         "PROXY_FAILURE_SCIENTIFIC_VALIDATION_GREEN_OK "
        "submission_ready=false human_admin_pending=true stable_downstream=3 stable_upstream=0 "
        "point_opposite=6 both_endpoint_resolved_opposite=0 "
        "primary_negative_g=17 primary_negative_lnRR=17 sign_discordance=0"
    )


if __name__ == "__main__":
    main()
