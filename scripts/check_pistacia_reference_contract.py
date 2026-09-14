from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "manuscript/PISTACIA_2012_REFERENCE_AUDIT.md"
EVIDENCE = ROOT / "evidence/meta_extraction/PS013_pistacia_reference_audit_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (AUDIT, EVIDENCE, REGISTRY):
        assert path.is_file(), path

    text = AUDIT.read_text(encoding="utf-8")
    assert "single_landscape_per_condition_no_fragmentation_replication" in text
    assert "October 2007" in text
    assert "2006 and 2007" in text
    assert "not simply calendar mismatch" in text
    assert "Mothers, seeds, males, loci and distance classes" in text
    assert "Do not manufacture a C-layer kernel contrast" in text
    assert "29 fragmented mothers and 30 continuous mothers are not fragmentation replicates" in text

    evidence = {r["comparison_id"]: r for r in rows(EVIDENCE)}
    assert set(evidence) == {"C_rp_2007", "C_rp_2006_sensitivity", "Gadult_Sp", "C_pollen_kernel"}
    rp07 = evidence["C_rp_2007"]
    assert rp07["layer"] == "G_mating"
    assert abs(float(rp07["fragmented_value"]) - 0.231) < 1e-12
    assert abs(float(rp07["continuous_reference_value"]) - 0.085) < 1e-12
    assert rp07["continuous_reference_season"] == "2007"
    assert rp07["fragmented_observation_season"] == "2007"
    assert rp07["fragmentation_unit_fragmented"] == "1"
    assert rp07["fragmentation_unit_reference"] == "1"
    assert rp07["effect_unit_status"] == "descriptive_cross_landscape_reference"

    rp06 = evidence["C_rp_2006_sensitivity"]
    assert abs(float(rp06["continuous_reference_value"]) - 0.030) < 1e-12
    assert rp06["effect_unit_status"] == "descriptive_temporal_sensitivity"
    sp = evidence["Gadult_Sp"]
    assert abs(float(sp["fragmented_value"]) - 0.0122) < 1e-12
    assert abs(float(sp["continuous_reference_value"]) - 0.0022) < 1e-12
    assert sp["source_harmonization"] == "source_recomputed_continuous_metric"
    kernel = evidence["C_pollen_kernel"]
    assert kernel["fragmented_value"] == "NA"
    assert kernel["continuous_reference_value"] == "NA"
    assert kernel["effect_unit_status"] == "not_reconstructable_as_common_contrast"

    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    ml009 = registry["ML009"]
    assert ml009["study_ids"] == "PS013"
    assert ml009["admissible_primary_layers"] == ""
    assert int(ml009["n_admissible_primary_effects"]) == 0
    assert ml009["covariance_status"] == "not_identifiable_from_one_landscape_per_condition"
    assert ml009["cluster_status"] == "single_landscape_per_condition_no_replication"
    assert "Mothers are not fragmentation replicates" in ml009["independence_note"]

    admitted = {cid for cid, row in registry.items() if row["cluster_status"] == "admissible_multilayer_cluster"}
    assert admitted == {"ML001", "ML002", "ML003", "ML014"}

    print(
        "ML009 Pistacia reference audit: PASS; 2007 season overlap retained descriptively, "
        "but one fragmented vs one continuous landscape contributes 0 effects; current primary denominator=4/11"
    )


if __name__ == "__main__":
    main()
