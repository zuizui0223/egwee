from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "evidence/meta_extraction/qualitative_process_function_sign_geometry_v1.csv"

ML020 = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_effects_v1.csv"
SEVENELLO = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_direct_effects_v1.csv"
KAKAMEGA = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_effects_v1.csv"
WANDOO = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv"
ZURICH = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_gradient_effects_v1.csv"
MILKWEED = ROOT / "evidence/meta_extraction/phase2_cf01_milkweed_urban_gradient_effects_v1.csv"
ACER = ROOT / "evidence/meta_extraction/phase2_cf01_acer_miyabei_gradient_effects_v1.csv"
CARDIO = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_effects_v1.csv"
PRITCHARD = ROOT / "evidence/meta_extraction/phase2_cf01_pritchard_gradient_effects_v1.csv"
SERAPIAS = ROOT / "evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv"
BROSIMUM = ROOT / "evidence/meta_extraction/PS004_brosimum_extraction_v1.csv"
SOCIALIS = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_effects_v1.csv"

TOL = 5e-9


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def add_pair(out: dict, programme: str, panel: str, design: str, stage: str, process: float, function: float) -> None:
    key = (programme, panel)
    assert key not in out
    out[key] = {
        "design_stream": design,
        "process_stage": stage,
        "process_effect": process,
        "reproductive_effect": function,
    }


def source_pairs() -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], dict] = {}

    # ML020: three dependent species panels.
    ml020 = rows(ML020)
    for species in sorted({r["species"] for r in ml020}):
        sr = [r for r in ml020 if r["species"] == species and r["analysis_role"] == "primary"]
        eff = {r["layer"]: float(r["oriented_effect"]) for r in sr}
        add_pair(out, "ML020", species.replace(" ", "_"), "direct", "I_interaction", eff["I_interaction"], eff["F_reproductive_function"])

    # Sevenello: three primary species panels; POGN is sensitivity only.
    sev = [r for r in rows(SEVENELLO) if r["primary_or_sensitivity"] == "primary"]
    for species in sorted({r["species"] for r in sev}):
        sr = [r for r in sev if r["species"] == species]
        eff = {r["layer"]: float(r["hedges_g"]) for r in sr}
        add_pair(out, "P2_CF01_SEVENELLO_2026", species, "direct", "I_interaction", eff["I"], eff["F"])

    # Kakamega: four primary panels.
    kak = [r for r in rows(KAKAMEGA) if r["primary_or_sensitivity"] == "primary"]
    for panel in sorted({r["panel_id"] for r in kak}):
        sr = [r for r in kak if r["panel_id"] == panel]
        eff = {r["layer"]: float(r["hedges_g"]) for r in sr}
        add_pair(out, "P2_CF01_BERGSDORF_KAKAMEGA_2006", panel, "direct", "I_interaction", eff["I_interaction"], eff["F_reproductive_function"])

    # Wandoo.
    wan = {r["layer"]: float(r["oriented_effect"]) for r in rows(WANDOO)}
    add_pair(out, "ML015", "Eucalyptus_wandoo", "gradient", "I_interaction", wan["I"], wan["F"])

    # Zurich: four primary phytometer panels.
    zur = rows(ZURICH)
    for phyt in sorted({r["phytometer"] for r in zur}):
        sr = [r for r in zur if r["phytometer"] == phyt]
        eff = {r["layer"]: float(r["oriented_effect"]) for r in sr}
        add_pair(out, "P2_CF01_ZURICH_2026", phyt, "gradient", "I_interaction", eff["I"], eff["F"])

    # Milkweed primary frame.
    milk = [r for r in rows(MILKWEED) if r["analysis_frame"] == "primary_source_code_nonzero"]
    eff = {r["layer"]: float(r["oriented_effect"]) for r in milk}
    add_pair(out, "P2_CF01_MILKWEED_URBAN_2023", "primary", "gradient", "I_interaction", eff["I"], eff["F"])

    # Acer primary C-F pair.
    acer = {r["endpoint_role"]: float(r["fisher_z"]) for r in rows(ACER) if r["primary_or_sensitivity"] == "primary"}
    add_pair(out, "P2_CF01_ACER_MIYABEI_2014", "primary", "gradient", "C_movement_connectivity", acer["C_primary"], acer["F_primary"])

    # Cardiopetalum primary I-F.
    car = {r["endpoint_role"]: float(r["fisher_z"]) for r in rows(CARDIO) if r["primary_or_sensitivity"] == "primary"}
    add_pair(out, "P2_CF01_CARDIOPETALUM_2012", "primary", "gradient", "I_interaction", car["I_primary"], car["F_primary"])

    # Pritchard primary I-F.
    pri = {r["endpoint_role"]: float(r["fisher_z"]) for r in rows(PRITCHARD) if r["primary_or_sensitivity"] == "primary"}
    add_pair(out, "P2_CF01_PRITCHARD_2005", "primary", "gradient", "I_interaction", pri["I_primary"], pri["F_primary"])

    # Serapias primary C-F.
    ser = {r["layer"]: float(r["oriented_effect"]) for r in rows(SERAPIAS) if r["primary_or_sensitivity"] == "primary"}
    add_pair(out, "ML001", "Serapias_lingua", "direct", "C_movement_connectivity", ser["C"], ser["F"])

    # Brosimum primary C-F.
    bro = {r["endpoint_id"]: float(r["oriented_effect"]) for r in rows(BROSIMUM) if r["effect_unit_status"] == "g_admissible"}
    add_pair(out, "ML002", "Brosimum_alicastrum", "direct", "C_movement_connectivity", bro["C_paternity_rp"], bro["F_progeny_vigour"])

    # Eucalyptus socialis Gmating-F.
    soc = {r["endpoint_id"]: float(r["oriented_effect"]) for r in rows(SOCIALIS)}
    add_pair(out, "ML014", "Eucalyptus_socialis", "direct", "G_mating", soc["Gmating_correlated_paternity_rp"], soc["F_family_growth"])

    return out


