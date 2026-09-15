from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "manuscript/meta_analysis_candidate_ledger.csv"
PRIMARY = ROOT / "manuscript/meta_analysis_primary_study_seed_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
REGISTRY_ML020 = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_extension_ml020.csv"
SUPP = ROOT / "manuscript/tables/table_s1_cluster_recovery_flow.csv"
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    candidates = rows(CANDIDATES)
    primary = rows(PRIMARY)
    registry = rows(REGISTRY) + rows(REGISTRY_ML020)
    supp = rows(SUPP)
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")

    assert len(candidates) == 20
    assert len(primary) == 19
    assert len(registry) == 16
    assert len({r["cluster_id"] for r in registry}) == 16

    primary_clusters = [r for r in registry if r["cluster_status"] == "admissible_multilayer_cluster"]
    gradient = [r for r in registry if r["cluster_status"] == "gradient_generalisation_multilayer_cluster"]
    closed = [r for r in registry if r not in primary_clusters and r not in gradient]

    assert {r["cluster_id"] for r in primary_clusters} == {"ML001", "ML002", "ML003", "ML014", "ML020"}
    assert {r["cluster_id"] for r in gradient} == {"ML015"}
    assert len(closed) == 10

    replication_statuses = {
        "single_landscape_per_condition_no_replication",
        "single_continuous_reference_population_no_replication",
    }
    replication = [r for r in closed if r["cluster_status"] in replication_statuses]
    recoverability = [r for r in closed if r["cluster_status"] not in replication_statuses]
    assert {r["cluster_id"] for r in replication} == {"ML009", "ML013"}
    assert len(recoverability) == 8

    assert len(supp) == 16
    assert {r["cluster_id"] for r in supp} == {r["cluster_id"] for r in registry}
    classes = {r["cluster_id"]: r["admission_class"] for r in supp}
    assert {cid for cid, cls in classes.items() if cls == "primary_direct"} == {"ML001", "ML002", "ML003", "ML014", "ML020"}
    assert {cid for cid, cls in classes.items() if cls == "gradient_generalisation"} == {"ML015"}
    assert sum(cls == "closed_recoverability" for cls in classes.values()) == 8
    assert sum(cls == "closed_replication" for cls in classes.values()) == 2

    for token in (
        "20 named system/program entries",
        "19 primary-study records",
        "Sixteen multilayer cluster attempts",
        "Five ultimately met the direct Hedges-g primary admission contract",
        "Ten registered attempts were closed without primary admission",
        "Eight closures reflected inability to reconstruct",
        "Two closures (`ML009`, `ML013`) were structural non-identifiability cases",
    ):
        assert token in manuscript, token

    print(
        "STUDY_FLOW_TRANSPARENCY_OK "
        f"candidates={len(candidates)} primary_studies={len(primary)} attempts={len(registry)} "
        f"primary={len(primary_clusters)} gradient={len(gradient)} closed={len(closed)} "
        f"recoverability_closed={len(recoverability)} replication_closed={len(replication)}"
    )


if __name__ == "__main__":
    main()
