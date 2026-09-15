from __future__ import annotations

import csv
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STANDS = ROOT / "evidence/meta_extraction/PS021_white_spruce_1994_stand_table_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/PS021_white_spruce_effects_v1.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
SEED = ROOT / "manuscript/meta_analysis_primary_study_seed_v1.csv"
CANDIDATES = ROOT / "manuscript/meta_analysis_candidate_ledger.csv"
CONTRACT = ROOT / "manuscript/WHITE_SPRUCE_2006_ML016_RECOVERY_CONTRACT.md"
RESULT = ROOT / "manuscript/WHITE_SPRUCE_2006_ML016_RECOVERY_RESULT.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def hedges_g_ls(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    df = n1 + n2 - 2
    s1, s2 = stats.stdev(fragmented), stats.stdev(reference)
    pooled = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / df)
    d = (stats.mean(fragmented) - stats.mean(reference)) / pooled
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    variance = 1 / n1 + 1 / n2 + g**2 / (2 * (n1 + n2))
    return g, variance


def main() -> None:
    for path in (STANDS, EFFECTS, REGISTRY, SEED, CANDIDATES, CONTRACT, RESULT):
        assert path.is_file(), path

    stands = rows(STANDS)
    assert len(stands) == 23
    assert sum(r["stand_size_class"] == "small" for r in stands) == 11
    assert sum(r["stand_size_class"] == "medium" for r in stands) == 6
    assert sum(r["stand_size_class"] == "large" for r in stands) == 6
    assert {r["stand"] for r in stands} == set("ABCDEFGHIJKLMNOPQRSTUVW")
    assert all(r["F_filled_seeds_per_cone"] == "" for r in stands)
    assert all(r["F_representation_status"] == "figure_only_not_digitized" for r in stands)

    small = [float(r["t_m_pct"]) for r in stands if r["stand_size_class"] == "small"]
    large = [float(r["t_m_pct"]) for r in stands if r["stand_size_class"] == "large"]
    g, variance = hedges_g_ls(small, large)
    assert abs(g - (-1.0471281101717307)) < 1e-12
    assert abs(variance - 0.28982508931434053) < 1e-12

    effects = {r["endpoint_id"]: r for r in rows(EFFECTS)}
    assert set(effects) == {"Gmating_tm", "F_filled_seeds_per_cone"}
    gm = effects["Gmating_tm"]
    assert gm["effect_unit_status"] == "descriptive_only_due_missing_companion_layer"
    assert gm["independent_unit"] == "stand"
    assert int(gm["n_independent_fragmented"]) == 11
    assert int(gm["n_independent_reference"]) == 6
    assert abs(float(gm["oriented_effect"]) - g) < 1e-12
    assert abs(float(gm["oriented_variance"]) - variance) < 1e-12
    f = effects["F_filled_seeds_per_cone"]
    assert f["effect_unit_status"] == "reproductive_stand_vector_not_reconstructable"
    assert f["raw_effect"] == "" and f["oriented_effect"] == ""

    registry = {r["cluster_id"]: r for r in rows(REGISTRY)}
    ml016 = registry["ML016"]
    assert ml016["admissible_primary_layers"] == ""
    assert int(ml016["n_admissible_primary_effects"]) == 0
    assert ml016["cluster_status"] == "reproductive_stand_vector_not_reconstructable"
    primary = [r for r in registry.values() if r["cluster_status"] == "admissible_multilayer_cluster"]
    assert {r["cluster_id"] for r in primary} == {"ML001", "ML002", "ML003", "ML014"}
    assert sum(int(r["n_admissible_primary_effects"]) for r in primary) == 11

    seed = rows(SEED)
    assert any(r["study_id"] == "PS021" and r["doi"] == "10.1038/sj.hdy.6800886;10.1139/b06-051" for r in seed)
    candidates = rows(CANDIDATES)
    assert any(r["candidate_id"] == "C20" and r["system"] == "Picea glauca white spruce" for r in candidates)

    text = RESULT.read_text(encoding="utf-8")
    for token in (
        "reproductive_stand_vector_not_reconstructable",
        "g = -1.04712811",
        "zero primary effects and zero primary clusters",
        "4 independent primary clusters / 11 effects",
        "Do not digitize Figure 2",
    ):
        assert token in text, token

    print(
        "ML016 white spruce closure: PASS; stand-level t_m descriptive g="
        f"{g:.6f} var={variance:.6f}; F stand vector unavailable; primary denominator remains 4 clusters / 11 effects"
    )


if __name__ == "__main__":
    main()
