from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "evidence/meta_extraction/stage_opportunity_source_ledger_v1.csv"
NOTE = ROOT / "manuscript/STAGE_OPPORTUNITY_TEST_2026-10-08.md"
STAGE_NOTE = ROOT / "manuscript/FRAGMENTATION_STAGE_DISPLACEMENT_2026-10-08.md"

with LEDGER.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 5, "Five literature reports, not five independent programmes"
assert len({r["source_id"] for r in rows}) == 5
assert all(r["admission"] == "external_mechanism_only" for r in rows)
groups = {r["landscape_group"] for r in rows}
assert groups == {"MYRTUS_GUADALQUIVIR", "HELICONIA_AMAZON", "PRIMULA_CANTABRIAN"}
assert sum(r["landscape_group"] == "MYRTUS_GUADALQUIVIR" for r in rows) == 3

myrtus = next(r for r in rows if r["source_id"] == "M2012")
cpl, cps = float(myrtus["cp_large"]), float(myrtus["cp_small"])
oprl, oprs = float(myrtus["opr_large"]), float(myrtus["opr_small"])
cp_ratio = cpl / cps
opr_ratio = oprl / oprs
contrast_amplification = opr_ratio / cp_ratio
assert abs(cp_ratio - 9.5) < 1e-10
assert abs(opr_ratio - (300 / 7)) < 1e-10
assert 4.5 < contrast_amplification < 4.6
for row in rows:
    if row["source_id"] != "M2012":
        assert all(not row[col] for col in ("cp_large", "cp_small", "opr_large", "opr_small"))

note = NOTE.read_text(encoding="utf-8")
stage = STAGE_NOTE.read_text(encoding="utf-8")
for token in (
    "not a measured causal multiplier",
    "standing bottleneck",
    "fragmentation-sensitive",
    "intervention",
    "Primula vulgaris",
    "held-out",
    "not three independent",
):
    assert token.lower() in note.lower(), token
assert "standing bottleneck" in stage
assert "source reports approximately 44-fold" in stage
print(
    "STAGE_OPPORTUNITY_LEDGER: PASS "
    f"reports={len(rows)} landscape_groups={len(groups)} "
    f"CP_ratio={cp_ratio:.3f} OPR_ratio={opr_ratio:.3f} "
    f"descriptive_ratio_of_ratios={contrast_amplification:.3f}; "
    "no pooled meta-analysis inference"
)
