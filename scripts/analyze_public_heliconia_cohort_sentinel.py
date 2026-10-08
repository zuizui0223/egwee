"""Exploratory, plot-first diagnostic of public BrunaLab Heliconia census.

Input provenance: https://github.com/BrunaLab/HeliconiaSurveys
data/survey_archive/HDP_survey.csv and HDP_plots.csv;
2023 Dryad https://doi.org/10.5061/dryad.stqjq2c8d

No reclassification of the frozen EGWEE effect-size evidence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

EXPECTED_BLOB = "f82a6f241493a979a2923d1c5deef6a1be0ff3ed"


def blob_sha(contents: bytes) -> str:
    return hashlib.sha1(f"blob {len(contents)}\0".encode() + contents).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--survey", type=Path, required=True)
    ap.add_argument("--plots", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    source_bytes = args.survey.read_bytes()
    assert blob_sha(source_bytes) == EXPECTED_BLOB, (
        "Survey blob changed; inspect versions and update provenance separately"
    )
    rows = read_csv(args.survey)
    plots = {r["plot_id"]: r for r in read_csv(args.plots)}
    assert len(rows) == 66396 and len(plots) == 13

    index: dict[tuple[str, str, int], dict[str, str]] = {}
    totals: dict[str, dict[str, object]] = {}
    for r in rows:
        p, y, pid = r["plot_id"], int(r["year"]), r["plant_id"]
        assert p in plots
        key = (p, pid, y)
        assert key not in index, "Do not duplicate plant-year observations"
        index[key] = r
        if p not in totals:
            totals[p] = {
                "plot_id": p,
                "habitat": plots[p]["habitat"],
                "ranch": plots[p]["ranch"],
                "years": set(),
                "new_seedlings": 0,
                "alive_1998": 0,
                "new_known_alive_next": 0,
                "new_known_dead_next": 0,
                "new_missing_next": 0,
                "new_no_next_record": 0,
                "baseline_known_alive_next": 0,
                "baseline_known_dead_next": 0,
            }
        t = totals[p]
        t["years"].add(y)
        t["new_seedlings"] += int(r["recorded_sdlg"] == "TRUE")
        if y == 1998 and r["census_status"] == "measured":
            t["alive_1998"] += 1

    def observe(t: dict[str, object], prefix: str, nxt: dict[str, str] | None) -> None:
        if nxt is None:
            if prefix == "new":
                t["new_no_next_record"] += 1
            return
        state = nxt["census_status"]
        if state == "measured":
            t[f"{prefix}_known_alive_next"] += 1
        elif state == "dead":
            t[f"{prefix}_known_dead_next"] += 1
        elif state == "missing" and prefix == "new":
            t["new_missing_next"] += 1
        else:
            assert state == "missing", f"Unknown census status {state!r}"

    for r in rows:
        if r["census_status"] != "measured":
            continue
        p, y, pid = r["plot_id"], int(r["year"]), r["plant_id"]
        nxt = index.get((p, pid, y + 1))
        t = totals[p]
        if r["recorded_sdlg"] == "TRUE":
            observe(t, "new", nxt)
        if y == 1998:
            observe(t, "baseline", nxt)

    output = []
    for p, t in sorted(totals.items()):
        survey_years = len([y for y in t["years"] if y > 1998])
        assert survey_years > 0 and t["alive_1998"] > 0
        known = t["new_known_alive_next"] + t["new_known_dead_next"]
        assert known > 0
        base_known = t["baseline_known_alive_next"] + t["baseline_known_dead_next"]
        output.append({
            "plot_id": p, "habitat": t["habitat"], "ranch": t["ranch"],
            "observed_postbaseline_years": survey_years,
            "baseline_alive_1998": t["alive_1998"],
            "new_seedling_entries": t["new_seedlings"],
            "entries_per_plot_year": round(t["new_seedlings"] / survey_years, 6),
            "entries_per_100_baseline_alive_per_year": round(
                100 * t["new_seedlings"] / (t["alive_1998"] * survey_years), 6
            ),
            "year1_seed_alive": t["new_known_alive_next"],
            "year1_seed_dead": t["new_known_dead_next"],
            "year1_seed_missing": t["new_missing_next"],
            "year1_seed_no_next_record": t["new_no_next_record"],
            "year1_seed_survival_given_known_status": round(
                t["new_known_alive_next"] / known, 6
            ),
            "year1_seed_survival_if_missing_are_failures": round(
                t["new_known_alive_next"] / (known + t["new_missing_next"]), 6
            ),
            "baseline_1998_year1_survival_given_known_status": round(
                t["baseline_known_alive_next"] / base_known, 6
            ) if base_known else None,
        })

    assert sum(r["new_seedling_entries"] for r in output) == 3464
    assert sorted(r["plot_id"] for r in output) == sorted(plots)
    assert sum(r["habitat"] == "forest" for r in output) == 6
    assert sum(r["habitat"] in ("one", "ten") for r in output) == 7

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    print(json.dumps({
        "source_sha": EXPECTED_BLOB, "rows": len(rows),
        "independent_plots": len(output),
        "new_seedling_entries": sum(r["new_seedling_entries"] for r in output),
        "plot_first_output": str(args.output),
        "interpretation": "Exploratory ratios and censored observations, not causal stage rescue",
    }))


if __name__ == "__main__":
    main()
