from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "evidence/meta_extraction/ecological_process_function_programme_census_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def resolved_directions(rs: list[dict[str, str]]) -> set[str]:
    return {
        r["resolved_direction"]
        for r in rs
        if r["resolved_mismatch"] == "yes"
    }


def main() -> None:
    census = rows(CENSUS)
    assert len(census) == 12

    full = resolved_directions(census)
    assert full == {"F_more_negative_than_process", "process_more_negative_than_F"}

    lost_both_directions: list[str] = []
    retained_both_directions: list[str] = []

    for drop in census:
        subset = [r for r in census if r["programme_id"] != drop["programme_id"]]
        directions = resolved_directions(subset)
        if len(directions) < 2:
            lost_both_directions.append(drop["programme_id"])
        else:
            retained_both_directions.append(drop["programme_id"])

    assert lost_both_directions == ["ML001"]
    assert len(retained_both_directions) == 11

    without_serapias = [
        r for r in census
        if r["programme_id"] != "ML001" and r["resolved_mismatch"] == "yes"
    ]
    assert len(without_serapias) == 3
    assert {r["resolved_direction"] for r in without_serapias} == {"F_more_negative_than_process"}

    downstream_ids = {
        r["programme_id"]
        for r in census
        if r["resolved_direction"] == "F_more_negative_than_process"
    }
    assert downstream_ids == {
        "ML015",
        "P2_CF01_CARDIOPETALUM_2012",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
    }

    print(
        "ECOLOGICAL_BOTTLENECK_INFLUENCE_OK "
        "programmes=12 full_directions=2 "
        "direction_diversity_lost_only_if_drop=ML001 "
        "without_ML001_resolved=3 without_ML001_direction=downstream_F_only"
    )


if __name__ == "__main__":
    main()
