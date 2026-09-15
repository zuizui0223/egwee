from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
SYNTHESIS = ROOT / "scripts/synthesize_state_separation.py"


def canonical_result() -> dict:
    proc = subprocess.run(
        [sys.executable, str(SYNTHESIS)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    line = next(
        (x for x in proc.stdout.splitlines() if x.startswith("EGWEE_STATE_SEPARATION ")),
        None,
    )
    if line is None:
        raise AssertionError("canonical synthesis did not emit EGWEE_STATE_SEPARATION")
    return json.loads(line.split(" ", 1)[1])


def require_claim_sync(path: Path, result: dict) -> None:
    text = path.read_text(encoding="utf-8")
    overall = float(result["primary_combined_p"])
    omit_ml001 = next(
        float(row["combined_p"])
        for row in result["primary_leave_one_cluster_out"]
        if row["dropped_cluster"] == "ML001"
    )
    ml020 = next(
        row for row in result["primary_clusters"] if row["cluster_id"] == "ML020"
    )

    required = [
        f"{overall:.8f}",
        f"{omit_ml001:.8f}",
        "17 marginal effects",
        "ML020",
        "Serapias",
        "sixth cluster",
    ]
    for token in required:
        if token not in text:
            raise AssertionError(f"{path}: missing canonical claim token {token!r}")

    if float(ml020["cluster_p_bonferroni"]) != 1.0:
        raise AssertionError("unexpected canonical ML020 programme p")
    if not ("p_ML020=1.0" in text or "p_ML020 = 1.0" in text or "p_programme=1.0" in text):
        raise AssertionError(f"{path}: ML020 non-separation result not represented")

    stale = [
        "Quantitative results are not yet claimed",
        "four independently admitted fragmented-versus-reference Hedges-g clusters",
        "4 independent clusters / 11 effects",
    ]
    for token in stale:
        if token in text:
            raise AssertionError(f"{path}: stale pre-ML020 claim remains: {token!r}")


def main() -> None:
    result = canonical_result()
    assert result["n_primary_independent_clusters"] == 5
    assert result["n_primary_effects"] == 17
    require_claim_sync(README, result)
    require_claim_sync(MANUSCRIPT, result)
    print(
        "MANUSCRIPT_CLAIM_SYNC_OK "
        f"clusters={result['n_primary_independent_clusters']} "
        f"effects={result['n_primary_effects']} "
        f"p={float(result['primary_combined_p']):.8f}"
    )


if __name__ == "__main__":
    main()
