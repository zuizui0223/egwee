from __future__ import annotations

import csv
import json
import math
import os
import random
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[1]
WANDOO = ROOT / "evidence/meta_extraction/if_reliability_wandoo_table6_v1.csv"
CARDIO = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_table1_v1.csv"
KAKA = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_site_values_v1.csv"
W_COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_covariance_v1.csv"
C_COV = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_covariance_v1.json"
K_COV = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_covariance_v1.json"
EXPECTED = ROOT / "evidence/meta_extraction/if_reliability_sufficiency_v1.csv"

ND = NormalDist()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def sample_variance(xs: list[float]) -> float:
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def reliability_from_mean_se(means: list[float], ses: list[float]) -> float:
    v_obs = sample_variance(means)
    v_err = sum(se * se for se in ses) / len(ses)
    if v_obs <= 0:
        raise AssertionError("non-positive observed variance")
    return max(0.0, min(1.0, (v_obs - v_err) / v_obs))


def pooled_within_variance(values: list[float], groups: list[str]) -> float:
    total = 0.0
    df = 0
    for g in sorted(set(groups)):
        xs = [x for x, gg in zip(values, groups) if gg == g]
        total += (len(xs) - 1) * sample_variance(xs)
        df += len(xs) - 1
    return total / df


def reliability_binomial_site_means(values: list[float], totals: list[int], groups: list[str]) -> float:
    v_obs = pooled_within_variance(values, groups)
    v_err = sum(p * (1 - p) / n for p, n in zip(values, totals)) / len(values)
    return max(0.0, min(1.0, (v_obs - v_err) / v_obs))


def inv2(v11: float, v12: float, v22: float) -> tuple[float, float, float]:
    det = v11 * v22 - v12 * v12
    if det <= 0:
        raise AssertionError("non-positive covariance determinant")
    return v22 / det, -v12 / det, v11 / det


def quad2(x1: float, x2: float, i11: float, i12: float, i22: float) -> float:
    return i11*x1*x1 + 2*i12*x1*x2 + i22*x2*x2


def chi_square1_sf(q: float) -> float:
    # chi-square_1 = Z^2
    return 2.0 * (1.0 - ND.cdf(math.sqrt(max(0.0, q))))


def fit_common_rho(z_i: float, z_f: float, r_i: float, r_f: float, v11: float, v12: float, v22: float) -> tuple[float, float]:
    i11, i12, i22 = inv2(v11, v12, v22)
    best_rho = 0.0
    best_q = float("inf")
    # deterministic dense grid; sufficient at reported precision.
    for k in range(19801):
        rho = -0.99 + k * 0.0001
        mu_i = math.atanh(max(-0.999999, min(0.999999, rho * math.sqrt(r_i))))
        mu_f = math.atanh(max(-0.999999, min(0.999999, rho * math.sqrt(r_f))))
        q = quad2(z_i-mu_i, z_f-mu_f, i11, i12, i22)
        if q < best_q:
            best_q = q
            best_rho = rho
    return best_rho, best_q


def fit_common_smd(g_i: float, g_f: float, r_i: float, r_f: float, v11: float, v12: float, v22: float) -> tuple[float, float]:
    i11, i12, i22 = inv2(v11, v12, v22)
    a1, a2 = math.sqrt(r_i), math.sqrt(r_f)
    num = a1*(i11*g_i + i12*g_f) + a2*(i12*g_i + i22*g_f)
    den = a1*(i11*a1 + i12*a2) + a2*(i12*a1 + i22*a2)
    delta = num / den
    q = quad2(g_i-delta*a1, g_f-delta*a2, i11, i12, i22)
    return delta, q


def downstream_probability(mu_i: float, mu_f: float, v11: float, v12: float, v22: float, alpha_pair: float) -> tuple[float, float]:
    var_delta = v11 + v22 - 2*v12
    se = math.sqrt(var_delta)
    critical = ND.inv_cdf(1.0 - alpha_pair/2.0) * se
    mean_delta = mu_i - mu_f
    p = 1.0 - ND.cdf((critical - mean_delta) / se)
    return p, critical


def bivar_draw(mu1: float, mu2: float, v11: float, v12: float, v22: float, rng: random.Random) -> tuple[float, float]:
    l11 = math.sqrt(v11)
    l21 = v12 / l11
    l22 = math.sqrt(v22 - l21*l21)
    z1 = rng.gauss(0.0, 1.0)
    z2 = rng.gauss(0.0, 1.0)
    return mu1 + l11*z1, mu2 + l21*z1 + l22*z2


