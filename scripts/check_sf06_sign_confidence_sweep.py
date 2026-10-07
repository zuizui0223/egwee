from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
NOTE = ROOT / "manuscript/SF06_SIGN_CONFIDENCE_SWEEP_2026-10-07.md"

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


def phi(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def audit(rows: list[dict], q: float) -> tuple:
    kept = [r for r in rows if r["pI"] >= q and r["pF"] >= q]
    ll = sum(r["dI"] < 0 and r["dF"] < 0 for r in kept)
    ln = sum(r["dI"] < 0 and r["dF"] >= 0 for r in kept)
    nl = sum(r["dI"] >= 0 and r["dF"] < 0 for r in kept)
    nn = sum(r["dI"] >= 0 and r["dF"] >= 0 for r in kept)
    mismatch = min(ll, ln) + min(nl, nn)
    return len(kept), ll, ln, nl, nn, mismatch


def main() -> None:
    with PAIRS.open(newline="", encoding="utf-8") as fh:
        rows = []
        for r in csv.DictReader(fh):
            if r["land_use_factor_normalized"] != "habitat fragmentation":
                continue
            dI = float(r["d_I"]); dF = float(r["d_F"])
            seI = math.sqrt(float(r["var_I"])); seF = math.sqrt(float(r["var_F"]))
            rows.append({
                "group": r["source_publication_key"],
                "dI": dI,
                "dF": dF,
                "pI": phi(abs(dI) / seI),
                "pF": phi(abs(dF) / seF),
            })

    ext = [r for r in rows if r["group"] not in OVERLAP]
    qs = (0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.975)

    full = {q: audit(rows, q) for q in qs}
    nonoverlap = {q: audit(ext, q) for q in qs}

    assert full == {
        0.50: (55, 36, 9, 7, 3, 12),
        0.60: (37, 27, 3, 4, 3, 6),
        0.70: (30, 24, 2, 2, 2, 4),
        0.80: (18, 15, 1, 1, 1, 2),
        0.90: (10, 9, 1, 0, 0, 1),
        0.95: (6, 5, 1, 0, 0, 1),
        0.975: (4, 4, 0, 0, 0, 0),
    }
    assert nonoverlap == {
        0.50: (32, 21, 6, 4, 1, 7),
        0.60: (21, 15, 3, 2, 1, 4),
        0.70: (16, 12, 2, 1, 1, 3),
        0.80: (12, 10, 1, 0, 1, 1),
        0.90: (7, 6, 1, 0, 0, 1),
        0.95: (6, 5, 1, 0, 0, 1),
        0.975: (4, 4, 0, 0, 0, 0),
    }

    note = NOTE.read_text(encoding="utf-8")
    assert "| **0.95** | **6** | **5** | **1** | 0 | 0 | **1** |" in note
    assert "q=0.975" in note
    assert "source-disjoint mismatch persists" in note

    print("SF06_SIGN_CONFIDENCE_SWEEP: PASS")


if __name__ == "__main__":
    main()
