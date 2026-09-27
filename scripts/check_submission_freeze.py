from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manuscript/submission_freeze_manifest_v1.json"
FREEZE_NOTE = ROOT / "manuscript/SUBMISSION_FREEZE_2026-09-27.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-27_ESTIMAND_SCALE.md"
SCALE_RESULT = ROOT / "manuscript/ESTIMAND_SCALE_SENSITIVITY_RESULT_2026-09-27.md"
SCALE_ENDPOINTS = ROOT / "evidence/meta_extraction/estimand_scale_sensitivity_v1.csv"
SCALE_CLUSTERS = ROOT / "evidence/meta_extraction/estimand_scale_cluster_summary_v1.csv"
SCALE_FISHER = ROOT / "evidence/meta_extraction/estimand_scale_fisher_sensitivity_v1.csv"
METADATA = ROOT / "manuscript/meta_analysis_submission_metadata.md"
TITLE_PAGE = ROOT / "manuscript/JOURNAL_OF_ECOLOGY_TITLE_PAGE_TEMPLATE.md"
COVER = ROOT / "manuscript/JOURNAL_OF_ECOLOGY_COVER_LETTER_DRAFT.md"
FIGURE_BUILDER = ROOT / "scripts/build_journal_of_ecology_figures.py"
FIGURE_CAPTIONS = ROOT / "manuscript/JOURNAL_OF_ECOLOGY_FIGURE_CAPTIONS.md"
ANON_BUILDER = ROOT / "scripts/build_anonymous_review_package.py"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = f"blob {len(data)}\0".encode("utf-8") + data
    return hashlib.sha1(payload).hexdigest()


