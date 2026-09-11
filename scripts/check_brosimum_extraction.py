from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "evidence/meta_extraction/PS004_brosimum_extraction_v1.csv"


def main() -> None:
    with PATH.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) >= 8
    rp = next(r for r in rows if r["endpoint_id"] == "C_paternity_rp")
    assert rp["effect_unit_status"] == "g_admissible"
    assert rp["independent_unit"] == "site"
    assert int(rp["n_independent_fragmented"]) == 3
    assert int(rp["n_independent_reference"]) == 3

    reference = [0.106, 0.164, 0.107]
    fragmented = [0.246, 0.208, 0.191]
    n_f, n_r = len(fragmented), len(reference)
    sd_f, sd_r = stdev(fragmented), stdev(reference)
    pooled = math.sqrt(((n_f - 1) * sd_f**2 + (n_r - 1) * sd_r**2) / (n_f + n_r - 2))
    d = (mean(fragmented) - mean(reference)) / pooled
    df = n_f + n_r - 2
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    var_d = (n_f + n_r) / (n_f * n_r) + d**2 / (2 * df)
    var_g = j**2 * var_d

    assert abs(float(rp["raw_effect"]) - g) < 1e-9
    assert abs(float(rp["raw_variance"]) - var_g) < 1e-9
    assert int(rp["orientation_multiplier"]) == -1
    assert abs(float(rp["oriented_effect"]) + g) < 1e-9
    assert abs(float(rp["oriented_variance"]) - var_g) < 1e-9

    # Derived effective-sire number is the reciprocal of the same rp signal and
    # must not be admitted as a second independent effect.
    nep = next(r for r in rows if r["endpoint_id"] == "C_effective_sires")
    assert nep["effect_unit_status"] == "descriptive_only"
    assert nep["source_observation_id"] == rp["source_observation_id"]

    # Lower-level genetic and paternity-event summaries remain outside naive g.
    for endpoint in ("C_pollen_distance", "Gadult_Ho", "Goffspring_Ho", "Goffspring_F"):
        row = next(r for r in rows if r["endpoint_id"] == endpoint)
        assert row["effect_unit_status"] == "raw_reanalysis_required"

    print(
        "PS004 Brosimum extraction audit: PASS; "
        f"site-level rp Hedges g raw={g:.6f}, oriented={-g:.6f}, SE={math.sqrt(var_g):.6f}; "
        "all nested/locus summaries blocked from naive standardisation"
    )


if __name__ == "__main__":
    main()
