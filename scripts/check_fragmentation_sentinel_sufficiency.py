from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"
NOTE = ROOT / "manuscript/FRAGMENTATION_SENTINEL_SUFFICIENCY_2026-10-03.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    rs = rows(MAP)
    note = NOTE.read_text(encoding="utf-8")
    assert len(rs) == 16

    represented = {
        "lower": {"lower", "higher", "no_detected_loss"},
        "no_detected_loss": {"lower", "no_detected_loss"},
        "higher": {"lower", "similar"},
    }
    for i_state, required_f in represented.items():
        observed = {
            r["function_signal"]
            for r in rs
            if r["interaction_signal"] == i_state
        }
        assert required_f <= observed, (i_state, observed)

    # Every simple upstream state used in the structural claim maps to >1 F state.
    assert all(
        len({
            r["function_signal"]
            for r in rs
            if r["interaction_signal"] == i_state
        }) > 1
        for i_state in represented
    )

    # Evidence tiers must remain non-overlapping.
    qsrc = {r["source_id"] for r in rs if r["evidence_tier"] == "quantitative"}
    xsrc = {r["source_id"] for r in rs if r["evidence_tier"] == "qualitative"}
    assert len(qsrc) == 8
    assert len(xsrc) == 8
    assert qsrc.isdisjoint(xsrc)

    for token in (
        "evidence-state identifiability",
        "not a sufficient state variable",
        "False reassurance",
        "Apparent over-warning",
        "positive cross-species association",
        "0/8 programmes",
    ):
        assert token in note, token

    print(
        "FRAGMENTATION_SENTINEL_SUFFICIENCY_OK "
        "programmes=16 upstream_states_tested=3 "
        "all_upstream_states_map_to_multiple_F_states=true "
        "false_reassurance_exists=true apparent_overwarning_exists=true "
        "prevalence_inference=false"
    )


if __name__ == "__main__":
    main()
