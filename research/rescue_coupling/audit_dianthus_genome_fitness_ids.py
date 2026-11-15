#!/usr/bin/env python3
"""ID-only join audit of original Dianthus translocation genotype and fitness files.

Reads only four explicit genetic identifiers (population, generation, source,
individual code) and plant/mother/seedling IDs from three fitness sheets.
Microsatellite allele columns, seed fitness, flower counts, growth, effects and
fitness outcomes are not read. No raw third-party workbooks are redistributed.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import argparse
import csv
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
from xml.etree import ElementTree as ET
import zipfile

from audit_zenodo_genetic_fitness_schema import request, file_list

NS={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
SRC={
    "genotype":(4650464,"VanRossum_Raspe_Dianthus_molecular.xlsx"),
    "fitness":(4650488,"VanRossumetal_Dianthus_fitness.xlsx")
}
HEADERS={
 "genotype":{"Population","Generation","Source","Ind. code"},
 "transplant_flowering":{"Population","Source","Transplant code"},
 "transplant_seed_fitness":{"Population","Source","Transplant code"},
 "F1_seedling_growth":{"Population","Source","Maternal transplant","Seedling code"}
}
SHEETS={
 "genotype":"xl/worksheets/sheet1.xml",
 "transplant_flowering":"xl/worksheets/sheet1.xml",
 "transplant_seed_fitness":"xl/worksheets/sheet2.xml",
 "F1_seedling_growth":"xl/worksheets/sheet3.xml"
}

def clean(t: str|None)->str:
    return (t or "").strip().casefold()

def read_whitelisted(source:bytes, sheet:str, fields:set[str]) -> list[dict]:
    """Never dereference any cell outside the explicitly verified ID columns."""
    with zipfile.ZipFile(BytesIO(source)) as z:
        if z.testzip() is not None: raise ValueError("XLSX CRC integrity failure")
        shared=[]
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si",NS):
                shared.append("".join(t.text or "" for t in si.findall(".//m:t",NS)))
        xml=ET.fromstring(z.read(sheet))
        rows=xml.findall(".//m:sheetData/m:row",NS)
        def parse(row,allowed=None):
            out={}
            for cell in row.findall("m:c",NS):
                m=re.match(r"([A-Z]+)\d+",cell.attrib.get("r",""))
                if m is None: continue
                idx=0
                for ch in m.group(1):idx=idx*26+ord(ch)-ord("A")+1
                idx-=1
                if allowed is not None and idx not in allowed: continue
                val=cell.find("m:v",NS)
                typ=cell.attrib.get("t")
                if typ=="s" and val is not None:
                    text=shared[int(val.text)]
                elif typ=="inlineStr":
                    text="".join(t.text or "" for t in cell.findall(".//m:t",NS))
                else:
                    text=val.text if val is not None else ""
                out[idx]=text
            return out
        header=parse(rows[0])
        col_ids={idx:value for idx,value in header.items() if value in fields}
        if set(col_ids.values())!=fields:
            raise ValueError("Missing ID columns in "+sheet+": "+repr(fields-set(col_ids.values())))
        result=[]
        for row in rows[1:]:
            vals=parse(row,set(col_ids))
            if vals:
                result.append({name:clean(vals.get(idx,"")) for idx,name in col_ids.items()})
    return result

def source_file(record_id:int,filename:str)->bytes:
    data=json.loads(request(f"https://zenodo.org/api/records/{record_id}",2*1024*1024).decode("utf-8"))
    files=file_list(data)
    found=[f for f in files if f["name"]==filename]
    if len(found)!=1:raise ValueError("Published Zenodo source file not unique")
    f=found[0]
    if f["size"]>4*1024*1024:raise ValueError("Unexpected source size")
    return request(f["download_url"],4*1024*1024)

def audit()->dict:
    genome=source_file(*SRC["genotype"])
    fitness=source_file(*SRC["fitness"])
    gen=read_whitelisted(genome,SHEETS["genotype"],HEADERS["genotype"])
    flw=read_whitelisted(fitness,SHEETS["transplant_flowering"],HEADERS["transplant_flowering"])
    seed=read_whitelisted(fitness,SHEETS["transplant_seed_fitness"],HEADERS["transplant_seed_fitness"])
    juvenile=read_whitelisted(fitness,SHEETS["F1_seedling_growth"],HEADERS["F1_seedling_growth"])
    def values(data,key):return [r[key] for r in data if r.get(key)]
    def keys(data,cols):
        arr=[tuple(r.get(c,"") for c in cols) for r in data]
        return Counter(k for k in arr if all(k))
    g_id=keys(gen,["Ind. code"])
    f0_id=keys(flw,["Transplant code"])
    f0seed_id=keys(seed,["Transplant code"])
    j_id=keys(juvenile,["Seedling code"])
    g_pop=keys(gen,["Population","Ind. code"])
    f0_pop=keys(flw,["Population","Transplant code"])
    f0seed_pop=keys(seed,["Population","Transplant code"])
    j_pop=keys(juvenile,["Population","Seedling code"])
    g_full=keys(gen,["Population","Source","Ind. code"])
    f0_full=keys(flw,["Population","Source","Transplant code"])
    f0seed_full=keys(seed,["Population","Source","Transplant code"])
    j_full=keys(juvenile,["Population","Source","Seedling code"])
    # The Seedling code is a local child number. Maternal transplant must be
    # retained when testing identity grain; do not treat 1171 F1 rows as
    # independent individual IDs before this hierarchical check.
    j_family=keys(juvenile,["Population","Source","Maternal transplant"])
    j_mother_child=keys(juvenile,["Population","Source","Maternal transplant","Seedling code"])
    f0_no_source=keys(flw,["Population","Transplant code"])
    f0seed_no_source=keys(seed,["Population","Transplant code"])
    j_family_no_source=keys(juvenile,["Population","Maternal transplant"])
    def joined(genome_keys,fitness_keys):
        match=set(genome_keys)&set(fitness_keys)
        return {"genomic_unique_keys":len(genome_keys),
                "fitness_unique_keys":len(fitness_keys),
                "shared_literal_keys":len(match),
                "fitness_rows_matching_a_genomic_key":sum(fitness_keys[k] for k in match),
                "genotype_rows_matching_a_fitness_key":sum(genome_keys[k] for k in match),
                "matched_genomic_keys_with_duplicate_genotype_rows":sum(genome_keys[k]>1 for k in match),
                "matched_fitness_keys_with_repeated_outcome_rows":sum(fitness_keys[k]>1 for k in match)}
    schemes={
        "F0_flowering":(f0_id,f0_pop,f0_full),
        "F0_seed":(f0seed_id,f0seed_pop,f0seed_full),
        "F1_juvenile":(j_id,j_pop,j_full)
    }
    rows={}
    for label,(idkey,popkey,fullkey) in schemes.items():
        rows[label]={
            "literal_individual_code_only":joined(g_id,idkey),
            "literal_population_plus_code":joined(g_pop,popkey),
            "literal_population_source_code":joined(g_full,fullkey)
        }
    f1_mother_matches=set(j_family)&set(f0seed_full)
    f1_mother_matches_flower=set(j_family)&set(f0_full)
    joint_f0_mother_key_match=set(f0_full)&set(f0seed_full)
    cohort_linkage={
        "F0_flowering_to_F0_seed_mother_shared_keys":len(joint_f0_mother_key_match),
        "F0_seed_to_F1_maternal_shared_population_source_keys":len(f1_mother_matches),
        "F0_flowering_to_F1_maternal_shared_population_source_keys":len(f1_mother_matches_flower),
        "F0_seed_to_F1_maternal_shared_population_keys":len(set(f0seed_no_source)&set(j_family_no_source)),
        "F0_flowering_to_F1_maternal_shared_population_keys":len(set(f0_no_source)&set(j_family_no_source)),
        "F1_repeated_local_seedling_code_unique":len(j_id),
        "F1_unique_full_mother_child_text_keys":len(j_mother_child),
        "F1_rows_with_full_mother_child_key":sum(j_mother_child.values()),
        "F1_full_mother_child_duplicate_label_keys":sum(v>1 for v in j_mother_child.values()),
        "F1_max_rows_per_mother_child_label":max(j_mother_child.values()) if j_mother_child else 0,
        "F1_maternal_family_keys":len(j_family),
        "F1_maternal_keys_with_multiple_offspring":sum(v>1 for v in j_family.values()),
        "F1_rows_from_mothers_with_a_F0_seed_record":sum(j_family[k] for k in f1_mother_matches),
        "mother_child_is_provisional_text_key":True,
        "do_not_promote_to_independent_cohort_without_source_crosswalk":True
    }
    result={
      "status":"DIANTHUS_F0_F1_SOURCE_ID_LINKAGE_AUDIT_NO_PHENOTYPES_OPENED",
      "study_doi":"10.1111/mec.15930",
      "genotype_dataset_doi":"10.5281/zenodo.4650464",
      "fitness_dataset_doi":"10.5281/zenodo.4650488",
      "genotype_source_sha256":hashlib.sha256(genome).hexdigest(),
      "fitness_source_sha256":hashlib.sha256(fitness).hexdigest(),
      "genotype_record_rows":len(gen),
      "fitness_flowering_record_rows":len(flw),
      "fitness_seed_record_rows":len(seed),
      "fitness_F1_juvenile_record_rows":len(juvenile),
      "genotype_generation_codes_counts":dict(sorted(Counter(values(gen,"Generation")).items())),
      "genotype_population_code_distinct":len(set(values(gen,"Population"))),
      "genotype_source_code_distinct":len(set(values(gen,"Source"))),
      "genotype_individual_code_nonempty":len(values(gen,"Ind. code")),
      "genotype_individual_code_distinct":len(set(values(gen,"Ind. code"))),
      "comparisons":rows,
      "phenotype_cohort_identifier_linkage":cohort_linkage,
      "outcome_fields_read":False,
      "microsatellite_alleles_read":False,
      "raw_data_redistributed":False,
      "interpretation_gate":"EXACT_TEXT_MATCH_ONLY; biological cohort/parent-juvenile mapping and independence require source dictionary; repeated plants/families not independent"
    }
    return result

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=Path,required=True)
    x=a.parse_args()
    d=audit()
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in d.items() if k not in ("comparisons",)},ensure_ascii=False,indent=2))
    for k,v in d["comparisons"].items():
        print(k, "code-only",v["literal_individual_code_only"]["shared_literal_keys"],
              "population+code",v["literal_population_plus_code"]["shared_literal_keys"],
              "fullkey",v["literal_population_source_code"]["shared_literal_keys"])

if __name__=="__main__":
    main()
