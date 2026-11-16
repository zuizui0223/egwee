#!/usr/bin/env python3
"""Identifier-only join audit for natural and translocated Campanula glomerata.

Source-level gate: only independently documented population, individual,
generation, source, and maternal keys are read; no molecular alleles,
HL numeric values, seed viability, flowering, survival or effects are read.
An exact text match is not proof of a cross-study biological sample identity.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import argparse
import hashlib
import json
from pathlib import Path

from audit_dianthus_genome_fitness_ids import source_file, read_whitelisted
from audit_zenodo_genetic_fitness_schema import workbook_sheets

FILES = {
    "natural_fitness": (5676272, "Campanula_fitness.xlsx",
                        "a1c50c74d0bd2c9a00b7a0d42322c31c30c53789e3b5cadbe67b08cee878f6a7"),
    "natural_genomic": (5676286, "Campanula_genotype.xlsx",
                        "6fa7f4289236d4deab2151f5a76a2a555ee3513f959821adb5aa8ce5a748df21"),
    "translocated_genomic": (7954368, "Cam_monitoring_microsat.xlsx",
                             "df204199595f7860b711b52ca49633f3a2339b0d37fa9ab8ae05866df8883636"),
    "translocated_fitness": (8217417, "CAM_fitness_data.xlsx",
                             "8bd38bb15f3fb1734b752d0eedb2a071e8340ee45596cf8e8efd98b871db47bf"),
}
IDENTIFIER_FIELDS = {
    "natural_fitness": {"POP", "Ind"},
    "natural_genomic": {"Pop", "Ind", "Generation"},
    "translocated_genomic": {"Site", "Generation", "Source", "Ind nb"},
    "translocated_maternal": {"Site", "sourcEMO pop", "maternal code"},
    "translocated_F1": {"Site", "source pop", "maternal code"},
}

def key_counter(rows, keys):
    result = Counter()
    for row in rows:
        key=tuple(row.get(k, "") for k in keys)
        if all(key):
            result[key]+=1
    return result

def compare(a,b):
    both=set(a)&set(b)
    return {
        "left_distinct_complete_keys":len(a),
        "right_distinct_complete_keys":len(b),
        "matched_literal_keys":len(both),
        "matched_right_records":sum(b[k] for k in both),
        "matched_left_records":sum(a[k] for k in both),
        "right_duplicate_key_matches":sum(b[k]>1 for k in both),
        "left_duplicate_key_matches":sum(a[k]>1 for k in both),
        "max_right_records_per_matched_key":max((b[k] for k in both),default=0),
        "identical_labels_do_not_prove_biological_identity":True,
    }

def normalize(row, mappings):
    return {out:row.get(raw, "") for out,raw in mappings.items()}

def count_labels(rows,column):
    return dict(sorted(Counter(row.get(column, "") for row in rows if row.get(column, "")).items()))

def audit():
    source={}
    for name,(dataset,file,expected) in FILES.items():
        buf=source_file(dataset,file)
        digest=hashlib.sha256(buf).hexdigest()
        if digest!=expected:
            raise ValueError("Immutable publication source digest changed: "+name)
        source[name]=buf

    nat_f=read_whitelisted(source["natural_fitness"],"xl/worksheets/sheet1.xml",
                           IDENTIFIER_FIELDS["natural_fitness"])
    nat_g=read_whitelisted(source["natural_genomic"],"xl/worksheets/sheet1.xml",
                           IDENTIFIER_FIELDS["natural_genomic"])
    tr_g=read_whitelisted(source["translocated_genomic"],"xl/worksheets/sheet1.xml",
                          IDENTIFIER_FIELDS["translocated_genomic"])
    tr_f0=read_whitelisted(source["translocated_fitness"],"xl/worksheets/sheet1.xml",
                           IDENTIFIER_FIELDS["translocated_maternal"])
    tr_f1=read_whitelisted(source["translocated_fitness"],"xl/worksheets/sheet2.xml",
                           IDENTIFIER_FIELDS["translocated_F1"])
    # The original spreadsheet count includes rows with absent or missing-ID
    # cells; read_whitelisted intentionally omits those. Keep BOTH denominators
    # and never treat ID-complete rows as all biological observations.
    raw_counts = {
        "natural_fitness_rows":workbook_sheets(source["natural_fitness"])[0]["xml_nonempty_rows"]-1,
        "natural_genomic_rows":workbook_sheets(source["natural_genomic"])[0]["xml_nonempty_rows"]-1,
        "translocated_genomic_rows":workbook_sheets(source["translocated_genomic"])[0]["xml_nonempty_rows"]-1,
        "translocated_fitness_maternal_rows":workbook_sheets(source["translocated_fitness"])[0]["xml_nonempty_rows"]-1,
        "translocated_fitness_F1_rows":workbook_sheets(source["translocated_fitness"])[1]["xml_nonempty_rows"]-1
    }
    expected = {
        "natural_fitness_rows":507, "natural_genomic_rows":680,
        "translocated_genomic_rows":716,
        "translocated_fitness_maternal_rows":188,
        "translocated_fitness_F1_rows":990
    }
    if raw_counts != expected:
        raise ValueError("Original source XML denominator drifted: "+repr(raw_counts))
    identifier_row_counts = {
        "natural_fitness_rows":len(nat_f), "natural_genomic_rows":len(nat_g),
        "translocated_genomic_rows":len(tr_g),
        "translocated_fitness_maternal_rows":len(tr_f0),
        "translocated_fitness_F1_rows":len(tr_f1)
    }
    if any(identifier_row_counts[k]>raw_counts[k] for k in expected):
        raise ValueError("Identifier parser generated more records than source XLSX")

    nf=[normalize(row,{"population":"POP","individual":"Ind"}) for row in nat_f]
    ng=[normalize(row,{"population":"Pop","individual":"Ind","generation":"Generation"}) for row in nat_g]
    tg=[normalize(row,{"site":"Site","source":"Source","individual":"Ind nb",
                       "generation":"Generation"}) for row in tr_g]
    tf0=[normalize(row,{"site":"Site","source":"sourcEMO pop",
                        "maternal":"maternal code"}) for row in tr_f0]
    tf1=[normalize(row,{"site":"Site","source":"source pop",
                        "maternal":"maternal code"}) for row in tr_f1]

    nat_g_by_generation={}
    for g in sorted(set(r["generation"] for r in ng)):
        subset=[r for r in ng if r["generation"]==g]
        nat_g_by_generation[g]={
            "source_rows":len(subset),
            "individual_only":compare(key_counter(subset,["individual"]),key_counter(nf,["individual"])),
            "population_individual":compare(key_counter(subset,["population","individual"]),
                                            key_counter(nf,["population","individual"])),
        }

    tf0_norm=[{"site":r["site"],"source":r["source"],"individual":r["maternal"]} for r in tf0]
    tf1_norm=[{"site":r["site"],"source":r["source"],"individual":r["maternal"]} for r in tf1]
    trans_by_gen={}
    for g in sorted(set(r["generation"] for r in tg)):
        subset=[r for r in tg if r["generation"]==g]
        trans_by_gen[g]={
            "genotype_records":len(subset),
            "fitness_maternal_sample_only":compare(key_counter(subset,["individual"]),
                                                   key_counter(tf0_norm,["individual"])),
            "fitness_maternal_site_id":compare(key_counter(subset,["site","individual"]),
                                             key_counter(tf0_norm,["site","individual"])),
            "fitness_maternal_site_source_id":compare(key_counter(subset,["site","source","individual"]),
                                                    key_counter(tf0_norm,["site","source","individual"])),
            "fitness_F1_mother_site_id":compare(key_counter(subset,["site","individual"]),
                                             key_counter(tf1_norm,["site","individual"])),
        }

    combined = {
       "status":"CAMPANULA_NATURAL_AND_TRANSLOCATED_IDENTIFIERS_ONLY",
       "source_dois":{k:"10.5281/zenodo."+str(v[0]) for k,v in FILES.items()},
       "source_sha256":{k:v[2] for k,v in FILES.items()},
       "source_counts":raw_counts,
       "identifier_rows_with_at_least_one_whitelisted_cell":identifier_row_counts,
       "source_rows_without_any_whitelisted_identifier":{k:raw_counts[k]-identifier_row_counts[k] for k in expected},
       "natural_genotype_generation_counts":count_labels(ng,"generation"),
       "translocated_genotype_generation_counts":count_labels(tg,"generation"),
       "translocated_genotype_missing_generation_code_rows":sum(not row["generation"] for row in tg),
       "natural_all_genotypes_to_fitness":{
           "individual_only":compare(key_counter(ng,["individual"]),key_counter(nf,["individual"])),
           "population_individual":compare(key_counter(ng,["population","individual"]),
                                           key_counter(nf,["population","individual"]))
       },
       "natural_by_genotype_generation":nat_g_by_generation,
       "translocated_genotypes_to_maternal_fitness_by_generation":trans_by_gen,
       "translocated_fitness_internal_F0_to_F1_maternal_code":{
           "maternal_name_only":compare(key_counter(tf0,["maternal"]),key_counter(tf1,["maternal"])),
           "site_maternal":compare(key_counter(tf0,["site","maternal"]),
                                  key_counter(tf1,["site","maternal"])),
           "site_source_maternal":compare(key_counter(tf0,["site","source","maternal"]),
                                         key_counter(tf1,["site","source","maternal"]))
       },
       "raw_allele_values_read":False,
       "HL_numeric_values_read":False,
       "reproductive_or_fitness_values_read":False,
       "raw_third_party_tables_redistributed":False,
       "source_genetic_sample_is_not_automatically_a_maternal_or_F1_fitness_unit":True,
       "decision":"IDENTIFIER_JOIN_COUNTS_ONLY_CHECK_GENERATION_AND_BIOLOGICAL_COHORT_BEFORE_ANY_EFFECT",
    }
    return combined

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    data=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":data["status"],"counts":data["source_counts"],
                      "natural_generations":data["natural_genotype_generation_counts"],
                      "trans_generations":data["translocated_genotype_generation_counts"],
                      "natural_population_ID_overlap":
                         data["natural_all_genotypes_to_fitness"]["population_individual"]["matched_literal_keys"],
                      "trans_within_fitness":
                         data["translocated_fitness_internal_F0_to_F1_maternal_code"]["site_source_maternal"]["matched_literal_keys"]},
                      ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
