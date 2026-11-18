from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
NOTE = ROOT / "manuscript/SF06_LOPO_PREDICTIVE_VALUE_2026-10-07.md"


def fit(rows: list[dict], fields: tuple[str, ...]) -> np.ndarray:
    X = np.array([[1.0] + [r[f] for f in fields] for r in rows], dtype=float)
    y = np.array([r["y"] for r in rows], dtype=float)
    return np.linalg.lstsq(X, y, rcond=None)[0]


def predict(beta: np.ndarray, r: dict, fields: tuple[str, ...]) -> float:
    x = np.array([1.0] + [r[f] for f in fields], dtype=float)
    return float(x @ beta)


def lopo(rows: list[dict], baseline_fields: tuple[str, ...], full_fields: tuple[str, ...]) -> dict:
    groups = sorted({r["group"] for r in rows})
    total = {
        "n": 0,
        "sse0": 0.0,
        "sse1": 0.0,
        "sae0": 0.0,
        "sae1": 0.0,
        "correct0": 0,
        "correct1": 0,
    }
    per_pub = []
    for group in groups:
        train = [r for r in rows if r["group"] != group]
        test = [r for r in rows if r["group"] == group]
        b0 = fit(train, baseline_fields)
        b1 = fit(train, full_fields)

        ss0 = ss1 = ae0 = ae1 = 0.0
        c0 = c1 = 0
        for r in test:
            p0 = predict(b0, r, baseline_fields)
            p1 = predict(b1, r, full_fields)
            ss0 += (r["y"] - p0) ** 2
            ss1 += (r["y"] - p1) ** 2
            ae0 += abs(r["y"] - p0)
            ae1 += abs(r["y"] - p1)
            c0 += (p0 < 0) == (r["y"] < 0)
            c1 += (p1 < 0) == (r["y"] < 0)

        n = len(test)
        total["n"] += n
        total["sse0"] += ss0
        total["sse1"] += ss1
        total["sae0"] += ae0
        total["sae1"] += ae1
        total["correct0"] += c0
        total["correct1"] += c1
        per_pub.append({
            "mse0": ss0 / n,
            "mse1": ss1 / n,
            "mae0": ae0 / n,
            "mae1": ae1 / n,
        })

    n = total["n"]
    return {
        "n": n,
        "n_publications": len(groups),
        "row_mse0": total["sse0"] / n,
        "row_mse1": total["sse1"] / n,
        "row_mae0": total["sae0"] / n,
        "row_mae1": total["sae1"] / n,
        "row_acc0": total["correct0"] / n,
        "row_acc1": total["correct1"] / n,
        "pub_mse0": float(np.mean([x["mse0"] for x in per_pub])),
        "pub_mse1": float(np.mean([x["mse1"] for x in per_pub])),
        "pub_mae0": float(np.mean([x["mae0"] for x in per_pub])),
        "pub_mae1": float(np.mean([x["mae1"] for x in per_pub])),
    }


def main() -> None:
    with PAIRS.open(newline="", encoding="utf-8") as fh:
        raw = [
            r for r in csv.DictReader(fh)
            if r["land_use_factor_normalized"] == "habitat fragmentation"
        ]

    all_rows = [
        {
            "group": r["source_publication_key"],
            "y": float(r["d_F"]),
            "dI": float(r["d_I"]),
        }
        for r in raw
    ]
    sc_rows = [
        {
            "group": r["source_publication_key"],
            "y": float(r["d_F"]),
            "dI": float(r["d_I"]),
            "SC": 1.0 if r["compatibility"] == "SC" else 0.0,
        }
        for r in raw if r["compatibility"] in {"SC", "SI"}
    ]

    a = lopo(all_rows, (), ("dI",))
    b = lopo(sc_rows, ("SC",), ("dI", "SC"))

    expected = {
        "a_row_mse0": 0.4553591777722885,
        "a_row_mse1": 0.4451088467534139,
        "a_row_mae0": 0.5174039239392523,
        "a_row_mae1": 0.5225738815230311,
        "a_acc0": 0.7818181818181819,
        "a_acc1": 0.7636363636363637,
        "a_pub_mse0": 0.4644559109627117,
        "a_pub_mse1": 0.448385813114355,
        "b_row_mse0": 0.41083595687968977,
        "b_row_mse1": 0.4007037341968013,
        "b_acc0": 0.7755102040816326,
        "b_acc1": 0.7551020408163265,
        "b_pub_mse0": 0.36310158609482734,
        "b_pub_mse1": 0.3496011473893452,
    }
    observed = {
        "a_row_mse0": a["row_mse0"],
        "a_row_mse1": a["row_mse1"],
        "a_row_mae0": a["row_mae0"],
        "a_row_mae1": a["row_mae1"],
        "a_acc0": a["row_acc0"],
        "a_acc1": a["row_acc1"],
        "a_pub_mse0": a["pub_mse0"],
        "a_pub_mse1": a["pub_mse1"],
        "b_row_mse0": b["row_mse0"],
        "b_row_mse1": b["row_mse1"],
        "b_acc0": b["row_acc0"],
        "b_acc1": b["row_acc1"],
        "b_pub_mse0": b["pub_mse0"],
        "b_pub_mse1": b["pub_mse1"],
    }
    for k, v in expected.items():
        assert math.isclose(observed[k], v, rel_tol=1e-9, abs_tol=1e-9), (k, observed[k], v)

    note = NOTE.read_text(encoding="utf-8")
    assert "MSE reduction = **2.25%**" in note
    assert "MSE reduction = **3.72%**" in note
    assert "77.6% SC-only vs 75.5% with pollination" in note

    print(
        "SF06_LOPO_PREDICTIVE_VALUE: PASS "
        f"all_mse_gain={(a['row_mse0']-a['row_mse1'])/a['row_mse0']:.4f} "
        f"sc_mse_gain={(b['row_mse0']-b['row_mse1'])/b['row_mse0']:.4f}"
    )


if __name__ == "__main__":
    main()
