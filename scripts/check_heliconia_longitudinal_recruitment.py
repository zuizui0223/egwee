"""Independent-plot audit of Bruna Lab's public Heliconia demographic archive.

This analysis is exploratory and does not augment any EGWEE primary denominator.
Run from repo root: python scripts/check_heliconia_longitudinal_recruitment.py
Network download is SHA-gated; use --source PATH to work offline with the same file.
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

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REPO = "BrunaLab/HeliconiaSurveys"
SOURCE_COMMIT = "830f9092f1a6906c66455f6c4dd916c0160d2fbc"
SOURCE_BLOB = "f82a6f241493a979a2923d1c5deef6a1be0ff3ed"
PLOTS_BLOB = "6fc835fb870d8c43ae4a4fcf04d515f419e6db22"
SRC_ROOT = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}/data/survey_archive"
LOCKED = ROOT / "evidence/meta_extraction/heliconia_cohort_1999_2005_plot_v1.csv"


def read_verified(source: str | None, name: str, sha: str) -> list[dict[str, str]]:
    if source:
        path = Path(source) if name == "HDP_survey.csv" else Path(source).with_name(name)
        data = path.read_bytes()
    else:
        with urlopen(f"{SRC_ROOT}/{name}", timeout=90) as response:
            data = response.read()
    actual_sha = hashlib.sha1(f"blob {len(data)}\\0".encode() + data).hexdigest()
    assert actual_sha == sha, (name, actual_sha, sha)
    return list(csv.DictReader(io.StringIO(data.decode("utf-8"), newline="")))


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def blocked_permutation(plot_rows: list[dict], metric: str) -> dict:
    blocks = []
    for ranch in sorted({row["ranch"] for row in plot_rows}):
        ids = [i for i, row in enumerate(plot_rows) if row["ranch"] == ranch]
        n_ref = sum(plot_rows[i]["habitat"] == "continuous" for i in ids)
        blocks.append(list(itertools.combinations(ids, n_ref)))
    observed = mean([r[metric] for r in plot_rows if r["habitat"] == "fragment"]) - mean(
        [r[metric] for r in plot_rows if r["habitat"] == "continuous"]
    )
    total = sum(r[metric] for r in plot_rows)
    extreme = 0
    count = 0
    for choice in itertools.product(*blocks):
        refs = {idx for block in choice for idx in block}
        ref_total = sum(plot_rows[i][metric] for i in refs)
        diff = (total - ref_total) / 7 - ref_total / 6
        extreme += abs(diff) >= abs(observed) - 1e-12
        count += 1
    assert count == 240
    return {"fragment_minus_continuous": observed, "exact_two_sided_p": extreme / count,
            "extreme_assignments": extreme, "permutations": count}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="Optional local HDP_survey.csv; neighboring HDP_plots.csv required")
    args = parser.parse_args()
    records = read_verified(args.source, "HDP_survey.csv", SOURCE_BLOB)
    plots = read_verified(args.source, "HDP_plots.csv", PLOTS_BLOB)
    assert len(records) == 66396
    assert len(plots) == 13
    meta = {
        p["plot_id"]: {"ranch": p["ranch"], "habitat": "continuous" if p["habitat"] == "forest" else "fragment"}
        for p in plots
    }
    assert sum(v["habitat"] == "continuous" for v in meta.values()) == 6
    assert sum(v["habitat"] == "fragment" for v in meta.values()) == 7

    individuals: dict[tuple[str, str], dict[int, dict[str, str]]] = defaultdict(dict)
    new_first: dict[tuple[str, str], int] = {}
    plots_yr: dict[tuple[str, int], dict] = defaultdict(
        lambda: {"measured_plant_years": 0, "flowering_plant_years": 0, "new_seedlings": 0}
    )
    states = {"measured", "dead", "missing"}
    for r in records:
        site, plant, year = r["plot_id"], r["plant_id"], int(r["year"])
        assert site in meta and 1998 <= year <= 2009
        assert r["census_status"] in states
        key = (site, plant)
        assert year not in individuals[key], (site, plant, year)
        individuals[key][year] = r
        siteyear = plots_yr[(site, year)]
        siteyear["measured_plant_years"] += r["census_status"] == "measured"
        siteyear["flowering_plant_years"] += r["infl"] not in ("", "NA")
        if r["recorded_sdlg"] == "TRUE":
            assert key not in new_first, key
            assert r["census_status"] == "measured"
            new_first[key] = year
            siteyear["new_seedlings"] += 1
        else:
            assert r["recorded_sdlg"] == "FALSE"
    assert len(individuals) == 8586 and len(new_first) == 3464
    assert all(min(individuals[key]) == year for key, year in new_first.items())
    # An identical annual census window is available for 1999-2005 cohorts.
    assert all((site, year) in plots_yr for site in meta for year in range(1999, 2007))

    result = {site: dict(meta[site], plot_id=site, cohort_year_start=1999, cohort_year_end=2005,
                         new_seedlings=0, measured_plant_years=0, flowering_plant_years=0,
                         following_year_measured=0, following_year_dead=0, following_year_missing=0)
              for site in meta}
    for site in meta:
        for year in range(1999, 2006):
            x = plots_yr[(site, year)]
            for field in ("measured_plant_years", "flowering_plant_years", "new_seedlings"):
                result[site][field] += x[field]

    missing_resighted = defaultdict(lambda: {"missing": 0, "reappeared_measured_yplus2": 0,
                                              "subsequently_unobserved_yplus2": 0})
    for key, year in new_first.items():
        site = key[0]
        if not 1999 <= year <= 2005:
            continue
        next_observation = individuals[key].get(year + 1)
        assert next_observation is not None, (key, year, "missing row")
        state = next_observation["census_status"]
        result[site][{"measured": "following_year_measured",
                      "dead": "following_year_dead",
                      "missing": "following_year_missing"}[state]] += 1
        if state == "missing":
            stat = missing_resighted[meta[site]["habitat"]]
            stat["missing"] += 1
            if (site, year + 2) not in plots_yr:
                stat["subsequently_unobserved_yplus2"] += 1
            elif individuals[key].get(year + 2, {}).get("census_status") == "measured":
                stat["reappeared_measured_yplus2"] += 1

    expected = list(csv.DictReader(LOCKED.open(encoding="utf-8", newline="")))
    assert len(expected) == 13
    for e in expected:
        computed = result[e["plot_id"]]
        for k, value in e.items():
            if k in ("plot_id", "ranch", "habitat"):
                assert str(computed[k]) == value, (e["plot_id"], k)
            else:
                assert computed[k] == int(value), (e["plot_id"], k, computed[k], value)

    plot_rows = []
    for site, v in sorted(result.items()):
        n = v["new_seedlings"]
        alive, dead, missing = (v["following_year_" + x] for x in ("measured", "dead", "missing"))
        assert alive + dead + missing == n
        plot_rows.append(dict(v, recruitment_per_year=n / 7,
                              entry_per_100_measured=100 * n / v["measured_plant_years"],
                              detected_survival=alive / (alive + dead),
                              alive_fraction_if_missing_naively_dead=alive / n,
                              missing_fraction=missing / n))
    checks = {metric: blocked_permutation(plot_rows, metric) for metric in (
        "recruitment_per_year", "entry_per_100_measured", "detected_survival",
        "alive_fraction_if_missing_naively_dead", "missing_fraction"
    )}
    assert sum(p["new_seedlings"] for p in plot_rows) == 2590
    assert sum(p["following_year_missing"] for p in plot_rows) == 222
    assert missing_resighted["continuous"]["reappeared_measured_yplus2"] == 83
    assert missing_resighted["fragment"]["reappeared_measured_yplus2"] == 19
    assert abs(checks["recruitment_per_year"]["exact_two_sided_p"] - .2375) < 1e-12
    assert abs(checks["entry_per_100_measured"]["exact_two_sided_p"] - (191 / 240)) < 1e-12
    assert abs(checks["detected_survival"]["exact_two_sided_p"] - (136 / 240)) < 1e-12

    group_means = {
        group: {metric: mean([p[metric] for p in plot_rows if p["habitat"] == group])
                for metric in checks}
        for group in ("continuous", "fragment")
    }
    report = {"source": f"{SOURCE_REPO}@{SOURCE_COMMIT}", "source_blob": SOURCE_BLOB,
              "n_rows": len(records), "n_individuals": len(individuals), "n_plots": len(plots),
              "cohort_years": "1999-2005", "n_eligible_seedlings": 2590,
              "plot_unit_group_means": group_means, "ranch_stratified_exact_tests": checks,
              "missing_then_reappeared": dict(missing_resighted),
              "interpretation": "Exploratory source audit only; no fragmentation causal effect or publication novelty certified. Missing != dead.",
              "meta_analysis_denominator_added": 0}
    print("HELICONIA_LONGITUDINAL_RECRUITMENT: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
