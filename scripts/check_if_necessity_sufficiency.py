from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def i_class(x: str) -> str | None:
    if x == "lower":
        return "lower"
    if x in {"higher", "higher_or_shifted"}:
        return "higher"
    if x == "no_detected_loss":
        return "no_detected_loss"
    return None


def f_class(x: str) -> str | None:
    if x == "lower":
        return "lower"
    if x == "higher":
        return "higher"
    if x in {"similar", "no_detected_loss"}:
        return "not_lower"
    return None


def main() -> None:
    rs = rows(MAP)
    assert len(rs) == 16

    mapped = [
        (r["programme_id"], i_class(r["interaction_signal"]), f_class(r["function_signal"]))
        for r in rs
        if i_class(r["interaction_signal"]) is not None
        and f_class(r["function_signal"]) is not None
    ]

    # Interaction decline is not sufficient for reproductive decline.
    lower_i_states = {f for _, i, f in mapped if i == "lower"}
    assert "lower" in lower_i_states
    assert "higher" in lower_i_states or "not_lower" in lower_i_states

    # Interaction decline is not necessary for reproductive decline.
    i_states_for_lower_f = {i for _, i, f in mapped if f == "lower"}
    assert "lower" in i_states_for_lower_f
    assert "higher" in i_states_for_lower_f or "no_detected_loss" in i_states_for_lower_f

    # Apparently intact/elevated interaction is not sufficient to assure function.
    assert any(i == "higher" and f == "lower" for _, i, f in mapped)
    assert any(i == "no_detected_loss" and f == "lower" for _, i, f in mapped)

    # Strict directional subset removes no-detected-loss and mixed states.
    strict = [
        (r["programme_id"], i_class(r["interaction_signal"]), f_class(r["function_signal"]))
        for r in rs
        if r["interaction_signal"] not in {"no_detected_loss", "mixed"}
        and r["function_signal"] not in {"no_detected_loss", "mixed"}
        and i_class(r["interaction_signal"]) is not None
        and f_class(r["function_signal"]) is not None
    ]
    strict_lower_i = {f for _, i, f in strict if i == "lower"}
    strict_higher_i = {f for _, i, f in strict if i == "higher"}
    assert {"lower", "higher"} <= strict_lower_i
    assert {"lower", "not_lower"} <= strict_higher_i

    # Explicit counterexamples, frozen by programme identity.
    lower_not_lower = {
        pid for pid, i, f in mapped
        if i == "lower" and f in {"higher", "not_lower"}
    }
    nonlower_lower = {
        pid for pid, i, f in mapped
        if i in {"higher", "no_detected_loss"} and f == "lower"
    }
    assert {"P2_CF01_MILKWEED_URBAN_2023", "QIF002", "QIF003"} <= lower_not_lower
    assert {"ML015", "QIF008"} <= nonlower_lower

    print(
        "IF_NECESSITY_SUFFICIENCY_OK "
        "programmes=16 "
        "interaction_decline_not_sufficient=true "
        "interaction_decline_not_necessary=true "
        "intact_or_higher_interaction_not_function_guarantee=true "
        "strict_directional_nonmonotonic=true "
        f"lower_I_counterexamples={len(lower_not_lower)} "
        f"nonlower_I_lower_F_counterexamples={len(nonlower_lower)} "
        "prevalence_inference=false"
    )


if __name__ == "__main__":
    main()
