#!/usr/bin/env python3
"""Independent-plot, provenance-locked audit of Heliconia annual censuses.

A secondary observation-process sensitivity, NOT a new causal life-table analysis
and NOT an additional independent EGWEE programme.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import itertools
import json
from collections import defaultdict
from pathlib import Path
from urllib.request import urlopen

UPSTREAM_COMMIT = "0b999f6bcb47df1c31f0dd0a8b472055b5f81bc0"
BASE_URL = f"https://raw.githubusercontent.com/BrunaLab/HeliconiaSurveys/{UPSTREAM_COMMIT}/data/survey_archive"
BLOBS = {
    "HDP_survey.csv": "f82a6f241493a979a2923d1c5deef6a1be0ff3ed",
    "HDP_plots.csv": "6fc835fb870d8c43ae4a4fcf04d515f419e6db22",
}
COHORT_START, COHORT_LAST = 1999, 2005
SOURCE_UNIT = "plot (6 continuous, 7 fragmented); 3 ranch blocks"


def read_bytes(filename: str, source_dir: Path | None) -> bytes:
    if source_dir is not None:
        raw = (source_dir / filename).read_bytes()
    else:
        with urlopen(f"{BASE_URL}/{filename}", timeout=45) as stream:
            raw = stream.read()
    sha = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    assert sha == BLOBS[filename], f"STOP: source hash differs for {filename}: {sha}"
    return raw


def rows(filename: str, source_dir: Path | None) -> list[dict[str, str]]:
    raw = read_bytes(filename, source_dir)
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))


def mean(xs: list[float]) -> float:
    assert xs
    return sum(xs) / len(xs)


def exact_permutation(plots: list[dict], field: str, ranch_block: bool) -> dict:
    idx = list(range(len(plots)))
    nf = sum(x["group"] == "fragment" for x in plots)
    groups = defaultdict(list)
    for i, p in enumerate(plots):
        groups[p["ranch"]].append(i)
    if ranch_block:
        choices = []
        for indices in groups.values():
            k = sum(plots[i]["group"] == "fragment" for i in indices)
            choices.append(list(itertools.combinations(indices, k)))
        assignments = (
            set(itertools.chain.from_iterable(blocks))
            for blocks in itertools.product(*choices)
        )
    else:
        assignments = (set(i) for i in itertools.combinations(idx, nf))

    values = [p[field] for p in plots]
    observed = mean([p[field] for p in plots if p["group"] == "fragment"]) - mean(
        [p[field] for p in plots if p["group"] == "continuous"]
    )
    extreme, total = 0, 0
    for selected in assignments:
        other = [i for i in idx if i not in selected]
        stat = mean([values[i] for i in selected]) - mean([values[i] for i in other])
        extreme += abs(stat) >= abs(observed) - 1e-12
        total += 1
    return {"difference_fragment_minus_continuous": observed,
            "extreme": extreme, "total": total, "two_sided_permutation_p": extreme / total,
            "stratified_by_ranch": ranch_block}


def run(source_dir: Path | None) -> dict:
    survey = rows("HDP_survey.csv", source_dir)
    descriptors = rows("HDP_plots.csv", source_dir)
    info = {r["plot_id"]: r for r in descriptors}
    assert len(info) == 13
    assert len(survey) == 66396

    individuals: dict[tuple[str, str], dict[int, dict]] = defaultdict(dict)
    plotyear = defaultdict(lambda: {"alive": 0, "new": 0})
    status_counts = defaultdict(int)
    total_new = 0
    for r in survey:
        plot, year = r["plot_id"], int(r["year"])
        key = (plot, r["plant_id"])
        assert plot in info
        assert year not in individuals[key], f"duplicate plot-person-year {key!r} {year}"
        status = r["census_status"]
        new = r["recorded_sdlg"] == "TRUE"
        assert status in ("measured", "dead", "missing")
        individuals[key][year] = {"status": status, "new": new}
        status_counts[status] += 1
        plotyear[(plot, year)]["alive"] += (status == "measured")
        plotyear[(plot, year)]["new"] += new
        total_new += new

    assert len(individuals) == 8586 and total_new == 3464
    counts = defaultdict(lambda: {"cohorts": 0, "alive": 0, "dead": 0,
                                  "missing": 0, "absent": 0, "later_reappeared": 0})
    for (plot, _plant), track in individuals.items():
        incoming = [y for y, v in track.items() if v["new"]]
        assert len(incoming) <= 1
        if not incoming:
            continue
        y = incoming[0]
        assert y == min(track), "recruitment flag after first observation"
        if not (COHORT_START <= y <= COHORT_LAST):
            continue
        c = counts[plot]
        c["cohorts"] += 1
        next_state = track.get(y + 1, {}).get("status", "absent")
        c["alive" if next_state == "measured" else next_state] += 1
        if next_state == "missing" and any(
            later > y + 1 and rec["status"] == "measured"
            for later, rec in track.items()
        ):
            c["later_reappeared"] += 1

    plots = []
    for plot, item in sorted(info.items()):
        group = "continuous" if item["habitat"] == "forest" else "fragment"
        assert group == ("continuous" if plot.startswith("CF-") else "fragment")
        c = counts[plot]
        recruits, prior_stock = 0, 0
        for y in range(COHORT_START, COHORT_LAST + 1):
            assert (plot, y) in plotyear and (plot, y - 1) in plotyear
            recruits += plotyear[(plot, y)]["new"]
            prior_stock += plotyear[(plot, y - 1)]["alive"]
        assert c["cohorts"] == recruits
        known = c["alive"] + c["dead"]
        unknown = c["missing"] + c["absent"]
        assert c["cohorts"] == known + unknown and known > 0 and prior_stock > 0
        plots.append({
            "plot": plot, "ranch": item["ranch"], "fragment_class": item["habitat"],
            "group": group, "cohort_seedlings": recruits,
            "annual_new_seedlings": recruits / 7,
            "previous_alive_stock_person_years": prior_stock,
            "new_per_100_prior_alive": 100 * recruits / prior_stock,
            "next_year_alive": c["alive"], "next_year_dead": c["dead"],
            "next_year_missing": c["missing"], "next_year_absent": c["absent"],
            "later_seen_alive_after_missing": c["later_reappeared"],
            "next_year_known_state_alive_fraction": c["alive"] / known,
            "next_year_unknown_fraction": unknown / c["cohorts"],
            "alive_lower_if_all_unknown_dead": c["alive"] / c["cohorts"],
            "alive_upper_if_all_unknown_alive": (c["alive"] + unknown) / c["cohorts"],
        })
    assert sum(p["cohort_seedlings"] for p in plots) == 2590
    assert sum(p["later_seen_alive_after_missing"] for p in plots) == 116
    assert sum(p["next_year_missing"] for p in plots) == 222

    fields = (
        "annual_new_seedlings", "new_per_100_prior_alive",
        "next_year_known_state_alive_fraction", "next_year_unknown_fraction",
        "alive_lower_if_all_unknown_dead", "alive_upper_if_all_unknown_alive",
    )
    summaries = {}
    for field in fields:
        cf = mean([p[field] for p in plots if p["group"] == "continuous"])
        ff = mean([p[field] for p in plots if p["group"] == "fragment"])
        summaries[field] = {"continuous": cf, "fragment": ff,
                            "fragment_minus_continuous": ff - cf,
                            "unblocked": exact_permutation(plots, field, False),
                            "ranch_blocked": exact_permutation(plots, field, True)}
    survival_difference_bounds = {
        "minimum": summaries["alive_lower_if_all_unknown_dead"]["fragment"]
                   - summaries["alive_upper_if_all_unknown_alive"]["continuous"],
        "maximum": summaries["alive_upper_if_all_unknown_alive"]["fragment"]
                   - summaries["alive_lower_if_all_unknown_dead"]["continuous"],
    }

    assert abs(summaries["new_per_100_prior_alive"]["continuous"] - 7.251815971862254) < 1e-10
    assert abs(summaries["new_per_100_prior_alive"]["fragment"] - 7.190957217875826) < 1e-10
    assert abs(summaries["next_year_known_state_alive_fraction"]["continuous"] - 0.84995835369592) < 1e-10
    assert abs(summaries["next_year_known_state_alive_fraction"]["fragment"] - 0.8582054820264126) < 1e-10
    assert summaries["new_per_100_prior_alive"]["unblocked"]["total"] == 1716
    assert summaries["new_per_100_prior_alive"]["ranch_blocked"]["total"] == 240

    return {"schema": 1, "status": "post_hoc_observation_process_sensitivity",
            "source": {"repository": "BrunaLab/HeliconiaSurveys",
                       "commit": UPSTREAM_COMMIT, "git_blob_shas": BLOBS,
                       "reanalysis_non_independent_of_prior_heliconia_papers": True},
            "cohort_years": "1999–2005; next census 2000–2006",
            "independence": SOURCE_UNIT,
            "data_quality": {"source_rows": len(survey), "individuals": len(individuals),
                             "new_seedlings_all_years": total_new,
                             "new_seedlings_selected_cohorts": 2590,
                             "missing_next_year": 222, "later_reappeared": 116,
                             "census_states": dict(status_counts)},
            "plot_metrics": plots, "plot_mean_summaries": summaries,
            "worst_case_missing_survival_difference_bounds": survival_difference_bounds,
            "limitations": [
                "P values describe 13 plots under exchangeability assumptions; observations share three ranches.",
                "Stock denominator includes live seedlings and vegetative plants, not known reproductive mothers.",
                "Remaining missing observations cannot be treated as deaths or survivors without assumptions.",
                "Survival among known states is conditional on being located again, not a full survival estimator.",
                "No inference of fragmentation causality or population-growth lambda.",
                "Prior publications analysed recruitment, stage-specific lambda and delayed climate effects in this system.",
                "This source remains outside all frozen EGWEE meta-analysis denominators.",
            ]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, help="Use local upstream CSVs instead of pinned download")
    parser.add_argument("--output", type=Path, help="Write full JSON output to this path")
    args = parser.parse_args()
    result = run(args.source_dir)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    d = result["plot_mean_summaries"]
    print("HELICONIA_COHORT_AUDIT: PASS")
    print(f"13 plots / 2590 cohort seedlings; source checksum verified; 116/222 missing later found alive")
    for key in ("annual_new_seedlings", "new_per_100_prior_alive",
                "next_year_known_state_alive_fraction", "next_year_unknown_fraction"):
        z = d[key]
        print(f"{key}: CF={z['continuous']:.5f} FF={z['fragment']:.5f} "
              f"diff={z['fragment_minus_continuous']:.5f} "
              f"p_exact={z['unblocked']['two_sided_permutation_p']:.5f} "
              f"p_ranch={z['ranch_blocked']['two_sided_permutation_p']:.5f}")
    print("survival_bounds:", result["worst_case_missing_survival_difference_bounds"])


if __name__ == "__main__":
    main()
