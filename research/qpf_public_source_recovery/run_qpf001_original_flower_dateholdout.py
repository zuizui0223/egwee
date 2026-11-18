#!/usr/bin/env python3
"""QPF001: same-flower visits -> CP/HP pollen -> original seed set, day held out.

Pure standard-library source decoder and Gaussian ridge. Original user-supplied
Dryad ZIP (or original XLSX) required locally. Never uploads workbook/individual
flower records or prints source row values. Exact pre-outcome protocol SHA
a1658c353a0c244edafab194f96301968dc84040 must be an ancestor of HEAD.
"""
from __future__ import annotations

import argparse
from collections import Counter
from io import BytesIO
import hashlib
import json
import math
from pathlib import Path
import re
from statistics import mean, median, pstdev
import subprocess
import zipfile
from xml.etree import ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "QPF001_FROZEN_DATE_POLLEN_SEED_PROTOCOL_20261118.json"
PROTOCOL_REL = "research/qpf_public_source_recovery/QPF001_FROZEN_DATE_POLLEN_SEED_PROTOCOL_20261118.json"
FREEZE_SHA = "a1658c353a0c244edafab194f96301968dc84040"
ARCHIVE_SHA = "09a47a94913c7087405679c5dc18c0c3c6ded4e8ecad298e6f94f87c5a78b653"
ORIGINAL_XLSX = "FIGO_2019_Data_20210523.xlsx"
XLSX_SHA = "83790bb7d63222e3e21c0ceed5d729cacf63a2df843e5807836d8e5c853447aa"
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
DAYS = (176, 177, 178, 182, 183, 190, 191, 196)
SEED_COMPLETE_BY_DAY = {176: 16, 177: 18, 178: 18, 182: 18,
                        183: 7, 190: 4, 191: 8, 196: 4}
HEADERS = (
    "Sample.number", "Date.film", "Julian.day", "Duration.hours",
    "Large.bee.visits", "Small.bee.visits", "Small.fly.visits",
    "Large.fly.visits", "Large.bee.bin", "Small.bee.bin", "Small.fly.bin",
    "Large.fly.bin", "Het.abundance", "Con.abundance", "Total.abundance",
    "CP.Count", "HP.Count", "Pollen.weight", "Seed.count", "Small.seed",
    "Ovule", "Seed.set", "Seed.weights", "Comments",
)


def verify_protocol() -> None:
    original = subprocess.check_output(
        ["git", "show", FREEZE_SHA + ":" + PROTOCOL_REL], cwd=ROOT
    )
    if original != PROTOCOL.read_bytes():
        raise RuntimeError("QPF001 protocol changed after the pre-outcome freeze")
    subprocess.run(["git", "merge-base", "--is-ancestor", FREEZE_SHA, "HEAD"],
                   cwd=ROOT, check=True)
    info = json.loads(original)
    if info["experiment_id"] != "QPF001_original_flower_stigma_seed_date_holdout_v1":
        raise RuntimeError("Incorrect protocol study family")


def _col(ref: str) -> int:
    m = re.match(r"^[A-Z]+", ref)
    if m is None:
        raise ValueError("Non-A1 original Excel cell address")
    n = 0
    for ch in m.group():
        n = 26 * n + ord(ch) - 64
    return n - 1


def _binary_original(source_zip: Path) -> bytes:
    if hashlib.sha256(source_zip.read_bytes()).hexdigest() != ARCHIVE_SHA:
        raise ValueError("Uploaded ZIP SHA256 is not original Dryad archived source")
    with zipfile.ZipFile(source_zip) as z:
        if z.testzip() is not None or z.namelist() != [ORIGINAL_XLSX]:
            raise ValueError("Original archive member roster or CRC changed")
        raw = z.read(ORIGINAL_XLSX)
    if len(raw) != 27351 or hashlib.sha256(raw).hexdigest() != XLSX_SHA:
        raise ValueError("Original XLSX differs from Dryad file manifest")
    return raw


