from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SPECIES_P = {
    "Atamisquea emarginata": 0.7982435450716795,
    "Cercidium australe": 0.6183090331468846,
    "Prosopis nigra": 0.5573656730134026,
}


def fisher(pvals: list[float]) -> tuple[float, int, float]:
    stat = -2.0 * sum(math.log(p) for p in pvals)
    k = len(pvals)
    x = stat / 2.0
    p = math.exp(-x) * sum(x**j / math.factorial(j) for j in range(k))
    return stat, 2 * k, p


def main() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/recover_ml020_aizen_feinsinger_v2.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    line = next(x for x in proc.stdout.splitlines() if x.startswith("EGWEE_ML020 "))
    result = json.loads(line.split(" ", 1)[1])
    assert result["cluster_id"] == "ML020"
    assert result["cluster_p_bonferroni"] == 1.0
    got = {r["species"]: r["contrast_p_two_sided"] for r in result["species_results"]}
    for sp, expected in EXPECTED_SPECIES_P.items():
        assert abs(got[sp] - expected) < 1e-12, (sp, got[sp], expected)

    base = [0.00354530, 0.19911670, 0.17406774, 0.09831774]
    stat, df, p = fisher(base + [1.0])
    assert abs(stat - 22.647716471332092) < 1e-12
    assert df == 10
    assert abs(p - 0.012124324105113144) < 1e-12

    stat_omit, df_omit, p_omit = fisher([0.19911670, 0.17406774, 0.09831774, 1.0])
    assert abs(stat_omit - 11.363451478643068) < 1e-12
    assert df_omit == 8
    assert abs(p_omit - 0.18194352880824005) < 1e-12
    print("ML020_EXPECTED_OK")


if __name__ == "__main__":
    main()
