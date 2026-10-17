from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"
QUANT = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
QUAL = ROOT / "evidence/meta_extraction/qualitative_external_if_audit_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    mapping = rows(MAP)
    quantitative = rows(QUANT)
    qualitative = rows(QUAL)

    assert len(mapping) == 16
    assert sum(r["evidence_tier"] == "quantitative" for r in mapping) == 8
    assert sum(r["evidence_tier"] == "qualitative" for r in mapping) == 8

    qmap = [r for r in mapping if r["evidence_tier"] == "quantitative"]
    xmap = [r for r in mapping if r["evidence_tier"] == "qualitative"]

    assert {r["programme_id"] for r in qmap} == {r["programme_id"] for r in quantitative}
    assert {r["programme_id"] for r in xmap} == {r["audit_id"] for r in qualitative}

    qsrc = {r["source_id"] for r in quantitative}
    xsrc = {r["source_id"] for r in qualitative}
    assert qsrc.isdisjoint(xsrc)
    assert len(qsrc | xsrc) == 16

    q_by = {r["programme_id"]: r for r in quantitative}
    for r in qmap:
        src = q_by[r["programme_id"]]
        assert r["source_id"] == src["source_id"]
        assert r["system"] == src["system"]

    x_by = {r["audit_id"]: r for r in qualitative}
    for r in xmap:
        src = x_by[r["programme_id"]]
        assert r["source_id"] == src["source_id"]
        assert r["system"] == src["taxon"]

    # Translation non-identifiability: the same upstream qualitative signal
    # is represented with more than one downstream functional state.
    lower_F = {
        r["function_signal"]
        for r in mapping
        if r["interaction_signal"] == "lower"
    }
    assert {"lower", "higher", "no_detected_loss"} <= lower_F

    no_loss_F = {
        r["function_signal"]
        for r in mapping
        if r["interaction_signal"] == "no_detected_loss"
    }
    assert {"lower", "no_detected_loss"} <= no_loss_F

    higher_F = {
        r["function_signal"]
        for r in mapping
        if r["interaction_signal"] == "higher"
    }
    assert {"lower", "similar"} <= higher_F

    # Strong quantitative downstream anchors remain exactly the frozen three.
    resolved_downstream = {
        r["programme_id"]
        for r in mapping
        if r["resolution_status"] in {
            "resolved_downstream",
            "one_resolved_downstream_panel",
        }
    }
    assert resolved_downstream == {
        "ML015",
        "P2_CF01_CARDIOPETALUM_2012",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
    }

    # Qualitative hidden function loss is external support, not quantitative replication.
    hidden_qual = {
        r["programme_id"]
        for r in mapping
        if r["evidence_tier"] == "qualitative"
        and r["translation_topology"] == "hidden_function_loss"
    }
    assert hidden_qual == {"QIF008"}

    print(
        "IF_TRANSLATION_MAP_OK "
        "programmes=16 quantitative=8 qualitative=8 unique_sources=16 "
        "I_lower_maps_to=lower+higher+no_detected_loss "
        "I_no_detected_loss_maps_to=lower+no_detected_loss "
        "I_higher_maps_to=lower+similar "
        "resolved_downstream_quantitative=3 qualitative_hidden_function_loss=1 "
        "prevalence_inference=false"
    )


if __name__ == "__main__":
    main()
