from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "manuscript/PENSTEMON_2019_ISOLATION_CLUSTER_RECOVERY_CONTRACT.md"
RESULT = ROOT / "manuscript/PENSTEMON_2019_ISOLATION_CLUSTER_RECOVERY_RESULT.md"
EVIDENCE = ROOT / "evidence/meta_extraction/C07_penstemon_2019_schema_gate_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (CONTRACT, RESULT, EVIDENCE, REGISTRY):
        assert path.is_file(), path

    contract = CONTRACT.read_text(encoding="utf-8")
    result = RESULT.read_text(encoding="utf-8")
    assert "mean distance from each experimental roof population to the other nine" in contract
    assert "isolation_severity = z(mean_distance_to_other_roofs)" in contract
    assert "source parentage assignments" in contract
    assert "Do **not** casually reproduce or replace that procedure" in contract
    assert "three natural-prairie versus three established-green-roof" in contract
    assert "source_parentage_assignments_not_reconstructable" in result
    assert "no source assignment-output fields" in result
    assert "other study data are available from the corresponding author on request" in result
    assert "G_offspring is therefore recorded as `structurally_reconstructable_but_not_opened_after_multilayer_gate_failure`" in result
    assert "Figure 4 is not digitized" in result

    evidence = rows(EVIDENCE)
    assert len(evidence) == 3
    by_layer = {(r["design_component"], r["layer"]): r for r in evidence}
    c = by_layer[("ten_experimental_roofs", "C_movement_connectivity")]
    assert c["independent_unit"] == "roof_population"
    assert "no_assignment_father_LOD_confidence_fields" in c["schema_status"]
    assert c["quantitative_effect_status"] == "source_parentage_assignments_not_reconstructable"
    g = by_layer[("ten_experimental_roofs", "G_offspring")]
    assert "9_diploid_loci" in g["schema_status"]
    assert g["quantitative_effect_status"] == "structurally_reconstructable_but_not_opened_after_multilayer_gate_failure"
    adult = by_layer[("natural_vs_established_roofs", "G_adult")]
    assert adult["quantitative_effect_status"] == "separate_design_not_joined_to_ML010"

    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    ml010 = registry["ML010"]
    assert ml010["study_ids"] == "C07"
    assert ml010["fragmentation_contrast"] == "source_defined_mean_distance_to_other_nine_roofs"
    assert ml010["admissible_primary_layers"] == ""
    assert int(ml010["n_admissible_primary_effects"]) == 0
    assert ml010["covariance_status"] == "blocked_before_effect_calculation"
    assert ml010["cluster_status"] == "source_parentage_assignments_not_reconstructable"
    assert "do not reimplement parentage or digitize Figure 4" in ml010["next_recovery_action"]

    admitted = {cid for cid, row in registry.items() if row["cluster_status"] == "admissible_multilayer_cluster"}
    assert admitted == {"ML001", "ML002", "ML003", "ML014"}

    print(
        "ML010 Penstemon recovery contract: PASS; source parentage assignments absent, "
        "G structurally recoverable but unopened, ML010 adds 0 effects; current primary denominator=4/11"
    )


if __name__ == "__main__":
    main()
