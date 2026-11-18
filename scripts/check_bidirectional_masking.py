from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "evidence/meta_extraction/estimand_scale_sensitivity_v1.csv"
BOTTLENECK_SCALE = ROOT / "evidence/meta_extraction/bottleneck_scale_robustness_v1.csv"
ACER = ROOT / "evidence/meta_extraction/phase2_cf01_acer_miyabei_gradient_effects_v1.csv"
CARDIO = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_effects_v1.csv"
WANDOO = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv"
KAKA = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_effects_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    scale_rows = rows(SCALE)
    by = {(r["cluster_id"], r["endpoint_id"]): r for r in scale_rows}

    # Motif A: movement/mating disruption can be larger than downstream function loss.
    # For the three direct systems this ordering must survive both g and lnRR.
    upstream_direct = {
        "ML001": ("C", "F"),
        "ML002": ("C", "F"),
        "ML014": ("Gmating", "F"),
    }
    upstream_checks = {}
    for cid, (proc, func) in upstream_direct.items():
        p = by[(cid, proc)]
        f = by[(cid, func)]
        g_proc = abs(float(p["hedges_g"]))
        g_func = abs(float(f["hedges_g"]))
        l_proc = abs(float(p["oriented_lnRR"]))
        l_func = abs(float(f["oriented_lnRR"]))
        assert g_proc > g_func, (cid, g_proc, g_func)
        assert l_proc > l_func, (cid, l_proc, l_func)
        upstream_checks[cid] = {
            "g_ratio_F_over_process": g_func / g_proc,
            "lnRR_ratio_F_over_process": l_func / l_proc,
        }

    acer = {r["endpoint_role"]: float(r["fisher_z"]) for r in rows(ACER) if r["primary_or_sensitivity"] == "primary"}
    assert abs(acer["C_primary"]) > abs(acer["F_primary"])
    upstream_checks["P2_CF01_ACER_MIYABEI_2014"] = {
        "native_ratio_F_over_process": abs(acer["F_primary"]) / abs(acer["C_primary"])
    }
    assert len(upstream_checks) == 4

    # Motif B: all resolved I-F mismatches are function-dominant.
    w = {r["layer"]: float(r["oriented_effect"]) for r in rows(WANDOO)}
    assert w["F"] < w["I"]

    c = {r["endpoint_role"]: float(r["fisher_z"]) for r in rows(CARDIO) if r["primary_or_sensitivity"] == "primary"}
    assert c["F_primary"] < c["I_primary"]

    k = [r for r in rows(KAKA) if r["panel_id"] == "AP_2001" and r["primary_or_sensitivity"] == "primary"]
    kv = {r["layer"]: float(r["hedges_g"]) for r in k}
    assert kv["F_reproductive_function"] < kv["I_interaction"]

    bscale = {r["programme_id"]: r for r in rows(BOTTLENECK_SCALE)}
    assert bscale["P2_CF01_BERGSDORF_KAKAMEGA_2006"]["cross_scale_status"] == "stable_downstream"
    assert bscale["ML015"]["cross_scale_status"] == "native_gradient_downstream"
    assert bscale["P2_CF01_CARDIOPETALUM_2012"]["cross_scale_status"] == "native_gradient_downstream"

    # These are descriptive motifs, not independent Bernoulli trials.
    print(
        "BIDIRECTIONAL_MASKING_AUDIT_OK "
        "upstream_process_gt_function=4of4 "
        "direct_upstream_order_scale_stable=3of3 "
        "resolved_IF_function_dominant=3of3 "
        "resolved_sign_discordant_hidden_function_loss=2programmes "
        f"ML001_F_over_C_lnRR={upstream_checks['ML001']['lnRR_ratio_F_over_process']:.3f} "
        f"ML002_F_over_C_lnRR={upstream_checks['ML002']['lnRR_ratio_F_over_process']:.3f} "
        f"ML014_F_over_mating_lnRR={upstream_checks['ML014']['lnRR_ratio_F_over_process']:.3f}"
    )


if __name__ == "__main__":
    main()
