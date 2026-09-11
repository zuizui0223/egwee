from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT / "manuscript/meta_analysis_primary_study_seed_v1.csv"
CANDIDATES = ROOT / "manuscript/meta_analysis_candidate_ledger.csv"
QUEUE = ROOT / "manuscript/meta_analysis_extraction_queue_v1.csv"
STATUS = ROOT / "manuscript/META_ANALYSIS_EXTRACTION_STATUS_2026-09-11.md"
SPONDIAS = ROOT / "evidence/meta_extraction/PS001_spondias_extraction_v1.csv"
BROSIMUM = ROOT / "evidence/meta_extraction/PS004_brosimum_extraction_v1.csv"
HULTING = ROOT / "evidence/meta_extraction/PS014_hulting_extraction_v1.csv"
CONOSPERMUM_2026 = ROOT / "evidence/meta_extraction/PS011_conospermum_2026_extraction_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (PRIMARY, CANDIDATES, QUEUE, STATUS, SPONDIAS, BROSIMUM, HULTING, CONOSPERMUM_2026):
        assert path.is_file(), path

    primary = rows(PRIMARY)
    candidates = rows(CANDIDATES)
    queue = rows(QUEUE)

    assert len(primary) >= 15, len(primary)
    assert len(candidates) >= 19, len(candidates)
    assert len(queue) >= 8, len(queue)

    primary_ids = {r["study_id"] for r in primary}
    queue_ids = [r["study_id"] for r in queue]
    assert len(primary_ids) == len(primary), "duplicate study_id in primary seed corpus"
    assert set(queue_ids) <= primary_ids, f"queue references unknown IDs: {set(queue_ids) - primary_ids}"
    assert "PS016" not in queue_ids, "stale Tillandsia ID survived queue repair"
    assert any(r["study_id"] == "PS012" and "Tillandsia" in r["species"] for r in queue)
    assert any(r["study_id"] == "PS015" and int(r["priority"]) == 5 for r in queue)
    assert any(r["study_id"] == "PS011" and r["design_stream"] == "fisher_z_gradient" for r in queue)

    ps015 = next(r for r in primary if r["study_id"] == "PS015")
    assert ps015["doi"] == "10.1016/j.biocon.2020.108824"
    assert ps015["fragmentation_design"] == "11_population_fragmentation_gradient"
    assert {"D", "I", "T", "F"} <= set(ps015["verified_layers"].split(";"))

    c19 = next(r for r in candidates if r["candidate_id"] == "C19")
    assert "Conospermum" in c19["system"]
    assert c19["direct_fragmentation_contrast"] == "gradient"
    assert "source_verified" in c19["current_status"]

    spondias = rows(SPONDIAS)
    brosimum = rows(BROSIMUM)
    hulting = rows(HULTING)
    cono26 = rows(CONOSPERMUM_2026)
    assert len(spondias) >= 10
    assert len(brosimum) >= 8
    assert len(hulting) >= 4
    assert len(cono26) >= 5

    # Spondias: no naive standardized effect admitted because published
    # denominators/dispersion units are incompatible with a simple group g.
    assert not any(r["effect_unit_status"] == "g_admissible" for r in spondias)

    # Brosimum: exactly one current g-admissible endpoint; reciprocal Nep is
    # descriptive only and shares the same source observation.
    b_g = [r for r in brosimum if r["effect_unit_status"] == "g_admissible"]
    assert len(b_g) == 1
    assert b_g[0]["endpoint_id"] == "C_paternity_rp"
    assert abs(float(b_g[0]["oriented_effect"]) - (-2.3215376099)) < 1e-9

    # Hulting: published pollination null is retained as a model contrast,
    # never synthesized as numerical zero.
    h_i = next(r for r in hulting if r["endpoint_id"] == "I_pollination_rate")
    assert h_i["effect_unit_status"] == "model_contrast_pending_standardisation"
    assert h_i["raw_effect"] in {"", "NA"}

    # Conospermum 2026: standing adult genetics overlaps PS010 and is not a new
    # independent adult-genetic effect; contemporary pollen/offspring rows remain.
    adult = next(r for r in cono26 if r["endpoint_id"] == "Gadult_context")
    assert adult["effect_unit_status"] == "descriptive_only"
    assert adult["source_observation_id"] == "Conospermum_adult_genotypes_2021_shared"
    assert any(r["endpoint_id"] == "C_pollen_immigration" for r in cono26)
    assert any(r["endpoint_id"] == "Goffspring_presence" for r in cono26)

    status = STATUS.read_text(encoding="utf-8")
    for token in (
        "source-verified primary-study seeds: **15**",
        "candidate systems/programmes: **19**",
        "studies with first-pass endpoint extraction materialized: **4**",
        "currently `g_admissible` effects: **1**",
        "PS015",
        "oriented `g=-2.32154`",
    ):
        assert token in status, token

    print(
        "EGWEE extraction progress: PASS; "
        f"{len(primary)} verified studies, {len(candidates)} candidates, {len(queue)} queued, "
        "4 materialized extractions, 1 current g-admissible effect"
    )


if __name__ == "__main__":
    main()