def _xlsx_data(source_bytes: bytes) -> list[dict]:
    if hashlib.sha256(source_bytes).hexdigest() != XLSX_SHA:
        raise ValueError("Invalid original source workbook digest")
    with zipfile.ZipFile(BytesIO(source_bytes)) as z:
        if z.testzip() is not None:
            raise ValueError("Original XLSX failed CRC")
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        sheet_names = [node.get("name") for node in wb.findall(
            "s:sheets/s:sheet", NS)]
        if sheet_names != ["Metadata", "Data"]:
            raise ValueError("Unexpected original source sheets")
        ss = []
        if "xl/sharedStrings.xml" in z.namelist():
            sr = ET.fromstring(z.read("xl/sharedStrings.xml"))
            ss = [
                "".join(t.text or "" for t in node.findall(".//s:t", NS))
                for node in sr.findall("s:si", NS)
            ]
        root = ET.fromstring(z.read("xl/worksheets/sheet2.xml"))
        data = []
        for row in root.findall(".//s:sheetData/s:row", NS):
            rec = {}
            for cell in row.findall("s:c", NS):
                v = cell.find("s:v", NS)
                dtype = cell.get("t", "n")
                if dtype == "s" and v is not None:
                    value = ss[int(v.text)]
                elif dtype == "inlineStr":
                    value = "".join(x.text or "" for x in cell.findall(".//s:t", NS))
                elif dtype in ("str", "e"):
                    value = v.text if v is not None else None
                elif v is None:
                    value = None
                else:
                    value = float(v.text)
                rec[_col(cell.get("r", ""))] = value
            data.append(rec)
    if len(data) != 123 or tuple(data[0].get(k) for k in range(24)) != HEADERS:
        raise ValueError("Original 122-row or 24-variable source schema changed")
    return [
        {name: rec.get(k) for k, name in enumerate(HEADERS)}
        for rec in data[1:]
    ]


def numeric(x):
    if isinstance(x, (float, int)) and math.isfinite(float(x)):
        return float(x)
    return None


def audit_source(data: list[dict]) -> tuple[list[dict], dict]:
    if len(data) != 122 or len({r["Sample.number"] for r in data}) != 122:
        raise ValueError("Wrong original flower/source identifier denominator")
    if {int(r["Julian.day"]) for r in data} != set(DAYS):
        raise ValueError("Source filming dates have changed")
    for row in data:
        if numeric(row["Duration.hours"]) is None or row["Duration.hours"] <= 0:
            raise ValueError("Invalid filmed hours")
        for key in ("Large.bee.visits", "Small.bee.visits",
                    "Small.fly.visits", "Large.fly.visits",
                    "CP.Count", "HP.Count"):
            if numeric(row[key]) is None or row[key] < 0:
                raise ValueError("Original visitation or pollen source missing/negative")
        for key in ("Con.abundance", "Het.abundance"):
            if numeric(row[key]) is not None and row[key] < 0:
                raise ValueError("Negative source floral abundance")
        if numeric(row["Seed.set"]) is not None and not 0 <= row["Seed.set"] <= 1:
            raise ValueError("Source seed-set proportion outside [0,1]")
    admitted = [r for r in data if numeric(r["Seed.set"]) is not None]
    if len(admitted) != 93 or Counter(int(r["Julian.day"]) for r in admitted) != SEED_COMPLETE_BY_DAY:
        raise ValueError("93-fruit, 8-date outcome denominator is not original")
    missing = lambda r: numeric(r["Con.abundance"]) is None or numeric(r["Het.abundance"]) is None
    if sum(map(missing, data)) != 6 or sum(map(missing, admitted)) != 5:
        raise ValueError("Original floral-context missingness changed")
    matches_source = 0
    matches_paper = 0
    for r in admitted:
        seed, ovules, immature = (numeric(r["Seed.count"]), numeric(r["Ovule"]),
                                   numeric(r["Small.seed"]))
        weight = numeric(r["Seed.weights"])
        if any(x is None or x < 0 for x in (seed, ovules, immature, weight)):
            raise ValueError("Invalid source seed-count or ovule metadata")
        if weight <= 0:
            raise ValueError("Original seed count has an invalid denominator")
        if abs(r["Seed.set"] - seed / weight) < 1e-9:
            matches_source += 1
        if seed + ovules > 0 and abs(r["Seed.set"] - seed/(seed+ovules)) < 1e-9:
            matches_paper += 1
    if (matches_source, matches_paper) != (93, 83):
        raise ValueError("Original seed-set vs paper-expression arithmetic changed")
    return admitted, {
        "n_filmed_flowers": 122, "n_unique_source_IDs": 122,
        "n_seedset_nonmissing": 93, "n_seedset_missing_NA": 29,
        "n_flower_context_missing_any": 6,
        "n_context_missing_among_seed_complete": 5,
        "n_film_days": 8,
        "source_seedset_arithmetic": {
            "n_complete": 93,
            "match_seed_count_over_count_plus_unfertilized_ovules": matches_paper,
            "match_seed_count_over_seed_weights": matches_source,
        },
    }


