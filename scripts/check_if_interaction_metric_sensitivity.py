from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"
METRICS = ROOT / "evidence/meta_extraction/if_interaction_metric_class_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def f_states(rs: list[dict[str, str]], i_state: str) -> set[str]:
    return {
        r["function_signal"]
        for r in rs
        if r["interaction_signal"] == i_state
    }


def ambiguous_inputs(rs: list[dict[str, str]]) -> set[str]:
    states = {r["interaction_signal"] for r in rs}
    return {s for s in states if len(f_states(rs, s)) >= 2}


def main() -> None:
    mapping = rows(MAP)
    metrics = rows(METRICS)
    assert len(mapping) == len(metrics) == 16

    metric_by = {r["programme_id"]: r for r in metrics}
    assert set(metric_by) == {r["programme_id"] for r in mapping}

    visitation_ids = {
        pid for pid, r in metric_by.items()
        if r["interaction_metric_class"] == "visitation_abundance"
    }
    assert len(visitation_ids) == 13

    visit = [r for r in mapping if r["programme_id"] in visitation_ids]
    assert len(visit) == 13

    # Metric-homogeneous existence result.
    assert {"lower", "higher", "no_detected_loss"} <= f_states(visit, "lower")
    assert {"lower", "no_detected_loss"} <= f_states(visit, "no_detected_loss")
    assert ambiguous_inputs(visit) >= {"lower", "no_detected_loss"}

    # No single programme carries the visitation-only non-identifiability result.
    for drop in visitation_ids:
        subset = [r for r in visit if r["programme_id"] != drop]
        assert ambiguous_inputs(subset), drop

    # Conservative explicit-direction subset removes mixed/no-detected states.
    strict = [
        r for r in visit
        if r["interaction_signal"] not in {"mixed", "no_detected_loss"}
        and r["function_signal"] not in {"mixed", "no_detected_loss"}
    ]
    assert len(strict) == 6
    assert f_states(strict, "lower") == {"lower", "higher"}
    assert f_states(strict, "higher") == {"similar"}

    # The strict lower->multiple-F result is carried by the milkweed higher-F point state.
    strict_without_milkweed = [
        r for r in strict
        if r["programme_id"] != "P2_CF01_MILKWEED_URBAN_2023"
    ]
    assert f_states(strict_without_milkweed, "lower") == {"lower"}

    print(
        "IF_METRIC_SENSITIVITY_OK "
        "programmes=16 visitation_abundance_programmes=13 "
        "visitation_lower_maps_to=lower+higher+no_detected_loss "
        "visitation_no_detected_loss_maps_to=lower+no_detected_loss "
        "visitation_only_LOO_nonidentifying=true "
        "strict_visitation_programmes=6 strict_lower_maps_to=lower+higher "
        "strict_lower_ambiguity_milkweed_dependent=true "
        "prevalence_inference=false"
    )


if __name__ == "__main__":
    main()
