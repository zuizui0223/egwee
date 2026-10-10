#!/usr/bin/env python3
"""Independent-plot Heliconia exploratory audit.

Input: audited plot-level 1999–2005 cohorts reconstructed from
BrunaLab/HeliconiaSurveys data/survey_archive/HDP_survey.csv
Git blob f82a6f241493a979a2923d1c5deef6a1be0ff3ed.
No input row is a new EGWEE primary meta-analysis cluster.
"""

from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence/meta_extraction/heliconia_plot_cohorts_1999_2005_v1.csv"
EXPECTED_SOURCE_BLOB = "f82a6f241493a979a2923d1c5deef6a1be0ff3ed"


def average(vals):
    return sum(vals) / len(vals)


def load():
    with SOURCE.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 13
    assert {r["habitat"] for r in rows} == {"continuous", "fragment"}
    assert sum(r["habitat"] == "continuous" for r in rows) == 6
    assert sum(r["habitat"] == "fragment" for r in rows) == 7
    assert len({r["plot_id"] for r in rows}) == 13
    assert len({r["ranch"] for r in rows}) == 3
    assert all(r["source_blob_sha"] == EXPECTED_SOURCE_BLOB for r in rows)
    assert all(int(r["cohort_years"]) == 7 for r in rows)

    for r in rows:
        for k in (
            "baseline_live_1998", "new_seedlings_1999_2005",
            "live_records_1999_2005", "flowering_records_1999_2005",
            "eligible_seedlings", "next_measured", "next_dead",
            "next_missing", "next_absent", "missing_later_measured",
        ):
            r[k] = int(r[k])
        assert r["eligible_seedlings"] == r["new_seedlings_1999_2005"]
        assert r["eligible_seedlings"] == sum(
            r[k] for k in ("next_measured", "next_dead", "next_missing", "next_absent")
        )
        assert r["missing_later_measured"] <= r["next_missing"]
        assert r["baseline_live_1998"] > 0
        r["new_per_plot_year"] = r["new_seedlings_1999_2005"] / 7
        r["new_per_live_record"] = (
            r["new_seedlings_1999_2005"] / r["live_records_1999_2005"]
        )
        r["new_per_initial_plant_7years"] = (
            r["new_seedlings_1999_2005"] / r["baseline_live_1998"]
        )
        r["known_next_survival"] = (
            r["next_measured"] / (r["next_measured"] + r["next_dead"])
        )
        r["next_survival_lb"] = r["next_measured"] / r["eligible_seedlings"]
        r["next_survival_ub"] = (
            (r["next_measured"] + r["next_missing"] + r["next_absent"])
            / r["eligible_seedlings"]
        )
        r["next_missing_fraction"] = (
            (r["next_missing"] + r["next_absent"]) / r["eligible_seedlings"]
        )
    assert sum(r["eligible_seedlings"] for r in rows) == 2590
    assert sum(r["next_missing"] for r in rows) == 222
    assert sum(r["missing_later_measured"] for r in rows) == 116
    return sorted(rows, key=lambda r: r["plot_id"])


def permutations(rows, ranch_stratified):
    indices = list(range(len(rows)))
    if not ranch_stratified:
        yield from itertools.combinations(indices, 6)
        return
    strata = {}
    for i, r in enumerate(rows):
        strata.setdefault(r["ranch"], []).append(i)
    groups = []
    for ix in strata.values():
        n_control = sum(rows[i]["habitat"] == "continuous" for i in ix)
        groups.append(list(itertools.combinations(ix, n_control)))
    for combo in itertools.product(*groups):
        yield tuple(i for subset in combo for i in subset)


def contrast(rows, continuous_indices, key):
    a = set(continuous_indices)
    return average([r[key] for i, r in enumerate(rows) if i in a]) - average(
        [r[key] for i, r in enumerate(rows) if i not in a]
    )


def exact(rows, key, within_ranch):
    original = tuple(i for i, r in enumerate(rows) if r["habitat"] == "continuous")
    observed = contrast(rows, original, key)
    perms = list(permutations(rows, within_ranch))
    assert len(perms) == (240 if within_ranch else 1716)
    extremes = sum(
        abs(contrast(rows, ix, key)) >= abs(observed) - 1e-12
        for ix in perms
    )
    return {"delta_CF_minus_FF": observed, "p_two_sided": extremes / len(perms),
            "extreme": extremes, "permutations": len(perms)}


def main():
    rows = load()
    metrics = {
        "new_per_plot_year": (0.26456876456876455, 0.2375),
        "new_per_live_record": (0.837995337995338, 0.7958333333333333),
        "new_per_initial_plant_7years": (0.39335664335664333, 0.30416666666666664),
        "known_next_survival": (0.6544289044289044, 0.5666666666666667),
        "next_survival_lb": (0.053613053613053616, 0.020833333333333332),
        "next_survival_ub": (0.40734265734265734, 0.35),
        "next_missing_fraction": (0.06876456876456877, 0.041666666666666664),
    }
    results = {}
    for metric, (target_all, target_ranch) in metrics.items():
        all_p = exact(rows, metric, within_ranch=False)
        ranch_p = exact(rows, metric, within_ranch=True)
        assert abs(all_p["p_two_sided"] - target_all) < 1e-12, metric
        assert abs(ranch_p["p_two_sided"] - target_ranch) < 1e-12, metric
        results[metric] = {
            "continuous_plot_mean": average(
                [r[metric] for r in rows if r["habitat"] == "continuous"]
            ),
            "fragment_plot_mean": average(
                [r[metric] for r in rows if r["habitat"] == "fragment"]
            ),
            "unstratified_exact": all_p,
            "ranch_conditioned_exact": ranch_p,
        }
    # Critical sign reversal: plot-area output favours continuous forest
    # but 7-year recruitment per 1998 live plant does not.
    assert results["new_per_plot_year"]["unstratified_exact"]["delta_CF_minus_FF"] > 0
    assert results["new_per_initial_plant_7years"]["unstratified_exact"]["delta_CF_minus_FF"] < 0

    print(json.dumps({
        "status": "PASS",
        "source": "BrunaLab/HeliconiaSurveys",
        "source_blob": EXPECTED_SOURCE_BLOB,
        "scope": "exploratory; 13 plots; 1999-2005 first-year recruits",
        "statistical_boundary": (
            "Unstratified and ranch-conditioned label permutations describe "
            "the observed grouping; exchangeability and causal randomization "
            "are not established by this observational contrast."
        ),
        "missing_boundary": (
            "Known-status survival excludes next-year missing; lower and "
            "upper survival bounds assume all missing dead or all alive."
        ),
        "counts": {
            "plots": len(rows),
            "new_seedlings": sum(r["eligible_seedlings"] for r in rows),
            "measured_next": sum(r["next_measured"] for r in rows),
            "dead_next": sum(r["next_dead"] for r in rows),
            "missing_next": sum(r["next_missing"] for r in rows),
            "missing_later_measured": sum(r["missing_later_measured"] for r in rows),
        },
        "metrics": results,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
