from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-19_GPAIR_SYNTHESIS.md"
INPUTS = ROOT / "evidence/meta_extraction/phase2_gpair_programme_contrasts_v1.csv"
RESULT = ROOT / "evidence/meta_extraction/phase2_gpair_synthesis_v1.json"
STATUS = ROOT / "manuscript/PHASE2_GPAIR_SYNTHESIS_2026-09-19.md"

SPONDIAS_CONTRASTS = ROOT / "evidence/meta_extraction/PS001_spondias_cohort_contrasts_v1.csv"
SPONDIAS_COV = ROOT / "evidence/meta_extraction/PS001_spondias_primary_pairwise_covariance_v2.csv"
PARKIA_COV = ROOT / "evidence/meta_extraction/phase2_sf05_93_parkia_covariance_v1.json"
HELICONIA_COV = ROOT / "evidence/meta_extraction/phase2_sf05_71_heliconia_covariance_v1.json"
PRUNUS_ETH_COV = ROOT / "evidence/meta_extraction/phase2_cf01_prunus_2014_covariance_v1.json"
PRUNUS_KAKAMEGA_COV = ROOT / "evidence/meta_extraction/phase2_cf01_prunus_kakamega_2008_covariance_v1.json"

PROGRAMME_ORDER = [
    "ML003",
    "P2_SF05_93",
    "P2_SF05_71",
    "P2_CF01_GPAIR_002",
    "P2_CF01_GPAIR_003",
]
TOL = 5e-9
T_CRIT_DF4 = 2.7764451051977987


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pair_json(path: Path) -> tuple[float, float]:
    data = json.loads(path.read_text(encoding="utf-8"))
    pair = data["primary_pair"]
    assert pair["pair_id"] == "G_adult-G_offspring"
    assert pair["positive_definite"] is True
    return (
        float(pair["effect_difference_Gadult_minus_Goffspring"]),
        float(pair["difference_variance"]),
    )


def spondias_programme() -> tuple[float, float, dict[str, float]]:
    contrasts = {r["contrast"]: r for r in rows(SPONDIAS_CONTRASTS)}
    juvenile = contrasts["juvenile_vs_adult_Ho"]
    seed = contrasts["seed_vs_adult_Ho"]

    # Stored source rows are later-minus-adult; Phase-2 pair orientation is adult-minus-offspring.
    d_aj = -float(juvenile["delta_later_minus_adult"])
    d_as = -float(seed["delta_later_minus_adult"])
    v_aj = float(juvenile["delta_variance"])
    v_as = float(seed["delta_variance"])

    cov_rows = rows(SPONDIAS_COV)
    by_pair = {(r["endpoint_i"], r["endpoint_j"]): float(r["sampling_covariance"]) for r in cov_rows}
    var_a = by_pair[("Gadult_Ho", "Gadult_Ho")]
    cov_aj_endpoint = by_pair[("Gadult_Ho", "Gjuvenile_Ho")]
    cov_as_endpoint = by_pair[("Gadult_Ho", "Gseed_Ho")]
    cov_js_endpoint = by_pair[("Gjuvenile_Ho", "Gseed_Ho")]

    cov_contrasts = var_a - cov_aj_endpoint - cov_as_endpoint + cov_js_endpoint
    d = 0.5 * (d_aj + d_as)
    v = 0.25 * (v_aj + v_as + 2 * cov_contrasts)
    assert v > 0
    return d, v, {
        "adult_minus_juvenile": d_aj,
        "adult_minus_seed": d_as,
        "var_adult_minus_juvenile": v_aj,
        "var_adult_minus_seed": v_as,
        "contrast_covariance": cov_contrasts,
    }


def reml_nll(tau2: float, effects: list[float], variances: list[float]) -> float:
    assert tau2 >= 0
    total_var = [v + tau2 for v in variances]
    weights = [1.0 / v for v in total_var]
    sw = sum(weights)
    mu = sum(w * y for w, y in zip(weights, effects)) / sw
    q = sum(w * (y - mu) ** 2 for w, y in zip(weights, effects))
    return 0.5 * (sum(math.log(v) for v in total_var) + math.log(sw) + q)


