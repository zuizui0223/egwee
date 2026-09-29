from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "evidence/meta_extraction/if_sign_geometry_census_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    rs = rows(CENSUS)
    assert len(rs) == 18

    programmes = {r["programme_id"] for r in rs}
    assert len(programmes) == 8

    counts = {}
    for r in rs:
        counts[r["sign_geometry"]] = counts.get(r["sign_geometry"], 0) + 1

    assert counts == {
        "concordant_deterioration": 8,
        "concordant_improvement": 4,
        "function_buffered_or_compensated": 4,
        "hidden_function_loss": 2,
    }

    discordant = [
        r for r in rs
        if r["interaction_sign"] != r["function_sign"]
    ]
    assert len(discordant) == 6

    discordant_programmes = {r["programme_id"] for r in discordant}
    assert discordant_programmes == {
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "ML015",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
    }

    hidden_loss_programmes = {
        r["programme_id"] for r in rs
        if r["sign_geometry"] == "hidden_function_loss"
    }
    buffered_programmes = {
        r["programme_id"] for r in rs
        if r["sign_geometry"] == "function_buffered_or_compensated"
    }
    assert hidden_loss_programmes == {
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "ML015",
    }
    assert buffered_programmes == {
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
    }

    # Multi-panel programmes sharing one registered landscape/exposure frame.
    multi = {}
    for r in rs:
        multi.setdefault(r["programme_id"], []).append(r["sign_geometry"])
    multi = {k: v for k, v in multi.items() if len(v) > 1}
    assert set(multi) == {
        "ML020",
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "P2_CF01_ZURICH_2026",
    }

    heterogeneous = {
        pid for pid, geoms in multi.items()
        if len(set(geoms)) > 1
    }
    assert heterogeneous == {
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "P2_CF01_ZURICH_2026",
    }
    assert set(multi["ML020"]) == {"concordant_deterioration"}

    # Scale robustness of sign geometry:
    # direct positive-valued contrasts preserve sign under g -> lnRR;
    # gradient programmes remain on their registered Fisher-z representation.
    assert all(r["scale_status"] in {"direct_sign_scale_invariant", "native_fisher_z"} for r in rs)

    print(
        "IF_SIGN_GEOMETRY_OK "
        "panels=18 programmes=8 discordant_panels=6 discordant_programmes=5 "
        "hidden_function_loss_programmes=2 buffered_or_gain_programmes=3 "
        "multi_panel_programmes=4 within_program_heterogeneous=3"
    )


if __name__ == "__main__":
    main()
