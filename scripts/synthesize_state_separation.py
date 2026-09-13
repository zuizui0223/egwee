from __future__ import annotations

import csv
import json
import math
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def two_sided_normal_p(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def fisher_survival_even_df(stat: float, k: int) -> float:
    # Fisher statistic has chi-square df=2k. For even df, survival is exact finite sum.
    x = stat / 2.0
    return math.exp(-x) * sum(x**j / math.factorial(j) for j in range(k))


def cluster_test(cluster: str, effects: dict[str, float], covariance: dict[tuple[str, str], float]) -> dict:
    pair_results = []
    for a, b in combinations(effects, 2):
        va = covariance[(a, a)]
        vb = covariance[(b, b)]
        cab = covariance.get((a, b), covariance[(b, a)])
        contrast_var = va + vb - 2.0 * cab
        if not math.isfinite(contrast_var) or contrast_var <= 0:
            raise AssertionError(f"{cluster} invalid pair variance {a},{b}: {contrast_var}")
        diff = effects[a] - effects[b]
        se = math.sqrt(contrast_var)
        z = diff / se
        p = two_sided_normal_p(z)
        pair_results.append({
            "endpoint_i": a,
            "endpoint_j": b,
            "difference": diff,
            "se": se,
            "z": z,
            "p_two_sided": p,
        })
    m = len(pair_results)
    cluster_p = min(1.0, m * min(r["p_two_sided"] for r in pair_results))
    return {
        "cluster_id": cluster,
        "n_endpoints": len(effects),
        "n_pairs": m,
        "effects": effects,
        "pairwise": pair_results,
        "cluster_p_bonferroni": cluster_p,
    }


def square_cov(path: str) -> dict[tuple[str, str], float]:
    out = {}
    for r in rows(path):
        out[(r["endpoint_i"], r["endpoint_j"])] = float(r["sampling_covariance"])
    return out


def ml001() -> dict:
    erows = [r for r in rows("evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv") if r["primary_or_sensitivity"] == "primary"]
    map_effect_to_cov = {
        "fruit_set": "F_fruit_set",
        "pollen_immigration_rate": "C_pollen_immigration",
        "observed_heterozygosity": "G_adult_Ho",
    }
    effects = {map_effect_to_cov[r["endpoint"]]: float(r["oriented_effect"]) for r in erows}
    return cluster_test("ML001", effects, square_cov("evidence/meta_extraction/PS003_serapias_primary_covariance_v1.csv"))


def ml002() -> dict:
    erows = rows("evidence/meta_extraction/PS004_brosimum_extraction_v1.csv")
    by = {r["endpoint_id"]: r for r in erows}
    effects = {
        "C_paternity_rp": float(by["C_paternity_rp"]["oriented_effect"]),
        "F_TPDW": float(by["F_progeny_vigour"]["oriented_effect"]),
    }
    return cluster_test("ML002", effects, square_cov("evidence/meta_extraction/PS004_brosimum_primary_covariance_v1.csv"))


def ml003() -> dict:
    erows = [r for r in rows("evidence/meta_extraction/PS001_spondias_site_effects_v1.csv") if r["analysis_role"] == "primary"]
    effects = {r["endpoint_id"]: float(r["oriented_effect"]) for r in erows}
    return cluster_test("ML003", effects, square_cov("evidence/meta_extraction/PS001_spondias_primary_pairwise_covariance_v2.csv"))


def z(x: np.ndarray) -> np.ndarray:
    return (x - np.mean(x)) / np.std(x, ddof=1)


def slope(x: np.ndarray, y: np.ndarray) -> float:
    xc = x - np.mean(x)
    yc = y - np.mean(y)
    return float((xc @ yc) / (xc @ xc))


def ml015() -> dict:
    data = rows("evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_population_table_v1.csv")
    size = np.array([float(r["population_size"]) for r in data])
    isolation = np.array([float(r["isolation"]) for r in data])
    shape = np.array([float(r["shape"]) for r in data])
    X = np.column_stack((-np.log10(size), np.sqrt(isolation), np.log10(shape)))
    Xz = np.column_stack([z(X[:, j]) for j in range(3)])
    vals, vecs = np.linalg.eigh(np.cov(Xz, rowvar=False, ddof=1))
    pc1 = vecs[:, int(np.argmax(vals))]
    if float(np.sum(pc1)) < 0:
        pc1 = -pc1
    severity = z(Xz @ pc1)
    idx = [i for i, r in enumerate(data) if r["pollen_tubes"] and r["seeds_per_fruit_y2"] and r["He"]]
    x = severity[idx]
    raw = np.column_stack([
        [float(data[i]["pollen_tubes"]) for i in idx],
        [float(data[i]["seeds_per_fruit_y2"]) for i in idx],
        [float(data[i]["He"]) for i in idx],
    ])
    yz = np.column_stack([z(raw[:, j]) for j in range(3)])
    names = ["I_pollen_tubes", "F_seeds_per_fruit_y2", "G_adult_He"]
    effects = {name: slope(x, yz[:, j]) for j, name in enumerate(names)}
    return cluster_test("ML015", effects, square_cov("evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_primary_covariance_v1.csv"))


def main() -> None:
    clusters = [ml001(), ml002(), ml003(), ml015()]
    pvals = [c["cluster_p_bonferroni"] for c in clusters]
    fisher_stat = -2.0 * sum(math.log(p) for p in pvals)
    combined_p = fisher_survival_even_df(fisher_stat, len(pvals))
    out = {
        "analysis_label": "retrospective_cross_family_state_separation_synthesis",
        "null": "within each cluster all admitted primary layer effects are exchangeable/equal on that cluster's own effect scale",
        "n_independent_clusters": 4,
        "clusters": clusters,
        "fisher_statistic": fisher_stat,
        "fisher_df": 2 * len(pvals),
        "combined_p": combined_p,
        "decision": "reject_general_layer_exchangeability" if combined_p < 0.05 else "do_not_reject_general_layer_exchangeability",
        "claim_ceiling": "does not pool effect magnitudes across effect families and does not imply every cluster is individually discordant",
    }
    print("EGWEE_STATE_SEPARATION " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
