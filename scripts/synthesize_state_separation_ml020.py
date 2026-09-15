from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def fisher_survival_even_df(stat: float, k: int) -> float:
    x = stat / 2.0
    return math.exp(-x) * sum(x**j / math.factorial(j) for j in range(k))


def fisher_combine(pvals: list[float]) -> tuple[float, int, float]:
    stat = -2.0 * sum(math.log(p) for p in pvals)
    return stat, 2 * len(pvals), fisher_survival_even_df(stat, len(pvals))


def ml020() -> dict:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/recover_ml020_aizen_feinsinger_v2.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    line = next(x for x in proc.stdout.splitlines() if x.startswith("EGWEE_ML020 "))
    out = json.loads(line.split(" ", 1)[1])
    assert out["cluster_id"] == "ML020"
    return out


def canonical_existing_p() -> dict[str, float]:
    # Frozen canonical four-cluster p-values from the pre-ML020 synthesis.
    return {
        "ML001": 0.00354530,
        "ML002": 0.19911670,
        "ML003": 0.17406774,
        "ML014": 0.09831774,
    }


def main() -> None:
    new = ml020()
    pvals = canonical_existing_p() | {"ML020": float(new["cluster_p_bonferroni"])}
    assert pvals["ML020"] == 1.0

    stat, df, p = fisher_combine(list(pvals.values()))
    loo = []
    for dropped in pvals:
        retained = {k: v for k, v in pvals.items() if k != dropped}
        s, d, q = fisher_combine(list(retained.values()))
        loo.append({
            "dropped_cluster": dropped,
            "retained_clusters": list(retained),
            "fisher_statistic": s,
            "fisher_df": d,
            "combined_p": q,
            "reject_at_0_05": q < 0.05,
        })

    influential = [r["dropped_cluster"] for r in loo if not r["reject_at_0_05"]]
    out = {
        "analysis_label": "five_primary_binary_clusters_after_ML020",
        "n_primary_independent_clusters": 5,
        "cluster_p_values": pvals,
        "primary_fisher_statistic": stat,
        "primary_fisher_df": df,
        "primary_combined_p": p,
        "primary_decision": "reject_primary_binary_layer_exchangeability" if p < 0.05 else "do_not_reject_primary_binary_layer_exchangeability",
        "primary_leave_one_cluster_out": loo,
        "primary_influential_cluster_dependency": {
            "detected": bool(influential),
            "clusters": influential,
            "interpretation": "full primary rejection is not leave-one-cluster-out robust" if influential else "full primary rejection is leave-one-cluster-out robust",
        },
        "key_omit_ML001_result": next(r for r in loo if r["dropped_cluster"] == "ML001"),
        "claim_ceiling": "ML020 is a retrospective independent replicated programme; full rejection remains materially dependent on ML001 Serapias",
    }
    print("EGWEE_STATE_SEPARATION_ML020 " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
