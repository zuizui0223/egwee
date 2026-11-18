#!/usr/bin/env python3
"""Exploratory external Heliconia longitudinal audit; NOT a meta-analysis admission.

Uses immutable BrunaLab GitHub revision and checks Git blob SHAs before reading.
All 13 plots are independent *summary* units; repeated plant-years are not.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.request import urlopen

REV = "0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0"
ROOT_URL = "https://raw.githubusercontent.com/BrunaLab/HeliconiaSurveys/" + REV
SOURCES = {
    "survey": ("data/survey_archive/HDP_survey.csv", "f82a6f241493a979a2923d1c5deef6a1be0ff3ed"),
    "plots": ("data/survey_archive/HDP_plots.csv", "6fc835fb870d8c43ae4a4fcf04d515f419e6db22"),
}


def load_csv(key: str, local_file: str | None = None) -> list[dict[str, str]]:
    name, expected_sha = SOURCES[key]
    if local_file:
        data = Path(local_file).read_bytes()
    else:
        with urlopen(ROOT_URL + "/" + name, timeout=50) as response:
            data = response.read()
    actual = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if actual != expected_sha:
        raise RuntimeError(f"{key} source drift: {actual}, expected {expected_sha}")
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))


def mean(rows, key):
    return sum(r[key] for r in rows) / len(rows)


def exact_pvalue(rows, target, by_ranch=False):
    # Label-randomization *descriptive sensitivity*, not design-randomized inference.
    idxs = tuple(range(len(rows)))
    n_ff = sum(r["group"] == "fragment" for r in rows)
    observed = mean([r for r in rows if r["group"] == "fragment"], target) - mean(
        [r for r in rows if r["group"] == "continuous"], target
    )
    if by_ranch:
        groups = []
        for ranch in sorted({r["ranch"] for r in rows}):
            ids = tuple(i for i, row in enumerate(rows) if row["ranch"] == ranch)
            m = sum(rows[i]["group"] == "fragment" for i in ids)
            groups.append(list(itertools.combinations(ids, m)))
        assignments = (
            tuple(i for block in blocks for i in block)
            for blocks in itertools.product(*groups)
        )
    else:
        assignments = itertools.combinations(idxs, n_ff)
    total = exceed = 0
    for indices in assignments:
        ff = set(indices)
        difference = (
            sum(rows[i][target] for i in ff) / n_ff
            - sum(rows[i][target] for i in idxs if i not in ff) / (len(rows) - n_ff)
        )
        exceed += abs(difference) >= abs(observed) - 1e-12
        total += 1
    return {"observed_diff": observed, "two_sided_fraction": exceed / total,
            "label_allocations": total}


def analyze(survey, descriptors):
    plots = {r["plot_id"]: r for r in descriptors}
    assert len(plots) == 13
    assert sum(r["habitat"] != "forest" for r in plots.values()) == 7
    assert len(survey) == 66396
    individuals = defaultdict(dict)
    years = defaultdict(lambda: Counter())
    admissions = {}
    key_seen = set()
    status = Counter()
    new_count = 0
    for row in survey:
        p, yr, plant = row["plot_id"], int(row["year"]), row["plant_id"]
        assert p in plots
        key = (p, yr, plant)
        assert key not in key_seen, "Duplicate plot-person-year"
        key_seen.add(key)
        st = row["census_status"]
        assert st in {"measured", "dead", "missing"}, st
        status[st] += 1
        birth = row["recorded_sdlg"] == "TRUE"
        obj = individuals[p, plant]
        obj[yr] = st
        if birth:
            assert (p, plant) not in admissions, "Multiple birth records"
            admissions[p, plant] = yr
            new_count += 1
        x = years[p, yr]
        x["alive"] += st == "measured"
        x["new"] += birth
        x["flower"] += row["infl"] not in {"NA", ""}
    assert len(individuals) == 8586
    assert new_count == 3464
    assert set(years) == {(p, yr) for p in plots for yr in range(1998, 2007)} | {
        (p, yr) for (p, yr) in years if yr > 2006
    }, "1998-2006 must be complete for all plots"

    per_plot = []
    for p, descriptor in sorted(plots.items()):
        group = "continuous" if descriptor["habitat"] == "forest" else "fragment"
        entry = {"plot": p, "group": group, "habitat": descriptor["habitat"],
                 "ranch": descriptor["ranch"]}
        for name, first, last in (("early", 1999, 2002),
                                  ("late", 2003, 2006),
                                  ("full", 1999, 2006)):
            nr = sum(years[p, y]["new"] for y in range(first, last + 1))
            denom = sum(years[p, y - 1]["alive"] for y in range(first, last + 1))
            entry[name + "_seedlings"] = nr
            entry[name + "_prior_alive"] = denom
            entry[name + "_rate"] = nr / denom
        entry["change"] = entry["late_rate"] - entry["early_rate"]
        fup = Counter()
        for (plant_plot, plant), born in admissions.items():
            if plant_plot != p or not 1999 <= born <= 2005:
                continue
            fup[individuals[plant_plot, plant].get(born + 1, "absent")] += 1
        assert not fup["absent"], (p, fup)
        n = sum(fup.values())
        entry["seedling_follow_n"] = n
        entry["seedling_next_alive"] = fup["measured"]
        entry["seedling_next_dead"] = fup["dead"]
        entry["seedling_next_missing"] = fup["missing"]
        entry["known_survival"] = fup["measured"] / (fup["measured"] + fup["dead"])
        entry["lower_survival_bound"] = fup["measured"] / n
        entry["upper_survival_bound"] = (fup["measured"] + fup["missing"]) / n
        per_plot.append(entry)

    all_missing = Counter()
    newly_missing = Counter()
    for person, observations in individuals.items():
        for year in range(1998, 2006):
            if observations.get(year) == "missing":
                all_missing[observations.get(year + 1, "absent")] += 1
        born = admissions.get(person)
        if born is not None and 1999 <= born <= 2004 and observations.get(born + 1) == "missing":
            newly_missing[observations.get(born + 2, "absent")] += 1
    assert sum(all_missing.values()) == 3169
    assert all_missing["measured"] == 1339
    assert sum(newly_missing.values()) == 210
    assert newly_missing["measured"] == 100

    grouped = {}
    for g in ("continuous", "fragment"):
        aa = [r for r in per_plot if r["group"] == g]
        grouped[g] = {
            "plots": len(aa),
            "mean_seedlings_per_plot_year": mean(aa, "full_seedlings") / 8,
            "mean_new_per_previous_measured": mean(aa, "full_rate"),
            "mean_early_rate": mean(aa, "early_rate"),
            "mean_late_rate": mean(aa, "late_rate"),
            "mean_confirmed_survival_given_known": mean(aa, "known_survival"),
            "mean_survival_lower_bound": mean(aa, "lower_survival_bound"),
            "mean_survival_upper_bound": mean(aa, "upper_survival_bound"),
        }
    result = {
        "status": "post_hoc_exploratory_external_noncausal",
        "source_repo": "BrunaLab/HeliconiaSurveys",
        "source_commit": REV,
        "source_blob_shas": {k: v[1] for k, v in SOURCES.items()},
        "rows": len(survey), "individuals": len(individuals),
        "new_seedlings": new_count, "plot_count": len(plots),
        "status_counts": dict(status),
        "balanced_years": "1999-2006",
        "per_plot": per_plot,
        "group_equal_plot_means": grouped,
        "mean_recruitment_fraction_of_CF": (
            grouped["fragment"]["mean_seedlings_per_plot_year"]
            / grouped["continuous"]["mean_seedlings_per_plot_year"]
        ),
        "mean_per_capita_fraction_of_CF": (
            grouped["fragment"]["mean_new_per_previous_measured"]
            / grouped["continuous"]["mean_new_per_previous_measured"]
        ),
        "recruitment_exact_label_test": exact_pvalue(per_plot, "full_rate"),
        "recruitment_ranch_conditional_label_test": exact_pvalue(per_plot, "full_rate", True),
        "period_change_exact_label_test": exact_pvalue(per_plot, "change"),
        "period_change_ranch_conditional_label_test": exact_pvalue(per_plot, "change", True),
        "missing_followed_by": dict(all_missing),
        "first_year_seedlings_missing_next_then_followed_by": dict(newly_missing),
        "limitations": [
            "No individual plant-year is an independent fragmentation replicate.",
            "Status 'missing' does not mean dead: some individuals reappear.",
            "Known-status survival conditions on ascertainment, with severe differential missingness.",
            "Prior-measured abundance is not reproductive adult density or seed supply.",
            "Fragment size and ranch context are non-exchangeable; label permutations are sensitivity diagnostics.",
            "Time-split differences may reflect climate, observation, density or other changes.",
            "Previously published Heliconia demography and recruitment mechanism studies preempt novelty claims.",
            "Never add this programme to frozen EGWEE primary quantitative denominators.",
        ],
    }
    assert abs(result["mean_per_capita_fraction_of_CF"] - 0.9460105252) < 1e-8
    assert result["recruitment_exact_label_test"]["label_allocations"] == 1716
    assert result["recruitment_ranch_conditional_label_test"]["label_allocations"] == 240
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--survey", default=None, help="Use locally cached source file")
    parser.add_argument("--plots", default=None, help="Use locally cached plot file")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    result = analyze(load_csv("survey", args.survey), load_csv("plots", args.plots))
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        target = Path(args.out)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(serialized, encoding="utf-8")
    g = result["group_equal_plot_means"]
    print("HELICONIA_LONGITUDINAL_AUDIT: PASS")
    print("CF rate", g["continuous"]["mean_new_per_previous_measured"],
          "FF rate", g["fragment"]["mean_new_per_previous_measured"])
    print("Absolute recruitment plot ratio", result["mean_recruitment_fraction_of_CF"])
    print("Density-index ratio", result["mean_per_capita_fraction_of_CF"])
    print("Exact plot-label sensitivity", result["recruitment_exact_label_test"])
    print("Period DID sensitivity", result["period_change_exact_label_test"])
    print("Missing reappearance", result["missing_followed_by"],
          "seedling missing reappearance", result["first_year_seedlings_missing_next_then_followed_by"])


if __name__ == "__main__":
    main()
