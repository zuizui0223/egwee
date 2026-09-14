from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EFFECTS = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_primary_covariance_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
SEED = ROOT / "manuscript/meta_analysis_primary_study_seed_v1.csv"
RESULT = ROOT / "manuscript/EUCALYPTUS_SOCIALIS_2012_ML014_RECOVERY_RESULT.md"
EFFECT_UNIT_AUDIT = ROOT / "manuscript/EUCALYPTUS_SOCIALIS_2012_EFFECT_UNIT_AUDIT.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    for path in (EFFECTS, COV, REGISTRY, SEED, RESULT, EFFECT_UNIT_AUDIT):
        assert path.is_file(), path

    effects = {r["endpoint_id"]: r for r in rows(EFFECTS)}
    assert set(effects) == {"Gmating_correlated_paternity_rp", "F_family_growth"}
    g = effects["Gmating_correlated_paternity_rp"]
    f = effects["F_family_growth"]
    assert g["layer"] == "G_mating"
    assert f["layer"] == "F_reproductive_function"
    assert all(r["effect_unit_status"] == "g_admissible" for r in effects.values())
    assert all(r["independent_unit"] == "maternal_family" for r in effects.values())
    assert all(int(r["n_independent_fragmented"]) == 13 for r in effects.values())
    assert all(int(r["n_independent_reference"]) == 15 for r in effects.values())
    assert abs(float(g["oriented_effect"]) + 1.023913881040) < 1e-9
    assert abs(float(g["oriented_variance"]) - 0.162311165657) < 1e-9
    assert abs(float(f["oriented_effect"]) + 0.271808874814) < 1e-9
    assert abs(float(f["oriented_variance"]) - 0.144909030455) < 1e-9

    endpoints = ["Gmating_correlated_paternity_rp", "F_family_growth"]
    cov = {(r["endpoint_i"], r["endpoint_j"]): r for r in rows(COV)}
    assert set(cov) == {(a, b) for a in endpoints for b in endpoints}
    off = cov[(endpoints[0], endpoints[1])]
    assert abs(float(off["correlation_proxy"]) - 0.326729868213) < 1e-9
    assert abs(float(off["sampling_covariance"]) - 0.050108426040) < 1e-9
    v1 = float(cov[(endpoints[0], endpoints[0])]["sampling_covariance"])
    v2 = float(cov[(endpoints[1], endpoints[1])]["sampling_covariance"])
    c = float(off["sampling_covariance"])
    assert v1 > 0 and v2 > 0 and v1 * v2 - c * c > 1e-12

    diff = float(g["oriented_effect"]) - float(f["oriented_effect"])
    contrast_var = v1 + v2 - 2 * c
    z = diff / math.sqrt(contrast_var)
    p = math.erfc(abs(z) / math.sqrt(2))
    assert abs(diff + 0.752105006226) < 1e-9
    assert abs(p - 0.09831773773971167) < 1e-9

    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    ml014 = registry["ML014"]
    assert ml014["cluster_status"] == "admissible_multilayer_cluster"
    assert ml014["design_stream"] == "hedges_g_direct"
    assert set(ml014["admissible_primary_layers"].split(";")) == {"G_mating", "F"}
    assert int(ml014["n_admissible_primary_effects"]) == 2
    assert ml014["covariance_status"] == "proxy_reconstructed_from_paired_families"
    primary = [r for r in registry.values() if r["cluster_status"] == "admissible_multilayer_cluster"]
    assert {r["cluster_id"] for r in primary} == {"ML001", "ML002", "ML003", "ML014"}
    assert sum(int(r["n_admissible_primary_effects"]) for r in primary) == 11

    seed = {r["study_id"]: r for r in rows(SEED)}
    assert seed["PS020"]["doi"] == "10.1111/mec.12056"
    assert {"G_mating", "F"} <= set(seed["PS020"]["verified_layers"].split(";"))

    text = RESULT.read_text(encoding="utf-8")
    for token in (
        "ML014_admitted_Gmating_F_covariance_aware",
        "fourth independent **primary Hedges-g multilayer cluster**",
        "`g = -1.02391388`",
        "`g = -0.27180887`",
        "`0.09831774`",
        "4 independent clusters / 11 primary effects",
    ):
        assert token in text, token

    audit = EFFECT_UNIT_AUDIT.read_text(encoding="utf-8")
    for token in (
        "individual local-context observational design",
        "same broad landscape",
        "near-neighbour mothers was explicitly avoided",
        "Why this differs from ML009 Pistacia",
        "not described as a replicated landscape experiment",
        "does not prove absence of all residual spatial correlation",
        "13 fragmented and 15 public complete-case reference families",
    ):
        assert token in audit, token

    print(
        "ML014 Eucalyptus socialis admission: PASS; 13 isolated-pasture + 15 small-remnant families; "
        "G_mating g=-1.023914, F g=-0.271809, covariance-aware p=0.098318; "
        "effect-unit audit confirms within-Monarto maternal-family local-context design; primary denominator=4/11"
    )


if __name__ == "__main__":
    main()
