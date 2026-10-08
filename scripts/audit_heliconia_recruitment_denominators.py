#!/usr/bin/env python3
"""Post-hoc audit of external Heliconia recruitment, with plot as the replicate.

Reproducibility: upstream GitHub blob SHAs are pinned and checked after download.
This is neither a preregistered fragmentation-effect test nor a new EGWEE cluster.
"""
from __future__ import annotations

import csv
import hashlib
import io
import itertools
import json
import pathlib
import urllib.request
from collections import defaultdict

BASE = "https://raw.githubusercontent.com/BrunaLab/HeliconiaSurveys/master/data/survey_archive/"
FILES = {
    "HDP_survey.csv": "f82a6f241493a979a2923d1c5deef6a1be0ff3ed",
    "HDP_plots.csv": "6fc835fb870d8c43ae4a4fcf04d515f419e6db22",
}
YEARS = range(1999, 2006)  # matched, complete t to t+1 coverage through 2006


def load_csv(filename: str) -> list[dict[str, str]]:
    cache = pathlib.Path(__file__).parents[1] / "data" / "external_raw" / filename
    if cache.exists():
        data = cache.read_bytes()
    else:
        req = urllib.request.Request(BASE + filename, headers={"User-Agent": "egwee-source-hash-audit"})
        with urllib.request.urlopen(req, timeout=40) as res:
            data = res.read()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert actual == FILES[filename], (filename, "upstream_source_changed", actual)
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))


def exact_plot_permutation(values: list[float], is_fragment: list[bool]) -> dict:
    """Two-sided exhaustive label permutation; exploratory, not randomized causal inference."""
    n = len(values)
    k = sum(is_fragment)
    total = sum(values)
    frag_sum = sum(v for v, flag in zip(values, is_fragment) if flag)
    observed = frag_sum / k - (total - frag_sum) / (n - k)
    count = extreme = 0
    for inds in itertools.combinations(range(n), k):
        frag = sum(values[i] for i in inds)
        delta = frag / k - (total - frag) / (n - k)
        count += 1
        extreme += abs(delta) >= abs(observed) - 1e-12
    assert count == 1716, count  # 13 choose 7
    return {"difference_fragment_minus_forest": observed, "two_sided_p": extreme / count, "permutations": count}


