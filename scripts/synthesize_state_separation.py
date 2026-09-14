from __future__ import annotations

import csv
import json
import math
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(path: str) -> list[dict[str, str]]:
    with (ROOT / path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def two_sided_normal_p(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def fisher_survival_even_df(stat: float, k: int) -> float:
    x = stat / 2.0
    return math.exp(-x) * sum(x**j / math.factorial(j) for j in range(k))


def fisher_combine(pvals: list[float]) -> tuple[float, int, float]:
    stat = -2.0 * sum(math.log(p) for p in pvals)
    return stat, 2 * len(pvals), fisher_survival_even_df(stat, len(pvals))


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
    return {
        (r["endpoint_i"], r["endpoint_j"]): float(r["sampling_covariance"])
        for r in rows(path)
    }


def ml001() -> dict:
    erows = [
        r for r in rows("evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv")
        if r["primary_or_sensitivity"] == "primary"
    ]
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
    erows = [
        r for r in rows("evidence/meta_extraction/PS001_spondias_site_effects_v1.csv")
        if r["analysis_role"] == "primary"
    ]
    effects = {r["endpoint_id"]: float(r["oriented_effect"]) for r in erows}
    return cluster_test("ML003", effects, square_cov("evidence/meta_extraction/PS001_spondias_primary_pairwise_covariance_v2.csv"))


def ml014() -> dict:
    erows = rows("evidence/meta_extraction/PS020_eucalyptus_socialis_effects_v1.csv")
    effects = {r["endpoint_id"]: float(r["oriented_effect"]) for r in erows}
    assert set(effects) == {"Gmating_correlated_paternity_rp", "F_family_growth"}
    return cluster_test("ML014", effects, square_cov("evidence/meta_extraction/PS020_eucalyptus_socialis_primary_covariance_v1.csv"))


def ml015_gradient_generalisation() -> dict:
    erows = rows("evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv")
    effect_name = {
        "pollen_tubes_at_base_of_style": "I_pollen_tubes",
        "seeds_per_fruit_y2": "F_seeds_per_fruit_y2",
        "unbiased_expected_heterozygosity_He": "G_adult_He",
    }
    effects = {effect_name[r["endpoint"]]: float(r["oriented_effect"]) for r in erows}
    return cluster_test(
        "ML015_gradient_generalisation",
        effects,
        square_cov("evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_covariance_v1.csv"),
    )


def main() -> None:
    registry = {r["cluster_id"]: r for r in rows("evidence/meta_extraction/multilayer_cluster_registry_v1.csv")}
    primary_ids = {
        cid for cid, r in registry.items()
        if r["cluster_status"] == "admissible_multilayer_cluster"
    }
    assert primary_ids == {"ML001", "ML002", "ML003", "ML014"}
    assert sum(int(registry[cid]["n_admissible_primary_effects"]) for cid in primary_ids) == 11
    assert registry["ML015"]["cluster_status"] == "gradient_generalisation_multilayer_cluster"
    assert registry["ML015"]["admissible_primary_layers"] == ""
    assert int(registry["ML015"]["n_admissible_primary_effects"]) == 0

    primary_clusters = [ml001(), ml002(), ml003(), ml014()]
    pvals = [c["cluster_p_bonferroni"] for c in primary_clusters]
    fisher_stat, fisher_df, combined_p = fisher_combine(pvals)

    loo = []
    for dropped in primary_clusters:
        retained = [c for c in primary_clusters if c["cluster_id"] != dropped["cluster_id"]]
        stat, df, p = fisher_combine([c["cluster_p_bonferroni"] for c in retained])
        loo.append({
            "dropped_cluster": dropped["cluster_id"],
            "retained_clusters": [c["cluster_id"] for c in retained],
            "fisher_statistic": stat,
            "fisher_df": df,
            "combined_p": p,
            "reject_at_0_05": p < 0.05,
        })
    influential = [r["dropped_cluster"] for r in loo if not r["reject_at_0_05"]]

    gradient = ml015_gradient_generalisation()

    out = {
        "analysis_label": "retrospective_primary_binary_state_separation_with_separate_gradient_generalisation",
        "primary_null": "within each primary binary/contrast cluster all admitted layer effects are exchangeable/equal on that cluster's own Hedges-g scale",
        "n_primary_independent_clusters": len(primary_clusters),
        "n_primary_effects": 11,
        "primary_clusters": primary_clusters,
        "primary_fisher_statistic": fisher_stat,
        "primary_fisher_df": fisher_df,
        "primary_combined_p": combined_p,
        "primary_decision": (
            "reject_primary_binary_layer_exchangeability"
            if combined_p < 0.05 else "do_not_reject_primary_binary_layer_exchangeability"
        ),
        "primary_leave_one_cluster_out": loo,
        "primary_influential_cluster_dependency": {
            "detected": bool(influential),
            "clusters": influential,
            "interpretation": (
                "full primary rejection is not leave-one-cluster-out robust"
                if influential else "full primary rejection is leave-one-cluster-out robust"
            ),
        },
        "gradient_generalisation": gradient,
        "gradient_combined_with_primary": False,
        "claim_ceiling": (
            "primary inference uses ML001-ML003 plus prospectively recovered ML014; ML015 is separate Fisher-z gradient generalisation evidence; "
            "no Hedges-g/Fisher-z cross-family Fisher combination is permitted; primary corpus-level rejection "
            "must be reported with its leave-one-cluster-out dependency"
        ),
    }
    print("EGWEE_STATE_SEPARATION " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
