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


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for p in (
        QUEUE, SCREEN, FULLTEXT, PAIR_COVERAGE, WAVE3, WAVE4, WAVE5, WAVE6, WAVE7, WAVE8, WAVE9, WAVE10, WAVE11, WAVE12, WAVE13, WAVE14, WAVE15, WAVE16, WAVE17, WAVE18, MILKWEED_CHECK,
        BRASSICA_CONTRACT, BRASSICA_MANIFEST, BRASSICA_SCHEMA, BRASSICA_GATE, BDFFP_SCHEMA, BDFFP_STATUS, HASS_CONTRACT, HASS_SCHEMA, HASS_STATUS, THAI_ORCHARD_CONTRACT, THAI_ORCHARD_ACCESS, THAI_ORCHARD_STATUS, PLECTRITIS_CONTRACT, CABRALEA_CONTRACT, PLECTRITIS_ACCESS, CABRALEA_ACCESS, COMARUM_CONTRACT, COMARUM_ACCESS, AEXTOXICON_ANCHOR, SCHUEPP_CONTRACT, SCHUEPP_ACCESS, ANAXAGOREA_CONTRACT, ANAXAGOREA_ACCESS, CELTIS_GATE, ATTALEA_GATE, CARDIOPETALUM_RULE, CARDIOPETALUM_RESULT,
    ):
        assert p.is_file(), p

    queue = rows(QUEUE)
    assert len(queue) == 360
    assert [r["queue_id"] for r in queue[:180]] == [f"CFTQ{i:04d}" for i in range(1, 181)]
    assert all(r["outcome_opened"] == "no" for r in queue)

    screen = rows(SCREEN)
    assert len(screen) == 180
    assert [r["queue_id"] for r in screen] == [f"CFTQ{i:04d}" for i in range(1, 181)]
    assert {r["screen_wave"] for r in screen} == {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"}
    assert all(sum(r["screen_wave"] == str(w) for r in screen) == 10 for w in range(1, 19))
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
        "primary direct I-F coverage remains **1/5",
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
        "primary direct I-F coverage remains **1/5",
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
        "primary direct I-F coverage remains **1/5",
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
        "primary direct I-F coverage remains **1/5",
        "primary direct C-F coverage remains **2/5**",
    ):
        assert token in w10, token

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
        assert token in w11, token

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
        assert token in w12, token

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
        assert token in w13, token

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
        assert token in w14, token

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
        assert token in w15, token

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
        assert token in w16, token

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
        assert token in w17, token

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
        assert token in w18, token

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
        assert token in attalea["fragmentation_exposure"]
    assert int(attalea["pair_programme_increment"]) == 0
    assert attalea["effect_calculation_opened"] == "no"

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
        assert token in hass_status, token

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
        assert token in thai_contract, token

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
        assert token in thai_status, token

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
        assert token in plectritis_contract, token

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
        assert token in cabralea_contract, token

    plectritis_access = PLECTRITIS_ACCESS.read_text(encoding="utf-8")
    for token in (
        "design-valid, quantitatively blocked by site-denominator reconciliation and site-level effect-unit recoverability",
        "12 named localities",
        "N = 13 sites",
        "not an ecological null",
        "choose 12 or 13 sites",
        "digitize figures",
    ):
        assert token in plectritis_access, token

    cabralea_access = CABRALEA_ACCESS.read_text(encoding="utf-8")
    for token in (
        "design-valid, quantitatively blocked by four-site effect-unit recoverability",
        "F1, F2",
        "C1, C2",
        "not a null I-F result",
        "group-level SD",
    ):
        assert token in cabralea_access, token

    comarum_contract = COMARUM_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "14 Belgian populations of Comarum palustre",
        "Independent fragmentation unit = **population/site**",
        "population isolation / landscape woody-area cover within",
        "Primary I = **total direct pollinator visitation rate to C. palustre**",
        "Primary F = **open-pollinated viable seed set**",
        "population-year rows as independent fragmentation units",
    ):
        assert token in comarum_contract, token

    comarum_access = COMARUM_ACCESS.read_text(encoding="utf-8")
    for token in (
        "design-valid, quantitatively blocked by population-level F recoverability",
        "Table 1 publishes",
        "Figure 3",
        "No EGWEE Fisher-z effect was calculated",
        "digitize Figure 3",
    ):
        assert token in comarum_access, token

    aextoxicon_anchor = AEXTOXICON_ANCHOR.read_text(encoding="utf-8")
    for token in (
        "close_no_common_patch_level_C_effect_unit",
        "movement-compensation / source-limitation anchor",
        "pooled small-patch immigrant-seed proportion is reported as 40%",
        "Direct C-F programme increment: **0**",
    ):
        assert token in aextoxicon_anchor, token

    schuepp_contract = SCHUEPP_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "30 spatially separated landscape sectors",
        "Independent unit = **landscape sector / experimental site**",
        "Primary exposure = **distance to the nearest woody habitat**",
        "Primary I = **site-level pollinator visitation rate to cherry flowers**",
        "Primary F = **site-level open/control fruit set**",
        "retrospective external recovery",
    ):
        assert token in schuepp_contract, token

    schuepp_access = SCHUEPP_ACCESS.read_text(encoding="utf-8")
    for token in (
        "design-valid, quantitatively blocked by common-site I/F vector recoverability",
        "30 spatially separated landscape sectors",
        "does **not** expose one authoritative table",
        "No EGWEE Fisher-z effect was calculated",
        "Gradient programme increment: **0**",
        "digitize response figures",
    ):
        assert token in schuepp_access, token

    celtis_gate = CELTIS_GATE.read_text(encoding="utf-8")
    for token in (
        "close_no_single_response_free_fragmentation_estimand",
        "36 study sites",
        "forest-modification factor",
        "assign equally spaced severity scores 1–6",
        "process-decoupling / service-persistence anchor",
        "Quantitative I-F programme increment: **0**",
    ):
        assert token in celtis_gate, token

    anaxagorea_contract = ANAXAGOREA_CONTRACT.read_text(encoding="utf-8")
    for token in (
        "three large Atlantic-rainforest fragments",
        "fragments (6–14 ha)",
        "Independent unit = **forest fragment**",
        "Primary I = **pollinator abundance per flower**",
        "Primary F = **fruit set = fruits per flower**",
        "retrospective external recovery",
    ):
        assert token in anaxagorea_contract, token

    anaxagorea_access = ANAXAGOREA_ACCESS.read_text(encoding="utf-8")
    for token in (
        "design-valid, quantitatively blocked by common six-fragment F effect-unit recovery",
        "only fragments **A, B and D**",
        "Direct I-F programme increment: **0**",
        "mature fruits per tree",
        "use 186 or 209 flowers as fragmentation n",
    ):
        assert token in anaxagorea_access, token

    attalea_gate = ATTALEA_GATE.read_text(encoding="utf-8")
    for token in (
        "one ecological programme",
        "AJ-19 + SH-57",
        "UN-2400 + PA-3500",
        "blocked_linked_four_fragment_CF_values_not_recoverable",
        "Direct C-F programme increment: **0**",
        "reproduction–movement trade-off / compensation anchor",
    ):
        assert token in attalea_gate, token

    cardiopetalum_rule = CARDIOPETALUM_RULE.read_text(encoding="utf-8")
    for token in (
        "10 independent cerrado forest fragments",
        "fragmentation_severity = -log(fragment_area_ha)",
        "Primary I = **pollinator abundance per flower (ABP)**",
        "Primary F = **fruit set per flower (F)**",
        "retrospective external recovery",
        "contributes **zero** primary direct Hedges-g I-F programmes",
    ):
        assert token in cardiopetalum_rule, token

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
        assert token in cardiopetalum_result, token

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
        "queue=360 screened=180 pending=180 wave3_advance=1 wave4_advance=0 wave5_advance=1 wave6_advance=2 wave7_advance=3 wave8_advance=1 wave9_advance=2 wave10_advance=0 wave11_advance=1 wave12_advance=1 wave12_link_existing=1 wave13_advance=2 wave14_advance=1 wave15_advance=1 wave16_advance=2 wave17_advance=3 wave18_advance=1 "
        "brassica_increment=0 milkweed_gradient_increment=1 phacelia_increment=0 hedysarum_increment=0 "
        "bdffp_access_stop=1 hass_access_stop=1 aloe_pending=1 thai_orchard_access_stop=1 brudvig_link_noK=1 acer_CF_increment=0 plectritis_access_stop=1 cabralea_access_stop=1 comarum_access_stop=1 acer_miyabei_gradient_admitted=1 aextoxicon_anchor_noK=1 schuepp_access_stop=1 celtis_estimand_stop=1 anaxagorea_access_stop=1 cardiopetalum_gradient_admitted=1 attalea_linked_stop=1 bdffp_increment=0 ophrys_increment=0 brazil_nut_CF_increment=0 primary_IF_increment=0 direct_IF=1/5 direct_CF=2/5"
    )


if __name__ == "__main__":
    main()
