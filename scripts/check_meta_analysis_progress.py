from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT / "manuscript/meta_analysis_primary_study_seed_v1.csv"
CANDIDATES = ROOT / "manuscript/meta_analysis_candidate_ledger.csv"
QUEUE = ROOT / "manuscript/meta_analysis_extraction_queue_v1.csv"
STATUS = ROOT / "manuscript/META_ANALYSIS_CLUSTER_STATUS_2026-09-12.md"
SPONDIAS = ROOT / "evidence/meta_extraction/PS001_spondias_extraction_v1.csv"
SPONDIAS_SITE = ROOT / "evidence/meta_extraction/PS001_spondias_site_effects_v1.csv"
BROSIMUM = ROOT / "evidence/meta_extraction/PS004_brosimum_extraction_v1.csv"
HULTING = ROOT / "evidence/meta_extraction/PS014_hulting_extraction_v1.csv"
CONOSPERMUM_2026 = ROOT / "evidence/meta_extraction/PS011_conospermum_2026_extraction_v1.csv"
CONOSPERMUM_2020 = ROOT / "evidence/meta_extraction/PS015_conospermum_2020_extraction_v1.csv"
TILLANDSIA = ROOT / "evidence/meta_extraction/PS012_tillandsia_extraction_v1.csv"
MAGNOLIA = ROOT / "evidence/meta_extraction/PS002_magnolia_extraction_v1.csv"
PRIMULA = ROOT / "evidence/meta_extraction/PS016_primula_2025_extraction_v1.csv"
SERAPIAS_GRADIENT = ROOT / "evidence/meta_extraction/PS003_serapias_gradient_effects_v1.csv"
SERAPIAS_BINARY = ROOT / "evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv"
CLUSTERS = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (
        PRIMARY, CANDIDATES, QUEUE, STATUS, SPONDIAS, SPONDIAS_SITE, BROSIMUM, HULTING,
        CONOSPERMUM_2026, CONOSPERMUM_2020, TILLANDSIA, MAGNOLIA, PRIMULA,
        SERAPIAS_GRADIENT, SERAPIAS_BINARY, CLUSTERS,
    ):
        assert path.is_file(), path

    primary = rows(PRIMARY)
    candidates = rows(CANDIDATES)
    queue = rows(QUEUE)
    assert len(primary) >= 16
    assert len(candidates) >= 19
    assert len(queue) >= 9
    assert len({r["study_id"] for r in primary}) == len(primary)
    assert {r["study_id"] for r in queue} <= {r["study_id"] for r in primary}

    ps015 = next(r for r in primary if r["study_id"] == "PS015")
    assert ps015["doi"] == "10.1016/j.biocon.2020.108824"
    assert {"D", "I", "T", "F"} <= set(ps015["verified_layers"].split(";"))
    ps016 = next(r for r in primary if r["study_id"] == "PS016")
    assert ps016["doi"] == "10.1016/j.biocon.2025.111044"
    assert {"D", "I", "T", "F", "G_adult"} <= set(ps016["verified_layers"].split(";"))

    spondias = rows(SPONDIAS)
    spondias_site = rows(SPONDIAS_SITE)
    brosimum = rows(BROSIMUM)
    hulting = rows(HULTING)
    cono26 = rows(CONOSPERMUM_2026)
    cono20 = rows(CONOSPERMUM_2020)
    till = rows(TILLANDSIA)
    mag = rows(MAGNOLIA)
    prim = rows(PRIMULA)
    ser_gradient = rows(SERAPIAS_GRADIENT)
    ser_binary = rows(SERAPIAS_BINARY)
    clusters = rows(CLUSTERS)

    assert len(spondias) == 13
    assert len(spondias_site) == 8
    assert len(brosimum) >= 8
    assert len(hulting) >= 4
    assert len(cono26) >= 5
    assert len(cono20) >= 4
    assert len(till) >= 8
    assert len(mag) == 6
    assert len(prim) == 6
    assert len(ser_gradient) == 2
    assert len(ser_binary) == 4

    # ML003: four co-primary outcomes, all on the same five-site frame.
    s_primary = [r for r in spondias_site if r["analysis_role"] == "primary"]
    assert {r["endpoint_id"] for r in s_primary} == {
        "C_paternity_correlation", "Gadult_Ho", "Gjuvenile_Ho", "Gseed_Ho"
    }
    assert all(r["effect_unit_status"] == "g_admissible" for r in s_primary)
    assert all(r["independent_unit"] == "site" for r in s_primary)
    assert abs(float(next(r for r in s_primary if r["endpoint_id"] == "C_paternity_correlation")["oriented_effect"]) + 0.254746780651) < 1e-9
    assert abs(float(next(r for r in s_primary if r["endpoint_id"] == "Gadult_Ho")["oriented_effect"]) + 0.940881526358) < 1e-9
    assert abs(float(next(r for r in s_primary if r["endpoint_id"] == "Gjuvenile_Ho")["oriented_effect"]) + 3.181330686725) < 1e-9
    assert abs(float(next(r for r in s_primary if r["endpoint_id"] == "Gseed_Ho")["oriented_effect"]) + 1.117905988897) < 1e-9
    assert next(r for r in spondias_site if r["endpoint_id"] == "Gadult_Sp")["analysis_role"] == "sensitivity_structure"
    assert {r["endpoint_id"] for r in spondias_site if r["analysis_role"] == "sensitivity_metric"} == {
        "Gadult_Fis", "Gjuvenile_Fis", "Gseed_Fis"
    }

    # I/F remain blocked; supplementary genetics did not create site-level I/F data.
    by_spondias = {r["endpoint_id"]: r for r in spondias}
    assert {by_spondias[e]["effect_unit_status"] for e in ("I_visitation", "F_fruit_production", "F_fruit_set")} == {"model_contrast_pending_standardisation"}
    assert by_spondias["C_pollen_distance"]["effect_unit_status"] == "raw_reanalysis_required"
    assert by_spondias["C_effective_sires"]["effect_unit_status"] == "descriptive_only"

    # ML002 remains C/F only.
    b_g = [r for r in brosimum if r["effect_unit_status"] == "g_admissible"]
    assert {r["endpoint_id"] for r in b_g} == {"C_paternity_rp", "F_progeny_vigour"}
    assert abs(float(next(r for r in b_g if r["endpoint_id"] == "C_paternity_rp")["oriented_effect"]) + 2.3215376099) < 1e-9
    assert abs(float(next(r for r in b_g if r["endpoint_id"] == "F_progeny_vigour")["oriented_effect"]) + 1.286939644908) < 1e-9

    # ML001 remains C/F/G_adult with FIS sensitivity.
    ser_primary = [r for r in ser_binary if r["primary_or_sensitivity"] == "primary"]
    assert len(ser_primary) == 3
    assert {r["layer"] for r in ser_primary} == {"C", "F", "G_adult"}
    assert next(r for r in ser_binary if r["primary_or_sensitivity"] == "sensitivity")["endpoint"] == "fixation_index_FIS"
    assert all(r["effect_unit_status"] == "fisher_z_admissible" for r in ser_gradient)

    # Unreconstructed systems stay closed.
    assert not any(r["effect_unit_status"] in {"g_admissible", "fisher_z_admissible"} for r in mag)
    assert not any(r["effect_unit_status"] in {"g_admissible", "fisher_z_admissible"} for r in prim)
    assert not any(r["effect_unit_status"] in {"g_admissible", "fisher_z_admissible"} for r in cono20)
    assert not any(r["effect_unit_status"] == "g_admissible" for r in till)
    assert next(r for r in hulting if r["endpoint_id"] == "I_pollination_rate")["effect_unit_status"] == "model_contrast_pending_standardisation"
    assert next(r for r in cono26 if r["endpoint_id"] == "Gadult_context")["effect_unit_status"] == "descriptive_only"

    by_cluster = {r["cluster_id"]: r for r in clusters}
    admissible = [r for r in clusters if r["cluster_status"] == "admissible_multilayer_cluster"]
    assert {r["cluster_id"] for r in admissible} == {"ML001", "ML002", "ML003"}
    assert set(by_cluster["ML001"]["admissible_primary_layers"].split(";")) == {"C", "F", "G_adult"}
    assert set(by_cluster["ML002"]["admissible_primary_layers"].split(";")) == {"C", "F"}
    assert set(by_cluster["ML003"]["admissible_primary_layers"].split(";")) == {"C", "G_adult", "G_offspring"}
    assert int(by_cluster["ML003"]["n_admissible_primary_effects"]) == 4
    assert by_cluster["ML003"]["covariance_status"] == "proxy_pairwise_low_rank_from_five_sites"
    assert sum(int(r["n_admissible_primary_effects"]) for r in admissible) == 9

    status = STATUS.read_text(encoding="utf-8")
    for token in (
        "independent admissible multilayer clusters: **3**",
        "primary admissible effects inside those clusters: **9**",
        "adult `H_O`: `g = -0.94088153`",
        "juvenile `H_O`: `g = -3.18133069`",
        "seed `H_O`: `g = -1.11790599`",
        "cohort-lag candidate",
        "not site-level visitation or reproductive-function values",
        "ML004 Conospermum 2020",
    ):
        assert token in status, token

    print(
        "EGWEE extraction progress: PASS; "
        f"{len(primary)} verified studies, {len(candidates)} candidates, {len(queue)} queued; "
        "3 independent clusters, 9 primary effects; ML003 now carries dependent adult/juvenile/seed genetics without inflating the cluster count"
    )


if __name__ == "__main__":
    main()
