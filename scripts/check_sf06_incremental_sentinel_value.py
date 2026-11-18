from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "evidence/meta_extraction/sf06_translation_residual_result_v1.json"
NOTE = ROOT / "manuscript/SF06_INCREMENTAL_SENTINEL_VALUE_2026-10-07.md"


def audit(topology: dict) -> dict:
    counts = topology["component_consensus_sign"]["counts"]
    states = ("lower", "nonlower")
    matrix = {
        i: {f: int(counts.get(i, {}).get(f, 0)) for f in states}
        for i in states
    }
    n = sum(matrix[i][f] for i in states for f in states)
    f_totals = {f: sum(matrix[i][f] for i in states) for f in states}
    baseline_errors = n - max(f_totals.values())
    lookup_errors = sum(
        sum(matrix[i].values()) - max(matrix[i].values())
        for i in states
        if sum(matrix[i].values()) > 0
    )
    return {
        "matrix": matrix,
        "n": n,
        "f_totals": f_totals,
        "baseline_errors": baseline_errors,
        "lookup_errors": lookup_errors,
        "incremental_gain_cases": baseline_errors - lookup_errors,
    }


def main() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    full = audit(result["scale_stable_external_topology"])
    nonoverlap = audit(result["scale_stable_external_topology_nonoverlap_sensitivity"])

    assert full["matrix"] == {
        "lower": {"lower": 35, "nonlower": 9},
        "nonlower": {"lower": 7, "nonlower": 3},
    }
    assert full["n"] == 54
    assert full["baseline_errors"] == 12
    assert full["lookup_errors"] == 12
    assert full["incremental_gain_cases"] == 0

    assert nonoverlap["matrix"] == {
        "lower": {"lower": 20, "nonlower": 6},
        "nonlower": {"lower": 4, "nonlower": 1},
    }
    assert nonoverlap["n"] == 31
    assert nonoverlap["baseline_errors"] == 7
    assert nonoverlap["lookup_errors"] == 7
    assert nonoverlap["incremental_gain_cases"] == 0

    beta = result["primary"]["primary_model_dF_on_dI_plus_SC"]["params"][1]
    beta_p = result["primary"]["primary_model_dF_on_dI_plus_SC"]["p_two_sided"][1]
    assert beta > 0
    assert beta_p < 0.01

    note = NOTE.read_text(encoding="utf-8")
    assert "incremental classification gain from pollination sign = 0 cases" in note
    assert "positive average amplitude association" in note
    assert "incremental diagnostic information" in note

    print(
        "SF06_SENTINEL_INCREMENTAL_VALUE: PASS "
        f"full_gain={full['incremental_gain_cases']} "
        f"nonoverlap_gain={nonoverlap['incremental_gain_cases']} "
        f"beta={beta:.6f} p={beta_p:.6g}"
    )


if __name__ == "__main__":
    main()
