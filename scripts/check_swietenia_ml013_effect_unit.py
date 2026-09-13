from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
AUDIT = ROOT / "manuscript/SWIETENIA_2011_EFFECT_UNIT_AUDIT.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    assert REGISTRY.is_file() and AUDIT.is_file()
    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    assert "ML013" in registry
    r = registry["ML013"]
    assert r["study_ids"] == "PS018"
    assert r["species"] == "Swietenia humilis"
    assert r["fragmentation_contrast"] == "isolated_remnant_vs_continuous_forest"
    assert r["admissible_primary_layers"] == ""
    assert int(r["n_admissible_primary_effects"]) == 0
    assert r["covariance_status"] == "not_identifiable_with_single_reference_population"
    assert r["cluster_status"] == "single_continuous_reference_population_no_replication"
    assert "only one continuous-forest reference population" in r["independent_unit_frame"]
    assert "Maternal trees, progeny and loci are not fragmentation replicates" in r["independence_note"]

    text = AUDIT.read_text(encoding="utf-8")
    for token in (
        "6.1",
        "8.3",
        "N_ep = 1.9",
        "3.6",
        "single forest population (`S`)",
        "not converted into primary Hedges-g effects",
    ):
        assert token in text

    admissible = [x for x in registry.values() if x["cluster_status"] == "admissible_multilayer_cluster"]
    assert {x["cluster_id"] for x in admissible} == {"ML001", "ML002", "ML003"}
    assert sum(int(x["n_admissible_primary_effects"]) for x in admissible) == 9

    print("Swietenia ML013 effect-unit audit: PASS; strong multilayer programme evidence retained, single continuous reference prevents replicated cluster admission; denominator remains 3 clusters / 9 effects")


if __name__ == "__main__":
    main()
