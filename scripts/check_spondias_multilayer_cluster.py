from __future__ import annotations

import csv
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C_SITE = ROOT / "evidence/meta_extraction/PS001_spondias_paternity_site_table_v1.csv"
SP_SITE = ROOT / "evidence/meta_extraction/PS001_spondias_adult_sgs_site_table_v1.csv"
GEN_SITE = ROOT / "evidence/meta_extraction/PS001_spondias_appendixB_genetic_site_table_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/PS001_spondias_site_effects_v1.csv"
PAIR_COV = ROOT / "evidence/meta_extraction/PS001_spondias_primary_pairwise_covariance_v2.csv"
CONTRASTS = ROOT / "evidence/meta_extraction/PS001_spondias_cohort_contrasts_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-13_COHORT_DEPENDENCE.md"

PRIMARY = ["C_paternity_correlation", "Gadult_Ho", "Gjuvenile_Ho", "Gseed_Ho"]
Z95 = 1.959963984540054


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


def matrix_rank(matrix: list[list[float]], tol: float = 1e-10) -> int:
    a = [row[:] for row in matrix]
    m, n = len(a), len(a[0])
    rank = 0
    col = 0
    while rank < m and col < n:
        pivot = max(range(rank, m), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) <= tol:
            col += 1
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pivot_value = a[rank][col]
        for j in range(col, n):
            a[rank][j] /= pivot_value
        for r in range(m):
            if r == rank:
                continue
            factor = a[r][col]
            if abs(factor) <= tol:
                continue
            for j in range(col, n):
                a[r][j] -= factor * a[rank][j]
        rank += 1
        col += 1
    return rank


