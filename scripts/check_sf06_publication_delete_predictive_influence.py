#!/usr/bin/env python3
"""Post hoc nested publication-deletion influence audit for the public SF06 sign-sentinel.

Re-fits both conditional-sign and context-only probability rules after deleting
each whole source publication. This *does not* convert literature-derived point
signs into verified physiological states or estimate monitoring error prevalence.
No frozen EGWEE effect, corpus membership, or preregistered claim is changed.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
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
HAUBER = "hauber et al. (2022) south african journal of botany 146:48- 57"


def selected_pairs() -> list[dict]:
    with PAIRS.open(encoding="utf-8", newline="") as fh:
        source = list(csv.DictReader(fh))
    assert len(source) == 59, len(source)
    rows = []
    for r in source:
        if r["land_use_factor_normalized"] != "habitat fragmentation":
            continue
        x, y = (r["I_component_consensus_sign"],
                r["F_component_consensus_sign"])
        if x not in {"lower", "nonlower"} or y not in {"lower", "nonlower"}:
            continue
        rows.append({"pub": r["source_publication_key"],
                     "x": int(x == "lower"), "y": int(y == "lower")})
    assert len(rows) == 54
    return rows


def lopo_delta(rows: list[dict], alpha: float) -> dict:
    """Compare honest held-publication losses, with *both* models refitted."""
    assert alpha > 0
    groups = sorted({r["pub"] for r in rows})
    total_brier = 0.0
    total_logloss = 0.0
    per_pub: list[float] = []
    for pub in groups:
        train = [r for r in rows if r["pub"] != pub]
        test = [r for r in rows if r["pub"] == pub]
        p0 = (sum(r["y"] for r in train) + alpha) / (len(train) + 2 * alpha)
        pb = 0.0
        pl = 0.0
        for r in test:
            sub = [z for z in train if z["x"] == r["x"]]
            p1 = (sum(z["y"] for z in sub) + alpha) / (len(sub) + 2 * alpha)
            pb += (r["y"] - p1) ** 2 - (r["y"] - p0) ** 2
            pl += (-(r["y"] * math.log(p1) +
                     (1 - r["y"]) * math.log(1 - p1)) +
                   (r["y"] * math.log(p0) +
                    (1 - r["y"]) * math.log(1 - p0)))
        total_brier += pb
        total_logloss += pl
        per_pub.append(pb / len(test))
    return {
        "n_pairs": len(rows), "n_publications": len(groups),
        "delta_brier_sign_minus_baseline": total_brier / len(rows),
        "delta_logloss_sign_minus_baseline": total_logloss / len(rows),
        "equal_publication_delta_brier": sum(per_pub) / len(per_pub),
    }


def audit(rows: list[dict], alpha: float) -> dict:
    base = lopo_delta(rows, alpha)
    leave_one = {}
    for pub in sorted({r["pub"] for r in rows}):
        leave_one[pub] = lopo_delta(
            [r for r in rows if r["pub"] != pub], alpha)
    diffs = {k: v["delta_brier_sign_minus_baseline"]
             for k, v in leave_one.items()}
    logdiffs = {k: v["delta_logloss_sign_minus_baseline"]
                for k, v in leave_one.items()}
    return {
        "baseline": base,
        "n_deleted_positive_brier": sum(v > 0 for v in diffs.values()),
        "n_deleted_negative_brier": sum(v < 0 for v in diffs.values()),
        "n_deleted_positive_logloss": sum(v > 0 for v in logdiffs.values()),
        "n_deleted_negative_logloss": sum(v < 0 for v in logdiffs.values()),
        "deleted_brier_min": min(diffs.values()),
        "deleted_brier_max": max(diffs.values()),
        "minimizing_deletion": min(diffs, key=diffs.get),
        "hauber_removed": leave_one[HAUBER] if HAUBER in leave_one else None,
    }


def close(a: float, b: float) -> None:
    assert math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9), (a, b)


def main() -> None:
    full = selected_pairs()
    disjoint = [r for r in full if r["pub"] not in OVERLAP]
    assert len({r["pub"] for r in full}) == 32
    assert len(disjoint) == 31
    assert len({r["pub"] for r in disjoint}) == 23
    assert sum(r["pub"] == HAUBER for r in disjoint) == 1
    out = {}
    for name, rows in (("full", full), ("disjoint", disjoint)):
        out[name] = {}
        for alpha in (0.5, 1.0, 2.0, 4.0):
            out[name][str(alpha)] = audit(rows, alpha)

    full_05 = out["full"]["0.5"]
    dis_05 = out["disjoint"]["0.5"]
    close(full_05["baseline"]["delta_brier_sign_minus_baseline"],
          0.004593137773350995)
    close(dis_05["baseline"]["delta_brier_sign_minus_baseline"],
          0.011510862845879601)
    assert full_05["n_deleted_positive_brier"] == 32
    assert full_05["n_deleted_positive_logloss"] == 32
    assert dis_05["n_deleted_positive_brier"] == 22
    assert dis_05["n_deleted_negative_brier"] == 1
    assert dis_05["n_deleted_positive_logloss"] == 22
    assert dis_05["n_deleted_negative_logloss"] == 1
    assert dis_05["minimizing_deletion"] == HAUBER
    close(dis_05["deleted_brier_min"], -0.0032876556614861367)
    close(dis_05["hauber_removed"]["delta_logloss_sign_minus_baseline"],
          -0.014514436513019957)
    # At stronger smoothing, the disjoint Hauber-deleted reversal disappears.
    for alpha in ("2.0", "4.0"):
        assert out["disjoint"][alpha]["n_deleted_positive_brier"] == 23
        assert out["disjoint"][alpha]["n_deleted_positive_logloss"] == 23
    # Laplace (alpha=1) preserves the small row-weighted reversal,
    # but not the sign of the equal-publication weighted difference.
    dis_1 = out["disjoint"]["1.0"]["hauber_removed"]
    close(dis_1["delta_brier_sign_minus_baseline"],
          -0.00010865489090604609)
    assert dis_1["equal_publication_delta_brier"] > 0

    report = {
        "status": "post_hoc_public_S1_nested_publication_delete_influence",
        "frozen_EGWEE_denominator_added": 0,
        "interpretation": (
            "A worse held-publication conditional-sign score is robust to every "
            "single publication deletion in the full set, but NOT across every "
            "single deletion in the source-disjoint subset at alpha<=1. "
            "This is a selected-literature predictive diagnostic, not a biological "
            "null result, prevalence estimate, or causal mediation test."),
        "results": out,
    }
    print("SF06_PUBLICATION_DELETE_INFLUENCE: PASS")
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
