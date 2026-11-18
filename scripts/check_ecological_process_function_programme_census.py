from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIFIED = ROOT / "evidence/meta_extraction/ecological_process_function_programme_census_v1.csv"
IF_CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
MF_CENSUS = ROOT / "evidence/meta_extraction/ecological_mating_function_programme_census_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    unified = rows(UNIFIED)
    if_rows = rows(IF_CENSUS)
    mf_rows = rows(MF_CENSUS)

    assert len(if_rows) == 8
    assert len(mf_rows) == 4
    if_ids = {r["programme_id"] for r in if_rows}
    mf_ids = {r["programme_id"] for r in mf_rows}
    assert if_ids.isdisjoint(mf_ids)

    by = {r["programme_id"]: r for r in unified}
    assert len(unified) == 12
    assert set(by) == if_ids | mf_ids

    # I-F programmes map exactly into the unified census.
    for src in if_rows:
        row = by[src["programme_id"]]
        assert row["system"] == src["system"]
        assert row["source_id"] == src["source_id"]
        assert row["process_stage"] == "interaction_quantity"
        assert row["process_endpoint"] == src["i_endpoint"]
        assert row["measurement_class"] == "quantity_only"
        assert row["effect_family"] == src["effect_family"]
        assert row["n_dependent_panels"] == src["n_dependent_if_panels"]
        assert row["pair_testable"] == src["if_pair_testable"]
        assert row["resolved_mismatch"] == src["resolved_if_mismatch"]
        if src["programme_adjusted_p"]:
            assert abs(float(row["programme_adjusted_p"]) - float(src["programme_adjusted_p"])) < 5e-8
        else:
            assert row["programme_adjusted_p"] == ""
        if src["resolved_direction"] == "F_more_negative_than_I":
            assert row["resolved_direction"] == "F_more_negative_than_process"
            assert row["ecological_regime"] == "downstream_function_dominant"
        elif src["resolved_direction"] == "unresolved":
            assert row["resolved_direction"] == "unresolved"
            assert row["ecological_regime"] == "unresolved_process_function_difference"
        else:
            assert src["resolved_direction"] == "not_testable"
            assert row["resolved_direction"] == "not_testable"
            assert row["ecological_regime"] == "not_testable"

    # Movement/mating-F programmes map exactly into the unified census.
    mf_stage = {
        "ML001": "movement_connectivity",
        "ML002": "movement_connectivity",
        "ML014": "mating_support",
        "P2_CF01_ACER_MIYABEI_2014": "movement_connectivity",
    }
    for src in mf_rows:
        row = by[src["programme_id"]]
        assert row["system"] == src["system"]
        assert row["source_id"] == src["source_id"]
        assert row["process_stage"] == mf_stage[src["programme_id"]]
        assert row["process_endpoint"] == src["process_endpoint"]
        assert row["measurement_class"] == "movement_or_mating_support"
        assert row["effect_family"] == src["effect_family"]
        assert row["pair_testable"] == "yes"
        assert row["resolved_mismatch"] == src["resolved_mismatch"]
        assert abs(float(row["programme_adjusted_p"]) - float(src["programme_adjusted_p"])) < 5e-8
        if src["resolved_direction"] == "process_more_negative_than_F":
            assert row["resolved_direction"] == "process_more_negative_than_F"
            assert row["ecological_regime"] == "upstream_process_dominant"
        else:
            assert src["resolved_direction"] == "unresolved"
            assert row["resolved_direction"] == "unresolved"
            assert row["ecological_regime"] == "unresolved_process_function_difference"

    testable = [r for r in unified if r["pair_testable"] == "yes"]
    resolved = [r for r in unified if r["resolved_mismatch"] == "yes"]
    unresolved = [r for r in unified if r["resolved_mismatch"] == "no"]
    not_testable = [r for r in unified if r["resolved_mismatch"] == "not_testable"]

    assert len(testable) == 11
    assert len(resolved) == 4
    assert len(unresolved) == 7
    assert len(not_testable) == 1

    assert sum(r["resolved_direction"] == "F_more_negative_than_process" for r in resolved) == 3
    assert sum(r["resolved_direction"] == "process_more_negative_than_F" for r in resolved) == 1

    assert sum(r["measurement_class"] == "quantity_only" for r in unified) == 8
    assert sum(r["measurement_class"] == "movement_or_mating_support" for r in unified) == 4

    assert sum(r["ecological_regime"] == "downstream_function_dominant" for r in unified) == 3
    assert sum(r["ecological_regime"] == "upstream_process_dominant" for r in unified) == 1
    assert sum(r["ecological_regime"] == "unresolved_process_function_difference" for r in unified) == 7
    assert sum(r["ecological_regime"] == "not_testable" for r in unified) == 1

    print(
        "ECOLOGICAL_PROCESS_FUNCTION_CENSUS_OK "
        "programmes=12 testable=11 resolved=4 unresolved=7 not_testable=1 "
        "resolved_downstream_F=3 resolved_upstream_process=1 "
        "quantity_I=8 movement_mating=4"
    )


if __name__ == "__main__":
    main()
