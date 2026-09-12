from __future__ import annotations

import csv
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C_SITE = ROOT / "evidence/meta_extraction/PS001_spondias_paternity_site_table_v1.csv"
G_SITE = ROOT / "evidence/meta_extraction/PS001_spondias_adult_sgs_site_table_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/PS001_spondias_site_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/PS001_spondias_primary_covariance_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"

ENDPOINTS = ["C_paternity_correlation", "Gadult_Sp"]


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def hedges_g_metafor_ls(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    df = n1 + n2 - 2
    pooled = math.sqrt(
        ((n1 - 1) * stats.stdev(fragmented) ** 2 + (n2 - 1) * stats.stdev(reference) ** 2) / df
    )
    d = (stats.mean(fragmented) - stats.mean(reference)) / pooled
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    variance = 1 / n1 + 1 / n2 + g**2 / (2 * (n1 + n2))
    return g, variance


def pearson(x: list[float], y: list[float]) -> float:
    mx, my = stats.mean(x), stats.mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(
        sum(a * a for a in dx) * sum(b * b for b in dy)
    )


def centered(values: dict[str, float], habitat: dict[str, str], pops: list[str]) -> list[float]:
    means = {
        group: stats.mean(values[p] for p in pops if habitat[p] == group)
        for group in {habitat[p] for p in pops}
    }
    return [values[p] - means[habitat[p]] for p in pops]


def main() -> None:
    for path in (C_SITE, G_SITE, EFFECTS, COV, REGISTRY):
        assert path.is_file(), path

    c_rows = rows(C_SITE)
    g_rows = rows(G_SITE)
    assert len(c_rows) == len(g_rows) == 5
    c_by_pop = {r["population"]: r for r in c_rows}
    g_by_pop = {r["population"]: r for r in g_rows}
    assert set(c_by_pop) == set(g_by_pop) == {"Careyes", "Chamela", "Mesa", "Nacastillo", "Ranchitos"}

    pops = sorted(c_by_pop)
    habitat = {p: c_by_pop[p]["habitat"] for p in pops}
    assert all(g_by_pop[p]["habitat"] == habitat[p] for p in pops)
    assert sum(habitat[p] == "FRA" for p in pops) == 3
    assert sum(habitat[p] == "CON" for p in pops) == 2

    raw_c = {p: float(c_by_pop[p]["multilocus_correlated_paternity_rp"]) for p in pops}
    raw_g = {p: float(g_by_pop[p]["adult_spatial_genetic_structure_Sp"]) for p in pops}
    frag = [p for p in pops if habitat[p] == "FRA"]
    ref = [p for p in pops if habitat[p] == "CON"]

    c_g, c_var = hedges_g_metafor_ls([raw_c[p] for p in frag], [raw_c[p] for p in ref])
    g_g, g_var = hedges_g_metafor_ls([raw_g[p] for p in frag], [raw_g[p] for p in ref])

    effects = {r["endpoint_id"]: r for r in rows(EFFECTS)}
    assert set(effects) == set(ENDPOINTS)
    c_effect = effects["C_paternity_correlation"]
    g_effect = effects["Gadult_Sp"]
    for row in (c_effect, g_effect):
        assert row["study_id"] == "PS001"
        assert row["cluster_id"] == "ML003"
        assert row["effect_unit_status"] == "g_admissible"
        assert row["independent_unit"] == "site"
        assert int(row["n_independent_fragmented"]) == 3
        assert int(row["n_independent_reference"]) == 2
        assert int(row["orientation_multiplier"]) == -1

    assert abs(float(c_effect["raw_effect"]) - c_g) < 1e-9
    assert abs(float(c_effect["raw_variance"]) - c_var) < 1e-9
    assert abs(float(c_effect["oriented_effect"]) + c_g) < 1e-9
    assert abs(float(c_effect["oriented_variance"]) - c_var) < 1e-9
    assert abs(float(g_effect["raw_effect"]) - g_g) < 1e-9
    assert abs(float(g_effect["raw_variance"]) - g_var) < 1e-9
    assert abs(float(g_effect["oriented_effect"]) + g_g) < 1e-9
    assert abs(float(g_effect["oriented_variance"]) - g_var) < 1e-9

    # The covariance proxy uses oriented biological-support values: -r_p and -Sp.
    c_support = {p: -raw_c[p] for p in pops}
    g_support = {p: -raw_g[p] for p in pops}
    c_centered = centered(c_support, habitat, pops)
    g_centered = centered(g_support, habitat, pops)
    r_cg = pearson(c_centered, g_centered)
    expected_cov = r_cg * math.sqrt(c_var * g_var)

    cov_rows = rows(COV)
    assert len(cov_rows) == 4
    by_pair = {(r["endpoint_i"], r["endpoint_j"]): r for r in cov_rows}
    assert set(by_pair) == {(a, b) for a in ENDPOINTS for b in ENDPOINTS}
    for a in ENDPOINTS:
        for b in ENDPOINTS:
            row = by_pair[(a, b)]
            assert row["cluster_id"] == "ML003"
            assert row["study_id"] == "PS001"
            assert int(row["n_paired_units"]) == 5
            assert row["covariance_status"] == "proxy_reconstructed"

    off = by_pair[("C_paternity_correlation", "Gadult_Sp")]
    assert abs(float(off["correlation_proxy"]) - r_cg) < 1e-9
    assert abs(float(off["sampling_covariance"]) - expected_cov) < 1e-9
    assert abs(float(by_pair[("Gadult_Sp", "C_paternity_correlation")]["sampling_covariance"]) - expected_cov) < 1e-9
    assert abs(float(by_pair[("C_paternity_correlation", "C_paternity_correlation")]["sampling_covariance"]) - c_var) < 1e-9
    assert abs(float(by_pair[("Gadult_Sp", "Gadult_Sp")]["sampling_covariance"]) - g_var) < 1e-9
    assert c_var * g_var - expected_cov**2 > 0

    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    ml003 = registry["ML003"]
    assert ml003["cluster_status"] == "admissible_multilayer_cluster"
    assert set(ml003["admissible_primary_layers"].split(";")) == {"C", "G_adult"}
    assert int(ml003["n_admissible_primary_effects"]) == 2
    assert ml003["covariance_status"] == "proxy_reconstructed_from_five_sites"

    print(
        "PS001 Spondias multilayer cluster: PASS; "
        f"C oriented g={-c_g:.6f}, G_adult(Sp) oriented g={-g_g:.6f}, "
        f"r_proxy={r_cg:.6f}; ML003 admitted as one C/G_adult cluster over five paired sites"
    )


if __name__ == "__main__":
    main()
