#!/usr/bin/env python3
"""LA002: per-single-visit seed calibration vs frozen LA001 site holdout.

Requires the exact original source ZIP as a local input. Source-specific parser
reuses LA001 source-integrity checks, without publishing any original workbook,
plant ID, genotype, individual seed count, or insect-event sequence.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from statistics import fmean
import zipfile

from run_leavenworthia_LA001 import (
    SITES, SITE_ID, SOURCE_SHA, draw_source, sheets, value, positive_int,
    ridge_predict, solve,
)

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "LA002_FROZEN_SINGLE_VISIT_PROTOCOL_20261117.json"
PREVIOUS = HERE / "LA001_HELDOUT_RESULT_20261117.json"
FROZEN_SHA = "9372a647950df565b387b96169c8c6c77bb6917d"


def calibrate_single_visit(outer: zipfile.ZipFile) -> dict[str, dict]:
    trial = sheets(outer, "Emasculation+experiment.xlsx")["Final pass"]
    if len(trial) != 73:
        raise ValueError("Single-visit trial row count shifted")
    groups: dict[str, list[dict]] = {}
    for rno, row in trial.items():
        if rno == 1:
            continue
        group = value(row, 0)
        fruit = value(row, 2)
        seed = value(row, 3)
        if group not in ("Solitary", "BeeFly", "Fly", "Honeybee", "Ant", "Control"):
            raise ValueError(f"Unknown single-visit assay group at row {rno}")
        if fruit not in (0.0, 1.0):
            raise ValueError("Unparseable fruit set in original assay")
        if fruit == 0.0:
            if seed is not None:
                raise ValueError("Seeds present on no-fruit assay row")
            seed = 0.0
        elif not isinstance(seed, (float, int)) or seed < 0:
            raise ValueError("Fruit-bearing assay without a nonnegative seed count")
        groups.setdefault(group, []).append({"fruit": int(fruit), "seed": float(seed)})
    expected = {
        "Solitary": (22, 14, 57.0), "BeeFly": (9, 6, 23.0),
        "Fly": (17, 2, 7.0), "Honeybee": (2, 1, 4.0),
        "Ant": (1, 0, 0.0), "Control": (21, 1, 1.0),
    }
    out = {}
    for label, (count, fruits, seeds) in expected.items():
        a = groups.get(label, [])
        if len(a) != count or sum(r["fruit"] for r in a) != fruits or abs(
            sum(r["seed"] for r in a) - seeds
        ) > 1e-10:
            raise ValueError("Source efficacy assay differs from frozen n/fruit/seed totals")
        out[label] = {
            "n": count, "n_fruits": fruits, "total_seeds": seeds,
            "mean_seeds_per_assigned_visit": seeds / count,
        }
    return out


def pollinator_sequences_by_plant(
    outer: zipfile.ZipFile,
    source_fields: dict[tuple[int, int, str], dict],
) -> tuple[dict[tuple[int, int, str], dict], dict]:
    """Rebuild AH/BF/F counts and flower-hours from complete source periods."""
    poll = {
        2014: sheets(outer, "Pollinator+Data+2014.xlsx"),
        2015: sheets(outer, "Pollinator+Data+2015.xlsx"),
    }
    ex = {}
    qc = Counter()
    for year, wb in poll.items():
        first = wb["First Flower"]
        for site_name in SITES:
            site = SITE_ID[site_name]
            col = {
                2014: {"Waco": 10, "Quarry": 2, "24-43": 14, "Landersville": 6},
                2015: {"Waco": 9, "Quarry": 1, "24-43": 13, "Landersville": 5},
            }[year][site_name]
            poscol = col - 1 if year == 2014 else col + 1
            position_to_id = {}
            for rno in range(5, 37):
                row = first[rno]
                id_ = value(row, col)
                position = positive_int(value(row, poscol))
                if not isinstance(id_, str) or position in position_to_id:
                    raise ValueError("Invalid field-to-position join")
                if (year, site, id_.strip()) not in source_fields:
                    raise ValueError("Position label does not match site-year field source")
                position_to_id[position] = id_.strip()
            if set(position_to_id) != set(range(1, 33)):
                raise ValueError("Missing/duplicate plant position in source")
            sheet = wb["Quarry Array" if year == 2014 and site_name == "Quarry" else site_name]
            periods = []
            period = None
            for rno, row in sorted(sheet.items()):
                status, taxon = value(row, 5), value(row, 6)
                if isinstance(status, str) and status.strip().lower() == "open flowers":
                    period = {"open": [value(row, c) for c in range(7, 39)],
                              "visits": [], "total": None}
                    periods.append(period)
                elif isinstance(status, str) and status.strip().lower() == "total":
                    if period is not None:
                        period["total"] = taxon
                elif isinstance(taxon, str) and taxon.strip() and (
                    isinstance(status, (float, int)) or str(status).isdigit()
                ):
                    if period is None:
                        raise ValueError("Visit without open-flower session")
                    for c in range(7, 200):
                        index = value(row, c)
                        if index is not None:
                            if not isinstance(index, (int, float)) or index != int(index):
                                raise ValueError("Noninteger field visit position")
                            period["visits"].append((int(index), taxon.strip().upper()))
            admitted = [p for p in periods if p["total"] is not None]
            if any(p["visits"] for p in periods if p["total"] is None):
                raise ValueError("Incomplete session holds visits")
            qc["open_flower_rows"] += len(periods)
            qc["complete_sessions"] += len(admitted)
            counts = {pos: {"flower_hours": 0.0, "AH": 0, "BF": 0, "F": 0,
                            "all": 0} for pos in range(1, 33)}
            for p in admitted:
                for pos in range(1, 33):
                    nflowers = p["open"][pos - 1]
                    if not isinstance(nflowers, (float, int)) or nflowers < 0:
                        raise ValueError("Invalid open-flower exposure in source")
                    counts[pos]["flower_hours"] += 0.5 * nflowers
                if not isinstance(p["total"], (float, int)) or len(p["visits"]) != int(p["total"]):
                    raise ValueError("Visit TOTAL mismatch")
                for pos, taxon in p["visits"]:
                    if pos not in range(1, 33):
                        qc["invalid_position_visits"] += 1
                        continue
                    qc["valid_position_visits"] += 1
                    if p["open"][pos - 1] <= 0:
                        qc["zero_open_flower_visits"] += 1
                        continue
                    counts[pos]["all"] += 1
                    if taxon in ("AH", "BF", "F"):
                        counts[pos][taxon] += 1
            for pos, id_ in position_to_id.items():
                if counts[pos]["flower_hours"] <= 0:
                    raise ValueError("Zero source flower exposure")
                ex[year, site, id_] = counts[pos]
    if len(ex) != 256 or (
        qc["open_flower_rows"], qc["complete_sessions"],
        qc["valid_position_visits"], qc["zero_open_flower_visits"],
        qc["invalid_position_visits"]
    ) != (125, 121, 6701, 38, 1):
        raise ValueError(f"LA001 provenance invariant failed: {dict(qc)}")
    return ex, dict(qc)


def prepare_original_252(source_zip: Path) -> tuple[list[dict], dict]:
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    if protocol["experiment_id"] != "LA002_independently_assayed_single_visit_quality_site_transfer":
        raise ValueError("Wrong frozen LA002 protocol")
    if hashlib.sha256(source_zip.read_bytes()).hexdigest() != SOURCE_SHA:
        raise ValueError("Original source archive hash mismatch")
    old_meta, old_rows = draw_source(source_zip)
    if len(old_rows) != 252 or old_meta["completed_sessions"] != 121:
        raise ValueError("Original LA001 source gate shifted")
    with zipfile.ZipFile(source_zip) as outer:
        trial = calibrate_single_visit(outer)
        field = sheets(outer, "2014+2015+Field+data.xlsx")["Sheet1"]
        source = {}
        for rno, row in field.items():
            if rno == 1:
                continue
            yc = positive_int(value(row, 0))
            y = {1: 2014, 2: 2015}[yc]
            site = positive_int(value(row, 1))
            pid = value(row, 2)
            if not isinstance(pid, str) or (y, site, pid.strip()) in source:
                raise ValueError("Invalid original field plant key")
            source[y, site, pid.strip()] = row
        if len(source) != 256:
            raise ValueError("Source field individual count drift")
        exposure, qc = pollinator_sequences_by_plant(outer, source)
    order = [k for k, row in source.items() if value(row, 10) is not None]
    if len(order) != len(old_rows):
        raise ValueError("Old LA001 eligible observation order shifted")
    weights = {
        "AH": trial["Solitary"]["mean_seeds_per_assigned_visit"],
        "BF": trial["BeeFly"]["mean_seeds_per_assigned_visit"],
        "F": trial["Fly"]["mean_seeds_per_assigned_visit"],
    }
    rows = []
    for key, prior in zip(order, old_rows):
        year, site, pid = key
        actual = source[key]
        cnt = exposure[key]
        if (prior["site"] != site or prior["year"] != year or
            abs(prior["y"] - math.log1p(value(actual, 10))) > 1e-10):
            raise ValueError("LA001 outcome key alignment changed")
        if abs(prior["effective"] - math.log1p(
            (cnt["AH"] + cnt["BF"]) / cnt["flower_hours"]
        )) > 1e-10 or abs(prior["total"] - math.log1p(
            cnt["all"] / cnt["flower_hours"]
        )) > 1e-10:
            raise ValueError("Independent visitor decoding does not reproduce LA001")
        quality = sum(cnt[code] * weight for code, weight in weights.items())
        row = dict(prior)
        row["quality"] = math.log1p(quality / cnt["flower_hours"])
        rows.append(row)
    return rows, {"assay": trial, "weights": weights, "visit_qc": qc}


def weighted_ridge(train: list[dict], hold: list[dict]) -> list[float]:
    """Exactly LA001 ridge lambda=1 applied to baseline + new quality score."""
    keys = lambda row: list(row["baseline"]) + [row["quality"]]
    raw = [keys(r) for r in train]
    p = len(raw[0])
    means = [fmean(x[j] for x in raw) for j in range(p)]
    scales = []
    for j in range(p):
        sd = math.sqrt(fmean((x[j] - means[j]) ** 2 for x in raw))
        scales.append(sd if sd > 1e-10 else 1.0)
    X = [[1.0] + [(x[j] - means[j]) / scales[j] for j in range(p)]
         for x in raw]
    gram = [[sum(x[j] * x[k] for x in X) + (1.0 if j == k and j > 0 else 0.0)
             for k in range(p + 1)] for j in range(p + 1)]
    rhs = [sum(x[j] * r["y"] for x, r in zip(X, train)) for j in range(p + 1)]
    coefs = solve(gram, rhs)
    return [coefs[0] + sum(coefs[j + 1] * (keys(r)[j] - means[j]) / scales[j]
                           for j in range(p)) for r in hold]


def analyze(source_zip: Path) -> dict:
    rows, source = prepare_original_252(source_zip)
    old = json.loads(PREVIOUS.read_text(encoding="utf-8"))
    if old["decision"] != "NO_ROBUST_SINGLE_PROGRAMME_INCREMENT":
        raise ValueError("Prior primary conclusion unexpectedly changed")
    scored = []
    folds = []
    for site, name in enumerate(SITES, 1):
        train = [r for r in rows if r["site"] != site]
        test = [r for r in rows if r["site"] == site]
        base = ridge_predict(train, test, "M0_baseline")
        simple = ridge_predict(train, test, "M1_effective_visits")
        overall = ridge_predict(train, test, "M2_all_visits")
        weighted = weighted_ridge(train, test)
        errors = {}
        for label, vals in (("M0", base), ("M1", simple),
                            ("M2", overall), ("M3", weighted)):
            residuals = [r["y"] - v for r, v in zip(test, vals)]
            errors[label] = {
                "mse": fmean(v * v for v in residuals),
                "mae": fmean(abs(v) for v in residuals),
            }
            scored.extend((label, v) for v in residuals)
        orig = next(f for f in old["folds"] if f["site"] == name)
        for label in ("M0", "M1", "M2"):
            if abs(errors[label]["mse"] - orig[f"{label}_mse"]) > 1e-9:
                raise ValueError(f"Original four-site LA001 MSE drift: {name}/{label}")
        folds.append({
            "site": name, "n": len(test),
            "models": errors,
            "M0_minus_M3_mse": errors["M0"]["mse"] - errors["M3"]["mse"],
            "M1_minus_M3_mse": errors["M1"]["mse"] - errors["M3"]["mse"],
        })
    if sum(x["n"] for x in folds) != 252:
        raise ValueError("Held-out sample count drift")
    pooled = {}
    for label in ("M0", "M1", "M2", "M3"):
        pooled[label] = {
            key: sum(f["n"] * f["models"][label][key] for f in folds) / 252
            for key in ("mse", "mae")
        }
    delta = pooled["M0"]["mse"] - pooled["M3"]["mse"]
    wins = sum(f["M0_minus_M3_mse"] > 0 for f in folds)
    return {
        "schema_version": 1,
        "experiment_id": "LA002_independently_assayed_single_visit_quality_site_transfer",
        "protocol_frozen_commit": FROZEN_SHA,
        "status": "SOURCE_PINNED_SAME_STUDY_SITE_HOLDOUT_COMPLETED",
        "original_source_SHA256": SOURCE_SHA,
        "single_visit_assay": source["assay"],
        "calibrated_weights": source["weights"],
        "source_visit_QC": source["visit_qc"],
        "eligible_field_plants": 252,
        "whole_site_fold_count": 4,
        "folds": folds,
        "pooled": pooled,
        "primary_M0_minus_M3_mse": delta,
        "secondary_M1_minus_M3_mse": pooled["M1"]["mse"] - pooled["M3"]["mse"],
        "positive_folds": wins,
        "frozen_decision": (
            "BOUNDED_WITHIN_PROGRAMME_QUALITY_WEIGHTED_GAIN"
            if delta > 0 and wins >= 3
            else "NO_ROBUST_ASSAY_CALIBRATED_SITE_TRANSFER_INCREMENT"
        ),
        "limitations": [
            "Original Waco 2015 single-visit assay is within same original research programme",
            "No genetically compatible pollen, paternal identity or viable offspring measurements",
            "Unassayed guilds excluded from calibrated numerator, not proven ineffective",
            "Field SC/SI completely corresponds to marker A/D; no independent S-locus effect",
            "Same-season lifetime seed count and flowering are not a future causal forecast",
            "All four entire sites held out, but only one source study is represented",
            "No posthoc guild selection, penalty re-tuning, site omission or source redistribution",
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-zip", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    result = analyze(args.source_zip)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "analysis": result["experiment_id"],
        "eligible": result["eligible_field_plants"],
        "M0_mse": result["pooled"]["M0"]["mse"],
        "M1_mse": result["pooled"]["M1"]["mse"],
        "M3_mse": result["pooled"]["M3"]["mse"],
        "primary_delta_mse": result["primary_M0_minus_M3_mse"],
        "site_folds_positive": result["positive_folds"],
        "decision": result["frozen_decision"],
    }, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
