from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPOLOGY = ROOT / "evidence/meta_extraction/transition_filtering_topology_v1.csv"
GPAIR = ROOT / "evidence/meta_extraction/phase2_gpair_synthesis_v1.json"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    topo = rows(TOPOLOGY)
    gpair = json.loads(GPAIR.read_text(encoding="utf-8"))

    interaction = [r for r in topo if r["transition_class"] == "interaction_quantity_to_F"]
    mating = [r for r in topo if r["transition_class"] == "movement_mating_to_F"]
    cohort = [r for r in topo if r["transition_class"] == "adult_to_offspring_G"]

    assert len(interaction) == 3
    assert {r["programme_id"] for r in interaction} == {
        "ML015",
        "P2_CF01_CARDIOPETALUM_2012",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
    }
    assert all(r["representation_1_order"] == "F_more_negative" for r in interaction)
    assert all(r["representation_2_order"] == "F_more_negative" for r in interaction)
    assert all(r["inference_status"] == "stable_resolved" for r in interaction)

    assert len(mating) == 3
    assert {r["programme_id"] for r in mating} == {"ML001", "ML002", "ML014"}
    assert all(r["representation_1_order"] == "process_more_negative" for r in mating)
    assert all(r["representation_2_order"] == "process_more_negative" for r in mating)
    assert all("scale_sensitive_resolution" in r["inference_status"] for r in mating)

    assert len(cohort) == 1
    assert cohort[0]["programme_id"] == "ML003"
    assert cohort[0]["representation_1_order"] == "offspring_more_negative"
    assert cohort[0]["representation_2_order"] == "offspring_more_negative"

    assert gpair["n_independent_programmes"] == 5
    re = gpair["primary_random_effects"]
    assert abs(re["pooled_mean"] - 0.128524493173) < 1e-12
    assert re["ci95_mKH"][0] < 0 < re["ci95_mKH"][1]
    assert abs(re["p_two_sided_t"] - 0.672436401972) < 1e-12
    contrasts = [
        row["programme_contrast"]
        for row in gpair["leave_one_programme_out"]
    ]
    assert min(contrasts) < 0 < max(contrasts)

    print(
        "TRANSITION_FILTERING_AUDIT_OK "
        "interaction_to_F_stable_downstream=3 "
        "movement_mating_to_F_cross_scale_point_attenuation=3 "
        "adult_offspring_programmes=5 common_lag=false"
    )


if __name__ == "__main__":
    main()
