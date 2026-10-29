from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def normalize_i(value: str) -> str | None:
    if value == "lower":
        return "lower"
    if value == "no_detected_loss":
        return "no_detected_loss"
    if value in {"higher", "higher_or_shifted"}:
        return "higher"
    return None


def normalize_f(value: str) -> str | None:
    if value == "lower":
        return "lower"
    if value in {"no_detected_loss", "similar"}:
        return "no_detected_loss_or_similar"
    if value == "higher":
        return "higher"
    return None


def image_sets(data: list[dict[str, str]]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for r in data:
        i = normalize_i(r["interaction_signal"])
        f = normalize_f(r["function_signal"])
        if i is None or f is None:
            continue
        out.setdefault(i, set()).add(f)
    return out


def ambiguous_inputs(data: list[dict[str, str]]) -> set[str]:
    return {i for i, vals in image_sets(data).items() if len(vals) >= 2}


def main() -> None:
    data = rows(MAP)
    assert len(data) == 16

    full = ambiguous_inputs(data)
    assert full == {"lower", "no_detected_loss", "higher"}

    quantitative = [r for r in data if r["evidence_tier"] == "quantitative"]
    qualitative = [r for r in data if r["evidence_tier"] == "qualitative"]

    q_amb = ambiguous_inputs(quantitative)
    b_amb = ambiguous_inputs(qualitative)
    assert q_amb == {"lower"}
    assert b_amb == {"lower", "no_detected_loss"}

    # Full map must remain non-identifying after deleting any one programme.
    loo_full = {}
    for drop in data:
        subset = [r for r in data if r["programme_id"] != drop["programme_id"]]
        amb = ambiguous_inputs(subset)
        loo_full[drop["programme_id"]] = amb
        assert len(amb) >= 2, (drop["programme_id"], amb)

    # The qualitative tier itself retains at least one ambiguous input after
    # deleting any one qualitative programme.
    loo_qual = {}
    for drop in qualitative:
        subset = [r for r in qualitative if r["programme_id"] != drop["programme_id"]]
        amb = ambiguous_inputs(subset)
        loo_qual[drop["programme_id"]] = amb
        assert len(amb) >= 1, (drop["programme_id"], amb)

    # Quantitative-only category ambiguity depends on the unresolved Milkweed
    # opposite-sign point estimate; this is a claim ceiling, not a failure.
    q_without_milkweed = [
        r for r in quantitative
        if r["programme_id"] != "P2_CF01_MILKWEED_URBAN_2023"
    ]
    assert ambiguous_inputs(q_without_milkweed) == set()

    min_full = min(len(v) for v in loo_full.values())
    min_qual = min(len(v) for v in loo_qual.values())
    assert min_full >= 2
    assert min_qual >= 1

    print(
        "IF_TRANSLATION_INFLUENCE_OK "
        "programmes=16 full_ambiguous_inputs=3 "
        "quantitative_ambiguous_inputs=1 qualitative_ambiguous_inputs=2 "
        f"loo_full_min_ambiguous_inputs={min_full} "
        f"loo_qualitative_min_ambiguous_inputs={min_qual} "
        "quantitative_ambiguity_without_milkweed=0 "
        "prevalence_inference=false"
    )


if __name__ == "__main__":
    main()
