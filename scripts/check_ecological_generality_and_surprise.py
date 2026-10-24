from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TRANSLATION = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"
PROXY = ROOT / "evidence/meta_extraction/scale_stable_quantity_function_proxy_failure_v1.csv"
RELIABILITY = ROOT / "evidence/meta_extraction/if_reliability_sufficiency_v1.csv"
METRICS = ROOT / "evidence/meta_extraction/if_interaction_metric_class_v1.csv"
SCALE = ROOT / "evidence/meta_extraction/estimand_scale_robustness_v1.csv"
TRANSITION = ROOT / "evidence/meta_extraction/transition_filtering_topology_v1.csv"
IF_CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
HIDDEN = ROOT / "evidence/meta_extraction/hidden_effective_mating_mechanism_context_v1.csv"
GPAIR = ROOT / "evidence/meta_extraction/phase2_gpair_synthesis_v1.json"

GENERALITY = ROOT / "manuscript/ECOLOGICAL_GENERALITY_AND_SURPRISE_2026-09-29.md"
HIDDEN_NOTE = ROOT / "manuscript/HIDDEN_EFFECTIVE_MATING_LAYER_HYPOTHESIS_2026-10-03.md"
TRANSLATION_NOTE = ROOT / "manuscript/IF_TRANSLATION_NONIDENTIFIABILITY_2026-10-03.md"
SENTINEL_NOTE = ROOT / "manuscript/FRAGMENTATION_SENTINEL_SUFFICIENCY_2026-10-03.md"
DETERMINISM_NOTE = ROOT / "manuscript/IF_SENTINEL_DETERMINISM_2026-10-05.md"
LOGIC_NOTE = ROOT / "manuscript/INTERACTION_DECLINE_NECESSITY_SUFFICIENCY_2026-10-03.md"
RELIABILITY_NOTE = ROOT / "manuscript/IF_RELIABILITY_SUFFICIENCY_2026-10-06.md"

PROMOTION = ROOT / "evidence/meta_extraction/ecological_generality_surprise_promotion_v1.json"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def normalize_i(value: str) -> str:
    if value in {"higher", "higher_or_shifted"}:
        return "higher"
    return value


def normalize_f(value: str) -> str:
    if value in {"similar", "no_detected_loss"}:
        return "similar_or_no_detected_loss"
    return value


