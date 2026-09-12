from __future__ import annotations

import csv
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv"

GROUPS = {
    "F": ([5.20, 5.50, 5.10], [13.58, 20.30, 14.23, 15.60, 14.68, 16.75], 1),
    "C": ([9.38, 11.11, 7.14], [28.68, 32.02, 28.34, 27.49, 30.53, 28.64], 1),
    "G_adult_Ho": ([0.418, 0.422, 0.382], [0.784, 0.774, 0.789, 0.776, 0.782, 0.777], 1),
    "G_adult_FIS": ([0.25, 0.28, 0.22], [-0.12, -0.04, -0.07, -0.02, -0.08, -0.04], -1),
}


def hedges_g_metafor_ls(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    """Hedges g and metafor escalc(SMD, vtype='LS') sampling variance."""
    n1, n2 = len(fragmented), len(reference)
    m1, m2 = stats.mean(fragmented), stats.mean(reference)
    s1, s2 = stats.stdev(fragmented), stats.stdev(reference)
    df = n1 + n2 - 2
    pooled = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / df)
    d = (m1 - m2) / pooled
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    variance = 1 / n1 + 1 / n2 + g**2 / (2 * (n1 + n2))
    return g, variance


def main() -> None:
    with OUT.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 4
    by_endpoint = {r["endpoint"]: r for r in rows}

    mapping = {
        "fruit_set": "F",
        "pollen_immigration_rate": "C",
        "observed_heterozygosity": "G_adult_Ho",
        "fixation_index_FIS": "G_adult_FIS",
    }
    for endpoint, key in mapping.items():
        row = by_endpoint[endpoint]
        frag, ref, orientation = GROUPS[key]
        g, variance = hedges_g_metafor_ls(frag, ref)
        assert int(row["n_fragmented"]) == 3
        assert int(row["n_reference"]) == 6
        assert row["fragmented_group"] == "C;F;G"
        assert row["reference_group"] == "A;B;D;E;H;I"
        assert row["effect_unit_status"] == "g_admissible"
        assert abs(float(row["raw_effect"]) - g) < 1e-9
        assert abs(float(row["raw_variance"]) - variance) < 1e-9
        assert int(row["orientation_multiplier"]) == orientation
        assert abs(float(row["oriented_effect"]) - g * orientation) < 1e-9
        assert abs(float(row["oriented_variance"]) - variance) < 1e-9

    assert by_endpoint["observed_heterozygosity"]["primary_or_sensitivity"] == "primary"
    assert by_endpoint["fixation_index_FIS"]["primary_or_sensitivity"] == "sensitivity"
    assert {r["layer"] for r in rows if r["primary_or_sensitivity"] == "primary"} == {"C", "F", "G_adult"}

    print("PS003 Serapias predefined 3-vs-6 multilayer contrast: PASS; metafor SMD vtype=LS variance locked")


if __name__ == "__main__":
    main()
