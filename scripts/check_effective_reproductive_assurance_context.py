from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "evidence/meta_extraction/effective_reproductive_assurance_context_v1.csv"
NOTE = ROOT / "manuscript/INTERACTION_PROVENANCE_HYPOTHESIS_2026-10-06.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    r = rows(TABLE)
    assert len(r) == 5
    assert {x["system"] for x in r} == {
        "Eucalyptus wandoo",
        "Conospermum undulatum",
        "Haloxylon ammodendron",
        "Lithraea molleoides",
        "Rhododendron ferrugineum",
    }

    effective = {
        x["system"] for x in r
        if x["route_effectiveness_for_viable_output"].startswith("effective")
    }
    assert effective == {
        "Haloxylon ammodendron",
        "Lithraea molleoides",
        "Rhododendron ferrugineum",
    }

    note = NOTE.read_text(encoding="utf-8")
    assert "effective assurance capacity" in note
    assert "mating-system label" in note
    assert "viable offspring" in note
    assert "not a moderator test" in note

    print(
        "EFFECTIVE_REPRODUCTIVE_ASSURANCE_CONTEXT: PASS; "
        "source-explicit compensation routes remain contextual and non-inferential"
    )


if __name__ == "__main__":
    main()
