from __future__ import annotations

import csv
import json
import math
import statistics as stats
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALUES = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_site_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_covariance_v1.json"
RULE = ROOT / "manuscript/CF01_BERGSDORF_KAKAMEGA_2006_DIRECT_IF_RECOVERY_RULE.md"
RESULT = ROOT / "manuscript/PHASE2_CF01_BERGSDORF_KAKAMEGA_DIRECT_IF_RECOVERY_2026-09-27.md"
PAIR = ROOT / "evidence/meta_extraction/coverage_expansion_pair_coverage_v1.csv"

PROGRAMME = "P2_CF01_BERGSDORF_KAKAMEGA_2006"
PANELS = ["AP_2001", "AE_2002", "AE_2003", "HD_2002_03"]
EXPECTED_N = {
    "AP_2001": (4, 3),
    "AE_2002": (2, 3),
    "AE_2003": (3, 4),
    "HD_2002_03": (3, 4),
}
TOL = 5e-10
Z95 = 1.959963984540054


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pearson(x: list[float], y: list[float]) -> float:
    mx, my = stats.mean(x), stats.mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(
        sum(a * a for a in dx) * sum(b * b for b in dy)
    )


def centered(values: list[float], groups: list[str]) -> list[float]:
    means = {
        g: stats.mean(v for v, gg in zip(values, groups) if gg == g)
        for g in set(groups)
    }
    return [v - means[g] for v, g in zip(values, groups)]


