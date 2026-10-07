from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
NOTE = ROOT / "manuscript/SF06_SIGN_MARGIN_SENSITIVITY_2026-10-07.md"

OVERLAP = {
    "aizen & feinsinger (1994) ecology 75:330- 351",
    "angoh et al. (2021) south african journal of botany 141:196- 199",
    "chen & zuo (2019) frontiers in plant science 10:327",
    "chen et al. (2019) science of the total environment 654:1056- 1063",
    "chiapero et al. (2021) forest ecology and management 492:119215",
    "da silva elias et al. (2012) journal of tropical ecology 28:317- 320",
    "gonzález-varo et al. (2009) biological conservation 142:1058- 1065",
    "kolb (2008) biological conservation 141:2540- 2549",
    "lopes & buzato (2007) oecologia 154:305- 314",
}


def audit(rows: list[dict[str, str]], eps: float) -> tuple:
    kept = [
        r for r in rows
        if abs(float(r["d_I"])) >= eps and abs(float(r["d_F"])) >= eps
    ]
    ll = sum(float(r["d_I"]) < 0 and float(r["d_F"]) < 0 for r in kept)
    ln = sum(float(r["d_I"]) < 0 and float(r["d_F"]) >= 0 for r in kept)
    nl = sum(float(r["d_I"]) >= 0 and float(r["d_F"]) < 0 for r in kept)
    nn = sum(float(r["d_I"]) >= 0 and float(r["d_F"]) >= 0 for r in kept)
    mismatch = min(ll, ln) + min(nl, nn)
    f_lower = ll + nl
    f_nonlower = ln + nn
    baseline = len(kept) - max(f_lower, f_nonlower)
    return len(kept), ll, ln, nl, nn, mismatch, baseline, baseline - mismatch


def main() -> None:
    with PAIRS.open(newline="", encoding="utf-8") as fh:
        rows = [
            r for r in csv.DictReader(fh)
            if r["land_use_factor_normalized"] == "habitat fragmentation"
        ]
    nonoverlap = [r for r in rows if r["source_publication_key"] not in OVERLAP]

    eps = (0.0, 0.1, 0.2, 0.3, 0.5)
    full = {e: audit(rows, e) for e in eps}
    ext = {e: audit(nonoverlap, e) for e in eps}

    assert full == {
        0.0: (55, 36, 9, 7, 3, 12, 12, 0),
        0.1: (41, 30, 5, 4, 2, 7, 7, 0),
        0.2: (31, 24, 2, 3, 2, 4, 4, 0),
        0.3: (28, 21, 2, 3, 2, 4, 4, 0),
        0.5: (18, 13, 2, 1, 2, 3, 4, 1),
    }
    assert ext == {
        0.0: (32, 21, 6, 4, 1, 7, 7, 0),
        0.1: (24, 18, 3, 2, 1, 4, 4, 0),
        0.2: (17, 13, 2, 1, 1, 3, 3, 0),
        0.3: (14, 10, 2, 1, 1, 3, 3, 0),
        0.5: (12, 9, 2, 0, 1, 2, 3, 1),
    }

    note = NOTE.read_text(encoding="utf-8")
    assert "| 0.5 | 18 | 13 | 2 | 1 | 2 | 3 | 4 | 1 |" in note
    assert "| 0.5 | 12 | 9 | 2 | 0 | 1 | 2 | 3 | 1 |" in note
    assert "not generated only by near-zero effects" in note

    print("SF06_SIGN_MARGIN_SENSITIVITY: PASS")


if __name__ == "__main__":
    main()
