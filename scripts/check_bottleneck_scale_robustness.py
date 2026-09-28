from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import check_estimand_scale_robustness as scale

ROOT = Path(__file__).resolve().parents[1]
UNIFIED = ROOT / "evidence/meta_extraction/ecological_process_function_programme_census_v1.csv"
SEVENELLO = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_transect_values_v1.csv"
KAKAMEGA = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_site_values_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pair_lnrr(records: list[dict[str, str]], group_field: str, frag: str, ref: str, i_field: str, f_field: str) -> dict:
    ef, cov = scale.split_values(
        records, group_field, frag, ref,
        {"I": (i_field, 1), "F": (f_field, 1)},
    )
    tested = scale.cluster_test("panel", ef, cov)
    pair = tested["pairwise"][0]
    return {
        "I": ef["I"][0],
        "F": ef["F"][0],
        "I_minus_F": pair["difference"],
        "p": pair["p_two_sided"],
    }


def sevenello_lnrr() -> dict:
    data = rows(SEVENELLO)
    primary = ["GORO", "LARO", "POAR"]
    panels = {}
    ps = []
    for sp in primary:
        sr = [r for r in data if r["species"] == sp and r["primary_or_sensitivity"] == "primary"]
        result = pair_lnrr(sr, "transect", "Edge", "Core", "I_all_bees", "F_mean_total_seeds_OP")
        panels[sp] = result
        ps.append(result["p"])
    p_programme = min(1.0, len(primary) * min(ps))
    return {"programme_p": p_programme, "panels": panels}


def kakamega_lnrr() -> dict:
    data = [r for r in rows(KAKAMEGA) if r["common_IF_frame"] == "yes"]
    panel_ids = ["AP_2001", "AE_2002", "AE_2003", "HD_2002_03"]
    panels = {}
    ps = []
    for pid in panel_ids:
        sr = [r for r in data if r["panel_id"] == pid]
        result = pair_lnrr(sr, "habitat", "fragment", "main", "I_visit_occurrence", "F_fruit_set")
        panels[pid] = result
        ps.append(result["p"])
    p_programme = min(1.0, len(panel_ids) * min(ps))
    return {"programme_p": p_programme, "panels": panels}


def classify(delta: float, p: float) -> tuple[str, str]:
    if p >= 0.05:
        return "unresolved", "unresolved_process_function_difference"
    if delta > 0:
        return "F_more_negative_than_process", "downstream_function_dominant"
    return "process_more_negative_than_F", "upstream_process_dominant"


def main() -> None:
    canonical = rows(UNIFIED)
    assert len(canonical) == 12
    g_by = {r["programme_id"]: r for r in canonical}

    # Direct primary systems re-expressed on lnRR.
    ml001 = scale.ml001()[0]
    ml002 = scale.ml002()[0]
    ml014 = scale.ml014()[0]
    ml020 = scale.ml020()[0]

    def only_pair(cluster: dict, a: str, b: str) -> tuple[float, float]:
        pair = next(r for r in cluster["pairwise"] if {r["endpoint_i"], r["endpoint_j"]} == {a, b})
        # orient process - F
        delta = pair["difference"]
        if pair["endpoint_i"] == b:
            delta = -delta
        return delta, pair["p_two_sided"]

    direct = {}
    direct["ML001"] = only_pair(ml001, "C_pollen_immigration", "F_fruit_set")
    direct["ML002"] = only_pair(ml002, "C_paternity_rp", "F_TPDW")
    direct["ML014"] = only_pair(ml014, "Gmating_correlated_paternity_rp", "F_family_growth")

    # ML020 is a dependent-species programme. Programme p is Bonferroni across species.
    ml020_pairs = []
    for sp in ml020["species_results"]:
        pair = sp["pairwise"][0]
        ml020_pairs.append((pair["difference"], pair["p_two_sided"]))
    p20 = ml020["cluster_p_bonferroni"]
    # No species-specific pair resolves; programme stays unresolved.
    direct["ML020"] = (sum(d for d, _ in ml020_pairs) / len(ml020_pairs), p20)

    seven = sevenello_lnrr()
    # Programme direction only matters if its internal gate resolves.
    min_sp = min(seven["panels"].values(), key=lambda x: x["p"])
    direct["P2_CF01_SEVENELLO_2026"] = (min_sp["I_minus_F"], seven["programme_p"])

    kaka = kakamega_lnrr()
    min_panel = min(kaka["panels"].values(), key=lambda x: x["p"])
    direct["P2_CF01_BERGSDORF_KAKAMEGA_2006"] = (min_panel["I_minus_F"], kaka["programme_p"])

    lnrr = {}
    for pid, row in g_by.items():
        if pid in direct:
            direction, regime = classify(*direct[pid])
            lnrr[pid] = {
                "resolved_direction": direction,
                "ecological_regime": regime,
                "p": direct[pid][1],
            }
        else:
            # Continuous-gradient Fisher-z programmes are unchanged by this direct-effect scale sensitivity.
            lnrr[pid] = {
                "resolved_direction": row["resolved_direction"],
                "ecological_regime": row["ecological_regime"],
                "p": float(row["programme_adjusted_p"]) if row["programme_adjusted_p"] else None,
            }

    def resolved_ids(mapping: dict, direction: str) -> set[str]:
        return {pid for pid, x in mapping.items() if x["resolved_direction"] == direction}

    g_down = {r["programme_id"] for r in canonical if r["resolved_direction"] == "F_more_negative_than_process"}
    g_up = {r["programme_id"] for r in canonical if r["resolved_direction"] == "process_more_negative_than_F"}
    l_down = resolved_ids(lnrr, "F_more_negative_than_process")
    l_up = resolved_ids(lnrr, "process_more_negative_than_F")

    assert g_down == {"ML015", "P2_CF01_CARDIOPETALUM_2012", "P2_CF01_BERGSDORF_KAKAMEGA_2006"}
    assert g_up == {"ML001"}
    assert l_down == {"ML015", "P2_CF01_CARDIOPETALUM_2012", "P2_CF01_BERGSDORF_KAKAMEGA_2006"}
    assert l_up == {"ML002", "ML014"}

    assert direct["ML001"][1] > 0.5
    assert direct["ML002"][1] < 0.05
    assert direct["ML014"][1] < 0.01
    assert direct["ML020"][1] > 0.05
    assert seven["programme_p"] > 0.05
    assert kaka["programme_p"] < 0.05

    out = {
        "g_plus_gradient": {
            "resolved_downstream": sorted(g_down),
            "resolved_upstream": sorted(g_up),
            "n_resolved": len(g_down | g_up),
        },
        "lnRR_plus_gradient": {
            "resolved_downstream": sorted(l_down),
            "resolved_upstream": sorted(l_up),
            "n_resolved": len(l_down | l_up),
        },
        "direct_lnRR": {
            pid: {"process_minus_F": delta, "programme_or_pair_p": p}
            for pid, (delta, p) in direct.items()
        },
        "sevenello": seven,
        "kakamega": kaka,
        "cross_scale": {
            "downstream_identity_stable": g_down == l_down,
            "upstream_identity_stable": g_up == l_up,
            "both_directions_present_g": bool(g_down and g_up),
            "both_directions_present_lnRR": bool(l_down and l_up),
        },
        "claim": (
            "Both downstream and upstream resolved response geometries occur under both scale representations, "
            "but the identity of upstream-supporting direct programmes changes from ML001 on Hedges g "
            "to ML002 and ML014 on lnRR. Bottleneck attribution to a specific system is therefore scale-sensitive."
        ),
    }
    print("BOTTLENECK_SCALE_AUDIT " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