def golden_minimum(effects: list[float], variances: list[float]) -> float:
    lo = 0.0
    hi = max(10.0, 100.0 * max(variances))
    phi = (1 + math.sqrt(5)) / 2
    c = hi - (hi - lo) / phi
    d = lo + (hi - lo) / phi
    fc = reml_nll(c, effects, variances)
    fd = reml_nll(d, effects, variances)
    for _ in range(250):
        if fc <= fd:
            hi, d, fd = d, c, fc
            c = hi - (hi - lo) / phi
            fc = reml_nll(c, effects, variances)
        else:
            lo, c, fc = c, d, fd
            d = lo + (hi - lo) / phi
            fd = reml_nll(d, effects, variances)
    candidate = (lo + hi) / 2
    if reml_nll(0.0, effects, variances) <= reml_nll(candidate, effects, variances) + 1e-11:
        return 0.0
    return candidate


def meta(effects: list[float], variances: list[float]) -> dict[str, object]:
    k = len(effects)
    tau2 = reml_tau = golden_minimum(effects, variances)
    weights = [1.0 / (v + reml_tau) for v in variances]
    sw = sum(weights)
    mu = sum(w * y for w, y in zip(weights, effects)) / sw
    se_model = math.sqrt(1.0 / sw)
    q = sum(w * (y - mu) ** 2 for w, y in zip(weights, effects))
    q_scale = q / (k - 1)
    q_star = max(1.0, q_scale)
    se_mkh = se_model * math.sqrt(q_star)
    i2 = max(0.0, (q - (k - 1)) / q) if q > 0 else 0.0
    return {
        "tau2": tau2,
        "mu": mu,
        "se_model": se_model,
        "Q": q,
        "q_scale": q_scale,
        "q_star": q_star,
        "se_mkh": se_mkh,
        "I2": i2,
        "weights": [w / sw for w in weights],
    }


def t4_two_sided_p(t_abs: float) -> float:
    # For df=4, two-sided p = I_x(2,1/2), x=4/(4+t^2).
    a = t_abs / math.sqrt(4.0 + t_abs * t_abs)
    return 1.0 - 1.5 * a + 0.5 * a**3


def assert_close(actual: float, expected: float, tol: float = TOL) -> None:
    assert abs(actual - expected) < tol, (actual, expected)


