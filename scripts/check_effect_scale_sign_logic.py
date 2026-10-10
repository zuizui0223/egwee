from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evidence/meta_extraction/estimand_scale_sensitivity_v1.csv"
README = ROOT / "README.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
AUDIT = ROOT / "manuscript/ESTIMAND_SIGN_INVARIANCE_AUDIT_2026-10-10.md"


def sign(x: float) -> int:
    return (x > 0) - (x < 0)


def main() -> None:
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 17
    assert {r["cluster_id"] for r in rows} == {"ML001", "ML002", "ML003", "ML014", "ML020"}
    for r in rows:
        mf = float(r["fragmented_mean"])
        mr = float(r["reference_mean"])
        o = int(r["orientation_multiplier"])
        g = float(r["hedges_g"])
        lnrr = float(r["oriented_lnRR"])
        assert mf > 0 and mr > 0 and o in (-1, 1), r
        assert int(r["n_fragmented"]) > 1 and int(r["n_reference"]) > 1, r
        raw_sign = sign(o * (mf - mr))
        assert sign(g) == raw_sign == sign(lnrr), r
        assert math.isclose(lnrr, o * math.log(mf / mr), rel_tol=0, abs_tol=2e-10), r
    assert sum(float(r["hedges_g"]) < 0 for r in rows) == 17
    for p in (README, MANUSCRIPT, AUDIT):
        assert "algebraic" in p.read_text(encoding="utf-8").lower(), p
    print("EFFECT_SCALE_SIGN_IDENTITY_OK: 17/17 oriented group-mean signs; not independent cross-scale replication")


if __name__ == "__main__":
    main()
