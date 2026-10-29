from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TIMELINE = ROOT / "manuscript/SF06_OUTCOME_EXPOSURE_TIMELINE_2026-10-06.md"
PREREG = ROOT / "manuscript/SF06_TRANSLATION_RESIDUAL_PREREGISTRATION_2026-10-06.md"
DECISION = ROOT / "manuscript/SF06_EXTERNAL_VALIDATION_DECISION_TREE_2026-10-06.md"
COVERAGE = ROOT / "manuscript/SF06_PUBLIC_SUPPLEMENT_COVERAGE_BOUNDARY_2026-10-07.md"
INVALIDATED = ROOT / "manuscript/SF06_SIGN_TOPOLOGY_MONOTONICITY_BOUNDARY_2026-10-07.md"


def main() -> None:
    timeline = TIMELINE.read_text(encoding="utf-8")
    prereg = PREREG.read_text(encoding="utf-8")
    decision = DECISION.read_text(encoding="utf-8")
    coverage = COVERAGE.read_text(encoding="utf-8")
    invalidated = INVALIDATED.read_text(encoding="utf-8")

    for token in (
        "14:36:47",
        "426",
        "500",
        "gamma_SC = -0.087740",
        "not biologically valid",
        "spaced-minus parser defect",
        "gamma_SC = +0.063904",
        "minimum deterministic mismatches = 12",
        "publication-LOO minimum = 8",
        "species-LOO minimum = 11",
        "Source-publication-disjoint sensitivity",
    ):
        assert token in timeline, token

    for token in (
        "Post-exposure sign-parser correction",
        "800ccfa",
        "12/54",
        "7/31",
        "directionally consistent but unresolved",
        "preregistered biological target",
    ):
        assert token in prereg, token

    assert "post-exposure correction" in decision
    assert "not a preregistration" in decision
    assert "Corrected outcome classification" in decision
    assert "robust external generalization" in decision
    assert "gamma_SC = +0.0639" in decision
    assert "Public-source coverage ceiling" in decision

    for token in (
        "426",
        "267 female fitness / 88 male fitness / 71 pollination",
        "45 / 17 / 12 = 74",
        "Calystegia collina",
        "public-supplement subset",
    ):
        assert token in coverage, token

    assert "INVALIDATED BY SIGN-PARSER BUG" in invalidated
    assert "800ccfa" in invalidated
    assert "12/54" in invalidated
    assert "7/31" in invalidated

    print("SF06_PROVENANCE_TIMELINE: PASS")


if __name__ == "__main__":
    main()