def wandoo() -> dict:
    rs = rows(WANDOO)
    r_i = reliability_from_mean_se([float(r["pollen_tubes"]) for r in rs], [float(r["pollen_tubes_se"]) for r in rs])
    r_f = reliability_from_mean_se([float(r["seeds_per_fruit_y2"]) for r in rs], [float(r["seeds_per_fruit_y2_se"]) for r in rs])
    cov = {(r["endpoint_i"], r["endpoint_j"]): float(r["sampling_covariance"]) for r in rows(W_COV)}
    v11 = cov[("I_pollen_tubes","I_pollen_tubes")]
    v22 = cov[("F_seeds_per_fruit_y2","F_seeds_per_fruit_y2")]
    v12 = cov[("I_pollen_tubes","F_seeds_per_fruit_y2")]
    z_i, z_f = 0.690291232004315, -0.875930795706820
    rho, q = fit_common_rho(z_i,z_f,r_i,r_f,v11,v12,v22)
    mu_i = math.atanh(rho*math.sqrt(r_i))
    mu_f = math.atanh(rho*math.sqrt(r_f))
    p_down, crit = downstream_probability(mu_i,mu_f,v11,v12,v22,0.05/3.0)
    return {
        "programme":"ML015_Wandoo","R_I":r_i,"R_F":r_f,"R_ratio":r_i/r_f,
        "required_R_ratio_abs":(math.tanh(z_i)/abs(math.tanh(z_f)))**2,
        "null_parameter":rho,"null_misfit_q":q,"null_misfit_p":chi_square1_sf(q),
        "artifact_downstream_probability":p_down,"critical_delta":crit,
        "mu_i":mu_i,"mu_f":mu_f,"point_sign_opposition":True,
        "note":"Source Table 6 population means and SE; sign opposition cannot arise in expectation from positive classical attenuation."
    }


def cardiopetalum() -> dict:
    rs = rows(CARDIO)
    i_mean=[float(r["pollinator_abundance_per_flower_mean"]) for r in rs]
    i_sd=[float(r["pollinator_abundance_per_flower_sd"]) for r in rs]
    f_mean=[float(r["fruit_set_mean"]) for r in rs]
    f_sd=[float(r["fruit_set_sd"]) for r in rs]
    # Source methods: ten marked plants per fragment. Using n=10 for both is conservative for I,
    # because I sampled 3-8 flowers on each of ten plants.
    r_i = reliability_from_mean_se(i_mean,[x/math.sqrt(10.0) for x in i_sd])
    r_f = reliability_from_mean_se(f_mean,[x/math.sqrt(10.0) for x in f_sd])
    cov=json.loads(C_COV.read_text(encoding="utf-8"))
    v11=float(cov["I_variance"]); v22=float(cov["F_variance"]); v12=float(cov["cov_IF"])
    z_i=float(cov["I_fisher_z"]); z_f=float(cov["F_fisher_z"])
    rho,q=fit_common_rho(z_i,z_f,r_i,r_f,v11,v12,v22)
    mu_i=math.atanh(rho*math.sqrt(r_i)); mu_f=math.atanh(rho*math.sqrt(r_f))
    p_down,crit=downstream_probability(mu_i,mu_f,v11,v12,v22,0.05)
    required=(math.tanh(z_i)/math.tanh(z_f))**2
    return {
        "programme":"P2_CARDIOPETALUM","R_I":r_i,"R_F":r_f,"R_ratio":r_i/r_f,
        "required_R_ratio_abs":required,"null_parameter":rho,"null_misfit_q":q,
        "null_misfit_p":chi_square1_sf(q),"artifact_downstream_probability":p_down,
        "critical_delta":crit,"mu_i":mu_i,"mu_f":mu_f,"point_sign_opposition":False,
        "note":"Reliability uses reported fragment SD / sqrt(10 plants); source I actually pools 3-8 flowers per each of ten plants."
    }


