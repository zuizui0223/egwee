#!/usr/bin/env python3
"""Blinded within-workbook F0 maternal + F1 offspring identifier linkage.

This asks whether the F0 flower sheet's molecular HL variable can be
associated with a seed-fitness table by an original shared maternal ID.
No HL numbers, seed counts, flowers, fitness, microsatellite alleles,
growth or outcome values are opened or redistributed.
"""
from __future__ import annotations
import argparse
import hashlib
from collections import Counter
import json
from pathlib import Path
from audit_dianthus_genome_fitness_ids import (
    source_file, read_whitelisted, SRC, SHEETS
)
from audit_zenodo_genetic_fitness_schema import workbook_sheets

FIELDS={
    "flower":{"Population","Source","Transplant code"},
    "seed":{"Population","Source","Transplant code"},
    "juvenile":{"Population","Source","Maternal transplant","Seedling code"},
}

def ckey(row, columns):
    vals=tuple(row.get(k,"") for k in columns)
    return vals if all(vals) else None

def join_audit(left, right, lcols, rcols):
    if len(lcols)!=len(rcols):raise ValueError("join keys must align")
    left_counts=Counter(k for r in left if (k:=ckey(r,lcols)) is not None)
    right_counts=Counter(k for r in right if (k:=ckey(r,rcols)) is not None)
    matched=set(left_counts)&set(right_counts)
    return {
        "left_valid_records":sum(left_counts.values()),
        "right_valid_records":sum(right_counts.values()),
        "left_distinct_valid_keys":len(left_counts),
        "right_distinct_valid_keys":len(right_counts),
        "matched_literal_keys":len(matched),
        "left_records_with_matching_right_key":sum(left_counts[k] for k in matched),
        "right_records_with_matching_left_key":sum(right_counts[k] for k in matched),
        "left_matched_keys_with_duplicate_left_rows":sum(left_counts[k]>1 for k in matched),
        "right_matched_keys_with_duplicate_right_rows":sum(right_counts[k]>1 for k in matched),
        "largest_matched_right_family_size":max((right_counts[k] for k in matched),default=0),
        "no_approximate_or_fuzzy_join":True,
    }

def audit():
    source=source_file(*SRC["fitness"])
    source_sha=hashlib.sha256(source).hexdigest()
    expected="07e37aa193dfdf974de229cf29f0255126dc3e75d32c0189002d8eb81e77b5b2"
    if source_sha != expected:
        raise ValueError("Source workbook digest changed")
    schemas=workbook_sheets(source)
    sheet_headers={record["sheet"]:set(record["first_row_header_fields"]) for record in schemas}
    for sname in SHEETS.values():
        if sname not in sheet_headers:
            raise ValueError("Original worksheet moved")
    if "HL" not in sheet_headers[SHEETS["transplant_flowering"]]:
        raise ValueError("F0 molecular index missing")
    if "HL" not in sheet_headers[SHEETS["F1_seedling_growth"]]:
        raise ValueError("F1 molecular index missing")
    if "HL" in sheet_headers[SHEETS["transplant_seed_fitness"]]:
        raise ValueError("F0 seed worksheet HL schema unexpectedly changed")
    flower=read_whitelisted(source,SHEETS["transplant_flowering"],FIELDS["flower"])
    seed=read_whitelisted(source,SHEETS["transplant_seed_fitness"],FIELDS["seed"])
    juvenile=read_whitelisted(source,SHEETS["F1_seedling_growth"],FIELDS["juvenile"])
    links={}
    for category,r, rightcode in [
        ("F0_mother_seed",seed,"Transplant code"),
        ("F1_seedling_mother",juvenile,"Maternal transplant")
    ]:
        for label,fields in [
            ("transplant_code_only",["Transplant code"]),
            ("population_plus_transplant",["Population","Transplant code"]),
            ("population_source_transplant",["Population","Source","Transplant code"])
        ]:
            rightfields=[rightcode if x=="Transplant code" else x for x in fields]
            links[category+"_"+label]=join_audit(flower,r,fields,rightfields)
    return {
      "status":"DIANTHUS_FITNESS_WORKBOOK_INTERNAL_IDS_NO_GENOTYPES_OR_OUTCOMES_OPENED",
      "fitness_source_doi":"10.5281/zenodo.4650488",
      "source_sha256":source_sha,
      "source_fitness_flowering_rows":len(flower),
      "source_fitness_seed_rows":len(seed),
      "source_fitness_F1_growth_rows":len(juvenile),
      "HL_column_exists_in_F0_flowering":True,
      "HL_column_exists_in_F1_seedling_growth":True,
      "HL_column_absent_from_F0_seed_sheet":True,
      "identifier_links":links,
      "outcome_values_read":False,
      "HL_values_read":False,
      "genotype_alleles_read":False,
      "third_party_source_redistributed":False,
      "semantic_warning":"Literal maternal codes alone do not establish measured F0 and F1 genomic identical units. F1 seedling genotype is not the maternal genotype. Verify population and source code meaning and maternal family grain with original codebook before any fit."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    result=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"source_rows":[result["source_fitness_flowering_rows"],result["source_fitness_seed_rows"],result["source_fitness_F1_growth_rows"]],
                      "links":{name:{"matches":v["matched_literal_keys"],"right_records":v["right_records_with_matching_left_key"]} for name,v in result["identifier_links"].items()},
                      "no_outcomes_read":not result["outcome_values_read"]},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
