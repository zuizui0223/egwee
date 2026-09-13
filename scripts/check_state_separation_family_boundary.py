from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
PROTOCOL = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-13_STATE_SEPARATION_SYNTHESIS.md"
RESULT = ROOT / "manuscript/STATE_SEPARATION_SYNTHESIS_RESULT_2026-09-13.md"
STATUS = ROOT / "manuscript/META_ANALYSIS_CLUSTER_STATUS_2026-09-12.md"
OLD_ML015_COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_primary_covariance_v1.csv"
GRADIENT_EFFECTS = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv"
GRADIENT_COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_covariance_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (REGISTRY, PROTOCOL, RESULT, STATUS, GRADIENT_EFFECTS, GRADIENT_COV):
        assert path.is_file(), path
    assert not OLD_ML015_COV.exists(), "obsolete ML015 primary covariance must remain deleted"

    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    primary = {
        cid: r for cid, r in registry.items()
        if r["cluster_status"] == "admissible_multilayer_cluster"
    }
    assert set(primary) == {"ML001", "ML002", "ML003"}
    assert sum(int(r["n_admissible_primary_effects"]) for r in primary.values()) == 9

    ml015 = registry["ML015"]
    assert ml015["design_stream"] == "fisher_z_gradient_generalisation"
    assert ml015["cluster_status"] == "gradient_generalisation_multilayer_cluster"
    assert ml015["admissible_primary_layers"] == ""
    assert int(ml015["n_admissible_primary_effects"]) == 0

    effects = rows(GRADIENT_EFFECTS)
    assert len(effects) == 3
    assert {r["layer"] for r in effects} == {"I", "F", "G_adult"}
    assert all(r["effect_stream"] == "fisher_z_gradient" for r in effects)
    assert all(r["effect_unit_status"] == "fisher_z_admissible" for r in effects)

    protocol = PROTOCOL.read_text(encoding="utf-8")
    assert "k = 3" in protocol
    assert "ML015 is **not** included in the primary Fisher combination" in protocol
    assert "combine Hedges-g and Fisher-z cluster p-values" in protocol

    result = RESULT.read_text(encoding="utf-8")
    assert "three independently admitted" in result
    assert "combined p: **0.00621**" in result
    assert "p_cluster = 0.00256953" in result
    assert "not counted as a fourth primary cluster" in result
    assert "superseded implementation" in result

    status = STATUS.read_text(encoding="utf-8")
    assert "independent **primary** admissible multilayer clusters: **3**" in status
    assert "primary admissible effects inside those clusters: **9**" in status
    assert "separate admissible Fisher-z gradient effects: **5**" in status
    assert "ML015 is **not** a fourth primary cluster" in status
    assert "chi-square(6) = 18.0086" in status

    print(
        "State-separation family boundary: PASS; primary ML001-ML003 = 3 clusters / 9 effects; "
        "ML015 = separate 3-effect Fisher-z gradient generalisation; no cross-family Fisher combination"
    )


if __name__ == "__main__":
    main()
