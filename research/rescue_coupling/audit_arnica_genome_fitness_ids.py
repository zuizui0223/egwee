#!/usr/bin/env python3
"""Outcome-blind Arnica 2020 source linkage gate.

Compare only identity/source/cohort columns from the independently archived
genotype and maternal/seed/juvenile fitness workbooks. Phenotype data and
allele calls are never parsed; all output contains *aggregate counts*, not
individual names/markers. A literal match is not a biological causal claim.
"""
from __future__ import annotations
import argparse
from collections import Counter
from pathlib import Path
import hashlib
import json

from audit_dianthus_genome_fitness_ids import read_whitelisted,clean
from audit_zenodo_genetic_fitness_schema import request,file_list

SOURCES={
    "genotypes": (3881466, "VanRossum_Raspe_Arnica_genetic.xlsx"),
    "fitness": (3881439, "VanRossumetal_Arnica_fitness.xlsx")
}
SHEETS={
    "genotypes":("xl/worksheets/sheet1.xml",{"Ind","Site","source","generation"}),
    "F0_seed":("xl/worksheets/sheet1.xml",{"Code","Site","source"}),
    "F1_rosette_1":("xl/worksheets/sheet2.xml",{"Site ","source","Mat plant code"}),
    "F1_rosette_2":("xl/worksheets/sheet3.xml",{"Site ","source","Mat plant code"}),
    "juvenile":("xl/worksheets/sheet4.xml",{"Site","Ind"}),
}

def source_raw(record_id:int,filename:str)->bytes:
    meta=json.loads(request(f"https://zenodo.org/api/records/{record_id}",2*1024*1024).decode("utf-8"))
    if (meta.get("doi") or "").lower()!=f"10.5281/zenodo.{record_id}":
        raise ValueError("Source DOI drift")
    entries=[r for r in file_list(meta) if r.get("name")==filename]
    if len(entries)!=1 or entries[0]["size"]>4*1024*1024:
        raise ValueError("Published original source missing or oversized")
    return request(entries[0]["download_url"],4*1024*1024)

def freq(rows:list[dict],cols:list[str])->Counter:
    items=[]
    for r in rows:
        k=tuple(r.get(x,"") for x in cols)
        if all(k):
            items.append(k)
    return Counter(items)

def compare(left:Counter,right:Counter)->dict:
    common=set(left)&set(right)
    return {
      "left_distinct_text_keys":len(left),
      "right_distinct_text_keys":len(right),
      "literal_join_candidate_keys":len(common),
      "matched_left_rows":sum(left[k] for k in common),
      "matched_right_rows":sum(right[k] for k in common),
      "matched_keys_repeated_in_left":sum(left[k]>1 for k in common),
      "matched_keys_repeated_in_right":sum(right[k]>1 for k in common),
      "largest_right_rows_per_matching_key":max((right[k] for k in common),default=0),
    }

