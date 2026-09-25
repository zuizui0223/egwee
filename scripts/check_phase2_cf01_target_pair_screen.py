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
WAVE11 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE11_2026-09-24.md"
WAVE12 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE12_2026-09-24.md"
WAVE13 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE13_2026-09-24.md"
WAVE14 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE14_2026-09-24.md"
WAVE15 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE15_2026-09-24.md"
WAVE16 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE16_2026-09-24.md"
WAVE17 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE17_2026-09-24.md"
WAVE18 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE18_2026-09-24.md"
WAVE19 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE19_2026-09-25.md"
WAVE20 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE20_2026-09-25.md"
WAVE21 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE21_2026-09-25.md"
WAVE22 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE22_2026-09-25.md"
WAVE23 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE23_2026-09-25.md"
WAVE24 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE24_2026-09-25.md"
WAVE25 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE25_2026-09-25.md"
WAVE26 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE26_2026-09-25.md"
WAVE27 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE27_2026-09-25.md"
WAVE28 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE28_2026-09-25.md"
WAVE29 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE29_2026-09-25.md"
WAVE30 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE30_2026-09-25.md"
WAVE31 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE31_2026-09-25.md"
WAVE32 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE32_2026-09-25.md"
WAVE33 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE33_2026-09-25.md"
WAVE34 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE34_2026-09-25.md"
WAVE35 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE35_2026-09-25.md"
WAVE36 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE36_2026-09-25.md"
MILKWEED_CHECK = ROOT / "scripts/check_phase2_cf01_milkweed_gradient.py"

BRASSICA_CONTRACT = ROOT / "manuscript/CF01_BRASSICA_GUATEMALA_2024_RECOVERY_CONTRACT.md"
BRASSICA_MANIFEST = ROOT / "evidence/meta_extraction/phase2_cf01_brassica_mendeley_manifest_v1.json"
BRASSICA_SCHEMA = ROOT / "manuscript/PHASE2_CF01_BRASSICA_MENDELEY_SCHEMA_2026-09-24.md"
BRASSICA_GATE = ROOT / "manuscript/PHASE2_CF01_BRASSICA_QUANTITATIVE_GATE_2026-09-24.md"
BDFFP_SCHEMA = ROOT / "evidence/meta_extraction/phase2_cf01_bdffp_dryad_schema_v1.json"
BDFFP_STATUS = ROOT / "manuscript/PHASE2_CF01_BDFFP_DRYAD_SCHEMA_2026-09-24.md"
HASS_CONTRACT = ROOT / "manuscript/CF01_HASS_WEUROPE_2018_GRADIENT_RECOVERY_CONTRACT.md"
HASS_SCHEMA = ROOT / "evidence/meta_extraction/phase2_cf01_hass_supplement_schema_v1.json"
HASS_STATUS = ROOT / "manuscript/PHASE2_CF01_HASS_SUPPLEMENT_SCHEMA_2026-09-24.md"
THAI_ORCHARD_CONTRACT = ROOT / "manuscript/CF01_THAI_ORCHARD_2016_RECOVERY_CONTRACT.md"
THAI_ORCHARD_ACCESS = ROOT / "evidence/meta_extraction/phase2_cf01_thai_orchard_access_v1.json"
THAI_ORCHARD_STATUS = ROOT / "manuscript/PHASE2_CF01_THAI_ORCHARD_ACCESS_GATE_2026-09-24.md"
PLECTRITIS_CONTRACT = ROOT / "manuscript/CF01_PLECTRITIS_2015_GRADIENT_RECOVERY_CONTRACT.md"
CABRALEA_CONTRACT = ROOT / "manuscript/CF01_CABRALEA_2015_DIRECT_IF_RECOVERY_CONTRACT.md"
PLECTRITIS_ACCESS = ROOT / "manuscript/PHASE2_CF01_PLECTRITIS_ACCESS_GATE_2026-09-24.md"
CABRALEA_ACCESS = ROOT / "manuscript/PHASE2_CF01_CABRALEA_ACCESS_GATE_2026-09-24.md"
COMARUM_CONTRACT = ROOT / "manuscript/CF01_COMARUM_2014_GRADIENT_RECOVERY_CONTRACT.md"
COMARUM_ACCESS = ROOT / "manuscript/PHASE2_CF01_COMARUM_ACCESS_GATE_2026-09-24.md"
AEXTOXICON_ANCHOR = ROOT / "manuscript/PHASE2_CF01_AEXTOXICON_PROCESS_ANCHOR_2026-09-24.md"
SCHUEPP_CONTRACT = ROOT / "manuscript/CF01_SCHUEPP_CHERRY_2014_GRADIENT_RECOVERY_CONTRACT.md"
SCHUEPP_ACCESS = ROOT / "manuscript/PHASE2_CF01_SCHUEPP_ACCESS_GATE_2026-09-24.md"
ANAXAGOREA_CONTRACT = ROOT / "manuscript/CF01_ANAXAGOREA_2012_DIRECT_IF_RECOVERY_CONTRACT.md"
ANAXAGOREA_ACCESS = ROOT / "manuscript/PHASE2_CF01_ANAXAGOREA_RECOVERY_GATE_2026-09-24.md"
CELTIS_GATE = ROOT / "manuscript/PHASE2_CF01_CELTIS_ESTIMAND_GATE_2026-09-24.md"
ATTALEA_GATE = ROOT / "manuscript/PHASE2_CF01_ATTALEA_LINKED_CF_GATE_2026-09-24.md"
CARDIOPETALUM_RULE = ROOT / "manuscript/CF01_CARDIOPETALUM_2012_GRADIENT_RECOVERY_RULE.md"
CARDIOPETALUM_RESULT = ROOT / "manuscript/PHASE2_CF01_CARDIOPETALUM_GRADIENT_RECOVERY_2026-09-24.md"
MYRMECOPHILA_GATE = ROOT / "manuscript/PHASE2_CF01_MYRMECOphila_ESTIMAND_GATE_2026-09-25.md"
BARTOMEUS_GATE = ROOT / "manuscript/PHASE2_CF01_BARTOMEUS_ESTIMAND_GATE_2026-09-25.md"
HELICONIA_URIARTE_GATE = ROOT / "manuscript/PHASE2_CF01_HELICONIA_URIARTE_GATE_2026-09-25.md"
BYRSONIMA_GATE = ROOT / "manuscript/PHASE2_CF01_BYRSONIMA_VARIANCE_GATE_2026-09-25.md"
LEPTONYCHIA_GATE = ROOT / "manuscript/PHASE2_CF01_LEPTONYCHIA_LINKED_CAMPAIGN_GATE_2026-09-25.md"
DIEKOETTER_GATE = ROOT / "manuscript/PHASE2_CF01_DIEKOETTER_FACTORIAL_ESTIMAND_GATE_2026-09-25.md"
ARTZ_GATE = ROOT / "manuscript/PHASE2_CF01_ARTZ_ASCLEPIAS_EFFECT_UNIT_GATE_2026-09-25.md"
BRUNSVIGIA_GATE = ROOT / "manuscript/PHASE2_CF01_BRUNSVIGIA_RADULOSA_ESTIMAND_GATE_2026-09-25.md"
QUESADA_GATE = ROOT / "manuscript/PHASE2_CF01_QUESADA_BOMBACACEOUS_EFFECT_UNIT_GATE_2026-09-25.md"
COFFEA_CONTRACT = ROOT / "manuscript/CF01_COFFEA_SULAWESI_2003_GRADIENT_RECOVERY_CONTRACT.md"
CATASETUM_CONTRACT = ROOT / "manuscript/CF01_CATASETUM_2002_DIRECT_IF_RECOVERY_CONTRACT.md"
ACHILLEA_GATE = ROOT / "manuscript/PHASE2_CF01_ACHILLEA_ISOLATION_EFFECT_UNIT_GATE_2026-09-25.md"
CALYSTEGIA_GATE = ROOT / "manuscript/PHASE2_CF01_CALYSTEGIA_EFFECT_UNIT_GATE_2026-09-25.md"
SPONDIAS_MOMBIN_GATE = ROOT / "manuscript/PHASE2_CF01_SPONDIAS_MOMBIN_CF_GATE_2026-09-25.md"
MANGROVE_GATE = ROOT / "manuscript/PHASE2_CF01_MANGROVE_HERMANSEN_GATE_2026-09-25.md"
MYRTUS_GATE = ROOT / "manuscript/PHASE2_CF01_MYRTUS_GATE_2026-09-25.md"
BUERGER_GATE = ROOT / "manuscript/PHASE2_CF01_BUERGER_LANDSCAPE_ESTIMAND_GATE_2026-09-25.md"
COVERAGE_COMPLETION = ROOT / "manuscript/PHASE2_CF01_COVERAGE_COMPLETION_2026-09-25.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def has_token(text: str, token: str) -> bool:
    """Whitespace-insensitive text invariant for prose/status documents."""
    return " ".join(token.split()) in " ".join(text.split())


