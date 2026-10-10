#!/usr/bin/env python3
"""Reconstruct frozen Heliconia 13-plot input from original external CSVs.

No network access or new discovery. Input files must be separately obtained
from BrunaLab/HeliconiaSurveys at the published Git blob versions.
Usage:
  python scripts/rebuild_heliconia_plot_cohorts.py --survey PATH/HDP_survey.csv --plots PATH/HDP_plots.csv
Defaults to verifying the existing frozen summary, not overwriting it.
"""
import argparse
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/meta_extraction/heliconia_plot_cohorts_1999_2005_v1.csv"
RAW_BLOB = "f82a6f241493a979a2923d1c5deef6a1be0ff3ed"
PLOT_BLOB = "6fc835fb870d8c43ae4a4fcf04d515f419e6db22"
COUNTS = ("baseline_live_1998", "new_seedlings_1999_2005",
          "live_records_1999_2005", "flowering_records_1999_2005",
          "eligible_seedlings", "next_measured", "next_dead",
          "next_missing", "next_absent", "missing_later_measured")


def blob_sha(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def source_rows(path, expected_blob):
    raw = Path(path).read_bytes()
    assert blob_sha(raw) == expected_blob, ("wrong input source revision", path)
    return list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--survey", required=True)
    p.add_argument("--plots", required=True)
    args = p.parse_args()
    data = source_rows(args.survey, RAW_BLOB)
    meta = source_rows(args.plots, PLOT_BLOB)
    assert len(data) == 66396 and len(meta) == 13
    expected = {r["plot_id"]: {
        "plot_id": r["plot_id"],
        "habitat": "continuous" if r["habitat"] == "forest" else "fragment",
        "ranch": r["ranch"],
        "cohort_years": "7",
        **{k: 0 for k in COUNTS},
        "source_blob_sha": RAW_BLOB,
    } for r in meta}
    assert len(expected) == 13
    plants = {}
    seen = set()
    new_all = 0
    present_year = set()
    for r in data:
        site, y, plant = r["plot_id"], int(r["year"]), r["plant_id"]
        assert site in expected
        key = (site, plant, y)
        assert key not in seen, "duplicated plant-year unit"
        seen.add(key)
        present_year.add((site, y))
        status = r["census_status"]
        assert status in ("measured", "dead", "missing")
        is_new = r["recorded_sdlg"] == "TRUE"
        rec = plants.setdefault((site, plant), {"obs": {}, "new_year": None})
        rec["obs"][y] = status
        if is_new:
            assert rec["new_year"] is None
            rec["new_year"] = y
            assert status == "measured"
            new_all += 1
        o = expected[site]
        if y == 1998 and status == "measured":
            o["baseline_live_1998"] += 1
        if 1999 <= y <= 2005:
            o["new_seedlings_1999_2005"] += int(is_new)
            o["live_records_1999_2005"] += int(status == "measured")
            o["flowering_records_1999_2005"] += int(r["infl"] not in ("", "NA"))
    assert new_all == 3464 and len(plants) == 8586
    assert all((site, year) in present_year
               for site in expected for year in range(1998, 2007))
    for (site, _plant), rec in plants.items():
        y = rec["new_year"]
        if y is None or not 1999 <= y <= 2005:
            continue
        o = expected[site]
        o["eligible_seedlings"] += 1
        status = rec["obs"].get(y + 1, "absent")
        o["next_" + status] += 1
        if status == "missing":
            o["missing_later_measured"] += int(any(
                k > y + 1 and v == "measured"
                for k, v in rec["obs"].items()))
    with OUT.open(encoding="utf-8", newline="") as handle:
        frozen = list(csv.DictReader(handle))
    assert set(expected) == {r["plot_id"] for r in frozen}
    for row in frozen:
        f = expected[row["plot_id"]]
        for k in ("plot_id", "habitat", "ranch", "cohort_years", "source_blob_sha"):
            assert str(f[k]) == row[k], (row["plot_id"], k, f[k], row[k])
        for k in COUNTS:
            assert f[k] == int(row[k]), (row["plot_id"], k, f[k], row[k])
    assert sum(r["eligible_seedlings"] for r in expected.values()) == 2590
    assert sum(r["next_missing"] for r in expected.values()) == 222
    assert sum(r["missing_later_measured"] for r in expected.values()) == 116
    print("HELICONIA_SOURCE_REBUILD: PASS 66,396 rows; 8,586 plants; 3,464 "
          "new seedlings; 13 plot summaries; 2,590 balanced eligible cohorts; "
          "222 initially missing, 116 later seen alive")


if __name__ == "__main__":
    main()
