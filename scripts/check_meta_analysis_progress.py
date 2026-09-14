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
WANDOO = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_population_table_v1.csv"
WANDOO_EFFECTS = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv"
WANDOO_COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_covariance_v1.csv"
SOCIALIS_EFFECTS = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_effects_v1.csv"
SOCIALIS_COV = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_primary_covariance_v1.csv"
MACROPHYLLA = ROOT / "evidence/meta_extraction/PS021_swietenia_macrophylla_summary_v1.csv"
CLUSTERS = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (
        PRIMARY, CANDIDATES, QUEUE, STATUS, SPONDIAS, SPONDIAS_SITE, BROSIMUM, HULTING,
        CONOSPERMUM_2026, CONOSPERMUM_2020, TILLANDSIA, MAGNOLIA, PRIMULA,
        SERAPIAS_GRADIENT, SERAPIAS_BINARY, WANDOO, WANDOO_EFFECTS, WANDOO_COV,
        SOCIALIS_EFFECTS, SOCIALIS_COV, MACROPHYLLA, CLUSTERS,
    ):
        assert path.is_file(), path

    primary = rows(PRIMARY)
    candidates = rows(CANDIDATES)
    queue = rows(QUEUE)
    assert len(primary) >= 19
    assert len(candidates) >= 19
    assert len(queue) >= 9
    assert len({r["study_id"] for r in primary}) == len(primary)
    assert {r["study_id"] for r in queue} <= {r["study_id"] for r in primary}
    assert any(r["study_id"] == "PS019" and r["doi"] == "10.3389/fevo.2018.00039" for r in primary)
    assert any(r["study_id"] == "PS020" and r["doi"] == "10.1111/mec.12056" for r in primary)
    assert any(r["study_id"] == "PS021" and r["doi"] == "10.1111/j.1461-0248.2012.01752.x" for r in primary)

    ps015 = next(r for r in primary if r["study_id"] == "PS015")
    assert ps015["doi"] == "10.1016/j.biocon.2020.108824"
    assert {"D", "I", "T", "F"} <= set(ps015["verified_layers"].split(";"))
    ps016 = next(r for r in primary if r["study_id"] == "PS016")
    assert {"D", "I", "T", "F", "G_adult"} <= set(ps016["verified_layers"].split(";"))
    ps020 = next(r for r in primary if r["study_id"] == "PS020")
    assert {"G_mating", "F"} <= set(ps020["verified_layers"].split(";"))
    ps021 = next(r for r in primary if r["study_id"] == "PS021")
    assert {"G_mating", "F"} <= set(ps021["verified_layers"].split(";"))

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
    wandoo = rows(WANDOO)
    wandoo_effects = rows(WANDOO_EFFECTS)
    wandoo_cov = rows(WANDOO_COV)
    socialis = rows(SOCIALIS_EFFECTS)
    socialis_cov = rows(SOCIALIS_COV)
    macrophylla = rows(MACROPHYLLA)
    clusters = rows(CLUSTERS)

    assert len(spondias) == 13 and len(spondias_site) == 8
    assert len(brosimum) >= 8 and len(hulting) >= 4
    assert len(cono26) >= 5 and len(cono20) >= 4
    assert len(till) >= 8 and len(mag) == 6 and len(prim) == 6
    assert len(ser_gradient) == 2 and len(ser_binary) == 4
    assert len(wandoo) == 19 and len(wandoo_effects) == 3 and len(wandoo_cov) == 9
    assert len(socialis) == 2 and len(socialis_cov) == 4
    assert len(macrophylla) == 12

    s_primary = [r for r in spondias_site if r["analysis_role"] == "primary"]
    assert {r["endpoint_id"] for r in s_primary} == {"C_paternity_correlation", "Gadult_Ho", "Gjuvenile_Ho", "Gseed_Ho"}
    assert all(r["effect_unit_status"] == "g_admissible" for r in s_primary)
    assert all(r["independent_unit"] == "site" for r in s_primary)
    assert abs(float(next(r for r in s_primary if r["endpoint_id"] == "C_paternity_correlation")["oriented_effect"]) + 0.254746780651) < 1e-9
    assert abs(float(next(r for r in s_primary if r["endpoint_id"] == "Gadult_Ho")["oriented_effect"]) + 0.940881526358) < 1e-9
    assert abs(float(next(r for r in s_primary if r["endpoint_id"] == "Gjuvenile_Ho")["oriented_effect"]) + 3.181330686725) < 1e-9
    assert abs(float(next(r for r in s_primary if r["endpoint_id"] == "Gseed_Ho")["oriented_effect"]) + 1.117905988897) < 1e-9

    by_spondias = {r["endpoint_id"]: r for r in spondias}
    assert {by_spondias[e]["effect_unit_status"] for e in ("I_visitation", "F_fruit_production", "F_fruit_set")} == {"model_contrast_pending_standardisation"}
    assert by_spondias["C_pollen_distance"]["effect_unit_status"] == "raw_reanalysis_required"

    b_g = [r for r in brosimum if r["effect_unit_status"] == "g_admissible"]
    assert {r["endpoint_id"] for r in b_g} == {"C_paternity_rp", "F_progeny_vigour"}
    assert abs(float(next(r for r in b_g if r["endpoint_id"] == "C_paternity_rp")["oriented_effect"]) + 2.3215376099) < 1e-9
    assert abs(float(next(r for r in b_g if r["endpoint_id"] == "F_progeny_vigour")["oriented_effect"]) + 1.286939644908) < 1e-9

    ser_primary = [r for r in ser_binary if r["primary_or_sensitivity"] == "primary"]
    assert len(ser_primary) == 3
    assert {r["layer"] for r in ser_primary} == {"C", "F", "G_adult"}
    assert all(r["effect_unit_status"] == "fisher_z_admissible" for r in ser_gradient)

    assert not any(r["effect_unit_status"] in {"g_admissible", "fisher_z_admissible"} for r in mag)
    assert not any(r["effect_unit_status"] in {"g_admissible", "fisher_z_admissible"} for r in prim)
    assert not any(r["effect_unit_status"] in {"g_admissible", "fisher_z_admissible"} for r in cono20)
    assert not any(r["effect_unit_status"] == "g_admissible" for r in till)
    assert next(r for r in hulting if r["endpoint_id"] == "I_pollination_rate")["effect_unit_status"] == "model_contrast_pending_standardisation"
    assert next(r for r in cono26 if r["endpoint_id"] == "Gadult_context")["effect_unit_status"] == "descriptive_only"

    assert {r["layer"] for r in wandoo_effects} == {"I", "F", "G_adult"}
    assert all(r["effect_stream"] == "fisher_z_gradient" for r in wandoo_effects)
    assert all(abs(float(r["raw_variance"]) - 0.125) < 1e-12 for r in wandoo_effects)

    by_socialis = {r["endpoint_id"]: r for r in socialis}
    assert set(by_socialis) == {"Gmating_correlated_paternity_rp", "F_family_growth"}
    assert by_socialis["Gmating_correlated_paternity_rp"]["layer"] == "G_mating"
    assert by_socialis["F_family_growth"]["layer"] == "F_reproductive_function"
    assert all(r["effect_unit_status"] == "g_admissible" for r in socialis)
    assert all(r["independent_unit"] == "maternal_family" for r in socialis)
    assert all(int(r["n_independent_fragmented"]) == 13 for r in socialis)
    assert all(int(r["n_independent_reference"]) == 15 for r in socialis)
    assert abs(float(by_socialis["Gmating_correlated_paternity_rp"]["oriented_effect"]) + 1.023913881040) < 1e-9
    assert abs(float(by_socialis["F_family_growth"]["oriented_effect"]) + 0.271808874814) < 1e-9
    assert any(abs(float(r["sampling_covariance"]) - 0.050108426040) < 1e-9 for r in socialis_cov if r["endpoint_i"] != r["endpoint_j"])

    assert {r["layer"] for r in macrophylla} == {"G_mating", "F"}
    assert all(r["effect_unit_status"] == "descriptive_only" for r in macrophylla)
    assert not any(r["effect_unit_status"] == "g_admissible" for r in macrophylla)
    macro_overall = {(r["layer"], r["context"]): r for r in macrophylla if r["provenance"] == "all"}
    assert abs(float(macro_overall[("G_mating", "forest")]["mean"]) - 0.163) < 1e-12
    assert abs(float(macro_overall[("G_mating", "isolated")]["mean"]) - 0.341) < 1e-12
    assert macro_overall[("G_mating", "forest")]["sd_representation"] == "group_MLTR_parameter_family_bootstrap_uncertainty"

    by_cluster = {r["cluster_id"]: r for r in clusters}
    binary = [r for r in clusters if r["cluster_status"] == "admissible_multilayer_cluster"]
    gradient = [r for r in clusters if r["cluster_status"] == "gradient_generalisation_multilayer_cluster"]
    assert {r["cluster_id"] for r in binary} == {"ML001", "ML002", "ML003", "ML014"}
    assert {r["cluster_id"] for r in gradient} == {"ML015"}
    assert set(by_cluster["ML014"]["admissible_primary_layers"].split(";")) == {"G_mating", "F"}
    assert int(by_cluster["ML014"]["n_admissible_primary_effects"]) == 2
    assert by_cluster["ML014"]["covariance_status"] == "proxy_reconstructed_from_paired_families"
    assert by_cluster["ML015"]["admissible_primary_layers"] == ""
    assert int(by_cluster["ML015"]["n_admissible_primary_effects"]) == 0
    assert by_cluster["ML016"]["admissible_primary_layers"] == ""
    assert int(by_cluster["ML016"]["n_admissible_primary_effects"]) == 0
    assert by_cluster["ML016"]["cluster_status"] == "family_level_mating_effect_and_dependence_not_reconstructable"
    assert by_cluster["ML016"]["covariance_status"] == "not_reconstructable_from_public_family_representation"
    assert sum(int(r["n_admissible_primary_effects"]) for r in binary) == 11

    status = STATUS.read_text(encoding="utf-8")
    for token in (
        "source-verified primary-study seeds: **19**",
        "independent **primary** admissible multilayer clusters: **4**",
        "primary admissible effects inside those clusters: **11**",
        "separate admissible Fisher-z gradient effects: **5**",
        "ML014 / PS020",
        "ML016 / PS021",
        "representation boundary, not a biological negative result",
        "chi-square(8) = 22.6477",
        "p = 0.07777",
        "ML001 remains influential",
    ):
        assert token in status, token

    print(
        "EGWEE extraction progress: PASS; "
        f"{len(primary)} verified studies, {len(candidates)} candidates, {len(queue)} queued; "
        "primary family = 4 clusters / 11 effects; ML015 gradient-only; ML016 representation-blocked / 0 effects"
    )


if __name__ == "__main__":
    main()
