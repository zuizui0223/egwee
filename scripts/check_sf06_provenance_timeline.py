from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIMELINE = ROOT / "manuscript/SF06_OUTCOME_EXPOSURE_TIMELINE_2026-10-06.md"
PREREG = ROOT / "manuscript/SF06_TRANSLATION_RESIDUAL_PREREGISTRATION_2026-10-06.md"
DECISION = ROOT / "manuscript/SF06_EXTERNAL_VALIDATION_DECISION_TREE_2026-10-06.md"
COVERAGE = ROOT / "manuscript/SF06_PUBLIC_SUPPLEMENT_COVERAGE_BOUNDARY_2026-10-07.md"


def main() -> None:
    timeline = TIMELINE.read_text(encoding="utf-8")
    prereg = PREREG.read_text(encoding="utf-8")
    decision = DECISION.read_text(encoding="utf-8")
    coverage = COVERAGE.read_text(encoding="utf-8")

    for token in (
        "14:36:47",
        "426",
        "500",
        "gamma_SC = -0.0877403395",
        "compatibility_translation_prediction_not_supported",
        "preliminary public-S1 outputs",
        "public-supplement coverage shortfall",
        "pre-exposure-defined target with post-exposure robustness gates",
        "external_sign_translation_nonidentifiability_not_supported",
        "minimum deterministic mismatches: **0**",
    ):
        assert token in timeline, token

    assert "Provenance correction after the first numerical execution" in prereg
    assert "Post-exposure source-coverage correction: public S1 versus paper-reported input counts" in prereg
    assert "Post-exposure reproducibility gate for corrected reruns" in prereg
    assert "Pre-exposure topology definition and post-exposure robustness extensions" in prereg
    assert "must not be labelled a preregistered confirmatory replication" in prereg

    assert "post-exposure correction" in decision
    assert "not a preregistration" in decision
    assert "Do not call this a preregistered confirmatory replication" in decision
    assert "Public-source coverage ceiling" in decision

    for token in (
        "426",
        "267 female fitness / 88 male fitness / 71 pollination",
        "45 / 17 / 12 = 74",
        "Calystegia collina",
        "public-supplement subset",
    ):
        assert token in coverage, token

    print("SF06_PROVENANCE_TIMELINE: PASS")


if __name__ == "__main__":
    main()
