#!/usr/bin/env python3
"""Frozen 2026 Lupinus source-only genotype-blocked phenology→seed proxy analysis.

Requires Git ancestry containing prior protocol SHA. Original workbook read from
official Figshare in runner memory, with aggregate outcomes only published.
No intervention codebook decoding, SNP variation, individual IDs or raw rows.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import argparse
import hashlib
import json
import math
import random
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research/rescue_coupling"))
from audit_lupinus_id_linkage import data_to_sparse_rows, download

FREEZE = "28938fe193d01d7eca5bd2fe776f37ecb1f58e27"
ARTICLE = 29606180
NAME = "Lupinus_angustifolius_data_field.xlsx"
COLS = {"id", "genotype", "population", "line", "flowering_onset", "number_of_seeds"}
LINES = ("C", "J", "L", "R", "T", "X")
FOLDS = 5
BOOT = 1000
RNG_SEED = 20261124

class SourceStop(Exception):
    pass

def freeze_gate():
    subprocess.run(["git", "merge-base", "--is-ancestor", FREEZE, "HEAD"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

def clean(value):
    return str(value or "").strip()

def numeric(value):
    s = clean(value)
    if not s or s.casefold() in {"na", "n/a", "nan", "null", "#n/a", "none"}:
        return None
    try:
        x = float(s)
    except (ValueError, OverflowError):
        return None
    return x if math.isfinite(x) else None

def fold_of(key):
    return int.from_bytes(hashlib.sha256(key.encode("utf8")).digest()[:4], "big") % FOLDS

def solve(A, b):
    n = len(b)
    rows = [list(A[i]) + [b[i]] for i in range(n)]
    for i in range(n):
        pivot = max(range(i, n), key=lambda r: abs(rows[r][i]))
        if abs(rows[pivot][i]) < 1e-12:
            raise SourceStop("MATRIX_SINGULAR_STOP")
        rows[i], rows[pivot] = rows[pivot], rows[i]
        div = rows[i][i]
        for j in range(i, n + 1):
            rows[i][j] /= div
        for r in range(n):
            if r == i:
                continue
            scale = rows[r][i]
            for j in range(i, n + 1):
                rows[r][j] -= scale * rows[i][j]
    return [r[-1] for r in rows]

def features(row, onset_included, mu, sd):
    pop, code, _group, onset, _seeds = row
    x = [1.0, float(pop == "PIC")] + [float(code == c) for c in LINES[1:]]
    if onset_included:
        x.append((onset - mu) / sd)
    return x

def fit_predict(train, test, onset_included):
    mu = sum(x[3] for x in train) / len(train)
    var = sum((x[3] - mu)**2 for x in train) / len(train)
    sd = math.sqrt(var) if var > 1e-15 else 1.0
    X = [features(row, onset_included, mu, sd) for row in train]
    dim = len(X[0])
    A = [[0.0] * dim for _ in range(dim)]
    b = [0.0] * dim
    for x, row in zip(X, train):
        y = math.log1p(row[4])
        for i in range(dim):
            b[i] += x[i] * y
            for j in range(dim):
                A[i][j] += x[i] * x[j]
    for i in range(1, dim):
        A[i][i] += 1.0  # lambda=1, intercept unpenalized
    beta = solve(A, b)
    return [sum(v * w for v, w in zip(features(row, onset_included, mu, sd), beta))
            for row in test]

def prepare(rows):
    if len(rows) != 3024:
        raise SourceStop("SOURCE_ROW_COUNT_MISMATCH")
    counts = {"population": Counter(), "line": Counter()}
    distinct_genotypes = set()
    records = []
    missing, flags = Counter(), Counter()
    for row in rows:
        pop, code, g = [clean(row.get(k)) for k in ("population", "line", "genotype")]
        counts["population"][pop] += 1
        counts["line"][code] += 1
        if pop not in {"FRO", "PIC"} or code not in LINES or not g:
            missing["invalid_core_labels"] += 1
            continue
        group = pop + "|" + g
        distinct_genotypes.add(group)
        y = numeric(row.get("number_of_seeds"))
        onset = numeric(row.get("flowering_onset"))
        if y is None:
            missing["missing_or_nonnumeric_seed"] += 1
        if onset is None:
            missing["missing_or_nonnumeric_flowering_onset"] += 1
        if y is not None:
            if y < 0 or abs(y - round(y)) > 1e-7:
                raise SourceStop("SOURCE_ENDPOINT_INVALID_STOP")
            if y == 0:
                flags["explicit_zero_seeds"] += 1
        if onset is not None and onset < 0:
            raise SourceStop("SOURCE_NEGATIVE_FLOWERING_ONSET_STOP")
        if y is not None and onset is None:
            flags["numeric_seed_missing_onset"] += 1
        if y is None or onset is None:
            continue
        records.append((pop, code, group, onset, y))
    if counts["population"] != Counter({"FRO": 1584, "PIC": 1440}):
        raise SourceStop("SOURCE_POPULATION_DENOMINATOR_MISMATCH")
    if counts["line"] != Counter({"C": 720, "J": 648, "L": 720,
                                 "R": 144, "T": 720, "X": 72}):
        raise SourceStop("SOURCE_LINE_DENOMINATOR_MISMATCH")
    if len(distinct_genotypes) != 84:
        raise SourceStop("SOURCE_GENOTYPE_LABEL_MISMATCH")
    return records, missing, flags, len(distinct_genotypes)

def evaluate(records):
    groups = {i: {r[2] for r in records if fold_of(r[2]) == i}
              for i in range(FOLDS)}
    if any(len(groups[i]) < 3 or
           sum(fold_of(r[2]) == i for r in records) < 10 for i in range(FOLDS)):
        raise SourceStop("INSUFFICIENT_FOLD_SUPPORT")
    fold_rows = []
    all_err0, all_err1, all_keys = [], [], []
    for i in range(FOLDS):
        train = [r for r in records if fold_of(r[2]) != i]
        test = [r for r in records if fold_of(r[2]) == i]
        p0 = fit_predict(train, test, False)
        p1 = fit_predict(train, test, True)
        e0 = [(math.log1p(r[4]) - p)**2 for r,p in zip(test,p0)]
        e1 = [(math.log1p(r[4]) - p)**2 for r,p in zip(test,p1)]
        mse0, mse1 = sum(e0)/len(test), sum(e1)/len(test)
        fold_rows.append({"fold": i, "n_records": len(test),
                          "n_genotype_groups": len(groups[i]),
                          "M0_MSE": mse0, "M1_MSE": mse1,
                          "gain_M0_minus_M1": mse0-mse1})
        all_err0 += e0
        all_err1 += e1
        all_keys += [r[2] for r in test]
    m0, m1 = sum(all_err0)/len(records), sum(all_err1)/len(records)
    group_err = defaultdict(list)
    for key, e0, e1 in zip(all_keys, all_err0, all_err1):
        group_err[key].append((e0,e1))
    keys = sorted(group_err)
    rng = random.Random(RNG_SEED)
    boot = []
    for _ in range(BOOT):
        draws = [keys[rng.randrange(len(keys))] for _ in keys]
        num, den = 0.0, 0
        for key in draws:
            for e0,e1 in group_err[key]:
                num += e0-e1
                den += 1
        boot.append(num/den)
    boot.sort()
    wins = sum(x["gain_M0_minus_M1"] > 0 for x in fold_rows)
    return {
        "n_complete_cases": len(records), "n_genotype_groups": len(keys),
        "M0_MSE": m0, "M1_MSE": m1, "gain_M0_minus_M1": m0-m1,
        "fold_wins": wins, "fold_results": fold_rows,
        "fixed_prediction_cluster_bootstrap_95pct": [boot[24], boot[975]],
        "bootstrap_is_not_full_model_refit": True,
        "decision": ("WITHIN_PROGRAMME_PREDICTIVE_INCREMENT"
                     if m0 > m1 and wins >= 4
                     else "NO_ROBUST_WITHIN_PROGRAMME_INCREMENT")
    }

def run():
    freeze_gate()
    m = json.loads(download(f"https://api.figshare.com/v2/articles/{ARTICLE}").decode("utf8"))
    doi = str(m.get("doi", "")).lower().removeprefix("https://doi.org/")
    if not (doi == "10.6084/m9.figshare.29606180" or
            doi.startswith("10.6084/m9.figshare.29606180.v")):
        raise SourceStop("SOURCE_DOI_MISMATCH")
    files = [f for f in m.get("files", []) if f.get("name") == NAME]
    if len(files) != 1:
        raise SourceStop("SOURCE_FILE_NOT_UNIQUE")
    url = files[0].get("download_url", "")
    if urlparse(url).scheme != "https" or urlparse(url).hostname not in {
            "figshare.com", "ndownloader.figshare.com", "api.figshare.com"}:
        raise SourceStop("UNREGISTERED_DOWNLOAD_HOST")
    blob = download(url)
    sha = hashlib.sha256(blob).hexdigest()
    header, rows = data_to_sparse_rows(blob, "xl/worksheets/sheet2.xml", COLS)
    if not COLS.issubset(set(header)):
        raise SourceStop("SOURCE_FIELD_HEADERS_CHANGED")
    records, missing, flags, ngroups = prepare(rows)
    result = {
        "status": "FROZEN_SOURCE_OUTCOME_AUDIT_COMPLETE",
        "frozen_protocol_commit": FREEZE,
        "source_article_id": ARTICLE, "source_workbook_sha256": sha,
        "source_rows": len(rows), "genotype_labels_in_source": ngroups,
        "source_missingness_aggregate": dict(sorted(missing.items())),
        "source_measurement_flags_aggregate": dict(sorted(flags.items())),
        "individual_source_data_redistributed": False,
        "genomic_marker_values_read": False,
        "genetic_intervention_effect_estimated": False,
        "natural_genetic_interaction_function_validation": False,
        "scope": "within-2026 same-season observed flowering-onset vs seed-count proxy only",
    }
    result.update(evaluate(records))
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    try:
        result = run()
    except (SourceStop, HTTPError, URLError, ValueError, KeyError, TypeError,
            IndexError, subprocess.CalledProcessError) as e:
        result = {
            "status": "SOURCE_OR_FROZEN_ANALYSIS_STOP",
            "reason_type": type(e).__name__,
            "reason": str(e)[:120] if isinstance(e, SourceStop) else type(e).__name__,
            "frozen_protocol_commit": FREEZE,
            "individual_source_data_redistributed": False,
            "genomic_marker_values_read": False,
            "genetic_intervention_effect_estimated": False,
            "natural_genetic_interaction_function_validation": False,
        }
        if isinstance(e, HTTPError):
            result["http_status"] = e.code
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
