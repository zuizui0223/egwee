from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def interaction_class(row: dict[str, str]) -> str | None:
    x = row["interaction_signal"]
    if x == "lower":
        return "lower"
    if x in {"higher", "higher_or_shifted"}:
        return "higher_or_shifted"
    return None


def function_class(row: dict[str, str]) -> str | None:
    x = row["function_signal"]
    if x == "lower":
        return "lower"
    if x == "higher":
        return "higher"
    if x == "similar":
        return "similar"
    return None


def strict_rows(rs: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        r for r in rs
        if interaction_class(r) is not None and function_class(r) is not None
    ]


def mappings(rs: list[dict[str, str]]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for r in rs:
        i = interaction_class(r)
        f = function_class(r)
        if i is None or f is None:
            continue
        out.setdefault(i, set()).add(f)
    return out


def ambiguous_inputs(rs: list[dict[str, str]]) -> set[str]:
    return {k for k, vals in mappings(rs).items() if len(vals) >= 2}


def main() -> None:
    rs = rows(MAP)
    assert len(rs) == 16
    strict = strict_rows(rs)

    expected_ids = {
        "ML020",
        "ML015",
        "P2_CF01_CARDIOPETALUM_2012",
        "P2_CF01_MILKWEED_URBAN_2023",
        "P2_CF01_PRITCHARD_2005",
        "QIF005",
        "QIF006",
        "QIF007",
    }
    assert {r["programme_id"] for r in strict} == expected_ids
    assert len(strict) == 8

    mp = mappings(strict)
    assert mp["lower"] == {"lower", "higher"}
    assert mp["higher_or_shifted"] == {"lower", "similar"}
    assert ambiguous_inputs(strict) == {"lower", "higher_or_shifted"}

    # The conservative map remains non-identifying after deleting any one
    # programme, even after removing all no-detected-loss and mixed states.
    loo_min = 99
    for drop in expected_ids:
        subset = [r for r in strict if r["programme_id"] != drop]
        amb = ambiguous_inputs(subset)
        assert amb, drop
        loo_min = min(loo_min, len(amb))

    assert loo_min >= 1

    quantitative = [r for r in strict if r["evidence_tier"] == "quantitative"]
    qualitative = [r for r in strict if r["evidence_tier"] == "qualitative"]
    assert len(quantitative) == 5
    assert len(qualitative) == 3

    print(
        "IF_TRANSLATION_CATEGORY_SENSITIVITY_OK "
        "full_programmes=16 strict_programmes=8 "
        "removed_no_detected_or_mixed=true "
        "lower_maps=lower+higher "
        "higher_maps=lower+similar "
        f"strict_LOO_min_ambiguous_inputs={loo_min} "
        "prevalence_inference=false"
    )


if __name__ == "__main__":
    main()
