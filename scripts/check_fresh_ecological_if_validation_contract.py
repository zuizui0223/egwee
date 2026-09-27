from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "manuscript/fresh_ecological_if_validation_contract_v1.json"
PREREG = ROOT / "manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_PREREGISTRATION_2026-09-27.md"
AMENDMENT = ROOT / "manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_AMENDMENT_2026-09-27_BOTTLENECK_LOCALIZATION.md"
FIELD_MODULE = ROOT / "manuscript/FRESH_ECOLOGICAL_IF_SYNCHRONIZED_FIELD_MODULE_V1.md"
CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
MODERATOR_SCHEMA = ROOT / "manuscript/fresh_ecological_if_moderator_schema_v1.csv"


def main() -> None:
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))
    p = PREREG.read_text(encoding="utf-8")
    amendment = AMENDMENT.read_text(encoding="utf-8")
    census_text = CENSUS.read_text(encoding="utf-8")
    field = FIELD_MODULE.read_text(encoding="utf-8")
    moderator_text = MODERATOR_SCHEMA.read_text(encoding="utf-8")

    assert c["schema_version"] == 2
    assert c["frozen_on"] == "2026-09-27"
    assert c["discovery_cutoff"] == "2026-09-18"
    assert c["amended_on"] == "2026-09-27"
    assert c["amendment"] == "manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_AMENDMENT_2026-09-27_BOTTLENECK_LOCALIZATION.md"
    assert c["effect_family_boundary"]["cross_family_pooling"] is False
    assert c["field_module"] == "manuscript/FRESH_ECOLOGICAL_IF_SYNCHRONIZED_FIELD_MODULE_V1.md"
    assert c["current_manuscript_role"] == "discovery_synthesis_not_fresh_confirmation"
    assert c["moderator_schema"] == "manuscript/fresh_ecological_if_moderator_schema_v1.csv"
    assert "Delta_QF=Q-F" in c["primary_estimand"]
    assert "Delta_QE=Q-E" in c["primary_estimand"]
    assert "Delta_EF=E-F" in c["primary_estimand"]

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

    expected_auxiliary = {
        "ML001",
        "ML002",
        "ML014",
        "P2_CF01_ACER_MIYABEI_2014",
    }
    assert set(c["burned_auxiliary_process_function_programmes"]) == expected_auxiliary
    assert c["auxiliary_discovery_audit"] == "manuscript/ECOLOGICAL_BOTTLENECK_POSITION_AUDIT_2026-09-27.md"

    for pid in expected:
        assert pid in census_text, pid

    assert c["fresh_gate"]["min_programmes_per_effect_family"] == 5
    assert c["fresh_gate"]["min_programmes_per_categorical_level"] == 4
    assert c["fresh_gate"]["leave_one_programme_out_required"] is True

    h2 = c["h2_v2"]
    assert h2["endpoint_chain"] == ["I_quantity", "I_effective_mating_quality", "F_reproductive"]
    assert h2["primary_contrast"] == "Delta_QE=Q-E"
    assert h2["primary_direction"] == "Delta_QE>0"
    assert h2["min_fresh_QEF_programmes_per_effect_family"] == 5
    assert set(h2["secondary_contrasts"]) == {"Delta_QF=Q-F", "Delta_EF=E-F"}
    assert set(h2["regimes"]) == {"B1", "B2", "B3", "B4"}

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
        "reuse_burned_auxiliary_process_function_programmes_as_fresh_H2_confirmation",
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
        "burned as auxiliary evidence for H2",
        "after 2026-09-18",
        "effect families are never pooled numerically",
        "No binomial sign test",
        "not required to complete or submit",
        "bottleneck-localization H2",
    ):
        assert token in p, token

    for token in (
        "H2 v2 — effective mating localizes the bottleneck",
        "Delta_QE = Q - E",
        "Delta_QE > 0",
        "B2 — mating bottleneck with downstream compensation",
        "before fresh validation data",
    ):
        assert token in amendment, token

    for token in (
        "I_quantity  →  I_effective / mating quality  →  F_reproductive",
        "Delta_QF = effect(I_quantity) - effect(F)",
        "Delta_QE = effect(I_quantity) - effect(I_effective)",
        "Delta_EF = effect(I_effective) - effect(F)",
        "localizes the bottleneck rather than requiring exact recoupling",
        "pollen supplementation or cross-pollination partially rescues F",
        "plants/flowers/fruits/offspring to independent fragmentation units",
    ):
        assert token in field, token

    for token in (
        "interaction_measurement_class",
        "quantity_only;effective_mating_quality;unknown",
        "self-compatibility alone is not assurance",
        "do not infer from low fruit set or high inbreeding",
        "do not define direct quality from association with F",
    ):
        assert token in moderator_text, token

    print(
        "FRESH_ECOLOGICAL_IF_VALIDATION_CONTRACT_OK "
        "burned_IF=8 burned_auxiliary=4 H2v2=Delta_QE_positive "
        "min_fresh_family=5 min_level=4 cross_family_pooling=false"
    )


if __name__ == "__main__":
    main()