def main() -> None:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    note = FREEZE_NOTE.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    amendment = AMENDMENT.read_text(encoding="utf-8")
    scale_result = SCALE_RESULT.read_text(encoding="utf-8")
    metadata = METADATA.read_text(encoding="utf-8")
    title_page = TITLE_PAGE.read_text(encoding="utf-8")
    cover = COVER.read_text(encoding="utf-8")
    builder = FIGURE_BUILDER.read_text(encoding="utf-8")
    captions = FIGURE_CAPTIONS.read_text(encoding="utf-8")
    anon = ANON_BUILDER.read_text(encoding="utf-8")

    assert m["schema_version"] == 4
    assert m["freeze_kind"] == "scale_aware_submission_freeze"
    assert m["frozen_on"] == "2026-09-27"
    assert m["scientific_base_commit"] == "5046c7f2bd793b36303ea85f887b4dec25e98d70"
    assert m["submission_state"] == "scale_aware_revision_complete_admin_pending"

    man = m["manuscript"]
    assert man["title"] == "Habitat fragmentation across plant reproductive life cycles: directional consistency and scale-sensitive response amplitudes"
    assert man["target_journal"] == "Journal of Ecology"
    assert man["main_text_words_at_freeze"] == 6816
    assert man["abstract_words_at_freeze"] == 263
    assert git_blob_sha(MANUSCRIPT) == man["blob_sha"]
    assert manuscript.startswith("# " + man["title"])
    assert man["title"] in title_page
    assert man["title"] in cover

    hp = m["historical_primary"]
    assert hp["estimand"] == "Hedges_g"
    assert hp["independent_clusters"] == 5
    assert hp["marginal_effects"] == 17
    assert hp["full_fisher_p"] == 0.01212432
    assert hp["omit_ML001_p"] == 0.18194353

    sa = m["estimand_scale_audit"]
    assert git_blob_sha(AMENDMENT) == sa["amendment_blob_sha"]
    assert git_blob_sha(SCALE_RESULT) == sa["result_blob_sha"]
    assert git_blob_sha(SCALE_ENDPOINTS) == sa["endpoint_table_blob_sha"]
    assert git_blob_sha(SCALE_CLUSTERS) == sa["cluster_summary_blob_sha"]
    assert git_blob_sha(SCALE_FISHER) == sa["fisher_summary_blob_sha"]
    assert abs(sa["lnRR_existing_rho_full_p"] - 1.1786949416822378e-10) < 1e-20
    assert abs(sa["lnRR_existing_rho_omit_ML001_p"] - 2.9182238842850177e-05) < 1e-15
    assert abs(sa["lnRR_zero_cov_full_p"] - 1.7227795177175651e-09) < 1e-19
    assert abs(sa["lnRR_zero_cov_omit_ML001_p"] - 0.004344181486474443) < 1e-14
    assert abs(sa["lnRR_cauchy_full_p"] - 9.946000181275223e-05) < 1e-14
    assert abs(sa["lnRR_cauchy_omit_ML001_p"] - 0.11137892442058767) < 1e-13
    assert abs(sa["ML001_CF_lnRR_p_existing_rho"] - 0.6048817291933912) < 1e-12
    assert sa["ML001_g_abs_order"] == ["G", "C", "F"]
    assert sa["ML001_lnRR_abs_order"] == ["C", "F", "G"]

    endpoint_rows = rows(SCALE_ENDPOINTS)
    assert len(endpoint_rows) == 17
    assert sum(float(r["hedges_g"]) < 0 for r in endpoint_rows) == 17
    assert sum(float(r["oriented_lnRR"]) < 0 for r in endpoint_rows) == 17

    fisher_rows = rows(SCALE_FISHER)
    assert len(fisher_rows) == 4
    by_key = {(r["estimand"], r["dependence_regime"]): r for r in fisher_rows}
    assert abs(float(by_key[("hedges_g", "registered_rho_proxy")]["omit_ML001_fisher_p"]) - 0.18194353) < 5e-8
    assert float(by_key[("oriented_lnRR", "carried_existing_rho_proxy")]["omit_ML001_fisher_p"]) < 0.05
    assert float(by_key[("oriented_lnRR", "zero_covariance")]["omit_ML001_fisher_p"]) < 0.05
    assert float(by_key[("oriented_lnRR", "cauchy_maximum_contrast_variance")]["omit_ML001_fisher_p"]) > 0.05

    stable = m["scale_stable_result"]
    assert stable["primary_direct_effects"] == 17
    assert stable["negative_on_oriented_g"] == 17
    assert stable["negative_on_oriented_lnRR"] == 17
    assert "no scale-independent magnitude ordering" in stable["interpretation"]

    assert m["separate_gradient_evidence"]["wandoo_sign_discordance"] is True
    assert m["separate_gradient_evidence"]["pooled_with_primary"] is False
    assert m["exploratory_ecology"]["status"] == "post_hoc_hypothesis_generating"
    assert m["former_bottleneck_census"]["status"] == "supplementary_exploratory_registered_scale_only"
    assert m["former_bottleneck_census"]["scale_invariant_claim_permitted"] is False

    ft = m["figure_table_package"]
    assert ft["figure2_role"] == "historical_Hedges_g_primary_only"
    assert ft["figure3_role"] == "registered_scale_examples_unresolved_not_equality"
    assert ft["figure4_role"] == "main_estimand_scale_sensitivity"
    assert ft["table2"] == "manuscript/tables/table2_estimand_scale_sensitivity.csv"
    assert ft["supplementary_table_s4"] == "manuscript/tables/table_s4_process_function_census.csv"
    for token in (
        "figure4_estimand_scale_sensitivity.svg",
        "table2_estimand_scale_sensitivity.csv",
        "table_s4_process_function_census.csv",
    ):
        assert token in builder, token
    assert "Historical Hedges-g leave-one-cluster-out influence" in captions
    assert "Relative response geometry is estimand-scale dependent" in captions
    assert "unresolved" in captions and "not evidence that the true I and F effects are equal" in captions

    for token in (
        "scale_aware_revision_complete_admin_pending",
        "estimand-scale audit completed",
        "g and lnRR sensitivity reported in Methods, Results, Limitations and figure/table package",
        "submission freeze renewed after scale-aware manuscript + figure/table revision",
    ):
        assert token in metadata, token
    assert "[ ] author/declaration metadata approved." in metadata

    for token in (
        "estimand_scale_fisher_sensitivity_v1.csv",
        "check_estimand_scale_sensitivity.py",
        "figure4_estimand_scale_sensitivity.svg",
        "table2_estimand_scale_sensitivity.csv",
    ):
        assert token in anon, token

    assert "not invariant to effect-size scale" in scale_result
    assert "17/17" in scale_result
    assert "not a replacement truth" in amendment
    assert "Scale-independent directional audit" in amendment

    for token in (
        "scale-invariant global layer-separation syndrome",
        "scale-invariant variable bottleneck ordering",
        "ML020 p equals evidence of true equality",
        "lnRR is uniquely correct effect scale",
    ):
        assert token in json.dumps(m), token

    assert "17/17 primary direct effects are negative" in note
    assert "relative response amplitude" in note
    assert "Supplementary Table S4" in note

    assert len(m["remaining_human_blockers"]) == 7

    print(
        "SCALE_AWARE_SUBMISSION_FREEZE_V4_OK "
        "clusters=5 effects=17 g_full=0.01212432 g_drop_ML001=0.18194353 "
        "sign_negative_g=17 sign_negative_lnRR=17 figure4=scale_sensitivity table2=scale_sensitivity "
        "admin_pending=7"
    )


if __name__ == "__main__":
    main()
