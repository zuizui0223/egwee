from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
PROTOCOL = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md"
SCHEMA = ROOT / "manuscript/meta_analysis_effect_schema.json"
METADATA = ROOT / "manuscript/meta_analysis_submission_metadata.md"
LEDGER = ROOT / "manuscript/meta_analysis_candidate_ledger.csv"
SEEDS = ROOT / "manuscript/meta_analysis_seed_sources.md"


def main() -> None:
    for path in (README, MANUSCRIPT, PROTOCOL, SCHEMA, METADATA, LEDGER, SEEDS):
        assert path.is_file(), path

    readme = README.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    protocol = PROTOCOL.read_text(encoding="utf-8")
    metadata = METADATA.read_text(encoding="utf-8")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    assert "active paper is now a multilevel meta-analysis" in readme
    assert "Question 1" in readme and "Question 2" in readme
    assert "H1 — biological layers do not share one fragmentation response" in manuscript
    assert "H2 — contemporary processes can change before standing adult genetics" in manuscript
    assert "H3 — process compensation modifies the function response" in manuscript
    assert "not yet claimed" in manuscript.lower()
    assert "primary meta-analysis requires a direct fragmented-versus-reference comparison" in protocol.lower()
    assert "Missing biological layers are not coded as zero effects" in protocol
    assert "Do not define a `compensated` category" in protocol
    assert schema["schema_version"] == 1
    assert schema["primary_effect_stream"] == "hedges_g_fragmented_minus_reference"
    assert schema["secondary_effect_stream"] == "fisher_z_correlation_with_fragmentation_severity"
    assert set(schema["primary_layers"]) == {
        "D_resource_demography",
        "I_interaction",
        "C_movement_connectivity",
        "F_reproductive_function",
        "G_adult",
        "G_offspring",
    }
    assert "protocol_locked_screening_and_extraction_pending" in metadata
    for forbidden in (
        "meta-analysis demonstrates",
        "meta-analysis showed",
        "pooled effect was",
        "significantly more negative",
    ):
        assert forbidden not in manuscript.lower(), forbidden

    print("EGWEE multilayer meta-analysis contract: PASS")


if __name__ == "__main__":
    main()
