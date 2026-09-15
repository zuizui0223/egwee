from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
REGISTRY_ML020 = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_extension_ml020.csv"
PROTOCOL = ROOT / "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-13_STATE_SEPARATION_SYNTHESIS.md"
RESULT = ROOT / "manuscript/STATE_SEPARATION_SYNTHESIS_RESULT_2026-09-15_ML020.md"
ML020_CLAIM = ROOT / "manuscript/ML020_CLAIM_GATE.md"
SOCIALIS_EFFECTS = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_effects_v1.csv"
SOCIALIS_COV = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_primary_covariance_v1.csv"
ML020_EFFECTS = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_effects_v1.csv"
ML020_COV = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_covariance_v1.csv"
OLD_ML015_COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_primary_covariance_v1.csv"
GRADIENT_EFFECTS = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv"
GRADIENT_COV = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_covariance_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (
        REGISTRY,
        REGISTRY_ML020,
        PROTOCOL,
        RESULT,
        ML020_CLAIM,
        SOCIALIS_EFFECTS,
        SOCIALIS_COV,
        ML020_EFFECTS,
        ML020_COV,
        GRADIENT_EFFECTS,
        GRADIENT_COV,
    ):
        assert path.is_file(), path
    assert not OLD_ML015_COV.exists(), "obsolete ML015 primary covariance must remain deleted"

    registry_rows = rows(REGISTRY) + rows(REGISTRY_ML020)
    registry = {r["cluster_id"]: r for r in registry_rows}
    assert len(registry) == len(registry_rows), "duplicate cluster_id across registry files"
    primary = {
        cid: r for cid, r in registry.items()
        if r["cluster_status"] == "admissible_multilayer_cluster"
    }
    assert set(primary) == {"ML001", "ML002", "ML003", "ML014", "ML020"}
    assert sum(int(r["n_admissible_primary_effects"]) for r in primary.values()) == 17
    assert set(registry["ML014"]["admissible_primary_layers"].split(";")) == {"G_mating", "F"}
    assert int(registry["ML014"]["n_admissible_primary_effects"]) == 2
    assert set(registry["ML020"]["admissible_primary_layers"].split(";")) == {"I", "F"}
    assert int(registry["ML020"]["n_admissible_primary_effects"]) == 6
    assert "species dependent within programme" in registry["ML020"]["independent_unit_frame"]

    socialis = rows(SOCIALIS_EFFECTS)
    assert len(socialis) == 2
    assert {r["layer"] for r in socialis} == {"G_mating", "F_reproductive_function"}
    assert all(r["effect_unit_status"] == "g_admissible" for r in socialis)
    assert len(rows(SOCIALIS_COV)) == 4

    ml020 = rows(ML020_EFFECTS)
    assert len(ml020) == 6
    assert {r["species"] for r in ml020} == {
        "Atamisquea emarginata",
        "Cercidium australe",
        "Prosopis nigra",
    }
    assert {r["layer"] for r in ml020} == {"I_interaction", "F_reproductive_function"}
    assert all(int(r["n_fragmented"]) == 4 and int(r["n_reference"]) == 4 for r in ml020)
    ml020_cov = rows(ML020_COV)
    assert len(ml020_cov) == 12

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
    assert "ML015 is **not** included in the primary Fisher combination" in protocol
    assert "combine Hedges-g and Fisher-z cluster p-values" in protocol

    result = RESULT.read_text(encoding="utf-8")
    assert "Five independent primary programme/study clusters" in result
    assert "ML020 Aizen–Feinsinger replicated Chaco programme" in result
    assert "p = `0.012124324105113144`" in result
    assert "omit ML001: p = `0.18194352880824005`" in result
    assert "does **not** remove the Serapias dependency" in result

    claim = ML020_CLAIM.read_text(encoding="utf-8")
    assert "Full five-cluster Fisher: `p=0.01212432`" in claim
    assert "Omit ML001 Serapias: `p=0.18194353`, no rejection" in claim
    assert "Do not count the three species as three independent systems" in claim

    print(
        "State-separation family boundary: PASS; primary ML001-ML003+ML014+ML020 = 5 clusters / 17 marginal effects; "
        "ML020 counts once despite three dependent species; ML015 remains separate Fisher-z gradient generalisation; "
        "omit-ML001 does not reject"
    )


if __name__ == "__main__":
    main()
