from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def i_state(x: str) -> str:
    if x in {"higher", "higher_or_shifted"}:
        return "higher_or_shifted"
    return x


def f_state(x: str) -> str:
    if x in {"similar", "no_detected_loss"}:
        return "similar_or_no_detected_loss"
    return x


def deterministic_error(rs: list[dict[str, str]]) -> tuple[int, dict[str, str], dict[str, Counter]]:
    by_i: dict[str, list[str]] = defaultdict(list)
    for r in rs:
        by_i[i_state(r["interaction_signal"])].append(f_state(r["function_signal"]))

    mapping: dict[str, str] = {}
    counters: dict[str, Counter] = {}
    errors = 0
    for i, vals in by_i.items():
        counts = Counter(vals)
        counters[i] = counts
        best_state, best_n = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0]
        mapping[i] = best_state
        errors += len(vals) - best_n
    return errors, mapping, counters


def strict(rs: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        r for r in rs
        if r["interaction_signal"] not in {"no_detected_loss", "mixed"}
        and r["function_signal"] not in {"no_detected_loss", "mixed"}
    ]


def main() -> None:
    rs = rows(MAP)
    assert len(rs) == 16

    full_errors, full_rule, full_counts = deterministic_error(rs)
    # Best possible programme-level deterministic lookup from interaction evidence
    # state to F evidence state still fails for multiple programmes.
    assert full_errors == 5, (full_errors, full_rule, full_counts)

    strict_rs = strict(rs)
    assert len(strict_rs) == 8
    strict_errors, strict_rule, strict_counts = deterministic_error(strict_rs)
    assert strict_errors == 2, (strict_errors, strict_rule, strict_counts)

    q = [r for r in strict_rs if r["evidence_tier"] == "quantitative"]
    assert len(q) == 5
    q_errors, q_rule, q_counts = deterministic_error(q)
    assert q_errors == 1, (q_errors, q_rule, q_counts)

    # Leave-one-programme-out: no single programme can make the full frozen map
    # perfectly deterministic.
    loo_min_errors = min(
        deterministic_error([r for r in rs if r["programme_id"] != drop])[0]
        for drop in {r["programme_id"] for r in rs}
    )
    assert loo_min_errors >= 4

    # In the strict mixed-tier subset, perfect determinism also cannot be
    # restored by deleting any single programme.
    strict_ids = {r["programme_id"] for r in strict_rs}
    strict_loo_min_errors = min(
        deterministic_error([r for r in strict_rs if r["programme_id"] != drop])[0]
        for drop in strict_ids
    )
    assert strict_loo_min_errors >= 1

    print(
        "IF_SENTINEL_DETERMINISM_OK "
        "programmes=16 full_min_misclassified=5 "
        "strict_programmes=8 strict_min_misclassified=2 "
        "strict_quantitative_programmes=5 strict_quantitative_min_misclassified=1 "
        f"full_LOO_min_misclassified={loo_min_errors} "
        f"strict_LOO_min_misclassified={strict_loo_min_errors} "
        "prevalence_inference=false"
    )


if __name__ == "__main__":
    main()