def main() -> None:
    for path in (C_SITE, SP_SITE, GEN_SITE, EFFECTS, PAIR_COV, CONTRASTS, REGISTRY, AMENDMENT):
        assert path.is_file(), path

    c_rows = rows(C_SITE)
    sp_rows = rows(SP_SITE)
    gen_rows = rows(GEN_SITE)
    assert len(c_rows) == len(sp_rows) == 5
    assert len(gen_rows) == 15

    c_by_pop = {r["population"]: r for r in c_rows}
    sp_by_pop = {r["population"]: r for r in sp_rows}
    pops = sorted(c_by_pop)
    assert set(pops) == set(sp_by_pop) == {"Careyes", "Chamela", "Mesa", "Nacastillo", "Ranchitos"}
    habitat = {p: c_by_pop[p]["habitat"] for p in pops}
    assert sum(habitat[p] == "FRA" for p in pops) == 3
    assert sum(habitat[p] == "CON" for p in pops) == 2

    gen_by_key = {(r["population"], r["developmental_stage"]): r for r in gen_rows}
    assert set(stage for _, stage in gen_by_key) == {"adult", "juvenile", "seed"}
    assert all((p, stage) in gen_by_key for p in pops for stage in ("adult", "juvenile", "seed"))
    assert all(gen_by_key[(p, "adult")]["habitat"] == habitat[p] for p in pops)

    raw = {
        "C_paternity_correlation": {p: float(c_by_pop[p]["multilocus_correlated_paternity_rp"]) for p in pops},
        "Gadult_Ho": {p: float(gen_by_key[(p, "adult")]["Ho"]) for p in pops},
        "Gjuvenile_Ho": {p: float(gen_by_key[(p, "juvenile")]["Ho"]) for p in pops},
        "Gseed_Ho": {p: float(gen_by_key[(p, "seed")]["Ho"]) for p in pops},
        "Gadult_Sp": {p: float(sp_by_pop[p]["adult_spatial_genetic_structure_Sp"]) for p in pops},
        "Gadult_Fis": {p: float(gen_by_key[(p, "adult")]["Fis"]) for p in pops},
        "Gjuvenile_Fis": {p: float(gen_by_key[(p, "juvenile")]["Fis"]) for p in pops},
        "Gseed_Fis": {p: float(gen_by_key[(p, "seed")]["Fis"]) for p in pops},
    }
    orientation = {
        "C_paternity_correlation": -1,
        "Gadult_Ho": 1,
        "Gjuvenile_Ho": 1,
        "Gseed_Ho": 1,
        "Gadult_Sp": -1,
        "Gadult_Fis": -1,
        "Gjuvenile_Fis": -1,
        "Gseed_Fis": -1,
    }
    role = {
        "C_paternity_correlation": "primary",
        "Gadult_Ho": "primary",
        "Gjuvenile_Ho": "primary",
        "Gseed_Ho": "primary",
        "Gadult_Sp": "sensitivity_structure",
        "Gadult_Fis": "sensitivity_metric",
        "Gjuvenile_Fis": "sensitivity_metric",
        "Gseed_Fis": "sensitivity_metric",
    }

    frag = [p for p in pops if habitat[p] == "FRA"]
    ref = [p for p in pops if habitat[p] == "CON"]
    effects = {r["endpoint_id"]: r for r in rows(EFFECTS)}
    assert set(effects) == set(raw)

    variances: dict[str, float] = {}
    oriented_effects: dict[str, float] = {}
    support_values: dict[str, dict[str, float]] = {}
    for endpoint, values in raw.items():
        g, variance = hedges_g_metafor_ls([values[p] for p in frag], [values[p] for p in ref])
        row = effects[endpoint]
        assert row["study_id"] == "PS001"
        assert row["cluster_id"] == "ML003"
        assert row["effect_unit_status"] == "g_admissible"
        assert row["analysis_role"] == role[endpoint]
        assert row["independent_unit"] == "site"
        assert int(row["n_independent_fragmented"]) == 3
        assert int(row["n_independent_reference"]) == 2
        assert int(row["orientation_multiplier"]) == orientation[endpoint]
        assert abs(float(row["raw_effect"]) - g) < 1e-9
        assert abs(float(row["raw_variance"]) - variance) < 1e-9
        assert abs(float(row["oriented_effect"]) - g * orientation[endpoint]) < 1e-9
        assert abs(float(row["oriented_variance"]) - variance) < 1e-9
        variances[endpoint] = variance
        oriented_effects[endpoint] = g * orientation[endpoint]
        support_values[endpoint] = {p: values[p] * orientation[endpoint] for p in pops}

    assert {e for e in effects if effects[e]["analysis_role"] == "primary"} == set(PRIMARY)
    assert effects["Gadult_Ho"]["layer"] == "G_adult"
    assert effects["Gadult_Sp"]["analysis_role"] == "sensitivity_structure"
    assert all(effects[e]["analysis_role"] == "sensitivity_metric" for e in ("Gadult_Fis", "Gjuvenile_Fis", "Gseed_Fis"))

    # Four co-primary outcomes on five sites split across two groups have only
    # 5-2=3 within-group residual dimensions. Store pairwise covariance terms,
    # but never force the resulting 4x4 proxy to be invertible.
    centered_vectors = {e: centered(support_values[e], habitat, pops) for e in PRIMARY}
    cov_rows = rows(PAIR_COV)
    assert len(cov_rows) == 16
    by_pair = {(r["endpoint_i"], r["endpoint_j"]): r for r in cov_rows}
    assert set(by_pair) == {(a, b) for a in PRIMARY for b in PRIMARY}
    matrix: list[list[float]] = []
    for a in PRIMARY:
        matrix_row: list[float] = []
        for b in PRIMARY:
            r_expected = pearson(centered_vectors[a], centered_vectors[b])
            cov_expected = r_expected * math.sqrt(variances[a] * variances[b])
            row = by_pair[(a, b)]
            assert row["covariance_status"] == "proxy_pairwise_low_rank"
            assert int(row["n_paired_units"]) == 5
            assert abs(float(row["correlation_proxy"]) - r_expected) < 1e-9
            assert abs(float(row["sampling_covariance"]) - cov_expected) < 1e-9
            assert abs(float(row["marginal_variance_i"]) - variances[a]) < 1e-9
            assert abs(float(row["marginal_variance_j"]) - variances[b]) < 1e-9
            matrix_row.append(float(row["sampling_covariance"]))
        matrix.append(matrix_row)
    assert matrix_rank(matrix) == 3, matrix

    # Cohort contrasts are lower-dimensional and therefore remain auditable.
    contrasts = {r["contrast"]: r for r in rows(CONTRASTS)}
    assert set(contrasts) == {"juvenile_vs_adult_Ho", "seed_vs_adult_Ho"}
    for contrast, later in (("juvenile_vs_adult_Ho", "Gjuvenile_Ho"), ("seed_vs_adult_Ho", "Gseed_Ho")):
        adult = "Gadult_Ho"
        cov = float(by_pair[(adult, later)]["sampling_covariance"])
        delta = oriented_effects[later] - oriented_effects[adult]
        variance = variances[later] + variances[adult] - 2 * cov
        se = math.sqrt(variance)
        lo = delta - Z95 * se
        hi = delta + Z95 * se
        row = contrasts[contrast]
        assert abs(float(row["covariance"]) - cov) < 1e-9
        assert abs(float(row["delta_later_minus_adult"]) - delta) < 1e-9
        assert abs(float(row["delta_variance"]) - variance) < 1e-9
        assert abs(float(row["delta_se"]) - se) < 1e-9
        assert abs(float(row["ci95_low"]) - lo) < 1e-9
        assert abs(float(row["ci95_high"]) - hi) < 1e-9
        assert lo < 0 < hi, (contrast, lo, hi)

    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    ml003 = registry["ML003"]
    assert ml003["cluster_status"] == "admissible_multilayer_cluster"
    assert set(ml003["admissible_primary_layers"].split(";")) == {"C", "G_adult", "G_offspring"}
    assert int(ml003["n_admissible_primary_effects"]) == 4
    assert ml003["covariance_status"] == "proxy_pairwise_low_rank_from_five_sites"

    amendment = AMENDMENT.read_text(encoding="utf-8")
    assert "proxy_pairwise_low_rank" in amendment
    assert "n-g" in amendment
    assert "H_O" in amendment and "F_IS" in amendment
    assert "does not by itself establish a cohort lag" in amendment

    print(
        "PS001 Spondias cohort cluster: PASS; "
        f"primary C={oriented_effects['C_paternity_correlation']:.6f}, "
        f"adult_Ho={oriented_effects['Gadult_Ho']:.6f}, "
        f"juvenile_Ho={oriented_effects['Gjuvenile_Ho']:.6f}, "
        f"seed_Ho={oriented_effects['Gseed_Ho']:.6f}; "
        "4x4 proxy rank=3 as expected, pairwise cohort contrasts cross zero"
    )


if __name__ == "__main__":
    main()
