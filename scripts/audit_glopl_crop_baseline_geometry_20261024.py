#!/usr/bin/env python3
"""Empirical EGWEE: source-controlled fruit-set baseline, stage mismatch and nulls.

The wild/crop paired contrasts are source-locked GloPL FS/SPFR and PolLimCrop
FS/SN. Only first-order mean signs (not confirmed latent effect directions).
Do not infer mating-quality, reproductive allocation or fragmentation cause.

1. Measure within-publication association with naturally observed fruit set.
2. Distinguish FS direction from cross-stage direction discordance.
3. Permute downstream sign WITHIN publication, keeping source marginals fixed.
4. Permute supplemented fruit-set values WITHIN publication to demonstrate
   the baseline coupling that can arise from subtracting the same control mean.
5. Bootstrap publications, not plant/case rows. Remove Rosaceae/apple/largest
   crop source as predeclared sensitivity to concentration.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from audit_pollimcrop_glopl_cross_context_20261024 import (
    crop_rows, glopl_rows, direction, number, case_pair
)

ROOT=Path(__file__).resolve().parents[1]


def cases(rows,dom):
    a,b=("FS","SPFR") if dom=="wild" else ("FS","SN")
    key="unique_study_number" if dom=="wild" else "article_code"
    kind="Family" if dom=="wild" else "family"
    sp="Species_accepted_names" if dom=="wild" else "species"
    scale=1.0 if dom=="wild" else 100.0
    output=[]
    for row,sg_fs,sg_seeds in case_pair(rows,a,b,dom):
        if not sg_fs or not sg_seeds:
            continue
        nat_key="Natural_X_FS" if dom=="wild" else "FS_NAT_m"
        sup_key="Sup_X_FS" if dom=="wild" else "FS_SUP_m"
        natural=number(row[nat_key])
        supplemental=number(row[sup_key])
        assert 0<=natural<=scale and 0<=supplemental<=scale
        output.append({
            "study":row[key],
            "family":row[kind],
            "species":row[sp].strip(),
            "scale":row["Level_of_Supplementation"] if dom=="wild" else row["scale"],
            "baseline":natural/scale,
            "supplemented":supplemental/scale,
            "seed_increases":int(sg_seeds>0),
            "fs_declines":int(sg_fs<0),
            "seed_declines":int(sg_seeds<0),
            "discordance":int(sg_fs!=sg_seeds),
            "mixed_percent_tiny_pair":bool(
                dom=="crop" and 0<=natural<=1 and 0<=supplemental<=1
            )
        })
    return output


def site_analysis(rows, label, seed, draws=6500, perm_draws=5500):
    rng=np.random.default_rng(seed)
    groups=defaultdict(list)
    for row in rows:
        groups[row["study"]].append(row)
    assert len(groups)>10
    components=[]
    for source,g in sorted(groups.items()):
        x=np.asarray([r["baseline"] for r in g],dtype=float)
        fs=np.asarray([r["fs_declines"] for r in g],dtype=int)
        y=np.asarray([r["seed_declines"] for r in g],dtype=int)
        discord=np.asarray([r["discordance"] for r in g],dtype=int)
        supplemented=np.asarray([r["supplemented"] for r in g],dtype=float)
        centered=x-x.mean()
        den=float(centered@centered)
        nu=np.array([float(centered@fs),
                     float(centered@y),
                     float(centered@discord)],float)
        k=len(g)
        up=k-fs.sum()
        seed_up=k-y.sum()
        expected=(up*(k-seed_up)+(k-up)*seed_up)/k
        # Counts: FS+ versus seed- OR FS- versus seed+
        observed=int(discord.sum())
        components.append({
            "source":source,
            "n":k,
            "x":x,
            "xc":centered,
            "supplemented":supplemented,
            "fs":fs,
            "seedneg":y,
            "discordance":discord,
            "den":den,
            "num":nu,
            "observed":observed,
            "expected":expected,
        })
    nsource=len(components)
    matrix=np.stack([c["num"] for c in components])
    den=np.asarray([c["den"] for c in components])
    numer=matrix.sum(axis=0)
    denom=den.sum()
    assert denom>1e-9
    slope=numer/denom
    labels=("fs_decline","seed_decline","stage_discordance")
    slope_obj=dict(zip(labels,slope.tolist()))
    boot_ids=rng.integers(0,nsource,size=(draws,nsource))
    boot_denom=den[boot_ids].sum(axis=1)
    valid=boot_denom>1e-12
    boot_slopes=np.sum(matrix[boot_ids],axis=1)[valid] / boot_denom[valid,None]
    boot95={
        key:[float(z) for z in np.quantile(boot_slopes[:,j],[.025,.975])]
        for j,key in enumerate(labels)}
    leave_range={
        key:[
            float(np.min([(numer[j]-c["num"][j])/(denom-c["den"])
                          for c in components])),
            float(np.max([(numer[j]-c["num"][j])/(denom-c["den"])
                          for c in components]))]
        for j,key in enumerate(labels)
    }
    observed=sum(c["observed"] for c in components)
    expected=sum(c["expected"] for c in components)
    ntotal=sum(c["n"] for c in components)
    obs_pub=np.array([c["observed"]/c["n"] for c in components])
    expect_pub=np.array([c["expected"]/c["n"] for c in components])
    gain_pub=expect_pub-obs_pub
    gain_boot=np.mean(gain_pub[boot_ids],axis=1)
    expected_null=np.zeros(perm_draws)
    fs_baseline_null=np.zeros(perm_draws)
    for perm in range(perm_draws):
        total_discord=0
        fs_num=0.0
        for c in components:
            # Exact source-margin conditional null, no ecological independence
            # assumption between papers or across species is required.
            shuffled_down=rng.permutation(c["seedneg"])
            total_discord+=int(np.sum(c["fs"] != shuffled_down))
            # A different, deliberately artificial source pairing break:
            # experiment-specific supplemented mean no longer belongs to its
            # original control baseline. A null of *broken case matching*,
            # not a null of random ecological treatment effects.
            shuffled_sup=rng.permutation(c["supplemented"])
            fs_num+=float(c["xc"]@(shuffled_sup<c["x"]))
        expected_null[perm]=total_discord/ntotal
        fs_baseline_null[perm]=fs_num/denom
    p_lower=float((1+np.sum(expected_null<=observed/ntotal+1e-12))/
                   (perm_draws+1))
    result={
        "frame":label,"n_cases":ntotal,"publication_groups":nsource,
        "sources_with_baseline_variation":sum(c["den"]>0 for c in components),
        "sources_informative_for_sign_independence":sum(
            c["n"]>1 and 0<c["fs"].sum()<c["n"] and
            0<c["seedneg"].sum()<c["n"] for c in components
        ),
        "natural_FS_declines":sum(int(c["fs"].sum()) for c in components),
        "stage_discordant":observed,
        "within_publication_slopes_per_0_to_1_natural_FS":slope_obj,
        "publication_cluster_bootstrap95":boot95,
        "leave_one_publication_slopes_range":leave_range,
        "pub_sign_margin_null":{
            "observed_case_fraction":observed/ntotal,
            "expected_discordant_count":expected,
            "expected_case_fraction":expected/ntotal,
            "observed_minus_expected":(observed-expected)/ntotal,
            "observed_publication_equal":float(obs_pub.mean()),
            "expected_publication_equal":float(expect_pub.mean()),
            "source_equal_gain95": [
                float(z) for z in np.quantile(gain_boot,[.025,.975])
            ],
            "within_publication_permutation_p_lower_tail":p_lower,
            "permuted_case_fraction95": [
                float(z) for z in np.quantile(expected_null,[.025,.975])
            ],
            "caution":"Source-balanced gain intervals cross zero; permutation assumes exchangeability of endpoint sign assignments within original publication, not of landscapes"
        },
        "break_FSUP_baseline_pairing_diagnostic":{
            "observed_FSdecline_slope":float(slope[0]),
            "expected_slope_under_source_within_shuffling":
                float(fs_baseline_null.mean()),
            "shuffled_slope95": [
                float(z) for z in np.quantile(fs_baseline_null,[.025,.975])
            ],
            "not_an_ecological_null":"Changing pairings of natural/supplemented recorded means creates a steeper baseline-to-decline relation by construction. This diagnoses shared-control bounded-measure geometry, not causal environmental effects."
        },
    }
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    wild,sha=glopl_rows()
    crop,provenance=crop_rows()
    W=cases(wild,"wild")
    C=cases(crop,"crop")
    assert (len(W),len(C))==(313,300)
    assert (sum(r["discordance"] for r in W),
            sum(r["discordance"] for r in C))==(81,75)
    # Show exact numeric source frames and sensitivity to strongly represented
    # Rosaceae / apple; data are not collapsed into an effect-size pool.
    largest=Counter(r["study"] for r in C).most_common(1)[0][0]
    frames={
        "wild_all":W,
        "crop_all":C,
        "wild_flower_supplement": [
            r for r in W if r["scale"]=="flower"],
        "wild_whole_plant_supplement": [
            r for r in W if r["scale"]=="whole_plant"],
        "crop_without_Malus": [
            r for r in C if r["species"]!="Malus domestica"],
        "crop_without_Rosaceae": [
            r for r in C if r["family"]!="Rosaceae"],
        "crop_without_largest_publication":[
            r for r in C if r["study"]!=largest],
        "crop_excluding_ambiguous_tiny_percent_FSes": [
            r for r in C if not r["mixed_percent_tiny_pair"]],
    }
    details={}
    for i,(name,rs) in enumerate(frames.items()):
        details[name]=site_analysis(rs,name,seed=20261024+31*i,
                                    draws=4500,perm_draws=4000)
    assert abs(details["wild_all"]["within_publication_slopes_per_0_to_1_natural_FS"]["fs_decline"]-
               .48716807958)<1e-6
    assert abs(details["crop_all"]["within_publication_slopes_per_0_to_1_natural_FS"]["fs_decline"]-
               .4896869010)<1e-6
    assert abs(details["wild_all"]["within_publication_slopes_per_0_to_1_natural_FS"]["stage_discordance"]-
               .35165311002)<1e-6
    assert abs(details["crop_all"]["within_publication_slopes_per_0_to_1_natural_FS"]["stage_discordance"]-
               .06689236209)<1e-6
    assert details["crop_without_Rosaceae"]["n_cases"]==108
    result={
        "status":"exploratory ecological baseline and falsification boundary",
        "source_wild_stored_blob_SHA":sha,
        "source_crop_stored_integrity":provenance,
        "common_question":"natural fruit-set baseline association and sign-coherence beyond source-specific null pairing",
        "estimand_mismatch":"wild downstream SPFR seeds per existing fruit; crop SN seed number as reported",
        "source_units":"wild natural FS reported 0..1; crop natural FS 0..100, divided by 100 for numerical unit only; ambiguous 0..1 crop source values screened separately",
        "frames":details,
        "crop_largest_publication":largest,
        "claim_gate":{
            "stage_discordance_is_a_point_contrast_not_certified_reversal":True,
            "source_conditional_mismatch_slope_CI_crosses_zero_in_both":(
                details["wild_all"]["publication_cluster_bootstrap95"]["stage_discordance"][0]<0<
                details["wild_all"]["publication_cluster_bootstrap95"]["stage_discordance"][1] and
                details["crop_all"]["publication_cluster_bootstrap95"]["stage_discordance"][0]<0<
                details["crop_all"]["publication_cluster_bootstrap95"]["stage_discordance"][1]
            ),
            "natural_FS_baseline_coupled_to_sign_of_difference_mathematically":True,
            "environmental_or_mating_causation_identified":False,
            "fragmentation_corpus_5_8_16_unchanged":True,
            "submission_ready":False,
        }
    }
    assert result["claim_gate"]["source_conditional_mismatch_slope_CI_crosses_zero_in_both"]
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,
                                           sort_keys=True)+"\n",encoding="utf-8")
    print("GLOPL_CROP_BASELINE_SOURCE_OK",len(W),len(C),sha)
    for name,v in details.items():
        print("BASELINE_GEOMETRY",name,"n",v["n_cases"],"sources",v["publication_groups"],
              "slope_FSdecline",round(
                  v["within_publication_slopes_per_0_to_1_natural_FS"]["fs_decline"],6),
              "slope_discord",round(
                  v["within_publication_slopes_per_0_to_1_natural_FS"]["stage_discordance"],6),
              "discord95",v["publication_cluster_bootstrap95"]["stage_discordance"],
              "paired_null_case",v["pub_sign_margin_null"]["expected_case_fraction"],
              "observed_case",v["pub_sign_margin_null"]["observed_case_fraction"])


if __name__=="__main__":
    main()
