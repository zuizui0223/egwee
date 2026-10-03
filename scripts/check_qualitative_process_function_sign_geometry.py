from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "evidence/meta_extraction/qualitative_process_function_sign_geometry_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    rs = rows(TABLE)
    assert len(rs) == 22

    programmes = {r["programme_id"] for r in rs}
    assert len(programmes) == 12

    opposite = [r for r in rs if r["sign_geometry"] == "opposite_sign"]
    same = [r for r in rs if r["sign_geometry"] == "same_sign"]
    assert len(opposite) == 7
    assert len(same) == 15

    discordant_programmes = {r["programme_id"] for r in opposite}
    assert discordant_programmes == {
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "ML015",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
        "P2_CF01_ACER_MIYABEI_2014",
    }
    assert len(discordant_programmes) == 6

    direct_discordant = {r["programme_id"] for r in opposite if r["design_stream"] == "direct"}
    gradient_discordant = {r["programme_id"] for r in opposite if r["design_stream"] == "gradient"}
    assert direct_discordant == {
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
    }
    assert gradient_discordant == {
        "ML015",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
        "P2_CF01_ACER_MIYABEI_2014",
    }

    failure_programmes = {
        r["programme_id"] for r in opposite
        if r["qualitative_mode"].startswith("downstream_failure")
    }
    buffering_programmes = {
        r["programme_id"] for r in opposite
        if r["qualitative_mode"] == "downstream_buffering"
    }
    assert failure_programmes == {
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "ML015",
        "P2_CF01_ACER_MIYABEI_2014",
    }
    assert buffering_programmes == {
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
    }

    # Panel-level direction is also bidirectional.
    assert sum(r["qualitative_mode"].startswith("downstream_failure") for r in opposite) == 3
    assert sum(r["qualitative_mode"] == "downstream_buffering" for r in opposite) == 4

    # Acer's function estimate is essentially zero, so keep it visibly fragile.
    acer = next(r for r in opposite if r["programme_id"] == "P2_CF01_ACER_MIYABEI_2014")
    assert abs(float(acer["reproductive_effect"])) < 0.001
    assert acer["qualitative_mode"] == "downstream_failure_near_zero_F"

    print(
        "QUALITATIVE_SIGN_GEOMETRY_OK "
        "programmes=12 panels=22 opposite_panels=7 same_sign_panels=15 "
        "programmes_with_opposite_sign=6 direct=2 gradient=4 "
        "failure_programmes=3 buffering_programmes=3 "
        "failure_panels=3 buffering_panels=4 acer_near_zero_F=true"
    )


if __name__ == "__main__":
    main()