def make_features(train: list[dict], hold: list[dict],
                  add_pollen: bool) -> tuple[list[list[float]], list[list[float]]]:
    neighbors = ("Con.abundance", "Het.abundance")
    medians = {
        key: median([math.log1p(numeric(r[key])) for r in train
                     if numeric(r[key]) is not None])
        for key in neighbors
    }
    def feature(r):
        result = [float(r["Julian.day"])]
        for key in neighbors:
            n = numeric(r[key])
            result.append(math.log1p(n) if n is not None else medians[key])
        for key in neighbors:
            result.append(int(numeric(r[key]) is None))
        for key in ("Large.bee.visits", "Small.bee.visits",
                    "Small.fly.visits", "Large.fly.visits"):
            result.append(math.log1p(numeric(r[key]) / numeric(r["Duration.hours"])))
        if add_pollen:
            cp, hp = math.log1p(numeric(r["CP.Count"])), math.log1p(numeric(r["HP.Count"]))
            result.extend((cp, hp, cp * hp))
        return result
    return [feature(r) for r in train], [feature(r) for r in hold]


def solve(matrix: list[list[float]], target: list[float]) -> list[float]:
    n = len(target)
    A = [row[:] + [target[i]] for i, row in enumerate(matrix)]
    for j in range(n):
        k = max(range(j, n), key=lambda i: abs(A[i][j]))
        A[j], A[k] = A[k], A[j]
        if abs(A[j][j]) < 1e-11:
            raise ValueError("Ridge normal matrix singular")
        pivot = A[j][j]
        A[j] = [a / pivot for a in A[j]]
        for i in range(n):
            if i == j:
                continue
            mult = A[i][j]
            for col in range(n+1):
                A[i][col] -= mult * A[j][col]
    return [row[-1] for row in A]


def predict(train: list[dict], test: list[dict], add_pollen: bool) -> list[float]:
    tr, te = make_features(train, test, add_pollen)
    dim = len(tr[0])
    means = [mean(row[j] for row in tr) for j in range(dim)]
    scale = [pstdev(row[j] for row in tr) for j in range(dim)]
    scale = [s if s > 1e-10 else 1.0 for s in scale]
    X = [[1.0] + [(v[j]-means[j])/scale[j] for j in range(dim)] for v in tr]
    H = [[1.0] + [(v[j]-means[j])/scale[j] for j in range(dim)] for v in te]
    gram = [[sum(row[j] * row[k] for row in X) +
             (1 if j == k and j > 0 else 0)
             for k in range(dim+1)] for j in range(dim+1)]
    rhs = [sum(z[j] * r["Seed.set"] for z, r in zip(X, train))
           for j in range(dim+1)]
    beta = solve(gram, rhs)
    return [min(1, max(0, sum(row[j] * beta[j] for j in range(dim+1))))
            for row in H]


