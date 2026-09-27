from __future__ import annotations

import csv
import json
import math
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
ML020_E = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_effects_v1.csv"
ML020_C = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_covariance_v1.csv"
SEVEN = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_direct_covariance_v1.json"
BERG = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_covariance_v1.json"
WANDOO_E = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv"
WANDOO_C = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_covariance_v1.csv"
CARDIO = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_covariance_v1.json"
ZURICH = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_gradient_covariance_v1.json"
MILKWEED = ROOT / "evidence/meta_extraction/phase2_cf01_milkweed_urban_gradient_covariance_v1.json"
PRITCHARD = ROOT / "evidence/meta_extraction/phase2_cf01_pritchard_gradient_dependence_v1.json"

TOL = 5e-8


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def obj(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def p_two_sided(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def pair_p(e1: float, v1: float, e2: float, v2: float, cov: float) -> tuple[float, float]:
    delta = e1 - e2
    var = v1 + v2 - 2.0 * cov
    assert var > 0
    z = delta / math.sqrt(var)
    return delta, p_two_sided(z)


def ml020_programme_p() -> float:
    effects: dict[str, dict[str, tuple[float, float]]] = {}
    for r in rows(ML020_E):
        effects.setdefault(r["species"], {})[r["endpoint_id"]] = (
            float(r["oriented_effect"]), float(r["sampling_variance"])
        )
    cov = {
        (r["species"], r["endpoint_i"], r["endpoint_j"]): float(r["sampling_covariance"])
        for r in rows(ML020_C)
    }
    ps = []
    for species, vals in effects.items():
        ei, vi = vals["I_pollen_tubes"]
        ef, vf = vals["F_fruit_set"]
        delta, p = pair_p(ei, vi, ef, vf, cov[(species, "I_pollen_tubes", "F_fruit_set")])
        assert delta > 0
        ps.append(p)
    return min(1.0, 3.0 * min(ps))


def wandoo_programme_p() -> tuple[float, float]:
    erows = rows(WANDOO_E)
    eff = {r["layer"]: (float(r["oriented_effect"]), float(r["oriented_variance"])) for r in erows}
    cov = {(r["endpoint_i"], r["endpoint_j"]): float(r["sampling_covariance"]) for r in rows(WANDOO_C)}
    cov_name = {
        "I": "I_pollen_tubes",
        "F": "F_seeds_per_fruit_y2",
        "G_adult": "G_adult_He",
    }
    names = ["I", "F", "G_adult"]
    ps = []
    if_delta = None
    if_p = None
    for a, b in combinations(names, 2):
        delta, p = pair_p(
            eff[a][0], eff[a][1], eff[b][0], eff[b][1],
            cov[(cov_name[a], cov_name[b])],
        )
        ps.append(p)
        if {a, b} == {"I", "F"}:
            i = eff["I"]
            f = eff["F"]
            if_delta, if_p = pair_p(
                i[0], i[1], f[0], f[1],
                cov[("I_pollen_tubes", "F_seeds_per_fruit_y2")],
            )
    assert if_delta is not None and if_p is not None and if_delta > 0
    return min(1.0, 3.0 * min(ps)), if_delta


def main() -> None:
    census = rows(CENSUS)
    by = {r["programme_id"]: r for r in census}
    assert len(census) == 8
    assert len(by) == 8

    expected_p = {
        "ML020": ml020_programme_p(),
        "P2_CF01_SEVENELLO_2026": float(obj(SEVEN)["programme_internal_bonferroni_p"]),
        "P2_CF01_BERGSDORF_KAKAMEGA_2006": float(obj(BERG)["programme_internal_gate"]["p_programme"]),
        "P2_CF01_CARDIOPETALUM_2012": float(obj(CARDIO)["p_delta_two_sided"]),
    }

    wp, wdelta = wandoo_programme_p()
    expected_p["ML015"] = wp
    assert wdelta > 0

    zurich = obj(ZURICH)["phytometer_blocks"]
    zps = [float(v["I_minus_F"]["p_two_sided"]) for v in zurich.values()]
    expected_p["P2_CF01_ZURICH_2026"] = min(1.0, 4.0 * min(zps))

    milk = obj(MILKWEED)["primary_source_code_nonzero"]["I_minus_F"]
    expected_p["P2_CF01_MILKWEED_URBAN_2023"] = p_two_sided(float(milk["z"]))
    assert float(milk["delta"]) < 0

    for pid, p in expected_p.items():
        stored = float(by[pid]["programme_adjusted_p"])
        assert abs(stored - p) < TOL, (pid, stored, p)

    assert obj(PRITCHARD)["paired_covariance_reconstructable"] is False
    assert by["P2_CF01_PRITCHARD_2005"]["if_pair_testable"] == "no"
    assert by["P2_CF01_PRITCHARD_2005"]["resolved_if_mismatch"] == "not_testable"

    testable = [r for r in census if r["if_pair_testable"] == "yes"]
    resolved = [r for r in testable if r["resolved_if_mismatch"] == "yes"]
    unresolved = [r for r in testable if r["resolved_if_mismatch"] == "no"]

    assert len(testable) == 7
    assert len(resolved) == 3
    assert len(unresolved) == 4
    assert {r["programme_id"] for r in resolved} == {
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "ML015",
        "P2_CF01_CARDIOPETALUM_2012",
    }
    assert {r["resolved_direction"] for r in resolved} == {"F_more_negative_than_I"}
    assert not any(r["resolved_direction"] == "I_more_negative_than_F" for r in census)

    print(
        "ECOLOGICAL_IF_CENSUS_OK "
        "programmes=8 pair_testable=7 resolved=3 unresolved=4 not_testable=1 "
        "resolved_F_more_negative=3 resolved_I_more_negative=0"
    )


if __name__ == "__main__":
    main()
