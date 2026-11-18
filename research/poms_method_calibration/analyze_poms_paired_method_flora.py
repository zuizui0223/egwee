#!/usr/bin/env python3
"""Source-pinned, prespecified PoMS same-site-date observation-channel analysis.

Original CSVs are downloaded into memory from the EIDC source and checked at
the uncompressed-member SHA-256 level. Only DERIVED estimates are reported.
See OUTCOME_ESTIMAND_FREEZE_20261117.md, committed before numeric fields opened.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
import math
from pathlib import Path
import sys

import numpy as np

import audit_poms_exact_site_date_ids as source


N_BOOT = 1000
BOOT_SEED = 20261117
FLOAT_TOL = 1e-8
BASIC_KEYS = ("sample_id", "country", "sample_projection", "x1km_square", "date", "year")
PAN_FIELDS = BASIC_KEYS + ("bees", "hoverflies")
FIT_FIELDS = BASIC_KEYS + ("bumblebees", "honeybees", "solitary_bees", "hoverflies")
FLOWER_FIELDS = ("sample_id", "source_taxon_version_key", "taxon_source")


def parse_count(raw: str) -> int | None:
    if not raw:
        return None
    try:
        number = float(raw)
    except ValueError:
        return None
    if not math.isfinite(number) or number < 0 or not number.is_integer():
        return None
    return int(number)


def parse_date(raw: str, year_text: str) -> tuple[int, int]:
    val = None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            val = datetime.strptime(raw, fmt)
            break
        except ValueError:
            continue
    if val is None:
        try:
            val = datetime.fromisoformat(raw)
        except ValueError as exc:
            raise ValueError("SOURCE_STOP: unrecognized date format") from exc
    if str(val.year) != year_text:
        raise ValueError("SOURCE_STOP: date and survey year disagree")
    return val.year, val.month


def gather_events(archive, member: str, fields: tuple[str, ...], method: str):
    events = {}
    seen_sample_ids = set()
    sample_events = {}
    for row in source.rows_only(archive, member, fields):
        rid = row["sample_id"]
        if not rid or rid in seen_sample_ids:
            raise ValueError("ID_STOP: missing/duplicate source sample_id")
        seen_sample_ids.add(rid)
        site = (row["country"], row["sample_projection"], row["x1km_square"])
        if not all(site) or not row["date"] or not row["year"]:
            raise ValueError("ID_STOP: missing key")
        key = (*site, row["date"])
        yr, month = parse_date(row["date"], row["year"])
        if key not in events:
            events[key] = {
                "site": site, "year": yr, "month": month, "sample_ids": [],
                "b": 0, "h": 0, "invalid": False,
            }
        ev = events[key]
        if ev["year"] != yr or ev["month"] != month:
            raise ValueError("ID_STOP: inconsistent date/year within exact event")
        ev["sample_ids"].append(rid)
        sample_events[rid] = key
        if method == "pan":
            raw_bees = (row["bees"],)
        else:
            raw_bees = (row["bumblebees"], row["honeybees"], row["solitary_bees"])
        vals = [parse_count(x) for x in raw_bees + (row["hoverflies"],)]
        if any(v is None for v in vals):
            ev["invalid"] = True
        else:
            ev["b"] += sum(vals[:-1])
            ev["h"] += vals[-1]
    return events, sample_events


def get_flower_context(archive, pan_ids: set[str]):
    flowers = defaultdict(set)
    orphan = 0
    no_taxon_key = 0
    for row in source.rows_only(archive, source.PAN_FLOWERS, FLOWER_FIELDS):
        rid = row["sample_id"]
        if rid not in pan_ids:
            orphan += 1
            continue
        # Preferred original taxon identifier and literal fallback, frozen.
        taxon = row["source_taxon_version_key"] or row["taxon_source"]
        if not taxon:
            no_taxon_key += 1
            continue
        flowers[rid].add(taxon)
    return flowers, {"orphan_flower_rows": orphan, "unkeyed_flower_rows": no_taxon_key}


def create_pairs(pan_z, fit_z):
    pan, pan_sample_map = gather_events(pan_z, source.PAN_SAMPLES, PAN_FIELDS, "pan")
    fit, _ = gather_events(fit_z, source.FIT_1KM, FIT_FIELDS, "fit")
    flowers, floral_report = get_flower_context(pan_z, set(pan_sample_map))
    matches = sorted(set(pan) & set(fit))
    if len(matches) != 1221:
        raise ValueError("ID_STOP: exact source join does not reproduce pre-outcome 1221 denominator")
    counts = Counter()
    by_year = Counter()
    paired = []
    for event in matches:
        p = pan[event]
        f = fit[event]
        if p["year"] != f["year"] or p["month"] != f["month"]:
            raise ValueError("ID_STOP: disagreeing source calendar")
        if p["invalid"] or f["invalid"]:
            counts["missing_or_invalid_source_count_event"] += 1
            continue
        if p["b"] + p["h"] == 0:
            counts["zero_pan_bee_hoverfly_event"] += 1
        if f["b"] + f["h"] == 0:
            counts["zero_fit_bee_hoverfly_event"] += 1
        if p["b"] + p["h"] == 0 or f["b"] + f["h"] == 0:
            counts["excluded_event_either_total_zero"] += 1
            continue
        x = float(sum(len(flowers[rid]) for rid in p["sample_ids"])) / len(p["sample_ids"])
        if x == 0:
            counts["zero_source_flower_record_event"] += 1
        paired.append({
            "site": p["site"], "year": p["year"], "month": p["month"],
            "x": x, "bp": p["b"], "hp": p["h"], "bf": f["b"], "hf": f["h"],
            "yp": math.log((p["b"] + 0.5) / (p["h"] + 0.5)),
            "yf": math.log((f["b"] + 0.5) / (f["h"] + 0.5)),
            "w": float(p["b"] + p["h"] + f["b"] + f["h"]),
        })
        by_year[p["year"]] += 1
    result = {
        "exact_matched_events_before_count_filter": len(matches),
        "positive_both_method_events": len(paired),
        "information_bearing_sites": len(set(row["site"] for row in paired)),
        "information_bearing_years": dict(sorted(by_year.items())),
        "exclusion_counts_nonexclusive": dict(counts),
        **floral_report,
        "observed_pan_sample_count": len(pan_sample_map),
        "observed_fit_sample_count": sum(len(x["sample_ids"]) for x in fit.values()),
    }
    return paired, result


def add_fixed_standardization(rows):
    x = np.array([r["x"] for r in rows], dtype=float)
    mu, sd = float(x.mean()), float(x.std(ddof=0))
    if sd <= 0 or not np.isfinite(sd):
        raise ValueError("COVERAGE_STOP: no variation in measured flower incidence")
    for r in rows:
        r["xz"] = (r["x"] - mu) / sd
    return {"x_mean": mu, "x_sd": sd, "min_x": float(x.min()), "max_x": float(x.max())}


def fit_slope(rows, outcome: str, weighted: bool = False) -> float:
    if len(rows) < 15:
        raise ValueError("FIT_STOP: too few events")
    years = sorted(set(r["year"] for r in rows))
    months = sorted(set(r["month"] for r in rows))
    xs = np.array([
        [r["xz"]]
        + [float(r["year"] == y) for y in years[1:]]
        + [float(r["month"] == m) for m in months[1:]]
        for r in rows
    ], dtype=float)
    response = np.array([r[outcome] if outcome != "d" else r["yf"] - r["yp"]
                         for r in rows], dtype=float)
    weights = np.array([r["w"] if weighted else 1.0 for r in rows], dtype=float)
    if np.any(weights <= 0):
        raise ValueError("FIT_STOP: nonpositive weights")
    grp = defaultdict(list)
    for i, row in enumerate(rows):
        grp[row["site"]].append(i)
    # Exact site fixed effects via within-site centering; weighted if requested.
    for ix in grp.values():
        inds = np.asarray(ix)
        w = weights[inds]
        xs[inds] -= np.average(xs[inds], axis=0, weights=w)
        response[inds] -= np.average(response[inds], weights=w)
    if float(np.linalg.norm(xs[:, 0])) <= FLOAT_TOL:
        raise ValueError("FIT_STOP: floral context lacks independent within-site variation")
    sw = np.sqrt(weights)
    beta, residuals, rank, singular = np.linalg.lstsq(
        xs * sw[:, None], response * sw, rcond=None
    )
    if rank < xs.shape[1]:
        raise ValueError("FIT_STOP: site-demeaned month/year exposure matrix rank deficient")
    if not np.isfinite(beta[0]):
        raise ValueError("FIT_STOP: nonfinite estimated primary slope")
    return float(beta[0])


def leave_one_out(rows, label):
    labels = sorted(set(r[label] for r in rows))
    results = []
    failed = 0
    for drop in labels:
        subset = [r for r in rows if r[label] != drop]
        try:
            results.append(fit_slope(subset, "d"))
        except ValueError:
            failed += 1
    if not results:
        return {"status": "not_estimable", "failed": failed, "attempted": len(labels)}
    return {
        "min_delta": min(results), "max_delta": max(results),
        "positive": sum(d > 0 for d in results), "negative": sum(d < 0 for d in results),
        "failed": failed, "attempted": len(labels)
    }


def bootstrap_sites(rows):
    sites = sorted(set(r["site"] for r in rows))
    groups = defaultdict(list)
    for row in rows:
        groups[row["site"]].append(row)
    rng = np.random.default_rng(BOOT_SEED)
    values = []
    failed = 0
    for j in range(N_BOOT):
        sampled = rng.integers(0, len(sites), size=len(sites))
        boot = []
        for resampled_site_index, original_site_idx in enumerate(sampled):
            site_original = sites[int(original_site_idx)]
            newsite = ("bootstrap", str(resampled_site_index), "")
            for row in groups[site_original]:
                # New site key for each resampled cluster, preserving within-site dependence.
                boot.append({**row, "site": newsite})
        try:
            values.append(fit_slope(boot, "d"))
        except ValueError:
            failed += 1
    if failed > 0.05 * N_BOOT:
        raise ValueError("BOOTSTRAP_STOP: >5% rank failures")
    if not values:
        raise ValueError("BOOTSTRAP_STOP: no successful resamples")
    return {
        "attempted": N_BOOT, "success": len(values), "failed": failed,
        "seed": BOOT_SEED,
        "percentile_95_ci": [float(v) for v in np.percentile(values, [2.5, 97.5])],
        "proportion_positive": sum(v > 0 for v in values) / len(values),
    }


def analyze(rows):
    n_sites = len({r["site"] for r in rows})
    n_years = len({r["year"] for r in rows})
    site_x = defaultdict(list)
    for r in rows:
        site_x[r["site"]].append(r["x"])
    varying_sites = sum(float(np.std(vals)) > 0 for vals in site_x.values())
    coverage = {"n_events": len(rows), "n_sites": n_sites, "n_years": n_years,
                "sites_with_within_site_flower_variation": varying_sites}
    if not (n_sites >= 20 and len(rows) >= 80 and n_years >= 3 and varying_sites > 0):
        return {"status": "UNIDENTIFIABLE_POST_OUTCOME_COVERAGE", "coverage": coverage}
    scaling = add_fixed_standardization(rows)
    delta = fit_slope(rows, "d")
    beta_pan = fit_slope(rows, "yp")
    beta_fit = fit_slope(rows, "yf")
    if abs(delta - (beta_fit - beta_pan)) > FLOAT_TOL:
        raise ValueError("MODEL_STOP: delta is not equal to within-method slope difference")
    boot = bootstrap_sites(rows)
    subset_positive = [r for r in rows if r["x"] > 0]
    try:
        no_zero_delta = fit_slope(subset_positive, "d")
        zero_sensitivity = {"status": "estimated", "delta": no_zero_delta,
                            "n_events": len(subset_positive),
                            "n_sites": len(set(r["site"] for r in subset_positive))}
    except ValueError as exc:
        zero_sensitivity = {"status": "not_estimable", "reason": str(exc),
                            "n_events": len(subset_positive)}
    try:
        weighted_delta = fit_slope(rows, "d", weighted=True)
        weighted_sensitivity = {"status": "estimated", "delta": weighted_delta}
    except ValueError as exc:
        weighted_sensitivity = {"status": "not_estimable", "reason": str(exc)}
    return {
        "status": "PRIMARY_ESTIMATED",
        "coverage": coverage,
        "x_scale": scaling,
        "primary": {
            "delta_fit_minus_pan": delta, "beta_fit": beta_fit,
            "beta_pan": beta_pan, "site_bootstrap": boot,
            "unit": "log bee-to-hoverfly observation-ratio contrast / 1 SD pan flower incidence",
        },
        "sensitivity": {
            "omit_zero_flower_record_event": zero_sensitivity,
            "total_pollinator_count_weighted": weighted_sensitivity,
            "leave_one_site_out": leave_one_out(rows, "site"),
            "leave_one_year_out": leave_one_out(rows, "year"),
        }
    }


def self_test():
    rng = np.random.default_rng(24)
    test = []
    for si in range(20):
        for yr in range(2017, 2022):
            for month in (5, 6, 7):
                x = (si % 5) * 0.2 + rng.normal() + 0.1 * (yr - 2017)
                test.append({"site": ("synthetic", "EPSG", str(si)), "year": yr,
                             "month": month, "xz": x,
                             "yp": 0.25 * x + 0.4 * (month == 6) + rng.normal(0, 0.02),
                             "yf": -0.1 * x + 0.3 * (yr == 2019) + rng.normal(0, 0.02),
                             "w": 5.0})
    bp = fit_slope(test, "yp")
    bf = fit_slope(test, "yf")
    delta = fit_slope(test, "d")
    if abs(delta - (bf - bp)) > 1e-10 or abs(delta + 0.35) > 0.02:
        raise AssertionError("Synthetic within-site FE test failed")
    # A site bootstrap must treat resampled copies as distinct clusters.
    print("SYNTHETIC_TEST_PASS", json.dumps({"beta_pan": bp, "beta_fit": bf, "delta": delta}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.output is None:
        parser.error("--output is required unless --self-test")
    report = {
        "analysis": "PoMS same-day flower observation mode interaction",
        "pre_outcome_freeze": "research/poms_method_calibration/OUTCOME_ESTIMAND_FREEZE_20261117.md",
        "source_uncompressed_csv_shas": source.EXPECTED_MEMBER_SHA,
        "raw_original_source_distributed": False,
        "model_type": "equal-site-date log-composition difference with site, year and month fixed effects",
        "source_public_FIT_excluded": True,
    }
    try:
        with source.load_archive("pan") as pz, source.load_archive("fit") as fz:
            pairs, coverage = create_pairs(pz, fz)
            report["source_coverage"] = coverage
            report.update(analyze(pairs))
    except Exception as err:
        report["status"] = "SOURCE_OR_ESTIMATION_STOP"
        report["reason"] = f"{type(err).__name__}: {str(err)[:300]}"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PAIRED_POMS_DERIVED_RESULT " + json.dumps(report, sort_keys=True), flush=True)
    return 0 if report["status"] in ("PRIMARY_ESTIMATED", "UNIDENTIFIABLE_POST_OUTCOME_COVERAGE") else 1


if __name__ == "__main__":
    sys.exit(main())
