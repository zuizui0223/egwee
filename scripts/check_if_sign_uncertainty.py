from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNCERTAINTY = ROOT / "evidence/meta_extraction/if_sign_uncertainty_v1.csv"
SIGN = ROOT / "evidence/meta_extraction/if_sign_geometry_census_v1.csv"

Z95 = 1.96


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def direction(effect: float, variance: float) -> tuple[float, float, str]:
    se = math.sqrt(variance)
    lo = effect - Z95 * se
    hi = effect + Z95 * se
    if lo > 0:
        status = "resolved_positive"
    elif hi < 0:
        status = "resolved_negative"
    else:
        status = "unresolved"
    return lo, hi, status


def main() -> None:
    u = rows(UNCERTAINTY)
    s = rows(SIGN)
    assert len(u) == len(s) == 18

    key_u = {(r["programme_id"], r["panel_id"]): r for r in u}
    key_s = {(r["programme_id"], r["panel_id"]): r for r in s}
    assert set(key_u) == set(key_s)

    for key, r in key_u.items():
        sign = key_s[key]
        ie = float(r["interaction_effect"])
        iv = float(r["interaction_variance"])
        fe = float(r["function_effect"])
        fv = float(r["function_variance"])
        ilo, ihi, ist = direction(ie, iv)
        flo, fhi, fst = direction(fe, fv)

        assert abs(ilo - float(r["interaction_ci_low"])) < 1e-10
        assert abs(ihi - float(r["interaction_ci_high"])) < 1e-10
        assert ist == r["interaction_direction_status"]
        assert abs(flo - float(r["function_ci_low"])) < 1e-10
        assert abs(fhi - float(r["function_ci_high"])) < 1e-10
        assert fst == r["function_direction_status"]

        point_opp = (ie > 0 > fe) or (fe > 0 > ie)
        assert r["point_opposite_sign"] == ("yes" if point_opp else "no")
        assert sign["sign_geometry"] == r["point_sign_geometry"]

        both_resolved_opp = (
            (ist == "resolved_positive" and fst == "resolved_negative")
            or (ist == "resolved_negative" and fst == "resolved_positive")
        )
        one_resolved_opp = (
            point_opp
            and not both_resolved_opp
            and ((ist != "unresolved") ^ (fst != "unresolved"))
        )
        both_unresolved_opp = point_opp and ist == "unresolved" and fst == "unresolved"

        expected = (
            "both_endpoints_resolved_opposite" if both_resolved_opp
            else "one_endpoint_resolved_opposite" if one_resolved_opp
            else "both_endpoints_unresolved_opposite" if both_unresolved_opp
            else "not_point_opposite"
        )
        assert r["discordance_strength"] == expected

    point_opp = [r for r in u if r["point_opposite_sign"] == "yes"]
    both_resolved = [r for r in u if r["discordance_strength"] == "both_endpoints_resolved_opposite"]
    one_resolved = [r for r in u if r["discordance_strength"] == "one_endpoint_resolved_opposite"]
    both_unresolved = [r for r in u if r["discordance_strength"] == "both_endpoints_unresolved_opposite"]

    assert len(point_opp) == 6
    assert len({r["programme_id"] for r in point_opp}) == 5
    assert len(both_resolved) == 0
    assert len(one_resolved) == 2
    assert {(r["programme_id"], r["panel_id"]) for r in one_resolved} == {
        ("ML015", "E_wandoo"),
        ("P2_CF01_BERGSDORF_KAKAMEGA_2006", "AP_2001"),
    }
    assert len(both_unresolved) == 4
    assert {(r["programme_id"], r["panel_id"]) for r in both_unresolved} == {
        ("P2_CF01_SEVENELLO_2026", "LARO"),
        ("P2_CF01_SEVENELLO_2026", "POAR"),
        ("P2_CF01_ZURICH_2026", "Onobrychis_viciifolia"),
        ("P2_CF01_MILKWEED_URBAN_2023", "A_syriaca"),
    }

    print(
        "IF_SIGN_UNCERTAINTY_OK "
        "panels=18 point_opposite=6 programmes_point_opposite=5 "
        "both_resolved_opposite=0 one_resolved_opposite=2 "
        "both_unresolved_opposite=4"
    )


if __name__ == "__main__":
    main()
