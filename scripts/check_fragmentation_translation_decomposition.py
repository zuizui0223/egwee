from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "manuscript/INTERACTION_PROVENANCE_HYPOTHESIS_2026-10-06.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"


def main() -> None:
    note = NOTE.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")

    for token in (
        "Q — interaction quantity",
        "P — transfer provenance",
        "V — post-transfer viability",
        "A — effective reproductive assurance",
        "F ∝ Q × P × V + A",
        "nominal self-compatibility is not the right moderator",
        "effective reproductive assurance",
    ):
        assert token in note, token

    assert "not a fitted equation, an exact identity" in note
    assert "Q × P × V + A" in manuscript
    assert "effective reproductive assurance" in manuscript

    print("FRAGMENTATION_TRANSLATION_DECOMPOSITION: PASS")


if __name__ == "__main__":
    main()
