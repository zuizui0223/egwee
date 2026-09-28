from __future__ import annotations

import csv
import json
import math
import statistics as stats
import urllib.request
from itertools import combinations
from pathlib import Path

import synthesize_state_separation as g_synth

ROOT = Path(__file__).resolve().parents[1]

SERA = ROOT / "evidence/meta_extraction/PS003_serapias_site_table_v1.csv"
BROS = ROOT / "evidence/meta_extraction/PS004_brosimum_site_table_v1.csv"
SPON_C = ROOT / "evidence/meta_extraction/PS001_spondias_paternity_site_table_v1.csv"
SPON_G = ROOT / "evidence/meta_extraction/PS001_spondias_appendixB_genetic_site_table_v1.csv"
AIZEN = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_site_means_v1.csv"
SOCIALIS_URL = "https://shared.tern.org.au/attachment/c5278af9-b0c9-4572-8eb4-9ce3058f1b2a/MECBreedfamily.csv"
UA = "Mozilla/5.0 egwee-estimand-scale-audit/1.0"

TOL = 5e-8


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def fetch_csv(url: str) -> list[dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/csv,*/*"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        text = resp.read().decode("utf-8-sig")
    physical = [line for line in text.splitlines() if line.strip()]
    out = list(csv.DictReader(physical))
    if not out:
        raise AssertionError(f"empty CSV from {url}")
    return out


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def sample_cov(x: list[float], y: list[float]) -> float:
    if len(x) != len(y) or len(x) < 2:
        raise AssertionError("paired covariance requires >=2 aligned units")
    mx, my = mean(x), mean(y)
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (len(x) - 1)


def lnrr(x_frag: list[float], x_ref: list[float], orientation: int) -> tuple[float, float]:
    if min(x_frag + x_ref) <= 0:
        raise AssertionError("lnRR requires strictly positive endpoint values")
    m1, m0 = mean(x_frag), mean(x_ref)
    v = stats.variance(x_frag) / (len(x_frag) * m1 * m1)
    v += stats.variance(x_ref) / (len(x_ref) * m0 * m0)
    return orientation * math.log(m1 / m0), v


def lnrr_cov(
    x_frag: list[float],
    y_frag: list[float],
    x_ref: list[float],
    y_ref: list[float],
    orientation_x: int,
    orientation_y: int,
) -> float:
    mx1, my1 = mean(x_frag), mean(y_frag)
    mx0, my0 = mean(x_ref), mean(y_ref)
    cov = sample_cov(x_frag, y_frag) / (len(x_frag) * mx1 * my1)
    cov += sample_cov(x_ref, y_ref) / (len(x_ref) * mx0 * my0)
    return orientation_x * orientation_y * cov


def normal_p(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def cluster_test(
    cluster_id: str,
    effects: dict[str, tuple[float, float]],
    covariances: dict[tuple[str, str], float],
) -> dict:
    pairwise = []
    for a, b in combinations(effects, 2):
        ea, va = effects[a]
        eb, vb = effects[b]
        cov = covariances.get((a, b), covariances.get((b, a), 0.0))
        variance = va + vb - 2.0 * cov
        if variance <= 0 or not math.isfinite(variance):
            raise AssertionError((cluster_id, a, b, variance))
        delta = ea - eb
        se = math.sqrt(variance)
        z = delta / se
        p = normal_p(z)
        pairwise.append({
            "endpoint_i": a,
            "endpoint_j": b,
            "difference": delta,
            "se": se,
            "z": z,
            "p_two_sided": p,
            "covariance": cov,
        })
    m = len(pairwise)
    p_cluster = min(1.0, m * min(r["p_two_sided"] for r in pairwise))
    return {
        "cluster_id": cluster_id,
        "effects": {k: v[0] for k, v in effects.items()},
        "variances": {k: v[1] for k, v in effects.items()},
        "pairwise": pairwise,
        "cluster_p_bonferroni": p_cluster,
    }


def fisher_survival_even_df(stat: float, k: int) -> float:
    x = stat / 2.0
    return math.exp(-x) * sum(x**j / math.factorial(j) for j in range(k))


def fisher(pvals: list[float]) -> tuple[float, int, float]:
    stat = -2.0 * sum(math.log(p) for p in pvals)
    return stat, 2 * len(pvals), fisher_survival_even_df(stat, len(pvals))


def split_values(
    records: list[dict[str, str]],
    group_field: str,
    frag_label: str,
    ref_label: str,
    endpoint_fields: dict[str, tuple[str, int]],
) -> tuple[dict[str, tuple[float, float]], dict[tuple[str, str], float]]:
    frag = [r for r in records if r[group_field] == frag_label]
    ref = [r for r in records if r[group_field] == ref_label]
    if len(frag) < 2 or len(ref) < 2:
        raise AssertionError((len(frag), len(ref)))
    effects: dict[str, tuple[float, float]] = {}
    vectors: dict[str, tuple[list[float], list[float], int]] = {}
    for endpoint, (field, orientation) in endpoint_fields.items():
        xf = [float(r[field]) for r in frag]
        xr = [float(r[field]) for r in ref]
        effects[endpoint] = lnrr(xf, xr, orientation)
        vectors[endpoint] = (xf, xr, orientation)
    cov: dict[tuple[str, str], float] = {}
    for a, b in combinations(endpoint_fields, 2):
        af, ar, ao = vectors[a]
        bf, br, bo = vectors[b]
        cov[(a, b)] = lnrr_cov(af, bf, ar, br, ao, bo)
        cov[(b, a)] = cov[(a, b)]
    return effects, cov


def ml001() -> tuple[dict, dict]:
    effects, cov = split_values(
        rows(SERA), "exposure_group", "anthropic", "natural",
        {
            "F_fruit_set": ("fruit_set_pct", 1),
            "C_pollen_immigration": ("pollen_immigration_pct", 1),
            "G_adult_Ho": ("observed_heterozygosity", 1),
        },
    )
    return cluster_test("ML001", effects, cov), cluster_test("ML001", effects, {})


def ml002() -> tuple[dict, dict]:
    effects, cov = split_values(
        rows(BROS), "habitat", "FRA", "CON",
        {
            "C_paternity_rp": ("C_paternity_rp", -1),
            "F_TPDW": ("F_TPDW_site_mean", 1),
        },
    )
    return cluster_test("ML002", effects, cov), cluster_test("ML002", effects, {})


def ml003() -> tuple[dict, dict]:
    c_rows = rows(SPON_C)
    g_rows = rows(SPON_G)
    by_gen = {(r["population"], r["developmental_stage"]): r for r in g_rows}
    pops = [r["population"] for r in c_rows]
    records = []
    for r in c_rows:
        p = r["population"]
        records.append({
            "population": p,
            "habitat": r["habitat"],
            "C": r["multilocus_correlated_paternity_rp"],
            "Ga": by_gen[(p, "adult")]["Ho"],
            "Gj": by_gen[(p, "juvenile")]["Ho"],
            "Gs": by_gen[(p, "seed")]["Ho"],
        })
    if set(pops) != {r["population"] for r in records}:
        raise AssertionError("Spondias population alignment failed")
    effects, cov = split_values(
        records, "habitat", "FRA", "CON",
        {
            "C_paternity_correlation": ("C", -1),
            "Gadult_Ho": ("Ga", 1),
            "Gjuvenile_Ho": ("Gj", 1),
            "Gseed_Ho": ("Gs", 1),
        },
    )
    return cluster_test("ML003", effects, cov), cluster_test("ML003", effects, {})


def socialis_records() -> list[dict[str, str]]:
    raw = fetch_csv(SOCIALIS_URL)
    out = []
    for r in raw:
        group = r["group"].strip().upper()
        if group not in {"MONLOW", "MONHIGH"}:
            continue
        try:
            rp = float(r["rp"])
            growth = float(r["plant height (cm)"])
        except (TypeError, ValueError):
            continue
        if not (math.isfinite(rp) and math.isfinite(growth)):
            continue
        out.append({
            "family": r["family"].strip(),
            "habitat": "FRA" if group == "MONLOW" else "CON",
            "rp": str(rp),
            "growth": str(growth),
        })
    if len(out) != 28:
        raise AssertionError(f"expected 28 common Monarto families, got {len(out)}")
    if sum(r["habitat"] == "FRA" for r in out) != 13:
        raise AssertionError("unexpected MONLOW count")
    if sum(r["habitat"] == "CON" for r in out) != 15:
        raise AssertionError("unexpected MONHIGH count")
    return out


def ml014() -> tuple[dict, dict]:
    effects, cov = split_values(
        socialis_records(), "habitat", "FRA", "CON",
        {
            "Gmating_correlated_paternity_rp": ("rp", -1),
            "F_family_growth": ("growth", 1),
        },
    )
    return cluster_test("ML014", effects, cov), cluster_test("ML014", effects, {})


def ml020() -> tuple[dict, dict]:
    data = rows(AIZEN)
    species = sorted({r["species"] for r in data})
    cov_species = []
    zero_species = []
    all_effects = []
    for sp in species:
        sr = [r for r in data if r["species"] == sp]
        effects, cov = split_values(
            sr, "condition", "small", "continuous",
            {
                "I_pollen_tubes": ("I_pollen_tubes", 1),
                "F_fruit_set": ("F_fruit_set", 1),
            },
        )
        cov_test = cluster_test(f"ML020:{sp}", effects, cov)
        zero_test = cluster_test(f"ML020:{sp}", effects, {})
        cov_species.append(cov_test)
        zero_species.append(zero_test)
        all_effects.extend(effects.values())
    p_cov = min(1.0, len(cov_species) * min(x["cluster_p_bonferroni"] for x in cov_species))
    p_zero = min(1.0, len(zero_species) * min(x["cluster_p_bonferroni"] for x in zero_species))
    return (
        {"cluster_id": "ML020", "species_results": cov_species, "cluster_p_bonferroni": p_cov},
        {"cluster_id": "ML020", "species_results": zero_species, "cluster_p_bonferroni": p_zero},
    )


def flatten_effects(cluster: dict) -> list[float]:
    if cluster["cluster_id"] == "ML020":
        return [
            effect
            for sp in cluster["species_results"]
            for effect in sp["effects"].values()
        ]
    return list(cluster["effects"].values())


def endpoint_rank(effects: dict[str, float]) -> list[str]:
    return [k for k, _ in sorted(effects.items(), key=lambda kv: abs(kv[1]), reverse=True)]


def main() -> None:
    for path in (SERA, BROS, SPON_C, SPON_G, AIZEN):
        assert path.is_file(), path

    lnrr_cov_clusters = [ml001()[0], ml002()[0], ml003()[0], ml014()[0], ml020()[0]]
    lnrr_zero_clusters = [ml001()[1], ml002()[1], ml003()[1], ml014()[1], ml020()[1]]

    # Canonical g-scale results from the existing frozen synthesis.
    g_clusters = [g_synth.ml001(), g_synth.ml002(), g_synth.ml003(), g_synth.ml014(), g_synth.ml020()]
    g_p = [x["cluster_p_bonferroni"] for x in g_clusters]
    _, _, g_full = fisher(g_p)
    _, _, g_drop_ml001 = fisher([x["cluster_p_bonferroni"] for x in g_clusters if x["cluster_id"] != "ML001"])

    cov_p = [x["cluster_p_bonferroni"] for x in lnrr_cov_clusters]
    zero_p = [x["cluster_p_bonferroni"] for x in lnrr_zero_clusters]
    _, _, lnrr_cov_full = fisher(cov_p)
    _, _, lnrr_cov_drop_ml001 = fisher([x["cluster_p_bonferroni"] for x in lnrr_cov_clusters if x["cluster_id"] != "ML001"])
    _, _, lnrr_zero_full = fisher(zero_p)
    _, _, lnrr_zero_drop_ml001 = fisher([x["cluster_p_bonferroni"] for x in lnrr_zero_clusters if x["cluster_id"] != "ML001"])

    assert abs(g_full - 0.01212432) < 5e-8
    assert abs(g_drop_ml001 - 0.18194353) < 5e-8

    # Scale-invariant sign information: every primary direct effect is detrimental.
    g_effects = [e for cl in g_clusters for e in flatten_effects(cl)]
    lnrr_effects = [e for cl in lnrr_cov_clusters for e in flatten_effects(cl)]
    assert len(g_effects) == len(lnrr_effects) == 17
    assert all(e < 0 for e in g_effects)
    assert all(e < 0 for e in lnrr_effects)

    g_ml001 = next(x for x in g_clusters if x["cluster_id"] == "ML001")
    l_ml001 = next(x for x in lnrr_cov_clusters if x["cluster_id"] == "ML001")
    g_cf = next(
        r for r in g_ml001["pairwise"]
        if {r["endpoint_i"], r["endpoint_j"]} == {"C_pollen_immigration", "F_fruit_set"}
    )
    l_cf = next(
        r for r in l_ml001["pairwise"]
        if {r["endpoint_i"], r["endpoint_j"]} == {"C_pollen_immigration", "F_fruit_set"}
    )

    g_rank = endpoint_rank(g_ml001["effects"])
    l_rank = endpoint_rank(l_ml001["effects"])
    assert g_rank == ["G_adult_Ho", "C_pollen_immigration", "F_fruit_set"]
    assert l_rank == ["C_pollen_immigration", "F_fruit_set", "G_adult_Ho"]
    assert g_cf["p_two_sided"] < 0.05
    assert l_cf["p_two_sided"] > 0.5

    # The manuscript headline is scale-sensitive if the ML001 LOO decision changes.
    assert g_drop_ml001 >= 0.05
    assert lnrr_zero_drop_ml001 < 0.05
    assert lnrr_cov_drop_ml001 < 0.05

    result = {
        "audit": "estimand_scale_robustness",
        "g_scale": {
            "full_fisher_p": g_full,
            "omit_ML001_fisher_p": g_drop_ml001,
            "cluster_p": {x["cluster_id"]: x["cluster_p_bonferroni"] for x in g_clusters},
        },
        "lnRR_delta_raw_covariance": {
            "full_fisher_p": lnrr_cov_full,
            "omit_ML001_fisher_p": lnrr_cov_drop_ml001,
            "cluster_p": {x["cluster_id"]: x["cluster_p_bonferroni"] for x in lnrr_cov_clusters},
        },
        "lnRR_zero_covariance": {
            "full_fisher_p": lnrr_zero_full,
            "omit_ML001_fisher_p": lnrr_zero_drop_ml001,
            "cluster_p": {x["cluster_id"]: x["cluster_p_bonferroni"] for x in lnrr_zero_clusters},
        },
        "sign_audit": {
            "n_primary_effects": 17,
            "g_negative": sum(e < 0 for e in g_effects),
            "lnRR_negative": sum(e < 0 for e in lnrr_effects),
            "discordant_signs": sum((a < 0) != (b < 0) for a, b in zip(g_effects, lnrr_effects)),
        },
        "ML001_scale_reversal": {
            "g_abs_rank": g_rank,
            "lnRR_abs_rank": l_rank,
            "g_C_minus_F_p": g_cf["p_two_sided"],
            "lnRR_C_minus_F_p": l_cf["p_two_sided"],
            "g_effects": g_ml001["effects"],
            "lnRR_effects": l_ml001["effects"],
        },
        "claim": (
            "The primary direct state-separation headline is estimand-scale dependent: "
            "g-scale ML001 omission does not reject, whereas lnRR sensitivity rejects "
            "with and without reconstructed raw-unit covariance. Sign-only evidence is "
            "uniformly detrimental (17/17) and contains no direction-discordant primary effect."
        ),
    }
    print("ESTIMAND_SCALE_AUDIT " + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
