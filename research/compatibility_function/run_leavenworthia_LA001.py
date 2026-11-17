#!/usr/bin/env python3
"""LA001: source-hashed Leavenworthia individual visit-to-seed holdout.

Pure standard-library OOXML reader; does not redistribute any source workbook,
raw plant ID, individual phenotype, visit trace, or S-locus genotype sequence.
The frozen scientific protocol is LA001_FROZEN_VISIT_SEED_PROTOCOL_20261117.json.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
from io import BytesIO
import json
import math
from pathlib import Path
import posixpath
import re
from statistics import fmean
import zipfile
from xml.etree import ElementTree as ET

NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
SOURCE_SHA = "82bcaa1c3a504cc779bc9c2aa95199a657dd404b3fdf62f7059e4ff5028b39c1"
PROTOCOL_COMMIT = "78af346b100b70c61bc12eb71f4d57afe7f28722"
SITES = ("Waco", "Quarry", "24-43", "Landersville")
SITE_ID = {name: i + 1 for i, name in enumerate(SITES)}
EFFECTIVE = frozenset({"AH", "BF"})
MODELS = ("M0_baseline", "M1_effective_visits", "M2_all_visits")


def colnum(address: str) -> int:
    prefix = re.match(r"^[A-Z]+", address)
    if prefix is None:
        raise ValueError("Not an A1-style source address")
    n = 0
    for char in prefix.group():
        n = 26 * n + ord(char) - 64
    return n - 1


def sheets(outer: zipfile.ZipFile, name: str) -> dict[str, dict[int, dict[int, object]]]:
    data = outer.read(name)
    with zipfile.ZipFile(BytesIO(data)) as source:
        if source.testzip() is not None:
            raise ValueError("Original inner XLSX CRC failure: " + name)
        wb = ET.fromstring(source.read("xl/workbook.xml"))
        links = {
            entry.attrib["Id"]: entry.attrib["Target"]
            for entry in ET.fromstring(source.read("xl/_rels/workbook.xml.rels"))
        }
        shared = []
        if "xl/sharedStrings.xml" in source.namelist():
            nodes = ET.fromstring(source.read("xl/sharedStrings.xml"))
            shared = [
                "".join((t.text or "") for t in si.findall(".//m:t", NS))
                for si in nodes.findall("m:si", NS)
            ]
        result = {}
        for sh in wb.findall("m:sheets/m:sheet", NS):
            target = links[sh.attrib["{" + NS["r"] + "}id"]]
            path = (target.lstrip("/") if target.startswith("/")
                    else posixpath.normpath(posixpath.join("xl", target)))
            rows = {}
            root = ET.fromstring(source.read(path))
            for row in root.findall(".//m:sheetData/m:row", NS):
                cells = {}
                for cell in row.findall("m:c", NS):
                    value = cell.find("m:v", NS)
                    dtype = cell.get("t", "n")
                    if dtype == "s" and value is not None:
                        token = shared[int(value.text)]
                    elif dtype == "inlineStr":
                        token = "".join(t.text or "" for t in cell.findall(".//m:t", NS))
                    elif dtype in ("str", "e", "b"):
                        token = value.text if value is not None else None
                    elif value is None:
                        token = None
                    else:
                        token = float(value.text)
                    if token is not None:
                        cells[colnum(cell.attrib["r"])] = token
                rows[int(row.attrib["r"])] = cells
            result[sh.attrib["name"]] = rows
        return result


def value(row: dict, col: int):
    return row.get(col)


def positive_int(obj) -> int:
    v = int(obj)
    if float(obj) != v:
        raise ValueError("Unexpected noninteger source value")
    return v


def draw_source(source_zip: Path) -> tuple[dict, list[dict]]:
    if hashlib.sha256(source_zip.read_bytes()).hexdigest() != SOURCE_SHA:
        raise ValueError("Original Dryad archive SHA256 mismatch")
    with zipfile.ZipFile(source_zip) as outer:
        if outer.testzip() is not None:
            raise ValueError("Outer Dryad ZIP CRC mismatch")
        field = sheets(outer, "2014+2015+Field+data.xlsx")["Sheet1"]
        genes = {
            2014: sheets(outer, "S-locus+Genotyping+2014.xlsx")["Sheet1"],
            2015: sheets(outer, "S-locus+genotyping+2015.xlsx")["Sheet1"],
        }
        poll = {
            2014: sheets(outer, "Pollinator+Data+2014.xlsx"),
            2015: sheets(outer, "Pollinator+Data+2015.xlsx"),
        }
    field_by_key = {}
    locus_key = {}
    for year in (2014, 2015):
        col = 2 if year == 2014 else 5
        rows = genes[year]
        for rno, row in rows.items():
            if rno == 1:
                continue
            if not isinstance(value(row, 0), (int, float)) or not isinstance(value(row, 1), (int, float)):
                continue
            key = (year, positive_int(value(row, 0)), positive_int(value(row, 1)))
            if key in locus_key:
                raise ValueError("Duplicate S-locus family and plant code")
            locus_key[key] = value(row, col)
    for rno, row in field.items():
        if rno == 1:
            continue
        yc = str(value(row, 0))
        y = {"1": 2014, "2": 2015}.get(yc)
        if y is None:
            raise ValueError("Unexpected field year code")
        site = positive_int(value(row, 1))
        pid = str(value(row, 2)).strip()
        if not re.fullmatch(r"\d+-\d+", pid):
            raise ValueError("Invalid field plant ID syntax")
        fam, individual = map(int, pid.split("-"))
        if positive_int(value(row, 3)) != fam:
            raise ValueError("Field family column conflicts with individual label")
        key = (y, site, pid)
        if key in field_by_key:
            raise ValueError("Duplicate site/year individual")
        coded = positive_int(value(row, 4))
        if coded not in (0, 1):
            raise ValueError("Genotype code outside SC/SI")
        locus = locus_key.get((y, fam, individual))
        if locus != ("A" if coded == 0 else "D"):
            raise ValueError("S-marker not exactly linked or confounded as predicted")
        field_by_key[key] = row
    if len(field_by_key) != 256:
        raise ValueError("Field source row count != 256")

    # Decode source event-position sequence, not spreadsheet column as plant ID.
    # Position maps come only from the correct site×year First Flower array.
    plant_exposure = {}
    meta = {"completed_sessions": 0, "open_flower_session_rows": 0,
            "valid_source_position_visits": 0, "out_of_range_visits": 0,
            "zero_open_flower_visits": 0, "source_total_mismatches": 0,
            "site_year_sessions": {}}
    for year in (2014, 2015):
        first = poll[year]["First Flower"]
        for site_label in SITES:
            site = SITE_ID[site_label]
            col = {2014: {"Waco": 10, "Quarry": 2, "24-43": 14, "Landersville": 6},
                   2015: {"Waco": 9, "Quarry": 1, "24-43": 13, "Landersville": 5}}[year][site_label]
            poscol = col - 1 if year == 2014 else col + 1
            pos_to_pid = {}
            for rno in range(5, 37):
                r = first.get(rno, {})
                pid = value(r, col)
                pos = value(r, poscol)
                if not isinstance(pid, str) or not isinstance(pos, (int, float)):
                    raise ValueError("Missing First Flower position, plant and ID")
                pn = positive_int(pos)
                if pn in pos_to_pid:
                    raise ValueError("Duplicated position in first-flower map")
                pos_to_pid[pn] = pid.strip()
                key = (year, site, pid.strip())
                if key not in field_by_key:
                    raise ValueError("Position map does not join to field plant")
                g = positive_int(value(field_by_key[key], 4))
                first_genotype = value(r, 0)
                if first_genotype != ("SC" if g == 0 else "SI"):
                    raise ValueError("First Flower genotype mismatch")
            if set(pos_to_pid) != set(range(1, 33)):
                raise ValueError("Incomplete 32-position site/year array")
            table = poll[year]["Quarry Array" if year == 2014 and site_label == "Quarry"
                               else site_label]
            hdr_row = 3 if year == 2014 else 2
            for pos in range(1, 33):
                gt = value(table[hdr_row], pos + 6)
                g = positive_int(value(field_by_key[(year, site, pos_to_pid[pos])], 4))
                if gt != ("SC" if g == 0 else "SI"):
                    raise ValueError("Array genotype row conflicts with field source")
            periods = []
            current = None
            for rno, row in sorted(table.items()):
                status = value(row, 5)
                taxon = value(row, 6)
                if isinstance(status, str) and status.strip().lower() == "open flowers":
                    current = {"row": rno, "open": [value(row, c) for c in range(7, 39)],
                               "visits": [], "reported": None}
                    periods.append(current)
                elif isinstance(status, str) and status.strip().lower() == "total":
                    if current is not None:
                        current["reported"] = taxon
                elif isinstance(taxon, str) and taxon.strip() and (
                    isinstance(status, (int, float)) or str(status).isdigit()
                ):
                    if current is None:
                        raise ValueError("Pollinator event without an Open Flowers context")
                    for c in range(7, 200):
                        event = value(row, c)
                        if event is None:
                            continue
                        if not isinstance(event, (int, float)) or float(event) != int(event):
                            raise ValueError("Unexpected non-position value in pollinator visit sequence")
                        current["visits"].append((int(event), taxon.upper().strip()))
            complete = [p for p in periods if p["reported"] is not None]
            if any(p["visits"] for p in periods if p["reported"] is None):
                raise ValueError("Incomplete observation period contains visits")
            meta["completed_sessions"] += len(complete)
            meta["open_flower_session_rows"] += len(periods)
            meta["site_year_sessions"][f"{year}:{site_label}"] = len(complete)
            counts = {pos: {"flower_hours": 0.0, "effective": 0, "all": 0} for pos in range(1, 33)}
            for period in complete:
                if len(period["open"]) != 32:
                    raise ValueError("Missing 32 flower-open observations")
                for pos in range(1, 33):
                    flowers = period["open"][pos - 1]
                    if not isinstance(flowers, (int, float)) or flowers < 0:
                        raise ValueError("Missing or invalid open flower exposure")
                    counts[pos]["flower_hours"] += 0.5 * flowers
                source_token_count = 0
                for pos, taxon in period["visits"]:
                    source_token_count += 1
                    if not 1 <= pos <= 32:
                        meta["out_of_range_visits"] += 1
                        continue
                    meta["valid_source_position_visits"] += 1
                    if period["open"][pos - 1] <= 0:
                        meta["zero_open_flower_visits"] += 1
                        continue
                    counts[pos]["all"] += 1
                    if taxon in EFFECTIVE:
                        counts[pos]["effective"] += 1
                if not isinstance(period["reported"], (int, float)):
                    raise ValueError("Non-numeric source TOTAL")
                if int(period["reported"]) != source_token_count:
                    meta["source_total_mismatches"] += 1
            for pos, pid in pos_to_pid.items():
                if counts[pos]["flower_hours"] <= 0:
                    raise ValueError("No measurable plant flower-hour exposure")
                plant_exposure[(year, site, pid)] = counts[pos]
    if (meta["completed_sessions"], meta["open_flower_session_rows"],
        meta["valid_source_position_visits"], meta["out_of_range_visits"],
        meta["zero_open_flower_visits"]) != (121, 125, 6701, 1, 38):
        raise ValueError("Source-only visitation coding changed; stop, do not retune")
    if meta["source_total_mismatches"] != 0:
        raise ValueError("TOTAL values differ from raw event sequence tokens")
    if len(plant_exposure) != 256:
        raise ValueError("Source plants with exposure != 256")
    dataset = []
    missing_seed = 0
    for (year, site, pid), row in field_by_key.items():
        seed_count = value(row, 10)
        if seed_count is None:
            missing_seed += 1
            continue
        flowers, day = value(row, 5), value(row, 9)
        if any(not isinstance(x, (int, float)) for x in (seed_count, flowers, day)):
            raise ValueError("Seed, flower or flowering-date column not numeric")
        if min(seed_count, flowers, day) < 0:
            raise ValueError("Negative source outcome/covariate")
        e = plant_exposure[(year, site, pid)]
        sc = int(positive_int(value(row, 4)) == 0)
        dataset.append({
            "site": site, "year": year, "SC": sc,
            "y": math.log1p(seed_count),
            "baseline": [int(year == 2015), sc, int(year == 2015) * sc,
                         math.log1p(flowers), day / 30.0],
            "effective": math.log1p(e["effective"] / e["flower_hours"]),
            "total": math.log1p(e["all"] / e["flower_hours"]),
        })
    if missing_seed != 4 or len(dataset) != 252:
        raise ValueError("Focal complete-data denominator changed")
    return meta, dataset


def solve(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    for j in range(n):
        k = max(range(j, n), key=lambda i: abs(m[i][j]))
        if abs(m[k][j]) < 1e-12:
            raise ValueError("Non-invertible design even with fixed ridge")
        m[j], m[k] = m[k], m[j]
        factor = m[j][j]
        for c in range(j, n + 1):
            m[j][c] /= factor
        for i in range(n):
            if i == j:
                continue
            mult = m[i][j]
            for c in range(j, n + 1):
                m[i][c] -= mult * m[j][c]
    return [row[-1] for row in m]


def features(row: dict, model: str) -> list[float]:
    base = row["baseline"]
    if model == "M0_baseline":
        return base
    if model == "M1_effective_visits":
        return base + [row["effective"]]
    if model == "M2_all_visits":
        return base + [row["total"]]
    raise ValueError("Unregistered model")


def ridge_predict(train: list[dict], holdout: list[dict], model: str) -> list[float]:
    raw = [features(r, model) for r in train]
    p = len(raw[0])
    means = [fmean(x[j] for x in raw) for j in range(p)]
    scales = []
    for j in range(p):
        v = math.sqrt(fmean((x[j] - means[j]) ** 2 for x in raw))
        scales.append(v if v > 1e-10 else 1.0)
    X = [[1.0] + [(row[j] - means[j]) / scales[j] for j in range(p)]
         for row in raw]
    A = [[sum(x[j] * x[k] for x in X) + (1.0 if j == k and j > 0 else 0.0)
          for k in range(p + 1)] for j in range(p + 1)]
    z = [sum(x[j] * r["y"] for x, r in zip(X, train)) for j in range(p + 1)]
    coef = solve(A, z)
    return [
        coef[0] + sum(coef[j + 1] * (features(r, model)[j] - means[j]) / scales[j]
                      for j in range(p))
        for r in holdout
    ]


def analyze(meta: dict, rows: list[dict]) -> dict:
    folds = []
    for site in range(1, 5):
        train = [r for r in rows if r["site"] != site]
        test = [r for r in rows if r["site"] == site]
        if len(train) + len(test) != 252 or len(test) < 50:
            raise ValueError("Invalid four-site CV fold denominator")
        preds = {model: ridge_predict(train, test, model) for model in MODELS}
        by_model = {}
        for model in MODELS:
            diff = [r["y"] - pred for r, pred in zip(test, preds[model])]
            by_model[model] = {
                "mse_log1p_seed_total": fmean(e * e for e in diff),
                "mae_log1p_seed_total": fmean(abs(e) for e in diff),
            }
        folds.append({
            "site": SITES[site - 1], "n": len(test),
            "models": by_model,
            "delta_mse_M0_minus_M1": (
                by_model["M0_baseline"]["mse_log1p_seed_total"] -
                by_model["M1_effective_visits"]["mse_log1p_seed_total"]
            ),
            "delta_mse_M2_minus_M1": (
                by_model["M2_all_visits"]["mse_log1p_seed_total"] -
                by_model["M1_effective_visits"]["mse_log1p_seed_total"]
            ),
        })
    if sum(f["n"] for f in folds) != 252:
        raise ValueError("Holdout accounting is incomplete")
    pooled = {}
    for model in MODELS:
        pooled[model] = {
            "mse_log1p_seed_total": sum(f["n"] * f["models"][model]["mse_log1p_seed_total"]
                                       for f in folds) / 252,
            "mae_log1p_seed_total": sum(f["n"] * f["models"][model]["mae_log1p_seed_total"]
                                       for f in folds) / 252,
        }
    delta = pooled["M0_baseline"]["mse_log1p_seed_total"] - pooled["M1_effective_visits"]["mse_log1p_seed_total"]
    positive_folds = sum(f["delta_mse_M0_minus_M1"] > 0 for f in folds)
    verdict = ("bounded_within_programme_predictive_gain"
               if delta > 0 and positive_folds >= 3
               else "NO_ROBUST_SINGLE_PROGRAMME_INCREMENT")
    return {
        "analysis_id": "LA001_leavenworthia_site_holdout_visit_seed_v1",
        "status": "original_archive_source_pinned_completed",
        "preregistered_protocol_commit": PROTOCOL_COMMIT,
        "raw_archive_sha256": SOURCE_SHA,
        "n_source_field_plants": 256, "n_eligible_plants": 252,
        "n_independent_sites": 4, "n_site_years": 8,
        "source_only_validation": meta,
        "holdout_folds": folds,
        "pooled": pooled,
        "primary_delta_mse_M0_minus_M1": delta,
        "positive_site_fold_count": positive_folds,
        "frozen_decision": verdict,
        "secondary_M2_minus_M1_mse": (
            pooled["M2_all_visits"]["mse_log1p_seed_total"] -
            pooled["M1_effective_visits"]["mse_log1p_seed_total"]
        ),
        "claim_ceiling": [
            "Same original 2017 four-site programme; not independent species/system replication",
            "SC/SI marker genotype and S-locus genotype call are perfectly confounded in field subjects",
            "Visits by effective guilds approximate visitation quality, not directly compatible pollen",
            "Seed total is lifetime seed count, not viable offspring or next-cohort recruitment",
            "Four site folds provide limited independent units; no naive plant-level p value",
            "Correlational predictive increment is not causal mediation or genetic rescue",
            "No parameter tuning or posthoc outcome substitution after frozen protocol",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source-zip", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    source, records = draw_source(args.source_zip)
    result = analyze(source, records)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "analysis_id": result["analysis_id"], "n": result["n_eligible_plants"],
        "primary_delta_mse": result["primary_delta_mse_M0_minus_M1"],
        "positive_site_folds": result["positive_site_fold_count"],
        "decision": result["frozen_decision"],
        "site_deltas": {f["site"]: f["delta_mse_M0_minus_M1"] for f in result["holdout_folds"]},
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
