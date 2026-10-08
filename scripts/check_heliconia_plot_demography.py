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
import math
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
    blob = hashlib.sha1(f"blob {len(raw)}\\0".encode().replace(b"\\0", b"\0") + raw).hexdigest()
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
        }
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
        "tests": tests, "plot_data": by_plot,
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
