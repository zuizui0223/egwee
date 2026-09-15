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
    # Canonical EGWEE primary scripts use the standard small-sample approximation.
    return 1.0 - 3.0 / (4.0 * df - 1.0)


def ls_smd_variance(g: float, n1: int, n2: int) -> float:
    # Matches the canonical primary direct-cluster variance implementation.
    return (n1 + n2) / (n1 * n2) + (g * g) / (2.0 * (n1 + n2))


def hedges_g(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    df = n1 + n2 - 2
    v1, v2 = sample_var(fragmented), sample_var(reference)
    sp2 = ((n1 - 1) * v1 + (n2 - 1) * v2) / df
    if sp2 <= 0:
        raise ValueError("pooled variance must be positive")
    d = (mean(fragmented) - mean(reference)) / math.sqrt(sp2)
    g = hedges_j(df) * d
    return g, ls_smd_variance(g, n1, n2)


def two_sided_normal_p(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def species_result(rows: list[dict[str, str]], species: str) -> dict:
    sr = [r for r in rows if r["species"] == species]
    assert len(sr) == 8
    by_cond = {
        cond: sorted((r for r in sr if r["condition"] == cond), key=lambda r: int(r["site_id"]))
        for cond in ("continuous", "small")
    }
    for cond in by_cond:
        assert [r["site_id"] for r in by_cond[cond]] == ["1", "2", "3", "5"]

    effects: dict[str, float] = {}
    variances: dict[str, float] = {}
    for endpoint in ("I_pollen_tubes", "F_fruit_set"):
        fragmented = [float(r[endpoint]) for r in by_cond["small"]]
        reference = [float(r[endpoint]) for r in by_cond["continuous"]]
        effects[endpoint], variances[endpoint] = hedges_g(fragmented, reference)

    centered_i: list[float] = []
    centered_f: list[float] = []
    for cond in ("continuous", "small"):
        rs = by_cond[cond]
        iv = [float(r["I_pollen_tubes"]) for r in rs]
        fv = [float(r["F_fruit_set"]) for r in rs]
        mi, mf = mean(iv), mean(fv)
        centered_i.extend(x - mi for x in iv)
        centered_f.extend(x - mf for x in fv)
    rho = pearson(centered_i, centered_f)
    cov = rho * math.sqrt(variances["I_pollen_tubes"] * variances["F_fruit_set"])

    vdiff = variances["I_pollen_tubes"] + variances["F_fruit_set"] - 2.0 * cov
    if not math.isfinite(vdiff) or vdiff <= 0:
        raise AssertionError((species, "invalid contrast variance", vdiff))
    det = variances["I_pollen_tubes"] * variances["F_fruit_set"] - cov * cov
    if det <= 0:
        raise AssertionError((species, "working covariance not positive definite", det))

    diff = effects["I_pollen_tubes"] - effects["F_fruit_set"]
    se = math.sqrt(vdiff)
    z = diff / se
    p = two_sided_normal_p(z)
    return {
        "species": species,
        "n_fragmented_sites": 4,
        "n_reference_sites": 4,
        "effects": effects,
        "variances": variances,
        "rho_group_centered": rho,
        "sampling_covariance_proxy": cov,
        "covariance_determinant": det,
        "I_minus_F": diff,
        "contrast_variance": vdiff,
        "contrast_se": se,
        "contrast_z": z,
        "contrast_p_two_sided": p,
    }


def main() -> None:
    # Regression check against canonical ML014 variance semantics.
    assert abs(ls_smd_variance(-1.02391388, 13, 15) - 0.16231117) < 1e-8
    # Regression check against the correction used by existing primary scripts.
    assert abs(hedges_j(6) - (1 - 3 / 23)) < 1e-15

    rows = read_rows()
    species = ["Atamisquea emarginata", "Cercidium australe", "Prosopis nigra"]
    results = [species_result(rows, sp) for sp in species]
    p_programme = min(1.0, 3.0 * min(r["contrast_p_two_sided"] for r in results))
    out = {
        "cluster_id": "ML020",
        "effect_family": "hedges_g_direct",
        "independent_programme_cluster": True,
        "species_are_dependent_subsystems": True,
        "species_results": results,
        "cluster_p_bonferroni": p_programme,
        "claim_ceiling": "retrospective source recovery; all source-explicit four-site replicated species retained; site habitat-unit means are independent observations; one programme-level primary cluster only",
    }
    print("EGWEE_ML020 " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
