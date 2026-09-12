from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "evidence/meta_extraction/PS004_brosimum_extraction_v1.csv"
SITE = ROOT / "evidence/meta_extraction/PS004_brosimum_site_table_v1.csv"


def hedges_g_metafor_ls(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n_f, n_r = len(fragmented), len(reference)
    sd_f, sd_r = stdev(fragmented), stdev(reference)
    df = n_f + n_r - 2
    pooled = math.sqrt(((n_f - 1) * sd_f**2 + (n_r - 1) * sd_r**2) / df)
    d = (mean(fragmented) - mean(reference)) / pooled
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    variance = 1 / n_f + 1 / n_r + g**2 / (2 * (n_f + n_r))
    return g, variance


def main() -> None:
    with PATH.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    with SITE.open(newline="", encoding="utf-8") as fh:
        sites = list(csv.DictReader(fh))
    assert len(rows) >= 8
    assert len(sites) == 6
    assert sum(r["habitat"] == "FRA" for r in sites) == 3
    assert sum(r["habitat"] == "CON" for r in sites) == 3

    by_id = {r["endpoint_id"]: r for r in rows}

    c_fragmented = [float(r["C_paternity_rp"]) for r in sites if r["habitat"] == "FRA"]
    c_reference = [float(r["C_paternity_rp"]) for r in sites if r["habitat"] == "CON"]
    c_g_raw, c_var = hedges_g_metafor_ls(c_fragmented, c_reference)
    rp = by_id["C_paternity_rp"]
    assert rp["effect_unit_status"] == "g_admissible"
    assert rp["independent_unit"] == "site"
    assert int(rp["n_independent_fragmented"]) == 3
    assert int(rp["n_independent_reference"]) == 3
    assert abs(float(rp["raw_effect"]) - c_g_raw) < 1e-9
    assert abs(float(rp["raw_variance"]) - c_var) < 1e-9
    assert int(rp["orientation_multiplier"]) == -1
    assert abs(float(rp["oriented_effect"]) + c_g_raw) < 1e-9
    assert abs(float(rp["oriented_variance"]) - c_var) < 1e-9

    f_fragmented = [float(r["F_TPDW_site_mean"]) for r in sites if r["habitat"] == "FRA"]
    f_reference = [float(r["F_TPDW_site_mean"]) for r in sites if r["habitat"] == "CON"]
    f_g, f_var = hedges_g_metafor_ls(f_fragmented, f_reference)
    vigor = by_id["F_progeny_vigour"]
    assert vigor["effect_unit_status"] == "g_admissible"
    assert vigor["independent_unit"] == "site"
    assert int(vigor["n_independent_fragmented"]) == 3
    assert int(vigor["n_independent_reference"]) == 3
    assert abs(float(vigor["raw_effect"]) - f_g) < 1e-9
    assert abs(float(vigor["raw_variance"]) - f_var) < 1e-9
    assert int(vigor["orientation_multiplier"]) == 1
    assert abs(float(vigor["oriented_effect"]) - f_g) < 1e-9
    assert abs(float(vigor["oriented_variance"]) - f_var) < 1e-9

    # Derived effective-sire number is the reciprocal of the same rp signal and
    # must not be admitted as a second independent effect.
    nep = by_id["C_effective_sires"]
    assert nep["effect_unit_status"] == "descriptive_only"
    assert nep["source_observation_id"] == rp["source_observation_id"]

    # Genetic raw-data recovery has started but is deliberately not promoted
    # until raw-genotype summaries reproduce the publication-level QA targets.
    for endpoint in ("Gadult_Ho", "Goffspring_Ho", "Goffspring_F"):
        assert by_id[endpoint]["effect_unit_status"] == "raw_reanalysis_required"

    assert by_id["C_pollen_distance"]["effect_unit_status"] == "raw_reanalysis_required"

    print(
        "PS004 Brosimum extraction audit: PASS; "
        f"C oriented g={-c_g_raw:.6f} var={c_var:.6f}; "
        f"F TPDW g={f_g:.6f} var={f_var:.6f}; "
        "G remains raw-QA pending"
    )


if __name__ == "__main__":
    main()
