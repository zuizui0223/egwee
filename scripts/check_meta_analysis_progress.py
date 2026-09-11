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
CONOSPERMUM_2020 = ROOT / "evidence/meta_extraction/PS015_conospermum_2020_extraction_v1.csv"
TILLANDSIA = ROOT / "evidence/meta_extraction/PS012_tillandsia_extraction_v1.csv"
MAGNOLIA = ROOT / "evidence/meta_extraction/PS002_magnolia_extraction_v1.csv"
PRIMULA = ROOT / "evidence/meta_extraction/PS016_primula_2025_extraction_v1.csv"
SERAPIAS = ROOT / "evidence/meta_extraction/PS003_serapias_gradient_effects_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    files = (
        PRIMARY, CANDIDATES, QUEUE, STATUS, SPONDIAS, BROSIMUM, HULTING,
        CONOSPERMUM_2026, CONOSPERMUM_2020, TILLANDSIA, MAGNOLIA, PRIMULA, SERAPIAS,
    )
    for path in files:
        assert path.is_file(), path

    primary = rows(PRIMARY)
    candidates = rows(CANDIDATES)
    queue = rows(QUEUE)

    assert len(primary) >= 16, len(primary)
    assert len(candidates) >= 19, len(candidates)
    assert len(queue) >= 9, len(queue)

    primary_ids = {r["study_id"] for r in primary}
    queue_ids = [r["study_id"] for r in queue]
    assert len(primary_ids) == len(primary), "duplicate study_id in primary seed corpus"
    assert set(queue_ids) <= primary_ids, f"queue references unknown IDs: {set(queue_ids) - primary_ids}"
    assert any(r["study_id"] == "PS012" and "Tillandsia" in r["species"] for r in primary)
    assert any(r["study_id"] == "PS016" and r["species"] == "Primula elatior" for r in primary)
    assert any(r["study_id"] == "PS012" and "Tillandsia" in r["species"] for r in queue)
    assert any(r["study_id"] == "PS016" and r["species"] == "Primula elatior" for r in queue)
    assert any(r["study_id"] == "PS015" and int(r["priority"]) == 5 for r in queue)
    assert any(r["study_id"] == "PS011" and r["design_stream"] == "fisher_z_gradient" for r in queue)

    ps015 = next(r for r in primary if r["study_id"] == "PS015")
    assert ps015["doi"] == "10.1016/j.biocon.2020.108824"
    assert ps015["fragmentation_design"] == "11_population_fragmentation_gradient"
    assert {"D", "I", "T", "F"} <= set(ps015["verified_layers"].split(";"))

    ps016 = next(r for r in primary if r["study_id"] == "PS016")
    assert ps016["doi"] == "10.1016/j.biocon.2025.111044"
    assert ps016["fragmentation_design"] == "33_population_landscape_gradient"
    assert {"D", "I", "T", "F", "G_adult"} <= set(ps016["verified_layers"].split(";"))

    c08 = next(r for r in candidates if r["candidate_id"] == "C08")
    assert c08["system"] == "Primula elatior"
    assert "source_verified" in c08["current_status"]

    c19 = next(r for r in candidates if r["candidate_id"] == "C19")
    assert "Conospermum" in c19["system"]
    assert c19["direct_fragmentation_contrast"] == "gradient"
    assert "source_verified" in c19["current_status"]

    spondias = rows(SPONDIAS)
    brosimum = rows(BROSIMUM)
    hulting = rows(HULTING)
    cono26 = rows(CONOSPERMUM_2026)
    cono20 = rows(CONOSPERMUM_2020)
    till = rows(TILLANDSIA)
    mag = rows(MAGNOLIA)
    prim = rows(PRIMULA)
    ser = rows(SERAPIAS)
    assert len(spondias) >= 10
    assert len(brosimum) >= 8
    assert len(hulting) >= 4
    assert len(cono26) >= 5
    assert len(cono20) >= 4
    assert len(till) >= 8
    assert len(mag) == 6
    assert len(prim) == 6
    assert len(ser) == 2

    assert not any(r["effect_unit_status"] == "g_admissible" for r in spondias)

    b_g = [r for r in brosimum if r["effect_unit_status"] == "g_admissible"]
    assert len(b_g) == 1
    assert b_g[0]["endpoint_id"] == "C_paternity_rp"
    assert abs(float(b_g[0]["oriented_effect"]) - (-2.3215376099)) < 1e-9

    assert {r["layer"] for r in ser} == {"C", "F"}
    assert all(r["effect_unit_status"] == "fisher_z_admissible" for r in ser)
    assert all(int(r["n_independent"]) == 9 for r in ser)

    assert not any(r["effect_unit_status"] in {"g_admissible", "fisher_z_admissible"} for r in mag)
    assert next(r for r in mag if r["endpoint_id"] == "F_population_size")["raw_effect"] == "0.00055"
    assert next(r for r in mag if r["endpoint_id"] == "C_population_separation_male_success")["raw_effect"] == "-0.575"

    # Primula is deliberately model-pending: source-reported cross-layer
    # separation is retained, but narrative nulls/directions are not converted to zero/r.
    assert not any(r["effect_unit_status"] in {"g_admissible", "fisher_z_admissible"} for r in prim)
    assert any(r["endpoint_id"] == "Gadult_population_size" for r in prim)
    assert any(r["endpoint_id"] == "F_seed_pollinator_abundance" for r in prim)
    prim_null = next(r for r in prim if r["endpoint_id"] == "F_seed_genetic_diversity")
    assert prim_null["effect_unit_status"] == "descriptive_only"
    assert prim_null["raw_effect"] in {"", "NA"}

    h_i = next(r for r in hulting if r["endpoint_id"] == "I_pollination_rate")
    assert h_i["effect_unit_status"] == "model_contrast_pending_standardisation"
    assert h_i["raw_effect"] in {"", "NA"}

    adult = next(r for r in cono26 if r["endpoint_id"] == "Gadult_context")
    assert adult["effect_unit_status"] == "descriptive_only"
    assert adult["source_observation_id"] == "Conospermum_adult_genotypes_2021_shared"
    assert any(r["endpoint_id"] == "C_pollen_immigration" for r in cono26)
    assert any(r["endpoint_id"] == "Goffspring_presence" for r in cono26)

    assert not any(r["effect_unit_status"] in {"g_admissible", "fisher_z_admissible"} for r in cono20)

    assert not any(r["effect_unit_status"] == "g_admissible" for r in till)
    assert all(r["n_independent_continuous"] in {"", "3"} for r in till)
    assert all(r["n_independent_fragmented"] in {"", "3"} for r in till)
    mak_seed = next(r for r in till if r["species"] == "Tillandsia makoyana" and r["endpoint"] == "seed_set_2011")
    assert mak_seed["effect_unit_status"] == "raw_reanalysis_required"

    status = STATUS.read_text(encoding="utf-8")
    for token in (
        "source-verified primary-study seeds: **16**",
        "candidate systems/programmes: **19**",
        "priority extraction queue: **9 studies**",
        "studies with first-pass endpoint extraction materialized: **9**",
        "currently admissible quantitative effects: **3**",
        "PS016",
        "PS015",
        "PS012",
        "PS002",
        "PS003",
        "oriented `g=-2.32154`",
        "Fisher `z=-1.5412215`",
        "Fisher `z=-2.3040450`",
    ):
        assert token in status, token

    print(
        "EGWEE extraction progress: PASS; "
        f"{len(primary)} verified studies, {len(candidates)} candidates, {len(queue)} queued, "
        "9 materialized extractions, 3 admissible effects (1 g + 2 Fisher-z)"
    )


if __name__ == "__main__":
    main()
