from __future__ import annotations

import csv
import json
from pathlib import Path

import check_estimand_scale_robustness as scale
import check_bottleneck_scale_robustness as bott

ROOT = Path(__file__).resolve().parents[1]
SEVEN_G = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_direct_covariance_v1.json"
KAKA_G = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_covariance_v1.json"
OUT = ROOT / "evidence/meta_extraction/process_function_difference_sign_stability_v1.csv"


def sign_label(x: float) -> str:
    if x > 0:
        return "F_more_negative_or_less_positive_than_process"
    if x < 0:
        return "process_more_negative_or_less_positive_than_F"
    return "equal_point_estimate"


def pair_from_cluster(cluster: dict, process: str, func: str) -> tuple[float, float]:
    pair = next(r for r in cluster["pairwise"] if {r["endpoint_i"], r["endpoint_j"]} == {process, func})
    delta = pair["difference"]
    if pair["endpoint_i"] == func:
        delta = -delta
    return delta, pair["p_two_sided"]


def main() -> None:
    records: list[dict[str, object]] = []

    # Single-pair direct programmes.
    for pid, cluster, process, func in (
        ("ML001", scale.ml001()[0], "C_pollen_immigration", "F_fruit_set"),
        ("ML002", scale.ml002()[0], "C_paternity_rp", "F_TPDW"),
        ("ML014", scale.ml014()[0], "Gmating_correlated_paternity_rp", "F_family_growth"),
    ):
        ln_delta, ln_p = pair_from_cluster(cluster, process, func)
        g_cluster = {"ML001": scale.g_synth.ml001(), "ML002": scale.g_synth.ml002(), "ML014": scale.g_synth.ml014()}[pid]
        g_delta, g_p = pair_from_cluster(g_cluster, process, func)
        records.append({
            "programme_id": pid,
            "panel_id": pid,
            "g_process_minus_F": g_delta,
            "g_pair_p": g_p,
            "lnRR_process_minus_F": ln_delta,
            "lnRR_pair_p": ln_p,
        })

    # ML020 dependent species panels.
    g20 = {x["cluster_id"].split(":", 1)[1]: x for x in scale.g_synth.ml020()["species_results"]}
    l20 = {x["cluster_id"].split(":", 1)[1]: x for x in scale.ml020()[0]["species_results"]}
    assert set(g20) == set(l20) == {"Atamisquea emarginata", "Cercidium australe", "Prosopis nigra"}
    for sp in sorted(g20):
        g_delta, g_p = pair_from_cluster(g20[sp], "I_pollen_tubes", "F_fruit_set")
        ln_delta, ln_p = pair_from_cluster(l20[sp], "I_pollen_tubes", "F_fruit_set")
        records.append({
            "programme_id": "ML020",
            "panel_id": sp,
            "g_process_minus_F": g_delta,
            "g_pair_p": g_p,
            "lnRR_process_minus_F": ln_delta,
            "lnRR_pair_p": ln_p,
        })

    # Sevenello primary species.
    seven_g = json.loads(SEVEN_G.read_text(encoding="utf-8"))
    seven_l = bott.sevenello_lnrr()["panels"]
    for sp in ("GORO", "LARO", "POAR"):
        g = seven_g["panels"][sp]["I_minus_F"]
        ln = seven_l[sp]
        records.append({
            "programme_id": "P2_CF01_SEVENELLO_2026",
            "panel_id": sp,
            "g_process_minus_F": float(g["delta"]),
            "g_pair_p": float(g["p_two_sided"]),
            "lnRR_process_minus_F": float(ln["I_minus_F"]),
            "lnRR_pair_p": float(ln["p"]),
        })

    # Kakamega recovered panels.
    kaka_g = json.loads(KAKA_G.read_text(encoding="utf-8"))
    kaka_l = bott.kakamega_lnrr()["panels"]
    for pid in ("AP_2001", "AE_2002", "AE_2003", "HD_2002_03"):
        g = kaka_g["panel_blocks"][pid]["I_minus_F"]
        ln = kaka_l[pid]
        records.append({
            "programme_id": "P2_CF01_BERGSDORF_KAKAMEGA_2006",
            "panel_id": pid,
            "g_process_minus_F": float(g["delta"]),
            "g_pair_p": float(g["p_two_sided"]),
            "lnRR_process_minus_F": float(ln["I_minus_F"]),
            "lnRR_pair_p": float(ln["p"]),
        })

    assert len(records) == 13

    for r in records:
        r["g_direction"] = sign_label(float(r["g_process_minus_F"]))
        r["lnRR_direction"] = sign_label(float(r["lnRR_process_minus_F"]))
        r["direction_agrees"] = r["g_direction"] == r["lnRR_direction"]
        r["resolved_on_g"] = float(r["g_pair_p"]) < 0.05
        r["resolved_on_lnRR"] = float(r["lnRR_pair_p"]) < 0.05
        r["resolved_on_either"] = bool(r["resolved_on_g"] or r["resolved_on_lnRR"])

    stable = [r for r in records if r["direction_agrees"]]
    unstable = [r for r in records if not r["direction_agrees"]]
    resolved = [r for r in records if r["resolved_on_either"]]
    resolved_stable = [r for r in resolved if r["direction_agrees"]]

    assert len(stable) == 11
    assert len(unstable) == 2
    assert {(r["programme_id"], r["panel_id"]) for r in unstable} == {
        ("P2_CF01_BERGSDORF_KAKAMEGA_2006", "AE_2002"),
        ("P2_CF01_BERGSDORF_KAKAMEGA_2006", "HD_2002_03"),
    }
    assert len(resolved) == 4
    assert len(resolved_stable) == 4
    assert {(r["programme_id"], r["panel_id"]) for r in resolved} == {
        ("ML001", "ML001"),
        ("ML002", "ML002"),
        ("ML014", "ML014"),
        ("P2_CF01_BERGSDORF_KAKAMEGA_2006", "AP_2001"),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "programme_id", "panel_id",
        "g_process_minus_F", "g_pair_p", "g_direction",
        "lnRR_process_minus_F", "lnRR_pair_p", "lnRR_direction",
        "direction_agrees", "resolved_on_g", "resolved_on_lnRR", "resolved_on_either",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

    print(
        "PROCESS_FUNCTION_DIRECTION_STABILITY_OK "
        "panels=13 stable_direction=11 unstable_direction=2 "
        "resolved_on_either=4 resolved_direction_stable=4 "
        "unstable_panels=Kakamega_AE2002,Kakamega_HD2002_03"
    )


if __name__ == "__main__":
    main()
