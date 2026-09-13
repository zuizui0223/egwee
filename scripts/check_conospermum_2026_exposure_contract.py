from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "manuscript/CONOSPERMUM_2026_CLUSTER_RECOVERY_CONTRACT.md"
RESULT = ROOT / "manuscript/CONOSPERMUM_2026_CLUSTER_RECOVERY_RESULT.md"
AUDIT = ROOT / "manuscript/CONOSPERMUM_2026_EXPOSURE_AUDIT.md"
MATRIX = ROOT / "evidence/meta_extraction/PS011_conospermum_2026_matrix_class_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
EXTRACTION = ROOT / "evidence/meta_extraction/PS011_conospermum_2026_extraction_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (CONTRACT, RESULT, AUDIT, MATRIX, REGISTRY, EXTRACTION):
        assert path.is_file(), path

    contract = CONTRACT.read_text(encoding="utf-8")
    result = RESULT.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")

    # Exposure must be source-defined and outcome-blind.
    for text in (contract, audit):
        assert "modified incidence-function connectivity index" in text
    assert "fragmentation_severity = -z(connectivity_index)" in contract
    assert "use realized pollen immigration to assign the primary landscape exposure" in contract
    assert "urban_barrier / permeable" in audit
    assert "not the primary exposure" in audit

    # Both reopening prerequisites are mandatory; neither may be rescued.
    assert "exact population-specific values" in contract
    assert "seedling genotype bytes" in contract
    for forbidden_rescue in (
        "population size",
        "straight-line distance",
        "area",
        "floral display",
        "binary matrix class",
    ):
        assert forbidden_rescue in contract

    # The terminal result remains a source boundary with no biological effect.
    assert "source_access_blocked + source_exposure_values_not_reconstructable" in result
    assert "No C/G_offspring effect was calculated" in result
    assert "zero quantitative effects" in result
    assert "access-control/transport boundary" in result

    # Matrix classes are retained only as descriptive sensitivity metadata and
    # their current source rationale must not use realized C outcomes.
    matrix = rows(MATRIX)
    assert len(matrix) == 6
    assert {r["population"] for r in matrix} == {"A", "B", "C", "D", "E", "F"}
    assert all("Descriptive landscape sensitivity only" in r["admission_note"] for r in matrix)
    outcome_words = ("pollen immigration", "no pollen", "significant pollen", "m_p")
    assert not any(
        any(word in r["source_basis"].lower() for word in outcome_words)
        for r in matrix
    )

    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    ml005 = registry["ML005"]
    assert ml005["fragmentation_contrast"] == "source_defined_modified_incidence_connectivity_index"
    assert ml005["admissible_primary_layers"] == ""
    assert int(ml005["n_admissible_primary_effects"]) == 0
    assert ml005["covariance_status"] == "blocked_before_effect_calculation"
    assert ml005["cluster_status"] == "source_access_blocked"
    assert "exact population-specific modified-incidence connectivity values" in ml005["next_recovery_action"]
    assert "seedling genotype bytes" in ml005["next_recovery_action"]
    assert "descriptive binary matrix class" in ml005["next_recovery_action"]

    # Existing PS011 extraction rows must still contain no calculated primary
    # effect from this attempted recovery.
    ps011 = rows(EXTRACTION)
    assert ps011
    for row in ps011:
        assert row.get("raw_effect", "") in {"", "NA"}
        assert row.get("oriented_effect", "") in {"", "NA"}

    print(
        "ML005 Conospermum exposure contract: PASS; "
        "continuous source connectivity is primary, matrix classes descriptive only, "
        "0 effects admitted, raw-byte and exact-exposure gates both remain closed"
    )


if __name__ == "__main__":
    main()
