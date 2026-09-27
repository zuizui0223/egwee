from __future__ import annotations

import csv
import math
from itertools import combinations
from pathlib import Path

import synthesize_state_separation as state

ROOT = Path(__file__).resolve().parents[1]
SCALE = ROOT / "evidence/meta_extraction/estimand_scale_sensitivity_v1.csv"
SUMMARY = ROOT / "evidence/meta_extraction/estimand_scale_cluster_summary_v1.csv"
ML020_SITE = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_site_means_v1.csv"

TOL = 5e-9


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def p_two(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def fisher(pvals: list[float]) -> tuple[float, int, float]:
    stat = -2.0 * sum(math.log(p) for p in pvals)
    k = len(pvals)
    x = stat / 2.0
    p = math.exp(-x) * sum(x**j / math.factorial(j) for j in range(k))
    return stat, 2 * k, p


def lnrr_var(mf: float, sdf: float, nf: int, mr: float, sdr: float, nr: int) -> float:
    assert mf > 0 and mr > 0
    return sdf**2 / (nf * mf**2) + sdr**2 / (nr * mr**2)


def rho_map(path: str, rho_field: str = "correlation_proxy") -> dict[tuple[str, str], float]:
    out = {}
    for r in rows(ROOT / path):
        a, b = r["endpoint_i"], r["endpoint_j"]
        if a != b:
            out[(a, b)] = float(r[rho_field])
    return out


def pair_p(ea: float, va: float, eb: float, vb: float, mode: str, rho: float = 0.0) -> float:
    if mode == "rho_proxy":
        cov = rho * math.sqrt(va * vb)
    elif mode == "zero_cov":
        cov = 0.0
    elif mode == "cauchy_maxvar":
        cov = -math.sqrt(va * vb)
    else:
        raise AssertionError(mode)
    vd = va + vb - 2.0 * cov
    assert vd > 0
    return p_two((ea - eb) / math.sqrt(vd))


def cluster_p(
    effects: dict[str, float],
    variances: dict[str, float],
    rhos: dict[tuple[str, str], float],
    mode: str,
) -> tuple[float, list[dict]]:
    tested = []
    for a, b in combinations(effects, 2):
        rho = rhos.get((a, b), rhos.get((b, a), 0.0))
        p = pair_p(effects[a], variances[a], effects[b], variances[b], mode, rho)
        tested.append({"a": a, "b": b, "p": p})
    return min(1.0, len(tested) * min(x["p"] for x in tested)), tested


def endpoint_table() -> dict[tuple[str, str], dict[str, float]]:
    out = {}
    for r in rows(SCALE):
        key = (r["cluster_id"], r["endpoint_id"])
        out[key] = {
            "g": float(r["hedges_g"]),
            "lnrr": float(r["oriented_lnRR"]),
            "v": float(r["lnRR_delta_variance"]),
        }
    assert len(out) == 17
    return out


def derive_ml020_rho() -> dict[str, float]:
    rhos = {}
    for r in rows(ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_covariance_v1.csv"):
        if r["endpoint_i"] == "I_pollen_tubes" and r["endpoint_j"] == "F_fruit_set":
            short = r["species"].split()[0]
            rhos[short] = float(r["rho_group_centered"])
    return rhos


def validate_ml020_endpoint_reconstruction(tab: dict[tuple[str, str], dict[str, float]]) -> None:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for r in rows(ML020_SITE):
        grouped.setdefault((r["species"].split()[0], r["condition"]), []).append(r)
    for sp in ("Atamisquea", "Cercidium", "Prosopis"):
        for endpoint, col in (("I", "I_pollen_tubes"), ("F", "F_fruit_set")):
            frag = [float(r[col]) for r in grouped[(sp, "small")]]
            ref = [float(r[col]) for r in grouped[(sp, "continuous")]]
            mf, mr = sum(frag) / 4.0, sum(ref) / 4.0
            sdf = math.sqrt(sum((x - mf) ** 2 for x in frag) / 3.0)
            sdr = math.sqrt(sum((x - mr) ** 2 for x in ref) / 3.0)
            eff = math.log(mf / mr)
            var = lnrr_var(mf, sdf, 4, mr, sdr, 4)
            got = tab[("ML020", f"{sp}:{endpoint}")]
            assert abs(got["lnrr"] - eff) < TOL
            assert abs(got["v"] - var) < TOL


def lnrr_clusters(mode: str) -> tuple[list[float], dict[str, dict]]:
    tab = endpoint_table()

    specs = {
        "ML001": (
            ["F", "C", "G"],
            {("F", "C"): 0.557960449907, ("F", "G"): -0.258045752634, ("C", "G"): 0.422147553150},
        ),
        "ML002": (
            ["C", "F"],
            {("C", "F"): 0.670831130376},
        ),
        "ML003": (
            ["C", "Gadult", "Gjuvenile", "Gseed"],
            {
                ("C", "Gadult"): 0.309901518137,
                ("C", "Gjuvenile"): -0.691640628738,
                ("C", "Gseed"): -0.986425142587,
                ("Gadult", "Gjuvenile"): 0.445755836016,
                ("Gadult", "Gseed"): -0.301014841261,
                ("Gjuvenile", "Gseed"): 0.718337563279,
            },
        ),
        "ML014": (
            ["Gmating", "F"],
            {("Gmating", "F"): 0.326729868213},
        ),
    }

    result = {}
    pvals = []
    for cid, (eps, rhos) in specs.items():
        eff = {ep: tab[(cid, ep)]["lnrr"] for ep in eps}
        var = {ep: tab[(cid, ep)]["v"] for ep in eps}
        p, pairs = cluster_p(eff, var, rhos, mode)
        result[cid] = {"p": p, "effects": eff, "pairs": pairs}
        pvals.append(p)

    ml020_rhos = derive_ml020_rho()
    species_ps = []
    species_result = {}
    for sp in ("Atamisquea", "Cercidium", "Prosopis"):
        eff = {ep: tab[("ML020", f"{sp}:{ep}")]["lnrr"] for ep in ("I", "F")}
        var = {ep: tab[("ML020", f"{sp}:{ep}")]["v"] for ep in ("I", "F")}
        p, pairs = cluster_p(eff, var, {("I", "F"): ml020_rhos[sp]}, mode)
        species_ps.append(p)
        species_result[sp] = {"p": p, "effects": eff, "pairs": pairs}
    programme_p = min(1.0, 3.0 * min(species_ps))
    result["ML020"] = {"p": programme_p, "species": species_result}
    pvals.append(programme_p)
    return pvals, result


def main() -> None:
    tab = endpoint_table()
    validate_ml020_endpoint_reconstruction(tab)

    g_clusters = [state.ml001(), state.ml002(), state.ml003(), state.ml014(), state.ml020()]
    g_p = [x["cluster_p_bonferroni"] for x in g_clusters]
    _, _, g_full = fisher(g_p)
    _, _, g_drop_ml001 = fisher(g_p[1:])
    assert abs(g_full - 0.01212432) < 5e-8
    assert abs(g_drop_ml001 - 0.18194353) < 5e-8

    outputs = {}
    for mode in ("rho_proxy", "zero_cov", "cauchy_maxvar"):
        pvals, detail = lnrr_clusters(mode)
        full = fisher(pvals)[2]
        drop = fisher(pvals[1:])[2]
        outputs[mode] = {"pvals": pvals, "full": full, "drop_ml001": drop, "detail": detail}

    # Key scale sensitivity: Serapias C-F no longer separates on lnRR.
    cf_pair = next(
        x for x in outputs["rho_proxy"]["detail"]["ML001"]["pairs"]
        if {x["a"], x["b"]} == {"C", "F"}
    )
    assert abs(cf_pair["p"] - 0.6048817291933912) < 5e-8

    # Hedges-g says full rejection is Serapias-dependent; common lnRR working
    # assumptions do not, while the covariance-free worst-case does not certify
    # the omit-Serapias rejection. Hence robustness classification is scale/dependence sensitive.
    assert outputs["rho_proxy"]["drop_ml001"] < 0.05
    assert outputs["zero_cov"]["drop_ml001"] < 0.05
    assert outputs["cauchy_maxvar"]["drop_ml001"] > 0.05

    # ML001 absolute-magnitude ordering reverses materially across scales.
    g_order = sorted(("F", "C", "G"), key=lambda ep: abs(tab[("ML001", ep)]["g"]), reverse=True)
    r_order = sorted(("F", "C", "G"), key=lambda ep: abs(tab[("ML001", ep)]["lnrr"]), reverse=True)
    assert g_order == ["G", "C", "F"]
    assert r_order == ["C", "F", "G"]

    # Scale-independent qualitative direction: all primary direct effects are deterioration-oriented.
    assert sum(v["g"] < 0 for v in tab.values()) == 17
    assert sum(v["lnrr"] < 0 for v in tab.values()) == 17
    assert not any(v["g"] > 0 or v["lnrr"] > 0 for v in tab.values())

    summary_rows = rows(SUMMARY)
    by_id = {(r["row_type"], r["row_id"]): r for r in summary_rows}
    assert len(summary_rows) == 7
    for cid, gp, rp, zp, bp in zip(
        ("ML001", "ML002", "ML003", "ML014", "ML020"),
        g_p,
        outputs["rho_proxy"]["pvals"],
        outputs["zero_cov"]["pvals"],
        outputs["cauchy_maxvar"]["pvals"],
    ):
        r = by_id[("cluster", cid)]
        assert abs(float(r["hedges_g_p"]) - gp) < 5e-8
        assert abs(float(r["lnRR_rho_proxy_p"]) - rp) < 5e-8
        assert abs(float(r["lnRR_zero_cov_p"]) - zp) < 5e-8
        assert abs(float(r["lnRR_cauchy_maxvar_p"]) - bp) < 5e-8

    for rid, gp, rp, zp, bp in (
        ("FULL", g_full, outputs["rho_proxy"]["full"], outputs["zero_cov"]["full"], outputs["cauchy_maxvar"]["full"]),
        ("OMIT_ML001", g_drop_ml001, outputs["rho_proxy"]["drop_ml001"], outputs["zero_cov"]["drop_ml001"], outputs["cauchy_maxvar"]["drop_ml001"]),
    ):
        r = by_id[("fisher", rid)]
        assert abs(float(r["hedges_g_p"]) - gp) < 5e-8
        assert abs(float(r["lnRR_rho_proxy_p"]) - rp) < 5e-8
        assert abs(float(r["lnRR_zero_cov_p"]) - zp) < 5e-8
        assert abs(float(r["lnRR_cauchy_maxvar_p"]) - bp) < 5e-8

    print(
        "ESTIMAND_SCALE_SENSITIVITY_OK "
        f"g_full={g_full:.8f} g_drop_ML001={g_drop_ml001:.8f} "
        f"lnRR_rho_full={outputs['rho_proxy']['full']:.10g} "
        f"lnRR_rho_drop_ML001={outputs['rho_proxy']['drop_ml001']:.10g} "
        f"lnRR_zero_drop_ML001={outputs['zero_cov']['drop_ml001']:.10g} "
        f"lnRR_cauchy_drop_ML001={outputs['cauchy_maxvar']['drop_ml001']:.10g} "
        f"ML001_CF_lnRR_p={cf_pair['p']:.8f} "
        "primary_direct_signs_negative=17/17"
    )


if __name__ == "__main__":
    main()
