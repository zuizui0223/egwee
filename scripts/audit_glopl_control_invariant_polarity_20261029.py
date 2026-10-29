#!/usr/bin/env python3
"""Empirical EGWEE GloPL baseline-pairing-invariant treatment polarity audit.

Same publication × same species, mean fruit set Bagout vs Natural. A *strong
crossover* exists if min(Bagout) < min(Natural) AND max(Bagout) > max(Natural):
the existence of both response directions then survives ANY re-pairing of the
observed natural control means within the source group. This is a deterministic
source-mean statement, not an experimental causal effect or 95% population
sign reversal. Additional SO/SPFR/SPFL/SPP endpoints are negative controls
for stage coverage, not independent sources.

The retrospective source-label taxonomy was constructed post hoc and is NOT
a species-level generalizable ecological moderator. A separately declared
Calystegia donor-by-area provenance correction is reported next to original
heuristic labels, without silently rewriting previous work.

Usage:
  python scripts/audit_glopl_control_invariant_polarity_20261029.py
  python scripts/audit_glopl_control_invariant_polarity_20261029.py --output result.json --cases cases.csv
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence/meta_extraction/glopl_2018/GloPL_with_id.csv"
STORED_SHA = "0809eaeee54e4375d26bacfe002787241f8ff72e"
UPSTREAM_BYTE_SHA = "d22fe333b19489c473e076dd173ed7a67b1afbf0"
ENDPOINTS = ("FS", "SO", "SPFR", "SPFL", "SPP")
FINGERPRINT_PREFIXES = (
    "Natural_X_", "Bagout_X_", "Natural_N_", "Bagout_N_",
    "Natural_SD_", "Bagout_SD_"
)


def read_source():
    raw = SOURCE.read_bytes()
    sha = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    assert sha == STORED_SHA, (len(raw),sha)
    with SOURCE.open(encoding="utf-8-sig",newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2969
    assert len({r["unique_study_number"] for r in rows}) == 927
    assert len({r["Species_accepted_names"] for r in rows}) == 1265
    return rows,sha


def numeric(s):
    if s is None or s.strip() in {"", "NA", "NaN"}:
        return None
    try:
        x=float(s)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def get_means(r,e):
    n,b=(numeric(r[f"{p}_X_{e}"]) for p in ("Natural","Bagout"))
    if n is None or b is None or min(n,b)<0:
        return None
    return n,b


def asdict_case(r,e):
    n,b=get_means(r,e)
    sen,seb=None,None
    valid_SD=True
    invalid_bounded=[]
    for prefix,mean in (("Natural",n),("Bagout",b)):
        count=numeric(r[f"{prefix}_N_{e}"])
        sd=numeric(r[f"{prefix}_SD_{e}"])
        if count is None or count<=1 or sd is None or sd<0:
            valid_SD=False
            se=None
        else:
            se=sd/math.sqrt(count)
            if e=="FS" and sd > .5*math.sqrt(count/(count-1))+1e-10:
                invalid_bounded.append(prefix)
        if prefix=="Natural":
            sen=se
        else:
            seb=se
    return {
        "case":r["unique_number"],"Natural":n,"Bagout":b,
        "Delta":b-n,"se_natural":sen,"se_bagout":seb,
        "has_sd_n":valid_SD,
        "bounded_FS_reported_SD_warning":invalid_bounded,
        "year":r["year_of_study"],"population":r["population"],
        "condition":r["Additional_Treatment_Information"],
        "level":r["Level_of_Supplementation"],
        "doi":r["DOI"]
    }


def original_context(group):
    s="|".join((r["Additional_Treatment_Information"] or "").lower()
               for r in group)
    if re.search(r"pollen_donor|yellow_anther|purple_anther",s):
        return "donor"
    if (re.search(r"pin|thrum|female|hermaphrodite|bisexual|short|medium|long|morph|styled|style",s)
        and not re.search(r"large_far|large_near|large_within|small_far|small_near|small_within",s)):
        return "morph"
    yrs={r["year_of_study"] for r in group
         if r["year_of_study"] not in ("","NA")}
    derived={",".join(re.findall(r"(?:19|20)\d{2}",
              r["Additional_Treatment_Information"] or "")) for r in group}
    derived.discard("")
    if len(yrs)>1 or len(derived)>1:
        return "time"
    populations={r["population"] for r in group}
    if (re.search(r"far|near|within|area|lake|road|reserve|knob|trail|stellenbosch|elandsberg|hennessey",s)
        or len(populations)>1):
        return "space"
    return "other"


def source_context_correction(pub,species,original,cases):
    """Source-paper verified provenance, not an outcome-selected new moderator."""
    if pub=="250" and species=="Calystegia_collina":
        donor_labels={x["condition"] for x in cases}
        required={f"{size}_{donor}" for size in ("large","small")
                  for donor in ("near","far","within")}
        assert donor_labels==required
        # The original paper explicitly crossed patch size with donor
        # source; its old regex misclassified this as a purely spatial
        # context. Retain BOTH design labels.
        assert original=="space"
        return "donor_by_patch_size"
    return original


def source_fingerprint(rows,e):
    return tuple(sorted(
        tuple(r[p+e] for p in FINGERPRINT_PREFIXES)
        for r in rows
    ))


def groups_for_endpoint(source,e):
    raw=[r for r in source if get_means(r,e) is not None]
    by=defaultdict(list)
    for r in raw:
        by[(r["unique_study_number"],r["Species_accepted_names"])].append(r)
    repeats=sorted(
        [(key,rr) for key,rr in by.items() if len(rr)>=2],
        key=lambda item:(int(item[0][0]),item[0][1])
    )
    dedup=[]
    duplicates=[]
    seen={}
    for (pub,species),rr in repeats:
        key=(species,source_fingerprint(rr,e))
        if key in seen:
            duplicates.append({
                "duplicate":f"{pub}|{species}","first":seen[key]
            })
            continue
        seen[key]=f"{pub}|{species}"
        cases=[asdict_case(r,e) for r in rr]
        n=[x["Natural"] for x in cases]
        b=[x["Bagout"] for x in cases]
        mixed=any(x["Delta"]>0 for x in cases) and any(x["Delta"]<0 for x in cases)
        nmin,nmax=min(n),max(n)
        bmin,bmax=min(b),max(b)
        # Identified fixed-mean crossover independent of any within-group
        # matching between natural and treated source means.
        invariant=bool(bmin<nmin and bmax>nmax)
        margin_low=nmin-bmin
        margin_high=bmax-nmax
        valid_ci=all(x["has_sd_n"] for x in cases)
        inside_bands=False
        nominal95_z=None
        if valid_ci:
            # Bonferroni simultaneous *within one selected group* (2m
            # marginal means, two-sided), conditional on correctly defined
            # published SD/N and a Gaussian working approximation.
            nominal95_z=NormalDist().inv_cdf(
                1-0.05/(4*len(cases))
            )
            low_b_upper=min(x["Bagout"]+nominal95_z*x["se_bagout"]
                            for x in cases)
            min_n_lower=min(x["Natural"]-nominal95_z*x["se_natural"]
                            for x in cases)
            high_b_lower=max(x["Bagout"]-nominal95_z*x["se_bagout"]
                             for x in cases)
            max_n_upper=max(x["Natural"]+nominal95_z*x["se_natural"]
                             for x in cases)
            inside_bands=bool(
                low_b_upper<min_n_lower and
                high_b_lower>max_n_upper
            )
        original=original_context(rr)
        corrected=source_context_correction(pub,species,original,cases) if e=="FS" else original
        dedup.append({
            "id":f"{pub}|{species}","publication":pub,"species":species,
            "family":rr[0]["Family"],"n_cases":len(cases),
            "original_context":original,
            "source_verified_context":corrected,
            "source_isolated_context":"source methods and treatments may conflate additional ecological dimensions",
            "mixed_observed_point_signs":mixed,
            "baseline_repair_invariant_crossover":invariant,
            "mean_envelope_control_range":[nmin,nmax],
            "mean_envelope_bagged_range":[bmin,bmax],
            "baseline_crossing_low_margin":margin_low,
            "baseline_crossing_high_margin":margin_high,
            "minimum_margin":min(margin_low,margin_high),
            "all_SD_N_available":valid_ci,
            "within_group_nominal95_Bonferroni_band_crossover":inside_bands,
            "within_group_nominal95_gaussian_z":nominal95_z,
            "any_impossible_bounded_FS_SD":any(
                x["bounded_FS_reported_SD_warning"] for x in cases),
            "cases":cases
        })
    return raw,repeats,dedup,duplicates


def count_categories(groups,field):
    out={}
    for category in ("donor","donor_by_patch_size","morph","time","space","other"):
        g=[x for x in groups if x[field]==category]
        if g:
            out[category]={
                "repeated_groups":len(g),
                "point_mixed":sum(x["mixed_observed_point_signs"] for x in g),
                "pair_invariant":sum(x["baseline_repair_invariant_crossover"]
                                     for x in g)
            }
    return out


def uncertainty_FS(rows):
    out={}
    for arm in ("Natural","Bagout"):
        total=0;invalid=0;ids=[]
        for r in rows:
            n=numeric(r[f"{arm}_N_FS"])
            sd=numeric(r[f"{arm}_SD_FS"])
            if n is None or n<=1 or sd is None or sd<0:
                continue
            total+=1
            # For genuinely bounded individual proportions in [0,1],
            # the maximum possible sample SD is .5 sqrt(n/(n-1)).
            # Values violating it have incompatible source-unit/SD
            # interpretations for a direct binomial-mean z test.
            if sd>.5*math.sqrt(n/(n-1))+1e-10:
                invalid+=1;ids.append(r["unique_number"])
        out[arm]={"with_n_sd":total,"SD_exceeds_max_possible_for_bounded_0_1_observation":invalid,
                  "case_ids":ids}
    return out


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    ap.add_argument("--cases_csv",type=Path)
    args=ap.parse_args()
    source,sha=read_source()
    census={}
    fs_groups=[]
    fs_cases=[]
    for e in ENDPOINTS:
        eligible,repeat,groups,duplicates=groups_for_endpoint(source,e)
        point=[g for g in groups if g["mixed_observed_point_signs"]]
        strong=[g for g in groups if g["baseline_repair_invariant_crossover"]]
        nominal=[g for g in strong if g["within_group_nominal95_Bonferroni_band_crossover"]]
        census[e]={
            "n_Natural_Bagout_pairs":len(eligible),
            "distinct_publications":len({r["unique_study_number"] for r in eligible}),
            "repeated_groups_pre_duplicate_screen":len(repeat),
            "numeric_duplicate_groups":duplicates,
            "repeated_publication_species_dedup":len(groups),
            "point_sign_mixed_groups":len(point),
            "point_mixed_distinct_publications":len({g["publication"] for g in point}),
            "baseline_repair_invariant_groups":len(strong),
            "baseline_repair_invariant_publications":len(
                {g["publication"] for g in strong}),
            "baseline_repair_invariant_families":len({g["family"] for g in strong}),
            "minimum_both_sides_margin_ge_0_01":
                sum(g["minimum_margin"]>=.01-1e-12 for g in strong),
            "minimum_both_sides_margin_ge_0_05":
                sum(g["minimum_margin"]>=.05-1e-12 for g in strong),
            "nominal95_groupwise_Bonferroni_mean_band_groups":len(nominal),
            "nominal_groupwise_band_ids":[g["id"] for g in nominal],
            "point_range_invariant_examples":[{
                k:v for k,v in g.items() if k!="cases"
            } for g in strong],
            "claim_limit":"Mean-range invariance is deterministic, does not prove true sign reversal or identify causal mechanism. Nominal Gaussian SD/N bands are NOT 129-group familywise corrected and can be invalid for heterogeneous marginal denominators.",
        }
        if e=="FS":
            fs_groups=groups
            fs_cases=eligible
    assert {e:(census[e]["n_Natural_Bagout_pairs"],
               census[e]["repeated_publication_species_dedup"],
               census[e]["point_sign_mixed_groups"],
               census[e]["baseline_repair_invariant_groups"])
            for e in ENDPOINTS}=={
                "FS":(811,129,28,10),
                "SO":(159,25,7,1),
                "SPFR":(193,34,6,1),
                "SPFL":(51,10,1,0),
                "SPP":(14,3,0,0)
            }
    assert census["FS"]["baseline_repair_invariant_publications"]==10
    assert census["FS"]["baseline_repair_invariant_families"]==9
    assert census["FS"]["minimum_both_sides_margin_ge_0_01"]==8
    assert census["FS"]["minimum_both_sides_margin_ge_0_05"]==4
    assert census["FS"]["nominal95_groupwise_Bonferroni_mean_band_groups"]==1
    assert census["FS"]["nominal_groupwise_band_ids"]==[
        "1089|Hugonia_serrata"
    ]
    assert census["FS"]["numeric_duplicate_groups"]==[
        {"duplicate":"119|Pachycereus_pringlei",
         "first":"92|Pachycereus_pringlei"}
    ]
    # Source verified categorical correction must not pretend the post hoc
    # mating-context study selection is a randomized explanatory factor.
    original=count_categories(fs_groups,"original_context")
    corrected=count_categories(fs_groups,"source_verified_context")
    assert original=={
        "donor":{"repeated_groups":4,"point_mixed":2,"pair_invariant":0},
        "morph":{"repeated_groups":23,"point_mixed":9,"pair_invariant":5},
        "time":{"repeated_groups":51,"point_mixed":10,"pair_invariant":2},
        "space":{"repeated_groups":41,"point_mixed":6,"pair_invariant":3},
        "other":{"repeated_groups":10,"point_mixed":1,"pair_invariant":0},
    }
    assert corrected=={
        "donor":{"repeated_groups":4,"point_mixed":2,"pair_invariant":0},
        "donor_by_patch_size":{"repeated_groups":1,"point_mixed":1,"pair_invariant":1},
        "morph":{"repeated_groups":23,"point_mixed":9,"pair_invariant":5},
        "time":{"repeated_groups":51,"point_mixed":10,"pair_invariant":2},
        "space":{"repeated_groups":40,"point_mixed":5,"pair_invariant":2},
        "other":{"repeated_groups":10,"point_mixed":1,"pair_invariant":0}
    }
    sd_warning=uncertainty_FS(fs_cases)
    assert (sd_warning["Natural"]["SD_exceeds_max_possible_for_bounded_0_1_observation"],
            sd_warning["Bagout"]["SD_exceeds_max_possible_for_bounded_0_1_observation"])==(17,15)
    by_id={g["id"]:g for g in fs_groups}
    caly=by_id["250|Calystegia_collina"]
    by_size=defaultdict(dict)
    for c in caly["cases"]:
        size, donor=c["condition"].split("_",1)
        by_size[size][donor]=c
    assert all(set(x)=={"near","far","within"} for x in by_size.values())
    caly_response={}
    for size,r in by_size.items():
        N={x["Natural"] for x in r.values()}
        assert len(N)==1
        N=next(iter(N))
        ext=(r["near"]["Bagout"]+r["far"]["Bagout"])/2
        inside=r["within"]["Bagout"]
        caly_response[size]={
            "Natural_same_within_size":N,
            "Bagout_within":inside,"Bagout_near":r["near"]["Bagout"],
            "Bagout_far":r["far"]["Bagout"],
            "external_donor_mean_minus_within_donor":ext-inside,
            "external_donor_mean_minus_Natural":ext-N,
            "within_donor_minus_Natural":inside-N
        }
    assert abs(caly_response["large"]["external_donor_mean_minus_within_donor"]-.4995)<1e-8
    assert abs(caly_response["small"]["external_donor_mean_minus_within_donor"]-.295)<1e-8

    if args.cases_csv:
        args.cases_csv.parent.mkdir(parents=True,exist_ok=True)
        with args.cases_csv.open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=[
                "group","publication","species","family","original_context",
                "corrected_context","margin_low","margin_high",
                "case","condition","Natural","Bagout","Delta",
                "Natural_N","Bagout_N","Natural_SD","Bagout_SD",
                "reported_SD_bound_warning"
            ])
            writer.writeheader()
            by_lookup={r["unique_number"]:r for r in fs_cases}
            for g in fs_groups:
                if not g["baseline_repair_invariant_crossover"]:
                    continue
                for c in g["cases"]:
                    r=by_lookup[c["case"]]
                    writer.writerow({
                        "group":g["id"],"publication":g["publication"],
                        "species":g["species"],"family":g["family"],
                        "original_context":g["original_context"],
                        "corrected_context":g["source_verified_context"],
                        "margin_low":g["baseline_crossing_low_margin"],
                        "margin_high":g["baseline_crossing_high_margin"],
                        "case":c["case"],"condition":c["condition"],
                        "Natural":c["Natural"],"Bagout":c["Bagout"],
                        "Delta":c["Delta"],
                        "Natural_N":r["Natural_N_FS"],
                        "Bagout_N":r["Bagout_N_FS"],
                        "Natural_SD":r["Natural_SD_FS"],
                        "Bagout_SD":r["Bagout_SD_FS"],
                        "reported_SD_bound_warning":"|".join(
                            c["bounded_FS_reported_SD_warning"])
                    })

    result={
        "status":"exploratory post hoc published-mean baseline-pairing invariance",
        "source_original_byte_blob":UPSTREAM_BYTE_SHA,
        "source_stored_utf8_blob":sha,
        "n_all_source_cases":2969,
        "endpoint_census":census,
        "FS_context_original_heuristic":original,
        "FS_context_source_verified_Calystegia_correction":corrected,
        "Calystegia_original_donor_by_patch_area":caly_response,
        "FS_source_reported_SD_violations_of_bounded_means":sd_warning,
        "method_ceiling":{
            "original_effect_morph_and_donor_studies_are_prior_art":True,
            "all_nonzero_source_mean_signs_not_statistically_resolved":True,
            "paper_source_design_classes_selected_post_hoc":True,
            "source_SD_as_if_binomial_variance_not_safely_interpretable":True,
            "source_specific_Bonferroni_not_whole_129_group_corrected":True,
            "fragmentation_5_8_16_programmes_unchanged":True,
            "theoretical_egwe_used":False,
            "submission_ready":False
        }
    }
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,
                                           sort_keys=True)+"\n",encoding="utf-8")
    print("GLOPL_BASELINE_INVARIANT_OK source",sha,"FS",census["FS"]["n_Natural_Bagout_pairs"],
          "repeat",census["FS"]["repeated_publication_species_dedup"],
          "mixed",census["FS"]["point_sign_mixed_groups"],
          "invariant",census["FS"]["baseline_repair_invariant_groups"],
          "publications",census["FS"]["baseline_repair_invariant_publications"],
          "families",census["FS"]["baseline_repair_invariant_families"])
    for e,item in census.items():
        print("GLOPL_INVARIANT_ENDPOINT",e,"n",item["n_Natural_Bagout_pairs"],
              "repeated",item["repeated_publication_species_dedup"],
              "mixed",item["point_sign_mixed_groups"],
              "invariant",item["baseline_repair_invariant_groups"])
    print("GLOPL_INVARIANT_GROUPWISE_NOMINAL_BAND",census["FS"]["nominal_groupwise_band_ids"])
    print("GLOPL_INVARIANT_CATEGORY_ORIGINAL",json.dumps(original,sort_keys=True))
    print("GLOPL_INVARIANT_CATEGORY_CORRECTED",json.dumps(corrected,sort_keys=True))
    print("GLOPL_INVARIANT_SD_QA",json.dumps(sd_warning,sort_keys=True))
    print("GLOPL_CALYSTEGIA_DONOR_CONTEXT",json.dumps(caly_response,sort_keys=True))


if __name__=="__main__":
    main()
