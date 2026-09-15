from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS = ROOT / "scripts/synthesize_state_separation.py"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
TABLE = ROOT / "manuscript/tables/table_s2_covariance_robustness.csv"


def rows(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def two_sided_normal_p(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def fisher_sf_even_df(pvalues: list[float]) -> tuple[float, float]:
    if not pvalues or any(p <= 0.0 or p > 1.0 for p in pvalues):
        raise ValueError(pvalues)
    x = -2.0 * sum(math.log(p) for p in pvalues)
    k = len(pvalues)
    t = x / 2.0
    sf = math.exp(-t) * sum((t**j) / math.factorial(j) for j in range(k))
    return x, sf


def pair_p(e1: float, v1: float, e2: float, v2: float, mode: str) -> float:
    if mode == "zero_covariance":
        cov = 0.0
    elif mode == "cauchy_schwarz_max_variance":
        cov = -math.sqrt(v1 * v2)
    else:
        raise ValueError(mode)
    variance = v1 + v2 - 2.0 * cov
    if variance <= 0:
        raise AssertionError((e1, v1, e2, v2, mode, variance))
    z = (e1 - e2) / math.sqrt(variance)
    return two_sided_normal_p(z)


def bonferroni_cluster(effects: list[tuple[str, float, float]], mode: str) -> float:
    pair_ps = [
        pair_p(a[1], a[2], b[1], b[2], mode)
        for a, b in combinations(effects, 2)
    ]
    if not pair_ps:
        raise AssertionError("cluster requires >=2 endpoints")
    return min(1.0, len(pair_ps) * min(pair_ps))


def load_direct_effects() -> dict[str, list[tuple[str, float, float]]]:
    ser = [r for r in rows("evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv") if r["primary_or_sensitivity"] == "primary"]
    bros = [r for r in rows("evidence/meta_extraction/PS004_brosimum_extraction_v1.csv") if r["effect_unit_status"] == "g_admissible"]
    spon = [r for r in rows("evidence/meta_extraction/PS001_spondias_site_effects_v1.csv") if r["analysis_role"] == "primary"]
    soc = rows("evidence/meta_extraction/PS020_eucalyptus_socialis_effects_v1.csv")

    return {
        "ML001": [(r["layer"], float(r["oriented_effect"]), float(r["oriented_variance"])) for r in ser],
        "ML002": [(r["layer"], float(r["oriented_effect"]), float(r["oriented_variance"])) for r in bros],
        "ML003": [(r["layer"] + ":" + r["endpoint_id"], float(r["oriented_effect"]), float(r["oriented_variance"])) for r in spon],
        "ML014": [(r["layer"], float(r["oriented_effect"]), float(r["oriented_variance"])) for r in soc],
    }


def ml020_programme_p(mode: str) -> float:
    rs = rows("evidence/meta_extraction/PS022_aizen_feinsinger_effects_v1.csv")
    by_species: dict[str, list[tuple[str, float, float]]] = {}
    for r in rs:
        by_species.setdefault(r["species"], []).append(
            (r["layer"], float(r["oriented_effect"]), float(r["sampling_variance"]))
        )
    if set(by_species) != {"Atamisquea emarginata", "Cercidium australe", "Prosopis nigra"}:
        raise AssertionError(set(by_species))
    species_ps = []
    for effects in by_species.values():
        if len(effects) != 2:
            raise AssertionError(effects)
        species_ps.append(bonferroni_cluster(effects, mode))
    return min(1.0, 3 * min(species_ps))


def canonical_proxy() -> dict[str, float]:
    proc = subprocess.run(
        [sys.executable, str(SYNTHESIS)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    line = next(
        (x for x in proc.stdout.splitlines() if x.startswith("EGWEE_STATE_SEPARATION ")),
        None,
    )
    if line is None:
        raise AssertionError(proc.stdout)
    result = json.loads(line.split(" ", 1)[1])
    return {
        r["cluster_id"]: float(r["cluster_p_bonferroni"])
        for r in result["primary_clusters"]
    }


def regime(mode: str) -> dict:
    effects = load_direct_effects()
    cluster_ps = {cid: bonferroni_cluster(eff, mode) for cid, eff in effects.items()}
    cluster_ps["ML020"] = ml020_programme_p(mode)
    order = ["ML001", "ML002", "ML003", "ML014", "ML020"]
    x, p = fisher_sf_even_df([cluster_ps[c] for c in order])
    loo = {}
    for drop in order:
        kept = [cluster_ps[c] for c in order if c != drop]
        _, lp = fisher_sf_even_df(kept)
        loo[drop] = lp
    return {"cluster_p": cluster_ps, "fisher_x": x, "fisher_p": p, "leave_one_out_p": loo}


def check_table(proxy: dict, zero: dict, bound: dict) -> None:
    with TABLE.open(newline="", encoding="utf-8") as fh:
        tab = {r["regime"]: r for r in csv.DictReader(fh)}
    assert set(tab) == {
        "frozen_paired_covariance_proxy",
        "zero_covariance",
        "cauchy_schwarz_certification_bound",
    }
    for name, result in (
        ("frozen_paired_covariance_proxy", proxy),
        ("zero_covariance", zero),
        ("cauchy_schwarz_certification_bound", bound),
    ):
        row = tab[name]
        for cid in ("ML001", "ML002", "ML003", "ML014", "ML020"):
            assert abs(float(row[f"{cid}_cluster_p"]) - result["cluster_p"][cid]) < 5e-8
        assert abs(float(row["fisher_statistic"]) - result["fisher_x"]) < 1e-10
        assert abs(float(row["full_fisher_p"]) - result["fisher_p"]) < 1e-12
        assert abs(float(row["omit_ML001_p"]) - result["leave_one_out_p"]["ML001"]) < 1e-12


def check_manuscript() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for token in (
        "### Dependence sensitivity and covariance-free certification boundary",
        "Supplementary Table S2",
        "p=0.03860161",
        "p=0.28061178",
        "p=0.57123438",
        "p=0.92060125",
        "cannot be certified from marginal effects alone",
        "not an alternative biological covariance model",
        "Standardized effects also depend on endpoint-specific between-unit dispersion",
        "It may not claim covariance-free global rejection",
    ):
        assert token in text, token


def main() -> None:
    proxy_ps = canonical_proxy()
    order = ["ML001", "ML002", "ML003", "ML014", "ML020"]
    proxy_x, proxy_p = fisher_sf_even_df([proxy_ps[c] for c in order])
    proxy_loo = {}
    for drop in order:
        _, p = fisher_sf_even_df([proxy_ps[c] for c in order if c != drop])
        proxy_loo[drop] = p
    proxy = {"cluster_p": proxy_ps, "fisher_x": proxy_x, "fisher_p": proxy_p, "leave_one_out_p": proxy_loo}

    zero = regime("zero_covariance")
    bound = regime("cauchy_schwarz_max_variance")

    assert abs(proxy_p - 0.01212432410511315) < 1e-12
    assert abs(zero["fisher_p"] - 0.038601605823083425) < 1e-12
    assert abs(bound["fisher_p"] - 0.280611779992871) < 1e-12
    assert abs(zero["leave_one_out_p"]["ML001"] - 0.5712343808812794) < 1e-12
    assert abs(bound["leave_one_out_p"]["ML001"] - 0.9206012453762535) < 1e-12

    check_table(proxy, zero, bound)
    check_manuscript()

    out = {
        "primary_proxy": proxy,
        "zero_covariance": zero,
        "cauchy_schwarz_certification_bound": bound,
        "interpretation": (
            "The full rejection survives a zero-covariance working sensitivity but is not "
            "certifiable from marginal effects alone under pairwise Cauchy-Schwarz covariance bounds. "
            "The bound is a covariance-free certification limit, not a jointly realised alternative covariance model."
        ),
    }
    print("COVARIANCE_ROBUSTNESS " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
