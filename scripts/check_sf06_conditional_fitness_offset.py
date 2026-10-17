from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "evidence/meta_extraction/sf06_translation_residual_result_v1.json"
PAIRS = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
NOTE = ROOT / "manuscript/SF06_CONDITIONAL_FITNESS_OFFSET_2026-10-07.md"


def quantile(values, p):
    x = sorted(values)
    i = (len(x) - 1) * p
    lo = int(i)
    hi = min(lo + 1, len(x) - 1)
    return x[lo] + (x[hi] - x[lo]) * (i - lo)


def main() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    model = result["primary"]["primary_model_dF_on_dI_plus_SC"]
    alpha, beta, gamma = map(float, model["params"])
    pvals = list(map(float, model["p_two_sided"]))

    assert math.isclose(alpha, -0.4134509711326793, rel_tol=1e-12)
    assert math.isclose(beta, 0.19042084675810997, rel_tol=1e-12)
    assert math.isclose(gamma, 0.06390397386984173, rel_tol=1e-12)
    assert pvals[0] < 0.01
    assert pvals[1] < 0.01

    with PAIRS.open(newline="", encoding="utf-8") as fh:
        rows = [
            r for r in csv.DictReader(fh)
            if r["land_use_factor_normalized"] == "habitat fragmentation"
            and r["compatibility"] in {"SC", "SI"}
        ]
    xs = [float(r["d_I"]) for r in rows]
    assert len(xs) == 49
    assert min(xs) == -2.224
    assert max(xs) == 2.034
    assert math.isclose(quantile(xs, 0.5), -0.48, abs_tol=1e-12)

    si_threshold = -alpha / beta
    sc_threshold = -(alpha + gamma) / beta
    assert math.isclose(si_threshold, 2.1712484645018026, rel_tol=1e-12)
    assert math.isclose(sc_threshold, 1.8356550935143368, rel_tol=1e-12)

    note = NOTE.read_text(encoding="utf-8")
    assert "SI: **d_F=-0.413**" in note
    assert "SC: **d_F=-0.350**" in note
    assert "estimand-specific" in note

    print(
        "SF06_CONDITIONAL_FITNESS_OFFSET: PASS "
        f"alpha={alpha:.6f} beta={beta:.6f} "
        f"SI_zero={si_threshold:.3f} SC_zero={sc_threshold:.3f}"
    )


if __name__ == "__main__":
    main()