def kakamega() -> dict:
    rs=[r for r in rows(KAKA) if r["panel_id"]=="AP_2001" and r["common_IF_frame"]=="yes"]
    vals=[float(r["I_visit_occurrence"]) for r in rs]
    totals=[int(r["total_visit_units"]) for r in rs]
    groups=[r["habitat"] for r in rs]
    r_i=reliability_binomial_site_means(vals,totals,groups)
    # F replicate n is not required for the conservative test. Set R_F=1, which maximizes
    # the reliability advantage of F over I and therefore favours the attenuation-artifact null.
    r_f=1.0
    cov=json.loads(K_COV.read_text(encoding="utf-8"))["panel_blocks"]["AP_2001"]
    v11=float(cov["I_variance"]); v22=float(cov["F_variance"]); v12=float(cov["cov_IF"])
    g_i=float(cov["I_g"]); g_f=float(cov["F_g"])
    delta,q=fit_common_smd(g_i,g_f,r_i,r_f,v11,v12,v22)
    mu_i=delta*math.sqrt(r_i); mu_f=delta
    p_down,crit=downstream_probability(mu_i,mu_f,v11,v12,v22,0.05/4.0)
    required=(abs(g_i)/abs(g_f))**2
    return {
        "programme":"P2_KAKAMEGA_AP","R_I":r_i,"R_F":r_f,"R_ratio":r_i,
        "required_R_ratio_abs":required,"null_parameter":delta,"null_misfit_q":q,
        "null_misfit_p":chi_square1_sf(q),"artifact_downstream_probability":p_down,
        "critical_delta":crit,"mu_i":mu_i,"mu_f":mu_f,"point_sign_opposition":True,
        "note":"I reliability from binomial site effort; R_F fixed to 1 as worst-case advantage for the attenuation-artifact null."
    }


def assert_expected(result: dict, expected: dict[str, str]) -> None:
    for key in ("R_I","R_F","R_ratio","required_R_ratio_abs","null_misfit_p","artifact_downstream_probability"):
        assert abs(float(result[key])-float(expected[key])) < 5e-6, (result["programme"],key,result[key],expected[key])


def main() -> None:
    for p in (WANDOO,CARDIO,KAKA,W_COV,C_COV,K_COV,EXPECTED):
        assert p.is_file(), p
    results=[wandoo(),cardiopetalum(),kakamega()]
    exp={r["programme"]:r for r in rows(EXPECTED)}
    assert set(exp)=={r["programme"] for r in results}
    for r in results:
        assert_expected(r,exp[r["programme"]])

    # Empirical sufficiency checks.
    card=next(r for r in results if r["programme"]=="P2_CARDIOPETALUM")
    kaka=next(r for r in results if r["programme"]=="P2_KAKAMEGA_AP")
    wand=next(r for r in results if r["programme"]=="ML015_Wandoo")
    assert card["R_ratio"] > 10 * card["required_R_ratio_abs"]
    assert kaka["R_ratio"] > 10 * kaka["required_R_ratio_abs"]
    assert wand["point_sign_opposition"] and kaka["point_sign_opposition"]
    assert all(r["null_misfit_p"] < 0.01 for r in results)

    analytic_joint=math.prod(r["artifact_downstream_probability"] for r in results)

    mc = None
    if os.environ.get("RUN_RELIABILITY_MONTE_CARLO") == "1":
        n=int(os.environ.get("RELIABILITY_MONTE_CARLO_N","2000000"))
        rng=random.Random(20261006)
        counts={r["programme"]:0 for r in results}
        joint=0
        for _ in range(n):
            flags=[]
            for r in results:
                if r["programme"]=="ML015_Wandoo":
                    v11,v12,v22=0.125,0.014647278947066,0.125
                elif r["programme"]=="P2_CARDIOPETALUM":
                    d=json.loads(C_COV.read_text(encoding="utf-8"))
                    v11,v12,v22=float(d["I_variance"]),float(d["cov_IF"]),float(d["F_variance"])
                else:
                    d=json.loads(K_COV.read_text(encoding="utf-8"))["panel_blocks"]["AP_2001"]
                    v11,v12,v22=float(d["I_variance"]),float(d["cov_IF"]),float(d["F_variance"])
                x1,x2=bivar_draw(r["mu_i"],r["mu_f"],v11,v12,v22,rng)
                flag=(x1-x2)>r["critical_delta"]
                flags.append(flag)
                if flag: counts[r["programme"]]+=1
            if all(flags): joint+=1
        mc={"n":n,"rates":{k:v/n for k,v in counts.items()},"joint_count":joint,"joint_rate":joint/n}
        for r in results:
            assert abs(mc["rates"][r["programme"]]-r["artifact_downstream_probability"]) < 0.001
        assert abs(mc["joint_rate"]-analytic_joint) < 1.0e-5

    payload={
        "audit":"IF_measurement_reliability_sufficiency",
        "results":results,
        "analytic_joint_independence_product":analytic_joint,
        "joint_is_formal_p_value":False,
        "post_hoc_anchor_selection":True,
        "interpretation":"Simple classical reliability attenuation is quantitatively insufficient for the three resolved downstream anchors under the audited reliability proxies; the 3:0 prevalence/asymmetry claim remains exploratory.",
        "monte_carlo":mc,
    }
    print("IF_RELIABILITY_SUFFICIENCY " + json.dumps(payload,sort_keys=True))


if __name__=="__main__":
    main()
