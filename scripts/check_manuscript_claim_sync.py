from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
SYNTHESIS = ROOT / "scripts/synthesize_state_separation.py"

DISPLAY_OVERALL = "0.01212432"
DISPLAY_OMIT_ML001 = "0.18194353"
DISPLAY_TOL = 5e-8


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

    # Keep numerical computation and manuscript display contracts separate.
    # The synthesis is checked numerically within the precision represented in
    # the manuscript, while the documents retain the frozen display tokens.
    assert abs(overall - float(DISPLAY_OVERALL)) < DISPLAY_TOL, overall
    assert abs(omit_ml001 - float(DISPLAY_OMIT_ML001)) < DISPLAY_TOL, omit_ml001

    required = [
        DISPLAY_OVERALL,
        DISPLAY_OMIT_ML001,
        "17 marginal effects",
        "ML020",
        "Serapias",
    ]
    for token in required:
        if token not in text:
            raise AssertionError(f"{path}: missing canonical claim token {token!r}")

    if "sixth cluster" not in text and "sixth-cluster" not in text:
        raise AssertionError(f"{path}: significance-repair search stop is not represented")

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
        f"p_display={DISPLAY_OVERALL}"
    )


if __name__ == "__main__":
    main()