def main() -> None:
    for path in (
        AMENDMENT, INPUTS, RESULT, STATUS, SPONDIAS_CONTRASTS, SPONDIAS_COV,
        PARKIA_COV, HELICONIA_COV, PRUNUS_ETH_COV, PRUNUS_KAKAMEGA_COV,
    ):
        assert path.is_file(), path

    amendment = AMENDMENT.read_text(encoding="utf-8")
    for token in (
        "exactly five independent programmes",
        "equal-weight mean",
        "restricted maximum likelihood",
        "modified Knapp–Hartung",
        "K-1 = 4",
        "leave-one-programme-out",
    ):
        assert token in amendment, token

    s_delta, s_var, s_parts = spondias_programme()
    source_values = {
        "ML003": (s_delta, s_var),
        "P2_SF05_93": pair_json(PARKIA_COV),
        "P2_SF05_71": pair_json(HELICONIA_COV),
        "P2_CF01_GPAIR_002": pair_json(PRUNUS_ETH_COV),
        "P2_CF01_GPAIR_003": pair_json(PRUNUS_KAKAMEGA_COV),
    }

    input_rows = rows(INPUTS)
    assert [r["programme_id"] for r in input_rows] == PROGRAMME_ORDER
    for r in input_rows:
        y, v = source_values[r["programme_id"]]
        assert r["pair_id"] == "G_adult-G_offspring"
        assert_close(float(r["programme_contrast"]), y)
        assert_close(float(r["programme_variance"]), v)

    effects = [source_values[p][0] for p in PROGRAMME_ORDER]
    variances = [source_values[p][1] for p in PROGRAMME_ORDER]
    fit = meta(effects, variances)
    assert fit["tau2"] == 0.0

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["n_independent_programmes"] == 5
    assert result["programme_ids"] == PROGRAMME_ORDER

    s_out = result["spondias_primary_aggregation"]
    assert_close(s_out["adult_minus_juvenile"], s_parts["adult_minus_juvenile"])
    assert_close(s_out["adult_minus_seed"], s_parts["adult_minus_seed"])
    assert_close(s_out["contrast_covariance"], s_parts["contrast_covariance"])
    assert_close(s_out["programme_contrast"], s_delta)
    assert_close(s_out["programme_variance"], s_var)

    primary = result["primary_random_effects"]
    assert_close(primary["tau2"], fit["tau2"])
    assert_close(primary["pooled_mean"], fit["mu"])
    assert_close(primary["model_based_se"], fit["se_model"])
    assert_close(primary["cochran_Q"], fit["Q"])
    assert_close(primary["I2"], fit["I2"])
    assert_close(primary["mKH_q"], fit["q_scale"])
    assert_close(primary["mKH_q_star"], fit["q_star"])
    assert_close(primary["mKH_se"], fit["se_mkh"])
    assert primary["t_df"] == 4

    t_stat = fit["mu"] / fit["se_mkh"]
    p = t4_two_sided_p(abs(t_stat))
    ci = [
        fit["mu"] - T_CRIT_DF4 * fit["se_mkh"],
        fit["mu"] + T_CRIT_DF4 * fit["se_mkh"],
    ]
    normal_ci = [
        fit["mu"] - 1.959963984540054 * fit["se_model"],
        fit["mu"] + 1.959963984540054 * fit["se_model"],
    ]
    assert_close(primary["t_statistic"], t_stat)
    assert_close(primary["p_two_sided_t"], p)
    for got, exp in zip(primary["ci95_mKH"], ci):
        assert_close(got, exp)
    for got, exp in zip(primary["ci95_model_based_normal"], normal_ci):
        assert_close(got, exp)
    assert ci[0] < 0 < ci[1]

    for pid, w in zip(PROGRAMME_ORDER, fit["weights"]):
        assert_close(primary["normalized_weights"][pid], w)

    # Endpoint sensitivity: replace only the equal-weight ML003 programme row.
    sens = result["spondias_endpoint_sensitivity"]
    for label, y, v in (
        ("juvenile_only", s_parts["adult_minus_juvenile"], s_parts["var_adult_minus_juvenile"]),
        ("seed_only", s_parts["adult_minus_seed"], s_parts["var_adult_minus_seed"]),
    ):
        y2 = effects[:]
        v2 = variances[:]
        y2[0] = y
        v2[0] = v
        f = meta(y2, v2)
        assert f["tau2"] == 0.0
        assert_close(sens[label]["pooled_mean"], f["mu"])
        assert_close(sens[label]["model_based_se"], f["se_model"])
        sci = [f["mu"] - T_CRIT_DF4 * f["se_mkh"], f["mu"] + T_CRIT_DF4 * f["se_mkh"]]
        for got, exp in zip(sens[label]["ci95_mKH"], sci):
            assert_close(got, exp)
        sp = t4_two_sided_p(abs(f["mu"] / f["se_mkh"]))
        assert_close(sens[label]["p_two_sided_t_df4"], sp)

    loo = {r["dropped"]: r for r in result["leave_one_programme_out"]}
    assert set(loo) == set(PROGRAMME_ORDER)
    for idx, pid in enumerate(PROGRAMME_ORDER):
        y2 = [y for j, y in enumerate(effects) if j != idx]
        v2 = [v for j, v in enumerate(variances) if j != idx]
        f = meta(y2, v2)
        assert_close(loo[pid]["pooled_mean"], f["mu"])
        assert_close(loo[pid]["tau2"], f["tau2"])

    interpretation = result["interpretation"]
    assert interpretation["directional_common_cohort_lag_resolved"] is False
    assert interpretation["exchangeability_proven"] is False
    assert interpretation["moderator_models_open"] is False
    assert interpretation["phase1_baseline_changed"] is False
    assert interpretation["phase2_supersession_allowed_yet"] is False

    status = STATUS.read_text(encoding="utf-8")
    for token in (
        "mean contrast = +0.129",
        "−0.655 to +0.912",
        "does **not** resolve a common directional cohort lag",
        "Moderator models remain closed at K=5",
        "systematic search universe is not yet complete",
    ):
        assert token in status, token

    print(
        "PHASE2_GPAIR_SYNTHESIS_OK "
        f"K=5 mean={fit['mu']:.9f} tau2={fit['tau2']:.9f} "
        f"mKH_CI=[{ci[0]:.9f},{ci[1]:.9f}] p={p:.9f} directional_lag=false"
    )


if __name__ == "__main__":
    main()
