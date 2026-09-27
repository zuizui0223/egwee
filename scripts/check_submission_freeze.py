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
SCALE_SUMMARY = ROOT / "evidence/meta_extraction/estimand_scale_cluster_summary_v1.csv"
SCALE_RESULT = ROOT / "manuscript/ESTIMAND_SCALE_SENSITIVITY_RESULT_2026-09-27.md"
SCALE_AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-27_ESTIMAND_SCALE.md"
FILTER_NOTE = ROOT / "manuscript/EXPLORATORY_TRANSITION_FILTERING_2026-09-27.md"
FILTER_TABLE = ROOT / "evidence/meta_extraction/exploratory_transition_filtering_v1.csv"
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
    filter_note = FILTER_NOTE.read_text(encoding="utf-8")
    builder = FIGURE_BUILDER.read_text(encoding="utf-8")
    captions = FIGURE_CAPTIONS.read_text(encoding="utf-8")
    anon = ANON_BUILDER.read_text(encoding="utf-8")

    assert m["schema_version"] == 4
    assert m["status"] == "revision_required_estimand_scale_sensitivity"
    assert m["submission_ready"] is False
    assert m["supersedes_submission_freeze"] is True
    assert m["revision_base_commit"] == "5046c7f2bd793b36303ea85f887b4dec25e98d70"

    man = m["manuscript"]
    assert git_blob_sha(MANUSCRIPT) == man["blob_sha"]
    assert man["title"] == "Habitat fragmentation across plant reproductive life cycles: directional consistency and scale-sensitive response amplitudes"
    assert man["target_journal"] == "Journal of Ecology"
    assert man["main_text_words"] == 6816
    assert man["abstract_words"] == 263
    assert manuscript.startswith("# " + man["title"])

    g = m["historical_primary_g"]
    assert g["independent_clusters"] == 5
    assert g["marginal_effects"] == 17
    assert g["full_fisher_p"] == 0.01212432
    assert g["omit_ML001_p"] == 0.18194353

    s = m["estimand_scale_sensitivity"]
    assert git_blob_sha(SCALE_ENDPOINTS) == s["endpoint_table_blob_sha"]
    assert git_blob_sha(SCALE_SUMMARY) == s["cluster_summary_blob_sha"]
    assert git_blob_sha(SCALE_RESULT) == s["result_note_blob_sha"]
    assert git_blob_sha(SCALE_AMENDMENT) == s["protocol_amendment_blob_sha"]
    assert s["primary_direct_negative_g"] == 17
    assert s["primary_direct_negative_lnRR"] == 17
    assert s["ML001_g_abs_order"] == ["G", "C", "F"]
    assert s["ML001_lnRR_abs_order"] == ["C", "F", "G"]
    assert abs(s["ML001_CF_lnRR_p_rho_proxy"] - 0.6048817291933912) < 1e-12
    assert s["lnRR_rho_omit_ML001_p"] < 0.05
    assert s["lnRR_zero_omit_ML001_p"] < 0.05
    assert s["lnRR_cauchy_omit_ML001_p"] > 0.05

    exp = m["exploratory_ecology"]
    assert exp["status"] == "post_hoc_hypothesis_generating"
    assert git_blob_sha(FILTER_NOTE) == exp["transition_filtering_note_blob_sha"]
    assert git_blob_sha(FILTER_TABLE) == exp["transition_filtering_table_blob_sha"]

    ft = m["figure_table_revision"]
    assert git_blob_sha(FIGURE_BUILDER) == ft["builder_blob_sha"]
    assert git_blob_sha(FIGURE_CAPTIONS) == ft["captions_blob_sha"]
    assert ft["main_figure4"] == "manuscript/figures/figure4_estimand_scale_sensitivity.svg"
    assert ft["main_table2"] == "manuscript/tables/table2_estimand_scale_sensitivity.csv"
    assert ft["supplementary_table_s4"] == "manuscript/tables/table_s4_process_function_census.csv"
    assert "figure4_estimand_scale_sensitivity.svg" in builder
    assert "table2_estimand_scale_sensitivity.csv" in builder
    assert "table_s4_process_function_census.csv" in builder
    assert "Figure 4. Relative response geometry is estimand-scale dependent" in captions
    assert "Table 2. Estimand-scale sensitivity of the direct synthesis" in captions

    ap = m["anonymous_package"]
    assert git_blob_sha(ANON_BUILDER) == ap["builder_blob_sha"]
    assert ap["reproduces_scale_audit"] is True
    assert "check_estimand_scale_sensitivity.py" in anon
    assert "figure4_estimand_scale_sensitivity.svg" in anon
    assert "table2_estimand_scale_sensitivity.csv" in anon

    for token in (
        "historical Hedges-g synthesis is exactly reproducible",
        "relative response amplitude and omit-Serapias robustness classification are estimand-scale dependent",
        "all 17 primary direct effects are negative on both oriented Hedges g and oriented lnRR",
    ):
        assert token in json.dumps(m), token

    for token in (
        "scale-invariant global layer-separation syndrome",
        "scale-invariant variable life-cycle bottleneck ordering",
        "claiming lnRR is the uniquely correct effect scale",
        "using ML020 p=1.0 as evidence of equality or coupling",
    ):
        assert token in json.dumps(m), token

    assert "**STATUS: NOT SUBMISSION-READY.**" in note
    assert "mandatory estimand-scale revision" in note
    assert "17/17" in note
    assert "Figure 4: estimand-scale sensitivity" in note
    assert "green CI while `submission_ready=false`" in note

    assert "`revision_required_estimand_scale_sensitivity`" in metadata
    assert "Submission hold" in metadata
    assert "estimand-scale audit completed" in metadata
    assert "[ ] submission freeze renewed" in metadata

    assert "relative response amplitude and robustness classification are estimand-scale dependent" in manuscript
    assert "all **17/17 primary direct effects were negative on both oriented g and oriented lnRR**" in manuscript
    assert "p≈0.605" in manuscript
    assert "post hoc / hypothesis-generating" in filter_note.casefold()
    assert "not a replacement truth" in scale_result
    assert "mandatory sensitivity audit" in amendment

    print(
        "REVISION_STATE_V4_OK "
        "submission_ready=false g_full=0.01212432 g_drop_ML001=0.18194353 "
        "primary_negative_g=17 primary_negative_lnRR=17 "
        "ML001_order_g=G>C>F ML001_order_lnRR=C>F>G "
        "main_figure4=estimand_scale main_table2=estimand_scale"
    )


if __name__ == "__main__":
    main()
