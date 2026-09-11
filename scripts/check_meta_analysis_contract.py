from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
PROTOCOL = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md"
SCHEMA = ROOT / "manuscript/meta_analysis_effect_schema.json"
METADATA = ROOT / "manuscript/meta_analysis_submission_metadata.md"
LEDGER = ROOT / "manuscript/meta_analysis_candidate_ledger.csv"
SEEDS = ROOT / "manuscript/meta_analysis_seed_sources.md"
PRIMARY_SEED = ROOT / "manuscript/meta_analysis_primary_study_seed_v1.csv"
PRIMARY_SEED_SOURCES = ROOT / "manuscript/meta_analysis_primary_study_seed_v1_sources.md"


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (
        README,
        MANUSCRIPT,
        PROTOCOL,
        SCHEMA,
        METADATA,
        LEDGER,
        SEEDS,
        PRIMARY_SEED,
        PRIMARY_SEED_SOURCES,
    ):
        assert path.is_file(), path

    readme = README.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    protocol = PROTOCOL.read_text(encoding="utf-8")
    metadata = METADATA.read_text(encoding="utf-8")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    assert "active paper is now a multilevel meta-analysis" in readme
    assert "Question 1" in readme and "Question 2" in readme
    assert "H1 — biological layers do not share one fragmentation response" in manuscript
    assert "H2 — contemporary processes can change before standing adult genetics" in manuscript
    assert "H3 — process compensation modifies the function response" in manuscript
    assert "not yet claimed" in manuscript.lower()
    assert "primary meta-analysis requires a direct fragmented-versus-reference comparison" in protocol.lower()
    assert "Missing biological layers are not coded as zero effects" in protocol
    assert "Do not define a `compensated` category" in protocol
    assert schema["schema_version"] == 1
    assert schema["primary_effect_stream"] == "hedges_g_fragmented_minus_reference"
    assert schema["secondary_effect_stream"] == "fisher_z_correlation_with_fragmentation_severity"
    assert set(schema["primary_layers"]) == {
        "D_resource_demography",
        "I_interaction",
        "C_movement_connectivity",
        "F_reproductive_function",
        "G_adult",
        "G_offspring",
    }
    assert "protocol_locked_screening_and_extraction_pending" in metadata
    for forbidden in (
        "meta-analysis demonstrates",
        "meta-analysis showed",
        "pooled effect was",
        "significantly more negative",
    ):
        assert forbidden not in manuscript.lower(), forbidden

    primary = _csv_rows(PRIMARY_SEED)
    assert len(primary) >= 14, len(primary)
    ids = [r["study_id"] for r in primary]
    assert len(ids) == len(set(ids)), "duplicate primary study_id"
    dois = [r["doi"].strip().lower() for r in primary if r["doi"].strip()]
    assert len(dois) == len(set(dois)), "duplicate DOI in primary-study seed"
    assert all(r["verified_layers"].strip() for r in primary)
    assert all(r["source_status"] == "source_verified" for r in primary)
    assert sum(r["seed_priority"] == "very_high" for r in primary) >= 4
    assert any(r["study_id"] == "PS001" and "G_offspring" in r["verified_layers"] for r in primary)
    assert any(r["study_id"] == "PS004" and r["fragmentation_design"] == "3_continuous_vs_3_fragmented" for r in primary)
    assert any(r["study_id"] == "PS014" and "I" in r["verified_layers"] and "F" in r["verified_layers"] for r in primary)

    candidates = _csv_rows(LEDGER)
    assert len(candidates) >= 18, len(candidates)
    assert any(r["system"] == "Spondias purpurea" and "source_verified" in r["current_status"] for r in candidates)
    assert any(r["system"] == "Brosimum alicastrum" and "priority_extraction" in r["current_status"] for r in candidates)
    assert any(r["system"] == "Magnolia stellata" and r["direct_fragmentation_contrast"] == "gradient" for r in candidates)

    provenance = PRIMARY_SEED_SOURCES.read_text(encoding="utf-8")
    for doi in (
        "10.1016/j.biocon.2021.109007",
        "10.1186/1472-6785-13-10",
        "10.1186/s12870-015-0600-8",
        "10.1002/ajb2.16157",
        "10.1111/1365-2745.14452",
    ):
        assert doi in provenance, doi

    print(
        "EGWEE multilayer meta-analysis contract: PASS; "
        f"{len(primary)} source-verified primary-study seeds, {len(candidates)} candidate systems"
    )


if __name__ == "__main__":
    main()
