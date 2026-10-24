#!/usr/bin/env python3
"""Source-verified, reserve-independent 2026 Sevenello pollen-addition audit.

This executes the previously fixed 2026-10-19 design in empirical egwee.
A quadrat supplies different OP and OPSupp *plants*, not paired measurements
of a single plant; reserv(es) and reserve×crop blocks define geography.

No new registered quantitative I–F programme, no inference about pollen
provenance, no theoretical egwe outputs. NumPy and SciPy required.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "evidence" / "meta_extraction" / "sevenello_2026_raw"
MD5 = {
    "landscape_seeds.csv": ("40caf98755786e32bec89fffd4b114f6", 135336, 2080),
    "local_seeds.csv": ("10f0b07ff3ff17ca94dbabdfbcec404e", 21953, 520),
    "landscape_bees.csv": ("b6cbdd11787f5ef5210fefcd502a29f5", 1775, 20),
}
SPECIES = ("GORO", "LARO", "POAR")
EXPECTED = {"GORO": (120, 5, 6), "LARO": (160, 6, 8), "POAR": (120, 4, 6)}
RESERVES = {"Buntine", "Maya", "MayaPrivate", "Milton", "WA12427",
            "XantippeEast", "XantippeTank"}


def read(name):
    path = BASE / name
    blob = path.read_bytes()
    checksum, nbytes, nrows = MD5[name]
    assert len(blob) == nbytes, (name, len(blob), nbytes)
    assert hashlib.md5(blob).hexdigest() == checksum, (name, "MD5 mismatch")
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == nrows
    return rows


def number(s):
    return None if s is None or s.strip() in {"", "NA", "NaN", "N/A"} else float(s)


def mean(xs):
    assert len(xs) > 0
    return float(np.mean(xs))


def two_sided_exact_signflip(xs):
    # Exact finite set of site sign swaps for a symmetric-site null.
    arr = np.asarray(xs, dtype=float)
    n = len(arr)
    observed = abs(arr.mean())
    extreme = 0
    for signs in itertools.product((-1, 1), repeat=n):
        if abs(np.dot(arr, signs) / n) >= observed - 1e-10:
            extreme += 1
    return extreme / (2 ** n)


def summary_site(xs):
    x = np.asarray(xs, float)
    n = len(x)
    assert n >= 3
    m = x.mean()
    se = x.std(ddof=1) / np.sqrt(n)
    lo, hi = m + np.array([-1, 1]) * stats.t.ppf(.975, n-1) * se
    t_p = float(2 * stats.t.sf(abs(m / se), n - 1)) if se else None
    leave = [(sum(x) - x[i]) / (n - 1) for i in range(n)]
    return {
        "n_independent_reserves": n, "estimate": float(m),
        "sd_between_reserves": float(x.std(ddof=1)),
        "t_95_interval_descriptive": [float(lo), float(hi)],
        "t_p_nominal": t_p,
        "signflip_p_exact_two_sided": two_sided_exact_signflip(x),
        "leave_one_reserve_out_mean_range": [float(min(leave)), float(max(leave))],
        "positive_reserves": int((x > 0).sum()),
        "negative_reserves": int((x < 0).sum()),
    }


def holm(pvals):
    order = sorted(range(len(pvals)), key=lambda j:pvals[j])
    result = [0.] * len(pvals)
    running = 0.
    for rank, j in enumerate(order):
        running = max(running, min(1., float(pvals[j]) * (len(pvals) - rank)))
        result[j] = running
    return result


def environmental_slope(pairs, key):
    # Within each reserve×crop×edge/core transect, subtract the means
    # in both X and Y; calculate single-predictor within-transect slopes.
    strata = defaultdict(list)
    for p in pairs:
        strata[(p["site"], p["crop"], p["transect"])].append(p)
    predictors = []
    responses = {"D": [], "OP": [], "OPSupp": []}
    sites = []
    for (site, crop, tr), records in strata.items():
        xv = np.asarray([p[key] for p in records], float)
        av = np.asarray([p["op"] for p in records], float)
        bv = np.asarray([p["supp"] for p in records], float)
        x = xv - xv.mean()
        predictors.extend(x.tolist())
        sites.extend([site] * len(records))
        for name, y in (("OP", av), ("OPSupp", bv), ("D", bv-av)):
            responses[name].extend((y - y.mean()).tolist())
    X = np.asarray(predictors, float)
    S = np.asarray(sites)
    if np.dot(X, X) < 1e-8:
        return None
    result = {}
    for name, Y in responses.items():
        Y = np.asarray(Y, float)
        slope = float(np.dot(X, Y) / np.dot(X, X))
        leave = []
        for site in sorted(set(sites)):
            mask = S != site
            leave.append(float(np.dot(X[mask], Y[mask]) / np.dot(X[mask], X[mask])))
        result[name] = {"within_transect_slope": slope,
                        "exclude_one_reserve_slope_range": [min(leave), max(leave)]}
    assert abs(result["D"]["within_transect_slope"] -
               (result["OPSupp"]["within_transect_slope"] -
                result["OP"]["within_transect_slope"])) < 1e-9
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    seedrows = read("landscape_seeds.csv")
    localrows = read("local_seeds.csv")
    bees = read("landscape_bees.csv")
    assert len(bees) == 20
    local = {r["id_plot"]: r for r in localrows}
    assert len(local) == 520

    plots = {}
    for r in seedrows:
        ident = r["id_plot"]
        if ident not in plots:
            plots[ident] = {"id_plot": ident, "species": r["species"],
                            "site": r["site"], "crop": r["crop_type"],
                            "transect": r["transect"], "treatments": {}}
        p = plots[ident]
        assert (p["species"], p["site"], p["crop"], p["transect"]) == (
            r["species"], r["site"], r["crop_type"], r["transect"])
        assert r["treat"] not in p["treatments"], (ident, r["treat"])
        p["treatments"][r["treat"]] = {
            "seeds": number(r["total_seeds"]),
            "flowers": number(r["flower_num"])
        }
    assert set(plots) == set(local) and len(plots) == 520
    assert all(set(p["treatments"]) == {"OP", "OPSupp", "Bag", "BagSup"} for p in plots.values())
    assert sum(z["seeds"] is None for p in plots.values() for z in p["treatments"].values()) == 31
    assert set(p["site"] for p in plots.values()) >= RESERVES
    count_by_species = Counter(p["species"] for p in plots.values())
    assert count_by_species == {"GORO": 120, "LARO": 160, "POAR": 120, "POGN": 120}

    out = {
        "source_doi": "10.6084/m9.figshare.31072189",
        "source_license": "CC BY 4.0",
        "primary_endpoint": "OPSupp viable-looking seeds per plant - OP seeds per plant",
        "independent_unit": "physical reserve, site×crop block averaged within reserve",
        "design_fixed_before_outcomes": "SEVENELLO_POLLEN_ADDITION_CONTEXT_DESIGN_2026-10-19.md",
        "source_validation": {
            "csv_file_md5s": {k:v[0] for k,v in MD5.items()},
            "treatment_plant_records": 2080,
            "quadrats_with_four_treatment_plants": 520,
            "transect_bee_records": 20,
            "missing_seed_count": 31,
        },
        "species": {}, "primary_exact_signflip_holm_by_species": {}
    }
    pvals = []

    for species in SPECIES:
        speciesplots = [p for p in plots.values() if p["species"] == species]
        complete = []
        missing_counts = Counter()
        for p in speciesplots:
            op, supp = p["treatments"]["OP"], p["treatments"]["OPSupp"]
            if op["seeds"] is None or supp["seeds"] is None:
                key = ("missing_OP" if op["seeds"] is None else "") + (
                    "+missing_OPSupp" if supp["seeds"] is None else "")
                missing_counts[key] += 1
                continue
            lo = local[p["id_plot"]]
            z = {k:p[k] for k in ("id_plot", "species", "site", "crop", "transect")}
            z.update(op=op["seeds"], supp=supp["seeds"],
                     D=supp["seeds"]-op["seeds"],
                     bare_ground_per10=float(lo["ground_p"]) / 10.,
                     floral_log1p=float(np.log1p(float(lo["total_flower"]))))
            if op["flowers"] is not None and supp["flowers"] is not None and (
                    op["flowers"] > 0 and supp["flowers"] > 0):
                z["D_per_flower"] = supp["seeds"]/supp["flowers"]-op["seeds"]/op["flowers"]
                z["OP_per_flower"] = op["seeds"]/op["flowers"]
                z["Supp_per_flower"] = supp["seeds"]/supp["flowers"]
            else:
                z["D_per_flower"] = None
            complete.append(z)

        groups = defaultdict(list)
        for p in complete:
            groups[(p["site"], p["crop"], p["transect"])].append(p)
        block = defaultdict(dict)
        for (site,crop,side), rr in groups.items():
            block[(site,crop)][side] = {
                "n_pairs":len(rr), "mean_OP": mean([x["op"] for x in rr]),
                "mean_OPSupp": mean([x["supp"] for x in rr]),
                "mean_D": mean([x["D"] for x in rr]),
                "mean_D_per_flower":
                    mean([x["D_per_flower"] for x in rr
                          if x["D_per_flower"] is not None])
                    if any(x["D_per_flower"] is not None for x in rr) else None,
            }
        reserveblocks = defaultdict(list)
        for (site,crop), sides in block.items():
            assert set(sides) == {"Edge", "Core"}, (species, site,crop,sides)
            edge, core = sides["Edge"], sides["Core"]
            b = {"crop":crop, "n_edge":edge["n_pairs"], "n_core":core["n_pairs"]}
            for key in ("OP","OPSupp","D"):
                b["contrast_"+key] = edge["mean_"+key] - core["mean_"+key]
            b["edge_D"], b["core_D"] = edge["mean_D"], core["mean_D"]
            b["mean_supp_response"] = (edge["mean_D"] + core["mean_D"])/2.
            if species != "GORO":
                b["mean_perflower_response"] = (
                    edge["mean_D_per_flower"] + core["mean_D_per_flower"])/2.
                b["contrast_D_perflower"] = (
                    edge["mean_D_per_flower"] - core["mean_D_per_flower"])
            assert abs(b["contrast_D"]-(b["contrast_OPSupp"]-b["contrast_OP"]))<1e-9
            reserveblocks[site].append(b)

        reserve = []
        for site, bs in sorted(reserveblocks.items()):
            z = {"site":site,"n_crop_blocks":len(bs),
                 "crop_blocks":bs}
            for key in ("OP","OPSupp","D"):
                z["edge_core_"+key] = mean([b["contrast_"+key] for b in bs])
            z["overall_supp_response"] = mean([b["mean_supp_response"] for b in bs])
            if species != "GORO":
                z["overall_perflower_response"] = mean(
                    [b["mean_perflower_response"] for b in bs])
                z["edge_core_D_perflower"] = mean(
                    [b["contrast_D_perflower"] for b in bs])
            assert abs(z["edge_core_D"] -
                       (z["edge_core_OPSupp"] - z["edge_core_OP"])) < 1e-8
            reserve.append(z)
        assert (len(speciesplots),len(reserve),sum(x["n_crop_blocks"] for x in reserve)) == EXPECTED[species]
        contrasts = [r["edge_core_D"] for r in reserve]
        site_response = [r["overall_supp_response"] for r in reserve]
        primary = summary_site(contrasts)
        pvals.append(primary["signflip_p_exact_two_sided"])
        s = {
            "n_quadrats":len(speciesplots), "n_complete_op_supp_pairs":len(complete),
            "n_incomplete":len(speciesplots)-len(complete),
            "missing_by_treatment_pair":dict(missing_counts),
            "raw_pair_mean_D_unbalanced":mean([p["D"] for p in complete]),
            "raw_pair_median_D_unbalanced":float(np.median([p["D"] for p in complete])),
            "raw_pair_positive":sum(p["D"] > 0 for p in complete),
            "raw_pair_negative":sum(p["D"] < 0 for p in complete),
            "raw_pair_zero":sum(p["D"] == 0 for p in complete),
            "reserve_summaries":reserve,
            "primary_edge_minus_core_of_supplement_response":primary,
            "reserve_equal_overall_supplement_response":summary_site(site_response),
        }
        if species != "GORO":
            pf = [p["D_per_flower"] for p in complete if p["D_per_flower"] is not None]
            s["complete_per_flower_pairs"] = len(pf)
            s["raw_pair_perflower_mean_D_unbalanced"] = mean(pf)
            s["reserve_equal_perflower_response"] = summary_site(
                [r["overall_perflower_response"] for r in reserve])
            s["reserve_equal_perflower_edge_core"] = summary_site(
                [r["edge_core_D_perflower"] for r in reserve])
        else:
            s["complete_per_flower_pairs"] = 0
            s["perflower_not_observed_reason"] = "GORO dehiscent fruit destroys flower counts"
        s["secondary_within_transect_slopes"] = {
            "bare_ground_10_percentage_points":environmental_slope(
                complete,"bare_ground_per10"),
            "log1p_neighbourhood_flower_count":environmental_slope(
                complete,"floral_log1p"),
        }
        out["species"][species] = s

    adjusted = holm(pvals)
    out["primary_exact_signflip_holm_by_species"] = dict(zip(SPECIES, adjusted))
    assert max(adjusted) <= 1 and len(out["species"]) == 3
    assert out["species"]["GORO"]["n_complete_op_supp_pairs"] == 117
    assert out["species"]["LARO"]["n_complete_op_supp_pairs"] == 157
    assert out["species"]["POAR"]["n_complete_op_supp_pairs"] == 115
    # Critical geometry: species POAR reverses sign under reserve equality.
    assert out["species"]["POAR"]["raw_pair_mean_D_unbalanced"] < 0
    assert out["species"]["POAR"]["reserve_equal_overall_supplement_response"]["estimate"] > 0
    assert out["species"]["POAR"]["raw_pair_perflower_mean_D_unbalanced"] > 0

    result=json.dumps(out, indent=2, ensure_ascii=False, allow_nan=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result,encoding="utf-8")
    print("SEVENELLO_SOURCE_VALIDATED",out["source_validation"])
    for sp in SPECIES:
        z=out["species"][sp]
        a=z["primary_edge_minus_core_of_supplement_response"]
        b=z["reserve_equal_overall_supplement_response"]
        print(f"SEVENELLO_SPECIES {sp} n={z['n_complete_op_supp_pairs']} reserves={len(z['reserve_summaries'])} "
              f"edge_core_D={a['estimate']:.6f} t95={a['t_95_interval_descriptive']} "
              f"exact_p={a['signflip_p_exact_two_sided']:.5f} "
              f"mean_total_D_all_quadrats={z['raw_pair_mean_D_unbalanced']:.6f} "
              f"reserve_equal_total_D={b['estimate']:.6f} "
              f"mean_perflower_D={z.get('raw_pair_perflower_mean_D_unbalanced',float('nan')):.6f}")
    print("SEVENELLO_HOLM_EXACT",out["primary_exact_signflip_holm_by_species"])


if __name__ == "__main__":
    main()
