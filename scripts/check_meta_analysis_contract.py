from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
PROTOCOL = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md"
AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-11_EFFECT_UNITS.md"
SCHEMA = ROOT / "manuscript/meta_analysis_effect_schema.json"
METADATA = ROOT / "manuscript/meta_analysis_submission_metadata.md"
LEDGER = ROOT / "manuscript/meta_analysis_candidate_ledger.csv"
SEEDS = ROOT / "manuscript/meta_analysis_seed_sources.md"
PRIMARY_SEED = ROOT / "manuscript/meta_analysis_primary_study_seed_v1.csv"
PRIMARY_SEED_SOURCES = ROOT / "manuscript/meta_analysis_primary_study_seed_v1_sources.md"
EXTRACTION_QUEUE = ROOT / "manuscript/meta_analysis_extraction_queue_v1.csv"
SPONDIAS = ROOT / "evidence/meta_extraction/PS001_spondias_extraction_v1.csv"
SPONDIAS_SITE_EFFECTS = ROOT / "evidence/meta_extraction/PS001_spondias_site_effects_v1.csv"


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (
        README, MANUSCRIPT, PROTOCOL, AMENDMENT, SCHEMA, METADATA, LEDGER, SEEDS,
        PRIMARY_SEED, PRIMARY_SEED_SOURCES, EXTRACTION_QUEUE, SPONDIAS, SPONDIAS_SITE_EFFECTS,
    ):
        assert path.is_file(), path

    readme = README.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    protocol = PROTOCOL.read_text(encoding="utf-8")
    amendment = AMENDMENT.read_text(encoding="utf-8")
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

    assert "pseudo-replication firewall" in amendment.lower()
    assert "do not manufacture g" in amendment.lower()
    assert schema["schema_version"] == 2
    assert schema["amendment"] == "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-11_EFFECT_UNITS.md"
    for field in (
        "effect_unit_status", "effect_unit_note", "independent_unit", "dispersion_unit",
        "n_independent_fragmented", "n_independent_reference", "n_individuals_fragmented",
        "n_individuals_reference",
    ):
        assert field in schema["required_fields"], field
    assert schema["primary_effect_stream"] == "hedges_g_fragmented_minus_reference"
    assert schema["secondary_effect_stream"] == "fisher_z_correlation_with_fragmentation_severity"
    assert set(schema["primary_layers"]) == {
        "D_resource_demography", "I_interaction", "C_movement_connectivity",
        "F_reproductive_function", "G_adult", "G_offspring",
    }
    assert set(schema["effect_unit_status_values"]) == {
        "g_admissible", "fisher_z_admissible", "model_contrast_pending_standardisation",
        "raw_reanalysis_required", "descriptive_only",
    }
    for forbidden_shortcut in (
        "pair_individual_sample_size_with_locus_level_SD",
        "treat_nested_offspring_or_paternity_events_as_independent_fragmentation_replicates",
        "force_model_based_contrasts_into_Hedges_g_without_compatible_standardisation",
    ):
        assert forbidden_shortcut in schema["forbidden_shortcuts"]

    assert "protocol_locked_screening_and_extraction_pending" in metadata
    for forbidden in (
        "meta-analysis demonstrates", "meta-analysis showed", "pooled effect was", "significantly more negative",
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

    queue = _csv_rows(EXTRACTION_QUEUE)
    assert len(queue) >= 7
    priorities = [int(r["priority"]) for r in queue]
    assert priorities == sorted(priorities), priorities
    assert queue[0]["study_id"] == "PS001"
    assert {r["design_stream"] for r in queue} >= {"hedges_g_direct", "fisher_z_gradient"}
    assert any(r["study_id"] == "PS004" for r in queue)
    assert any(r["study_id"] == "PS014" for r in queue)

    # PS001 now has one effect-unit-valid C endpoint reconstructed from five
    # site-specific Table 3 estimates. The lower-level firewall remains active
    # for I/F/G and pollen-distance summaries.
    spondias = _csv_rows(SPONDIAS)
    spondias_site = _csv_rows(SPONDIAS_SITE_EFFECTS)
    assert len(spondias) >= 10
    assert len(spondias_site) == 1
    allowed = set(schema["effect_unit_status_values"])
    assert all(r["effect_unit_status"] in allowed for r in spondias)
    s_g = [r for r in spondias if r["effect_unit_status"] == "g_admissible"]
    assert len(s_g) == 1 and s_g[0]["endpoint_id"] == "C_paternity_correlation"
    assert s_g[0]["independent_unit"] == "site"
    assert sum(r["effect_unit_status"] == "model_contrast_pending_standardisation" for r in spondias) >= 3
    assert sum(r["effect_unit_status"] == "raw_reanalysis_required" for r in spondias) >= 5
    assert any(r["endpoint_id"] == "C_effective_sires" and r["effect_unit_status"] == "descriptive_only" for r in spondias)
    assert any("locus" in r["effect_unit_note"].lower() for r in spondias)
    assert any("nested" in r["effect_unit_note"].lower() for r in spondias)
    assert spondias_site[0]["endpoint_id"] == "C_paternity_correlation"
    assert spondias_site[0]["effect_unit_status"] == "g_admissible"
    assert int(spondias_site[0]["n_independent_fragmented"]) == 3
    assert int(spondias_site[0]["n_independent_reference"]) == 2

    provenance = PRIMARY_SEED_SOURCES.read_text(encoding="utf-8")
    for doi in (
        "10.1016/j.biocon.2021.109007", "10.1186/1472-6785-13-10",
        "10.1186/s12870-015-0600-8", "10.1002/ajb2.16157", "10.1111/1365-2745.14452",
    ):
        assert doi in provenance, doi

    print(
        "EGWEE multilayer meta-analysis contract: PASS; "
        f"{len(primary)} source-verified primary-study seeds, "
        f"{len(candidates)} candidate systems, {len(queue)} queued extraction studies, "
        f"{len(spondias)} PS001 endpoints; effect-unit firewall active, "
        "one site-level Spondias C effect admitted without promoting nested I/F/G units"
    )


if __name__ == "__main__":
    main()
