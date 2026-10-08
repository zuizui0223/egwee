from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "evidence/meta_extraction/myrtus_2010_2012_patch_crosswalk_v1.csv"
STAGE = ROOT / "evidence/meta_extraction/fragmentation_stage_displacement_context_v1.csv"
NOTE = ROOT / "manuscript/FRAGMENTATION_STAGE_DISPLACEMENT_2026-10-08.md"
MS = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"


def rows(p: Path) -> list[dict[str, str]]:
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    patches = rows(PATCH)
    stages = rows(STAGE)
    assert len(patches) == 4
    expected = {"DBL": (0.23, "large"), "CHP": (0.46, "large"),
                "PTR": (0.72, "small_connected"), "CRB": (0.13, "small_isolated")}
    actual = {r["patch_code"]: (float(r["2010_outcrossing_tm"]), r["2010_patch_class"]) for r in patches}
    assert actual == expected, (actual, expected)
    by_code = {r["patch_code"]: r for r in patches}
    assert by_code["PTR"]["2012_field_patch_class"] == "small"
    assert by_code["CRB"]["2012_field_patch_class"] == "small"
    assert "worst_field" in by_code["PTR"]["2012_field_early_performance"]
    assert "among_better" in by_code["CRB"]["2012_field_early_performance"]
    assert "no_saplings_or_juveniles" in by_code["CRB"]["2012_sapling_juvenile_status"]
    assert all("separate_samples" in r["source_frame_status"] for r in patches)

    stage_by_id = {r["case_id"]: r for r in stages}
    assert {"MY2009", "MY2010", "MY2012", "MY2015"} <= stage_by_id.keys()
    assert stage_by_id["MY2015"]["source_doi"] == "10.1111/1365-2664.12424"
    assert all(r["frozen_quantitative_denominator_role"] == "none" for r in stages)

    note = NOTE.read_text(encoding="utf-8")
    for token in (
        "PTR", "CRB", "68.3%", "43.3%", "44-fold",
        "110", "304", "1956", "2002", "316.9", "327.6",
        "not a synchronous mediation dataset",
        "not a newly measured synchronized path model",
    ):
        assert token.lower() in note.lower(), token

    manuscript = MS.read_text(encoding="utf-8")
    assert "González-Varo et al., 2009, 2010, 2012, 2015" in manuscript
    assert "10.1111/1365-2664.12424" in manuscript
    assert "44-fold lower recruitment" in manuscript

    # Contextual examples cannot change the frozen quantitative denominator.
    assert len(patches) == 4 and len({r["patch_code"] for r in patches}) == 4
    print("MYRTUS_STAGE_DISPLACEMENT: PASS "
          "four matched population codes; stage 2009/2010/2012/2015; "
          "no synchronous/causal inference or denominator reclassification")


if __name__ == "__main__":
    main()
