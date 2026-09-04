from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "manuscript" / "natural_data_gate_registry.json"
BOUNDARY = ROOT / "manuscript" / "unreachable_six_systems.json"
SPINE = ROOT / "manuscript" / "natural_data_ecological_indicators_spine.md"


def main() -> int:
    gates = json.loads(GATES.read_text(encoding="utf-8"))
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    spine = SPINE.read_text(encoding="utf-8")

    assert gates["schema_version"] == 1
    assert boundary["schema_version"] == 1
    by_system = {row["system"]: row for row in gates["systems"]}
    rows = boundary["systems"]
    assert len(rows) == 6
    assert len({row["system"] for row in rows}) == 6

    expected = {
        "Honshu-Izu",
        "Zurich BetterBlooms",
        "Toronto community gardens",
        "Eschscholzia californica",
        "Mallorca carob",
        "Campanula americana",
    }
    assert {row["system"] for row in rows} == expected
    assert boundary["excluded_positive_system"]["system"] == "Oenothera harringtonii"
    assert "20.93%" in boundary["excluded_positive_system"]["reason"]
    assert boundary["separate_synthesis_boundary"]["locked_outcome"] == gates["cross_study"]["locked_outcome"]

    for row in rows:
        source = by_system[row["system"]]
        assert row["gate_reached"] == source["gate_reached"]
        assert row["locked_outcome"] == source["locked_outcome"]
        assert row["numeric_certificate"]
        assert row["unreachable_stronger_inference"]
        assert row["blocking_reason"]
        assert row["boundary_class"]
        assert row["system"] in spine

    # The publication table must preserve the three logically distinct reasons
    # for non-progression rather than collapsing all six into one generic fail.
    classes = {row["boundary_class"] for row in rows}
    assert "negative_residual_does_not_certify_completeness" in classes
    assert "measurement_identifiability_blocks_downstream_gate" in classes
    assert "failed_measurement_adequacy_blocks_residual_gate" in classes
    assert "representation_collapse_blocks_downstream_gate" in classes

    required_spine_tokens = (
        "Six system-level branches did not license a stronger downstream inference",
        "unreachable under the frozen evidence",
        "0/6",
        "4932.9195",
        "Fallow ground",
        "-0.10195",
        "8.88e-16",
        "Oenothera",
        "not one of these six rows",
    )
    for token in required_spine_tokens:
        assert token in spine, token

    forbidden = (
        "biologically impossible",
        "all six failed at the same gate",
        "six independent replications of one effect",
    )
    lower = spine.lower()
    for token in forbidden:
        assert token.lower() not in lower, token

    print("Six-system downstream-inference boundary validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
