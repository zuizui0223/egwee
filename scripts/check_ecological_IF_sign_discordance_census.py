from __future__ import annotations

import csv
import json
import math
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "evidence/meta_extraction/ecological_IF_sign_discordance_census_v1.csv"

ML020 = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_effects_v1.csv"
SEVEN = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_direct_effects_v1.csv"
BERG = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_effects_v1.csv"
BERG_COV = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_covariance_v1.json"
WANDOO = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv"
WANDOO_COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_covariance_v1.csv"
CARDIO = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_effects_v1.csv"
ZURICH = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_gradient_effects_v1.csv"
ZURICH_COV = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_gradient_covariance_v1.json"
MILK = ROOT / "evidence/meta_extraction/phase2_cf01_milkweed_urban_gradient_effects_v1.csv"
MILK_COV = ROOT / "evidence/meta_extraction/phase2_cf01_milkweed_urban_gradient_covariance_v1.json"
PRITCH = ROOT / "evidence/meta_extraction/phase2_cf01_pritchard_gradient_effects_v1.csv"

TOL = 5e-8


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def p_two(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def opposite(a: float, b: float) -> bool:
    return a * b < 0


def pair_count(records: list[dict[str, str]], group: str, layer: str, effect: str) -> tuple[int, int]:
    by: dict[str, dict[str, float]] = {}
    for r in records:
        by.setdefault(r[group], {})[r[layer]] = float(r[effect])
    assert all(len(x) == 2 for x in by.values())
    return len(by), sum(opposite(*list(x.values())) for x in by.values())


def lnrr_var(mf: float, sdf: float, nf: int, mr: float, sdr: float, nr: int) -> float:
    return sdf**2 / (nf * mf**2) + sdr**2 / (nr * mr**2)


def main() -> None:
    census = rows(CENSUS)
    by = {r["programme_id"]: r for r in census}
    assert len(census) == 8
    assert len(by) == 8

    ml020 = rows(ML020)
    n, opp = pair_count(ml020, "species", "layer", "oriented_effect")
    assert (n, opp) == (3, 0)

    seven = [r for r in rows(SEVEN) if r["primary_or_sensitivity"] == "primary"]
    n, opp = pair_count(seven, "species", "layer", "hedges_g")
    assert (n, opp) == (3, 2)

    berg = [r for r in rows(BERG) if r["primary_or_sensitivity"] == "primary"]
    n, opp = pair_count(berg, "panel_id", "layer", "hedges_g")
    assert (n, opp) == (4, 1)

    w = {r["layer"]: float(r["oriented_effect"]) for r in rows(WANDOO)}
    assert opposite(w["I"], w["F"])

    cardio = {
        r["layer"]: float(r["fisher_z"])
        for r in rows(CARDIO)
        if r["primary_or_sensitivity"] == "primary"
    }
    assert not opposite(cardio["I_interaction"], cardio["F_reproductive_function"])

    zurich = rows(ZURICH)
    n, opp = pair_count(zurich, "phytometer", "layer", "oriented_effect")
    assert (n, opp) == (4, 1)

    milk = {
        r["layer"]: float(r["oriented_effect"])
        for r in rows(MILK)
        if r["analysis_frame"] == "primary_source_code_nonzero"
    }
    assert opposite(milk["I"], milk["F"])

    pritch = {
        r["layer"]: float(r["fisher_z"])
        for r in rows(PRITCH)
        if r["primary_or_sensitivity"] == "primary"
    }
    assert not opposite(pritch["I_interaction"], pritch["F_reproductive_function"])

    expected_opp = {
        "ML020": 0,
        "P2_CF01_SEVENELLO_2026": 2,
        "P2_CF01_BERGSDORF_KAKAMEGA_2006": 1,
        "ML015": 1,
        "P2_CF01_CARDIOPETALUM_2012": 0,
        "P2_CF01_ZURICH_2026": 1,
        "P2_CF01_MILKWEED_URBAN_2023": 1,
        "P2_CF01_PRITCHARD_2005": 0,
    }
    for pid, k in expected_opp.items():
        assert int(by[pid]["n_opposite_sign_primary_panels"]) == k
        assert by[pid]["has_opposite_sign_primary_panel"] == ("yes" if k else "no")

    # Registered resolved opposite-sign programme: Bergsdorf/Kakamega.
    berg_cov = json.loads(BERG_COV.read_text(encoding="utf-8"))
    assert abs(float(berg_cov["programme_internal_gate"]["p_programme"]) - 0.0065353881319876956) < TOL
    ap = next(r for r in berg if r["panel_id"] == "AP_2001" and r["layer"] == "I_interaction")
    apf = next(r for r in berg if r["panel_id"] == "AP_2001" and r["layer"] == "F_reproductive_function")
    assert opposite(float(ap["hedges_g"]), float(apf["hedges_g"]))

    # Acanthopale remains opposite-sign and resolved on lnRR using the same residual-rho proxy.
    nf, nr = int(ap["n_fragment"]), int(ap["n_main"])
    ei = math.log(float(ap["mean_fragment"]) / float(ap["mean_main"]))
    ef = math.log(float(apf["mean_fragment"]) / float(apf["mean_main"]))
    vi = lnrr_var(float(ap["mean_fragment"]), float(ap["sd_fragment"]), nf,
                  float(ap["mean_main"]), float(ap["sd_main"]), nr)
    vf = lnrr_var(float(apf["mean_fragment"]), float(apf["sd_fragment"]), nf,
                  float(apf["mean_main"]), float(apf["sd_main"]), nr)
    rho = float(berg_cov["panel_blocks"]["AP_2001"]["residual_rho_IF"])
    cov = rho * math.sqrt(vi * vf)
    z = (ei - ef) / math.sqrt(vi + vf - 2.0 * cov)
    p_ap_lnrr = p_two(z)
    p_programme_lnrr = min(1.0, 4.0 * p_ap_lnrr)
    assert ei > 0 and ef < 0
    assert abs(p_ap_lnrr - 0.00012259006684100862) < TOL
    assert p_programme_lnrr < 0.001

    # Registered resolved opposite-sign programme: Eucalyptus wandoo.
    wcov = {
        (r["endpoint_i"], r["endpoint_j"]): float(r["sampling_covariance"])
        for r in rows(WANDOO_COV)
    }
    we = {
        r["endpoint"]: (float(r["oriented_effect"]), float(r["oriented_variance"]))
        for r in rows(WANDOO)
    }
    names = list(we)
    ps = []
    if_p = None
    key = {
        "pollen_tubes_at_base_of_style": "I_pollen_tubes",
        "seeds_per_fruit_y2": "F_seeds_per_fruit_y2",
        "unbiased_expected_heterozygosity_He": "G_adult_He",
    }
    for a, b in combinations(names, 2):
        ea, va = we[a]
        eb, vb = we[b]
        cov = wcov[(key[a], key[b])]
        pp = p_two((ea - eb) / math.sqrt(va + vb - 2.0 * cov))
        ps.append(pp)
        if {a, b} == {"pollen_tubes_at_base_of_style", "seeds_per_fruit_y2"}:
            if_p = pp
    assert if_p is not None
    w_programme_p = min(1.0, 3.0 * min(ps))
    assert if_p < 0.001
    assert abs(w_programme_p - 0.00256953) < 5e-6

    # Opposite-sign but unresolved programmes.
    seven_p = json.loads((ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_direct_covariance_v1.json").read_text(encoding="utf-8"))
    assert float(seven_p["programme_internal_bonferroni_p"]) == 1.0

    zur = json.loads(ZURICH_COV.read_text(encoding="utf-8"))
    zps = [float(v["I_minus_F"]["p_two_sided"]) for v in zur["phytometer_blocks"].values()]
    assert min(1.0, 4.0 * min(zps)) > 0.05

    mk = json.loads(MILK_COV.read_text(encoding="utf-8"))["primary_source_code_nonzero"]["I_minus_F"]
    milk_p = p_two(float(mk["z"]))
    assert milk_p > 0.05

    programmes_any = [r for r in census if r["has_opposite_sign_primary_panel"] == "yes"]
    programmes_resolved = [r for r in census if r["resolved_opposite_sign_panel"] == "yes"]
    assert len(programmes_any) == 5
    assert {r["programme_id"] for r in programmes_resolved} == {
        "ML015", "P2_CF01_BERGSDORF_KAKAMEGA_2006"
    }

    print(
        "IF_SIGN_DISCORDANCE_CENSUS_OK "
        "programmes=8 any_opposite_sign=5 resolved_opposite_sign=2 "
        f"Acanthopale_lnRR_pair_p={p_ap_lnrr:.9g} "
        f"Acanthopale_lnRR_programme_p={p_programme_lnrr:.9g} "
        f"Wandoo_programme_p={w_programme_p:.8g}"
    )


if __name__ == "__main__":
    main()
