from __future__ import annotations

import csv
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "evidence/meta_extraction/PS001_spondias_paternity_site_table_v1.csv"
EFFECT = ROOT / "evidence/meta_extraction/PS001_spondias_site_effects_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def hedges_g_metafor_ls(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    df = n1 + n2 - 2
    s1, s2 = stats.stdev(fragmented), stats.stdev(reference)
    pooled = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / df)
    d = (stats.mean(fragmented) - stats.mean(reference)) / pooled
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    variance = 1 / n1 + 1 / n2 + g**2 / (2 * (n1 + n2))
    return g, variance


def main() -> None:
    site = rows(SITE)
    effect_rows = rows(EFFECT)
    assert len(site) == 5
    assert len(effect_rows) == 1
    assert sum(r["habitat"] == "FRA" for r in site) == 3
    assert sum(r["habitat"] == "CON" for r in site) == 2
    assert {r["population"] for r in site} == {"Careyes", "Chamela", "Mesa", "Nacastillo", "Ranchitos"}

    fragmented = [float(r["multilocus_correlated_paternity_rp"]) for r in site if r["habitat"] == "FRA"]
    reference = [float(r["multilocus_correlated_paternity_rp"]) for r in site if r["habitat"] == "CON"]
    g, variance = hedges_g_metafor_ls(fragmented, reference)

    row = effect_rows[0]
    assert row["study_id"] == "PS001"
    assert row["cluster_id"] == "ML003"
    assert row["endpoint_id"] == "C_paternity_correlation"
    assert row["layer"] == "C_movement_connectivity"
    assert row["effect_unit_status"] == "g_admissible"
    assert row["independent_unit"] == "site"
    assert int(row["n_independent_fragmented"]) == 3
    assert int(row["n_independent_reference"]) == 2
    assert int(row["orientation_multiplier"]) == -1
    assert abs(float(row["fragmented_mean"]) - stats.mean(fragmented)) < 1e-9
    assert abs(float(row["fragmented_sd"]) - stats.stdev(fragmented)) < 1e-9
    assert abs(float(row["reference_mean"]) - stats.mean(reference)) < 1e-9
    assert abs(float(row["reference_sd"]) - stats.stdev(reference)) < 1e-9
    assert abs(float(row["raw_effect"]) - g) < 1e-9
    assert abs(float(row["raw_variance"]) - variance) < 1e-9
    assert abs(float(row["oriented_effect"]) + g) < 1e-9
    assert abs(float(row["oriented_variance"]) - variance) < 1e-9

    print(
        "PS001 Spondias paternity effect: PASS; "
        f"5 independent sites, raw g={g:.6f}, oriented g={-g:.6f}, "
        f"var={variance:.6f}; ML003 has one admissible C layer only"
    )


if __name__ == "__main__":
    main()