def audit()->dict:
    geno=source_raw(*SOURCES["genotypes"])
    fitness=source_raw(*SOURCES["fitness"])
    data={}
    for label,(sheet,fields) in SHEETS.items():
        source=geno if label=="genotypes" else fitness
        data[label]=read_whitelisted(source,sheet,fields)
    # Compare the same named biological generation, not all genotyped plants:
    # juvenile-genome rows versus established-F1-juvenile fitness rows.
    juvenile_genomes=[r for r in data["genotypes"] if r.get("generation")=="juvenile"]
    juvenile_fitness=data["juvenile"]
    geno_by_ind={}
    repeated_genome_id=0
    for r in juvenile_genomes:
        ind=r.get("Ind","")
        if ind in geno_by_ind:repeated_genome_id+=1
        else:geno_by_ind[ind]=r.get("Site","")
    fitness_by_ind={}
    repeated_fitness_id=0
    for r in juvenile_fitness:
        ind=r.get("Ind","")
        if ind in fitness_by_ind:repeated_fitness_id+=1
        else:fitness_by_ind[ind]=r.get("Site","")
    common=set(geno_by_ind)&set(fitness_by_ind)
    site_pairs=Counter((geno_by_ind[i],fitness_by_ind[i]) for i in common)
    by_gen_site={}
    by_fitness_site={}
    for left,right in site_pairs:
        by_gen_site.setdefault(left,set()).add(right)
        by_fitness_site.setdefault(right,set()).add(left)
    site_mapping_unambiguous=(
        all(len(v)==1 for v in by_gen_site.values())
        and all(len(v)==1 for v in by_fitness_site.values())
    )
    # Independently test the clearly defined juvenile genetic cohort. Overlap
    # of bare individual labels is not the same as validated sample identity:
    # compare literal SITE codes and retain only aggregate public group counts.
    gen_juvenile=[r for r in data["genotypes"] if r["generation"]=="juvenile"]
    geno_juvenile_id={r["Ind"]:r for r in gen_juvenile if r["Ind"]}
    fitness_juvenile_id={r["Ind"]:r for r in data["juvenile"] if r["Ind"]}
    shared_ids=set(geno_juvenile_id)&set(fitness_juvenile_id)
    site_pairs=Counter(
        (geno_juvenile_id[k]["Site"],fitness_juvenile_id[k]["Site"])
        for k in shared_ids
    )
    site_map_gen={}
    site_map_fit={}
    for (g,f),n in site_pairs.items():
        site_map_gen.setdefault(g,set()).add(f)
        site_map_fit.setdefault(f,set()).add(g)
    cohort_bridge={
        "genomic_juvenile_source_rows":len(gen_juvenile),
        "genomic_juvenile_unique_individual_labels":len(geno_juvenile_id),
        "fitness_juvenile_source_rows":len(data["juvenile"]),
        "fitness_juvenile_unique_individual_labels":len(fitness_juvenile_id),
        "juvenile_generation_exact_ID_overlap":len(shared_ids),
        "matched_IDs_appearing_in_nonjuvenile_genomic_cohorts":sum(
           1 for r in data["genotypes"] if r["generation"]!="juvenile" and r["Ind"] in shared_ids),
        "matched_IDs_with_same_raw_site_code":sum(
            n for (g,f),n in site_pairs.items() if g==f),
        "matched_IDs_with_different_raw_site_codes":sum(
            n for (g,f),n in site_pairs.items() if g!=f),
        "genomic_site_names_in_overlap":len(site_map_gen),
        "fitness_site_names_in_overlap":len(site_map_fit),
        "site_label_pairing_count":len(site_pairs),
        "site_labels_1_to_1_among_matched_IDs":
             all(len(v)==1 for v in site_map_gen.values()) and
             all(len(v)==1 for v in site_map_fit.values()),
        "site_label_contingency_public_groups":[
            {"genomic_site_code":g,"fitness_site_code":f,"matched_ID_count":n}
            for (g,f),n in sorted(site_pairs.items())
        ],
        "sample_identifiers_exposed":False,
        "cross_source_site_code_semantics_verified":False,
        "no_allele_or_fitness_values_examined":True
    }
    d={
        "status":"ARNICA_2020_ID_ONLY_JOINS_NO_EFFECT_VALUES",
        "paper_doi":"10.1111/mec.15550",
        "genetic_source_doi":"10.5281/zenodo.3881466",
        "fitness_source_doi":"10.5281/zenodo.3881439",
        "genetic_sha256":hashlib.sha256(geno).hexdigest(),
        "fitness_sha256":hashlib.sha256(fitness).hexdigest(),
        "original_rows":{k:len(v) for k,v in data.items()},
        "genotype_generation_labels":dict(sorted(Counter(r["generation"] for r in data["genotypes"] if r["generation"]).items())),
        "genotype_site_distinct":len({r["Site"] for r in data["genotypes"] if r["Site"]}),
        "fitness_F0_site_distinct":len({r["Site"] for r in data["F0_seed"] if r["Site"]}),
        "genotype_vs_F0_seed":{
            "ID_only":compare(freq(data["genotypes"],["Ind"]),freq(data["F0_seed"],["Code"])),
            "Site_ID":compare(freq(data["genotypes"],["Site","Ind"]),freq(data["F0_seed"],["Site","Code"])),
            "Site_source_ID":compare(freq(data["genotypes"],["Site","source","Ind"]),freq(data["F0_seed"],["Site","source","Code"]))
        },
        "F0_seed_vs_F1_rosettes":{
            label:{
                "ID_only":compare(freq(data["F0_seed"],["Code"]),freq(data[label],["Mat plant code"])),
                "Site_ID":compare(freq(data["F0_seed"],["Site","Code"]),freq(data[label],["Site ","Mat plant code"])),
                "Site_source_ID":compare(freq(data["F0_seed"],["Site","source","Code"]),freq(data[label],["Site ","source","Mat plant code"]))
            } for label in ("F1_rosette_1","F1_rosette_2")
        },
        "genotype_vs_F1_juvenile":{
            "ID_only":compare(freq(data["genotypes"],["Ind"]),freq(data["juvenile"],["Ind"])),
            "Site_ID":compare(freq(data["genotypes"],["Site","Ind"]),freq(data["juvenile"],["Site","Ind"]))
        },
        "same_generation_F1_juvenile_identifier_link":{
            "genetic_rows_labeled_juvenile":len(juvenile_genomes),
            "fitness_juvenile_rows":len(juvenile_fitness),
            "unique_genetic_juvenile_IDs":len(geno_by_ind),
            "unique_fitness_juvenile_IDs":len(fitness_by_ind),
            "genetic_ID_duplicates":repeated_genome_id,
            "fitness_ID_duplicates":repeated_fitness_id,
            "exact_individual_ID_overlap":len(common),
            "matched_identifiers_with_exact_site_text":sum(geno_by_ind[k]==fitness_by_ind[k] for k in common),
            "distinct_site_pair_links":len(site_pairs),
            "anonymised_site_pair_counts":sorted(site_pairs.values(),reverse=True),
            "candidate_mapping_one_to_one_between_site_labels":site_mapping_unambiguous,
            "site_label_match_is_NOT_original_author_crosswalk":True,
            "biological_join_status":"CANDIDATE_COHORT_MATCH_NEEDS_ORIGINAL_SITE_CODEBOOK",
        },
        "genomic_F1_juvenile_cohort_ID_mapping":cohort_bridge,
        "F0_seed_has_maternal_HL_column":True,
        "F0_seed_has_viable_seed_germination_columns":True,
        "genome_allele_values_read":False,
        "HL_numeric_values_read":False,
        "seed_fitness_values_read":False,
        "all_phenotypic_outcomes_read":False,
        "raw_files_redistributed":False,
        "source_code_mapping_unverified":True,
        "decision":"IDENTIFIER_CANDIDATE_ONLY_VERIFY_GENERATION_COORT_AND_SOURCE_CODE",
        "warning":"The fitness F0 mother and F1 maternal codes are lineage relations, not identical genotypes; no source outcome or allele value opened."
    }
    return d

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    j=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(j,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:j[k] for k in ("status","original_rows","genotype_generation_labels","genotype_vs_F0_seed","F0_seed_vs_F1_rosettes","decision")},indent=2))

if __name__=="__main__":
    main()
