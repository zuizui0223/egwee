from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manuscript/submission_freeze_manifest_v1.json"
FREEZE_NOTE = ROOT / "manuscript/SUBMISSION_FREEZE_2026-09-27.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
METADATA = ROOT / "manuscript/meta_analysis_submission_metadata.md"
README = ROOT / "README.md"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    payload = f"blob {len(data)}\0".encode("utf-8") + data
    return hashlib.sha1(payload).hexdigest()


def main() -> None:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    note = FREEZE_NOTE.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    census = CENSUS.read_text(encoding="utf-8")
    metadata = METADATA.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    assert m["schema_version"] == 1
    assert m["frozen_on"] == "2026-09-27"
    assert m["scientific_base_commit"] == "9fe74375346112747c9aa84ae6fa977a7c380255"

    assert git_blob_sha(MANUSCRIPT) == m["manuscript"]["blob_sha"]
    assert git_blob_sha(CENSUS) == m["ecological_IF_census"]["blob_sha"]

    assert m["manuscript"]["target_journal"] == "Journal of Ecology"
    assert m["manuscript"]["main_text_words_at_freeze"] == 6156
    assert m["manuscript"]["abstract_words_at_freeze"] == 301
    assert manuscript.startswith("# " + m["manuscript"]["title"])

    direct = m["primary_direct"]
    assert direct == {
        "independent_clusters": 5,
        "marginal_effects": 17,
        "canonical_p": 0.01212432,
        "omit_ML001_p": 0.18194353,
        "zero_covariance_p": 0.03860161,
        "covariance_free_bound_p": 0.28061178,
    }

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

    for token in (
        "programme_id,system,source_id,i_endpoint,interaction_measurement_class",
        "quantity_only",
        "F_more_negative_than_I",
        "not_testable",
    ):
        assert token in census, token

    for token in (
        "all eight current I endpoints are quantity-level and none directly measures effective mating quality on the same I-F frame",
        "universal F-dominant I-F law",
        "direct validation of finite EGWE or NEE operators",
    ):
        assert token in json.dumps(m), token

    assert m["fresh_validation"]["current_IF_programmes_burned"] == 8
    assert m["fresh_validation"]["min_fresh_programmes_per_effect_family"] == 5

    assert m["automated_readiness"]["full_contract_conclusion"] == "success"
    assert m["automated_readiness"]["submission_shape"] is True
    assert m["automated_readiness"]["double_anonymous"] is True
    assert m["automated_readiness"]["figures_tables_reproduced"] is True
    assert m["automated_readiness"]["anonymous_review_package_reproduced"] is True

    assert len(m["remaining_human_blockers"]) == 7
    assert "[ ] author/declaration metadata approved." in metadata
    assert "[x] double-anonymous submission package checked" in metadata
    assert "[x] final figure/table package completed" in metadata

    for token in (
        "empirical plant-fragmentation",
        "quantity",
        "effective mating",
    ):
        assert token.casefold() in (readme + "\n" + note).casefold(), token

    print(
        "SUBMISSION_FREEZE_OK "
        "direct=5 effects=17 phase2=360/360 IF=3/5 CF=2/5 "
        "IF_census=8 testable=7 resolved=3 Fdominant=3 quantity_only=8 effective=0 "
        "automated_ready=true human_admin_pending=7"
    )


if __name__ == "__main__":
    main()
