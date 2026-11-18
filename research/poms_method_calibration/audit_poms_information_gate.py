#!/usr/bin/env python3
"""Post-primary descriptive audit of PoMS matched-event selection.

Selection into the *positive bee+hoverfly counts in BOTH methods* contrast may
vary with flowers and method effort. Retrospective; does not re-test the
registered primary bee/hoverfly outcome, nor estimate true abundance.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys

import numpy as np

N_BOOT = 1000
SEED = 20261118


def load_original_event_rows():
    # Lazy import allows an offline synthetic self-test, without raw sources.
    import audit_poms_exact_site_date_ids as source
    import analyze_poms_paired_method_flora as main

    with source.load_archive("pan") as pan_zip, source.load_archive("fit") as fit_zip:
        pan, pan_sample_map = main.gather_events(
            pan_zip, source.PAN_SAMPLES, main.PAN_FIELDS, "pan")
        fit, _ = main.gather_events(
            fit_zip, source.FIT_1KM, main.FIT_FIELDS, "fit")
        flowers, floral_receipt = main.get_flower_context(
            pan_zip, set(pan_sample_map))
    pairs = sorted(set(pan) & set(fit))
    if len(pairs) != 1221:
        raise ValueError("SOURCE_STOP: expected 1,221 exact original same-date events")

    rows = []
    categories = Counter()
    by_year = defaultdict(lambda: {"n": 0, "R_one": 0})
    for event in pairs:
        p, f = pan[event], fit[event]
        if p["site"] != f["site"] or p["year"] != f["year"] or p["month"] != f["month"]:
            raise ValueError("SOURCE_STOP: mismatch in matched key components")
        categories["exact_source_matched_events"] += 1
        if p["invalid"] or f["invalid"]:
            categories["invalid_source_group_count_events"] += 1
            continue
        pan_zero = (p["b"] + p["h"] == 0)
        fit_zero = (f["b"] + f["h"] == 0)
        if pan_zero:
            categories["zero_pan_nonexclusive"] += 1
        if fit_zero:
            categories["zero_fit_nonexclusive"] += 1
        if pan_zero and fit_zero:
            cat = "both_zero"
        elif pan_zero:
            cat = "pan_only_zero"
        elif fit_zero:
            cat = "fit_only_zero"
        else:
            cat = "both_positive"
        categories[cat] += 1

        if not p["sample_ids"] or not f["sample_ids"]:
            raise ValueError("SOURCE_STOP: empty method effort on a source-exact matched event")
        x = sum(len(flowers[rid]) for rid in p["sample_ids"]) / len(p["sample_ids"])
        row = {
            "site": p["site"], "year": p["year"], "month": p["month"],
            "x": float(x), "pan_n": len(p["sample_ids"]),
            "fit_n": len(f["sample_ids"]),
            "R": int(not pan_zero and not fit_zero),
        }
        rows.append(row)
        by_year[p["year"]]["n"] += 1
        by_year[p["year"]]["R_one"] += row["R"]

    if categories["both_positive"] != 972:
        raise ValueError("SOURCE_STOP: informative-event count disagrees with frozen primary")
    if categories["invalid_source_group_count_events"] != 0:
        raise ValueError("SOURCE_STOP: primary denominator altered by invalid fields")
    return rows, {
        "event_categories": dict(sorted(categories.items())),
        "information_by_year": {
            str(y): {**r, "fraction": r["R_one"] / r["n"]}
            for y, r in sorted(by_year.items())},
        "original_flower_source_receipt": floral_receipt,
        "expected_source_member_sha256": source.EXPECTED_MEMBER_SHA,
    }


def standardized_rows(rows):
    x = np.array([r["x"] for r in rows], dtype=float)
    mean, sd = float(x.mean()), float(x.std(ddof=0))
    if sd <= 0 or not np.isfinite(sd):
        raise ValueError("COVERAGE_STOP: no X variation on all original matched events")
    for row in rows:
        row["xz"] = (row["x"] - mean) / sd
    return {"mean_X": mean, "SD_X": sd,
            "X_range": [float(x.min()), float(x.max())]}


def fit_information_slope(rows, with_effort=False):
    """FWL within-site OLS LPM slope for R; never a causal probability."""
    years = sorted({r["year"] for r in rows})
    months = sorted({r["month"] for r in rows})
    if len(rows) < 80 or len(years) < 3:
        raise ValueError("FIT_STOP: coverage below specified gate")
    design = np.asarray([
        [r["xz"]]
        + ([float(r["pan_n"]), float(r["fit_n"])] if with_effort else [])
        + [float(r["year"] == y) for y in years[1:]]
        + [float(r["month"] == m) for m in months[1:]]
        for r in rows
    ], dtype=float)
    response = np.asarray([r["R"] for r in rows], dtype=float)
    grouped = defaultdict(list)
    for i, r in enumerate(rows):
        grouped[r["site"]].append(i)
    for ids in grouped.values():
        ind = np.asarray(ids)
        design[ind] -= design[ind].mean(axis=0)
        response[ind] -= response[ind].mean()
    if np.linalg.norm(design[:, 0]) <= 1e-9:
        raise ValueError("FIT_STOP: no within-site X variation")
    betas, _, rank, _ = np.linalg.lstsq(design, response, rcond=None)
    if rank != design.shape[1]:
        raise ValueError("FIT_STOP: site-demeaned design rank deficient")
    return float(betas[0])


def cluster_bootstrap(rows, with_effort):
    sites = sorted({r["site"] for r in rows})
    grouped = defaultdict(list)
    for r in rows:
        grouped[r["site"]].append(r)
    rng = np.random.default_rng(SEED)
    successful = []
    failed = 0
    for _ in range(N_BOOT):
        sampled = rng.integers(0, len(sites), size=len(sites))
        boot = []
        for newsite, idx in enumerate(sampled):
            boot.extend({**r, "site": ("bootstrap", newsite)}
                        for r in grouped[sites[int(idx)]])
        try:
            successful.append(fit_information_slope(boot, with_effort=with_effort))
        except ValueError:
            failed += 1
    if failed > 0.05 * N_BOOT or not successful:
        raise ValueError("BOOTSTRAP_STOP: >5% failed whole-site resamples")
    return {
        "attempted": N_BOOT, "success": len(successful), "failed": failed,
        "seed": SEED,
        "percentile_95_CI": [float(z) for z in np.percentile(successful, [2.5, 97.5])],
        "fraction_positive": sum(z > 0 for z in successful) / len(successful),
    }


def analyse(rows, receipt):
    if len(rows) != 1221 or len({r["site"] for r in rows}) < 20:
        raise ValueError("COVERAGE_STOP: original event denominator or site gate failed")
    scale = standardized_rows(rows)
    variable_sites = sum(len({r["x"] for r in rows if r["site"] == site}) > 1
                         for site in {r["site"] for r in rows})
    if variable_sites == 0:
        raise ValueError("COVERAGE_STOP: no within-site X variation")
    positive_x = [r["x"] for r in rows if r["R"] == 1]
    excluded_x = [r["x"] for r in rows if r["R"] == 0]
    receipt.update({
        "analysis": "post-primary exploratory PoMS informative-event selection gate",
        "status": "EXPLORATORY_INFORMATION_GATE_ESTIMATED",
        "source_rows_distributed": False,
        "n_valid_original_events": len(rows),
        "n_sites": len({r["site"] for r in rows}),
        "n_years": len({r["year"] for r in rows}),
        "sites_with_varying_X": variable_sites,
        "R_fraction": sum(r["R"] for r in rows) / len(rows),
        "floral_scale_on_ALL_events": scale,
        "floral_X_mean_by_gate": {
            "R_1": float(np.mean(positive_x)),
            "R_0": float(np.mean(excluded_x)),
        },
        "method_effort_summary": {
            "pan_samples_per_event_min_max": [min(r["pan_n"] for r in rows), max(r["pan_n"] for r in rows)],
            "FIT_counts_per_event_min_max": [min(r["fit_n"] for r in rows), max(r["fit_n"] for r in rows)],
        },
    })
    for key, with_effort in (("site_year_month_FEs", False),
                             ("plus_pan_sample_and_FIT_count_effort_proxies", True)):
        receipt.setdefault("retrospective_lpm_diagnostics", {})[key] = {
            "slope_per_X_SD_probability_points": fit_information_slope(rows, with_effort),
            "whole_site_bootstrap": cluster_bootstrap(rows, with_effort),
        }
    return receipt


def self_test():
    rng = np.random.default_rng(20261118)
    rows = []
    for s in range(30):
        for y in range(2017, 2021):
            for m in (5, 6, 7):
                x = rng.normal() + 0.2 * (s % 4)
                pn, fn = int(rng.integers(1, 7)), int(rng.integers(1, 11))
                R = 0.27 * x + 0.15 * pn - 0.12 * fn + 0.05 * (m == 6) + 0.03 * (y == 2019)
                rows.append({"site": ("synthetic", s), "year": y, "month": m,
                             "x": x, "pan_n": pn, "fit_n": fn, "R": R})
    scale = standardized_rows(rows)
    b = fit_information_slope(rows, with_effort=True)
    if abs(b - 0.27 * scale["SD_X"]) > 1e-10:
        raise AssertionError("Synthetic FE+effort slope identity failed")
    print("INFORMATION_GATE_SYNTHETIC_PASS", json.dumps({"beta": b}))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.output is None:
        p.error("--output required unless --self-test")
    result = {
        "spec": "research/poms_method_calibration/INFORMATION_GATE_DIAGNOSTIC_SPEC_20261117.md",
        "post_primary_exploratory": True,
        "primary_estimator_or_frozen_denominator_altered": False,
    }
    try:
        rows, receipt = load_original_event_rows()
        result.update(analyse(rows, receipt))
    except Exception as exc:
        result["status"] = "SOURCE_OR_DIAGNOSTIC_STOP"
        result["reason"] = f"{type(exc).__name__}: {str(exc)[:300]}"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("POST_PRIMARY_INFORMATION_GATE " + json.dumps(result, sort_keys=True), flush=True)
    return 0 if result["status"] == "EXPLORATORY_INFORMATION_GATE_ESTIMATED" else 1


if __name__ == "__main__":
    sys.exit(main())
