from __future__ import annotations

import csv
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POP = ROOT / "evidence/meta_extraction/PS017_dieffenbachia_population_recovery_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/PS017_dieffenbachia_effects_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
CONTRACT = ROOT / "manuscript/DIEFFENBACHIA_2010_CLUSTER_RECOVERY_CONTRACT.md"
RESULT = ROOT / "manuscript/DIEFFENBACHIA_2010_CLUSTER_RECOVERY_RESULT.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def hedges_g_ls(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    m1, m2 = stats.mean(fragmented), stats.mean(reference)
    s1, s2 = stats.stdev(fragmented), stats.stdev(reference)
    df = n1 + n2 - 2
    pooled = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / df)
    d = (m1 - m2) / pooled
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    return g, 1 / n1 + 1 / n2 + g * g / (2 * (n1 + n2))


def main() -> None:
    for path in (POP, EFFECTS, REGISTRY, CONTRACT, RESULT):
        assert path.is_file(), path

    pop = rows(POP)
    assert [r["population"] for r in pop] == ["F1", "F2", "C1", "C2"]
    expected_local = {"F1": 0.667, "F2": 0.712, "C1": 0.813, "C2": 0.661}
    expected_phi = {"F1": 0.377, "F2": 0.372, "C1": 0.340, "C2": 0.425}
    expected_old_nep = {"F1": 1.326, "F2": 1.344, "C1": 1.470, "C2": 1.176}
    by_pop = {r["population"]: r for r in pop}
    for name in expected_local:
        r = by_pop[name]
        local = float(r["local_male_gamete_assignment"])
        assert math.isclose(local, expected_local[name], abs_tol=1e-12)
        assert math.isclose(float(r["immigration_fraction"]), 1 - local, abs_tol=1e-12)
        assert math.isclose(float(r["phi_ft"]), expected_phi[name], abs_tol=1e-12)
        assert math.isclose(float(r["thesis_unadjusted_nep"]), expected_old_nep[name], abs_tol=1e-12)
        assert r["published_adjusted_nep"] == ""
        assert r["primary_status"] == "C_exact_G_missing"

    fragmented = [float(by_pop[p]["immigration_fraction"]) for p in ("F1", "F2")]
    reference = [float(by_pop[p]["immigration_fraction"]) for p in ("C1", "C2")]
    g, v = hedges_g_ls(fragmented, reference)
    assert math.isclose(stats.mean(fragmented), 0.3105, abs_tol=1e-12)
    assert math.isclose(stats.mean(reference), 0.263, abs_tol=1e-12)

    effects = {r["endpoint_id"]: r for r in rows(EFFECTS)}
    assert set(effects) == {"C_pollen_immigration", "G_mating_adjusted_Nep"}
    c = effects["C_pollen_immigration"]
    assert c["effect_unit_status"] == "descriptive_only_due_missing_companion_layer"
    assert int(c["n_independent_fragmented"]) == 2 and int(c["n_independent_reference"]) == 2
    assert math.isclose(float(c["oriented_effect"]), g, abs_tol=1e-12)
    assert math.isclose(float(c["oriented_variance"]), v, abs_tol=1e-12)
    gm = effects["G_mating_adjusted_Nep"]
    assert gm["effect_unit_status"] == "population_specific_Nep_not_reconstructable"
    assert gm["oriented_effect"] == "" and gm["oriented_variance"] == ""
    assert "adjusted N_ep" in gm["extraction_notes"]
    assert "1/(2 PhiFT)" in gm["extraction_notes"] and "1/r_p" in gm["extraction_notes"]

    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    ml012 = registry["ML012"]
    assert ml012["study_ids"] == "PS017"
    assert ml012["admissible_primary_layers"] == ""
    assert int(ml012["n_admissible_primary_effects"]) == 0
    assert ml012["cluster_status"] == "population_specific_Nep_not_reconstructable"

    admissible = [r for r in registry.values() if r["cluster_status"] == "admissible_multilayer_cluster"]
    assert {r["cluster_id"] for r in admissible} == {"ML001", "ML002", "ML003", "ML014"}
    assert sum(int(r["n_admissible_primary_effects"]) for r in admissible) == 11

    contract = CONTRACT.read_text(encoding="utf-8")
    result = RESULT.read_text(encoding="utf-8")
    assert "source `N_ep`" in contract and "Do not replace C" in contract
    assert "population_specific_Nep_not_reconstructable" in result
    assert "No Table 2 cell was inferred" in result
    assert "no C/G covariance is calculated or set to zero" in result

    print(
        "Dieffenbachia ML012 closure: PASS; exact C vector recovered "
        f"(g={g:.12f}, var={v:.12f}) but adjusted population-specific N_ep unavailable; "
        "ML012 adds 0 effects; current primary denominator=4/11"
    )


if __name__ == "__main__":
    main()
