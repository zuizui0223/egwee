from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ML020 = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_effects_v1.csv"
SEVEN = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_direct_effects_v1.csv"
KAKA = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_effects_v1.csv"
WANDOO = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv"
ZURICH = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_gradient_effects_v1.csv"
MILK = ROOT / "evidence/meta_extraction/phase2_cf01_milkweed_urban_gradient_effects_v1.csv"
CARDIO = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_effects_v1.csv"
PRITCH = ROOT / "evidence/meta_extraction/phase2_cf01_pritchard_gradient_effects_v1.csv"
CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
SCALE = ROOT / "evidence/meta_extraction/bottleneck_scale_robustness_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def sign(x: float, eps: float = 1e-12) -> str:
    if x > eps:
        return "+"
    if x < -eps:
        return "-"
    return "0"


def panel(programme: str, panel_id: str, i: float, f: float, source: str) -> dict:
    return {
        "programme_id": programme,
        "panel_id": panel_id,
        "I": i,
        "F": f,
        "I_sign": sign(i),
        "F_sign": sign(f),
        "opposite_sign": sign(i) != "0" and sign(f) != "0" and sign(i) != sign(f),
        "polarity": f"{sign(i)}{sign(f)}",
        "source": source,
    }


def main() -> None:
    panels: list[dict] = []

    # ML020: three dependent species panels.
    for sp in sorted({r["species"] for r in rows(ML020)}):
        sr = [r for r in rows(ML020) if r["species"] == sp and r["analysis_role"] == "primary"]
        vals = {r["layer"]: float(r["oriented_effect"]) for r in sr}
        panels.append(panel("ML020", sp, vals["I_interaction"], vals["F_reproductive_function"], "Hedges_g"))

    # Sevenello: three primary species only; POGN remains sensitivity.
    for sp in sorted({r["species"] for r in rows(SEVEN) if r["primary_or_sensitivity"] == "primary"}):
        sr = [r for r in rows(SEVEN) if r["species"] == sp and r["primary_or_sensitivity"] == "primary"]
        vals = {r["layer"]: float(r["hedges_g"]) for r in sr}
        panels.append(panel("P2_CF01_SEVENELLO_2026", sp, vals["I"], vals["F"], "Hedges_g"))

    # Kakamega: four recovered primary panels.
    for pid in sorted({r["panel_id"] for r in rows(KAKA) if r["primary_or_sensitivity"] == "primary"}):
        sr = [r for r in rows(KAKA) if r["panel_id"] == pid and r["primary_or_sensitivity"] == "primary"]
        vals = {r["layer"]: float(r["hedges_g"]) for r in sr}
        panels.append(panel(
            "P2_CF01_BERGSDORF_KAKAMEGA_2006",
            pid,
            vals["I_interaction"],
            vals["F_reproductive_function"],
            "Hedges_g",
        ))

    wr = rows(WANDOO)
    w = {r["layer"]: float(r["oriented_effect"]) for r in wr}
    panels.append(panel("ML015", "Eucalyptus_wandoo", w["I"], w["F"], "Fisher_z"))

    # Zurich: four dependent phytometers.
    for sp in sorted({r["phytometer"] for r in rows(ZURICH)}):
        sr = [r for r in rows(ZURICH) if r["phytometer"] == sp]
        vals = {r["layer"]: float(r["oriented_effect"]) for r in sr}
        panels.append(panel("P2_CF01_ZURICH_2026", sp, vals["I"], vals["F"], "Fisher_z"))

    mr = [r for r in rows(MILK) if r["analysis_frame"] == "primary_source_code_nonzero"]
    m = {r["layer"]: float(r["oriented_effect"]) for r in mr}
    panels.append(panel("P2_CF01_MILKWEED_URBAN_2023", "primary", m["I"], m["F"], "Fisher_z"))

    cr = [r for r in rows(CARDIO) if r["primary_or_sensitivity"] == "primary"]
    c = {r["endpoint_role"]: float(r["fisher_z"]) for r in cr}
    panels.append(panel("P2_CF01_CARDIOPETALUM_2012", "primary", c["I_primary"], c["F_primary"], "Fisher_z"))

    pr = [r for r in rows(PRITCH) if r["primary_or_sensitivity"] == "primary"]
    p = {r["endpoint_role"]: float(r["fisher_z"]) for r in pr}
    panels.append(panel("P2_CF01_PRITCHARD_2005", "primary", p["I_primary"], p["F_primary"], "Fisher_z"))

    assert len(panels) == 18

    opposite = [x for x in panels if x["opposite_sign"]]
    assert len(opposite) == 6
    assert sum(x["polarity"] == "+-" for x in opposite) == 2
    assert sum(x["polarity"] == "-+" for x in opposite) == 4

    programme_ids = {x["programme_id"] for x in panels}
    assert len(programme_ids) == 8
    programmes_with_opposite = {x["programme_id"] for x in opposite}
    assert programmes_with_opposite == {
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "ML015",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
    }

    census = {r["programme_id"]: r for r in rows(CENSUS)}
    resolved = {pid for pid, r in census.items() if r["resolved_if_mismatch"] == "yes"}
    assert resolved == {
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "ML015",
        "P2_CF01_CARDIOPETALUM_2012",
    }
    assert all(census[pid]["resolved_direction"] == "F_more_negative_than_I" for pid in resolved)

    # Among programmes with any opposite-sign panel, only Kakamega and Wandoo are resolved.
    resolved_opposite = resolved & programmes_with_opposite
    assert resolved_opposite == {"P2_CF01_BERGSDORF_KAKAMEGA_2006", "ML015"}

    # Both resolved opposite-sign programmes have I positive and F negative.
    for pid in resolved_opposite:
        assert any(
            x["programme_id"] == pid and x["polarity"] == "+-"
            for x in panels
        )

    # No I-negative/F-positive programme resolves its I-F mismatch.
    reverse_programmes = {
        x["programme_id"] for x in panels if x["polarity"] == "-+"
    }
    assert reverse_programmes == {
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
    }
    assert not (resolved & reverse_programmes)

    # Kakamega downstream attribution survives direct g -> lnRR re-expression.
    scale = {r["programme_id"]: r for r in rows(SCALE)}
    assert scale["P2_CF01_BERGSDORF_KAKAMEGA_2006"]["cross_scale_status"] == "stable_downstream"
    assert scale["P2_CF01_BERGSDORF_KAKAMEGA_2006"]["sensitivity_direction"] == "F_more_negative_than_process"
    assert scale["ML015"]["cross_scale_status"] == "native_gradient_downstream"

    print(
        "IF_SIGN_TOPOLOGY_OK "
        "programmes=8 primary_panels=18 opposite_sign_panels=6 "
        "programmes_with_opposite_sign=5 polarity_plus_minus=2 polarity_minus_plus=4 "
        "resolved_IF_programmes=3 all_resolved_F_dominant=3 "
        "resolved_opposite_sign_programmes=2 resolved_plus_minus=2 resolved_minus_plus=0"
    )


if __name__ == "__main__":
    main()