def image_sets(data: list[dict[str, str]]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for r in data:
        out.setdefault(normalize_i(r["interaction_signal"]), set()).add(
            normalize_f(r["function_signal"])
        )
    return out


def ambiguous_inputs(data: list[dict[str, str]]) -> set[str]:
    return {i for i, vals in image_sets(data).items() if len(vals) >= 2}


def strict_rows(data: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        r for r in data
        if r["interaction_signal"] not in {"no_detected_loss", "mixed"}
        and r["function_signal"] not in {"no_detected_loss", "mixed"}
    ]


def deterministic_error(data: list[dict[str, str]]) -> int:
    by_i: dict[str, list[str]] = defaultdict(list)
    for r in data:
        by_i[normalize_i(r["interaction_signal"])].append(normalize_f(r["function_signal"]))
    errors = 0
    for vals in by_i.values():
        counts = Counter(vals)
        errors += len(vals) - max(counts.values())
    return errors


def main() -> None:
    translation = rows(TRANSLATION)
    proxy = rows(PROXY)
    reliability = rows(RELIABILITY)
    metrics = rows(METRICS)
    scale = rows(SCALE)
    transition = rows(TRANSITION)
    ifc = rows(IF_CENSUS)
    hidden = rows(HIDDEN)
    gpair = json.loads(GPAIR.read_text(encoding="utf-8"))
    promotion = json.loads(PROMOTION.read_text(encoding="utf-8"))

    generality = GENERALITY.read_text(encoding="utf-8")
    hidden_note = HIDDEN_NOTE.read_text(encoding="utf-8")
    translation_note = TRANSLATION_NOTE.read_text(encoding="utf-8")
    sentinel_note = SENTINEL_NOTE.read_text(encoding="utf-8")
    determinism_note = DETERMINISM_NOTE.read_text(encoding="utf-8")
    logic_note = LOGIC_NOTE.read_text(encoding="utf-8")
    reliability_note = RELIABILITY_NOTE.read_text(encoding="utf-8")

    # 1. Scale-stable directional coherence.
    assert len(scale) >= 15
    g_rows = [r for r in scale if r["scale"] == "hedges_g"]
    l_rows = [r for r in scale if r["scale"] == "lnRR" and r["covariance_mode"] == "delta_raw_unit_covariance"]
    assert len(g_rows) == len(l_rows) == 5
    assert {int(r["n_primary_effects"]) for r in g_rows + l_rows} == {17}
    assert {int(r["negative_effects"]) for r in g_rows + l_rows} == {17}
    assert {int(r["discordant_signs"]) for r in g_rows + l_rows} == {0}

    # 2. Frozen 16-programme translation universe is many-to-many.
    assert len(translation) == 16
    assert sum(r["evidence_tier"] == "quantitative" for r in translation) == 8
    assert sum(r["evidence_tier"] == "qualitative" for r in translation) == 8
    full_amb = ambiguous_inputs(translation)
    assert {"lower", "no_detected_loss", "higher"} <= full_amb

    # Full map remains non-identifying under every single deletion.
    for drop in {r["programme_id"] for r in translation}:
        subset = [r for r in translation if r["programme_id"] != drop]
        assert len(ambiguous_inputs(subset)) >= 2, drop

    # 3. Conservative category sensitivity.
    strict = strict_rows(translation)
    assert len(strict) == 8
    assert ambiguous_inputs(strict) == {"lower", "higher"}
    for drop in {r["programme_id"] for r in strict}:
        subset = [r for r in strict if r["programme_id"] != drop]
        assert ambiguous_inputs(subset), drop

    # 4. Interaction-metric sensitivity: visitation/abundance only.
    metric_by = {r["programme_id"]: r for r in metrics}
    assert len(metric_by) == 16
    visit_ids = {
        pid for pid, r in metric_by.items()
        if r["interaction_metric_class"] == "visitation_abundance"
    }
    assert len(visit_ids) == 13
    visit = [r for r in translation if r["programme_id"] in visit_ids]
    assert len(visit) == 13
    assert {"lower", "no_detected_loss"} <= ambiguous_inputs(visit)
    for drop in visit_ids:
        subset = [r for r in visit if r["programme_id"] != drop]
        assert ambiguous_inputs(subset), drop

    # 5. No deterministic interaction-only sentinel fits the observed map.
    assert deterministic_error(translation) == 5
    assert deterministic_error(strict) == 2
    strict_q = [r for r in strict if r["evidence_tier"] == "quantitative"]
    assert len(strict_q) == 5
    assert deterministic_error(strict_q) == 1
    assert min(
        deterministic_error([r for r in translation if r["programme_id"] != drop])
        for drop in {r["programme_id"] for r in translation}
    ) >= 4
    assert min(
        deterministic_error([r for r in strict if r["programme_id"] != drop])
        for drop in {r["programme_id"] for r in strict}
    ) >= 1

    # 6. Necessity and sufficiency both fail in the mixed-tier map.
    not_necessary = [
        r for r in translation
        if normalize_f(r["function_signal"]) == "lower"
        and normalize_i(r["interaction_signal"]) != "lower"
    ]
    not_sufficient = [
        r for r in translation
        if normalize_i(r["interaction_signal"]) == "lower"
        and normalize_f(r["function_signal"]) != "lower"
    ]
    assert len(not_necessary) >= 2
    assert len(not_sufficient) >= 3
    for drop in {r["programme_id"] for r in translation}:
        subset = [r for r in translation if r["programme_id"] != drop]
        assert any(
            normalize_f(r["function_signal"]) == "lower"
            and normalize_i(r["interaction_signal"]) != "lower"
            for r in subset
        ), drop
        assert any(
            normalize_i(r["interaction_signal"]) == "lower"
            and normalize_f(r["function_signal"]) != "lower"
            for r in subset
        ), drop

    # 7. High-confidence resolved false-reassurance anchors.
    assert {r["programme_id"] for r in proxy} == {
        "ML015",
        "P2_CF01_CARDIOPETALUM_2012",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
    }
    assert len({r["region"] for r in proxy}) == 3
    assert len({r["plant_family"] for r in proxy}) == 3
    assert {r["downstream_mismatch_status"] for r in proxy} == {"stable_downstream"}

    # 8. Simple reliability attenuation is quantitatively insufficient for all 3 anchors.
    assert {r["programme"] for r in reliability} == {
        "ML015_Wandoo", "P2_CARDIOPETALUM", "P2_KAKAMEGA_AP"
    }
    assert all(float(r["null_misfit_p"]) < 0.01 for r in reliability)
    assert all(float(r["artifact_downstream_probability"]) < 0.03 for r in reliability)

    # 9. Current quantitative measurement gap.
    assert len(ifc) == 8
    assert {r["interaction_measurement_class"] for r in ifc} == {"quantity_only"}

    # 10. Mechanistic triangulation remains external/hypothesis-generating.
    assert len(hidden) == 5
    assert sum(r["evidence_role"] == "external_context" for r in hidden) == 4
    assert sum(r["evidence_role"] == "internal_anchor" for r in hidden) == 1

    # 11. Broader transition filtering remains exploratory, not a promoted law.
    interaction = [r for r in transition if r["transition_class"] == "interaction_quantity_to_F"]
    mating = [r for r in transition if r["transition_class"] == "movement_mating_to_F"]
    cohort = [r for r in transition if r["transition_class"] == "adult_to_offspring_G"]
    assert len(interaction) == 3
    assert len(mating) == 3
    assert len(cohort) == 1
    re = gpair["primary_random_effects"]
    assert gpair["n_independent_programmes"] == 5
    assert re["ci95_mKH"][0] < 0 < re["ci95_mKH"][1]
    assert re["p_two_sided_t"] > 0.05

    # Promotion manifest / claim ceiling.
    assert promotion["schema_version"] == 1
    assert promotion["promoted_on"] == "2026-10-06"
    assert promotion["generality_gate"] == "pass"
    assert promotion["surprise_gate"] == "pass"
    assert promotion["main_general_principle"] == (
        "directional_coherence_without_interaction_function_identifiability"
    )
    assert promotion["strongest_resolved_failure_mode"] == "false_reassurance"
    assert promotion["mechanism_status"] == "hidden_effective_mating_hypothesis_not_confirmed"

    for token in (
        "directional coherence at coarse scale but no one-to-one interaction→function translation",
        "Interaction quantity is a non-identifying stand-alone sentinel",
        "neither necessary nor sufficient",
        "Strongest surprise: high-confidence error is directionally asymmetric",
        "Best current general ecological statement",
    ):
        assert token in generality, token

    for token in (
        "Mechanistic triangulation / hypothesis-generating context",
        "interaction quantity  →  effective mating quality  →  reproductive function",
        "not established by the current corpus",
    ):
        assert token in hidden_note, token

    assert "minimum 5 programme mismatches" in determinism_note
    assert "neither necessary nor sufficient" in logic_note
    assert "not readily explained by the audited difference in endpoint measurement reliability" in reliability_note
    assert "survives deletion of every single programme" in sentinel_note
    assert "three representation-stable quantitative false-reassurance anchors" in translation_note

    print(
        "ECOLOGICAL_GENERALITY_SURPRISE_PROMOTED "
        "direct_effects=17 negative_both_scales=17 "
        "translation_programmes=16 full_LOO_nonidentifying=true "
        "strict_programmes=8 strict_LOO_nonidentifying=true "
        "visitation_only_programmes=13 visitation_LOO_nonidentifying=true "
        "deterministic_min_errors=5 strict_errors=2 quantitative_strict_errors=1 "
        "necessity_fails=true sufficiency_fails=true "
        "stable_false_reassurance=3 reliability_artifact_null_misfit_all_p_lt_0.01=true "
        "effective_mating_measured=0_of_8 "
        "main_principle=directional_coherence_without_functional_identifiability "
        "mechanism=hidden_effective_mating_hypothesis_only prevalence_inference=false"
    )


if __name__ == "__main__":
    main()
