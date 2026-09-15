from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/recover_ml020_aizen_feinsinger_v2.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    line = next(x for x in proc.stdout.splitlines() if x.startswith("EGWEE_ML020 "))
    result = json.loads(line.split(" ", 1)[1])
    assert result["effect_family"] == "hedges_g_direct"
    assert result["independent_programme_cluster"] is True
    assert result["species_are_dependent_subsystems"] is True
    assert len(result["species_results"]) == 3
    for r in result["species_results"]:
        assert r["n_fragmented_sites"] == 4
        assert r["n_reference_sites"] == 4
        assert r["covariance_determinant"] > 0
        assert r["contrast_variance"] > 0
    assert result["cluster_p_bonferroni"] == 1.0
    print("ML020_PROGRAMME_GATE_OK")


if __name__ == "__main__":
    main()
