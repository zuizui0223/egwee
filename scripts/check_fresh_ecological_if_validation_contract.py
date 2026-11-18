from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "manuscript/fresh_ecological_if_validation_contract_v1.json"
PREREG = ROOT / "manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_PREREGISTRATION_2026-09-27.md"
BOTTLENECK_AMENDMENT = ROOT / "manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_AMENDMENT_2026-09-27_BOTTLENECK_LOCALIZATION.md"
SCALE_AMENDMENT = ROOT / "manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_AMENDMENT_2026-09-29_EFFECT_SCALE.md"
FIELD_MODULE = ROOT / "manuscript/FRESH_ECOLOGICAL_IF_SYNCHRONIZED_FIELD_MODULE_V1.md"
CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
MODERATOR_SCHEMA = ROOT / "manuscript/fresh_ecological_if_moderator_schema_v1.csv"


def main() -> None:
    c = json.loads(CONTRACT.read_text(encoding="utf-8"))
    p = PREREG.read_text(encoding="utf-8")
    bottleneck_amendment = BOTTLENECK_AMENDMENT.read_text(encoding="utf-8")
    scale_amendment = SCALE_AMENDMENT.read_text(encoding="utf-8")
    census_text = CENSUS.read_text(encoding="utf-8")
    field = FIELD_MODULE.read_text(encoding="utf-8")
    moderator_text = MODERATOR_SCHEMA.read_text(encoding="utf-8")

    assert c["schema_version"] == 3
    assert c["frozen_on"] == "2026-09-27"
    assert c["discovery_cutoff"] == "2026-09-18"
    assert c["amended_on"] == "2026-09-29"
    assert c["previous_amendment"] == "manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_AMENDMENT_2026-09-27_BOTTLENECK_LOCALIZATION.md"
    assert c["amendment"] == "manuscript/FRESH_ECOLOGICAL_IF_VALIDATION_AMENDMENT_2026-09-29_EFFECT_SCALE.md"
    assert c["effect_family_boundary"]["direct_primary"] == "oriented_lnRR_for_positive_Q_E_F"
    assert c["effect_family_boundary"]["direct_mandatory_sensitivity"] == "Hedges_g_same_independent_units"
    assert c["effect_family_boundary"]["gradient_primary"] == "Fisher_z_or_prespecified_native_model_scale"
    assert c["effect_family_boundary"]["cross_family_pooling"] is False
    assert c["field_module"] == "manuscript/FRESH_ECOLOGICAL_IF_SYNCHRONIZED_FIELD_MODULE_V1.md"
    assert c["current_manuscript_role"] == "scale_sensitive_discovery_synthesis_not_fresh_confirmation"
    assert c["moderator_schema"] == "manuscript/fresh_ecological_if_moderator_schema_v1.csv"

    direct_scale = c["direct_effect_scale"]
    assert direct_scale["primary"] == "oriented_lnRR_for_positive_Q_E_F"
    assert direct_scale["mandatory_sensitivity"] == "Hedges_g_same_independent_units"
    assert direct_scale["outcome_selected_scale_forbidden"] is True
    assert direct_scale["contradictory_direction_blocks_scale_general_bottleneck_claim"] is True

    burned = set(c["burned_programmes"])
    expected = {
        "ML020", "P2_CF01_SEVENELLO_2026", "P2_CF01_BERGSDORF_KAKAMEGA_2006",
        "ML015", "P2_CF01_CARDIOPETALUM_2012", "P2_CF01_ZURICH_2026",
        "P2_CF01_MILKWEED_URBAN_2023", "P2_CF01_PRITCHARD_2005",
    }
    assert burned == expected

    expected_auxiliary = {"ML001", "ML002", "ML014", "P2_CF01_ACER_MIYABEI_2014"}
    assert set(c["burned_auxiliary_process_function_programmes"]) == expected_auxiliary
    for pid in expected:
        assert pid in census_text, pid

    assert c["fresh_gate"]["min_programmes_per_effect_family"] == 5
    assert c["fresh_gate"]["min_programmes_per_categorical_level"] == 4
    assert c["fresh_gate"]["leave_one_programme_out_required"] is True

    h2 = c["h2_v3"]
    assert h2["endpoint_chain"] == ["I_quantity", "I_effective_mating_quality", "F_reproductive"]
    assert h2["primary_direct_contrast"] == "Delta_QE=lnRR_Q-lnRR_E"
    assert h2["primary_direction"] == "Delta_QE>0"
    assert set(h2["secondary_direct_contrasts"]) == {"Delta_QF=lnRR_Q-lnRR_F", "Delta_EF=lnRR_E-lnRR_F"}
    assert h2["hedges_g_sensitivity_required"] is True
    assert h2["scale_general_promotion_requires_noncontradictory_ordering"] is True
    assert h2["leave_one_programme_out_required_after_gate"] is True

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
        "outcome_selected_effect_scale",
        "scale_general_bottleneck_claim_under_contradictory_ordering",
    ):
        assert token in forbidden, token

    for token in ("future-only ecological validation programme", "burned discovery system", "No binomial sign test"):
        assert token in p, token

    for token in ("H2 v2 — effective mating localizes the bottleneck", "Delta_QE = Q - E", "before fresh validation data"):
        assert token in bottleneck_amendment, token

    for token in (
        "before any fresh validation outcome has been opened",
        "primary amplitude estimand = oriented lnRR",
        "mandatory sensitivity = Hedges g",
        "H2-v3 — scale-aware bottleneck localization",
        "Delta_QE = lnRR_Q - lnRR_E",
        "outcome-selected effect scale",
    ):
        assert token in scale_amendment, token

    for token in (
        "I_quantity  →  I_effective / mating quality  →  F_reproductive",
        "Delta_QF = effect(I_quantity) - effect(F)",
        "Delta_QE = effect(I_quantity) - effect(I_effective)",
        "Delta_EF = effect(I_effective) - effect(F)",
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
        "schema=3 burned_IF=8 burned_auxiliary=4 H2v3=scale_aware_Delta_QE_positive "
        "direct_primary=lnRR sensitivity=Hedges_g min_fresh_family=5 cross_family_pooling=false"
    )


if __name__ == "__main__":
    main()
