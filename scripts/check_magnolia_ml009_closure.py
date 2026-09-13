from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
RESULT = ROOT / "manuscript/MAGNOLIA_ML009_CLUSTER_RECOVERY_RESULT.md"
CONTRACT = ROOT / "manuscript/MAGNOLIA_ML009_CLUSTER_RECOVERY_CONTRACT.md"
LOCK = ROOT / "manuscript/MAGNOLIA_ML009_CALCULATION_LOCK.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (REGISTRY, RESULT, CONTRACT, LOCK):
        assert path.is_file(), path
    clusters = rows(REGISTRY)
    by_id = {r["cluster_id"]: r for r in clusters}
    assert "ML009" in by_id
    ml009 = by_id["ML009"]
    assert ml009["study_ids"] == "PS002"
    assert ml009["species"] == "Magnolia stellata"
    assert ml009["fragmentation_contrast"] == "source_defined_summed_adult_genet_basal_area"
    assert ml009["layers_targeted"] == "C;F"
    assert ml009["admissible_primary_layers"] == ""
    assert int(ml009["n_admissible_primary_effects"]) == 0
    assert ml009["covariance_status"] == "blocked_before_effect_calculation"
    assert ml009["cluster_status"] == "source_population_size_values_not_recoverable"

    admissible = [r for r in clusters if r["cluster_status"] == "admissible_multilayer_cluster"]
    assert {r["cluster_id"] for r in admissible} == {"ML001", "ML002", "ML003"}
    assert sum(int(r["n_admissible_primary_effects"]) for r in admissible) == 9

    result = RESULT.read_text(encoding="utf-8")
    assert "No C/F effect or covariance was calculated" in result
    assert "summed basal area" in result
    assert "Y = 85" in result and "F = 4" in result
    print("Magnolia ML009 closure: PASS; source supplement exposes pollen matrix but not the locked summed-basal-area exposure; 3 admissible clusters / 9 effects unchanged")


if __name__ == "__main__":
    main()
