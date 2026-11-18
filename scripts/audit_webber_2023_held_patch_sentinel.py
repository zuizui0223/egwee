#!/usr/bin/env python3
"""Peralta/Webber 2023: held-patch ecological sentinel calibration.

Read *original* CC0 Zenodo CSVs, verify source MD5, reconcile two documented
species-label mismatches and aggregate at the only shared biological grain:
experimental patch x planted plant species. Assess whether six-hour captures
(and size/richness descriptors) forecast mean seeds per *tagged flower* when
an ENTIRE PATCH, with all 7 species, is held out.

External one-farm/one-season comparator to empirical egwee; NOT an independent
forest-fragmentation effect or an admitted EGWEE primary/IF/SF06 programme.
The published article already reports positive in-sample FD–seed effects;
this particular exercise tests held-patch incremental diagnostic utility.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
import hashlib
import io
import json
import math
import random
from pathlib import Path
from urllib.request import Request, urlopen

BASE="https://zenodo.org/records/7618753/files/"
PINS={
    "Data_S1.csv":"ae6df5d3d1a5d6cac12aa509752c74a5",
    "Data_S2.csv":"7a5c3020cbd084470ed4fe5e6de45cd3",
}
SPECIES={
    "anise.hyssop":"anisehyssop","anise hyssop":"anisehyssop",
    "nepeta":"nepeta","napeta":"nepeta",
}
SEED_SPECIES={"lucerne","buckwheat","canola","nepeta",
              "anisehyssop","clover","coreopsis"}
FEATURES={
    "species_mean_only":(),
    "captured_visitors_same_plant_species":("species_captures",),
    "total_patch_captures":("patch_captures",),
    "patch_visitor_taxon_richness":("taxon_richness",),
    "patch_rarefied_taxon_richness":("rarefied_taxon_richness",),
    "patch_mean_visitor_size":("mean_itd",),
    "patch_body_size_dispersion":("log_itd_sd",),
    "patch_body_size_range":("size_range_taxon_means",),
    "patch_1d_FEve_proxy":("feve_proxy",),
    "patch_rarefied_1d_FEve_proxy":("rarefied_feve_proxy",),
    "species_captures_plus_taxon_richness":("species_captures","taxon_richness"),
    "patch_total_captures_plus_taxon_richness":("patch_captures","taxon_richness"),
    "patch_total_captures_plus_rarefied_richness":("patch_captures","rarefied_taxon_richness"),
    "species_captures_plus_patch_total":("species_captures","patch_captures"),
    "species_captures_plus_size_dispersion":("species_captures","log_itd_sd"),
}

def read(name: str, local_dir:Path|None) -> tuple[list[dict[str,str]],str]:
    assert name in PINS
    if local_dir:
        raw=(local_dir/name).read_bytes()
    else:
        req=Request(BASE+name+"?download=1",headers={
            "User-Agent":"EGWEE-open-CC0-patch-sentinel/1",
            "Accept":"text/csv"})
        with urlopen(req,timeout=65) as response:
            assert response.status==200
            raw=response.read()
    digest=hashlib.md5(raw).hexdigest()
    assert digest==PINS[name],(name,digest,PINS[name])
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))),digest

def canonical(name:str)->str:
    token=name.strip().lower()
    return SPECIES.get(token,token.replace(".","").replace(" ",""))

def one_dimensional_fev_proxy(taxon_by_size:dict[str,list[float]])->float:
    """One-dimensional minimum-spanning-tree edge-evenness analogue of FEve.

    Taxa mean ITD are sorted, with adjacent edges weighted by inverse summed
    abundances. Unlike original R FD::dbFD FEve, this has not been independently
    checked for package-specific algorithm behavior; descriptive proxy ONLY.
    """
    if len(taxon_by_size)<3:
        return 0.
    ordered=sorted((sum(v)/len(v),len(v)) for v in taxon_by_size.values())
    edges=[max(0.,ordered[i+1][0]-ordered[i][0])/
           (ordered[i][1]+ordered[i+1][1])
           for i in range(len(ordered)-1)]
    total=sum(edges)
    if total<=1e-12:
        return 0.
    e=len(edges)
    uniform=1./e
    evenness=(sum(min(w/total,uniform) for w in edges)-uniform)/(1.-uniform)
    return max(0.,min(1.,evenness))


def prepare(local_dir:Path|None)->tuple[list[dict],dict]:
    captures,hash_i=read("Data_S1.csv",local_dir)
    flowers,hash_f=read("Data_S2.csv",local_dir)
    assert len(captures)==1470 and len(flowers)==3430
    assert set(captures[0])=={"Patch","Plant","ITD","Family","Genus","Species"}
    assert set(flowers[0])=={"patch","plant","plant.number","seeds"}
    patch_records=defaultdict(list)
    taxon_records=defaultdict(lambda:defaultdict(list))
    patch_taxon_visitor_records=defaultdict(list)
    patch_species_captures=Counter()
    sample_plants=Counter()
    seed_total=Counter()
    seed_n=Counter()
    seed_zero=Counter()
    visitor_taxa=set()
    for row in captures:
        p=int(row["Patch"])
        s=canonical(row["Plant"])
        itd=float(row["ITD"])
        assert 1<=p<=14 and math.isfinite(itd) and itd>0
        taxon="|".join((row["Family"],row["Genus"],row["Species"]))
        patch_records[p].append(itd)
        taxon_records[p][taxon].append(itd)
        patch_taxon_visitor_records[p].append((taxon,itd))
        patch_species_captures[(p,s)]+=1
        visitor_taxa.add(taxon)
    for row in flowers:
        p=int(row["patch"])
        s=canonical(row["plant"])
        plant_id=row["plant.number"].strip()
        seeds=float(row["seeds"])
        assert 1<=p<=14 and s in SEED_SPECIES
        assert plant_id and math.isfinite(seeds) and 0<=seeds<=100
        key=(p,s)
        seed_total[key]+=seeds
        seed_n[key]+=1
        seed_zero[key]+=int(seeds==0)
        sample_plants[(p,s,plant_id)]+=1
    assert len(seed_total)==98 and len(sample_plants)==686
    assert all(v==5 for v in sample_plants.values())
    assert set(s for _,s in seed_total)==SEED_SPECIES
    assert set(p for p,_ in seed_total)==set(range(1,15))
    assert len(patch_records)==14 and sum(map(len,patch_records.values()))==1470
    patch_features={}
    min_capture_n=min(len(v) for v in patch_records.values())
    assert min_capture_n==54
    def sample_absent_probability(N:int,n_taxon:int,m:int)->float:
        # P(no one from this taxon in m draws without replacement).
        assert 0<n_taxon<=N and 0<=m<=N
        if N-n_taxon<m:
            return 0.
        probability=1.
        for i in range(m):
            probability*=((N-n_taxon-i)/(N-i))
        return probability
    for p in range(1,15):
        values=patch_records[p]
        logs=[math.log(v) for v in values]
        mu=sum(logs)/len(logs)
        taxon_means=[sum(v)/len(v) for v in taxon_records[p].values()]
        rarefied=sum(
            1.-sample_absent_probability(len(values),len(z),min_capture_n)
            for z in taxon_records[p].values()
        )
        assert 0<rarefied<=len(taxon_records[p])+1e-9
        feve=one_dimensional_fev_proxy(taxon_records[p])
        assert 0<=feve<=1
        rng=random.Random(20261018+p)
        draw_features=[]
        for _ in range(300):
            subsample=rng.sample(patch_taxon_visitor_records[p],min_capture_n)
            represented=defaultdict(list)
            for tag,trait in subsample:
                represented[tag].append(trait)
            draw_features.append(one_dimensional_fev_proxy(represented))
        rarefied_feve=sum(draw_features)/len(draw_features)
        assert 0<=rarefied_feve<=1
        patch_features[p]={
            "feve_proxy":feve,
            "rarefied_feve_proxy":rarefied_feve,
            "patch_captures":math.log1p(len(values)),
            "rarefied_taxon_richness":rarefied,
            "taxon_richness":float(len(taxon_records[p])),
            "mean_itd":sum(values)/len(values),
            "log_itd_sd":math.sqrt(sum((v-mu)**2 for v in logs)/len(logs)),
            # Experimental 1D trait range proxy; NOT identical to the source
            # article's trait functional-diversity model or its FEve measure.
            "size_range_taxon_means":max(taxon_means)-min(taxon_means),
        }
    rows=[]
    for (p,s),total in sorted(seed_total.items()):
        n=seed_n[(p,s)]
        assert n>0
        row={
            "patch":p,"species":s,"n_tagged_flowers":n,
            "mean_seeds_per_flower":total/n,
            "seed_zeros":seed_zero[(p,s)],
            "y":math.log1p(total/n),
            "species_captures":math.log1p(patch_species_captures[(p,s)]),
            "n_same_plant_visitors_captured":patch_species_captures[(p,s)],
            **patch_features[p],
        }
        rows.append(row)
    zero_capture=[r for r in rows if r["n_same_plant_visitors_captured"]==0]
    assert len(zero_capture)==19 and all(r["mean_seeds_per_flower"]>0 for r in zero_capture)
    return rows,{
        "source_doi":"10.5061/dryad.5qfttdz9q",
        "published_analysis_doi":"10.1111/ecog.06453",
        "zenodo_record":"https://zenodo.org/records/7618753",
        "source_MD5":{"Data_S1.csv":hash_i,"Data_S2.csv":hash_f},
        "n_patch_experimental_units":14,
        "n_distinct_seed_production_species":len(SEED_SPECIES),
        "n_patch_species_shared_cells":len(rows),
        "n_capture_records":len(captures),
        "n_distinct_captured_visitor_taxa":len(visitor_taxa),
        "n_tagged_flower_seed_records":len(flowers),
        "n_separately_tagged_plants":len(sample_plants),
        "flowers_per_tagged_plant":"exactly five",
        "n_no_capture_patch_species_cells_with_positive_seed_output":len(zero_capture),
        "all_patch_rarefaction_sample_size":min_capture_n,
        "rarefaction":"Expected taxon-label richness under hypergeometric draws of 54 captures without replacement in each patch, calculated from capture label frequencies (not species true richness).",
        "trait_evenness_proxy":"1D taxon-mean-ITD MST edge regularity weighted by abundance; NOT independently validated against original R FD::dbFD FEve.",
        "rarefied_evenness":"Mean of 300 fixed-seed (20261018+patch) without-replacement 54-capture subsamples of the 1D FEve proxy; descriptive effort sensitivity.",
        "label_reconciliation":{
            "Anise.Hyssop vs Anise Hyssop":"anisehyssop",
            "Nepeta vs Napeta":"nepeta",
        },
        "plant_species":sorted(SEED_SPECIES),
        "sampling":"Six 1-hour insect capture surveys per patch, Dec 2012 to Feb 2013; 5 tagged flowers per sampled plant",
        "not_fragment_vs_control":"14 isolated planted flower patches in one pasture; no paired continuous habitat or randomized forest fragmentation control.",
    }

def linear_solve(gram:list[list[float]],rhs:list[float])->list[float]:
    n=len(rhs)
    if n==0:return []
    a=[line[:]+[v] for line,v in zip(gram,rhs)]
    for j in range(n):
        k=max(range(j,n),key=lambda i:abs(a[i][j]))
        a[k],a[j]=a[j],a[k]
        assert abs(a[j][j])>1e-10
        v=a[j][j]
        for t in range(j,n+1):a[j][t]/=v
        for i in range(n):
            if i==j:continue
            q=a[i][j]
            for t in range(j,n+1):a[i][t]-=q*a[j][t]
    return [a[i][-1] for i in range(n)]

def held_patch_predict(rows:list[dict],pred:tuple[str,...])->dict:
    species=sorted({r["species"] for r in rows})
    predictions=[]
    for held in sorted({r["patch"] for r in rows}):
        train=[r for r in rows if r["patch"]!=held]
        test=[r for r in rows if r["patch"]==held]
        assert len(train)==91 and len(test)==7
        ymu={}
        ysd={}
        fmu={}
        for s in species:
            a=[r for r in train if r["species"]==s]
            assert len(a)==13
            mean=sum(r["y"] for r in a)/len(a)
            sd=math.sqrt(sum((r["y"]-mean)**2 for r in a)/len(a))
            ymu[s]=mean
            ysd[s]=max(0.05,sd)
            fmu[s]={f:sum(r[f] for r in a)/len(a) for f in pred}
        scales={}
        for f in pred:
            z=[r[f]-fmu[r["species"]][f] for r in train]
            scales[f]=max(1e-8,math.sqrt(sum(v*v for v in z)/len(z)))
        X=[[(r[f]-fmu[r["species"]][f])/scales[f] for f in pred]
           for r in train]
        Y=[(r["y"]-ymu[r["species"]])/ysd[r["species"]] for r in train]
        if pred:
            n=len(pred)
            gram=[[sum(x[i]*x[j] for x in X)+(1. if i==j else 0.)
                    for j in range(n)] for i in range(n)]
            rhs=[sum(x[j]*y for x,y in zip(X,Y)) for j in range(n)]
            beta=linear_solve(gram,rhs)
        else:beta=[]
        for r in test:
            yz=sum(beta[j]*(r[f]-fmu[r["species"]][f])/scales[f]
                   for j,f in enumerate(pred))
            predictions.append({
                "patch":held,"species":r["species"],"obs_log_seed_mean":r["y"],
                "predict_log_seed_mean":ymu[r["species"]]+ysd[r["species"]]*yz,
                "error_standardized":(r["y"]-ymu[r["species"]])/ysd[r["species"]]-yz,
            })
    assert len(predictions)==98
    def avg(items:list[float])->float:
        return sum(items)/len(items)
    return {
        "standardized_MSE_equal_species_and_patch":avg([r["error_standardized"]**2
                                                      for r in predictions]),
        "raw_log_seed_MSE":avg([(r["obs_log_seed_mean"]-r["predict_log_seed_mean"])**2
                              for r in predictions]),
        "heldout_patch_standardized_MSE":{
            str(p):avg([r["error_standardized"]**2 for r in predictions if r["patch"]==p])
            for p in range(1,15)},
        "heldout_species_standardized_MSE":{
            s:avg([r["error_standardized"]**2 for r in predictions if r["species"]==s])
            for s in species},
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--local-dir",type=Path,help="Local original source CSV files (MD5 verified)")
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    rows,source=prepare(args.local_dir)
    scores={name:held_patch_predict(rows,pred) for name,pred in FEATURES.items()}
    baseline=scores["species_mean_only"]
    for name,val in scores.items():
        val["percent_standardized_MSE_improvement_over_species_mean"]=100*(
            baseline["standardized_MSE_equal_species_and_patch"]-
            val["standardized_MSE_equal_species_and_patch"]
        )/baseline["standardized_MSE_equal_species_and_patch"]
        val["n_patches_lower_standardized_loss_than_baseline"]=sum(
            val["heldout_patch_standardized_MSE"][str(p)] <
            baseline["heldout_patch_standardized_MSE"][str(p)]
            for p in range(1,15))
    assert abs(baseline["standardized_MSE_equal_species_and_patch"]-
               1.3677203147762984)<1e-9
    assert abs(scores["captured_visitors_same_plant_species"][
        "standardized_MSE_equal_species_and_patch"]-1.3910224974440426)<1e-9
    assert abs(scores["patch_visitor_taxon_richness"][
        "standardized_MSE_equal_species_and_patch"]-1.318764551974037)<1e-9
    def deletion_scores(frame:str)->dict:
        result={}
        for removed in sorted(SEED_SPECIES):
            remaining=sorted(SEED_SPECIES-{removed})
            metric="standardized_MSE_equal_species_and_patch" if frame=="standardized" else "raw_log_seed_MSE"
            for model,v in scores.items():
                result.setdefault(removed,{})[model]=sum(
                    v["heldout_species_standardized_MSE"][sp]
                    for sp in remaining
                )/len(remaining) if frame=="standardized" else None
        return result
    source_species_removal=deletion_scores("standardized")
    for removed,metrics in source_species_removal.items():
        metrics["richness_better_than_species_baseline"]=(
            metrics["patch_visitor_taxon_richness"]<metrics["species_mean_only"])
        metrics["same_species_captures_better_than_baseline"]=(
            metrics["captured_visitors_same_plant_species"]<metrics["species_mean_only"])
    patch_removal={}
    for excluded in range(1,15):
        values={}
        for name,item in scores.items():
            values[name]=sum(v for p,v in item["heldout_patch_standardized_MSE"].items()
                             if p!=str(excluded))/13
        patch_removal[str(excluded)]={
            "richness_better_than_baseline":values["patch_visitor_taxon_richness"]<
                                            values["species_mean_only"],
            "same_species_capture_better_than_baseline":values[
                "captured_visitors_same_plant_species"]<values["species_mean_only"],
            "richness_plus_total_better_than_richness_only":values[
                "patch_total_captures_plus_taxon_richness"]<
                values["patch_visitor_taxon_richness"],
        }
    response={
        "status":"EXPLORATORY_EXTERNAL_HELD_PATCH_SENTINEL_AUDIT",
        "provenance":source,
        "prediction_models":scores,
        "seed_species_deletion_diagnostic":source_species_removal,
        "number_of_species_deletions_with_richness_gain":sum(
            r["richness_better_than_species_baseline"] for r in source_species_removal.values()),
        "number_of_species_deletions_with_same_species_capture_gain":sum(
            r["same_species_captures_better_than_baseline"] for r in source_species_removal.values()),
        "heldout_patch_score_influence":patch_removal,
        "number_of_patch_deletions_with_richness_gain":sum(
            r["richness_better_than_baseline"] for r in patch_removal.values()),
        "species_descriptives":{
            s:{
                "n_patches":14,
                "mean_seeds_per_tagged_flower":sum(
                    r["mean_seeds_per_flower"] for r in rows if r["species"]==s)/14,
                "n_zero_capture_patches":sum(r["n_same_plant_visitors_captured"]==0
                                             for r in rows if r["species"]==s),
            }
            for s in sorted(SEED_SPECIES)
        },
        "limits":[
            "A captured insect is a detected flower visitor during six one-hour rounds, NOT a measured effective conspecific pollen transfer or standardized per-flower visitation rate.",
            "No captures for a patch/plant species is NOT biological zero pollination; all 19 such cells have positive seed set, and sampling covered only some hours and flowers.",
            "Seven species share the same 14 planted patches; 98 patch x species rows do NOT represent 98 independent spatial experiments.",
            "These patches are planted local-isolation replicates in ONE sheep farm, not fragmented-vs-continuous habitat control units. Do not add to frozen EGWEE direct-effect or interaction-function denominators.",
            "Seed endpoint is mean seeds per FIVE tagged flowers on each sampled plant; it is NOT whole-plant or whole-patch seed production, viable establishment or recruitment.",
            "Body-size dispersion/range and 1D FEve proxy are simple visit-capture descriptors; FEve proxy NOT independently verified against original R FD::dbFD metric or network complementarity.",
            "Predictors are measured during the same season; held-patch prediction is spatial transfer, NOT prospective time-series validation or a causal effect.",
            "After-source-inspection model and score selection is post hoc. Fourteen patches in one experimental landscape have no independent source-level external replication.",
            "Standardized and unstandardized seed-score rankings may differ; both are reported. No universal seed function prediction law or new ecological mechanism is inferred.",
            "Taxon label richness increases with sampled catches; conditioning on patch total capture number and rarefying to 54 captures are exploratory checks, not identified functional diversity effects.",
            "Leave-one-species and leave-one-held-patch deletion scores reweight heavily overlapping predictions and do not add independent study replicates.",
            "Original Peralta et al. 2023 already identified in-sample relationships between insect functional diversity and seed set; only the held-patch diagnostic estimand differs.",
        ],
    }
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(response,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("WEBBER_PATCH_SPECIES_SOURCE_CHECK: PASS")
    print(json.dumps({
        "source":source,
        "models":{k:{
            "standardized_MSE":round(v["standardized_MSE_equal_species_and_patch"],6),
            "raw_log_seed_MSE":round(v["raw_log_seed_MSE"],6),
            "percent_gain":round(v["percent_standardized_MSE_improvement_over_species_mean"],3),
            "patches_improved":v["n_patches_lower_standardized_loss_than_baseline"],
        } for k,v in scores.items()},
        "species":response["species_descriptives"],
        "deletion_diagnostics":{
            "richness_better_after_omitting_species":response[
                "number_of_species_deletions_with_richness_gain"],
            "same_species_visits_better_after_omitting_species":response[
                "number_of_species_deletions_with_same_species_capture_gain"],
            "richness_better_after_omitting_one_held_patch":response[
                "number_of_patch_deletions_with_richness_gain"],
        },
    },indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
