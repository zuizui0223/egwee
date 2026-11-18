from __future__ import annotations

import csv
import json
import math
import statistics as stats
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALUES = ROOT / "evidence/meta_extraction/phase2_cf01_prunus_kakamega_2008_population_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_prunus_kakamega_2008_effects_v1.csv"
COVARIANCE = ROOT / "evidence/meta_extraction/phase2_cf01_prunus_kakamega_2008_covariance_v1.json"
CONTRACT = ROOT / "manuscript/CF01_GPAIR_003_PRUNUS_KAKAMEGA_2008_PHASE2_RECOVERY_CONTRACT.md"
STATUS = ROOT / "manuscript/PHASE2_CF01_PRUNUS_KAKAMEGA_2008_RECOVERY_2026-09-19.md"

SITE_ORDER = ["Malava", "Kisere", "Mukangu", "Buyangu", "Isecheno B", "Isecheno A", "Ikuywa", "Kaimosi"]
GROUP = {
    "Malava": "fragment", "Kisere": "fragment", "Mukangu": "main_forest", "Buyangu": "main_forest",
    "Isecheno B": "main_forest", "Isecheno A": "main_forest", "Ikuywa": "fragment", "Kaimosi": "fragment",
}
TOL = 5e-10


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def hedges_g(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    assert n1 == n2 == 4
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
        group: stats.mean(values[s] for s in SITE_ORDER if GROUP[s] == group)
        for group in ("fragment", "main_forest")
    }
    return [values[s] - means[GROUP[s]] for s in SITE_ORDER]


def main() -> None:
    for path in (VALUES, EFFECTS, COVARIANCE, CONTRACT, STATUS):
        assert path.is_file(), path

    value_rows = rows(VALUES)
    assert len(value_rows) == 8
    assert [r["site"] for r in value_rows] == SITE_ORDER
    assert all(r["independent_unit_note"] == "site_population_is_independent_fragmentation_unit" for r in value_rows)

    adult = {r["site"]: float(r["G_adult_HE"]) for r in value_rows}
    offspring = {r["site"]: float(r["G_offspring_HE"]) for r in value_rows}
    assert adult == {
        "Malava": 0.82, "Kisere": 0.81, "Mukangu": 0.78, "Buyangu": 0.83,
        "Isecheno B": 0.76, "Isecheno A": 0.80, "Ikuywa": 0.82, "Kaimosi": 0.79,
    }
    assert offspring == {
        "Malava": 0.79, "Kisere": 0.79, "Mukangu": 0.73, "Buyangu": 0.80,
        "Isecheno B": 0.71, "Isecheno A": 0.72, "Ikuywa": 0.73, "Kaimosi": 0.76,
    }

    effects = {r["layer"]: r for r in rows(EFFECTS)}
    assert set(effects) == {"G_adult", "G_offspring"}
    computed: dict[str, tuple[float, float]] = {}
    for layer, values in (("G_adult", adult), ("G_offspring", offspring)):
        frag = [values[s] for s in SITE_ORDER if GROUP[s] == "fragment"]
        ref = [values[s] for s in SITE_ORDER if GROUP[s] == "main_forest"]
        g, var = hedges_g(frag, ref)
        row = effects[layer]
        assert row["cluster_id"] == "P2_CF01_GPAIR_003"
        assert row["effect_unit_status"] == "g_admissible"
        assert row["independent_unit"] == "site_population"
        assert int(row["n_fragmented"]) == int(row["n_reference"]) == 4
        assert abs(float(row["fragmented_mean"]) - stats.mean(frag)) < TOL
        assert abs(float(row["fragmented_sd"]) - stats.stdev(frag)) < TOL
        assert abs(float(row["reference_mean"]) - stats.mean(ref)) < TOL
        assert abs(float(row["reference_sd"]) - stats.stdev(ref)) < TOL
        assert abs(float(row["oriented_effect"]) - g) < TOL
        assert abs(float(row["oriented_variance"]) - var) < TOL
        computed[layer] = (g, var)

    rho = pearson(residuals(adult), residuals(offspring))
    va = computed["G_adult"][1]
    vo = computed["G_offspring"][1]
    cov = rho * math.sqrt(va * vo)
    delta = computed["G_adult"][0] - computed["G_offspring"][0]
    dvar = va + vo - 2 * cov
    assert dvar > 0

    cj = json.loads(COVARIANCE.read_text(encoding="utf-8"))
    pair = cj["primary_pair"]
    assert pair["positive_definite"] is True
    assert min(pair["eigenvalues_ascending"]) > 0
    assert abs(pair["residual_correlation"] - rho) < 1e-9
    assert abs(pair["sampling_covariance"] - cov) < 1e-9
    assert abs(pair["effect_difference_Gadult_minus_Goffspring"] - delta) < 1e-9
    assert abs(pair["difference_variance"] - dvar) < 1e-9

    contract = CONTRACT.read_text(encoding="utf-8")
    for token in (
        "retrospective external recovery",
        "Malava, Kisere, Ikuywa, Kaimosi",
        "Mukangu, Buyangu, Isecheno B, Isecheno A",
        "expected heterozygosity `H_E`",
        "site/population",
    ):
        assert token in contract, token

    status = STATUS.read_text(encoding="utf-8")
    for token in (
        "pair-specific covariance-aware Phase-2 cluster",
        "5 independent programmes",
        "5-programme analysis-opening gate is now met",
        "does **not** enter or alter the frozen Phase-1 five-cluster Fisher synthesis",
    ):
        assert token in status, token

    print(
        "PHASE2_CF01_PRUNUS_KAKAMEGA_2008_OK "
        f"Gadult={computed['G_adult'][0]:.8f} "
        f"Goffspring={computed['G_offspring'][0]:.8f} "
        f"delta={delta:.8f} pair_covariance=PD gate=5/5"
    )


if __name__ == "__main__":
    main()
