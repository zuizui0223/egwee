from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "manuscript/fresh_ecological_if_validation_contract_v1.json"
PREREG = ROOT / "manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_PREREGISTRATION_2026-09-27.md"
CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"


def main() -> None:
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))
    p = PREREG.read_text(encoding="utf-8")
    census_text = CENSUS.read_text(encoding="utf-8")

    assert c["schema_version"] == 1
    assert c["frozen_on"] == "2026-09-27"
    assert c["discovery_cutoff"] == "2026-09-18"
    assert c["effect_family_boundary"]["cross_family_pooling"] is False
    assert c["primary_estimand"].startswith("Delta_IF=")

    burned = set(c["burned_programmes"])
    expected = {
        "ML020",
        "P2_CF01_SEVENELLO_2026",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "ML015",
        "P2_CF01_CARDIOPETALUM_2012",
        "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023",
        "P2_CF01_PRITCHARD_2005",
    }
    assert burned == expected

    for pid in expected:
        assert pid in census_text, pid

    assert c["fresh_gate"]["min_programmes_per_effect_family"] == 5
    assert c["fresh_gate"]["min_programmes_per_categorical_level"] == 4
    assert c["fresh_gate"]["leave_one_programme_out_required"] is True

    assert set(c["primary_moderators"]) == {
        "interaction_measurement_class",
        "autonomous_reproductive_assurance",
        "outcrossing_dependence",
        "pollination_specialisation",
        "fragmentation_component",
    }

    forbidden = set(c["forbidden"])
    for token in (
        "reuse_burned_programmes_as_fresh_confirmation",
        "outcome_based_moderator_coding",
        "self_compatibility_as_assurance_without_measurement",
        "cross_family_delta_pooling",
        "endpoint_switch_after_outcome",
        "search_until_significance",
        "unresolved_as_zero",
    ):
        assert token in forbidden

    for token in (
        "future-only ecological validation programme",
        "burned discovery system",
        "This 3/3 direction is **motivation only**",
        "after 2026-09-18",
        "effect families are never pooled numerically",
        "No binomial sign test",
        "not required to complete or submit",
    ):
        assert token in p, token

    print(
        "FRESH_ECOLOGICAL_IF_VALIDATION_CONTRACT_OK "
        "burned=8 min_fresh_family=5 min_level=4 cross_family_pooling=false"
    )


if __name__ == "__main__":
    main()
