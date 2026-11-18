from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
NOTE = ROOT / "manuscript/SF06_SEVERITY_DIAGNOSTIC_THRESHOLD_SWEEP_2026-10-07.md"

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


def auc(rows, threshold):
    pos = [r for r in rows if r["dF"] < threshold]
    neg = [r for r in rows if r["dF"] >= threshold]
    wins = total = 0.0
    for p in pos:
        for n in neg:
            sp = -p["dI"]
            sn = -n["dI"]
            wins += 1.0 if sp > sn else 0.5 if sp == sn else 0.0
            total += 1.0
    return wins / total


def sign_lookup(rows, threshold):
    errors = 0
    for lower in (True, False):
        rr = [r for r in rows if (r["dI"] < 0) == lower]
        target = sum(r["dF"] < threshold for r in rr)
        other = len(rr) - target
        errors += min(target, other)
    target = sum(r["dF"] < threshold for r in rows)
    baseline = min(target, len(rows) - target)
    return baseline, errors, baseline - errors


def main() -> None:
    with PAIRS.open(newline="", encoding="utf-8") as fh:
        rows = [
            {
                "pub": r["source_publication_key"],
                "dI": float(r["d_I"]),
                "dF": float(r["d_F"]),
            }
            for r in csv.DictReader(fh)
            if r["land_use_factor_normalized"] == "habitat fragmentation"
        ]
    ext = [r for r in rows if r["pub"] not in OVERLAP]
    thresholds = (0.0, -0.2, -0.5, -0.8, -1.0)

    expected_full = {
        0.0: (0.5872093023255814, (12, 12, 0)),
        -0.2: (0.6038011695906432, (19, 17, 2)),
        -0.5: (0.6411290322580645, (24, 24, 0)),
        -0.8: (0.6117216117216118, (13, 13, 0)),
        -1.0: (0.6065891472868217, (12, 12, 0)),
    }
    expected_ext = {
        0.0: (0.5714285714285714, (7, 7, 0)),
        -0.2: (0.6125, (12, 11, 1)),
        -0.5: (0.7058823529411765, (15, 12, 3)),
        -0.8: (0.6045454545454545, (10, 10, 0)),
        -1.0: (0.5845410628019324, (9, 9, 0)),
    }

    for threshold in thresholds:
        a = auc(rows, threshold)
        e = auc(ext, threshold)
        assert math.isclose(a, expected_full[threshold][0], rel_tol=1e-12)
        assert sign_lookup(rows, threshold) == expected_full[threshold][1]
        assert math.isclose(e, expected_ext[threshold][0], rel_tol=1e-12)
        assert sign_lookup(ext, threshold) == expected_ext[threshold][1]

    note = NOTE.read_text(encoding="utf-8")
    assert "| -0.5 | 24 | 0.641 | 24 | 24 | 0 |" in note
    assert "| -0.5 | 17 | 0.706 | 15 | 12 | 3 |" in note
    assert "insufficient stand-alone diagnostic/sentinel" in note

    print("SF06_SEVERITY_DIAGNOSTIC_THRESHOLD_SWEEP: PASS")


if __name__ == "__main__":
    main()
