from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "evidence/meta_extraction/PS021_swietenia_macrophylla_summary_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
SEED = ROOT / "manuscript/meta_analysis_primary_study_seed_v1.csv"
RESULT = ROOT / "manuscript/SWIETENIA_MACROPHYLLA_2012_ML016_RECOVERY_RESULT.md"
STATUS = ROOT / "manuscript/META_ANALYSIS_CLUSTER_STATUS_2026-09-12.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (SUMMARY, REGISTRY, SEED, RESULT, STATUS):
        assert path.is_file(), path

    summary = rows(SUMMARY)
    assert len(summary) == 12
    assert {r["study_id"] for r in summary} == {"PS021"}
    assert {r["layer"] for r in summary} == {"G_mating", "F"}
    assert all(r["effect_unit_status"] == "descriptive_only" for r in summary)
    assert not any("g_admissible" == r["effect_unit_status"] for r in summary)

    overall = [r for r in summary if r["provenance"] == "all"]
    assert len(overall) == 4
    by = {(r["layer"], r["context"]): r for r in overall}
    assert abs(float(by[("G_mating", "forest")]["mean"]) - 0.163) < 1e-12
    assert abs(float(by[("G_mating", "isolated")]["mean"]) - 0.341) < 1e-12
    assert abs(float(by[("F", "forest")]["mean"]) - 0.060) < 1e-12
    assert abs(float(by[("F", "isolated")]["mean"]) - 0.048) < 1e-12
    assert by[("G_mating", "forest")]["sd_representation"] == "group_MLTR_parameter_family_bootstrap_uncertainty"
    assert by[("G_mating", "isolated")]["sd_representation"] == "group_MLTR_parameter_family_bootstrap_uncertainty"
    assert int(by[("G_mating", "forest")]["n_family"]) == 47
    assert int(by[("G_mating", "isolated")]["n_family"]) == 24

    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    ml016 = registry["ML016"]
    assert ml016["study_ids"] == "PS021"
    assert ml016["admissible_primary_layers"] == ""
    assert int(ml016["n_admissible_primary_effects"]) == 0
    assert ml016["covariance_status"] == "not_reconstructable_from_public_family_representation"
    assert ml016["cluster_status"] == "family_level_mating_effect_and_dependence_not_reconstructable"
    assert "group-bootstrap" in ml016["independence_note"]
    assert "Do not combine n_family" in ml016["independence_note"]

    primary = [r for r in registry.values() if r["cluster_status"] == "admissible_multilayer_cluster"]
    assert {r["cluster_id"] for r in primary} == {"ML001", "ML002", "ML003", "ML014"}
    assert sum(int(r["n_admissible_primary_effects"]) for r in primary) == 11

    seed = {r["study_id"]: r for r in rows(SEED)}
    ps021 = seed["PS021"]
    assert ps021["doi"] == "10.1111/j.1461-0248.2012.01752.x"
    assert ps021["source_status"] == "source_verified"
    assert {"G_mating", "F"} <= set(ps021["verified_layers"].split(";"))

    result = RESULT.read_text(encoding="utf-8")
    for token in (
        "family_level_mating_effect_and_dependence_not_reconstructable",
        "zero primary effects",
        "4 independent clusters / 11 primary effects",
        "not a between-family sample SD",
        "representation boundary, not a biological negative result",
        "Do not redesign the estimand after opening it",
    ):
        assert token in result, token

    status = STATUS.read_text(encoding="utf-8")
    for token in (
        "source-verified primary-study seeds: **19**",
        "ML016 / PS021",
        "contributes **zero primary effects**",
        "primary multilayer denominator remains **4 independent clusters / 11 effects**",
        "ML001 remains influential",
    ):
        assert token in status, token

    print(
        "ML016 Swietenia macrophylla closure: PASS; source direction retained "
        "(rp 0.163->0.341, growth 0.060->0.048), but group-bootstrap mating uncertainty "
        "and missing paired family rows block standardized G/F effects and covariance; primary denominator=4/11"
    )


if __name__ == "__main__":
    main()
