from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TRANSLATION = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"
PROXY = ROOT / "evidence/meta_extraction/scale_stable_quantity_function_proxy_failure_v1.csv"
TRANSITION = ROOT / "evidence/meta_extraction/transition_filtering_topology_v1.csv"
IF_CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
HIDDEN = ROOT / "evidence/meta_extraction/hidden_effective_mating_mechanism_context_v1.csv"
GPAIR = ROOT / "evidence/meta_extraction/phase2_gpair_synthesis_v1.json"
GENERALITY = ROOT / "manuscript/ECOLOGICAL_GENERALITY_AND_SURPRISE_2026-09-29.md"
HIDDEN_NOTE = ROOT / "manuscript/HIDDEN_EFFECTIVE_MATING_LAYER_HYPOTHESIS_2026-10-03.md"
TRANSLATION_NOTE = ROOT / "manuscript/IF_TRANSLATION_NONIDENTIFIABILITY_2026-10-03.md"
SENTINEL_NOTE = ROOT / "manuscript/FRAGMENTATION_SENTINEL_SUFFICIENCY_2026-10-03.md"
INFLUENCE = ROOT / "scripts/check_if_translation_influence.py"
LOGIC_NOTE = ROOT / "manuscript/INTERACTION_DECLINE_NECESSITY_SUFFICIENCY_2026-10-03.md"
LOGIC_CHECKER = ROOT / "scripts/check_interaction_decline_necessity_sufficiency.py"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    translation = rows(TRANSLATION)
    proxy = rows(PROXY)
    transition = rows(TRANSITION)
    ifc = rows(IF_CENSUS)
    hidden = rows(HIDDEN)
    gpair = json.loads(GPAIR.read_text(encoding="utf-8"))
    generality = GENERALITY.read_text(encoding="utf-8")
    hidden_note = HIDDEN_NOTE.read_text(encoding="utf-8")
    translation_note = TRANSLATION_NOTE.read_text(encoding="utf-8")
    sentinel_note = SENTINEL_NOTE.read_text(encoding="utf-8")
    influence = INFLUENCE.read_text(encoding="utf-8")
    logic_note = LOGIC_NOTE.read_text(encoding="utf-8")
    logic_checker = LOGIC_CHECKER.read_text(encoding="utf-8")

    # Frozen 16-programme translation universe.
    assert len(translation) == 16
    assert sum(r["evidence_tier"] == "quantitative" for r in translation) == 8
    assert sum(r["evidence_tier"] == "qualitative" for r in translation) == 8

    lower_F = {
        r["function_signal"] for r in translation
        if r["interaction_signal"] == "lower"
    }
    no_loss_F = {
        r["function_signal"] for r in translation
        if r["interaction_signal"] == "no_detected_loss"
    }
    higher_F = {
        r["function_signal"] for r in translation
        if r["interaction_signal"] == "higher"
    }
    assert {"lower", "higher", "no_detected_loss"} <= lower_F
    assert {"lower", "no_detected_loss"} <= no_loss_F
    assert {"lower", "similar"} <= higher_F

    # Representation-stable downstream false-reassurance anchors.
    assert {r["programme_id"] for r in proxy} == {
        "ML015",
        "P2_CF01_CARDIOPETALUM_2012",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
    }
    assert len({r["region"] for r in proxy}) == 3
    assert len({r["plant_family"] for r in proxy}) == 3

    # Current quantitative I-F measurement gap.
    assert len(ifc) == 8
    assert {r["interaction_measurement_class"] for r in ifc} == {"quantity_only"}

    # Transition-filtering topology remains exploratory.
    interaction = [r for r in transition if r["transition_class"] == "interaction_quantity_to_F"]
    mating = [r for r in transition if r["transition_class"] == "movement_mating_to_F"]
    cohort = [r for r in transition if r["transition_class"] == "adult_to_offspring_G"]
    assert len(interaction) == 3
    assert all(r["representation_1_order"] == "F_more_negative" for r in interaction)
    assert all(r["representation_2_order"] == "F_more_negative" for r in interaction)
    assert len(mating) == 3
    assert all(r["representation_1_order"] == "process_more_negative" for r in mating)
    assert all(r["representation_2_order"] == "process_more_negative" for r in mating)
    assert len(cohort) == 1 and cohort[0]["programme_id"] == "ML003"

    re = gpair["primary_random_effects"]
    assert gpair["n_independent_programmes"] == 5
    assert re["ci95_mKH"][0] < 0 < re["ci95_mKH"][1]
    assert re["p_two_sided_t"] > 0.05

    # External mechanism context is triangulation only.
    assert len(hidden) == 5
    assert sum(r["evidence_role"] == "external_context" for r in hidden) == 4
    assert sum(r["evidence_role"] == "internal_anchor" for r in hidden) == 1
    assert {r["system"] for r in hidden if r["evidence_role"] == "external_context"} == {
        "Dianella revoluta",
        "Linnaea borealis",
        "Heliconia tortuosa",
        "Conospermum undulatum",
    }

    # Canonical generality wording.
    for token in (
        "directional coherence at coarse scale but no one-to-one interaction→function translation",
        "False reassurance",
        "False alarm / apparent over-warning",
        "Hidden effective-mating layer hypothesis",
        "0/8 programmes",
    ):
        assert token in generality, token

    for token in (
        "Mechanistic triangulation / hypothesis-generating context",
        "interaction quantity  →  effective mating quality  →  reproductive function",
        "outcome-selected effect scale",
        "not established by the current corpus",
    ):
        assert token in hidden_note, token

    for token in (
        "at least two interaction evidence states that map to multiple reproductive-function states",
        "quantitative-only tier is weaker",
        "three representation-stable quantitative false-reassurance anchors",
    ):
        assert token in translation_note, token

    for token in (
        "survives deletion of every single programme",
        "mixed quantitative + source-explicit qualitative evidence map",
        "category-level ambiguity depends on the unresolved common-milkweed point estimate",
    ):
        assert token in sentinel_note, token

    assert 'assert len(amb) >= 2' in influence
    assert 'quantitative_ambiguity_without_milkweed=0' in influence
    assert "neither necessary nor sufficient" in logic_note
    assert "necessity_counterexamples=2" in logic_checker
    assert "sufficiency_counterexamples=3" in logic_checker

    print(
        "ECOLOGICAL_GENERALITY_OK "
        "translation_programmes=16 quantitative=8 qualitative=8 "
        "same_I_signal_multiple_F_states=true "
        "stable_false_reassurance=3 continents=3 families=3 "
        "effective_mating_measured=0_of_8 "
        "movement_mating_point_order=3 adult_offspring_common_lag=false "
        "hidden_mating_mechanism_external_context=4 "
        "interaction_decline_neither_necessary_nor_sufficient=true prevalence_inference=false"
    )


if __name__ == "__main__":
    main()
