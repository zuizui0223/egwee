from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
NOTE = ROOT / "manuscript/SF06_PROBABILISTIC_SENTINEL_VALIDATION_2026-10-08.md"

# Previously frozen whole-publication exclusions, not outcome-selected.
OVERLAP = {
    "aizen & feinsinger (1994) ecology 75:330- 351",
    "angoh et al. (2021) south african journal of botany 141:196- 199",
    "chen & zuo (2019) frontiers in plant science 10:327",
    "chen et al. (2019) science of the total environment 654:1056- 1063",
    "chiapero et al. (2021) forest ecology and management 492:119215",
    "da silva elias et al. (2012) journal of tropical ecology 28:317- 320",
    "gonzález-varo et al. (2009) biological conservation 142:1058- 1065",
    "kolb (2008) biological conservation 141:2540- 2549",
    "lopes & buzato (2007) oecologia 154:305- 314",
}


def selected_pairs() -> list[dict]:
    with PAIRS.open(newline="", encoding="utf-8") as handle:
        source = list(csv.DictReader(handle))
    return [
        {
            "pub": r["source_publication_key"],
            "species": r["species"],
            "x": int(r["I_component_consensus_sign"] == "lower"),
            "y": int(r["F_component_consensus_sign"] == "lower"),
        }
        for r in source
        if r["land_use_factor_normalized"] == "habitat fragmentation"
        and r["I_component_consensus_sign"] in {"lower", "nonlower"}
        and r["F_component_consensus_sign"] in {"lower", "nonlower"}
    ]


def plug_in_information(rows: list[dict]) -> tuple[float, float, float]:
    n = len(rows)
    p = sum(r["y"] for r in rows) / n

    def entropy(q: float) -> float:
        if q in (0.0, 1.0):
            return 0.0
        return -q * math.log(q) - (1 - q) * math.log(1 - q)

    h = entropy(p)
    conditional_h = 0.0
    conditional_brier = 0.0
    for x in (0, 1):
        group = [r for r in rows if r["x"] == x]
        q = sum(r["y"] for r in group) / len(group)
        conditional_h += len(group) / n * entropy(q)
        conditional_brier += len(group) / n * q * (1 - q)
    return (h - conditional_h) / math.log(2), p * (1 - p), conditional_brier


def held_out(rows: list[dict], block: str, alpha: float) -> dict:
    assert block in {"pub", "species"}
    assert alpha > 0

    totals = {"brier0": 0.0, "brier1": 0.0, "logloss0": 0.0, "logloss1": 0.0}
    per_block: list[dict] = []

    for group in sorted({r[block] for r in rows}):
        train = [r for r in rows if r[block] != group]
        test = [r for r in rows if r[block] == group]
        p0 = (sum(r["y"] for r in train) + alpha) / (len(train) + 2 * alpha)
        stats = {key: 0.0 for key in totals}

        for r in test:
            subset = [z for z in train if z["x"] == r["x"]]
            p1 = (sum(z["y"] for z in subset) + alpha) / (len(subset) + 2 * alpha)
            for k, p in ((0, p0), (1, p1)):
                stats[f"brier{k}"] += (r["y"] - p) ** 2
                stats[f"logloss{k}"] -= (
                    r["y"] * math.log(p) + (1 - r["y"]) * math.log(1 - p)
                )

        for k in totals:
            totals[k] += stats[k]
        per_block.append({k: v / len(test) for k, v in stats.items()})

    result = {key: value / len(rows) for key, value in totals.items()}
    result["n"] = len(rows)
    result["blocks"] = len(per_block)
    result["block_balanced"] = {
        key: sum(item[key] for item in per_block) / len(per_block)
        for key in totals
    }
    return result


def approx(actual: float, expected: float) -> None:
    assert math.isclose(actual, expected, rel_tol=1e-8, abs_tol=1e-8), (
        actual, expected,
    )


def main() -> None:
    full = selected_pairs()
    independent = [r for r in full if r["pub"] not in OVERLAP]
    assert len(full) == 54
    assert len(independent) == 31
    assert len({r["pub"] for r in full}) == 32
    assert len({r["pub"] for r in independent}) == 23

    info_bits, brier0, brier1 = plug_in_information(full)
    approx(info_bits, 0.005432847132816968)
    approx(brier0, 0.1728395061728395)
    approx(brier1, 0.17146464646464646)
    assert info_bits > 0  # Classification equality is not information equality.

    expected = {
        ("full", "pub"): (0.1765888798031861, 0.1811820175765371,
                          0.5405584122836147, 0.551205251817771),
        ("disjoint", "pub"): (0.18310434464069428, 0.19461520748657388,
                              0.5578789047416953, 0.5958933164330948),
        ("full", "species"): (0.1794778959303102, 0.18591801508620812,
                              0.5489008782694261, 0.5647663761037238),
        ("disjoint", "species"): (0.18686851733745083, 0.198717083412865,
                                  0.5685728757933118, 0.607414936553136),
    }

    for name, rows in (("full", full), ("disjoint", independent)):
        for block in ("pub", "species"):
            result = held_out(rows, block, alpha=0.5)
            for field, target in zip(
                ("brier0", "brier1", "logloss0", "logloss1"),
                expected[(name, block)],
            ):
                approx(result[field], target)
            assert result["brier1"] > result["brier0"]
            assert result["logloss1"] > result["logloss0"]

        # Even when beta-binomial smoothing is varied after exposure, the same
        # direction of relative out-of-publication scores persists.
        for alpha in (0.5, 1.0, 2.0, 4.0):
            result = held_out(rows, "pub", alpha)
            assert result["brier1"] > result["brier0"]
            assert result["logloss1"] > result["logloss0"]
            for field in ("brier", "logloss"):
                assert result["block_balanced"][field + "1"] > result["block_balanced"][field + "0"]

    note = NOTE.read_text(encoding="utf-8")
    for token in (
        "0.00543 bits",
        "0.17659",
        "0.18118",
        "0.18310",
        "0.19462",
        "0.17948",
        "0.18592",
        "not a verified true physiological state",
    ):
        assert token in note, token

    print(
        "SF06_PROBABILISTIC_SENTINEL_VALUE: PASS "
        f"MI_bits={info_bits:.6f} "
        "full_and_disjoint_publication_and_species_LOO=baseline_better "
        "smoothing=0.5,1,2,4"
    )


if __name__ == "__main__":
    main()
