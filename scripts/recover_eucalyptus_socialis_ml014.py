from __future__ import annotations

import csv
import json
import math
import statistics as stats
import urllib.request
from collections import Counter

URL = "https://shared.tern.org.au/attachment/c5278af9-b0c9-4572-8eb4-9ce3058f1b2a/MECBreedfamily.csv"
UA = "Mozilla/5.0 egwee-eucalyptus-socialis-ml014-recovery/1.0"


def fetch_rows() -> list[dict[str, str]]:
    req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept": "text/csv,*/*"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = resp.read()
    text = payload.decode("utf-8-sig")
    physical = [line for line in text.splitlines() if line.strip()]
    rows = list(csv.DictReader(physical))
    required = {"family", "group", "plant height (cm)", "rp"}
    if not rows or not required <= set(rows[0]):
        raise AssertionError(f"unexpected source schema: {list(rows[0]) if rows else []}")
    return rows


def classify_group(label: str) -> str:
    x = label.strip().upper()
    if x == "MONLOW":
        return "fragmented"
    if x == "MONHIGH":
        return "reference"
    if x == "YOOKA":
        return "sensitivity"
    return "unknown"


def hedges_g_metafor_ls(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    m1, m2 = stats.mean(fragmented), stats.mean(reference)
    s1, s2 = stats.stdev(fragmented), stats.stdev(reference)
    df = n1 + n2 - 2
    pooled = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / df)
    d = (m1 - m2) / pooled
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    variance = 1 / n1 + 1 / n2 + g**2 / (2 * (n1 + n2))
    return g, variance


def centered(values: list[float], groups: list[str]) -> list[float]:
    means = {g: stats.mean(v for v, gg in zip(values, groups) if gg == g) for g in set(groups)}
    return [v - means[g] for v, g in zip(values, groups)]


def pearson(x: list[float], y: list[float]) -> float:
    mx, my = stats.mean(x), stats.mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    den = math.sqrt(sum(v*v for v in dx) * sum(v*v for v in dy))
    if den <= 0:
        raise AssertionError("zero residual variance")
    return sum(a*b for a, b in zip(dx, dy)) / den


def main() -> None:
    rows = fetch_rows()
    raw_groups = Counter(r["group"].strip() for r in rows)
    classified_counts = Counter()
    for label, n in raw_groups.items():
        classified_counts[classify_group(label)] += n
    print(f"SOCIALIS_RECOVERY raw_group_counts={dict(raw_groups)!r} classified_counts={dict(classified_counts)!r}")
    if "unknown" in classified_counts:
        raise AssertionError(f"unrecognized source group labels: {dict(raw_groups)!r}")

    common: list[tuple[str, str, float, float]] = []
    for r in rows:
        group = classify_group(r["group"])
        if group not in {"fragmented", "reference"}:
            continue
        try:
            rp = float(r["rp"])
            growth = float(r["plant height (cm)"])
        except (TypeError, ValueError):
            continue
        if not (math.isfinite(rp) and math.isfinite(growth)):
            continue
        common.append((r["family"].strip(), group, rp, growth))

    families = [r[0] for r in common]
    if len(families) != len(set(families)):
        raise AssertionError("duplicate maternal-family rows in common frame")
    groups = [r[1] for r in common]
    n_frag, n_ref = groups.count("fragmented"), groups.count("reference")
    if min(n_frag, n_ref) < 2:
        raise AssertionError(f"common family frame insufficient: fragmented={n_frag}, reference={n_ref}")

    frag_rp = [r[2] for r in common if r[1] == "fragmented"]
    ref_rp = [r[2] for r in common if r[1] == "reference"]
    frag_growth = [r[3] for r in common if r[1] == "fragmented"]
    ref_growth = [r[3] for r in common if r[1] == "reference"]

    raw_g_rp, var_g = hedges_g_metafor_ls(frag_rp, ref_rp)
    g_support = -raw_g_rp
    g_growth, var_f = hedges_g_metafor_ls(frag_growth, ref_growth)

    support = [-r[2] for r in common]
    growth = [r[3] for r in common]
    rho = pearson(centered(support, groups), centered(growth, groups))
    cov = rho * math.sqrt(var_g * var_f)
    det = var_g * var_f - cov * cov
    pd = var_g > 0 and var_f > 0 and det > 1e-12
    terminal = "ML014_admitted_Gmating_F_covariance_aware" if pd else "dependence_not_reconstructable"

    out = {
        "terminal_state": terminal,
        "source_url": URL,
        "n_source_family_rows": len(rows),
        "n_common": len(common),
        "n_fragmented": n_frag,
        "n_reference": n_ref,
        "family_ids": families,
        "raw_group_counts": dict(raw_groups),
        "G_mating_rp": {
            "raw_hedges_g_fragmented_minus_reference": raw_g_rp,
            "orientation_multiplier": -1,
            "oriented_support_g": g_support,
            "variance": var_g,
            "fragmented_mean_rp": stats.mean(frag_rp),
            "reference_mean_rp": stats.mean(ref_rp),
            "fragmented_sd_rp": stats.stdev(frag_rp),
            "reference_sd_rp": stats.stdev(ref_rp),
        },
        "F_growth": {
            "hedges_g": g_growth,
            "variance": var_f,
            "fragmented_mean": stats.mean(frag_growth),
            "reference_mean": stats.mean(ref_growth),
            "fragmented_sd": stats.stdev(frag_growth),
            "reference_sd": stats.stdev(ref_growth),
        },
        "within_cluster": {
            "residual_correlation_proxy": rho,
            "sampling_covariance": cov,
            "determinant": det,
            "positive_definite": pd,
        },
    }
    print("SOCIALIS_ML014_RESULT " + json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
