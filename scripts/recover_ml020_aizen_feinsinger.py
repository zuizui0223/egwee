from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_site_means_v1.csv"


def read_rows() -> list[dict[str, str]]:
    with DATA.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def sample_var(xs: list[float]) -> float:
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def pearson(x: list[float], y: list[float]) -> float:
    mx, my = mean(x), mean(y)
    sx = math.sqrt(sum((v - mx) ** 2 for v in x))
    sy = math.sqrt(sum((v - my) ** 2 for v in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def hedges_j(df: int) -> float:
    # Exact small-sample correction used for Hedges g.
    return math.exp(math.lgamma(df / 2.0) - 0.5 * math.log(df / 2.0) - math.lgamma((df - 1.0) / 2.0))


def hedges_g(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    if n1 < 2 or n2 < 2:
        raise ValueError("need at least two independent units per group")
    df = n1 + n2 - 2
    v1, v2 = sample_var(fragmented), sample_var(reference)
    sp2 = ((n1 - 1) * v1 + (n2 - 1) * v2) / df
    if sp2 <= 0:
        raise ValueError("pooled variance must be positive")
    d = (mean(fragmented) - mean(reference)) / math.sqrt(sp2)
    j = hedges_j(df)
    g = j * d
    # Large-sample (LS) sampling variance for SMD/Hedges g.
    var_g = (n1 + n2) / (n1 * n2) + (g * g) / (2.0 * df)
    return g, var_g


def two_sided_normal_p(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def species_result(rows: list[dict[str, str]], species: str) -> dict:
    sr = [r for r in rows if r["species"] == species]
    assert len(sr) == 8
    by_cond = {
        cond: sorted((r for r in sr if r["condition"] == cond), key=lambda r: int(r["site_id"]))
        for cond in ("continuous", "small")
    }
    assert [r["site_id"] for r in by_cond["continuous"]] == ["1", "2", "3", "5"]
    assert [r["site_id"] for r in by_cond["small"]] == ["1", "2", "3", "5"]

    effects: dict[str, float] = {}
    variances: dict[str, float] = {}
    for endpoint in ("I_pollen_tubes", "F_fruit_set"):
        frag = [float(r[endpoint]) for r in by_cond["small"]]
        ref = [float(r[endpoint]) for r in by_cond["continuous"]]
        g, v = hedges_g(frag, ref)
        effects[endpoint] = g
        variances[endpoint] = v

    # Group-centered correlation across the 8 aligned habitat units.
    x: list[float] = []
    y: list[float] = []
    for cond in ("continuous", "small"):
        rs = by_cond[cond]
        xv = [float(r["I_pollen_tubes"]) for r in rs]
        yv = [float(r["F_fruit_set"]) for r in rs]
        mx, my = mean(xv), mean(yv)
        x.extend(v - mx for v in xv)
        y.extend(v - my for v in yv)
    rho = pearson(x, y)
    cov = rho * math.sqrt(variances["I_pollen_tubes"] * variances["F_fruit_set"])
    var_diff = variances["I_pollen_tubes"] + variances["F_fruit_set"] - 2.0 * cov
    if not math.isfinite(var_diff) or var_diff <= 0:
        raise AssertionError(f"invalid I-F contrast variance for {species}: {var_diff}")
    diff = effects["I_pollen_tubes"] - effects["F_fruit_set"]
    se = math.sqrt(var_diff)
    z = diff / se
    p = two_sided_normal_p(z)

    # Positive definiteness for the 2x2 working V.
    det = variances["I_pollen_tubes"] * variances["F_fruit_set"] - cov * cov
    if not det > 0:
        raise AssertionError(f"non-positive-definite V for {species}: det={det}")

    return {
        "species": species,
        "n_fragmented_sites": 4,
        "n_reference_sites": 4,
        "effects": effects,
        "variances": variances,
        "rho_group_centered": rho,
        "sampling_covariance_proxy": cov,
        "I_minus_F": diff,
        "contrast_variance": var_diff,
        "contrast_se": se,
        "contrast_z": z,
        "contrast_p_two_sided": p,
    }


def main() -> None:
    rows = read_rows()
    species = ["Atamisquea emarginata", "Cercidium australe", "Prosopis nigra"]
    results = [species_result(rows, sp) for sp in species]
    p_programme = min(1.0, len(results) * min(r["contrast_p_two_sided"] for r in results))
    out = {
        "cluster_id": "ML020",
        "effect_family": "hedges_g_direct",
        "independent_programme_cluster": True,
        "species_are_dependent_subsystems": True,
        "species_results": results,
        "cluster_p_bonferroni": p_programme,
        "claim_ceiling": "retrospective source recovery; all source-explicit four-site replicated species retained; site habitat-unit means are the independent observations; one programme-level primary cluster only",
    }
    print("EGWEE_ML020 " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
