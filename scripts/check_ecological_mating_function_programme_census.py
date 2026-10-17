from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "evidence/meta_extraction/ecological_mating_function_programme_census_v1.csv"
SERA_E = ROOT / "evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv"
SERA_C = ROOT / "evidence/meta_extraction/PS003_serapias_primary_covariance_v1.csv"
BROS_E = ROOT / "evidence/meta_extraction/PS004_brosimum_extraction_v1.csv"
BROS_C = ROOT / "evidence/meta_extraction/PS004_brosimum_primary_covariance_v1.csv"
SOC_E = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_effects_v1.csv"
SOC_C = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_primary_covariance_v1.csv"
ACER_E = ROOT / "evidence/meta_extraction/phase2_cf01_acer_miyabei_gradient_effects_v1.csv"
ACER_C = ROOT / "evidence/meta_extraction/phase2_cf01_acer_miyabei_gradient_covariance_v1.json"

TOL = 5e-9


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def covariance(path: Path, a: str, b: str) -> float:
    r = next(x for x in rows(path) if x["endpoint_i"] == a and x["endpoint_j"] == b)
    return float(r["sampling_covariance"])


def p_two(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def pair(process: float, function: float, vp: float, vf: float, cov: float) -> tuple[float, float]:
    delta = process - function
    var = vp + vf - 2.0 * cov
    assert var > 0
    return delta, p_two(delta / math.sqrt(var))


def main() -> None:
    census = rows(CENSUS)
    assert len(census) == 4
    by = {r["programme_id"]: r for r in census}
    assert set(by) == {"ML001", "ML002", "ML014", "P2_CF01_ACER_MIYABEI_2014"}

    sera = rows(SERA_E)
    se_p = next(r for r in sera if r["endpoint"] == "pollen_immigration_rate" and r["primary_or_sensitivity"] == "primary")
    se_f = next(r for r in sera if r["endpoint"] == "fruit_set" and r["primary_or_sensitivity"] == "primary")
    sd, sp = pair(
        float(se_p["oriented_effect"]), float(se_f["oriented_effect"]),
        float(se_p["oriented_variance"]), float(se_f["oriented_variance"]),
        covariance(SERA_C, "C_pollen_immigration", "F_fruit_set"),
    )
    assert abs(float(by["ML001"]["process_minus_function"]) - sd) < TOL
    assert abs(float(by["ML001"]["pair_p"]) - sp) < TOL
    assert abs(float(by["ML001"]["programme_adjusted_p"]) - min(1.0, 3.0 * sp)) < TOL

    bros = rows(BROS_E)
    bp = next(r for r in bros if r["endpoint_id"] == "C_paternity_rp")
    bf = next(r for r in bros if r["endpoint_id"] == "F_progeny_vigour")
    bd, bpp = pair(
        float(bp["oriented_effect"]), float(bf["oriented_effect"]),
        float(bp["oriented_variance"]), float(bf["oriented_variance"]),
        covariance(BROS_C, "C_paternity_rp", "F_TPDW"),
    )
    assert abs(float(by["ML002"]["process_minus_function"]) - bd) < TOL
    assert abs(float(by["ML002"]["pair_p"]) - bpp) < TOL

    soc = rows(SOC_E)
    gp = next(r for r in soc if r["endpoint_id"] == "Gmating_correlated_paternity_rp")
    gf = next(r for r in soc if r["endpoint_id"] == "F_family_growth")
    gd, gpp = pair(
        float(gp["oriented_effect"]), float(gf["oriented_effect"]),
        float(gp["oriented_variance"]), float(gf["oriented_variance"]),
        covariance(SOC_C, "Gmating_correlated_paternity_rp", "F_family_growth"),
    )
    assert abs(float(by["ML014"]["process_minus_function"]) - gd) < TOL
    assert abs(float(by["ML014"]["pair_p"]) - gpp) < TOL

    acer_e = rows(ACER_E)
    ap = next(r for r in acer_e if r["endpoint_role"] == "C_primary")
    af = next(r for r in acer_e if r["endpoint_role"] == "F_primary")
    ac = json.loads(ACER_C.read_text(encoding="utf-8"))
    ad, app = pair(
        float(ap["fisher_z"]), float(af["fisher_z"]),
        float(ap["variance"]), float(af["variance"]), float(ac["cov_CF"]),
    )
    assert abs(float(by["P2_CF01_ACER_MIYABEI_2014"]["process_minus_function"]) - ad) < TOL
    assert abs(float(by["P2_CF01_ACER_MIYABEI_2014"]["pair_p"]) - app) < TOL

    resolved = [r for r in census if r["resolved_mismatch"] == "yes"]
    unresolved = [r for r in census if r["resolved_mismatch"] == "no"]
    assert len(resolved) == 1
    assert len(unresolved) == 3
    assert resolved[0]["programme_id"] == "ML001"
    assert resolved[0]["resolved_direction"] == "process_more_negative_than_F"
    assert sum(float(r["process_minus_function"]) < 0 for r in census) == 3
    assert sum(float(r["process_minus_function"]) > 0 for r in census) == 1

    print(
        "ECOLOGICAL_MATING_FUNCTION_CENSUS_OK "
        "programmes=4 resolved=1 unresolved=3 "
        "resolved_process_more_negative=1 resolved_F_more_negative=0 "
        "point_process_more_negative=3 point_F_more_negative=1"
    )


if __name__ == "__main__":
    main()
