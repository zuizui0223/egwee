from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "evidence/meta_extraction/phase2_cf01_target_pair_queue_v1.csv"
SCREEN = ROOT / "evidence/meta_extraction/phase2_cf01_target_pair_design_screen_v1.csv"
FULLTEXT = ROOT / "evidence/meta_extraction/phase2_cf01_target_pair_fulltext_gate_v1.csv"
PAIR_COVERAGE = ROOT / "evidence/meta_extraction/coverage_expansion_pair_coverage_v1.csv"

WAVE3 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE3_2026-09-24.md"
WAVE4 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE4_2026-09-24.md"
WAVE5 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE5_2026-09-24.md"
WAVE6 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE6_2026-09-24.md"
WAVE7 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE7_2026-09-24.md"
WAVE8 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE8_2026-09-24.md"
WAVE9 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE9_2026-09-24.md"
WAVE10 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE10_2026-09-24.md"
MILKWEED_CHECK = ROOT / "scripts/check_phase2_cf01_milkweed_gradient.py"

BRASSICA_CONTRACT = ROOT / "manuscript/CF01_BRASSICA_GUATEMALA_2024_RECOVERY_CONTRACT.md"
BRASSICA_MANIFEST = ROOT / "evidence/meta_extraction/phase2_cf01_brassica_mendeley_manifest_v1.json"
BRASSICA_SCHEMA = ROOT / "manuscript/PHASE2_CF01_BRASSICA_MENDELEY_SCHEMA_2026-09-24.md"
BRASSICA_GATE = ROOT / "manuscript/PHASE2_CF01_BRASSICA_QUANTITATIVE_GATE_2026-09-24.md"
BDFFP_SCHEMA = ROOT / "evidence/meta_extraction/phase2_cf01_bdffp_dryad_schema_v1.json"
BDFFP_STATUS = ROOT / "manuscript/PHASE2_CF01_BDFFP_DRYAD_SCHEMA_2026-09-24.md"
HASS_CONTRACT = ROOT / "manuscript/CF01_HASS_WEUROPE_2018_GRADIENT_RECOVERY_CONTRACT.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for p in (
        QUEUE, SCREEN, FULLTEXT, PAIR_COVERAGE, WAVE3, WAVE4, WAVE5, WAVE6, WAVE7, WAVE8, WAVE9, WAVE10, MILKWEED_CHECK,
        BRASSICA_CONTRACT, BRASSICA_MANIFEST, BRASSICA_SCHEMA, BRASSICA_GATE, BDFFP_SCHEMA, BDFFP_STATUS, HASS_CONTRACT,
    ):
        assert p.is_file(), p

    queue = rows(QUEUE)
    assert len(queue) == 360
    assert [r["queue_id"] for r in queue[:100]] == [f"CFTQ{i:04d}" for i in range(1, 101)]
    assert all(r["outcome_opened"] == "no" for r in queue)

    screen = rows(SCREEN)
    assert len(screen) == 100
    assert [r["queue_id"] for r in screen] == [f"CFTQ{i:04d}" for i in range(1, 101)]
    assert {r["screen_wave"] for r in screen} == {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}
    assert all(sum(r["screen_wave"] == str(w) for r in screen) == 10 for w in range(1, 11))
    assert all(r["outcome_opened"] == "no" for r in screen)
    assert all(r["outcome_blind_confirmation"] == "yes" for r in screen)

    by_id = {r["queue_id"]: r for r in screen}
    wave3 = [r for r in screen if r["screen_wave"] == "3"]
    assert [r["queue_id"] for r in wave3] == [f"CFTQ{i:04d}" for i in range(21, 31)]
    assert [r["queue_id"] for r in wave3 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0030"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave3) == 9

    wave4 = [r for r in screen if r["screen_wave"] == "4"]
    assert [r["queue_id"] for r in wave4] == [f"CFTQ{i:04d}" for i in range(31, 41)]
    assert all(r["screen_decision"].startswith("close_") for r in wave4)
    assert by_id["CFTQ0036"]["screen_decision"] == "close_duplicate_publication"
    assert "CFTQ0032" in by_id["CFTQ0036"]["pair_frame_status"]
    assert by_id["CFTQ0034"]["screen_decision"] == "close_no_fragmentation_contrast"
    assert by_id["CFTQ0038"]["screen_decision"] == "close_no_habitat_fragmentation_exposure"

    wave5 = [r for r in screen if r["screen_wave"] == "5"]
    assert [r["queue_id"] for r in wave5] == [f"CFTQ{i:04d}" for i in range(41, 51)]
    assert [r["queue_id"] for r in wave5 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0044"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave5) == 9
    assert by_id["CFTQ0043"]["screen_decision"] == "close_duplicate_publication"
    assert "CFTQ0039" in by_id["CFTQ0043"]["pair_frame_status"]
    assert by_id["CFTQ0049"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0050"]["screen_decision"] == "close_nonprimary_modelled_fragmentation"

    w3 = WAVE3.read_text(encoding="utf-8")
    for token in (
        "screened in wave 3: **10**",
        "advance to full-text design/quantitative recovery: **1**",
        "cumulative target-pair screen: **30 / 360**",
        "CFTQ0030",
    ):
        assert token in w3, token

    w4 = WAVE4.read_text(encoding="utf-8")
    for token in (
        "screened in wave 4: **10**",
        "advance to full-text target-pair recovery: **0**",
        "cumulative target-pair screen: **40 / 360**",
        "pending target-pair screen: **320**",
        "CFTQ0036",
        "CFTQ0034",
        "CFTQ0038",
    ):
        assert token in w4, token

    w5 = WAVE5.read_text(encoding="utf-8")
    for token in (
        "screened in wave 5: **10**",
        "advance to full-text design/quantitative recovery: **1**",
        "cumulative target-pair screen: **50 / 360**",
        "pending target-pair screen: **310**",
        "CFTQ0044",
        "10.1007/s11252-022-01278-9",
    ):
        assert token in w5, token

    wave6 = [r for r in screen if r["screen_wave"] == "6"]
    assert [r["queue_id"] for r in wave6] == [f"CFTQ{i:04d}" for i in range(51, 61)]
    assert [r["queue_id"] for r in wave6 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0052", "CFTQ0060"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave6) == 8
    assert by_id["CFTQ0055"]["screen_decision"] == "close_single_fragment_edge_interior_pseudoreplication"
    assert by_id["CFTQ0058"]["screen_decision"] == "close_single_fragmented_single_reference_landrace"
    assert by_id["CFTQ0059"]["screen_decision"] == "close_no_direct_F"

    w6 = WAVE6.read_text(encoding="utf-8")
    for token in (
        "screened in wave 6: **10**",
        "advance to full-text design/quantitative gate: **2**",
        "cumulative target-pair screen: **60 / 360**",
        "pending target-pair screen: **300**",
        "CFTQ0052",
        "CFTQ0060",
        "primary direct I-F coverage remains **1/5**",
    ):
        assert token in w6, token

    wave7 = [r for r in screen if r["screen_wave"] == "7"]
    assert [r["queue_id"] for r in wave7] == [f"CFTQ{i:04d}" for i in range(61, 71)]
    assert [r["queue_id"] for r in wave7 if r["screen_decision"] == "advance_full_text_design_screen"] == [
        "CFTQ0065", "CFTQ0069", "CFTQ0070"
    ]
    assert sum(r["screen_decision"].startswith("close_") for r in wave7) == 7
    assert by_id["CFTQ0061"]["screen_decision"] == "close_no_fragmentation_contrast"
    assert by_id["CFTQ0065"]["screen_decision"] == "advance_full_text_design_screen"
    assert by_id["CFTQ0068"]["screen_decision"] == "close_no_direct_F_and_no_fragmentation_contrast"

    w7 = WAVE7.read_text(encoding="utf-8")
    for token in (
        "screened in wave 7: **10**",
        "advance to full-text design clarification: **3**",
        "cumulative target-pair screen: **70 / 360**",
        "pending target-pair screen: **290**",
        "CFTQ0065",
        "CFTQ0069",
        "CFTQ0070",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert token in w7, token

    wave8 = [r for r in screen if r["screen_wave"] == "8"]
    assert [r["queue_id"] for r in wave8] == [f"CFTQ{i:04d}" for i in range(71, 81)]
    assert [r["queue_id"] for r in wave8 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0078"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave8) == 9
    assert by_id["CFTQ0072"]["screen_decision"] == "close_no_direct_C_response"
    assert by_id["CFTQ0075"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0077"]["screen_decision"] == "close_nonprimary_review"

    w8 = WAVE8.read_text(encoding="utf-8")
    for token in (
        "screened in wave 8: **10**",
        "advance to full-text design clarification: **1**",
        "cumulative target-pair screen: **80 / 360**",
        "pending target-pair screen: **280**",
        "CFTQ0078",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert token in w8, token

    wave9 = [r for r in screen if r["screen_wave"] == "9"]
    assert [r["queue_id"] for r in wave9] == [f"CFTQ{i:04d}" for i in range(81, 91)]
    assert [r["queue_id"] for r in wave9 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0084", "CFTQ0088"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave9) == 8
    assert by_id["CFTQ0083"]["screen_decision"] == "close_single_fragment_no_fragmentation_contrast"
    assert by_id["CFTQ0086"]["screen_decision"] == "close_nonprimary_synthesis"
    assert by_id["CFTQ0090"]["screen_decision"] == "close_single_site_per_fragmentation_category_pseudoreplication"

    w9 = WAVE9.read_text(encoding="utf-8")
    for token in (
        "screened in wave 9: **10**",
        "advance to full-text design clarification: **2**",
        "cumulative target-pair screen: **90 / 360**",
        "pending target-pair screen: **270**",
        "CFTQ0084",
        "CFTQ0088",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert token in w9, token

    wave10 = [r for r in screen if r["screen_wave"] == "10"]
    assert [r["queue_id"] for r in wave10] == [f"CFTQ{i:04d}" for i in range(91, 101)]
    assert not [r for r in wave10 if r["screen_decision"] == "advance_full_text_design_screen"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave10) == 10
    assert by_id["CFTQ0094"]["screen_decision"] == "close_single_habitat_per_treatment_pseudoreplication"
    assert by_id["CFTQ0099"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0100"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"

    w10 = WAVE10.read_text(encoding="utf-8")
    for token in (
        "screened in wave 10: **10**",
        "advance to full-text design clarification: **0**",
        "cumulative target-pair screen: **100 / 360**",
        "pending target-pair screen: **260**",
        "CFTQ0094",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert token in w10, token

    fulltext = {r["queue_id"]: r for r in rows(FULLTEXT)}
    assert "CFTQ0030" in fulltext
    b = fulltext["CFTQ0030"]
    assert b["programme_identity"] == "P2_CF01_BRASSICA_GUATEMALA_2024"
    assert b["quantitative_gate_status"] == "blocked_primary_I_raw_not_publicly_recoverable_under_locked_contract"
    assert int(b["pair_programme_increment"]) == 0
    assert b["effect_calculation_opened"] == "no"

    assert "CFTQ0044" in fulltext
    m = fulltext["CFTQ0044"]
    assert m["programme_identity"] == "P2_CF01_MILKWEED_URBAN_2023"
    assert m["identity_status"] == "peer_reviewed_replacement_of_preprint"
    assert m["quantitative_gate_status"] == "recovered_gradient_generalisation_multilayer_cluster"
    assert int(m["pair_programme_increment"]) == 0
    assert m["effect_calculation_opened"] == "yes"

    milk_proc = subprocess.run(
        [sys.executable, str(MILKWEED_CHECK)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "PHASE2_CF01_MILKWEED_CHECK_OK" in milk_proc.stdout
    assert "primary_n=31" in milk_proc.stdout
    assert "sensitivity_n=38" in milk_proc.stdout
    assert "gradient_programmes=3" in milk_proc.stdout
    assert "direct_IF=1/5" in milk_proc.stdout

    assert "CFTQ0052" in fulltext
    ph = fulltext["CFTQ0052"]
    assert ph["programme_identity"] == "P2_CF01_PHACELIA_GRASSLAND_2021"
    assert ph["quantitative_gate_status"] == "blocked_raw_common_IF_plot_data_not_publicly_recoverable"
    assert int(ph["pair_programme_increment"]) == 0
    assert ph["effect_calculation_opened"] == "no"

    assert "CFTQ0060" in fulltext
    he = fulltext["CFTQ0060"]
    assert he["programme_identity"] == "P2_CF01_HEDYSARUM_2021"
    assert he["quantitative_gate_status"] == "closed_single_habitat_per_treatment_pseudoreplication"
    assert int(he["pair_programme_increment"]) == 0
    assert he["effect_calculation_opened"] == "no"

    assert "CFTQ0065" in fulltext
    bdffp = fulltext["CFTQ0065"]
    assert bdffp["programme_identity"] == "P2_CF01_BDFFP_SEED_RAIN_2020"
    assert bdffp["quantitative_gate_status"] == "blocked_public_dryad_file_bytes_not_recoverable"
    assert int(bdffp["pair_programme_increment"]) == 0
    assert bdffp["effect_calculation_opened"] == "no"

    assert "CFTQ0069" in fulltext
    ophrys = fulltext["CFTQ0069"]
    assert ophrys["programme_identity"] == "P2_CF01_OPHRYS_BALEARICA_2021"
    assert ophrys["quantitative_gate_status"] == "close_no_habitat_fragmentation_exposure"
    assert int(ophrys["pair_programme_increment"]) == 0
    assert ophrys["effect_calculation_opened"] == "no"

    assert "CFTQ0070" in fulltext
    brazil = fulltext["CFTQ0070"]
    assert brazil["programme_identity"] == "P2_CF01_BRAZIL_NUT_2021"
    assert brazil["quantitative_gate_status"] == "retain_C_G_gradient_close_CF_no_direct_F"
    assert int(brazil["pair_programme_increment"]) == 0
    assert brazil["effect_calculation_opened"] == "no"

    assert "CFTQ0078" in fulltext
    banksia = fulltext["CFTQ0078"]
    assert banksia["programme_identity"] == "P2_CF01_BANKSIA_NIVEA_2019"
    assert banksia["quantitative_gate_status"] == "close_no_common_IF_fragmentation_frame"
    assert int(banksia["pair_programme_increment"]) == 0
    assert banksia["effect_calculation_opened"] == "no"

    assert "CFTQ0084" in fulltext
    hass = fulltext["CFTQ0084"]
    assert hass["programme_identity"] == "P2_CF01_HASS_WEUROPE_2018"
    assert hass["quantitative_gate_status"] == "recovery_contract_frozen_public_supplement_pending"
    assert "94 landscapes" in hass["independent_unit"]
    assert "229 focal fields" in hass["independent_unit"]
    assert int(hass["pair_programme_increment"]) == 0
    assert hass["effect_calculation_opened"] == "no"

    assert "CFTQ0088" in fulltext
    aloe = fulltext["CFTQ0088"]
    assert aloe["programme_identity"] == "P2_CF01_ALOE_THRASKII_2018"
    assert aloe["quantitative_gate_status"] == "pending_fulltext_habitat_exposure_definition"
    assert int(aloe["pair_programme_increment"]) == 0
    assert aloe["effect_calculation_opened"] == "no"

    bdffp_schema = json.loads(BDFFP_SCHEMA.read_text(encoding="utf-8"))
    assert bdffp_schema["candidate"] == "CFTQ0065"
    assert bdffp_schema["dataset_doi"] == "10.5061/dryad.612jm640h"
    assert bdffp_schema["access_status"] == "public_metadata_visible_file_bytes_blocked"
    assert set(bdffp_schema["indexed_files"]) == {
        "density.rich.data.xlsx", "dispersed.matrix.xlsx",
        "functional.diversity.xlsx", "undispersed.matrix.xlsx"
    }
    assert bdffp_schema["downloaded_files"] == {}
    assert bdffp_schema["effect_outcomes_opened"] is False
    assert bdffp_schema["numeric_effects_calculated"] is False

    bdffp_status = BDFFP_STATUS.read_text(encoding="utf-8")
    for token in (
        "public file-byte access: **blocked**",
        "access/recoverability",
        "not an ecological null",
        "authentication bypass",
    ):
        assert token in bdffp_status, token

    hass_contract = HASS_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "94 independent 1-km² agricultural landscapes",
        "229 focal fields",
        "independent EGWEE unit = landscape",
        "Primary I = **wild-bee abundance**",
        "Primary F = **mean radish seeds per pod**",
        "fragmentation_severity = - field_border_density",
    ):
        assert token in hass_contract, token

    manifest = json.loads(BRASSICA_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["dataset_id"] == "6jw833yrt4"
    assert manifest["version"] == 1
    assert manifest["dataset_doi"] == "10.17632/6jw833yrt4.1"
    assert len(manifest["files"]) == 1
    assert manifest["files"][0]["filename"] == "Data.xlsx"
    assert manifest["direct_visitation_file_hint_detected"] is False
    assert manifest["fruit_set_file_hint_detected"] is True
    assert manifest["effect_calculation_opened"] is False
    sheets = manifest["files"][0]["schema"]["sheets"]
    assert set(sheets) == {"PlotInfo", "FSetData", "BeeDivData"}
    assert sheets["PlotInfo"]["data_rows"] == 23
    assert sheets["FSetData"]["data_rows"] == 751

    schema_status = BRASSICA_SCHEMA.read_text(encoding="utf-8")
    assert "direct-visitation file/column hint detected: **false**" in schema_status
    assert "fruit-set file/column hint detected: **true**" in schema_status

    gate_status = BRASSICA_GATE.read_text(encoding="utf-8")
    for token in (
        "design-valid but quantitatively blocked",
        "does **not** expose the one-hour flower-visitation census rows",
        "new I-F programme increment: **0**",
        "direct I-F coverage remains **1/5**",
    ):
        assert token in gate_status, token

    pair = {r["pair_id"]: r for r in rows(PAIR_COVERAGE)}
    assert int(pair["I-F"]["current_independent_direct_systems"]) == 1
    assert pair["I-F"]["current_system_ids"] == "ML020"
    assert int(pair["C-F"]["current_independent_direct_systems"]) == 2
    assert int(pair["G_adult-G_offspring"]["current_independent_direct_systems"]) == 5

    contract = BRASSICA_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "Primary I = **total floral visitation rate to B. rapa experimental plots**.",
        "Primary F = **natural/open fruit set of B. rapa** in the experimental plots.",
        "Primary fragmentation-level independent unit = **site**",
        "`n_fragmented = 3`;",
        "`n_reference = 3`.",
    ):
        assert token in contract, token

    print(
        "PHASE2_CF01_TARGET_PAIR_SCREEN_OK "
        "queue=360 screened=100 pending=260 wave3_advance=1 wave4_advance=0 wave5_advance=1 wave6_advance=2 wave7_advance=3 wave8_advance=1 wave9_advance=2 wave10_advance=0 "
        "brassica_increment=0 milkweed_gradient_increment=1 phacelia_increment=0 hedysarum_increment=0 "
        "bdffp_access_stop=1 hass_pending=1 aloe_pending=1 bdffp_increment=0 ophrys_increment=0 brazil_nut_CF_increment=0 primary_IF_increment=0 direct_IF=1/5 direct_CF=2/5"
    )


if __name__ == "__main__":
    main()
