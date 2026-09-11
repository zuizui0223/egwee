from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "evidence/meta_extraction/PS002_magnolia_extraction_v1.csv"


def main() -> None:
    with PATH.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    assert len(rows) == 6
    by_id = {r["endpoint_id"]: r for r in rows}
    expected = {
        "F_population_size": 0.00055,
        "F_neighbor_population_size": 0.00013,
        "F_local_density": -0.00056,
        "R_selfing_local_density": -0.00534,
        "C_between_population_pollen_flow": 0.0609,
        "C_population_separation_male_success": -0.575,
    }
    for endpoint, value in expected.items():
        assert endpoint in by_id
        assert abs(float(by_id[endpoint]["raw_effect"]) - value) < 1e-12

    assert by_id["F_population_size"]["effect_unit_status"] == "model_contrast_pending_standardisation"
    assert by_id["F_neighbor_population_size"]["effect_unit_status"] == "model_contrast_pending_standardisation"
    assert by_id["C_population_separation_male_success"]["effect_unit_status"] == "model_contrast_pending_standardisation"
    assert by_id["R_selfing_local_density"]["effect_unit_status"] == "descriptive_only"
    assert not any(r["effect_unit_status"] in {"g_admissible", "fisher_z_admissible"} for r in rows)
    assert all(r["oriented_effect"] == "NA" for r in rows)

    print("PS002 Magnolia extraction: PASS; native model scales preserved, 0 fabricated standardized effects")


if __name__ == "__main__":
    main()
