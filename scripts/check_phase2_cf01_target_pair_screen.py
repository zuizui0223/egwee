from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "evidence/meta_extraction/phase2_cf01_target_pair_queue_v1.csv"
SCREEN = ROOT / "evidence/meta_extraction/phase2_cf01_target_pair_design_screen_v1.csv"
FULLTEXT = ROOT / "evidence/meta_extraction/phase2_cf01_target_pair_fulltext_gate_v1.csv"
PAIR_COVERAGE = ROOT / "evidence/meta_extraction/coverage_expansion_pair_coverage_v1.csv"

WAVE3 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE3_2026-09-24.md"
WAVE4 = ROOT / "manuscript/PHASE2_CF01_TARGET_PAIR_SCREEN_WAVE4_2026-09-24.md"

BRASSICA_CONTRACT = ROOT / "manuscript/CF01_BRASSICA_GUATEMALA_2024_RECOVERY_CONTRACT.md"
BRASSICA_MANIFEST = ROOT / "evidence/meta_extraction/phase2_cf01_brassica_mendeley_manifest_v1.json"
BRASSICA_SCHEMA = ROOT / "manuscript/PHASE2_CF01_BRASSICA_MENDELEY_SCHEMA_2026-09-24.md"
BRASSICA_GATE = ROOT / "manuscript/PHASE2_CF01_BRASSICA_QUANTITATIVE_GATE_2026-09-24.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for p in (
        QUEUE, SCREEN, FULLTEXT, PAIR_COVERAGE, WAVE3, WAVE4,
        BRASSICA_CONTRACT, BRASSICA_MANIFEST, BRASSICA_SCHEMA, BRASSICA_GATE,
    ):
        assert p.is_file(), p

    queue = rows(QUEUE)
    assert len(queue) == 360
    assert [r["queue_id"] for r in queue[:40]] == [f"CFTQ{i:04d}" for i in range(1, 41)]
    assert all(r["outcome_opened"] == "no" for r in queue)

    screen = rows(SCREEN)
    assert len(screen) == 40
    assert [r["queue_id"] for r in screen] == [f"CFTQ{i:04d}" for i in range(1, 41)]
    assert {r["screen_wave"] for r in screen} == {"1", "2", "3", "4"}
    assert all(sum(r["screen_wave"] == str(w) for r in screen) == 10 for w in range(1, 5))
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

    fulltext = {r["queue_id"]: r for r in rows(FULLTEXT)}
    assert "CFTQ0030" in fulltext
    b = fulltext["CFTQ0030"]
    assert b["programme_identity"] == "P2_CF01_BRASSICA_GUATEMALA_2024"
    assert b["quantitative_gate_status"] == "blocked_primary_I_raw_not_publicly_recoverable_under_locked_contract"
    assert int(b["pair_programme_increment"]) == 0
    assert b["effect_calculation_opened"] == "no"

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
        "primary I = **total floral visitation rate to B. rapa experimental plots**",
        "Primary F = **natural/open fruit set of B. rapa**",
        "Primary fragmentation-level independent unit = **site**",
        "n_fragmented = 3",
        "n_reference = 3",
    ):
        assert token in contract, token

    print(
        "PHASE2_CF01_TARGET_PAIR_SCREEN_OK "
        "queue=360 screened=40 pending=320 wave3_advance=1 wave4_advance=0 "
        "brassica_increment=0 direct_IF=1/5"
    )


if __name__ == "__main__":
    main()
