from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "evidence/meta_extraction/PS020_eucalyptus_socialis_sufficient_stats_v1.json"


def hedges_g_from_summary(
    fragmented_mean: float,
    fragmented_sd: float,
    n_fragmented: int,
    reference_mean: float,
    reference_sd: float,
    n_reference: int,
) -> tuple[float, float]:
    df = n_fragmented + n_reference - 2
    pooled = math.sqrt(
        ((n_fragmented - 1) * fragmented_sd**2 + (n_reference - 1) * reference_sd**2)
        / df
    )
    d = (fragmented_mean - reference_mean) / pooled
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    variance = 1 / n_fragmented + 1 / n_reference + g**2 / (2 * (n_fragmented + n_reference))
    return g, variance


def main() -> None:
    if not SNAPSHOT.is_file():
        raise AssertionError(SNAPSHOT)
    s = json.loads(SNAPSHOT.read_text(encoding="utf-8"))

    assert s["schema_version"] == 1
    assert s["source"]["article_doi"] == "10.1111/mec.12056"
    assert s["source"]["dataset_doi"] == "10.4227/05/54C4E38139B4B"
    assert s["source"]["source_file"] == "MECBreedfamily.csv"
    assert s["source"]["license"] == "CC BY 4.0"

    frame = s["frame"]
    assert frame["n_source_rows"] == 46
    assert frame["groups"] == {"MONLOW": 13, "MONHIGH": 15, "YOOKA": 18}
    assert frame["primary_fragmented"] == "MONLOW"
    assert frame["primary_reference"] == "MONHIGH"
    assert frame["n_fragmented"] == 13
    assert frame["n_reference"] == 15
    assert frame["n_primary_complete_case"] == 28

    hg = s["hedges_g"]
    gm = hg["Gmating_correlated_paternity_rp"]
    ff = hg["F_family_growth"]

    raw_g_rp, var_g = hedges_g_from_summary(
        gm["fragmented_mean"], gm["fragmented_sd"], frame["n_fragmented"],
        gm["reference_mean"], gm["reference_sd"], frame["n_reference"],
    )
    g_support = gm["orientation_multiplier"] * raw_g_rp

    raw_g_f, var_f = hedges_g_from_summary(
        ff["fragmented_mean"], ff["fragmented_sd"], frame["n_fragmented"],
        ff["reference_mean"], ff["reference_sd"], frame["n_reference"],
    )
    g_growth = ff["orientation_multiplier"] * raw_g_f

    assert abs(g_support - gm["oriented_effect"]) < 1e-10
    assert abs(var_g - gm["sampling_variance"]) < 1e-10
    assert abs(g_growth - ff["oriented_effect"]) < 1e-10
    assert abs(var_f - ff["sampling_variance"]) < 1e-10

    dep = hg["dependence"]
    rho = dep["residual_correlation_proxy"]
    cov = rho * math.sqrt(var_g * var_f)
    assert abs(cov - dep["sampling_covariance"]) < 1e-10
    det = var_g * var_f - cov * cov
    assert det > 1e-12

    out = {
        "terminal_state": "ML014_admitted_Gmating_F_covariance_aware",
        "source_snapshot": str(SNAPSHOT.relative_to(ROOT)),
        "source_url": s["source"]["source_url"],
        "source_dataset_doi": s["source"]["dataset_doi"],
        "source_license": s["source"]["license"],
        "source_refresh_required_for_ci": False,
        "n_source_family_rows": frame["n_source_rows"],
        "n_common": frame["n_primary_complete_case"],
        "n_fragmented": frame["n_fragmented"],
        "n_reference": frame["n_reference"],
        "G_mating_rp": {
            "raw_hedges_g_fragmented_minus_reference": raw_g_rp,
            "orientation_multiplier": gm["orientation_multiplier"],
            "oriented_support_g": g_support,
            "variance": var_g,
            "fragmented_mean_rp": gm["fragmented_mean"],
            "reference_mean_rp": gm["reference_mean"],
            "fragmented_sd_rp": gm["fragmented_sd"],
            "reference_sd_rp": gm["reference_sd"],
        },
        "F_growth": {
            "hedges_g": g_growth,
            "variance": var_f,
            "fragmented_mean": ff["fragmented_mean"],
            "reference_mean": ff["reference_mean"],
            "fragmented_sd": ff["fragmented_sd"],
            "reference_sd": ff["reference_sd"],
        },
        "within_cluster": {
            "residual_correlation_proxy": rho,
            "sampling_covariance": cov,
            "determinant": det,
            "positive_definite": True,
            "snapshot_method": dep["proxy_method"],
        },
    }
    print("SOCIALIS_ML014_RESULT " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
