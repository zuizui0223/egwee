from __future__ import annotations

import csv
import json
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALUES = ROOT / "evidence/meta_extraction/phase2_cf01_prunus_2014_population_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_prunus_2014_effects_v1.csv"
COVARIANCE = ROOT / "evidence/meta_extraction/phase2_cf01_prunus_2014_covariance_v1.json"
CONTRACT = ROOT / "manuscript/CF01_GPAIR_002_PRUNUS_2014_PHASE2_RECOVERY_CONTRACT.md"
STATUS = ROOT / "manuscript/PHASE2_CF01_PRUNUS_2014_RECOVERY_2026-09-19.md"

POP_ORDER = ["Bradi", "DarabaSigsi", "Demba", "Dishi", "Kambo", "Metin", "Temcha", "Wonse"]
GROUP = {
    "Bradi": "large", "DarabaSigsi": "large", "Demba": "small", "Dishi": "small",
    "Kambo": "large", "Metin": "small", "Temcha": "small", "Wonse": "large",
}
TOL = 5e-10


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def hedges_g(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    df = n1 + n2 - 2
    sp = math.sqrt(
        ((n1 - 1) * stats.stdev(fragmented) ** 2 + (n2 - 1) * stats.stdev(reference) ** 2) / df
    )
    d = (stats.mean(fragmented) - stats.mean(reference)) / sp
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    var = 1 / n1 + 1 / n2 + g * g / (2 * (n1 + n2))
    return g, var


def pearson(x: list[float], y: list[float]) -> float:
    mx, my = stats.mean(x), stats.mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    return sum(a*b for a,b in zip(dx,dy)) / math.sqrt(sum(a*a for a in dx) * sum(b*b for b in dy))


def residuals(values: dict[str, float]) -> list[float]:
    means = {
        group: stats.mean(values[p] for p in POP_ORDER if GROUP[p] == group)
        for group in ("large", "small")
    }
    return [values[p] - means[GROUP[p]] for p in POP_ORDER]


def main() -> None:
    for path in (VALUES, EFFECTS, COVARIANCE, CONTRACT, STATUS):
        assert path.is_file(), path

    value_rows = rows(VALUES)
    assert len(value_rows) == 8
    assert [r["patch"] for r in value_rows] == POP_ORDER
    assert all(r["independent_unit_note"] == "forest_patch_is_independent_fragmentation_unit" for r in value_rows)

    adult = {r["patch"]: float(r["G_adult_HS"]) for r in value_rows}
    seed = {r["patch"]: float(r["G_offspring_HS"]) for r in value_rows}
    assert adult == {
        "Bradi": 0.817, "DarabaSigsi": 0.793, "Demba": 0.758, "Dishi": 0.767,
        "Kambo": 0.768, "Metin": 0.732, "Temcha": 0.757, "Wonse": 0.760,
    }
    assert seed == {
        "Bradi": 0.746, "DarabaSigsi": 0.713, "Demba": 0.716, "Dishi": 0.738,
        "Kambo": 0.739, "Metin": 0.654, "Temcha": 0.692, "Wonse": 0.711,
    }

    effects = {r["layer"]: r for r in rows(EFFECTS)}
    assert set(effects) == {"G_adult", "G_offspring"}
    computed = {}
    for layer, values in (("G_adult", adult), ("G_offspring", seed)):
        frag = [values[p] for p in POP_ORDER if GROUP[p] == "small"]
        ref = [values[p] for p in POP_ORDER if GROUP[p] == "large"]
        g, var = hedges_g(frag, ref)
        row = effects[layer]
        assert row["cluster_id"] == "P2_CF01_GPAIR_002"
        assert row["effect_unit_status"] == "g_admissible"
        assert row["independent_unit"] == "forest_patch"
        assert int(row["n_fragmented"]) == int(row["n_reference"]) == 4
        assert abs(float(row["fragmented_mean"]) - stats.mean(frag)) < TOL
        assert abs(float(row["fragmented_sd"]) - stats.stdev(frag)) < TOL
        assert abs(float(row["reference_mean"]) - stats.mean(ref)) < TOL
        assert abs(float(row["reference_sd"]) - stats.stdev(ref)) < TOL
        assert abs(float(row["oriented_effect"]) - g) < TOL
        assert abs(float(row["oriented_variance"]) - var) < TOL
        computed[layer] = (g, var)

    rho = pearson(residuals(adult), residuals(seed))
    va = computed["G_adult"][1]
    vs = computed["G_offspring"][1]
    cov = rho * math.sqrt(va * vs)
    delta = computed["G_adult"][0] - computed["G_offspring"][0]
    dvar = va + vs - 2 * cov
    dse = math.sqrt(dvar)
    z = delta / dse
    p = math.erfc(abs(z) / math.sqrt(2))

    cj = json.loads(COVARIANCE.read_text(encoding="utf-8"))
    pair = cj["primary_pair"]
    assert pair["positive_definite"] is True
    assert abs(pair["residual_correlation"] - rho) < 1e-9
    assert abs(pair["sampling_covariance"] - cov) < 1e-9
    assert abs(pair["effect_difference_Gadult_minus_Goffspring"] - delta) < 1e-9
    assert abs(pair["difference_variance"] - dvar) < 1e-9
    assert abs(pair["p_two_sided"] - p) < 1e-9
    assert min(pair["eigenvalues_ascending"]) > 0

    contract = CONTRACT.read_text(encoding="utf-8")
    for token in ("retrospective external recovery", "small patch", "large patch", "gene diversity `H_S`", "forest patch"):
        assert token in contract, token

    status = STATUS.read_text(encoding="utf-8")
    for token in (
        "pair-specific covariance-aware Phase-2 cluster",
        "4 independent programmes",
        "remains closed at **4/5**",
        "Afrocarpus remains a registered prospective candidate",
    ):
        assert token in status, token

    print(
        "PHASE2_CF01_PRUNUS_2014_OK "
        f"Gadult={computed['G_adult'][0]:.8f} "
        f"Goffspring={computed['G_offspring'][0]:.8f} "
        f"delta={delta:.8f} p={p:.8f} pair_covariance=PD"
    )


if __name__ == "__main__":
    main()