def expected_geometry(process: float, function: float, programme: str) -> tuple[str, str]:
    if process * function > 0:
        if process < 0:
            return "same_sign", "co_deterioration"
        return "same_sign", "co_positive"
    assert process * function < 0
    if process > 0 and function < 0:
        if programme == "P2_CF01_ACER_MIYABEI_2014":
            assert abs(function) < 0.001
            return "opposite_sign", "downstream_failure_near_zero_F"
        return "opposite_sign", "downstream_failure"
    assert process < 0 and function > 0
    return "opposite_sign", "downstream_buffering"


def main() -> None:
    canonical = rows(TABLE)
    source = source_pairs()

    assert len(canonical) == 22
    assert len(source) == 22
    by = {(r["programme_id"], r["panel_id"]): r for r in canonical}
    assert set(by) == set(source)

    for key, src in source.items():
        row = by[key]
        assert row["design_stream"] == src["design_stream"]
        assert row["process_stage"] == src["process_stage"]
        assert abs(float(row["process_effect"]) - src["process_effect"]) < TOL
        assert abs(float(row["reproductive_effect"]) - src["reproductive_effect"]) < TOL
        geom, mode = expected_geometry(src["process_effect"], src["reproductive_effect"], key[0])
        assert row["sign_geometry"] == geom
        assert row["qualitative_mode"] == mode

    programmes = {r["programme_id"] for r in canonical}
    assert len(programmes) == 12

    opposite = [r for r in canonical if r["sign_geometry"] == "opposite_sign"]
    same = [r for r in canonical if r["sign_geometry"] == "same_sign"]
    assert len(opposite) == 7
    assert len(same) == 15

    discordant_programmes = {r["programme_id"] for r in opposite}
    assert len(discordant_programmes) == 6
    assert discordant_programmes == {
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "ML015",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
        "P2_CF01_ACER_MIYABEI_2014",
    }

    # Five programmes show clear opposite-sign I-F geometry; Acer is the only
    # movement/connectivity-F nominal reversal and its F estimate is ~0.
    clear_discordant = discordant_programmes - {"P2_CF01_ACER_MIYABEI_2014"}
    assert clear_discordant == {
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "ML015",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
    }

    interaction_programmes = {r["programme_id"] for r in canonical if r["process_stage"] == "I_interaction"}
    interaction_discordant = {r["programme_id"] for r in opposite if r["process_stage"] == "I_interaction"}
    assert len(interaction_programmes) == 8
    assert len(interaction_discordant) == 5

    movement_mating_programmes = programmes - interaction_programmes
    assert len(movement_mating_programmes) == 4
    mm_discordant = {r["programme_id"] for r in opposite if r["process_stage"] != "I_interaction"}
    assert mm_discordant == {"P2_CF01_ACER_MIYABEI_2014"}

    direct_discordant = {r["programme_id"] for r in opposite if r["design_stream"] == "direct"}
    gradient_discordant = {r["programme_id"] for r in opposite if r["design_stream"] == "gradient"}
    assert direct_discordant == {"P2_CF01_SEVENELLO_2026", "P2_CF01_BERGSDORF_KAKAMEGA_2006"}
    assert gradient_discordant == {
        "ML015",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
        "P2_CF01_ACER_MIYABEI_2014",
    }

    failure_programmes = {r["programme_id"] for r in opposite if r["qualitative_mode"].startswith("downstream_failure")}
    buffering_programmes = {r["programme_id"] for r in opposite if r["qualitative_mode"] == "downstream_buffering"}
    assert failure_programmes == {"P2_CF01_BERGSDORF_KAKAMEGA_2006", "ML015", "P2_CF01_ACER_MIYABEI_2014"}
    assert buffering_programmes == {"P2_CF01_SEVENELLO_2026", "P2_CF01_ZURICH_2026", "P2_CF01_MILKWEED_URBAN_2023"}

    assert sum(r["qualitative_mode"].startswith("downstream_failure") for r in opposite) == 3
    assert sum(r["qualitative_mode"] == "downstream_buffering" for r in opposite) == 4

    print(
        "QUALITATIVE_SIGN_GEOMETRY_OK "
        "programmes=12 panels=22 opposite_panels=7 same_sign_panels=15 "
        "programmes_with_opposite_sign=6 clear_opposite_programmes=5 "
        "interaction_programmes=8 interaction_opposite_programmes=5 "
        "movement_mating_programmes=4 nominal_movement_mating_opposite=1 "
        "direct_opposite_programmes=2 gradient_opposite_programmes=4 "
        "failure_programmes=3 buffering_programmes=3 "
        "acer_near_zero_F=true"
    )


if __name__ == "__main__":
    main()