def main() -> None:
    metadata = {r["plot_id"]: r for r in load_csv("HDP_plots.csv")}
    plots = {p: r["habitat"] for p, r in metadata.items()}
    assert len(plots) == 13
    survey = load_csv("HDP_survey.csv")
    assert len(survey) == 66396
    observed = {}
    new_year = {}
    per_year = defaultdict(lambda: {"new": 0, "measured": 0})
    for row in survey:
        plot, plant, year = row["plot_id"], row["plant_id"], int(row["year"])
        status = row["census_status"]
        assert plot in plots and status in ("measured", "dead", "missing")
        key = (plot, plant, year)
        assert key not in observed, ("duplicate_plant_year", key)
        observed[key] = status
        per_year[(plot, year)]["measured"] += status == "measured"
        if row["recorded_sdlg"] == "TRUE":
            assert status == "measured"
            assert (plot, plant) not in new_year
            new_year[(plot, plant)] = year
            per_year[(plot, year)]["new"] += 1
    assert len(new_year) == 3464
    assert len({(p, z) for p, z, _ in observed}) == 8586

    out = []
    for plot in sorted(plots):
        group = plots[plot]
        assert group in ("forest", "one", "ten")
        nnew = sum(per_year[(plot, y)]["new"] for y in YEARS)
        nmeasured = sum(per_year[(plot, y)]["measured"] for y in YEARS)
        assert all((plot, y) in per_year for y in range(1998, 2007))
        alive = dead = missing = late_return = 0
        for (p, plant), year in new_year.items():
            if p != plot or year not in YEARS:
                continue
            state = observed.get((p, plant, year + 1))
            assert state in ("measured", "dead", "missing"), (plot, plant, year)
            alive += state == "measured"
            dead += state == "dead"
            missing += state == "missing"
            if state == "missing":
                # Return is an *observed* lower bound; follow-up is not even after 2006.
                late_return += any(observed.get((p, plant, later)) == "measured"
                                   for later in range(year + 2, 2010))
        assert nnew == alive + dead + missing
        out.append({
            "plot": plot, "habitat": group, "ranch": metadata[plot]["ranch"],
            "initial_measured_1998": per_year[(plot, 1998)]["measured"], "new_cohort": nnew,
            "mean_new_per_year": nnew / len(YEARS),
            "mean_measured_per_year": nmeasured / len(YEARS),
            # This is NOT fecundity; measured standing stock includes new seedlings.
            "new_per_measured_stock": nnew / nmeasured,
            "alive_next": alive, "dead_next": dead, "missing_next": missing,
            "known_status_survival": alive / (alive + dead),
            "survival_lower_bound": alive / nnew,
            "survival_upper_bound": (alive + missing) / nnew,
            "later_reappeared_after_missing": late_return,
        })
    groups = {}
    for name in ("forest", "fragment", "one", "ten"):
        members = [r for r in out if (r["habitat"] != "forest") == (name == "fragment")]
        if name in ("forest", "one", "ten"):
            members = [r for r in out if r["habitat"] == name]
        if not members:
            continue
        groups[name] = {
            "n_plots": len(members),
            "mean_new_per_plot_year": sum(r["mean_new_per_year"] for r in members) / len(members),
            "mean_plot_new_per_stock": sum(r["new_per_measured_stock"] for r in members) / len(members),
            "known_next_survival_pooled": sum(r["alive_next"] for r in members) /
                 sum(r["alive_next"] + r["dead_next"] for r in members),
            "missing_next": sum(r["missing_next"] for r in members),
            "reappeared_after_missing": sum(r["later_reappeared_after_missing"] for r in members),
            "cohort_n": sum(r["new_cohort"] for r in members),
        }
    assert groups["forest"]["n_plots"] == 6 and groups["fragment"]["n_plots"] == 7
    assert groups["one"]["n_plots"] == 4 and groups["ten"]["n_plots"] == 3
    flag = [r["habitat"] != "forest" for r in out]
    permutation = {
        "absolute_new_per_plot_year": exact_plot_permutation([r["mean_new_per_year"] for r in out], flag),
        "new_per_measured_stock": exact_plot_permutation([r["new_per_measured_stock"] for r in out], flag),
        "survival_conditional_on_known": exact_plot_permutation([r["known_status_survival"] for r in out], flag),
    }
    assert abs(permutation["absolute_new_per_plot_year"]["two_sided_p"] - 0.26456876456876455) < 1e-12
    assert abs(permutation["new_per_measured_stock"]["two_sided_p"] - 0.837995337995338) < 1e-12
    assert (groups["forest"]["missing_next"], groups["fragment"]["missing_next"]) == (151, 71)
    assert (groups["forest"]["reappeared_after_missing"], groups["fragment"]["reappeared_after_missing"]) == (91, 25)

    result = {
        "status": "POST_HOC_NOT_PRIMARY_CORPUS",
        "source": "BrunaLab/HeliconiaSurveys data/survey_archive",
        "source_blob_sha": FILES, "cohort_years": [min(YEARS), max(YEARS)],
        "replicate": "independent_0_5ha_plot", "n_plots": 13, "n_record_rows": len(survey),
        "n_distinct_plants": len({(p, z) for p, z, _ in observed}),
        "groups": groups, "permutation": permutation,
        "cautions": [
            "Plot labels are not a randomized fragmentation experiment for this post hoc contrast",
            "New seedlings / standing stock is NOT per-adult fecundity or per-seed germination",
            "Known-status survival conditions on detection: missing does not equal dead",
            "Later reappearance has unequal follow-up horizons and does not identify detection probability",
            "Never treat 66396 plant-years or 3464 seedlings as independent landscape replicates",
            "No inference about causal stage-specific intervention leverage or unique novelty",
        ],
    }
    output = pathlib.Path(__file__).parents[1] / "build" / "heliconia_external_audit"
    output.mkdir(parents=True, exist_ok=True)
    (output / "summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    with (output / "per_plot.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    print("HELICONIA_RECRUITMENT_AUDIT: PASS " + json.dumps({
        "n_plots": 13, "recruits_1999_2005": sum(r["new_cohort"] for r in out),
        "new_absolute_permutation_p": permutation["absolute_new_per_plot_year"]["two_sided_p"],
        "new_stock_normalized_permutation_p": permutation["new_per_measured_stock"]["two_sided_p"],
        "missing_next": {g: groups[g]["missing_next"] for g in ("forest", "fragment")}
    }))


if __name__ == "__main__":
    main()
