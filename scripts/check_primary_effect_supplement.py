from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "manuscript/tables/table_s3_primary_marginal_effects.csv"


def rows(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def expected_rows() -> list[dict[str, object]]:
    out: list[dict[str, object]] = []

    ser = [r for r in rows("evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv") if r["primary_or_sensitivity"] == "primary"]
    ser_map = {
        "pollen_immigration_rate": ("C", "pollen immigration rate"),
        "fruit_set": ("F", "fruit set"),
        "observed_heterozygosity": ("G_adult", "observed heterozygosity"),
    }
    for r in ser:
        layer, endpoint = ser_map[r["endpoint"]]
        out.append({
            "cluster_id": "ML001", "system_or_subsystem": "Serapias lingua", "layer": layer,
            "endpoint": endpoint, "fragmentation_contrast": "predefined anthropic populations vs natural populations",
            "independent_unit": "population", "n_fragmented": 3, "n_reference": 6,
            "hedges_g": float(r["oriented_effect"]), "sampling_variance": float(r["oriented_variance"]),
        })

    bros = [r for r in rows("evidence/meta_extraction/PS004_brosimum_extraction_v1.csv") if r["effect_unit_status"] == "g_admissible"]
    bros_map = {
        "C_paternity_rp": ("C", "multilocus correlated paternity support"),
        "F_progeny_vigour": ("F", "one-year total dry mass"),
    }
    for r in bros:
        layer, endpoint = bros_map[r["endpoint_id"]]
        out.append({
            "cluster_id": "ML002", "system_or_subsystem": "Brosimum alicastrum", "layer": layer,
            "endpoint": endpoint, "fragmentation_contrast": "fragmented forest vs continuous forest",
            "independent_unit": "site/population", "n_fragmented": 3, "n_reference": 3,
            "hedges_g": float(r["oriented_effect"]), "sampling_variance": float(r["oriented_variance"]),
        })

    spon = [r for r in rows("evidence/meta_extraction/PS001_spondias_site_effects_v1.csv") if r["analysis_role"] == "primary"]
    spon_map = {
        "C_paternity_correlation": ("C", "multilocus correlated paternity support"),
        "Gadult_Ho": ("G_adult", "adult observed heterozygosity"),
        "Gjuvenile_Ho": ("G_offspring", "juvenile observed heterozygosity"),
        "Gseed_Ho": ("G_offspring", "seed observed heterozygosity"),
    }
    for r in spon:
        layer, endpoint = spon_map[r["endpoint_id"]]
        out.append({
            "cluster_id": "ML003", "system_or_subsystem": "Spondias purpurea", "layer": layer,
            "endpoint": endpoint, "fragmentation_contrast": "fragmented forest vs continuous forest",
            "independent_unit": "site", "n_fragmented": 3, "n_reference": 2,
            "hedges_g": float(r["oriented_effect"]), "sampling_variance": float(r["oriented_variance"]),
        })

    soc = rows("evidence/meta_extraction/PS020_eucalyptus_socialis_effects_v1.csv")
    soc_map = {
        "Gmating_correlated_paternity_rp": ("G_mating", "family multilocus correlated paternity support"),
        "F_family_growth": ("F", "family mean progeny height"),
    }
    for r in soc:
        layer, endpoint = soc_map[r["endpoint_id"]]
        out.append({
            "cluster_id": "ML014", "system_or_subsystem": "Eucalyptus socialis", "layer": layer,
            "endpoint": endpoint,
            "fragmentation_contrast": "MONLOW isolated-pasture fragments vs MONHIGH small-remnant reference",
            "independent_unit": "maternal family", "n_fragmented": 13, "n_reference": 15,
            "hedges_g": float(r["oriented_effect"]), "sampling_variance": float(r["oriented_variance"]),
        })

    for r in rows("evidence/meta_extraction/PS022_aizen_feinsinger_effects_v1.csv"):
        endpoint_map = {
            "I_pollen_tubes": ("I", "pollen tubes"),
            "F_fruit_set": ("F", "fruit set"),
        }
        layer, endpoint = endpoint_map[r["endpoint_id"]]
        out.append({
            "cluster_id": "ML020", "system_or_subsystem": r["species"], "layer": layer,
            "endpoint": endpoint, "fragmentation_contrast": "small forest fragment vs continuous forest",
            "independent_unit": "site-specific habitat unit", "n_fragmented": 4, "n_reference": 4,
            "hedges_g": float(r["oriented_effect"]), "sampling_variance": float(r["sampling_variance"]),
        })

    order = {"ML001": 0, "ML002": 1, "ML003": 2, "ML014": 3, "ML020": 4}
    out.sort(key=lambda r: (order[str(r["cluster_id"])], str(r["system_or_subsystem"]), str(r["layer"]), str(r["endpoint"])))
    return out


def main() -> None:
    expected = expected_rows()
    with TABLE.open(newline="", encoding="utf-8") as fh:
        actual = list(csv.DictReader(fh))
    assert len(expected) == 17
    assert len(actual) == 17

    def key(r: dict[str, object]) -> tuple[str, str, str, str]:
        return tuple(str(r[k]) for k in ("cluster_id", "system_or_subsystem", "layer", "endpoint"))  # type: ignore[return-value]

    exp = {key(r): r for r in expected}
    act = {key(r): r for r in actual}
    assert set(exp) == set(act)

    for k, e in exp.items():
        a = act[k]
        for field in ("fragmentation_contrast", "independent_unit"):
            assert str(a[field]) == str(e[field]), (k, field, a[field], e[field])
        for field in ("n_fragmented", "n_reference"):
            assert int(a[field]) == int(e[field]), (k, field)
        g = float(e["hedges_g"])
        v = float(e["sampling_variance"])
        se = math.sqrt(v)
        lo = g - 1.96 * se
        hi = g + 1.96 * se
        targets = {
            "hedges_g": g,
            "sampling_variance": v,
            "se": se,
            "ci95_lower": lo,
            "ci95_upper": hi,
        }
        for field, target in targets.items():
            assert abs(float(a[field]) - target) < 5e-12, (k, field, a[field], target)

    # Transparent checks for the influential extreme standardized effects.
    ser = [r for r in actual if r["cluster_id"] == "ML001"]
    assert len(ser) == 3
    assert min(float(r["hedges_g"]) for r in ser) < -25
    assert all(float(r["ci95_upper"]) < 0 for r in ser)

    print("PRIMARY_EFFECT_SUPPLEMENT_OK rows=17 clusters=5")


if __name__ == "__main__":
    main()
