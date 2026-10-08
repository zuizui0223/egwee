from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "evidence/meta_extraction/interaction_provenance_context_v1.csv"
NOTE = ROOT / "manuscript/INTERACTION_PROVENANCE_HYPOTHESIS_2026-10-06.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    assert TABLE.is_file()
    assert NOTE.is_file()
    assert MANUSCRIPT.is_file()

    r = rows(TABLE)
    assert len(r) == 10
    assert all(x["quantitative_denominator_role"] == "none" for x in r)

    false_reassurance = {
        x["system"] for x in r if x["evidence_role"] == "internal_false_reassurance_anchor"
    }
    assert false_reassurance == {
        "Eucalyptus wandoo",
        "Cardiopetalum calophyllum",
        "Acanthopale pubescens",
    }

    bridges = {
        x["system"] for x in r
        if x["evidence_role"] in {"internal_provenance_fitness_bridge", "internal_localization_bridge"}
    }
    assert bridges == {"Eucalyptus socialis", "Spondias purpurea"}

    direct_external = {
        x["system"] for x in r if x["evidence_role"] == "external_direct_mechanism"
    }
    assert direct_external == {"Dianella revoluta", "Rhododendron ferrugineum"}

    translation_contrast = [
        x for x in r if x["evidence_role"] == "external_simultaneous_translation_contrast"
    ]
    assert len(translation_contrast) == 1
    assert translation_contrast[0]["system"] == "Rhododendron ferrugineum"
    assert translation_contrast[0]["survivor_filter_relevance"] == "reproductive_assurance_buffer"

    survivor_rows = [
        x for x in r if x["survivor_filter_relevance"] in {"direct_clue", "direct_survivor_filter"}
    ]
    assert {x["system"] for x in survivor_rows} == {"Eucalyptus wandoo", "Pinus cembra"}

    note = NOTE.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")

    assert "two-stage masking hypothesis" in note
    assert "local-count masking" in note
    assert "survivor-filter masking" in note
    assert "not a confirmed common mechanism" in note
    assert "Eucalyptus socialis" in note
    assert "16.6%" in note
    assert "Translation modifier: reproductive assurance" in note
    assert "mating system and reproductive assurance determine" in note

    # Main manuscript now promotes a broader branching-pathway synthesis.
    # The narrower two-stage hypothesis is preserved in the provenance note,
    # but must not be imposed as the exclusive manuscript mechanism.
    assert "branching-pathway explanation" in manuscript
    assert "within-pathway masking" in manuscript
    assert "Transfer provenance and effective mating remain important missing coordinates" in manuscript
    assert "not required to explain every mismatch" in manuscript

    print(
        "INTERACTION_PROVENANCE_CONTEXT: PASS; "
        "3 false-reassurance anchors, 2 internal mechanism bridges, "
        "2 direct external count-provenance examples, survivor-filter context kept non-denominator"
    )


if __name__ == "__main__":
    main()
