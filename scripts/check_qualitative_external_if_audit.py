from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "evidence/meta_extraction/qualitative_external_if_audit_v1.csv"
GATE = ROOT / "evidence/meta_extraction/phase2_if_quantitative_gate_v1.csv"
HULTING = ROOT / "evidence/meta_extraction/PS014_hulting_extraction_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    audit = rows(AUDIT)
    gate = rows(GATE)
    hulting = rows(HULTING)

    assert len(audit) == 8
    assert len({r["audit_id"] for r in audit}) == 8

    expected_gate_ids = {
        "IFQ003",
        "IFQ006",
        "IFQ007",
        "IFQ008",
        "IFQ015",
        "IFQ020",
        "IFQ022",
    }
    audit_gate_ids = {r["gate_id"] for r in audit if r["gate_id"].startswith("IFQ")}
    assert audit_gate_ids == expected_gate_ids

    gate_by = {r["queue_id"]: r for r in gate}
    assert expected_gate_ids <= set(gate_by)
    for qid in expected_gate_ids:
        g = gate_by[qid]
        assert g["design_screen_status"] == "design_passed", (qid, g["design_screen_status"])
        assert g["effect_calculation_opened"] == "no", qid
        assert g["pair_programme_admitted"] == "no", qid
        assert g["pair_programme_increment"] == "0", qid

    audit_by_gate = {r["gate_id"]: r for r in audit}
    for qid in expected_gate_ids:
        assert audit_by_gate[qid]["quantitative_gate_status"] == gate_by[qid]["quantitative_gate_status"]

    # Hulting is an already-registered qualitative programme, not a Phase-2
    # quantitative-gate row.
    h_by = {r["endpoint_id"]: r for r in hulting}
    assert h_by["I_pollination_rate"]["fragmented_mean"] == "no_detected_edge_effect"
    assert h_by["I_pollination_rate"]["reference_mean"] == "no_detected_edge_effect"
    assert h_by["F_seed_production"]["fragmented_mean"] == "lower_near_edge"
    assert h_by["F_seed_production"]["reference_mean"] == "higher_farther_from_edge"
    assert audit_by_gate["ML007"]["quantitative_gate_status"] == "source_access_blocked_no_covariance_aware_IF_effect"

    counts: dict[str, int] = {}
    for r in audit:
        counts[r["qualitative_geometry"]] = counts.get(r["qualitative_geometry"], 0) + 1

    assert counts == {
        "resilient_no_detected_loss": 2,
        "interaction_loss_function_not_detected_lower": 2,
        "interaction_increase_or_shift_function_similar": 1,
        "concordant_population_size_effect": 1,
        "interaction_increase_function_similar": 1,
        "qualitative_hidden_function_loss": 1,
    }

    nonmonotonic_ids = {
        r["gate_id"]
        for r in audit
        if r["qualitative_geometry"] in {
            "interaction_loss_function_not_detected_lower",
            "interaction_increase_or_shift_function_similar",
            "interaction_increase_function_similar",
            "qualitative_hidden_function_loss",
        }
    }
    assert nonmonotonic_ids == {"IFQ006", "IFQ007", "IFQ015", "IFQ022", "ML007"}

    # Explicit firewall: no-detected-effect language may not be silently
    # promoted to equality/zero-effect claims.
    forbidden_fragments = ("effect=0", "true_equal", "proved_equal", "confirmed_zero")
    for r in audit:
        joined = " ".join(r.values()).casefold()
        assert not any(token in joined for token in forbidden_fragments)

    print(
        "QUALITATIVE_EXTERNAL_IF_AUDIT_OK "
        "programmes=8 quantitative_blocked=8 "
        "qualitative_nonmonotonic=5 resilient_no_detected_loss=2 "
        "concordant_size_effect=1 hidden_function_loss=1 "
        "no_prevalence_inference=true"
    )


if __name__ == "__main__":
    main()
