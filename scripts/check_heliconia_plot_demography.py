"""Plot-level reanalysis of published Heliconia individual-by-year census.

Exploratory, post-outcome audit. Not part of the frozen EGWEE primary meta-analysis.
Uses the archived public CSV with a Git-blob hash guard, no extra Python packages.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import itertools
import json
import statistics
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = "https://raw.githubusercontent.com/BrunaLab/HeliconiaSurveys/master/data/survey_archive/"
EXPECTED_BLOBS = {
    "HDP_survey.csv": "f82a6f241493a979a2923d1c5deef6a1be0ff3ed",
    "HDP_plots.csv": "6fc835fb870d8c43ae4a4fcf04d515f419e6db22",
}
YEARS = range(1999, 2006)  # 2000–2006 are complete subsequent censuses in 13 plots


def load(filename: str, local_dir: Path | None) -> list[dict[str, str]]:
    if local_dir is None:
        request = urllib.request.Request(ROOT + filename, headers={"User-Agent": "egwee-research-audit"})
        with urllib.request.urlopen(request, timeout=45) as response:
            raw = response.read()
    else:
        raw = (local_dir / filename).read_bytes()
    blob = hashlib.sha1(f"blob {len(raw)}".encode("ascii") + bytes([0]) + raw).hexdigest()
    assert blob == EXPECTED_BLOBS[filename], (filename, blob, "source changed; stop")
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))


def avg(x: list[float]) -> float:
    return statistics.mean(x)


def test_exact(plots: list[dict], key: str, mode: str) -> dict:
    obs = avg([p[key] for p in plots if p["fragment"]]) - avg([p[key] for p in plots if not p["fragment"]])
    if mode == "unrestricted":
        sets = itertools.combinations([p["plot"] for p in plots], 7)
    else:
        strata = []
        for ranch in sorted({p["ranch"] for p in plots}):
            names = [p["plot"] for p in plots if p["ranch"] == ranch]
            k = sum(p["fragment"] for p in plots if p["ranch"] == ranch)
            strata.append(list(itertools.combinations(names, k)))
        sets = (tuple(itertools.chain.from_iterable(groups)) for groups in itertools.product(*strata))
    n, extreme = 0, 0
    for choice in sets:
        group = set(choice)
        d = avg([p[key] for p in plots if p["plot"] in group]) - avg(
            [p[key] for p in plots if p["plot"] not in group]
        )
        n += 1
        extreme += abs(d) >= abs(obs) - 1e-12
    assert n == (1716 if mode == "unrestricted" else 240)
    return {"difference_FF_minus_CF": obs, "p_two_sided": extreme / n,
            "extreme_assignments": extreme, "assignments": n}


def compare_ranch_estimands(plots: list[dict], key: str) -> dict:
    """Sensitivity to which *statistic* is used with ranch-stratified labels.

    The global unequal-composition contrast can have a nonzero permutation
    expectation despite fixed labels per ranch. Compare its centered tail
    against truly within-ranch standardized contrasts.
    """
    ranches = sorted({p["ranch"] for p in plots})
    strata = []
    for ranch in ranches:
        group = [p for p in plots if p["ranch"] == ranch]
        k = sum(p["fragment"] for p in group)
        assert 0 < k < len(group), ("no common ranch contrast", ranch)
        strata.append(list(itertools.combinations([p["plot"] for p in group], k)))
    assignments = [
        set(itertools.chain.from_iterable(parts))
        for parts in itertools.product(*strata)
    ]
    assert len(assignments) == 240

    def mean_gap(choice: set[str], rows: list[dict]) -> float:
        ff = [row[key] for row in rows if row["plot"] in choice]
        cf = [row[key] for row in rows if row["plot"] not in choice]
        return avg(ff) - avg(cf)

    def statistic(choice: set[str], mode: str) -> float:
        if mode == "global":
            return mean_gap(choice, plots)
        pairs = [(len(rows), mean_gap(choice, rows))
                 for ranch in ranches
                 for rows in [[p for p in plots if p["ranch"] == ranch]]]
        if mode == "ranch_equal":
            return avg([d for _, d in pairs])
        assert mode == "ranch_size"
        return sum(n * d for n, d in pairs) / len(plots)

    actual = {p["plot"] for p in plots if p["fragment"]}
    result = {}
    for mode in ("global", "ranch_equal", "ranch_size"):
        obs = statistic(actual, mode)
        null = [statistic(a, mode) for a in assignments]
        center = avg(null)
        extreme = sum(abs(v - center) >= abs(obs - center) - 1e-12 for v in null)
        result[mode] = {
            "observed_difference": obs,
            "randomization_mean": center,
            "p_centered_two_sided": extreme / len(null),
            "assignments": len(null),
        }
    assert abs(result["ranch_equal"]["randomization_mean"]) < 1e-12
    assert abs(result["ranch_size"]["randomization_mean"]) < 1e-12
    return result


def analyze(survey: list[dict], plotmeta: list[dict]) -> dict:
    meta = {p["plot_id"]: p for p in plotmeta}
    assert len(meta) == 13
    assert sum(p["habitat"] == "forest" for p in plotmeta) == 6
    annual = defaultdict(lambda: {"alive": 0, "born": 0})
    individuals = defaultdict(dict)
    births = {}
    keys = set()
    for r in survey:
        p, year, pid = r["plot_id"], int(r["year"]), r["plant_id"]
        assert p in meta
        key = (p, pid, year)
        assert key not in keys, ("duplicate plant-year", key)
        keys.add(key)
        assert r["census_status"] in ("measured", "dead", "missing")
        is_new = r["recorded_sdlg"] == "TRUE"
        assert r["recorded_sdlg"] in ("TRUE", "FALSE")
        annual[(p, year)]["alive"] += (r["census_status"] == "measured")
        annual[(p, year)]["born"] += is_new
        individuals[(p, pid)][year] = r["census_status"]
        if is_new:
            assert r["census_status"] == "measured"
            assert (p, pid) not in births
            births[(p, pid)] = year

    assert len(survey) == 66396 and len(individuals) == 8586 and len(births) == 3464
    by_plot = []
    for plot in sorted(meta):
        for year in range(1998, 2007):
            assert (plot, year) in annual, ("missing baseline/follow-up census", plot, year)
        born = sum(annual[(plot, year)]["born"] for year in YEARS)
        lagstock = sum(annual[(plot, year - 1)]["alive"] for year in YEARS)
        known_alive = known_dead = missing = 0
        for (p, pid), b in births.items():
            if p != plot or b not in YEARS:
                continue
            status = individuals[(p, pid)].get(b + 1)
            assert status is not None, ("unexpected absent next-year record", p, pid, b)
            known_alive += status == "measured"
            known_dead += status == "dead"
            missing += status == "missing"
        assert born == known_alive + known_dead + missing
        group = meta[plot]["habitat"]
        by_plot.append({
            "plot": plot, "ranch": meta[plot]["ranch"],
            "fragment": group != "forest", "habitat": group, "new_seedlings": born,
            "lagged_individual_years": lagstock,
            "new_per_plot_year": born / len(YEARS),
            "new_per_100_lagged_individual_years": 100 * born / lagstock,
            "next_alive": known_alive, "next_dead": known_dead, "next_missing": missing,
            "survival_known": known_alive / (known_alive + known_dead),
            "survival_lower": known_alive / born,
            "survival_upper": (known_alive + missing) / born,
            "missing_fraction": missing / born,
        })

    assert sum(p["new_seedlings"] for p in by_plot) == 2590
    # Use only 1999–2004 entrants for a common *second* follow-up across
    # all 13 plots (2001–2006); 2007 is not observed in every fragment.
    # Direct evidence that the intervening 'missing' status is not death:
    recovery_plot = {
        row["plot"]: {"plot": row["plot"], "ranch": row["ranch"],
                      "fragment": row["fragment"], "cohort": 0,
                      "alive_at_plus1": 0, "reappeared_at_plus2": 0}
        for row in by_plot
    }
    reappearance = {"CF": {"cohort": 0, "missing_next": 0, "alive_plus2": 0,
                           "dead_plus2": 0, "missing_plus2": 0},
                    "FF": {"cohort": 0, "missing_next": 0, "alive_plus2": 0,
                           "dead_plus2": 0, "missing_plus2": 0}}
    for (p, pid), b in births.items():
        if b < 1999 or b > 2004:
            continue
        group = "CF" if meta[p]["habitat"] == "forest" else "FF"
        rec = reappearance[group]
        rec["cohort"] += 1
        row = recovery_plot[p]
        row["cohort"] += 1
        if individuals[(p, pid)].get(b + 1) == "measured":
            row["alive_at_plus1"] += 1
        if individuals[(p, pid)].get(b + 1) == "missing":
            rec["missing_next"] += 1
            plus2 = individuals[(p, pid)].get(b + 2)
            assert plus2 in ("measured", "dead", "missing"), (p, pid, b, plus2)
            rec[{"measured": "alive_plus2", "dead": "dead_plus2",
                 "missing": "missing_plus2"}[plus2]] += 1
            if plus2 == "measured":
                row["reappeared_at_plus2"] += 1
    assert reappearance["CF"] == {
        "cohort": 1437, "missing_next": 146, "alive_plus2": 81,
        "dead_plus2": 22, "missing_plus2": 43}
    assert reappearance["FF"] == {
        "cohort": 932, "missing_next": 64, "alive_plus2": 19,
        "dead_plus2": 10, "missing_plus2": 35}

    for row in recovery_plot.values():
        row["missing_as_death_lower"] = row["alive_at_plus1"] / row["cohort"]
        row["recovery_confirmed_lower"] = (
            row["alive_at_plus1"] + row["reappeared_at_plus2"]
        ) / row["cohort"]
    survival_lower_sensitivity = {}
    for field in ("missing_as_death_lower", "recovery_confirmed_lower"):
        survival_lower_sensitivity[field] = {
            "means": {
                "CF": avg([r[field] for r in recovery_plot.values() if not r["fragment"]]),
                "FF": avg([r[field] for r in recovery_plot.values() if r["fragment"]]),
            },
            "unrestricted": test_exact(list(recovery_plot.values()), field, "unrestricted"),
            "ranch_restricted": test_exact(list(recovery_plot.values()), field, "ranch"),
        }
    assert abs(survival_lower_sensitivity["missing_as_death_lower"]["unrestricted"]["p_two_sided"] - 85 / 1716) < 1e-12
    assert abs(survival_lower_sensitivity["recovery_confirmed_lower"]["unrestricted"]["p_two_sided"] - 391 / 1716) < 1e-12
    assert abs(survival_lower_sensitivity["missing_as_death_lower"]["ranch_restricted"]["p_two_sided"] - 5 / 240) < 1e-12
    assert abs(survival_lower_sensitivity["recovery_confirmed_lower"]["ranch_restricted"]["p_two_sided"] - 38 / 240) < 1e-12
    fields = ("new_per_plot_year", "new_per_100_lagged_individual_years",
              "survival_known", "survival_lower", "survival_upper", "missing_fraction")
    tests = {}
    for key in fields:
        tests[key] = {
            "means": {
                "CF": avg([p[key] for p in by_plot if not p["fragment"]]),
                "FF": avg([p[key] for p in by_plot if p["fragment"]]),
            },
            "unrestricted": test_exact(by_plot, key, "unrestricted"),
            "ranch_restricted": test_exact(by_plot, key, "ranch"),
            "ranch_estimand_sensitivity": compare_ranch_estimands(by_plot, key),
        }
    # Ranch-conditional assignments are composition-unbalanced. An
    # uncentered global difference can have a nonzero permutation mean.
    # These are post hoc diagnostic statistics, not randomized causal tests.
    assert abs(tests["new_per_plot_year"]["ranch_estimand_sensitivity"]
               ["global"]["randomization_mean"] + 9.794897959183668) < 1e-9
    assert abs(tests["new_per_plot_year"]["ranch_estimand_sensitivity"]
               ["global"]["p_centered_two_sided"] - 115 / 240) < 1e-12
    assert abs(tests["new_per_plot_year"]["ranch_estimand_sensitivity"]
               ["ranch_equal"]["p_centered_two_sided"] - 148 / 240) < 1e-12
    assert abs(tests["new_per_plot_year"]["ranch_estimand_sensitivity"]
               ["ranch_size"]["p_centered_two_sided"] - 120 / 240) < 1e-12
    assert abs(tests["new_per_100_lagged_individual_years"]
               ["ranch_estimand_sensitivity"]["global"]
               ["p_centered_two_sided"] - 109 / 240) < 1e-12
    # 1-ha vs 10-ha remnants: all census plots still cover 0.5 ha.
    ff_one = [p for p in by_plot if p["habitat"] == "one"]
    ff_ten = [p for p in by_plot if p["habitat"] == "ten"]
    assert len(ff_one) == 4 and len(ff_ten) == 3
    observed_size = avg([p["new_per_plot_year"] for p in ff_one]) - avg(
        [p["new_per_plot_year"] for p in ff_ten]
    )
    n_size = extreme_size = 0
    for subset in itertools.combinations([p["plot"] for p in by_plot if p["fragment"]], 4):
        selected = set(subset)
        first = [p["new_per_plot_year"] for p in by_plot if p["plot"] in selected]
        second = [p["new_per_plot_year"] for p in by_plot if p["fragment"] and p["plot"] not in selected]
        n_size += 1
        extreme_size += abs(avg(first) - avg(second)) >= abs(observed_size) - 1e-12
    assert n_size == 35 and extreme_size == 3
    size_test = {"one_ha_mean": avg([p["new_per_plot_year"] for p in ff_one]),
                 "ten_ha_mean": avg([p["new_per_plot_year"] for p in ff_ten]),
                 "difference": observed_size, "p": extreme_size / n_size,
                 "assignments": n_size}

    # A low p for recruitment conditional on post-exposure standing stock is NOT
    # a causal estimate; record sensitivity to one entire site being removed.
    leave_one_out = {}
    for key in ("new_per_plot_year", "new_per_100_lagged_individual_years"):
        full = tests[key]["unrestricted"]["difference_FF_minus_CF"]
        omissions = {}
        for omitted in by_plot:
            survivors = [p for p in by_plot if p["plot"] != omitted["plot"]]
            d = avg([p[key] for p in survivors if p["fragment"]]) - avg(
                [p[key] for p in survivors if not p["fragment"]]
            )
            omissions[omitted["plot"]] = d
        leave_one_out[key] = {
            "min_difference": min(omissions.values()),
            "max_difference": max(omissions.values()),
            "sign_flips": [plot for plot, d in omissions.items() if d * full < 0],
        }
    assert not leave_one_out["new_per_plot_year"]["sign_flips"]
    assert len(leave_one_out["new_per_100_lagged_individual_years"]["sign_flips"]) == 6
    assert abs(tests["new_per_plot_year"]["unrestricted"]["p_two_sided"] - 454 / 1716) < 1e-12
    assert abs(tests["new_per_100_lagged_individual_years"]["unrestricted"]["p_two_sided"] - 1659 / 1716) < 1e-12
    assert abs(tests["survival_known"]["unrestricted"]["p_two_sided"] - 1123 / 1716) < 1e-12
    assert abs(tests["new_per_plot_year"]["ranch_restricted"]["p_two_sided"] - 57 / 240) < 1e-12
    return {
        "data": "BrunaLab/HeliconiaSurveys master, Git blobs pinned",
        "status": "post_hoc_exploratory_not_primary",
        "rows": len(survey), "individuals": len(individuals), "all_seedlings": len(births),
        "eligible_seedlings": 2590, "plots_CF": 6, "plots_FF": 7,
        "years": "1999-2005 first observed seedlings, 2000-2006 next census",
        "disclaimer": "New seedlings are detected individuals, not seed germination probability. "
                      "Normalization conditions on potentially fragmentation-affected standing stock. "
                      "Missing is NOT death; groups are unbalanced by ranch.",
        "tests": tests, "fragment_size_exploratory": size_test,
        "leave_one_plot_out": leave_one_out, "missing_return_at_plus2": reappearance,
        "recovered_survival_lower_bounds": survival_lower_sensitivity,
        "recovery_plot_data": list(recovery_plot.values()),
        "plot_data": by_plot,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-dir", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    result = analyze(load("HDP_survey.csv", args.local_dir), load("HDP_plots.csv", args.local_dir))
    dump = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(dump, encoding="utf-8")
    print("HELICONIA_PLOT_DEMOGRAPHY: PASS")
    for key, t in result["tests"].items():
        print(f"{key}: CF={t['means']['CF']:.6f} FF={t['means']['FF']:.6f} "
              f"p={t['unrestricted']['p_two_sided']:.6f} "
              f"p_ranch={t['ranch_restricted']['p_two_sided']:.6f}")


if __name__ == "__main__":
    main()
