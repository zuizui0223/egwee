#!/usr/bin/env python3
"""Source-exact, outcome-blind discovery of three Campanula glomerata Zenodo datasets.

Two source archives (2021, natural populations) support the 2022 paper;
the 2023 translocated F1 archive is a DIFFERENT cohort and must not be merged
with natural 2021 seed fitness through guessed identifiers. Download only
bounded public source files, inspect text headers/row counts and hashes,
never genomic alleles, seed traits or signed effects.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from audit_zenodo_genetic_fitness_schema import request, file_list, inspect_file

SOURCES=[
 {"id":5676272,"role":"natural_7population_seed_progeny_fitness","study":"Campanula_glomerata_2022_natural_pops","publication_doi":"10.3389/fcosc.2022.829332"},
 {"id":5676286,"role":"natural_8population_adult_and_seed_progeny_15SSR","study":"Campanula_glomerata_2022_natural_pops","publication_doi":"10.3389/fcosc.2022.829332"},
 {"id":7954368,"role":"translocated_2population_F1_15SSR","study":"Campanula_glomerata_2023_translocated_F1","publication_doi":"10.1016/j.gecco.2023.e02538"}
]
MAX=6*1024*1024

def main():
    arg=argparse.ArgumentParser()
    arg.add_argument("--output",type=Path,required=True)
    args=arg.parse_args()
    result=[]
    for row in SOURCES:
        x={"zenodo_id":row["id"],"expected_doi":f"10.5281/zenodo.{row['id']}",
           "role":row["role"],"study_programme":row["study"],
           "publication_doi_to_confirm":row["publication_doi"],
           "allele_or_fitness_values_read":False,"source_raw_data_redistributed":False,
           "no_interstudy_sample_crosswalk_assumed":True}
        try:
            meta=json.loads(request(f"https://zenodo.org/api/records/{row['id']}",2*1024*1024).decode("utf-8"))
            if str(meta.get("doi","")).casefold()!=x["expected_doi"]:
                raise ValueError("Public source DOI/version mismatch")
            x["metadata_status"]="verified"
            x["title"]=meta.get("metadata",{}).get("title")
            x["files"]=[]
            for f in file_list(meta):
                item={"name":f.get("name"),"source_bytes":f.get("size"),
                      "source_checksum":f.get("checksum")}
                fn=(f.get("name") or "").lower()
                if fn.endswith((".csv",".tsv",".xlsx")) and 0<(f.get("size") or 0)<=MAX and f.get("download_url"):
                    try:
                        binary=request(f["download_url"],MAX)
                        item["source_sha256"]=hashlib.sha256(binary).hexdigest()
                        item["public_raw_bytes_downloaded"]=len(binary)
                        item["schema"]=inspect_file(f["name"],binary)
                        item["schema_status"]="verified_no_outcomes"
                    except Exception as e:
                        item["schema_status"]="source_access_stop"
                        item["reason"]=str(e)[:240]
                else:
                    item["schema_status"]="metadata_only_other_format_or_size"
                x["files"].append(item)
            x["decision"]="SOURCE_METADATA_VERIFIED_INDIVIDUAL_ID_LINKAGE_NOT_YET_TESTED"
        except Exception as e:
            x["metadata_status"]="source_access_stop"
            x["reason"]=str(e)[:240]
            x["decision"]="SOURCE_ACCESS_STOP_NO_INFERENCE"
        result.append(x)
    output={
       "status":"CAMPANULA_2022_2023_SCHEMA_ONLY_NO_GENETIC_FUNCTION_INFERENCE",
       "source_dataset_records":len(SOURCES),
       "distinct_programme/cohort_labels":len(set(r["study"] for r in SOURCES)),
       "same_programme_data_pairs_do_not_create_independent_studies":True,
       "future_function_outcomes_read":False,
       "genotypes_read":False,
       "results":result
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":output["status"],"sources":[{
        "id":r["zenodo_id"],"metadata":r["metadata_status"],
        "files":len(r.get("files",[])),"verified_schemas":sum(f.get("schema_status")=="verified_no_outcomes" for f in r.get("files",[]))
    } for r in result]},indent=2))
if __name__=="__main__":
    main()
