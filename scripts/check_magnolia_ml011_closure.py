from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
RESULT = ROOT / "manuscript/MAGNOLIA_ML011_CLUSTER_RECOVERY_RESULT.md"
CONTRACT = ROOT / "manuscript/MAGNOLIA_ML011_CLUSTER_RECOVERY_CONTRACT.md"
LOCK = ROOT / "manuscript/MAGNOLIA_ML011_CALCULATION_LOCK.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (REGISTRY, RESULT, CONTRACT, LOCK):
        assert path.is_file(), path

    clusters = rows(REGISTRY)
    by_id = {r["cluster_id"]: r for r in clusters}
    assert "ML011" in by_id
    ml011 = by_id["ML011"]
    assert ml011["study_ids"] == "PS002"
    assert ml011["species"] == "Magnolia stellata"
    assert ml011["fragmentation_contrast"] == "source_defined_summed_adult_genet_basal_area"
    assert ml011["layers_targeted"] == "C;F"
    assert ml011["admissible_primary_layers"] == ""
    assert int(ml011["n_admissible_primary_effects"]) == 0
    assert ml011["covariance_status"] == "blocked_before_effect_calculation"
    assert ml011["cluster_status"] == "source_population_size_values_not_recoverable"

    admissible = [r for r in clusters if r["cluster_status"] == "admissible_multilayer_cluster"]
    assert {r["cluster_id"] for r in admissible} == {"ML001", "ML002", "ML003"}
    assert sum(int(r["n_admissible_primary_effects"]) for r in admissible) == 9

    contract = CONTRACT.read_text(encoding="utf-8")
    lock = LOCK.read_text(encoding="utf-8")
    result = RESULT.read_text(encoding="utf-8")

    assert "summed basal area" in contract
    assert "Adult-genet count must not be substituted" in contract
    assert "ML011_admitted_C_F_covariance_aware" in contract
    assert "A_ij = N_i * P_ij / 100" in lock
    assert "RNG seed `20260913`" in lock
    assert "No C/F effect or covariance was calculated" in result
    assert "Y = 85" in result and "F = 4" in result
    assert "integer genet-count-scale values" in result
    assert "donor-by-sink pollen table" in result

    print(
        "Magnolia ML011 closure: PASS; donor-by-sink C is structurally recoverable but the locked "
        "summed-basal-area exposure is absent; 0 effects admitted; denominator remains 3 clusters / 9 effects"
    )


if __name__ == "__main__":
    main()
