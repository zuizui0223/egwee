from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "evidence/meta_extraction/cross_system_cf_pilot_v1.csv"
SERA_EFFECTS = ROOT / "evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv"
SERA_COV = ROOT / "evidence/meta_extraction/PS003_serapias_primary_covariance_v1.csv"
BROS_EFFECTS = ROOT / "evidence/meta_extraction/PS004_brosimum_extraction_v1.csv"
BROS_COV = ROOT / "evidence/meta_extraction/PS004_brosimum_primary_covariance_v1.csv"

Z95 = 1.959963984540054


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def covariance(path: Path, a: str, b: str) -> float:
    row = next(r for r in rows(path) if r["endpoint_i"] == a and r["endpoint_j"] == b)
    return float(row["sampling_covariance"])


def expected_inputs() -> dict[str, dict[str, float | str]]:
    sera = rows(SERA_EFFECTS)
    s_c = next(r for r in sera if r["endpoint"] == "pollen_immigration_rate" and r["primary_or_sensitivity"] == "primary")
    s_f = next(r for r in sera if r["endpoint"] == "fruit_set" and r["primary_or_sensitivity"] == "primary")

    bros = rows(BROS_EFFECTS)
    b_c = next(r for r in bros if r["endpoint_id"] == "C_paternity_rp")
    b_f = next(r for r in bros if r["endpoint_id"] == "F_progeny_vigour")

    return {
        "ML001": {
            "study_id": "PS003",
            "species": "Serapias lingua",
            "C": float(s_c["oriented_effect"]),
            "F": float(s_f["oriented_effect"]),
            "vC": float(s_c["oriented_variance"]),
            "vF": float(s_f["oriented_variance"]),
            "cov": covariance(SERA_COV, "C_pollen_immigration", "F_fruit_set"),
        },
        "ML002": {
            "study_id": "PS004",
            "species": "Brosimum alicastrum",
            "C": float(b_c["oriented_effect"]),
            "F": float(b_f["oriented_effect"]),
            "vC": float(b_c["oriented_variance"]),
            "vF": float(b_f["oriented_variance"]),
            "cov": covariance(BROS_COV, "C_paternity_rp", "F_TPDW"),
        },
    }


def main() -> None:
    for path in (PILOT, SERA_EFFECTS, SERA_COV, BROS_EFFECTS, BROS_COV):
        assert path.is_file(), path

    pilot = rows(PILOT)
    assert len(pilot) == 2
    by_cluster = {r["cluster_id"]: r for r in pilot}
    inputs = expected_inputs()
    assert set(by_cluster) == set(inputs) == {"ML001", "ML002"}

    deltas: list[float] = []
    delta_vars: list[float] = []
    for cluster_id, source in inputs.items():
        row = by_cluster[cluster_id]
        c = float(source["C"])
        f = float(source["F"])
        vc = float(source["vC"])
        vf = float(source["vF"])
        cov = float(source["cov"])
        delta = f - c
        variance = vf + vc - 2 * cov
        assert variance > 0
        se = math.sqrt(variance)
        lo = delta - Z95 * se
        hi = delta + Z95 * se

        assert row["study_id"] == source["study_id"]
        assert row["species"] == source["species"]
        for observed, expected in (
            (float(row["C_effect"]), c),
            (float(row["F_effect"]), f),
            (float(row["C_variance"]), vc),
            (float(row["F_variance"]), vf),
            (float(row["C_F_covariance"]), cov),
            (float(row["delta_F_minus_C"]), delta),
            (float(row["delta_variance"]), variance),
            (float(row["delta_se"]), se),
            (float(row["delta_ci95_low"]), lo),
            (float(row["delta_ci95_high"]), hi),
        ):
            assert abs(observed - expected) < 1e-9, (cluster_id, observed, expected)

        assert row["C_negative"] == str(c < 0).lower()
        assert row["F_negative"] == str(f < 0).lower()
        assert row["within_cluster_direction_concordant"] == str(c < 0 and f < 0).lower()
        assert row["C_more_negative_than_F"] == str(c < f).lower()
        deltas.append(delta)
        delta_vars.append(variance)

    # Fixed-effect pooling is diagnostic only: k=2 is below the claim threshold.
    weights = [1 / variance for variance in delta_vars]
    pooled = sum(w * delta for w, delta in zip(weights, deltas)) / sum(weights)
    pooled_var = 1 / sum(weights)
    pooled_se = math.sqrt(pooled_var)
    pooled_lo = pooled - Z95 * pooled_se
    pooled_hi = pooled + Z95 * pooled_se
    q = sum(w * (delta - pooled) ** 2 for w, delta in zip(weights, deltas))
    i2_descriptive = max(0.0, (q - 1) / q) if q > 0 else 0.0

    assert abs(pooled - 1.631458064043) < 1e-9
    assert abs(pooled_var - 0.563271773357) < 1e-9
    assert abs(q - 4.146829046699) < 1e-9
    assert all(float(r["C_effect"]) < 0 and float(r["F_effect"]) < 0 for r in pilot)
    assert all(float(r["C_effect"]) < float(r["F_effect"]) for r in pilot)

    print(
        "EGWEE C-F cross-system pilot: PASS; "
        "2/2 independent clusters have C<0 and F<0; "
        "2/2 have C more negative than F; "
        f"covariance-aware fixed-effect diagnostic delta(F-C)={pooled:.6f} "
        f"95%CI=[{pooled_lo:.6f},{pooled_hi:.6f}], Q(df=1)={q:.6f}, "
        f"descriptive I2={100*i2_descriptive:.1f}%; k=2 => no broad generalization"
    )


if __name__ == "__main__":
    main()
