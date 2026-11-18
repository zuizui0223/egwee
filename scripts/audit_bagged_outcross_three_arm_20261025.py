#!/usr/bin/env python3
"""EGWEE empirical study: bagged manual outcross != natural pollinator access.

Source A: GloPL 2018, 2969 literature cases, NAT / Sup / Bagout treatments.
Source B: Sevenello et al. 2026 Western Australian remnant experiment, 520
          quadrats with FOUR distinct treatment plants each.

Exploratory comparison of (1) *same* GloPL case three-arm rankings and stages,
(2) broad publication-balanced bagged-outcross versus natural control,
(3) independent-site reserve-ordering in ONE Sevenello landscape.

This is NOT a causal meta-estimate pooling different treatment protocols,
and does not enlarge frozen EGWEE fragmentation programmes 5/8/16.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
GLOPL = ROOT / "evidence/meta_extraction/glopl_2018/GloPL_with_id.csv"
GLOPL_STORED_BLOB = "0809eaeee54e4375d26bacfe002787241f8ff72e"
GLOPL_UPSTREAM_BLOB = "d22fe333b19489c473e076dd173ed7a67b1afbf0"
SEVENELLO = ROOT / "evidence/meta_extraction/sevenello_2026_raw/landscape_seeds.csv"
SEVENELLO_MD5 = "40caf98755786e32bec89fffd4b114f6"
ENDPOINTS = ("FS","SO","SPFR","SPFL","SPP")

def mean(a):
    assert len(a)>0
    return float(np.mean(a))

def read_glopl():
    raw = GLOPL.read_bytes()
    sha = hashlib.sha1(f"blob {len(raw)}\0".encode("ascii")+raw).hexdigest()
    assert sha == GLOPL_STORED_BLOB, sha
    with GLOPL.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows)==2969
    assert len({r["unique_study_number"] for r in rows})==927
    return rows,sha

def read_sevenello():
    raw=SEVENELLO.read_bytes()
    assert len(raw)==135336 and hashlib.md5(raw).hexdigest()==SEVENELLO_MD5
    with SEVENELLO.open("r",encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==2080
    return rows

def observed(s):
    if s is None or s.strip() in ("","NA","NaN","nan"):return None
    try:
        x=float(s)
    except ValueError:
        return None
    return x if np.isfinite(x) and x>=0 else None

def triple_means(r, endpoint):
    vals=[observed(r[p+endpoint]) for p in
          ("Natural_X_","Sup_X_","Bagout_X_")]
    if any(z is None for z in vals):
        return None
    return tuple(vals)

def natural_bag(r, endpoint):
    a=observed(r["Natural_X_"+endpoint])
    b=observed(r["Bagout_X_"+endpoint])
    if a is None or b is None:
        return None
    return a,b

def rank_label(n,s,b):
    if len({n,s,b})<3:return "tie"
    d={"N":n,"S":s,"B":b}
    return "<".join(sorted(d,key=d.get))

def publication_summary(rows, endpoint, seed=20261025):
    studies=defaultdict(list)
    for r in rows:
        pair=natural_bag(r,endpoint)
        if pair is not None:
            studies[r["unique_study_number"]].append((r,pair))
    cases=[(r,x) for group in studies.values() for r,x in group]
    sig=sum(b>n for r,(n,b) in cases)
    nonsig=sum(b<n for r,(n,b) in cases)
    zero=sum(b==n for r,(n,b) in cases)
    fracs=np.array([mean([b>n for r,(n,b) in xs])
                    for xs in studies.values()],dtype=float)
    rng=np.random.default_rng(seed)
    indices=rng.integers(0,len(fracs),size=(10000,len(fracs)))
    boot=fracs[indices].mean(axis=1)
    # Descriptive nominal independent-arm z screen, NOT model-ready inference:
    # source responses and sample sizes can share maternal plants and covariance.
    zcases=[]
    for r,(n,b) in cases:
        n0=observed(r["Natural_N_"+endpoint])
        n1=observed(r["Bagout_N_"+endpoint])
        sd0=observed(r["Natural_SD_"+endpoint])
        sd1=observed(r["Bagout_SD_"+endpoint])
        if any(x is None for x in (n0,n1,sd0,sd1)) or min(n0,n1)<=1:
            continue
        se=(sd0**2/n0+sd1**2/n1)**.5
        if se>0:
            zcases.append((r,(b-n)/se))
    z196=[(r,z) for r,z in zcases if abs(z)>=1.96]
    scales=defaultdict(list)
    for r,(n,b) in cases:
        scales[r["Level_of_Supplementation"]].append((r,n,b))
    return {
        "observed_cases":len(cases),
        "distinct_publications":len(studies),
        "distinct_families":len({r["Family"] for r,(n,b) in cases}),
        "bagout_gt_natural":sig,
        "natural_gt_bagout":nonsig,
        "equal":zero,
        "bagout_gt_natural_publications_any":
           len({r["unique_study_number"] for r,(n,b) in cases if b>n}),
        "natural_gt_bagout_publications_any":
           len({r["unique_study_number"] for r,(n,b) in cases if n>b}),
        "case_fraction_bagout_gt_natural":sig/len(cases),
        "publication_equal_fraction_bagout_gt_natural":mean(fracs),
        "publication_cluster_bootstrap95":[float(x) for x in
                                            np.quantile(boot,[.025,.975])],
        "scale":{k:{"cases":len(v),"positive":sum(b>n for r,n,b in v),
                    "publications":len({r["unique_study_number"] for r,n,b in v})}
                 for k,v in sorted(scales.items())},
        "rough_z_nonzero_se_available":len(zcases),
        "rough_z_abs_ge_1_96":len(z196),
        "rough_z_positive_cases":sum(z>0 for r,z in z196),
        "rough_z_negative_cases":sum(z<0 for r,z in z196),
        "rough_z_positive_publications":len({r["unique_study_number"]
                                            for r,z in z196 if z>0}),
        "rough_z_negative_publications":len({r["unique_study_number"]
                                            for r,z in z196 if z<0}),
        "precision_warning":"N, SD and marginal mean z reference ignore same-maternal/within-study dependence, bounded outcomes and simultaneous testing; point signs are not certified treatment effects",
    }

def triple_summary(rows, endpoint):
    cases=[(r,triple_means(r,endpoint)) for r in rows]
    cases=[(r,v) for r,v in cases if v is not None]
    pub=defaultdict(list)
    for r,(n,s,b) in cases:
        pub[r["unique_study_number"]].append((n,s,b))
    ranks=Counter(rank_label(*v) for r,v in cases)
    def pub_avg(pred):
        return mean([mean([pred(*v) for v in values]) for values in pub.values()])
    return {
        "observed_three_arm_cases":len(cases),
        "publications":len(pub),
        "species":len({r["Species_accepted_names"] for r,v in cases}),
        "families":len({r["Family"] for r,v in cases}),
        "rankings":dict(ranks),
        "bagout_gt_natural":sum(b>n for r,(n,s,b) in cases),
        "natural_gt_bagout":sum(n>b for r,(n,s,b) in cases),
        "supplement_gt_natural":sum(s>n for r,(n,s,b) in cases),
        "bagout_gt_supplement":sum(b>s for r,(n,s,b) in cases),
        "supplement_gt_bagout":sum(s>b for r,(n,s,b) in cases),
        "publication_equal_bagout_gt_natural":pub_avg(lambda n,s,b:b>n),
        "publication_equal_supplement_gt_natural":pub_avg(lambda n,s,b:s>n),
        "publication_equal_bagout_gt_supplement":pub_avg(lambda n,s,b:b>s),
        "natural_gt_bagout_distinct_publications":
            len({r["unique_study_number"] for r,(n,s,b) in cases if n>b}),
        "natural_gt_bagout_distinct_families":
            len({r["Family"] for r,(n,s,b) in cases if n>b}),
    }

def same_case_cross_stage(rows):
    both=[(r, triple_means(r,"FS"), triple_means(r,"SPFR")) for r in rows]
    both=[(r,a,b) for r,a,b in both if a is not None and b is not None]
    flags=Counter()
    pubs=defaultdict(list)
    switched=[]
    strict=[]
    n_fs_bagbetter=n_spfr_bagbetter=0
    for r,a,b in both:
        # A tuple is Natural, Sup, Bagout in precisely the same source case.
        bg=bool(np.sign(a[2]-a[0])!=np.sign(b[2]-b[0]))
        sp=bool(np.sign(a[1]-a[0])!=np.sign(b[1]-b[0]))
        flags[("bagged_diff" if bg else "bagged_same")+
              "_"+("open_added_diff" if sp else "open_added_same")]+=1
        fs_bs=int(np.sign(a[2]-a[1]))
        spfr_bs=int(np.sign(b[2]-b[1]))
        assert fs_bs!=0 and spfr_bs!=0, (r["unique_number"],fs_bs,spfr_bs)
        fs_bagbetter=int(fs_bs>0)
        seed_bagbetter=int(spfr_bs>0)
        n_fs_bagbetter+=fs_bagbetter
        n_spfr_bagbetter+=seed_bagbetter
        pubs[r["unique_study_number"]].append(seed_bagbetter-fs_bagbetter)
        if fs_bagbetter!=seed_bagbetter:
            switched.append(r)
        # If any of four changes relative to Natural equals zero, do not
        # call it a strictly resolved binary stage discordance contrast.
        if all(np.sign(v[2]-v[0])!=0 and np.sign(v[1]-v[0])!=0 for v in (a,b)):
            strict.append((r,bg,sp))
    forward=sum(x==1 for vals in pubs.values() for x in vals)
    reverse=sum(x==-1 for vals in pubs.values() for x in vals)
    assert (len(both),len(pubs),n_fs_bagbetter,n_spfr_bagbetter,
            forward,reverse)==(22,8,9,18,10,1)
    paper_mean=np.array([mean(v) for v in pubs.values()],dtype=float)
    rng=np.random.default_rng(20261025)
    boot=paper_mean[rng.integers(0,len(paper_mean),
         size=(25000,len(paper_mean)))].mean(axis=1)
    # Third-stage sanity check on exactly the same source cases. Seeds per
    # flower measures flower-wide output, unlike seeds per existing fruit.
    all_three_stage=[
        (r,a,b,triple_means(r,"SPFL"))
        for r,a,b in both if triple_means(r,"SPFL") is not None
    ]
    forward_three=[
        (r,a,b,c) for r,a,b,c in all_three_stage
        if a[2]<a[1] and b[2]>b[1]
    ]
    assert len(all_three_stage)==11
    assert len({r["unique_study_number"] for r,a,b,c
                in all_three_stage})==3
    assert len(forward_three)==4
    assert sum(c[2]<c[1] for r,a,b,c in forward_three)==2
    assert sum(c[2]>c[1] for r,a,b,c in forward_three)==2
    by_paper={
        p:{"n_cases":len(differences),
           "mean_SPFR_minus_FS_bagwin":mean(differences),
           "forward_switch":sum(x==1 for x in differences),
           "reverse_switch":sum(x==-1 for x in differences)}
        for p,differences in sorted(pubs.items(),key=lambda item:int(item[0]))
    }
    strict_only=sum(bg!=sp for _,bg,sp in strict)
    assert (len(strict),strict_only)==(18,10)
    return {
        "same_case_six_means":len(both),
        "publications":len(pubs),
        "families":len({r["Family"] for r,a,b in both}),
        "both_intervention_stage_comparisons":dict(flags),
        "third_output_seed_per_flower_subset":{
            "n_same_case_natural_supp_bagged_for_FS_SPFR_SPFL":
                len(all_three_stage),
            "distinct_publications":len({r["unique_study_number"] for r,a,b,c
                                          in all_three_stage}),
            "FS_open_supp_higher_SPFR_bagout_higher_cases":
                len(forward_three),
            "among_forward_switches_seed_per_flower_agrees_with_FS":
                sum(c[2]<c[1] for r,a,b,c in forward_three),
            "among_forward_switches_seed_per_flower_agrees_with_SPFR":
                sum(c[2]>c[1] for r,a,b,c in forward_three),
            "caveat":"11 cases/3 publications only, and seeds per flower is independently reported rather than reconstructed from marginal product",
        },
        "method_specific_stage_discordance_count":sum(
            (k in {"bagged_diff_open_added_same",
                   "bagged_same_open_added_diff"})*v
            for k,v in flags.items()),
        "method_specific_stage_discordance_no_zero_contrasts":strict_only,
        "strict_no_zero_four_contrasts_cases":len(strict),
        "direct_Bagout_minus_Sup_by_reproductive_stage":{
            "Bagout_gt_Sup_in_FS":n_fs_bagbetter,
            "Bagout_gt_Sup_in_SPFR":n_spfr_bagbetter,
            "FS_Sup_gt_Bagout_then_SPFR_Bagout_gt_Sup":forward,
            "FS_Bagout_gt_Sup_then_SPFR_Sup_gt_Bagout":reverse,
            "case_direction_difference":(forward-reverse)/len(both),
            "publication_equal_direction_difference":mean(paper_mean),
            "publication_bootstrap_percentile95":
                [float(z) for z in np.quantile(boot,[.025,.975])],
            "publication_census":by_paper,
            "switched_cases_distinct_publications":
                len({r["unique_study_number"] for r in switched}),
            "switched_cases_distinct_families":
                len({r["Family"] for r in switched}),
            "no_simple_mechanism_claim":True,
        },
        "warning":"22 same cases from 8 source publications; FS and SPFR denominators differ, shared within-plant covariance unavailable, breeding-system heterogeneity and nonrandom measurement selection. All signs are published mean orders only.",
    }

def sevenello_perflower(rows):
    p=defaultdict(dict)
    for r in rows:
        ident=r["id_plot"]
        z=p[ident]
        if not "species" in z:
            z.update(species=r["species"],site=r["site"],
                     crop=r["crop_type"],side=r["transect"])
        assert r["treat"] not in z
        z[r["treat"]]={
            "seeds":observed(r["total_seeds"]),
            "flowers":observed(r["flower_num"]),
        }
    assert len(p)==520
    by_species={}
    all_cells=0
    for sp in ("LARO","POAR","POGN"):
        records=[v for v in p.values() if v["species"]==sp]
        valid=[z for z in records if all(
            z[t]["seeds"] is not None and
            z[t]["flowers"] is not None and
            z[t]["flowers"]>0
            for t in ("OP","OPSupp","Bag","BagSup"))]
        expect={"LARO":156,"POAR":111,"POGN":114}[sp]
        assert len(valid)==expect, (sp,len(valid))
        by_transect=defaultdict(list)
        for z in valid:
            op=z["OP"]["seeds"]/z["OP"]["flowers"]
            bs=z["BagSup"]["seeds"]/z["BagSup"]["flowers"]
            b=z["Bag"]["seeds"]/z["Bag"]["flowers"]
            by_transect[(z["site"],z["crop"],z["side"])].append(
                {"open_minus_bagged_manual":op-bs,
                 "manual_minus_bagged":bs-b,
                 "open_minus_bagged":op-b})
        by_crop=defaultdict(list)
        for (site,crop,side),samples in by_transect.items():
            by_crop[(site,crop)].append(
                {key:mean([x[key] for x in samples]) for key in samples[0]})
        by_site=defaultdict(list)
        for (site,crop),arms in by_crop.items():
            by_site[site].append({
                key:mean([x[key] for x in arms]) for key in arms[0]})
        sites=[{"site":site,**{key:mean([x[key] for x in blocks])
                            for key in blocks[0]}}
               for site,blocks in sorted(by_site.items())]
        assert len(sites)=={"LARO":6,"POAR":4,"POGN":6}[sp]
        measurements=tuple(k for k in sites[0] if k!="site")
        assert all(sum(x[key]>0 for x in sites)==len(sites)
                   for key in measurements)
        all_cells+=len(sites)
        by_species[sp]={
            "complete_four_arm_flower_exposure_quadrats":len(valid),
            "physical_reserves":len(sites),
            "reserves_with_open_gt_bagged_manual":
                sum(z["open_minus_bagged_manual"]>0 for z in sites),
            "perflower_contrasts_reserve_equal":{
                k:mean([z[k] for z in sites]) for k in measurements},
            "individual_site_contrasts":sites,
        }
    assert all_cells==16
    return {"one_source_landscape":True,
            "species_reserve_cells":all_cells,
            "source_independent_studies":1,
            "different_plant_treatments":True,
            "by_species":by_species,
            "warning":"Site×species observations share reserves and one source paper; bagging, manual dose, pollen-donor provenance and flower count differ from GloPL. Not a study-independent 16-replicate effect.",
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    wild,stored_sha=read_glopl()
    seven=read_sevenello()
    endpoint_result={e:publication_summary(wild,e,seed=20261025+7*i)
                     for i,e in enumerate(ENDPOINTS)}
    triple_result={e:triple_summary(wild,e) for e in ENDPOINTS}
    both=same_case_cross_stage(wild)
    sea=sevenello_perflower(seven)
    assert (endpoint_result["FS"]["observed_cases"],
            endpoint_result["FS"]["distinct_publications"],
            endpoint_result["FS"]["bagout_gt_natural"],
            endpoint_result["FS"]["natural_gt_bagout"],
            endpoint_result["FS"]["equal"])==(811,413,577,214,20)
    assert (endpoint_result["SPFL"]["observed_cases"],
            endpoint_result["SPFL"]["distinct_publications"],
            endpoint_result["SPFL"]["bagout_gt_natural"])==(51,25,44)
    assert (triple_result["FS"]["observed_three_arm_cases"],
            triple_result["FS"]["publications"],
            triple_result["FS"]["natural_gt_bagout"],
            triple_result["FS"]["natural_gt_bagout_distinct_publications"],
            triple_result["FS"]["natural_gt_bagout_distinct_families"]) == \
           (45,20,11,4,8)
    assert triple_result["FS"]["rankings"]=={
        "N<S<B":16, "B<N<S":4, "B<S<N":4,
        "N<B<S":12,"S<N<B":5,"tie":4
    }
    assert (both["same_case_six_means"],both["publications"])==(22,8)
    assert (sum(both["both_intervention_stage_comparisons"].values()),
            sea["species_reserve_cells"])==(22,16)
    out={
        "status":"retrospective_same_case_cross_programme_analogy_only",
        "empirical_egwee_not_theoretical_egwe":True,
        "GloPL_source_stored_utf8_blob":stored_sha,
        "GloPL_upstream_legacy_byte_blob":GLOPL_UPSTREAM_BLOB,
        "GloPL_bagged_outcross_vs_natural_by_endpoint":endpoint_result,
        "GloPL_same_case_open_added_bagged_manual":triple_result,
        "GloPL_six_means_two_stage_subset":both,
        "Sevenello_same_quadrat_4_arm_per_flower":sea,
        "claim_gate":{
            "same_kind_of_effect_size_across_programmes":False,
            "source_publications_not_case_rows_independent":True,
            "zero_effects_are_not_significance":True,
            "mechanism_identified":False,
            "prior_art_acknowledged":True,
            "frozen_5_8_16_fragmentation_programmes_changed":False,
            "submission_ready":False,
        }
    }
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(out,indent=2,sort_keys=True,
                                         ensure_ascii=False)+"\n",
                               encoding="utf-8")
    print("BAGGED_OUTCROSS_SOURCE_CONTRACT_OK",stored_sha,"GloPL",len(wild),
          "Sevenello",len(seven))
    for e,z in endpoint_result.items():
        print("GLOPL_BAGGED_NATURAL",e,"cases",z["observed_cases"],
              "sources",z["distinct_publications"],
              "bagged_gt",z["bagout_gt_natural"],"natural_gt",
              z["natural_gt_bagout"],"pub_equal",round(
                  z["publication_equal_fraction_bagout_gt_natural"],6),
              "boot95",z["publication_cluster_bootstrap95"])
    for e,z in triple_result.items():
        print("GLOPL_TRIPLE",e,"cases",z["observed_three_arm_cases"],
              "sources",z["publications"],"rankings",z["rankings"])
    print("GLOPL_SIX_MEANS",both["same_case_six_means"],
          both["publications"],both["both_intervention_stage_comparisons"])
    print("SEVENELLO_COMPARE",sea["species_reserve_cells"],
          {k:(v["physical_reserves"],
              v["reserves_with_open_gt_bagged_manual"])
           for k,v in sea["by_species"].items()})

if __name__=="__main__":
    main()