def hedges_g(fragmented: list[float], main: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(main)
    df = n1 + n2 - 2
    m1, m2 = stats.mean(fragmented), stats.mean(main)
    s1, s2 = stats.stdev(fragmented), stats.stdev(main)
    sp = math.sqrt(((n1 - 1) * s1 * s1 + (n2 - 1) * s2 * s2) / df)
    d = (m1 - m2) / sp
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    variance = 1 / n1 + 1 / n2 + g * g / (2 * (n1 + n2))
    return g, variance


def panel_calc(rr: list[dict[str, str]]) -> dict[str, float]:
    common = [r for r in rr if r["common_IF_frame"] == "yes"]
    frag = [r for r in common if r["habitat"] == "fragment"]
    main = [r for r in common if r["habitat"] == "main"]
    i_frag = [float(r["I_visit_occurrence"]) for r in frag]
    i_main = [float(r["I_visit_occurrence"]) for r in main]
    f_frag = [float(r["F_fruit_set"]) for r in frag]
    f_main = [float(r["F_fruit_set"]) for r in main]

    gi, vi = hedges_g(i_frag, i_main)
    gf, vf = hedges_g(f_frag, f_main)

    i_all = i_frag + i_main
    f_all = f_frag + f_main
    groups = ["fragment"] * len(frag) + ["main"] * len(main)
    rho = pearson(centered(i_all, groups), centered(f_all, groups))
    cov = rho * math.sqrt(vi * vf)
    det = vi * vf - cov * cov
    assert det > 0
    delta = gi - gf
    vd = vi + vf - 2 * cov
    assert vd > 0
    se = math.sqrt(vd)
    z = delta / se
    p = math.erfc(abs(z) / math.sqrt(2))
    return {
        "n_fragment": len(frag),
        "n_main": len(main),
        "I_g": gi,
        "I_variance": vi,
        "F_g": gf,
        "F_variance": vf,
        "rho": rho,
        "cov": cov,
        "det": det,
        "delta": delta,
        "variance": vd,
        "se": se,
        "z": z,
        "p": p,
        "ci_low": delta - Z95 * se,
        "ci_high": delta + Z95 * se,
    }


def main() -> None:
    for path in (VALUES, EFFECTS, COV, RULE, RESULT, PAIR):
        assert path.is_file(), path

    values = rows(VALUES)
    assert all(r["programme_id"] == PROGRAMME for r in values)
    by_panel: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in values:
        by_panel[row["panel_id"]].append(row)
        if row["common_IF_frame"] == "yes":
            assert row["I_visit_occurrence"] != ""
            assert row["F_fruit_set"] != ""
            n0 = int(row["zero_visit_units"])
            nt = int(row["total_visit_units"])
            assert nt > 0 and 0 <= n0 <= nt
            assert abs(float(row["I_visit_occurrence"]) - (1 - n0 / nt)) < 5e-12

    assert set(by_panel) == set(PANELS)
    assert len([r for r in by_panel["AE_2002"] if r["common_IF_frame"] == "no"]) == 1
    yala = next(r for r in by_panel["AE_2002"] if r["site"] == "Yala")
    assert yala["common_IF_frame"] == "no"
    assert yala["I_visit_occurrence"] == ""
    assert yala["F_fruit_set"] == "0.03"

    calc = {p: panel_calc(by_panel[p]) for p in PANELS}
    assert {
        p: (calc[p]["n_fragment"], calc[p]["n_main"]) for p in PANELS
    } == EXPECTED_N

    effects = {(r["panel_id"], r["layer"]): r for r in rows(EFFECTS)}
    assert len(effects) == 8
    for p in PANELS:
        x = calc[p]
        for layer, g_key, v_key in (
            ("I_interaction", "I_g", "I_variance"),
            ("F_reproductive_function", "F_g", "F_variance"),
        ):
            row = effects[(p, layer)]
            assert row["programme_id"] == PROGRAMME
            assert row["effect_stream"] == "hedges_g_direct"
            assert row["primary_or_sensitivity"] == "primary"
            assert int(row["n_fragment"]) == x["n_fragment"]
            assert int(row["n_main"]) == x["n_main"]
            assert abs(float(row["hedges_g"]) - x[g_key]) < TOL
            assert abs(float(row["variance"]) - x[v_key]) < TOL

    co = json.loads(COV.read_text(encoding="utf-8"))
    assert co["programme_id"] == PROGRAMME
    assert co["status"] == "direct_IF_four_panel_covariance_aware_retrospective"
    assert co["recovered_panels"] == PANELS
    assert co["programme_is_retrospective"] is True
    assert co["pair_programme_increment"] == 1
    assert co["phase1_primary_cluster_increment"] == 0
    assert len(co["blocked_panels"]) == 1
    assert co["blocked_panels"][0]["panel"] == "Dracaena_fragrans_2002_03"

    for p in PANELS:
        x = calc[p]
        block = co["panel_blocks"][p]
        assert block["positive_definite"] is True
        for key, calc_key in (
            ("I_g", "I_g"),
            ("I_variance", "I_variance"),
            ("F_g", "F_g"),
            ("F_variance", "F_variance"),
            ("residual_rho_IF", "rho"),
            ("cov_IF", "cov"),
            ("covariance_determinant", "det"),
        ):
            assert abs(block[key] - x[calc_key]) < TOL
        pair = block["I_minus_F"]
        assert abs(pair["delta"] - x["delta"]) < TOL
        assert abs(pair["variance"] - x["variance"]) < TOL
        assert abs(pair["se"] - x["se"]) < TOL
        assert abs(pair["z"] - x["z"]) < TOL
        assert abs(pair["p_two_sided"] - x["p"]) < TOL
        assert abs(pair["ci95"][0] - x["ci_low"]) < TOL
        assert abs(pair["ci95"][1] - x["ci_high"]) < TOL

    min_p = min(calc[p]["p"] for p in PANELS)
    programme_p = min(1.0, 4 * min_p)
    gate = co["programme_internal_gate"]
    assert gate["method"] == "Bonferroni_across_four_recovered_dependent_panels"
    assert abs(gate["min_panel_p"] - min_p) < TOL
    assert gate["multiplier"] == 4
    assert abs(gate["p_programme"] - programme_p) < TOL

    assert calc["AP_2001"]["delta"] > 0
    assert calc["AP_2001"]["ci_low"] > 0
    assert calc["AP_2001"]["p"] < 0.01
    assert calc["AE_2002"]["ci_low"] < 0 < calc["AE_2002"]["ci_high"]
    assert calc["AE_2003"]["ci_low"] < 0 < calc["AE_2003"]["ci_high"]
    assert calc["HD_2002_03"]["ci_low"] < 0 < calc["HD_2002_03"]["ci_high"]

    rule = RULE.read_text(encoding="utf-8")
    for token in (
        "retrospective external recovery",
        "site/local-context observational contrast",
        "Every panel meeting those criteria is retained regardless of effect direction or significance",
        "Dracaena fragrans",
        "standardized visitation-occurrence support",
        "p_programme=min(1, 4*min(p_panel))",
        "pair-specific direct I-F coverage by one",
        "does **not** modify the frozen Phase-1 five-cluster Fisher synthesis",
    ):
        assert token in rule, token

    result = RESULT.read_text(encoding="utf-8")
    for token in (
        "one retrospective direct I-F programme",
        "four dependent species×campaign panels",
        "I − F: **+3.197**",
        "p = **0.00163**",
        "p_programme = min(1, 4 × min(p_panel)) = 0.00653539",
        "2/5 to **3/5**",
        "does not add a sixth Phase-1 cluster",
    ):
        assert token in result, token

    pair_rows = {r["pair_id"]: r for r in rows(PAIR)}
    i_f = pair_rows["I-F"]
    assert int(i_f["current_independent_direct_systems"]) == 3
    assert set(i_f["current_system_ids"].split(";")) == {
        "ML020",
        "P2_CF01_SEVENELLO_2026",
        PROGRAMME,
    }

    print(
        "PHASE2_CF01_BERGSDORF_CHECK_OK "
        f"panels=4 programme_p={programme_p:.8f} "
        f"AP_delta={calc['AP_2001']['delta']:.8f} AP_p={calc['AP_2001']['p']:.8f} "
        "direct_IF=3/5 phase1_unchanged=true retrospective=true"
    )


if __name__ == "__main__":
    main()
