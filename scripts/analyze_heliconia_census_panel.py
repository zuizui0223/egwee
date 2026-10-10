#!/usr/bin/env python3
"""Exploratory, source-pinned Heliconia population-level census audit.

This is an independent external audit and NEVER enters EGWEE's frozen I-F,
five-direct-cluster, 16-programme or SF06 quantitative denominators.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import itertools
import json
import urllib.request
from collections import defaultdict
from pathlib import Path

BASE = ("https://raw.githubusercontent.com/BrunaLab/HeliconiaSurveys/"
        "0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0/data/survey_archive/")
PINNED = {
    "HDP_survey.csv": "f82a6f241493a979a2923d1c5deef6a1be0ff3ed",
    "HDP_plots.csv": "6fc835fb870d8c43ae4a4fcf04d515f419e6db22",
}
EXTERNAL_ONLY = True


def load_csv(name: str, local: Path | None) -> list[dict[str, str]]:
    if local is None:
        request = urllib.request.Request(BASE + name, headers={"User-Agent": "EGWEE-HDP-audit/1"})
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = response.read()
    else:
        raw = (local / name).read_bytes()
    sha = hashlib.sha1((f"blob {len(raw)}\\0".replace("\\0", "\0")).encode() + raw).hexdigest()
    assert sha == PINNED[name], (name, sha, PINNED[name])
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))


def mean(items: list[float]) -> float:
    assert items
    return sum(items) / len(items)


def permutation_test(rows: list[dict], key: str, stratified: bool) -> dict:
    nfragment = sum(x["group"] == "fragment" for x in rows)
    obs = mean([x[key] for x in rows if x["group"] == "fragment"]) - mean(
        [x[key] for x in rows if x["group"] == "continuous"]
    )
    if stratified:
        by_ranch: dict[str, list[int]] = defaultdict(list)
        for i, row in enumerate(rows):
            by_ranch[row["ranch"]].append(i)
        combinations = [
            list(itertools.combinations(v, sum(rows[i]["group"] == "fragment" for i in v)))
            for _, v in sorted(by_ranch.items())
        ]
        assignments = (tuple(itertools.chain.from_iterable(parts))
                       for parts in itertools.product(*combinations))
    else:
        assignments = itertools.combinations(range(len(rows)), nfragment)
    extreme, total = 0, 0
    for selected in assignments:
        ss = set(selected)
        d = mean([row[key] for i, row in enumerate(rows) if i in ss]) - mean(
            [row[key] for i, row in enumerate(rows) if i not in ss]
        )
        extreme += int(abs(d) >= abs(obs) - 1e-12)
        total += 1
    assert total == (240 if stratified else 1716), total
    return {"difference_fragment_minus_continuous": obs, "two_sided_p": extreme / total,
            "assignments": total}


def analyze(plot_rows: list[dict[str, str]], plant_rows: list[dict[str, str]]) -> dict:
    assert len(plot_rows) == 13 and len(plant_rows) == 66396
    assert len({p["plot_id"] for p in plot_rows}) == 13
    plots: dict[str, dict] = {}
    for x in plot_rows:
        p = x["plot_id"]
        plots[p] = {
            "plot": p, "group": "fragment" if p.startswith("FF-") else "continuous",
            "ranch": x["ranch"], "habitat": x["habitat"],
            "new": 0, "measured": 0, "eligible": 0,
            "alive": 0, "dead": 0, "missing": 0, "missing_later_resighted": 0,
        }
    assert sum(x["group"] == "fragment" for x in plots.values()) == 7

    status: dict[tuple[str, str], dict[int, str]] = defaultdict(dict)
    first_seed_year: dict[tuple[str, str], int] = {}
    seen: set[tuple[str, str, int]] = set()
    count_seed = 0
    years_by_plot: dict[str, set[int]] = defaultdict(set)
    for row in plant_rows:
        p, plant, year = row["plot_id"], row["plant_id"], int(row["year"])
        state, new = row["census_status"], row["recorded_sdlg"] == "TRUE"
        assert p in plots and 1998 <= year <= 2009
        assert state in {"measured", "dead", "missing"}
        k = (p, plant, year)
        assert k not in seen, k
        seen.add(k)
        years_by_plot[p].add(year)
        status[(p, plant)][year] = state
        if new:
            assert state == "measured" and (p, plant) not in first_seed_year
            first_seed_year[(p, plant)] = year
            count_seed += 1
        if 1999 <= year <= 2006:
            plots[p]["new"] += int(new)
            plots[p]["measured"] += int(state == "measured")
    assert len(status) == 8586 and count_seed == 3464
    assert all(set(range(1999, 2007)) <= years for years in years_by_plot.values())

    for key, year in first_seed_year.items():
        if not 1999 <= year <= 2005:
            continue
        rec = plots[key[0]]
        rec["eligible"] += 1
        state = status[key].get(year + 1)
        assert state in {"measured", "dead", "missing"}, (key, year, state)
        rec[{"measured": "alive", "dead": "dead", "missing": "missing"}[state]] += 1
        if state == "missing" and any(s == "measured" for yr, s in status[key].items() if yr > year + 1):
            rec["missing_later_resighted"] += 1

    plot_summary: list[dict] = []
    for x in sorted(plots.values(), key=lambda r: r["plot"]):
        assert x["alive"] + x["dead"] + x["missing"] == x["eligible"]
        assert x["measured"] > 0 and x["alive"] + x["dead"] > 0
        x["new_per_plot_year"] = x["new"] / 8
        x["new_per_100_alive_records"] = 100 * x["new"] / x["measured"]
        x["known_alive_fraction"] = x["alive"] / (x["alive"] + x["dead"])
        x["documented_alive_fraction"] = x["alive"] / x["eligible"]
        x["missing_fraction"] = x["missing"] / x["eligible"]
        x["all_missing_alive_bound"] = (x["alive"] + x["missing"]) / x["eligible"]
        plot_summary.append(x)

    metric_names = [
        "new_per_plot_year", "new_per_100_alive_records", "known_alive_fraction",
        "documented_alive_fraction", "missing_fraction", "all_missing_alive_bound",
    ]
    stats = {}
    for key in metric_names:
        stats[key] = {
            "mean_by_group": {
                g: mean([x[key] for x in plot_summary if x["group"] == g])
                for g in ("continuous", "fragment")
            },
            "unrestricted_exact_plot_label": permutation_test(plot_summary, key, False),
            "ranch_stratified_exact_plot_label": permutation_test(plot_summary, key, True),
        }

    assert all(x["group"] in {"continuous", "fragment"} for x in plot_summary)
    # Fail-closed reference checks: exploratory figures only, not a new primary effect.
    assert abs(stats["new_per_plot_year"]["mean_by_group"]["continuous"] - 35.0208333333) < 1e-8
    assert abs(stats["new_per_plot_year"]["mean_by_group"]["fragment"] - 20.25) < 1e-8
    assert abs(stats["known_alive_fraction"]["mean_by_group"]["continuous"] - 0.8499583537) < 1e-8
    assert abs(stats["known_alive_fraction"]["mean_by_group"]["fragment"] - 0.8582054820) < 1e-8
    assert abs(stats["missing_fraction"]["ranch_stratified_exact_plot_label"]["two_sided_p"] - 0.0416666667) < 1e-8
    assert sum(x["missing_later_resighted"] for x in plot_summary if x["group"] == "continuous") == 91
    assert sum(x["missing_later_resighted"] for x in plot_summary if x["group"] == "fragment") == 25
    return {
        "status": "EXPLORATORY_EXTERNAL_DIAGNOSTIC_NOT_PRIMARY_EGWEE",
        "source_repo": "BrunaLab/HeliconiaSurveys",
        "source_commit": "0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0",
        "source_blob": PINNED,
        "n_plant_year_records": len(plant_rows),
        "n_individuals": len(status),
        "n_seedlings_first_recorded": count_seed,
        "n_plots": len(plots), "balanced_recruitment_years": "1999-2006",
        "later_resighted_after_missing_by_group": {
            g: sum(x["missing_later_resighted"] for x in plot_summary if x["group"] == g)
            for g in ("continuous", "fragment")
        },
        "followup_seedling_cohorts": "1999-2005, next year observed",
        "plot_rows": plot_summary,
        "stats": stats,
        "critical_limits": [
            "Exact plot-label permutations are descriptive under observational habitat labels; not randomized treatment p-values.",
            "Recorded seedlings are already detected recruits, not seed arrival, viable seed, true seedling production or safe-site supply.",
            "Per-100-live-records is not an annual per-capita birth rate; contemporaneous density includes new seedlings.",
            "Missing means not found, not dead. Both complete-case and documented-alive summaries can be selection biased.",
            "13 plots (not 66396 independent replicates); plot ranch/size and prior history can confound contrasts.",
            "No matched pollinator, mating provenance, quality, safe-site availability or direct intervention outcomes.",
            "Pre-existing published studies already analyzed Heliconia recruitment and delayed climate effects.",
            "No additions to frozen EGWEE denominators, no publication-level hypothesis promotion."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-dir", type=Path, help="Pinned HDP CSVs already present on disk")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    result = analyze(load_csv("HDP_plots.csv", args.local_dir),
                     load_csv("HDP_survey.csv", args.local_dir))
    for k in ("new_per_plot_year", "new_per_100_alive_records",
              "known_alive_fraction", "documented_alive_fraction", "missing_fraction"):
        s = result["stats"][k]
        print(f"{k}: continuous={s['mean_by_group']['continuous']:.6f} "
              f"fragment={s['mean_by_group']['fragment']:.6f} "
              f"p_unrestricted={s['unrestricted_exact_plot_label']['two_sided_p']:.6f} "
              f"p_ranch={s['ranch_stratified_exact_plot_label']['two_sided_p']:.6f}")
    print(f"post_missing_resighted: {result['later_resighted_after_missing_by_group']}")
    print("HELICONIA_SOURCE_PINNED_AUDIT: PASS, external_only=True")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
