from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
PROTOCOL = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_2026-09-11.md"
EFFECT_AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-11_EFFECT_UNITS.md"
COHORT_AMENDMENT = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-13_COHORT_DEPENDENCE.md"
SCHEMA = ROOT / "manuscript/meta_analysis_effect_schema.json"
METADATA = ROOT / "manuscript/meta_analysis_submission_metadata.md"
LEDGER = ROOT / "manuscript/meta_analysis_candidate_ledger.csv"
PRIMARY_SEED = ROOT / "manuscript/meta_analysis_primary_study_seed_v1.csv"
PRIMARY_SEED_SOURCES = ROOT / "manuscript/meta_analysis_primary_study_seed_v1_sources.md"
EXTRACTION_QUEUE = ROOT / "manuscript/meta_analysis_extraction_queue_v1.csv"
SPONDIAS = ROOT / "evidence/meta_extraction/PS001_spondias_extraction_v1.csv"
SPONDIAS_EFFECTS = ROOT / "evidence/meta_extraction/PS001_spondias_site_effects_v1.csv"
SPONDIAS_GEN = ROOT / "evidence/meta_extraction/PS001_spondias_appendixB_genetic_site_table_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (
        README, MANUSCRIPT, PROTOCOL, EFFECT_AMENDMENT, COHORT_AMENDMENT, SCHEMA,
        METADATA, LEDGER, PRIMARY_SEED, PRIMARY_SEED_SOURCES, EXTRACTION_QUEUE,
        SPONDIAS, SPONDIAS_EFFECTS, SPONDIAS_GEN,
    ):
        assert path.is_file(), path

    readme = README.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    protocol = PROTOCOL.read_text(encoding="utf-8")
    effect_amendment = EFFECT_AMENDMENT.read_text(encoding="utf-8")
    cohort_amendment = COHORT_AMENDMENT.read_text(encoding="utf-8")
    metadata = METADATA.read_text(encoding="utf-8")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    # The repository is now results-bearing. Guard the current conditional
    # conclusion rather than obsolete protocol-only wording.
    assert "active paper is a cluster-first empirical synthesis" in readme
    assert "five independent programme/study clusters / 17 marginal effects" in readme
    assert "not Serapias-independent" in readme
    assert "Primary hypothesis — response layers are not universally exchangeable" in manuscript
    assert "The pooled rejection is not leave-one-cluster-out robust" in manuscript
    assert "Status of the original H2 and H3 extensions" in manuscript
    assert "primary meta-analysis requires a direct fragmented-versus-reference comparison" in protocol.lower()
    assert "pseudo-replication firewall" in effect_amendment.lower()
    assert "proxy_pairwise_low_rank" in cohort_amendment
    assert "does not by itself establish a cohort lag" in cohort_amendment
    assert "results_bearing_conditional_state_separation" in metadata
    assert "p = 0.01212432" in metadata
    assert "p = 0.18194353" in metadata

    assert schema["schema_version"] == 2
    assert schema["primary_effect_stream"] == "hedges_g_fragmented_minus_reference"
    assert schema["secondary_effect_stream"] == "fisher_z_correlation_with_fragmentation_severity"
    assert set(schema["effect_unit_status_values"]) == {
        "g_admissible", "fisher_z_admissible", "model_contrast_pending_standardisation",
        "raw_reanalysis_required", "descriptive_only",
    }

    primary = rows(PRIMARY_SEED)
    candidates = rows(LEDGER)
    queue = rows(EXTRACTION_QUEUE)
    assert len(primary) >= 16
    assert len(candidates) >= 19
    assert len(queue) >= 9
    assert len({r["study_id"] for r in primary}) == len(primary)
    assert {r["study_id"] for r in queue} <= {r["study_id"] for r in primary}
    assert any(r["study_id"] == "PS001" and "G_offspring" in r["verified_layers"] for r in primary)
    assert any(r["system"] == "Spondias purpurea" and "source_verified" in r["current_status"] for r in candidates)

    # Appendix B changes the PS001 effect-unit state: site-level adult, juvenile
    # and seed genetics are now admissible, while I/F and pollen-distance remain blocked.
    spondias = rows(SPONDIAS)
    effects = rows(SPONDIAS_EFFECTS)
    genetic = rows(SPONDIAS_GEN)
    assert len(spondias) == 13
    assert len(effects) == 8
    assert len(genetic) == 15

    by_endpoint = {r["endpoint_id"]: r for r in spondias}
    assert {r["endpoint_id"] for r in spondias if r["effect_unit_status"] == "g_admissible"} == {
        "C_paternity_correlation", "Gadult_Ho", "Gadult_Fis", "Gadult_Sp",
        "Goffspring_juvenile_Ho", "Goffspring_seed_Ho",
        "Goffspring_juvenile_F", "Goffspring_seed_F",
    }
    assert {r["endpoint_id"] for r in spondias if r["effect_unit_status"] == "model_contrast_pending_standardisation"} == {
        "I_visitation", "F_fruit_production", "F_fruit_set"
    }
    assert by_endpoint["C_pollen_distance"]["effect_unit_status"] == "raw_reanalysis_required"
    assert by_endpoint["C_effective_sires"]["effect_unit_status"] == "descriptive_only"
    assert all(r["independent_unit"] == "site" for r in spondias if r["effect_unit_status"] == "g_admissible")

    effect_by_endpoint = {r["endpoint_id"]: r for r in effects}
    assert {e for e, r in effect_by_endpoint.items() if r["analysis_role"] == "primary"} == {
        "C_paternity_correlation", "Gadult_Ho", "Gjuvenile_Ho", "Gseed_Ho"
    }
    assert effect_by_endpoint["Gadult_Sp"]["analysis_role"] == "sensitivity_structure"
    assert {e for e, r in effect_by_endpoint.items() if r["analysis_role"] == "sensitivity_metric"} == {
        "Gadult_Fis", "Gjuvenile_Fis", "Gseed_Fis"
    }
    assert all(r["effect_unit_status"] == "g_admissible" for r in effects)
    assert all(int(r["n_independent_fragmented"]) == 3 for r in effects)
    assert all(int(r["n_independent_reference"]) == 2 for r in effects)

    assert {r["developmental_stage"] for r in genetic} == {"adult", "juvenile", "seed"}
    assert {r["population"] for r in genetic} == {"Careyes", "Chamela", "Mesa", "Nacastillo", "Ranchitos"}
    assert all(r["source_location"].endswith("Appendix B (mmc1.docx)") for r in genetic)

    provenance = PRIMARY_SEED_SOURCES.read_text(encoding="utf-8")
    assert "10.1016/j.biocon.2021.109007" in provenance

    print(
        "EGWEE multilayer meta-analysis contract: PASS; "
        f"{len(primary)} verified studies, {len(candidates)} candidates, {len(queue)} queued; "
        "active paper is results-bearing with conditional state separation and locked claim sync"
    )


if __name__ == "__main__":
    main()
