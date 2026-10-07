from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
NOTE = ROOT / "manuscript/SF06_LOPO_SIGN_PROBABILITY_VALUE_2026-10-07.md"

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


def lopo(rows: list[dict], alpha: float) -> dict:
    groups = sorted({r["group"] for r in rows})
    b0 = b1 = l0 = l1 = 0.0
    n = 0
    per = []

    for g in groups:
        train = [r for r in rows if r["group"] != g]
        test = [r for r in rows if r["group"] == g]

        sy = sum(r["y"] for r in train)
        p0 = (sy + alpha) / (len(train) + 2 * alpha)

        p = {}
        for x in (0, 1):
            vals = [r["y"] for r in train if r["x"] == x]
            p[x] = (sum(vals) + alpha) / (len(vals) + 2 * alpha)

        pb0 = pb1 = pl0 = pl1 = 0.0
        for r in test:
            q0 = p0
            q1 = p[r["x"]]
            pb0 += (r["y"] - q0) ** 2
            pb1 += (r["y"] - q1) ** 2
            pl0 += -(r["y"] * math.log(q0) + (1-r["y"]) * math.log(1-q0))
            pl1 += -(r["y"] * math.log(q1) + (1-r["y"]) * math.log(1-q1))

        k = len(test)
        b0 += pb0; b1 += pb1; l0 += pl0; l1 += pl1; n += k
        per.append((pb0/k, pb1/k, pl0/k, pl1/k))

    return {
        "n": n,
        "brier0": b0/n,
        "brier1": b1/n,
        "log0": l0/n,
        "log1": l1/n,
        "pub_brier0": sum(x[0] for x in per)/len(per),
        "pub_brier1": sum(x[1] for x in per)/len(per),
        "pub_log0": sum(x[2] for x in per)/len(per),
        "pub_log1": sum(x[3] for x in per)/len(per),
    }


def close(a: float, b: float) -> None:
    assert math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9), (a, b)


def main() -> None:
    with PAIRS.open(newline="", encoding="utf-8") as fh:
        rows = [
            {
                "group": r["source_publication_key"],
                "x": 1 if float(r["d_I"]) < 0 else 0,
                "y": 1 if float(r["d_F"]) < 0 else 0,
            }
            for r in csv.DictReader(fh)
            if r["land_use_factor_normalized"] == "habitat fragmentation"
        ]

    ext = [r for r in rows if r["group"] not in OVERLAP]

    full_l = lopo(rows, 1.0)
    ext_l = lopo(ext, 1.0)
    full_j = lopo(rows, 0.5)
    ext_j = lopo(ext, 0.5)

    close(full_l["brier0"], 0.17421488481756345)
    close(full_l["brier1"], 0.1781122313327732)
    close(full_l["log0"], 0.5350839195374845)
    close(full_l["log1"], 0.5434820994149493)

    close(ext_l["brier0"], 0.17875050505050513)
    close(ext_l["brier1"], 0.1889659509637188)
    close(ext_l["log0"], 0.5476765297505461)
    close(ext_l["log1"], 0.5747625779908286)

    close(full_j["brier0"], 0.17429604603593668)
    close(full_j["brier1"], 0.17866241232508798)
    close(ext_j["brier0"], 0.17874399820963544)
    close(ext_j["brier1"], 0.19002164780521255)

    note = NOTE.read_text(encoding="utf-8")
    assert "0.17421" in note
    assert "0.17811" in note
    assert "0.17875 → 0.18897" in note
    assert "association is not the same thing as incremental sentinel information" in note

    print(
        "SF06_LOPO_SIGN_PROBABILITY_VALUE: PASS "
        f"full_brier_delta={(full_l['brier1']-full_l['brier0'])/full_l['brier0']:.4f} "
        f"ext_brier_delta={(ext_l['brier1']-ext_l['brier0'])/ext_l['brier0']:.4f}"
    )


if __name__ == "__main__":
    main()
