#!/usr/bin/env python3
"""Post-outcome SF06 mean I–F contrast: publication-cluster sensitivity audit.

Exploratory only; neither a new independent primary study nor confirmation of
any universal process→function amplification. Stdlib only, no source download.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
SOURCE_BLOB = "80edf240425c0e4439a276176bc1996c651fab92"

def avg(vals):
    return sum(vals) / len(vals)

def quantile(vals, fraction):
    vals = sorted(vals)
    return vals[int(fraction * (len(vals) - 1))]

def run(source=SRC, bootstrap=8000, seed=20261117):
    content = Path(source).read_bytes()
    blob = hashlib.sha1(
        b"blob " + str(len(content)).encode() + b"\0" + content
    ).hexdigest()
    if blob != SOURCE_BLOB:
        raise ValueError("Source-locked SF06 pair table was modified: " + blob)
    allrows = list(csv.DictReader(content.decode("utf-8-sig").splitlines()))
    if len(allrows) != 59:
        raise ValueError("Expected 59 exact I–F paired units in public-S1 subset")
    observed_keys = set()
    selected = []
    for r in allrows:
        key = (r["source_publication_key"], r["species"], r["land_use_factor_normalized"])
        if key in observed_keys:
            raise ValueError("Duplicate paired source key: " + repr(key))
        observed_keys.add(key)
        if r["land_use_factor_normalized"] != "habitat fragmentation":
            continue
        if r["numeric_model_eligible"] != "yes":
            raise ValueError("Fragmentation pair changed eligibility")
        di, df, delta = (float(r[k]) for k in ("d_I", "d_F", "delta_F_minus_I"))
        if not all(math.isfinite(v) for v in (di, df, delta)):
            raise ValueError("Nonfinite matched outcome")
        if abs(df - di - delta) > 1e-9:
            raise ValueError("Stored delta does not equal d_F minus d_I")
        selected.append((r["source_publication_key"], di, df, delta))
    by_pub = defaultdict(list)
    for row in selected:
        by_pub[row[0]].append(row)
    n, g = len(selected), len(by_pub)
    if (n, g) != (55, 33):
        raise ValueError("Expected 55 fragmentation pairs from 33 publications")
    pubs = sorted(by_pub)
    d = [r[3] for r in selected]
    m = avg(d)
    means = [avg([r[3] for r in by_pub[p]]) for p in pubs]
    mb = avg(means)
    cr1 = math.sqrt(
        (g / (g - 1))
        * sum(sum(x[3] - m for x in by_pub[p]) ** 2 for p in pubs)
        / (n * n)
    )
    mb_se = math.sqrt(sum((x - mb) ** 2 for x in means) / (g * (g - 1)))
    pub_loo = [
        avg([r[3] for r in selected if r[0] != pub]) for pub in pubs
    ]
    rng = random.Random(seed)
    bs, bs_bal = [], []
    for _ in range(bootstrap):
        sample = [by_pub[pubs[rng.randrange(g)]] for __ in range(g)]
        bs.append(avg([r[3] for pubrows in sample for r in pubrows]))
        bs_bal.append(avg([avg([r[3] for r in pubrows]) for pubrows in sample]))
    neg, pos = sum(x < 0 for x in d), sum(x > 0 for x in d)
    if (neg, pos) != (29, 26):
        raise ValueError("Paired direction census changed")
    # Independent arithmetic invariants, not after-the-fact significance gates.
    if abs(m + 0.00853724104650449) > 1e-9:
        raise ValueError("Unweighted matched mean arithmetic mismatch")
    if abs(mb + 0.05343412228289471) > 1e-9:
        raise ValueError("Publication-balanced matched mean arithmetic mismatch")
    return {
        "status": "post_outcome_exploratory_no_confirmatory_p_value",
        "source": "Aguilar et al. 2024-online/2025-volume, public S1 subset",
        "source_pair_table_git_blob_sha1": blob,
        "source_coverage": "426 accessible effect rows; original paper reports 500",
        "estimator": "paired Hedges d_F minus d_I, NOT a biological-scale ratio",
        "within_pair_covariance": "unavailable; do not inverse-variance test d_F-d_I",
        "n_all_land_use_pairs": len(allrows),
        "n_fragmentation_pairs": n,
        "n_publications": g,
        "mean_d_I": avg([r[1] for r in selected]),
        "mean_d_F": avg([r[2] for r in selected]),
        "mean_delta": m,
        "pub_cluster_CR1_SE": cr1,
        "pub_cluster_normal_reference_95pct": [m - 1.96 * cr1, m + 1.96 * cr1],
        "pub_cluster_bootstrap_95pct": [quantile(bs, .025), quantile(bs, .975)],
        "publication_balanced_mean_delta": mb,
        "publication_balanced_SE": mb_se,
        "publication_balanced_bootstrap_95pct": [quantile(bs_bal, .025), quantile(bs_bal, .975)],
        "negative_delta_pairs": neg,
        "positive_delta_pairs": pos,
        "publication_leave_one_out_mean_min": min(pub_loo),
        "publication_leave_one_out_mean_max": max(pub_loo),
        "bootstrap_seed": seed,
        "bootstrap_draws": bootstrap,
        "scope_limit": (
            "Not an equivalence test, prevalence estimate, or independent replication. "
            "Paired effects use different biological endpoint SDs; the subset has "
            "nonrandom publications and overlaps prior EGWEE source programmes."
        ),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SRC)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--bootstrap", type=int, default=8000)
    a = parser.parse_args()
    if a.bootstrap < 1000:
        parser.error("Require >=1000 whole-publication resamples")
    result = run(a.source, a.bootstrap)
    value = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if a.output:
        a.output.write_text(value, encoding="utf-8")
    else:
        print(value, end="")

if __name__ == "__main__":
    main()