def main() -> None:
    for p in (
        QUEUE, SCREEN, FULLTEXT, PAIR_COVERAGE, WAVE3, WAVE4, WAVE5, WAVE6, WAVE7, WAVE8, WAVE9, WAVE10, WAVE11, WAVE12, WAVE13, WAVE14, WAVE15, WAVE16, WAVE17, WAVE18, WAVE19, WAVE20, WAVE21, WAVE22, WAVE23, WAVE24, WAVE25, WAVE26, WAVE27, WAVE28, WAVE29, WAVE30, WAVE31, WAVE32, WAVE33, WAVE34, WAVE35, WAVE36, MILKWEED_CHECK,
        BRASSICA_CONTRACT, BRASSICA_MANIFEST, BRASSICA_SCHEMA, BRASSICA_GATE, BDFFP_SCHEMA, BDFFP_STATUS, HASS_CONTRACT, HASS_SCHEMA, HASS_STATUS, THAI_ORCHARD_CONTRACT, THAI_ORCHARD_ACCESS, THAI_ORCHARD_STATUS, PLECTRITIS_CONTRACT, CABRALEA_CONTRACT, PLECTRITIS_ACCESS, CABRALEA_ACCESS, COMARUM_CONTRACT, COMARUM_ACCESS, AEXTOXICON_ANCHOR, SCHUEPP_CONTRACT, SCHUEPP_ACCESS, ANAXAGOREA_CONTRACT, ANAXAGOREA_ACCESS, CELTIS_GATE, ATTALEA_GATE, CARDIOPETALUM_RULE, CARDIOPETALUM_RESULT, MYRMECOPHILA_GATE, BARTOMEUS_GATE, HELICONIA_URIARTE_GATE, BYRSONIMA_GATE, LEPTONYCHIA_GATE, DIEKOETTER_GATE, ARTZ_GATE, BRUNSVIGIA_GATE, QUESADA_GATE, COFFEA_CONTRACT, CATASETUM_CONTRACT, ACHILLEA_GATE, CALYSTEGIA_GATE, SPONDIAS_MOMBIN_GATE, MANGROVE_GATE, MYRTUS_GATE, BUERGER_GATE, COVERAGE_COMPLETION,
    ):
        assert p.is_file(), p

    queue = rows(QUEUE)
    assert len(queue) == 360
    assert [r["queue_id"] for r in queue[:360]] == [f"CFTQ{i:04d}" for i in range(1, 361)]
    assert all(r["outcome_opened"] == "no" for r in queue)

    screen = rows(SCREEN)
    assert len(screen) == 360
    assert [r["queue_id"] for r in screen] == [f"CFTQ{i:04d}" for i in range(1, 361)]
    assert {r["screen_wave"] for r in screen} == {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"}
    assert all(sum(r["screen_wave"] == str(w) for r in screen) == 10 for w in range(1, 37))
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
        assert has_token(w3, token), token

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
        assert has_token(w4, token), token

    w5 = WAVE5.read_text(encoding="utf-8")
    for token in (
        "screened in wave 5: **10**",
        "advance to full-text design/quantitative recovery: **1**",
        "cumulative target-pair screen: **50 / 360**",
        "pending target-pair screen: **310**",
        "CFTQ0044",
        "10.1007/s11252-022-01278-9",
    ):
        assert has_token(w5, token), token

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
        "primary direct I-F coverage remains **1/5",
    ):
        assert has_token(w6, token), token

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
        assert has_token(w7, token), token

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
        "primary direct I-F coverage remains **1/5",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w8, token), token

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
        "primary direct I-F coverage remains **1/5",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w9, token), token

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
        "primary direct I-F coverage remains **1/5",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w10, token), token

    wave11 = [r for r in screen if r["screen_wave"] == "11"]
    assert [r["queue_id"] for r in wave11] == [f"CFTQ{i:04d}" for i in range(101, 111)]
    assert [r["queue_id"] for r in wave11 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0103"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave11) == 9
    assert by_id["CFTQ0102"]["screen_decision"] == "close_nonplant_or_wrong_biological_system"
    assert by_id["CFTQ0103"]["screen_decision"] == "advance_full_text_design_screen"
    assert by_id["CFTQ0107"]["screen_decision"] == "close_no_direct_C_response"

    w11 = WAVE11.read_text(encoding="utf-8")
    for token in (
        "screened in wave 11: **10**",
        "advance to full-text design / quantitative-access gate: **1**",
        "cumulative target-pair screen: **110 / 360**",
        "pending target-pair screen: **250**",
        "CFTQ0103",
        "primary direct I-F coverage remains **1/5",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w11, token), token

    wave12 = [r for r in screen if r["screen_wave"] == "12"]
    assert [r["queue_id"] for r in wave12] == [f"CFTQ{i:04d}" for i in range(111, 121)]
    assert [r["queue_id"] for r in wave12 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0119"]
    assert [r["queue_id"] for r in wave12 if r["screen_decision"] == "link_existing_programme"] == ["CFTQ0117"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave12) == 8
    assert by_id["CFTQ0112"]["screen_decision"] == "close_single_fragmented_single_reference_population"
    assert by_id["CFTQ0116"]["screen_decision"] == "close_nonplant_or_wrong_biological_system"
    assert by_id["CFTQ0120"]["screen_decision"] == "close_nonprimary_review"

    w12 = WAVE12.read_text(encoding="utf-8")
    for token in (
        "screened in wave 12: **10**",
        "advance to full-text design clarification: **1**",
        "link to an existing programme: **1**",
        "cumulative target-pair screen: **120 / 360**",
        "pending target-pair screen: **240**",
        "CFTQ0119",
        "CFTQ0117",
        "primary direct I-F coverage remains **1/5",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w12, token), token

    wave13 = [r for r in screen if r["screen_wave"] == "13"]
    assert [r["queue_id"] for r in wave13] == [f"CFTQ{i:04d}" for i in range(121, 131)]
    assert [r["queue_id"] for r in wave13 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0121", "CFTQ0124"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave13) == 8
    assert by_id["CFTQ0122"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0125"]["screen_decision"] == "close_no_direct_C_response"
    assert by_id["CFTQ0130"]["screen_decision"] == "close_nonprimary_review"

    w13 = WAVE13.read_text(encoding="utf-8")
    for token in (
        "screened in wave 13: **10**",
        "advance to full-text / recovery gate: **2**",
        "cumulative target-pair screen: **130 / 360**",
        "pending target-pair screen: **230**",
        "CFTQ0121",
        "CFTQ0124",
        "primary direct I-F coverage remains **1/5",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w13, token), token

    wave14 = [r for r in screen if r["screen_wave"] == "14"]
    assert [r["queue_id"] for r in wave14] == [f"CFTQ{i:04d}" for i in range(131, 141)]
    assert [r["queue_id"] for r in wave14 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0135"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave14) == 9
    assert by_id["CFTQ0131"]["screen_decision"] == "close_nonprimary_modelled_fragmentation"
    assert by_id["CFTQ0139"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0140"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"

    w14 = WAVE14.read_text(encoding="utf-8")
    for token in (
        "screened in wave 14: **10**",
        "advance to full-text / recovery gate: **1**",
        "cumulative target-pair screen: **140 / 360**",
        "pending target-pair screen: **220**",
        "CFTQ0135",
        "primary direct I-F coverage remains **1/5",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w14, token), token

    wave15 = [r for r in screen if r["screen_wave"] == "15"]
    assert [r["queue_id"] for r in wave15] == [f"CFTQ{i:04d}" for i in range(141, 151)]
    assert [r["queue_id"] for r in wave15 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0142"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave15) == 9
    assert by_id["CFTQ0141"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"
    assert by_id["CFTQ0147"]["screen_decision"] == "close_no_direct_I"
    assert by_id["CFTQ0150"]["screen_decision"] == "close_nonprimary_review"

    w15 = WAVE15.read_text(encoding="utf-8")
    for token in (
        "screened in wave 15: **10**",
        "advance to full-text / recovery gate: **1**",
        "cumulative target-pair screen: **150 / 360**",
        "pending target-pair screen: **210**",
        "CFTQ0142",
        "fourth gradient/generalisation programme",
        "C-F contrast: **+0.181**",
        "p: **0.624**",
        "primary direct I-F coverage remains **1/5",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w15, token), token

    wave16 = [r for r in screen if r["screen_wave"] == "16"]
    assert [r["queue_id"] for r in wave16] == [f"CFTQ{i:04d}" for i in range(151, 161)]
    assert [r["queue_id"] for r in wave16 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0155", "CFTQ0156"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave16) == 8
    assert by_id["CFTQ0154"]["screen_decision"] == "close_single_habitat_per_treatment_pseudoreplication"
    assert by_id["CFTQ0158"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0160"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"

    w16 = WAVE16.read_text(encoding="utf-8")
    for token in (
        "screened in wave 16: **10**",
        "advance to full-text / recovery gate: **2**",
        "cumulative target-pair screen: **160 / 360**",
        "pending target-pair screen: **200**",
        "CFTQ0155",
        "CFTQ0156",
        "movement-compensation",
        "gradient/generalisation registry remains **4 programmes**",
        "primary direct I-F coverage remains **1/5",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w16, token), token

    wave17 = [r for r in screen if r["screen_wave"] == "17"]
    assert [r["queue_id"] for r in wave17] == [f"CFTQ{i:04d}" for i in range(161, 171)]
    assert [r["queue_id"] for r in wave17 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0162", "CFTQ0165", "CFTQ0166"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave17) == 7
    assert by_id["CFTQ0164"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"
    assert by_id["CFTQ0168"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0169"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"

    w17 = WAVE17.read_text(encoding="utf-8")
    for token in (
        "screened in wave 17: **10**",
        "advance to full-text / recovery gate: **3**",
        "cumulative target-pair screen: **170 / 360**",
        "pending target-pair screen: **190**",
        "CFTQ0162",
        "CFTQ0165",
        "CFTQ0166",
        "fifth gradient/generalisation programme",
        "I − F: **+1.439**",
        "p = **0.00316**",
        "primary direct I-F coverage remains **1/5",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w17, token), token

    wave18 = [r for r in screen if r["screen_wave"] == "18"]
    assert [r["queue_id"] for r in wave18] == [f"CFTQ{i:04d}" for i in range(171, 181)]
    assert [r["queue_id"] for r in wave18 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0171"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave18) == 9
    assert by_id["CFTQ0174"]["screen_decision"] == "close_no_habitat_fragmentation_exposure"
    assert by_id["CFTQ0179"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"
    assert by_id["CFTQ0180"]["screen_decision"] == "close_single_reference_site_pseudoreplication"

    w18 = WAVE18.read_text(encoding="utf-8")
    for token in (
        "screened in wave 18: **10**",
        "advance to linked-publication/full-text gate: **1**",
        "cumulative target-pair screen: **180 / 360**",
        "pending target-pair screen: **180**",
        "CFTQ0171",
        "reproduction–movement sign reversal",
        "blocked_linked_four_fragment_CF_values_not_recoverable",
        "CFTQ0174",
        "CFTQ0180",
        "gradient/generalisation registry remains **5 programmes / 17 primary Fisher-z effects**",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w18, token), token

    wave19 = [r for r in screen if r["screen_wave"] == "19"]
    assert [r["queue_id"] for r in wave19] == [f"CFTQ{i:04d}" for i in range(181, 191)]
    assert [r["queue_id"] for r in wave19 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0187"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave19) == 9
    assert by_id["CFTQ0183"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0186"]["screen_decision"] == "close_nonplant_or_wrong_biological_system"
    assert by_id["CFTQ0189"]["screen_decision"] == "close_nonprimary_modelled_fragmentation"

    w19 = WAVE19.read_text(encoding="utf-8")
    for token in (
        "screened in wave 19: **10**",
        "advance to full-text / estimand gate: **1**",
        "cumulative target-pair screen: **190 / 360**",
        "pending target-pair screen: **170**",
        "CFTQ0187",
        "fragment area/size",
        "habitat disturbance / affectation",
        "gradient/generalisation registry remains **5 programmes / 17 primary Fisher-z effects**",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w19, token), token

    wave20 = [r for r in screen if r["screen_wave"] == "20"]
    assert [r["queue_id"] for r in wave20] == [f"CFTQ{i:04d}" for i in range(191, 201)]
    assert not [r for r in wave20 if r["screen_decision"] == "advance_full_text_design_screen"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave20) == 10
    assert by_id["CFTQ0191"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0194"]["screen_decision"] == "close_nonplant_or_wrong_biological_system"
    assert by_id["CFTQ0196"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0200"]["screen_decision"] == "close_nonplant_or_wrong_biological_system"

    w20 = WAVE20.read_text(encoding="utf-8")
    for token in (
        "screened in wave 20: **10**",
        "advance to full-text / recovery gate: **0**",
        "cumulative target-pair screen: **200 / 360**",
        "pending target-pair screen: **160**",
        "CFTQ0196",
        "C → D",
        "D_resource_demography",
        "gradient/generalisation registry remains **5 programmes / 17 primary Fisher-z effects**",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w20, token), token

    wave21 = [r for r in screen if r["screen_wave"] == "21"]
    assert [r["queue_id"] for r in wave21] == [f"CFTQ{i:04d}" for i in range(201, 211)]
    assert [r["queue_id"] for r in wave21 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0202", "CFTQ0204", "CFTQ0209"]
    assert [r["queue_id"] for r in wave21 if r["screen_decision"] == "link_existing_programme"] == ["CFTQ0206"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave21) == 6
    assert by_id["CFTQ0201"]["screen_decision"] == "close_no_common_pair_frame"
    assert by_id["CFTQ0208"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0210"]["screen_decision"] == "close_no_direct_F"

    w21 = WAVE21.read_text(encoding="utf-8")
    for token in (
        "screened in wave 21: **10**",
        "advance to full-text design screen: **3**",
        "link to existing/umbrella programme identity: **1**",
        "cumulative target-pair screen: **210 / 360**",
        "pending target-pair screen: **150**",
        "CFTQ0202",
        "CFTQ0204",
        "CFTQ0209",
        "CFTQ0206",
        "blocked_fragment_level_IF_dispersion_and_dependence_not_recoverable",
        "C → D / seed-limitation process anchor",
        "EGWEE does not promote modelled potential seed supply to direct F",
        "gradient/generalisation registry remains **5 programmes / 17 primary Fisher-z effects**",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w21, token), token

    wave22 = [r for r in screen if r["screen_wave"] == "22"]
    assert [r["queue_id"] for r in wave22] == [f"CFTQ{i:04d}" for i in range(211, 221)]
    assert [r["queue_id"] for r in wave22 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0215"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave22) == 9
    assert by_id["CFTQ0211"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0213"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"
    assert by_id["CFTQ0216"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0220"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"

    w22 = WAVE22.read_text(encoding="utf-8")
    for token in (
        "screened in wave 22: **10**",
        "advance to linked-publication/full-text gate: **1**",
        "cumulative target-pair screen: **220 / 360**",
        "pending target-pair screen: **140**",
        "CFTQ0215",
        "2, 9, 13 and 31 ha",
        "pending_linked_2003_2009_site_and_campaign_alignment",
        "gradient/generalisation registry remains **5 programmes / 17 primary Fisher-z effects**",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w22, token), token

    wave23 = [r for r in screen if r["screen_wave"] == "23"]
    assert [r["queue_id"] for r in wave23] == [f"CFTQ{i:04d}" for i in range(221, 231)]
    assert [r["queue_id"] for r in wave23 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0229"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave23) == 9
    assert by_id["CFTQ0221"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0228"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"
    assert by_id["CFTQ0230"]["screen_decision"] == "close_no_direct_F"

    w23 = WAVE23.read_text(encoding="utf-8")
    for token in (
        "screened in wave 23: **10**",
        "advance to factorial full-text / estimand gate: **1**",
        "cumulative target-pair screen: **230 / 360**",
        "pending target-pair screen: **130**",
        "CFTQ0229",
        "habitat area",
        "fragmentation / configuration",
        "matrix composition",
        "pending_factorial_fragmentation_estimand_and_independent_unit_recovery",
        "gradient/generalisation registry remains **5 programmes / 17 primary Fisher-z effects**",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w23, token), token

    wave24 = [r for r in screen if r["screen_wave"] == "24"]
    assert [r["queue_id"] for r in wave24] == [f"CFTQ{i:04d}" for i in range(231, 241)]
    assert [r["queue_id"] for r in wave24 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0235"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave24) == 9
    assert by_id["CFTQ0231"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"
    assert by_id["CFTQ0236"]["screen_decision"] == "close_no_direct_I"
    assert by_id["CFTQ0238"]["screen_decision"] == "close_nonplant_or_wrong_biological_system"
    assert by_id["CFTQ0240"]["screen_decision"] == "close_no_common_pair_frame"

    w24 = WAVE24.read_text(encoding="utf-8")
    for token in (
        "screened in wave 24: **10**",
        "advance to full-text / effect-unit gate: **1**",
        "cumulative target-pair screen: **240 / 360**",
        "pending target-pair screen: **120**",
        "CFTQ0235",
        "5 small and 6 large Everglades tree islands",
        "blocked_repeated_island_IF_effect_unit_not_recoverable",
        "tree island",
        "gradient/generalisation registry remains **5 programmes / 17 primary Fisher-z effects**",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w24, token), token

    wave25 = [r for r in screen if r["screen_wave"] == "25"]
    assert [r["queue_id"] for r in wave25] == [f"CFTQ{i:04d}" for i in range(241, 251)]
    assert not [r for r in wave25 if r["screen_decision"] == "advance_full_text_design_screen"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave25) == 10
    assert by_id["CFTQ0242"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0246"]["screen_decision"] == "close_duplicate_publication"
    assert by_id["CFTQ0249"]["screen_decision"] == "close_nonprimary_review"

    w25 = WAVE25.read_text(encoding="utf-8")
    for token in (
        "screened in wave 25: **10**",
        "advance to full-text / recovery gate: **0**",
        "cumulative target-pair screen: **250 / 360**",
        "pending target-pair screen: **110**",
        "CFTQ0241",
        "CFTQ0243",
        "CFTQ0245",
        "CFTQ0246",
        "gradient/generalisation registry remains **5 programmes / 17 primary Fisher-z effects**",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w25, token), token

    wave26 = [r for r in screen if r["screen_wave"] == "26"]
    assert [r["queue_id"] for r in wave26] == [f"CFTQ{i:04d}" for i in range(251, 261)]
    assert not [r for r in wave26 if r["screen_decision"] == "advance_full_text_design_screen"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave26) == 10
    assert by_id["CFTQ0251"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0256"]["screen_decision"] == "close_nonplant_or_wrong_biological_system"
    assert by_id["CFTQ0257"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0260"]["screen_decision"] == "close_nonprimary_modelled_fragmentation"

    w26 = WAVE26.read_text(encoding="utf-8")
    for token in (
        "screened in wave 26: **10**",
        "advance to full-text / recovery gate: **0**",
        "cumulative target-pair screen: **260 / 360**",
        "pending target-pair screen: **100**",
        "CFTQ0257",
        "outcross pollen receipt",
        "do **not** measure realised fruit set or seed production",
        "CFTQ0254",
        "CFTQ0255",
        "gradient/generalisation registry remains **5 programmes / 17 primary Fisher-z effects**",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w26, token), token

    wave27 = [r for r in screen if r["screen_wave"] == "27"]
    assert [r["queue_id"] for r in wave27] == [f"CFTQ{i:04d}" for i in range(261, 271)]
    assert [r["queue_id"] for r in wave27 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0263", "CFTQ0267"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave27) == 8
    assert by_id["CFTQ0261"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"
    assert by_id["CFTQ0264"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0268"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0269"]["screen_decision"] == "close_no_direct_I"

    w27 = WAVE27.read_text(encoding="utf-8")
    for token in (
        "screened in wave 27: **10**",
        "advance to full-text / estimand-effect-unit gate: **2**",
        "cumulative target-pair screen: **270 / 360**",
        "pending target-pair screen: **90**",
        "CFTQ0263",
        "CFTQ0267",
        "fragment area or isolation",
        "one publication programme",
        "gradient/generalisation registry remains **5 programmes / 17 primary Fisher-z effects**",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w27, token), token

    wave28 = [r for r in screen if r["screen_wave"] == "28"]
    assert [r["queue_id"] for r in wave28] == [f"CFTQ{i:04d}" for i in range(271, 281)]
    assert [r["queue_id"] for r in wave28 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0272", "CFTQ0278"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave28) == 8
    assert by_id["CFTQ0271"]["screen_decision"] == "close_no_direct_I"
    assert by_id["CFTQ0275"]["screen_decision"] == "close_nonplant_or_wrong_biological_system"
    assert by_id["CFTQ0279"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0280"]["screen_decision"] == "close_nonprimary_review"

    w28 = WAVE28.read_text(encoding="utf-8")
    for token in (
        "screened in wave 28: **10**",
        "advance to full-text / recovery contract: **2**",
        "cumulative target-pair screen: **280 / 360**",
        "pending target-pair screen: **80**",
        "CFTQ0272",
        "CFTQ0278",
        "distance to forest",
        "five island and five mainland sites",
        "gradient/generalisation registry remains **5 programmes / 17 primary Fisher-z effects** pending Coffea",
        "primary direct I-F coverage remains **1/5** pending Catasetum recovery",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w28, token), token

    wave29 = [r for r in screen if r["screen_wave"] == "29"]
    assert [r["queue_id"] for r in wave29] == [f"CFTQ{i:04d}" for i in range(281, 291)]
    assert [r["queue_id"] for r in wave29 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0283", "CFTQ0286"]
    assert sum(r["screen_decision"] == "close_duplicate_publication" for r in wave29) == 3
    assert sum(r["screen_decision"].startswith("close_") for r in wave29) == 8
    assert by_id["CFTQ0281"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0282"]["screen_decision"] == "close_no_eligible_EGWEE_pair"
    assert by_id["CFTQ0289"]["screen_decision"] == "close_no_direct_F"

    w29 = WAVE29.read_text(encoding="utf-8")
    for token in (
        "screened: **10**",
        "advanced to full-text/effect-unit gate: **2**",
        "duplicates linked: **3**",
        "cumulative screen: **290 / 360**",
        "pending: **70**",
        "CFTQ0283",
        "CFTQ0286",
        "16 small versus seven large serpentine outcrops",
        "independent habitat unit is the outcrop",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w29, token), token

    wave30 = [r for r in screen if r["screen_wave"] == "30"]
    assert [r["queue_id"] for r in wave30] == [f"CFTQ{i:04d}" for i in range(291, 301)]
    assert not [r for r in wave30 if r["screen_decision"] == "advance_full_text_design_screen"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave30) == 10
    assert by_id["CFTQ0293"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0296"]["screen_decision"] == "close_nonplant_or_wrong_biological_system"
    assert by_id["CFTQ0299"]["screen_decision"] == "close_duplicate_publication"
    assert by_id["CFTQ0300"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"

    w30 = WAVE30.read_text(encoding="utf-8")
    for token in (
        "screened: **10**",
        "advance: **0**",
        "cumulative screen: **300 / 360**",
        "pending: **60**",
        "CFTQ0291",
        "CFTQ0292",
        "CFTQ0299",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w30, token), token

    wave31 = [r for r in screen if r["screen_wave"] == "31"]
    assert [r["queue_id"] for r in wave31] == [f"CFTQ{i:04d}" for i in range(301, 311)]
    assert [r["queue_id"] for r in wave31 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0301"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave31) == 9
    assert by_id["CFTQ0302"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"
    assert by_id["CFTQ0306"]["screen_decision"] == "close_no_direct_I"
    assert by_id["CFTQ0307"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0309"]["screen_decision"] == "close_no_direct_F"

    w31 = WAVE31.read_text(encoding="utf-8")
    for token in (
        "screened: **10**",
        "advance to full-text / effect-unit gate: **1**",
        "cumulative screen: **310 / 360**",
        "pending: **50**",
        "CFTQ0301",
        "90–100%",
        "80–1000 m",
        "small island fragments",
        "continuous-forest populations FDP + LC",
        "movement-compensation / reproductive-decline anchor",
        "primary direct C-F coverage remains **2/5** pending Spondias recovery",
    ):
        assert has_token(w31, token), token

    wave32 = [r for r in screen if r["screen_wave"] == "32"]
    assert [r["queue_id"] for r in wave32] == [f"CFTQ{i:04d}" for i in range(311, 321)]
    assert [r["queue_id"] for r in wave32 if r["screen_decision"] == "advance_full_text_design_screen"] == [
        "CFTQ0312", "CFTQ0313", "CFTQ0314", "CFTQ0315",
        "CFTQ0316", "CFTQ0317", "CFTQ0318", "CFTQ0319",
    ]
    assert [r["queue_id"] for r in wave32 if r["screen_decision"] == "link_existing_programme"] == ["CFTQ0320"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave32) == 1
    assert by_id["CFTQ0311"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"

    w32 = WAVE32.read_text(encoding="utf-8")
    for token in (
        "screened: **10**",
        "advance to full-text / effect-unit gate: **8**",
        "link to existing programme / umbrella identity: **1**",
        "cumulative screen: **320 / 360**",
        "pending: **40**",
        "CFTQ0312",
        "CFTQ0315",
        "CFTQ0316",
        "CFTQ0320",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
        "5 programmes / 17 primary Fisher-z effects",
    ):
        assert has_token(w32, token), token

    wave33 = [r for r in screen if r["screen_wave"] == "33"]
    assert [r["queue_id"] for r in wave33] == [f"CFTQ{i:04d}" for i in range(321, 331)]
    assert [r["queue_id"] for r in wave33 if r["screen_decision"] == "advance_full_text_design_screen"] == [
        "CFTQ0322", "CFTQ0324", "CFTQ0329"
    ]
    assert [r["queue_id"] for r in wave33 if r["screen_decision"] == "link_existing_programme"] == ["CFTQ0325"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave33) == 6
    assert by_id["CFTQ0323"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0328"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"
    assert by_id["CFTQ0330"]["screen_decision"] == "close_no_direct_F"

    w33 = WAVE33.read_text(encoding="utf-8")
    for token in (
        "screened: **10**",
        "advance to full-text / effect-unit gate: **3**",
        "link to existing / umbrella programme identity: **1**",
        "cumulative screen: **330 / 360**",
        "pending: **30**",
        "CFTQ0324",
        "20 mapped habitat patches",
        "CFTQ0322",
        "CFTQ0329",
        "linked_umbrella_source_no_new_K",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w33, token), token

    wave34 = [r for r in screen if r["screen_wave"] == "34"]
    assert [r["queue_id"] for r in wave34] == [f"CFTQ{i:04d}" for i in range(331, 341)]
    assert [r["queue_id"] for r in wave34 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0334", "CFTQ0338"]
    assert [r["queue_id"] for r in wave34 if r["screen_decision"] == "link_existing_programme"] == ["CFTQ0333", "CFTQ0340"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave34) == 6
    assert by_id["CFTQ0331"]["screen_decision"] == "close_nonprimary_review"
    assert by_id["CFTQ0336"]["screen_decision"] == "close_no_direct_I"
    assert by_id["CFTQ0339"]["screen_decision"] == "close_no_eligible_EGWEE_layer"

    w34 = WAVE34.read_text(encoding="utf-8")
    for token in (
        "screened: **10**",
        "advance to full-text / effect-unit gate: **2**",
        "link to existing / umbrella programme identity: **2**",
        "cumulative screen: **340 / 360**",
        "pending: **20**",
        "CFTQ0334",
        "three plant species are **dependent panels inside one programme**",
        "CFTQ0338",
        "CFTQ0333",
        "CFTQ0340",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w34, token), token

    wave35 = [r for r in screen if r["screen_wave"] == "35"]
    assert [r["queue_id"] for r in wave35] == [f"CFTQ{i:04d}" for i in range(341, 351)]
    assert [r["queue_id"] for r in wave35 if r["screen_decision"] == "advance_full_text_design_screen"] == [
        "CFTQ0344", "CFTQ0345", "CFTQ0349", "CFTQ0350"
    ]
    assert sum(r["screen_decision"].startswith("close_") for r in wave35) == 6
    assert by_id["CFTQ0341"]["screen_decision"] == "close_no_direct_F"
    assert by_id["CFTQ0343"]["screen_decision"] == "close_no_direct_C_response"
    assert by_id["CFTQ0348"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"

    w35 = WAVE35.read_text(encoding="utf-8")
    for token in (
        "screened: **10**",
        "advance to full-text / effect-unit gate: **4**",
        "cumulative screen: **350 / 360**",
        "pending: **10**",
        "CFTQ0344",
        "six fragment trees and five continuous-forest trees",
        "CFTQ0345",
        "CFTQ0349",
        "CFTQ0350",
        "primary direct I-F coverage remains **1/5**",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert has_token(w35, token), token

    wave36 = [r for r in screen if r["screen_wave"] == "36"]
    assert [r["queue_id"] for r in wave36] == [f"CFTQ{i:04d}" for i in range(351, 361)]
    assert [r["queue_id"] for r in wave36 if r["screen_decision"] == "advance_full_text_design_screen"] == ["CFTQ0356"]
    assert [r["queue_id"] for r in wave36 if r["screen_decision"] == "link_existing_programme"] == ["CFTQ0355", "CFTQ0357"]
    assert sum(r["screen_decision"].startswith("close_") for r in wave36) == 7
    assert by_id["CFTQ0354"]["screen_decision"] == "close_nonplant_or_wrong_biological_system"
    assert by_id["CFTQ0359"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"
    assert by_id["CFTQ0360"]["screen_decision"] == "close_no_source_defined_fragmentation_exposure"

    w36 = WAVE36.read_text(encoding="utf-8")
    for token in (
        "screened: **10**",
        "advance to full-text / effect-unit gate: **1**",
        "link to existing / umbrella programme identity: **2**",
        "cumulative screen: **360 / 360**",
        "pending: **0**",
        "P2_CF01_COFFEA_SULAWESI_2003",
        "search-completion stopping rule",
        "primary direct I-F coverage: **1/5**",
        "primary direct C-F coverage: **2/5**",
        "G_adult-G_offspring direct coverage: **5/5**",
        "5 programmes / 17 primary Fisher-z marginal",
        "No NEE operator",
    ):
        assert has_token(w36, token), token

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
    assert "gradient_programmes=5" in milk_proc.stdout
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
    assert hass["quantitative_gate_status"] == "blocked_public_S3_workbook_not_recoverable"
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

    assert "CFTQ0103" in fulltext
    thai = fulltext["CFTQ0103"]
    assert thai["programme_identity"] == "P2_CF01_THAI_ORCHARD_FOREST_PROXIMITY_2016"
    assert thai["quantitative_gate_status"] == "blocked_public_orchard_level_IF_data_not_recoverable"
    assert "10 near + 10 far orchards" in thai["independent_unit"]
    assert int(thai["pair_programme_increment"]) == 0
    assert thai["effect_calculation_opened"] == "no"

    assert "CFTQ0117" in fulltext
    brudvig = fulltext["CFTQ0117"]
    assert brudvig["programme_identity"] == "PS014_ML007_HULTING_PROGRAMME"
    assert brudvig["identity_status"] == "linked_existing_programme_same_Savannah_River_experiment"
    assert brudvig["quantitative_gate_status"] == "linked_existing_programme_historical_IF_campaign_no_new_K"
    assert int(brudvig["pair_programme_increment"]) == 0
    assert brudvig["effect_calculation_opened"] == "no"

    assert "CFTQ0119" in fulltext
    acer = fulltext["CFTQ0119"]
    assert acer["programme_identity"] == "P2_CF01_ACER_MONO_2015"
    assert acer["quantitative_gate_status"] == "retain_C_G_close_CF_no_direct_current_F"
    assert "pollen dispersal" in acer["I_endpoint"] or "pollen dispersal" in acer["gate_reason"]
    assert int(acer["pair_programme_increment"]) == 0
    assert acer["effect_calculation_opened"] == "no"

    assert "CFTQ0121" in fulltext
    plectritis = fulltext["CFTQ0121"]
    assert plectritis["programme_identity"] == "P2_CF01_PLECTRITIS_ISLAND_CONNECTIVITY_2015"
    assert plectritis["quantitative_gate_status"] == "blocked_public_site_level_connectivity_IF_values_not_recoverable"
    assert "12 source localities" in plectritis["independent_unit"]
    assert int(plectritis["pair_programme_increment"]) == 0
    assert plectritis["effect_calculation_opened"] == "no"

    assert "CFTQ0124" in fulltext
    cabralea = fulltext["CFTQ0124"]
    assert cabralea["programme_identity"] == "P2_CF01_CABRALEA_2015"
    assert cabralea["quantitative_gate_status"] == "blocked_public_four_site_IF_values_not_recoverable"
    for token in ("F1", "F2", "C1", "C2"):
        assert token in cabralea["independent_unit"]
    assert int(cabralea["pair_programme_increment"]) == 0
    assert cabralea["effect_calculation_opened"] == "no"

    assert "CFTQ0135" in fulltext
    comarum = fulltext["CFTQ0135"]
    assert comarum["programme_identity"] == "P2_CF01_COMARUM_2014"
    assert comarum["quantitative_gate_status"] == "blocked_population_level_open_seed_set_not_recoverable_without_figure_digitization"
    assert "14 Belgian populations" in comarum["independent_unit"]
    assert int(comarum["pair_programme_increment"]) == 0
    assert comarum["effect_calculation_opened"] == "no"

    assert "CFTQ0142" in fulltext
    acer_m = fulltext["CFTQ0142"]
    assert acer_m["programme_identity"] == "P2_CF01_ACER_MIYABEI_2014"
    assert acer_m["quantitative_gate_status"] == "recovered_gradient_generalisation_multilayer_cluster_retrospective"
    assert "21 source forests" in acer_m["independent_unit"]
    assert "9 forests" in acer_m["independent_unit"]
    assert int(acer_m["pair_programme_increment"]) == 0
    assert acer_m["effect_calculation_opened"] == "yes"

    assert "CFTQ0155" in fulltext
    aext = fulltext["CFTQ0155"]
    assert aext["programme_identity"] == "P2_CF01_AEXTOXICON_2013"
    assert aext["quantitative_gate_status"] == "close_no_common_patch_level_C_effect_unit"
    assert int(aext["pair_programme_increment"]) == 0
    assert aext["effect_calculation_opened"] == "no"

    assert "CFTQ0156" in fulltext
    sch = fulltext["CFTQ0156"]
    assert sch["programme_identity"] == "P2_CF01_SCHUEPP_CHERRY_2014"
    assert sch["quantitative_gate_status"] == "blocked_public_common_site_IF_vectors_not_recoverable"
    assert "30 maximum sites" in sch["independent_unit"]
    assert int(sch["pair_programme_increment"]) == 0
    assert sch["effect_calculation_opened"] == "no"

    assert "CFTQ0162" in fulltext
    celtis = fulltext["CFTQ0162"]
    assert celtis["programme_identity"] == "P2_CF01_CELTIS_MODIFIED_FORESTS_2013"
    assert celtis["quantitative_gate_status"] == "close_no_single_response_free_fragmentation_estimand"
    assert "36 sites total" in celtis["independent_unit"]
    assert int(celtis["pair_programme_increment"]) == 0
    assert celtis["effect_calculation_opened"] == "no"

    assert "CFTQ0165" in fulltext
    anax = fulltext["CFTQ0165"]
    assert anax["programme_identity"] == "P2_CF01_ANAXAGOREA_2012"
    assert anax["quantitative_gate_status"] == "blocked_common_six_fragment_fruit_set_not_recoverable"
    assert "3 small + 3 large" in anax["independent_unit"]
    assert int(anax["pair_programme_increment"]) == 0
    assert anax["effect_calculation_opened"] == "no"

    assert "CFTQ0166" in fulltext
    card = fulltext["CFTQ0166"]
    assert card["programme_identity"] == "P2_CF01_CARDIOPETALUM_2012"
    assert card["quantitative_gate_status"] == "recovered_gradient_generalisation_multilayer_cluster_retrospective"
    assert "10 Table-1 fragments" in card["independent_unit"]
    assert int(card["pair_programme_increment"]) == 0
    assert card["effect_calculation_opened"] == "yes"

    assert "CFTQ0171" in fulltext
    attalea = fulltext["CFTQ0171"]
    assert attalea["programme_identity"] == "P2_CF01_ATTALEA_HUMILIS_2012"
    assert attalea["identity_status"] == "linked_companion_programme_same_fragment_system"
    assert attalea["quantitative_gate_status"] == "blocked_linked_four_fragment_CF_values_not_recoverable"
    for token in ("AJ-19", "SH-57", "UN-2400", "PA-3500"):
        assert token in attalea["fragmentation_exposure_status"]
    assert int(attalea["pair_programme_increment"]) == 0
    assert attalea["effect_calculation_opened"] == "no"

    assert "CFTQ0187" in fulltext
    myrm = fulltext["CFTQ0187"]
    assert myrm["programme_identity"] == "P2_CF01_MYRMECOPHILA_2011"
    assert myrm["quantitative_gate_status"] == "pending_fulltext_fragmentation_estimand_and_common_population_frame"
    assert "14 maximum populations" in myrm["independent_unit"]
    assert "pollen limitation" in myrm["I_endpoint"]
    assert int(myrm["pair_programme_increment"]) == 0
    assert myrm["effect_calculation_opened"] == "no"

    assert "CFTQ0202" in fulltext
    bart = fulltext["CFTQ0202"]
    assert bart["programme_identity"] == "P2_CF01_BARTOMEUS_2010"
    assert bart["quantitative_gate_status"] == "pending_landscape_estimand_radius_and_common_Raphanus_IF_frame"
    assert "14 independent landscapes" in bart["independent_unit"]
    assert int(bart["pair_programme_increment"]) == 0
    assert bart["effect_calculation_opened"] == "no"

    assert "CFTQ0204" in fulltext
    uri = fulltext["CFTQ0204"]
    assert uri["programme_identity"] == "P2_CF01_HELICONIA_URIARTE_2010"
    assert uri["quantitative_gate_status"] == "retain_C_D_seed_limitation_close_CF_no_direct_observed_F"
    assert "4 fragment + 6 continuous plots" in uri["independent_unit"]
    assert int(uri["pair_programme_increment"]) == 0
    assert uri["effect_calculation_opened"] == "no"

    assert "CFTQ0206" in fulltext
    braun = fulltext["CFTQ0206"]
    assert braun["programme_identity"] == "P2_CF01_BRAUN_THESIS_2010"
    assert braun["identity_status"] == "linked_umbrella_thesis_source_no_new_programme"
    assert braun["quantitative_gate_status"] == "linked_umbrella_source_no_new_K"
    assert int(braun["pair_programme_increment"]) == 0
    assert braun["effect_calculation_opened"] == "no"

    assert "CFTQ0209" in fulltext
    byr = fulltext["CFTQ0209"]
    assert byr["programme_identity"] == "P2_CF01_BYRSONIMA_2009"
    assert byr["quantitative_gate_status"] == "blocked_fragment_level_IF_dispersion_and_dependence_not_recoverable"
    assert "six fragments total" in byr["independent_unit"]
    assert int(byr["pair_programme_increment"]) == 0
    assert byr["effect_calculation_opened"] == "no"

    assert "CFTQ0215" in fulltext
    lep = fulltext["CFTQ0215"]
    assert lep["programme_identity"] == "P2_CF01_LEPTONYCHIA_2003_2009"
    assert lep["quantitative_gate_status"] == "pending_linked_2003_2009_site_and_campaign_alignment"
    assert "forest fragment / continuous-forest habitat unit" in lep["independent_unit"]
    assert int(lep["pair_programme_increment"]) == 0
    assert lep["effect_calculation_opened"] == "no"

    assert "CFTQ0229" in fulltext
    diek = fulltext["CFTQ0229"]
    assert diek["programme_identity"] == "P2_CF01_DIEKOETTER_2007"
    assert diek["quantitative_gate_status"] == "pending_factorial_fragmentation_estimand_and_independent_unit_recovery"
    assert "experimental habitat unit/landscape replicate" in diek["independent_unit"]
    assert int(diek["pair_programme_increment"]) == 0
    assert diek["effect_calculation_opened"] == "no"

    assert "CFTQ0235" in fulltext
    artz = fulltext["CFTQ0235"]
    assert artz["programme_identity"] == "P2_CF01_ARTZ_ASCLEPIAS_2006"
    assert artz["quantitative_gate_status"] == "blocked_repeated_island_IF_effect_unit_not_recoverable"
    assert "11 total" in artz["independent_unit"]
    assert "tree island" in artz["independent_unit"]
    assert int(artz["pair_programme_increment"]) == 0
    assert artz["effect_calculation_opened"] == "no"

    assert "CFTQ0263" in fulltext
    brun = fulltext["CFTQ0263"]
    assert brun["programme_identity"] == "P2_CF01_BRUNSVIGIA_RADULOSA_2005"
    assert brun["quantitative_gate_status"] == "pending_fragment_area_or_isolation_estimand_and_common_population_IF_frame"
    assert "population/site" in brun["independent_unit"]
    assert int(brun["pair_programme_increment"]) == 0
    assert brun["effect_calculation_opened"] == "no"

    assert "CFTQ0267" in fulltext
    ques = fulltext["CFTQ0267"]
    assert ques["programme_identity"] == "P2_CF01_QUESADA_BOMBACACEOUS_2004"
    assert ques["quantitative_gate_status"] == "pending_species_specific_common_IF_effect_unit_and_dependence_recovery"
    assert "tree/local-context observational unit" in ques["independent_unit"]
    assert int(ques["pair_programme_increment"]) == 0
    assert ques["effect_calculation_opened"] == "no"

    assert "CFTQ0272" in fulltext
    coff = fulltext["CFTQ0272"]
    assert coff["programme_identity"] == "P2_CF01_COFFEA_SULAWESI_2003"
    assert coff["quantitative_gate_status"] == "recovery_contract_frozen_site_level_distance_bee_openfruit_vectors_pending"
    assert "15 independent sites" in coff["independent_unit"]
    assert int(coff["pair_programme_increment"]) == 0
    assert coff["effect_calculation_opened"] == "no"

    assert "CFTQ0278" in fulltext
    cat = fulltext["CFTQ0278"]
    assert cat["programme_identity"] == "P2_CF01_CATASETUM_2002"
    assert cat["quantitative_gate_status"] == "recovery_contract_frozen_1997_ten_site_common_IF_values_pending"
    assert "5 island + 5 mainland sites" in cat["independent_unit"]
    assert int(cat["pair_programme_increment"]) == 0
    assert cat["effect_calculation_opened"] == "no"

    assert "CFTQ0283" in fulltext
    ach = fulltext["CFTQ0283"]
    assert ach["programme_identity"] == "P2_CF01_ACHILLEA_ISOLATION_2002"
    assert ach["quantitative_gate_status"] == "blocked_island_replicate_count_and_fragment_level_IF_variance_not_publicly_recoverable"
    assert "island is the required fragmentation unit" in ach["independent_unit"]
    assert int(ach["pair_programme_increment"]) == 0
    assert ach["effect_calculation_opened"] == "no"

    assert "CFTQ0286" in fulltext
    cal = fulltext["CFTQ0286"]
    assert cal["programme_identity"] == "P2_CF01_CALYSTEGIA_2001"
    assert cal["quantitative_gate_status"] == "blocked_outcrop_level_IF_marginals_and_dispersion_not_publicly_recoverable"
    assert "serpentine outcrop is the required independent habitat unit" in cal["independent_unit"]
    assert int(cal["pair_programme_increment"]) == 0
    assert cal["effect_calculation_opened"] == "no"

    assert "CFTQ0301" in fulltext
    sm = fulltext["CFTQ0301"]
    assert sm["programme_identity"] == "P2_CF01_SPONDIAS_MOMBIN_1997"
    assert sm["quantitative_gate_status"] == "pending_common_population_CF_effect_unit_and_fruit_production_recovery"
    assert "Spondias population/forest-fragment unit" in sm["independent_unit"]
    assert int(sm["pair_programme_increment"]) == 0
    assert sm["effect_calculation_opened"] == "no"

    assert "CFTQ0312" in fulltext
    mangrove = fulltext["CFTQ0312"]
    assert mangrove["programme_identity"] == "P2_CF01_MANGROVE_HERMANSEN_2017"
    assert mangrove["quantitative_gate_status"] == "pending_18stand_common_IF_values_and_estuary_block_recovery"
    assert "18 stands maximum" in mangrove["independent_unit"]
    assert int(mangrove["pair_programme_increment"]) == 0
    assert mangrove["effect_calculation_opened"] == "no"

    assert "CFTQ0313" in fulltext
    banksia32 = fulltext["CFTQ0313"]
    assert banksia32["programme_identity"] == "P2_CF01_BANKSIA_CAesia_2012_2013"
    assert banksia32["quantitative_gate_status"] == "pending_linked_2012_2013_population_and_campaign_alignment"
    assert int(banksia32["pair_programme_increment"]) == 0

    assert "CFTQ0314" in fulltext
    kodagu = fulltext["CFTQ0314"]
    assert kodagu["quantitative_gate_status"] == "blocked_common_location_level_IF_effect_not_recoverable_from_published_nested_analysis"
    assert int(kodagu["pair_programme_increment"]) == 0

    assert "CFTQ0315" in fulltext
    myrtus = fulltext["CFTQ0315"]
    assert myrtus["programme_identity"] == "P2_CF01_MYRTUS_2009"
    assert myrtus["quantitative_gate_status"] == "pending_six_population_IF_values_and_fragment_class_variance_recovery"
    assert "six populations maximum" in myrtus["independent_unit"]
    assert int(myrtus["pair_programme_increment"]) == 0

    assert "CFTQ0316" in fulltext
    astro = fulltext["CFTQ0316"]
    assert astro["quantitative_gate_status"] == "blocked_exact_fragment_level_F_effect_not_recoverable_without_figure_digitization"
    assert "forest fragment; n=6" in astro["independent_unit"]

    assert "CFTQ0317" in fulltext
    poly = fulltext["CFTQ0317"]
    assert poly["quantitative_gate_status"] == "blocked_fragment_level_IF_aggregation_not_recoverable_from_published_tree_level_summary"
    assert "forest fragment is required independent unit" in poly["independent_unit"]

    for thesis_id in ("CFTQ0318", "CFTQ0319"):
        assert thesis_id in fulltext
        assert fulltext[thesis_id]["quantitative_gate_status"] == "pending_thesis_chapter_identity_mapping_no_new_K"
        assert int(fulltext[thesis_id]["pair_programme_increment"]) == 0

    assert "CFTQ0320" in fulltext
    hass_thesis = fulltext["CFTQ0320"]
    assert hass_thesis["programme_identity"] == "P2_CF01_HASS_THESIS_2019"
    assert hass_thesis["quantitative_gate_status"] == "linked_umbrella_source_no_new_K"
    assert int(hass_thesis["pair_programme_increment"]) == 0

    assert "CFTQ0322" in fulltext
    linaria = fulltext["CFTQ0322"]
    assert linaria["programme_identity"] == "P2_CF01_LINARIA_URBAN_2019"
    assert linaria["quantitative_gate_status"] == "pending_urbanization_metric_population_frame_and_I_endpoint_recovery"
    assert int(linaria["pair_programme_increment"]) == 0

    assert "CFTQ0324" in fulltext
    erica = fulltext["CFTQ0324"]
    assert erica["programme_identity"] == "P2_CF01_ERICA_ANGOH_2016"
    assert erica["quantitative_gate_status"] == "pending_20patch_visitation_and_viable_seed_set_vector_recovery"
    assert "habitat patch; n=20 maximum" in erica["independent_unit"]
    assert int(erica["pair_programme_increment"]) == 0
    assert erica["effect_calculation_opened"] == "no"

    assert "CFTQ0325" in fulltext
    ritchie = fulltext["CFTQ0325"]
    assert ritchie["programme_identity"] == "P2_CF01_RITCHIE_THESIS_2015"
    assert ritchie["quantitative_gate_status"] == "linked_umbrella_source_no_new_K"
    assert int(ritchie["pair_programme_increment"]) == 0

    assert "CFTQ0329" in fulltext
    angadenia = fulltext["CFTQ0329"]
    assert angadenia["programme_identity"] == "P2_CF01_ANGADENIA_2015"
    assert angadenia["quantitative_gate_status"] == "pending_dissertation_chapter_common_fragmentation_IF_frame"
    assert int(angadenia["pair_programme_increment"]) == 0
    assert angadenia["effect_calculation_opened"] == "no"

    assert "CFTQ0333" in fulltext
    pv_thesis = fulltext["CFTQ0333"]
    assert pv_thesis["quantitative_gate_status"] == "linked_umbrella_source_no_new_K"
    assert int(pv_thesis["pair_programme_increment"]) == 0

    assert "CFTQ0334" in fulltext
    spring = fulltext["CFTQ0334"]
    assert spring["programme_identity"] == "P2_CF01_SCHLOTMAN_2011"
    assert spring["quantitative_gate_status"] == "pending_fragment_ids_common_Bombus_species_F_frames_and_site_level_values"
    assert int(spring["pair_programme_increment"]) == 0
    assert spring["effect_calculation_opened"] == "no"

    assert "CFTQ0338" in fulltext
    eagg = fulltext["CFTQ0338"]
    assert eagg["quantitative_gate_status"] == "pending_thesis_chapter_publication_identity_and_common_CF_or_IF_frame"
    assert int(eagg["pair_programme_increment"]) == 0

    assert "CFTQ0340" in fulltext
    saint = fulltext["CFTQ0340"]
    assert saint["quantitative_gate_status"] == "linked_umbrella_source_no_new_K"
    assert int(saint["pair_programme_increment"]) == 0

    assert "CFTQ0344" in fulltext
    cramer = fulltext["CFTQ0344"]
    assert cramer["programme_identity"] == "P2_CF01_CRAMER_DUCKEODENDRON_2007"
    assert cramer["quantitative_gate_status"] == "pending_Duckeodendron_11tree_common_CF_values_model_variance_and_forest_nesting_recovery"
    assert "11 adult trees" in cramer["independent_unit"]
    assert int(cramer["pair_programme_increment"]) == 0

    assert "CFTQ0345" in fulltext
    ottewell = fulltext["CFTQ0345"]
    assert ottewell["quantitative_gate_status"] == "linked_thesis_to_primary_publications_pending_common_effect_unit_mapping_no_new_K"
    assert "10.1016/j.biocon.2008.12.019" in ottewell["fragmentation_exposure_status"]
    assert int(ottewell["pair_programme_increment"]) == 0

    assert "CFTQ0349" in fulltext
    kenya = fulltext["CFTQ0349"]
    assert kenya["programme_identity"] == "P2_CF01_BERGSDORF_KAKAMEGA_2006"
    assert kenya["quantitative_gate_status"] == "pending_species_campaign_site_replication_and_common_IF_frames"
    assert int(kenya["pair_programme_increment"]) == 0

    assert "CFTQ0350" in fulltext
    pritchard = fulltext["CFTQ0350"]
    assert pritchard["programme_identity"] == "P2_CF01_PRITCHARD_2005"
    assert pritchard["quantitative_gate_status"] == "pending_crop_site_isolation_IF_vectors_and_multicrop_identity_recovery"
    assert int(pritchard["pair_programme_increment"]) == 0

    assert "CFTQ0355" in fulltext
    llorens = fulltext["CFTQ0355"]
    assert llorens["quantitative_gate_status"] == "linked_umbrella_source_no_new_K"
    assert int(llorens["pair_programme_increment"]) == 0

    assert "CFTQ0356" in fulltext
    buerger = fulltext["CFTQ0356"]
    assert buerger["programme_identity"] == "P2_CF01_BUERGER_2004"
    assert buerger["quantitative_gate_status"] == "pending_chapter_identity_site_overlap_landscape_radius_and_common_IF_frame"
    assert int(buerger["pair_programme_increment"]) == 0
    assert buerger["effect_calculation_opened"] == "no"

    assert "CFTQ0357" in fulltext
    klein_thesis = fulltext["CFTQ0357"]
    assert klein_thesis["programme_identity"] == "P2_CF01_COFFEA_SULAWESI_2003"
    assert klein_thesis["quantitative_gate_status"] == "linked_umbrella_source_no_new_K"
    assert "15-site" in klein_thesis["fragmentation_exposure_status"]
    assert int(klein_thesis["pair_programme_increment"]) == 0

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
        assert has_token(bdffp_status, token), token

    hass_contract = HASS_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "94 independent 1-km² agricultural landscapes",
        "229 focal fields",
        "independent EGWEE unit = landscape",
        "Primary I = **wild-bee abundance**",
        "Primary F = **mean radish seeds per pod**",
        "fragmentation_severity = - field_border_density",
    ):
        assert has_token(hass_contract, token), token

    hass_schema = json.loads(HASS_SCHEMA.read_text(encoding="utf-8"))
    assert hass_schema["candidate"] == "CFTQ0084"
    assert hass_schema["access_status"] == "public_s3_access_blocked"
    assert hass_schema["effect_outcomes_opened"] is False
    assert hass_schema["numeric_effects_calculated"] is False

    hass_status = HASS_STATUS.read_text(encoding="utf-8")
    for token in (
        "public S3 access: **blocked**",
        "access boundary, not an ecological result",
        "Do not",
        "digitised figures",
    ):
        assert has_token(hass_status, token), token

    thai_contract = THAI_ORCHARD_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "10 matched pairs of mixed-fruit orchards",
        "Primary independent unit = **orchard**",
        "Primary direct fragmentation contrast = **far from forest versus near forest**",
        "Mandatory species rule",
        "rambutan",
        "durian",
        "mango",
        "primary I = **flower visitation frequency**",
        "primary F = **fruit set**",
        "p_programme = min(1, 3 * min(p_rambutan, p_durian, p_mango))",
    ):
        assert has_token(thai_contract, token), token

    thai_access = json.loads(THAI_ORCHARD_ACCESS.read_text(encoding="utf-8"))
    assert thai_access["candidate"] == "CFTQ0103"
    assert thai_access["access_status"] == "design_valid_public_orchard_level_IF_data_not_recoverable"
    assert thai_access["direct_IF_programme_increment"] == 0
    assert thai_access["effect_outcomes_opened"] is False
    assert thai_access["orchard_level_effects_calculated"] is False
    assert len(thai_access["design"]["crops"]) == 3

    thai_status = THAI_ORCHARD_STATUS.read_text(encoding="utf-8")
    for token in (
        "quantitatively blocked by orchard-level data recoverability",
        "files are marked **restricted**",
        "direct I-F programme increment: **0**",
        "direct I-F coverage remains **1/5 (ML020 only)**",
        "not an ecological null",
    ):
        assert has_token(thai_status, token), token

    plectritis_contract = PLECTRITIS_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "12 Plectritis congesta sampling localities",
        "N = 13 sites",
        "Independent unit = **Plectritis population/site**",
        "12-locality map versus N=13 visitation-model denominator",
        "habitat connectivity within a 1-km radius",
        "Primary I = **total floral visitation rate to Plectritis congesta**",
        "Primary F = **Plectritis seed production / maternal female fitness**",
        "fragmentation_severity = - source_connectivity",
    ):
        assert has_token(plectritis_contract, token), token

    cabralea_contract = CABRALEA_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "three fragmented and three continuous Atlantic-forest sites",
        "Independent unit = **forest site**",
        "fragmented: F1 + F2",
        "reference: C1 + C2",
        "Primary I = **pollinator visit frequency: number of flower visits per 30 min**",
        "Primary F = **number of developed fruits per sampled tree**",
        "very small 2+2 common denominator",
        "only four paired site observations",
    ):
        assert has_token(cabralea_contract, token), token

    plectritis_access = PLECTRITIS_ACCESS.read_text(encoding="utf-8")
    for token in (
        "design-valid, quantitatively blocked by site-denominator reconciliation and site-level effect-unit recoverability",
        "12 named localities",
        "N = 13 sites",
        "not an ecological null",
        "choose 12 or 13 sites",
        "digitize figures",
    ):
        assert has_token(plectritis_access, token), token

    cabralea_access = CABRALEA_ACCESS.read_text(encoding="utf-8")
    for token in (
        "design-valid, quantitatively blocked by four-site effect-unit recoverability",
        "F1, F2",
        "C1, C2",
        "not a null I-F result",
        "group-level SD",
    ):
        assert has_token(cabralea_access, token), token

    comarum_contract = COMARUM_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "14 Belgian populations of Comarum palustre",
        "Independent fragmentation unit = **population/site**",
        "population isolation / landscape woody-area cover within",
        "Primary I = **total direct pollinator visitation rate to C. palustre**",
        "Primary F = **open-pollinated viable seed set**",
        "population-year rows as independent fragmentation units",
    ):
        assert has_token(comarum_contract, token), token

    comarum_access = COMARUM_ACCESS.read_text(encoding="utf-8")
    for token in (
        "design-valid, quantitatively blocked by population-level F recoverability",
        "Table 1 publishes",
        "Figure 3",
        "No EGWEE Fisher-z effect was calculated",
        "digitize Figure 3",
    ):
        assert has_token(comarum_access, token), token

    aextoxicon_anchor = AEXTOXICON_ANCHOR.read_text(encoding="utf-8")
    for token in (
        "close_no_common_patch_level_C_effect_unit",
        "movement-compensation / source-limitation anchor",
        "pooled small-patch immigrant-seed proportion is reported as 40%",
        "Direct C-F programme increment: **0**",
    ):
        assert has_token(aextoxicon_anchor, token), token

    schuepp_contract = SCHUEPP_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "30 spatially separated landscape sectors",
        "Independent unit = **landscape sector / experimental site**",
        "Primary exposure = **distance to the nearest woody habitat**",
        "Primary I = **site-level pollinator visitation rate to cherry flowers**",
        "Primary F = **site-level open/control fruit set**",
        "retrospective external recovery",
    ):
        assert has_token(schuepp_contract, token), token

    schuepp_access = SCHUEPP_ACCESS.read_text(encoding="utf-8")
    for token in (
        "design-valid, quantitatively blocked by common-site I/F vector recoverability",
        "30 spatially separated landscape sectors",
        "does **not** expose one authoritative table",
        "No EGWEE Fisher-z effect was calculated",
        "Gradient programme increment: **0**",
        "digitize response figures",
    ):
        assert has_token(schuepp_access, token), token

    celtis_gate = CELTIS_GATE.read_text(encoding="utf-8")
    for token in (
        "close_no_single_response_free_fragmentation_estimand",
        "36 study sites",
        "forest-modification factor",
        "assign equally spaced severity scores 1–6",
        "process-decoupling / service-persistence anchor",
        "Quantitative I-F programme increment: **0**",
    ):
        assert has_token(celtis_gate, token), token

    anaxagorea_contract = ANAXAGOREA_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "three large Atlantic-rainforest fragments",
        "fragments (6–14 ha)",
        "Independent unit = **forest fragment**",
        "Primary I = **pollinator abundance per flower**",
        "Primary F = **fruit set = fruits per flower**",
        "retrospective external recovery",
    ):
        assert has_token(anaxagorea_contract, token), token

    anaxagorea_access = ANAXAGOREA_ACCESS.read_text(encoding="utf-8")
    for token in (
        "design-valid, quantitatively blocked by common six-fragment F effect-unit recovery",
        "only fragments **A, B and D**",
        "Direct I-F programme increment: **0**",
        "mature fruits per tree",
        "use 186 or 209 flowers as fragmentation n",
    ):
        assert has_token(anaxagorea_access, token), token

    attalea_gate = ATTALEA_GATE.read_text(encoding="utf-8")
    for token in (
        "one ecological programme",
        "AJ-19 + SH-57",
        "UN-2400 + PA-3500",
        "blocked_linked_four_fragment_CF_values_not_recoverable",
        "Direct C-F programme increment: **0**",
        "reproduction–movement trade-off / compensation anchor",
    ):
        assert has_token(attalea_gate, token), token

    cardiopetalum_rule = CARDIOPETALUM_RULE.read_text(encoding="utf-8")
    for token in (
        "10 independent cerrado forest fragments",
        "fragmentation_severity = -log(fragment_area_ha)",
        "Primary I = **pollinator abundance per flower (ABP)**",
        "Primary F = **fruit set per flower (F)**",
        "retrospective external recovery",
        "contributes **zero** primary direct Hedges-g I-F programmes",
    ):
        assert has_token(cardiopetalum_rule, token), token

    cardiopetalum_result = CARDIOPETALUM_RESULT.read_text(encoding="utf-8")
    for token in (
        "independent forest fragments: **10**",
        "Fisher z = **−0.245**",
        "Fisher z = **−1.684**",
        "I − F = **+1.439**",
        "95% CI = **[+0.483, +2.394]**",
        "p = **0.00316**",
        "interaction persistence with reproductive collapse",
    ):
        assert has_token(cardiopetalum_result, token), token

    myrm_gate = MYRMECOPHILA_GATE.read_text(encoding="utf-8")
    for token in (
        "14 populations",
        "fragment size/area",
        "habitat disturbance / affectation",
        "pollen limitation",
        "one response-free fragmentation estimand",
        "Do not",
        "choose fragment area versus disturbance",
    ):
        assert has_token(myrm_gate, token), token

    bart_gate = BARTOMEUS_GATE.read_text(encoding="utf-8")
    for token in (
        "14 independent riparian sites",
        "500–3000 m radii",
        "one landscape-severity variable",
        "one spatial radius",
        "Do not",
        "choose agricultural versus forest versus grassland cover by significance",
    ):
        assert has_token(bart_gate, token), token

    uri_gate = HELICONIA_URIARTE_GATE.read_text(encoding="utf-8")
    for token in (
        "four plots in 1-ha forest fragments",
        "six plots in continuous forest",
        "20 fruits × 3 seeds per inflorescence",
        "retain C-D / seed-limitation process anchor",
        "close direct C-F",
        "No C-F Hedges-g effect is calculated",
    ):
        assert has_token(uri_gate, token), token

    byr_gate = BYRSONIMA_GATE.read_text(encoding="utf-8")
    for token in (
        "small fragments: SF1 = 0.22 ha",
        "large fragments: LF1 = 36 ha",
        "160 min per fragment",
        "design-valid direct I-F candidate",
        "fragmentation-unit marginal",
        "cluster-robust fallback",
        "Direct I-F coverage remains unchanged",
    ):
        assert has_token(byr_gate, token), token

    lep_gate = LEPTONYCHIA_GATE.read_text(encoding="utf-8")
    for token in (
        "four small forest fragments",
        "2, 9, 13 and 31 ha",
        "diminished fecundity",
        "Same species + same region + linked citations are not sufficient",
        "linked-campaign",
        "direct C-F increment = 0",
    ):
        assert has_token(lep_gate, token), token

    diek_gate = DIEKOETTER_GATE.read_text(encoding="utf-8")
    for token in (
        "habitat area",
        "habitat fragmentation / configuration",
        "matrix composition",
        "genuine experimental I-F candidate",
        "one response-independent fragmentation estimand shared by I and F",
        "small + bare ground",
        "direct I-F programme increment = **0**",
    ):
        assert has_token(diek_gate, token), token

    artz_gate = ARTZ_GATE.read_text(encoding="utf-8")
    for token in (
        "11 bayhead tree islands",
        "5 small islands",
        "6 large islands",
        "25 m",
        "700–1000 m",
        "tree island (n=11)",
        "blocked_repeated_island_IF_effect_unit_not_recoverable",
        "n=40",
        "n=48",
        "effect-unit/reporting limitation, not an ecological null",
    ):
        assert has_token(artz_gate, token), token

    brun_gate = BRUNSVIGIA_GATE.read_text(encoding="utf-8")
    for token in (
        "habitat fragment area",
        "population isolation",
        "Population size remains a separate demographic / mate-availability moderator",
        "Independent unit = population/site",
        "Primary candidate I = population-level pollen limitation",
        "Primary candidate F = population-level direct seed production per plant",
        "Do not",
        "choose population size because it is the strongest published predictor",
    ):
        assert has_token(brun_gate, token), token

    ques_gate = QUESADA_GATE.read_text(encoding="utf-8")
    for token in (
        "three species are **dependent panels inside one publication programme**",
        "filmed flowers/inflorescences",
        "Primary I candidate = total bat visitation rate",
        "Primary F candidate = fruit set",
        "At most **one direct I-F programme increment**",
        "cluster-robust",
        "cannot be counted as independent K",
    ):
        assert has_token(ques_gate, token), token

    coffea_contract = COFFEA_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "15 coffee agroforestry systems",
        "distance to nearest old-growth rainforest / forest margin",
        "Independent unit = **agroforestry system/site**",
        "Primary I = **total coffee flower-visiting bee abundance / visitation",
        "Primary F = **open-pollinated coffee fruit set**",
        "Do not",
        "choose social bees because distance to forest is strongest for that guild",
    ):
        assert has_token(coffea_contract, token), token

    catasetum_contract = CATASETUM_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "10 Panama Canal island sites",
        "five island sites",
        "five mainland sites",
        "1997 ten-site overlap",
        "Independent unit = **site/population**",
        "Primary I = **1997 site-level abundance of Eulaema cingulata**",
        "Primary F = **1997 female reproductive success measured as fruit set**",
        "cluster-robust fallback",
        "choose 1996 or 1998 because fruit-set differences were stronger",
    ):
        assert has_token(catasetum_contract, token), token

    ach_gate = ACHILLEA_GATE.read_text(encoding="utf-8")
    for token in (
        "isolated and non-isolated",
        "Independent fragmentation unit = **island**",
        "pollen deposition and fecundity",
        "blocked_island_replicate_count_and_fragment_level_IF_variance_not_publicly_recoverable",
        "not an ecological null",
        "Do not use individual transplants as island n",
    ):
        assert has_token(ach_gate, token), token

    cal_gate = CALYSTEGIA_GATE.read_text(encoding="utf-8")
    for token in (
        "16 small serpentine outcrops",
        "7 large serpentine outcrops",
        "39 plant patches",
        "Independent habitat unit = **serpentine outcrop**",
        "n=23 maximum",
        "blocked_outcrop_level_IF_marginals_and_dispersion_not_publicly_recoverable",
        "Never promote the 39 plant patches",
    ):
        assert has_token(cal_gate, token), token

    spond_gate = SPONDIAS_MOMBIN_GATE.read_text(encoding="utf-8")
    for token in (
        "P2_CF01_SPONDIAS_MOMBIN_1997",
        "90–100% pollen immigration",
        "80–1000 m",
        "Primary fragmented condition = **small island fragments**",
        "Primary reference condition = the source continuous-forest populations **FDP + LC**",
        "larger island/fragment **DL**",
        "Primary C = population-level pollen immigration",
        "Primary F = population-level fruit production / fecundity",
        "five *Ficus* species",
        "do not increase C-F programme K",
        "cluster-robust fallback",
    ):
        assert has_token(spond_gate, token), token

    mangrove_gate = MANGROVE_GATE.read_text(encoding="utf-8")
    for token in (
        "large: >1500 trees",
        "medium: 300–500 trees",
        "small: <50 trees",
        "Independent unit = **mangrove stand**",
        "Estuary is a source blocking factor",
        "Primary F candidate = direct fruit production",
        "Do not",
        "collapse medium stands into small or large after inspecting effect strength",
    ):
        assert has_token(mangrove_gate, token), token

    myrtus_gate = MYRTUS_GATE.read_text(encoding="utf-8")
    for token in (
        "six source populations",
        "Independent unit = **population/site**",
        "Primary direct contrast candidate = source Large versus Small",
        "broad population-level total visitation rate",
        "natural fruit set",
        "Honeybee-only or native-bee-only responses are sensitivities",
        "Do not",
        "use flowers or plants as n",
    ):
        assert has_token(myrtus_gate, token), token

    buerger_gate = BUERGER_GATE.read_text(encoding="utf-8")
    for token in (
        "P2_CF01_BUERGER_2004",
        "five studies/chapters",
        "Independent unit = **landscape/site**",
        "one response-free landscape variable",
        "one source-supported radius",
        "Brassica napus",
        "choose 750 m versus 3000 m by effect size",
        "validation of an EGWE/NEE finite operator",
    ):
        assert has_token(buerger_gate, token), token

    completion = COVERAGE_COMPLETION.read_text(encoding="utf-8")
    for token in (
        "screened: **360 / 360**",
        "screening waves: **36 × 10 candidates**",
        "advanced to full-text/design/effect-unit gate: **66**",
        "linked to an existing/umbrella programme identity: **8**",
        "closed at screening/design stage: **286**",
        "unscreened candidates: **0**",
        "search-completion stopping rule",
        "I-F: **1 / 5 independent programmes**",
        "C-F: **2 / 5 independent programmes**",
        "G_adult-G_offspring: **5 / 5 independent programmes**",
        "5 programmes / 17 primary Fisher-z marginal effects",
        "EGWEE search completion is **not** validation of a finite EGWE operator sequence",
    ):
        assert has_token(completion, token), token

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
        assert has_token(gate_status, token), token

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
        assert has_token(contract, token), token

    print(
        "PHASE2_CF01_TARGET_PAIR_SCREEN_OK "
        "queue=360 screened=360 pending=0 wave3_advance=1 wave4_advance=0 wave5_advance=1 wave6_advance=2 wave7_advance=3 wave8_advance=1 wave9_advance=2 wave10_advance=0 wave11_advance=1 wave12_advance=1 wave12_link_existing=1 wave13_advance=2 wave14_advance=1 wave15_advance=1 wave16_advance=2 wave17_advance=3 wave18_advance=1 wave19_advance=1 wave20_advance=0 wave21_advance=3 wave21_link_existing=1 wave22_advance=1 wave23_advance=1 wave24_advance=1 wave25_advance=0 wave26_advance=0 wave27_advance=2 wave28_advance=2 wave29_advance=2 wave30_advance=0 wave31_advance=1 wave32_advance=8 wave32_link_existing=1 wave33_advance=3 wave33_link_existing=1 wave34_advance=2 wave34_link_existing=2 wave35_advance=4 wave36_advance=1 wave36_link_existing=2 search_complete=1 "
        "brassica_increment=0 milkweed_gradient_increment=1 phacelia_increment=0 hedysarum_increment=0 "
        "bdffp_access_stop=1 hass_access_stop=1 aloe_pending=1 thai_orchard_access_stop=1 brudvig_link_noK=1 acer_CF_increment=0 plectritis_access_stop=1 cabralea_access_stop=1 comarum_access_stop=1 acer_miyabei_gradient_admitted=1 aextoxicon_anchor_noK=1 schuepp_access_stop=1 celtis_estimand_stop=1 anaxagorea_access_stop=1 cardiopetalum_gradient_admitted=1 attalea_linked_stop=1 myrmecophila_estimand_pending=1 herrera_CD_anchor_noK=1 bartomeus_estimand_pending=1 uriarte_CD_anchor_noK=1 braun_umbrella_noK=1 byrsonima_variance_stop=1 leptonychia_linked_pending=1 diekoetter_factorial_pending=1 artz_repeated_island_stop=1 wave25_noK=1 wave26_noK=1 brunsvigia_estimand_pending=1 quesada_effect_unit_pending=1 coffea_gradient_pending=1 catasetum_direct_IF_pending=1 achillea_effect_unit_stop=1 calystegia_effect_unit_stop=1 wave30_noK=1 spondias_mombin_CF_pending=1 bdffp_increment=0 ophrys_increment=0 brazil_nut_CF_increment=0 primary_IF_increment=0 direct_IF=1/5 direct_CF=2/5"
    )


if __name__ == "__main__":
    main()
