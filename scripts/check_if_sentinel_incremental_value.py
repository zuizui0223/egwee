from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"
NOTE = ROOT / "manuscript/IF_SENTINEL_INCREMENTAL_VALUE_2026-10-07.md"


def rows():
    with MAP.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def i_class(x: str):
    if x == "lower":
        return "lower"
    if x in {"higher", "higher_or_shifted"}:
        return "higher_or_shifted"
    return None


def f_class(x: str):
    return x if x in {"lower", "higher", "similar"} else None


def audit(rs, ikey, fkey):
    f_counts = Counter(r[fkey] for r in rs)
    baseline = len(rs) - max(f_counts.values())
    by = defaultdict(Counter)
    for r in rs:
        by[r[ikey]][r[fkey]] += 1
    lookup = sum(sum(v.values()) - max(v.values()) for v in by.values())
    return baseline, lookup, baseline - lookup


def main() -> None:
    rs = rows()
    assert len(rs) == 16

    full = audit(rs, "interaction_signal", "function_signal")
    assert full == (10, 5, 5)

    strict = []
    for r in rs:
        i = i_class(r["interaction_signal"])
        f = f_class(r["function_signal"])
        if i is not None and f is not None:
            strict.append({**r, "I": i, "F": f})
    assert len(strict) == 8
    strict_a = audit(strict, "I", "F")
    assert strict_a == (3, 2, 1)

    quant = [r for r in strict if r["evidence_tier"] == "quantitative"]
    assert len(quant) == 5
    quant_a = audit(quant, "I", "F")
    assert quant_a == (1, 1, 0)

    note = NOTE.read_text(encoding="utf-8")
    assert "errors = **10/16**" in note
    assert "errors = **5/16**" in note
    assert "errors = **3/8**" in note
    assert "errors = **2/8**" in note
    assert "**0 programmes**" in note

    print("IF_SENTINEL_INCREMENTAL_VALUE: PASS full_gain=5 strict_gain=1 strict_quant_gain=0")


if __name__ == "__main__":
    main()
