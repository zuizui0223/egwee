from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def necessity_counterexamples(rs: list[dict[str, str]]) -> set[str]:
    # Reproductive decline occurs without an observed interaction decline.
    return {
        r["programme_id"]
        for r in rs
        if r["function_signal"] == "lower"
        and r["interaction_signal"] in {"no_detected_loss", "higher", "higher_or_shifted"}
    }


def sufficiency_counterexamples(rs: list[dict[str, str]]) -> set[str]:
    # Interaction decline occurs without an observed reproductive decline.
    return {
        r["programme_id"]
        for r in rs
        if r["interaction_signal"] == "lower"
        and r["function_signal"] in {"no_detected_loss", "similar", "higher"}
    }


def main() -> None:
    rs = rows(MAP)
    assert len(rs) == 16
    assert len({r["programme_id"] for r in rs}) == 16

    not_necessary = necessity_counterexamples(rs)
    not_sufficient = sufficiency_counterexamples(rs)

    assert not_necessary == {"ML015", "QIF008"}
    assert not_sufficient == {
        "P2_CF01_MILKWEED_URBAN_2023",
        "QIF002",
        "QIF003",
    }

    # Both logical failures survive removal of every single programme in the
    # frozen mixed-tier evidence universe.
    for drop in {r["programme_id"] for r in rs}:
        subset = [r for r in rs if r["programme_id"] != drop]
        assert necessity_counterexamples(subset), drop
        assert sufficiency_counterexamples(subset), drop

    # Quantitative-only evidence is weaker: one clean state-level counterexample
    # in each logical direction, so do not claim quantitative-tier LOO robustness.
    q = [r for r in rs if r["evidence_tier"] == "quantitative"]
    assert necessity_counterexamples(q) == {"ML015"}
    assert sufficiency_counterexamples(q) == {"P2_CF01_MILKWEED_URBAN_2023"}

    print(
        "INTERACTION_DECLINE_LOGIC_OK "
        "programmes=16 necessity_counterexamples=2 sufficiency_counterexamples=3 "
        "mixed_tier_LOO_both_failures=true "
        "quantitative_not_necessary_anchor=ML015 "
        "quantitative_not_sufficient_anchor=P2_CF01_MILKWEED_URBAN_2023 "
        "prevalence_inference=false"
    )


if __name__ == "__main__":
    main()
