from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
NOTE = ROOT / "manuscript/SF06_WITHIN_PUBLICATION_COUPLING_2026-10-07.md"


def slope_corr(rows):
    mx = sum(r["x"] for r in rows) / len(rows)
    my = sum(r["y"] for r in rows) / len(rows)
    num = sum((r["x"] - mx) * (r["y"] - my) for r in rows)
    dx = sum((r["x"] - mx) ** 2 for r in rows)
    dy = sum((r["y"] - my) ** 2 for r in rows)
    return num / dx, num / math.sqrt(dx * dy)


def main() -> None:
    with PAIRS.open(newline="", encoding="utf-8") as fh:
        rows = [
            {
                "group": r["source_publication_key"],
                "x": float(r["d_I"]),
                "y": float(r["d_F"]),
            }
            for r in csv.DictReader(fh)
            if r["land_use_factor_normalized"] == "habitat fragmentation"
        ]

    groups = defaultdict(list)
    for r in rows:
        groups[r["group"]].append(r)
    multi = {g: rr for g, rr in groups.items() if len(rr) > 1}
    assert sorted(len(rr) for rr in multi.values()) == [9, 15]

    results = {g: slope_corr(rr) for g, rr in multi.items()}
    aguilar = next(v for g, v in results.items() if g.startswith("aguilar (2005)"))
    chaco = next(v for g, v in results.items() if g.startswith("aizen & feinsinger (1994)"))
    assert math.isclose(aguilar[0], 0.5961847042113811, rel_tol=1e-12)
    assert math.isclose(aguilar[1], 0.41350000165585604, rel_tol=1e-12)
    assert math.isclose(chaco[0], 0.15728439686925327, rel_tol=1e-12)
    assert math.isclose(chaco[1], 0.31941890207553975, rel_tol=1e-12)

    num = den = 0.0
    for rr in multi.values():
        mx = sum(r["x"] for r in rr) / len(rr)
        my = sum(r["y"] for r in rr) / len(rr)
        for r in rr:
            num += (r["x"] - mx) * (r["y"] - my)
            den += (r["x"] - mx) ** 2
    within = num / den
    assert math.isclose(within, 0.23929101438428033, rel_tol=1e-12)

    overall = slope_corr(rows)[0]
    assert math.isclose(overall, 0.2198292930278231, rel_tol=1e-12)

    means = []
    for g, rr in groups.items():
        means.append({
            "x": sum(r["x"] for r in rr) / len(rr),
            "y": sum(r["y"] for r in rr) / len(rr),
        })
    between = slope_corr(means)[0]
    assert math.isclose(between, 0.242534143709277, rel_tol=1e-12)

    note = NOTE.read_text(encoding="utf-8")
    assert "pooled within-publication slope = **+0.239**" in note
    assert "simple slope across all 55 fragmentation pairs = **+0.220**" in note

    print("SF06_WITHIN_PUBLICATION_COUPLING: PASS")


if __name__ == "__main__":
    main()
