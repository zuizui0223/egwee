#!/usr/bin/env python3
"""GloPL pollination-regime polarity across repeat species-within-study cases.

Empirical EGWEE exploratory meta-extraction, NOT theoretical EGWE/NEE.

For a fixed species in the same GloPL publication, does Bagout−Natural fruit
set retain one sign across different flower morphs, donor classes, local
settings or years? This detects *published mean sign polarity*, not 95%
confirmed pollination effects or fragmentation-induced genetic mechanisms.

The context taxonomy is post hoc source-label classification. Descriptive
publication-cluster bootstrap does NOT remove study-selection confounding.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"evidence/meta_extraction/glopl_2018/GloPL_with_id.csv"
BLOB="0809eaeee54e4375d26bacfe002787241f8ff72e"
CATEGORY_ORDER=("donor","morph","time","space","other")
ANCHORS=(
    "92|Pachycereus_pringlei",
    "161|Oxalis_squamata",
    "250|Calystegia_collina",
    "559|Eriocnema_fulva",
    "1089|Hugonia_serrata",
    "2129|Dichorisandra_incurva",
    "2189|Rourea_induta",
)


def num(value):
    if value is None or value.strip() in ("", "NA", "NaN"):
        return None
    try:
        x=float(value)
    except ValueError:
        return None
    return x if np.isfinite(x) else None


def load():
    blob=SOURCE.read_bytes()
    check=hashlib.sha1(f"blob {len(blob)}\0".encode()+blob).hexdigest()
    assert check==BLOB,(len(blob),check)
    with SOURCE.open("r",encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==2969
    assert len({r["unique_study_number"] for r in rows})==927
    assert len({r["Species_accepted_names"] for r in rows})==1265
    return rows


def labels(group):
    return "|".join((r["Additional_Treatment_Information"] or "").lower()
                    for r in group)


def context(group):
    s=labels(group)
    # All classes are mutually exclusive by explicit source-label priority.
    if re.search(r"pollen_donor|yellow_anther|purple_anther",s):
        return "donor"
    if (re.search(r"pin|thrum|female|hermaphrodite|bisexual|short|medium|long|morph|styled|style",s)
        and not re.search(r"large_far|large_near|large_within|small_far|small_near|small_within",s)):
        return "morph"
    years={r["year_of_study"] for r in group if r["year_of_study"] not in ("","NA")}
    derived={",".join(re.findall(r"(?:19|20)\d{2}",
              r["Additional_Treatment_Information"] or "")) for r in group}
    derived.discard("")
    if len(years)>1 or len(derived)>1:
        return "time"
    pop={r["population"] for r in group}
    if (re.search(r"far|near|within|area|lake|road|reserve|knob|trail|stellenbosch|elandsberg|hennessey",s)
        or len(pop)>1):
        return "space"
    return "other"


def values(r):
    n=num(r["Natural_X_FS"]);b=num(r["Bagout_X_FS"])
    if n is None or b is None or min(n,b)<0:
        return None
    assert max(n,b)<=1+1e-12
    return n,b


def nominal_z(r):
    v=values(r)
    if v is None:return None
    n0=num(r["Natural_N_FS"]);n1=num(r["Bagout_N_FS"])
    sd0=num(r["Natural_SD_FS"]);sd1=num(r["Bagout_SD_FS"])
    if any(x is None for x in (n0,n1,sd0,sd1)) or min(n0,n1)<=1 or min(sd0,sd1)<0:
        return None
    se=(sd0*sd0/n0 + sd1*sd1/n1)**.5
    return (v[1]-v[0])/se if se>0 else None


def fingerprint(group):
    # Exactly matching numerical source row profiles, with biological identity
    # required outside the fingerprint before calling an apparent duplication.
    return tuple(sorted(
        tuple(r[k] for k in (
            "Natural_X_FS","Bagout_X_FS","Natural_N_FS","Bagout_N_FS",
            "Natural_SD_FS","Bagout_SD_FS"))
        for r in group
    ))


def summarize(groups):
    categories={k:{"n":0,"mixed":0,"both_nominal_196":0} for k in CATEGORY_ORDER}
    for g in groups:
        c=categories[g["category"]]
        c["n"]+=1;c["mixed"]+=int(g["mixed"])
        c["both_nominal_196"]+=int(g["both_nominal_196"])
    def combine(kinds):
        selected=[g for g in groups if g["category"] in kinds]
        return {
            "n":len(selected),
            "mixed":sum(g["mixed"] for g in selected),
            "both_nominal_196":sum(g["both_nominal_196"] for g in selected),
            "mixed_rate":(sum(g["mixed"] for g in selected)/len(selected)
                          if selected else None)
        }
    return {
        "categories":categories,
        "mating_context":combine({"donor","morph"}),
        "environmental_or_temporal":combine({"time","space"}),
        "other":combine({"other"}),
    }


def study_bootstrap(groups, seed=20261028, draws=30000):
    pub=defaultdict(list)
    for g in groups:pub[g["publication"]].append(g)
    sources=list(pub.values())
    rng=np.random.default_rng(seed)
    b=[]
    for _ in range(draws):
        sample=[s for j in rng.integers(0,len(sources),size=len(sources))
                for s in sources[j]]
        z=summarize(sample)
        m=z["mating_context"]["mixed_rate"]
        e=z["environmental_or_temporal"]["mixed_rate"]
        if m is not None and e is not None:
            b.append(m-e)
    b=np.asarray(b,float)
    z=summarize(groups)
    observed=(z["mating_context"]["mixed_rate"]-
              z["environmental_or_temporal"]["mixed_rate"])
    loo=[]
    for p in pub:
        subset=[g for g in groups if g["publication"]!=p]
        w=summarize(subset)
        loo.append(w["mating_context"]["mixed_rate"]-
                   w["environmental_or_temporal"]["mixed_rate"])
    return {
        "publication_clusters":len(sources),
        "observed_difference":observed,
        "publication_cluster_bootstrap95":[float(x) for x in
                                            np.quantile(b,[.025,.975])],
        "leave_one_publication_difference_range":[min(loo),max(loo)],
        "n_boot_valid":len(b),
        "interpretation":"Exploratory selected-case difference, NOT a causal trait effect or prevalence across all plants; taxonomy built after inspecting GloPL source labels"
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    parser.add_argument("--mixed_csv",type=Path)
    args=parser.parse_args()

    rows=load()
    eligible=[r for r in rows if values(r) is not None]
    assert len(eligible)==811
    studies=len({r["unique_study_number"] for r in eligible})
    species=len({r["Species_accepted_names"] for r in eligible})
    assert (studies,species)==(413,588)

    by=defaultdict(list)
    for r in eligible:
        by[r["unique_study_number"]+"|"+r["Species_accepted_names"]].append(r)
    assert len(by)==613
    repeated={k:v for k,v in by.items() if len(v)>=2}
    assert len(repeated)==130

    raw_groups=[]
    for key,group in sorted(repeated.items(),
                            key=lambda item:(int(item[1][0]["unique_study_number"]),
                                             item[1][0]["Species_accepted_names"])):
        sign=[np.sign(values(r)[1]-values(r)[0]) for r in group]
        z=[nominal_z(r) for r in group]
        mixed=(1 in sign and -1 in sign)
        precise=(any(x is not None and x>=1.96 for x in z) and
                 any(x is not None and x<=-1.96 for x in z))
        r=group[0]
        raw_groups.append({
            "id":key,
            "publication":r["unique_study_number"],
            "species":r["Species_accepted_names"],
            "family":r["Family"],
            "author":r["Author"],"original_paper_year":r["Year"],
            "doi":r["DOI"],
            "category":context(group),
            "n_original_cases":len(group),
            "mixed":bool(mixed),
            "both_nominal_196":bool(precise),
            "distinct_population_labels":
                sorted({r["population"] for r in group}),
            "recorded_year_labels":sorted({r["year_of_study"] for r in group}),
            "condition_labels":
                sorted({r["Additional_Treatment_Information"] for r in group}),
            "signature":fingerprint(group),
            "cases":[{
                "case_id":r["unique_number"],
                "natural_fruit_set":values(r)[0],
                "bagged_outcross_fruit_set":values(r)[1],
                "difference":values(r)[1]-values(r)[0],
                "rough_z":nominal_z(r),
                "natural_N":num(r["Natural_N_FS"]),
                "bagout_N":num(r["Bagout_N_FS"]),
                "population":r["population"],
                "year":r["year_of_study"],
                "source_condition":r["Additional_Treatment_Information"]
            } for r in group],
        })

    full_mixed=[g for g in raw_groups if g["mixed"]]
    assert (len(full_mixed),sum(g["both_nominal_196"] for g in full_mixed))==(29,13)
    # Drop apparent repeated source observations only when the species AND
    # all six source treatment mean/N/SD cells for EACH case match exactly.
    # Do not call two published reports independent experiments.
    fingerprints={}
    dedup=[]
    overlaps=[]
    for g in raw_groups:
        key=(g["species"],g["signature"])
        if key in fingerprints:
            overlaps.append({"repeated_source_group":g["id"],
                             "first_source_group":fingerprints[key],
                             "same_species_and_all_numeric_cells":True})
            continue
        fingerprints[key]=g["id"]
        dedup.append(g)
    assert overlaps==[{
        "repeated_source_group":"119|Pachycereus_pringlei",
        "first_source_group":"92|Pachycereus_pringlei",
        "same_species_and_all_numeric_cells":True}]
    assert len(dedup)==129
    unique_mixed=[g for g in dedup if g["mixed"]]
    assert (len(unique_mixed),sum(g["both_nominal_196"] for g in unique_mixed))==(28,12)
    categorical=summarize(dedup)
    assert categorical["categories"]=={
        "donor":{"n":4,"mixed":2,"both_nominal_196":1},
        "morph":{"n":23,"mixed":9,"both_nominal_196":5},
        "time":{"n":51,"mixed":10,"both_nominal_196":4},
        "space":{"n":41,"mixed":6,"both_nominal_196":2},
        "other":{"n":10,"mixed":1,"both_nominal_196":0},
    },categorical
    assert ((categorical["mating_context"]["n"],
             categorical["mating_context"]["mixed"]),
            (categorical["environmental_or_temporal"]["n"],
             categorical["environmental_or_temporal"]["mixed"]))==((27,11),(92,16))
    bootstrap=study_bootstrap(dedup)
    examples={}
    for key in ANCHORS:
        g=next((g for g in dedup if g["id"]==key),None)
        assert g is not None and g["mixed"],key
        examples[key]={k:v for k,v in g.items() if k!="signature"}

    # A source-specific landscape anchor: Calystegia same flower population
    # baseline repeated for manually bagged pollen sourced from far/near/within
    # the same patch, across both large and small habitat contexts.
    C=examples["250|Calystegia_collina"]["cases"]
    bypatch=defaultdict(dict)
    for case in C:
        code=case["source_condition"]
        size,donor=code.split("_",1)
        assert size in {"large","small"} and donor in {"far","near","within"}
        bypatch[size][donor]=case
    assert all(set(v)=={"far","near","within"} for v in bypatch.values())
    donor_anchor={}
    for size,values_by_donor in bypatch.items():
        far,near,within=(values_by_donor[t]["bagged_outcross_fruit_set"]
                          for t in ("far","near","within"))
        nat=values_by_donor["within"]["natural_fruit_set"]
        assert all(abs(q["natural_fruit_set"]-nat)<1e-12
                   for q in values_by_donor.values())
        donor_anchor[size]={
            "natural_same_comparison_frame":nat,
            "bagout_within":within,"bagout_near":near,"bagout_far":far,
            "near_minus_within":near-within,
            "far_minus_within":far-within,
            "external_average_minus_within":(far+near)/2-within,
            "one_source_only":True
        }
    assert abs(donor_anchor["large"]["external_average_minus_within"]-0.4995)<1e-9
    assert abs(donor_anchor["small"]["external_average_minus_within"]-0.295)<1e-9

    if args.mixed_csv:
        args.mixed_csv.parent.mkdir(parents=True,exist_ok=True)
        with args.mixed_csv.open("w",newline="",encoding="utf-8") as f:
            field=["group","publication","species","family","category",
                   "case_id","natural_FS","bagout_FS","bagout_minus_natural",
                   "rough_z","condition","population","year"]
            writer=csv.DictWriter(f,fieldnames=field);writer.writeheader()
            for g in unique_mixed:
                for c in g["cases"]:
                    writer.writerow({
                        "group":g["id"],"publication":g["publication"],
                        "species":g["species"],"family":g["family"],
                        "category":g["category"],"case_id":c["case_id"],
                        "natural_FS":c["natural_fruit_set"],
                        "bagout_FS":c["bagged_outcross_fruit_set"],
                        "bagout_minus_natural":c["difference"],
                        "rough_z":c["rough_z"],
                        "condition":c["source_condition"],
                        "population":c["population"],"year":c["year"]
                    })

    result={
        "status":"post_hoc original publication×species design taxonomy",
        "n_original_glopl_cases":2969,
        "n_fruit_set_Natural_Bagout_pairs":len(eligible),
        "n_distinct_publications":studies,
        "n_distinct_species":species,
        "publication_by_species_groups":len(by),
        "groups_with_two_or_more_cases":len(repeated),
        "pre_exact_profile_dedup":{
            "mixed_groups":len(full_mixed),
            "both_nominal_196_mixed_groups":
                sum(g["both_nominal_196"] for g in full_mixed)},
        "duplicate_numeric_profiles":overlaps,
        "after_exact_profile_dedup":{
            "groups":len(dedup),
            "source_publications":len({g["publication"] for g in dedup}),
            "mixed_groups":len(unique_mixed),
            "publications_with_mixed_groups":
                len({g["publication"] for g in unique_mixed}),
            "nominally_opposite_marginal_z_groups":
                sum(g["both_nominal_196"] for g in unique_mixed),
            "categories":categorical,
            "category_exploratory_publication_cluster_bootstrap":
                bootstrap,
        },
        "selected_original_source_anchor_contrasts":examples,
        "published_calystegia_donor_distance_study":
            donor_anchor,
        "specific_claim_boundaries":{
            "opposite_marginal_z_is_not_confirmed_independent_tradeoff":True,
            "source_N_SD_does_not_identify_within_maternal_covariance":True,
            "paper_case_classification_was_derived_post_hoc":True,
            "chosen_morph_donor_studies_are_study_design_selected":True,
            "original_calystegia_donor_mechanism_is_prior_art":True,
            "original_morph_specific_pollination_results_are_prior_art":True,
            "one_source_per_publication_not_many_independent_cases":True,
            "frozen_fragmentation_5_8_16_still_unchanged":True,
            "theoretical_egwe_used":False,
            "submission_ready":False
        }
    }
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,
                                           indent=2,sort_keys=True)+"\n",
                               encoding="utf-8")
    print("GLOPL_SOURCE_PIN_PASS n=2969 pairs=811 publications=413 species=588")
    print("GLOPL_REPEATED n=130 mixed=29 nominal_both=13 dedup=129 mixed_dedup=28 nominal_dedup=12")
    print("GLOPL_CATEGORY",json.dumps(categorical,sort_keys=True))
    print("GLOPL_CATEGORY_CLUSTER_BOOT",bootstrap)
    print("GLOPL_ORIGINAL_NUMERIC_DUPLICATE",overlaps)
    print("GLOPL_CALYSTEGIA_DONOR_SOURCE",donor_anchor)


if __name__=="__main__":
    main()