def analyze(source_zip: Path) -> dict:
    verify_protocol()
    original = _xlsx_data(_binary_original(source_zip))
    rows, receipt = audit_source(original)
    folds = []
    for day in DAYS:
        train = [r for r in rows if int(r["Julian.day"]) != day]
        hold = [r for r in rows if int(r["Julian.day"]) == day]
        if len(hold) != SEED_COMPLETE_BY_DAY[day]:
            raise RuntimeError("Source outcome date-heldout split changed")
        entry = {"day": day, "n": len(hold)}
        for model, include in (("M0", False), ("M1", True)):
            predicted = predict(train, hold, include)
            errors = [p - r["Seed.set"] for p, r in zip(predicted, hold)]
            entry[model+"_mse"] = mean(e*e for e in errors)
            entry[model+"_mae"] = mean(abs(e) for e in errors)
        entry["M0_minus_M1_mse"] = entry["M0_mse"] - entry["M1_mse"]
        folds.append(entry)
    def pool(k):
        return sum(x["n"]*x[k] for x in folds)/len(rows)
    m0, m1 = pool("M0_mse"), pool("M1_mse")
    relative = 100*(m0-m1)/m0
    wins = sum(f["M0_minus_M1_mse"] > 0 for f in folds)
    success = relative >= 5 and wins >= 6
    return {
        "analysis_id": "QPF001_original_flower_stigma_seed_date_holdout_v1",
        "status": "ORIGINAL_SOURCE_FROZEN_EIGHT_DATE_HOLDOUT_COMPLETE",
        "protocol_commit": FREEZE_SHA,
        "original_zip_sha256": ARCHIVE_SHA, "original_xlsx_sha256": XLSX_SHA,
        "original_dataset_doi": "10.5061/dryad.hqbzkh1g9",
        "original_article_doi": "10.1002/ajb2.1720",
        "source_grain": receipt,
        "folds": folds,
        "pooled": {
            "n": len(rows), "M0_mse": m0, "M1_mse": m1,
            "M0_mae": pool("M0_mae"), "M1_mae": pool("M1_mae"),
            "M0_minus_M1_mse": m0-m1,
            "relative_mse_reduction_pct": relative,
            "positive_date_folds": wins, "date_folds": len(DAYS),
        },
        "registered_decision": (
            "BOUNDED_WITHIN_STUDY_DATE_TRANSFER_GAIN" if success
            else "NO_ROBUST_WITHIN_STUDY_DATE_TRANSFER_GAIN"
        ),
        "decision_threshold": "M0-M1 pooled MSE >=5% improvement and >=6/8 positive date folds",
        "causal_limitations": [
            "One study site, one flower per mother, only eight observation dates",
            "Original article already established the HP x CP seed-set interaction",
            "93 mature recovered fruits / 122 filmed flowers: missing outcomes not proven random",
            "Source Seed.set uses Seed.weights denominator including immature seed counts for some flowers",
            "Source pollen grains do not measure genetically compatible paternity or future offspring recruitment",
            "No new urban/island shared regime or universal ecological causal mechanism confirmed",
        ],
        "no_individual_source_rows_exported": True,
        "no_raw_workbook_redistributed": True,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source-zip", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    result = analyze(a.source_zip)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "analysis":result["analysis_id"], "n":result["pooled"]["n"],
        "M0_mse":result["pooled"]["M0_mse"],
        "M1_mse":result["pooled"]["M1_mse"],
        "relative_pct":result["pooled"]["relative_mse_reduction_pct"],
        "positive_day_folds":result["pooled"]["positive_date_folds"],
        "decision":result["registered_decision"],
    }, indent=2))


if __name__ == "__main__":
    main()
