#!/usr/bin/env python3
"""Public Shorea/Rubroshorea microsatellite genotype vs nursery-survival ID schema.

No genotype calls, survival outcomes, seedling growth/seed weight, or effect
directions are read or re-distributed. If Dryad direct-file access is unavailable,
record ACCESS_STOP and do not claim ID linkage.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,io,re,urllib.request
from pathlib import Path

DOI="10.5061/dryad.nzs7h451m"
FILES=[
  ("seedling_genotypes","ShoreaCurtisiiSeedlingGenotypeCERVUS.csv","https://datadryad.org/downloads/file_stream/3834861"),
  ("nursery_survival","ShoreaCurtisiiSeedlingSurvivalGrowthRecord.csv","https://datadryad.org/downloads/file_stream/3834863"),
]
MAX_FILE=300_000

def public_download(url):
    req=urllib.request.Request(url,headers={"User-Agent":"EGWEE-Shorea-source-schema/0.1","Accept":"text/csv,*/*"})
    with urllib.request.urlopen(req,timeout=25) as r:
        raw=r.read(MAX_FILE+1)
        if len(raw)>MAX_FILE: raise ValueError("File exceeds source cap")
        if r.headers.get("content-type","").lower().startswith("text/html"):
            raise ValueError("HTML response instead of published CSV")
        return raw

def load_csv(raw):
    try: s=raw.decode("utf-8-sig")
    except UnicodeError:
        s=raw.decode("latin-1")
    head=s.splitlines()[:10]
    delim="\t" if sum(x.count("\t") for x in head)>sum(x.count(",") for x in head) else ","
    rows=list(csv.reader(io.StringIO(s),delimiter=delim))
    if not rows:raise ValueError("Empty source")
    return rows,delim

def label(value):
    return re.sub(r"\s+","",str(value or "")).casefold()

def clean(value):
    t=label(value)
    return "" if t in {"","na","n/a","nan","null","unknown","none","-9"} else t

def audit():
    report={"date":"2026-11-15","status":"SHOREA_SOURCE_ID_ONLY_NO_OUTCOME_VALUES",
      "source_dataset_doi":DOI,"files":[],"survival_values_examined":False,
      "genotype_alleles_examined":False,"seed_weight_values_examined":False,
      "raw_datasets_redistributed":False,"effect_sizes_estimated":False}
    found={}
    for kind,name,url in FILES:
        row={"role":kind,"file":name,"published_direct_file_url":url}
        try:
            raw=public_download(url)
            rows,sep=load_csv(raw)
            row.update({"status":"source_bytes_verified","sha256":hashlib.sha256(raw).hexdigest(),
                "csv_delimiter":"tab" if sep=="\t" else "comma",
                "raw_table_rows_including_header":len(rows),
                "header_fields":rows[0][:40]})
            found[kind]=rows
        except Exception as e:
            row.update({"status":"ACCESS_STOP","error":str(e)[:180]})
        report["files"].append(row)
    if len(found)<2:
        report["linkage_decision"]="RAW_SOURCE_ACCESS_STOP_NO_ID_LINK_CLAIM"
        return report
    geno=found["seedling_genotypes"];surv=found["nursery_survival"]
    # Genotype source's first column is explicitly documented as tree/seedling
    # identity; the beginning block is adults and the later block is seedlings.
    # No microsatellite allele columns are read or compared.
    raw_gen_ids=[clean(row[0]) for row in geno[1:] if row]
    gen_candidates={a for a in raw_gen_ids if a}
    sur_header=surv[0]
    options=["seedlingid","seedling_id","seedling id"]
    found_id_cols=[i for i,name in enumerate(sur_header) if label(name) in {label(x) for x in options}]
    if len(found_id_cols)!=1:
        report["linkage_decision"]="SURVIVAL_ID_HEADER_UNRESOLVED"
        report["survival_id_header_candidates_count"]=len(found_id_cols)
        return report
    ix=found_id_cols[0]
    survival_ids=[clean(row[ix]) for row in surv[1:] if len(row)>ix]
    sset={a for a in survival_ids if a}
    gcounts={a:raw_gen_ids.count(a) for a in gen_candidates}
    report["genotype_first_column_nonempty_labels"]=sum(bool(a) for a in raw_gen_ids)
    report["genotype_first_column_unique_labels"]=len(gen_candidates)
    report["duplicate_genotype_row_ID_labels"]=sum(n>1 for n in gcounts.values())
    report["survival_rows_excluding_header"]=len(surv)-1
    report["survival_nonempty_seedling_ID_rows"]=sum(bool(a) for a in survival_ids)
    report["survival_unique_seedling_ID_labels"]=len(sset)
    report["survival_ids_with_repeated_records"]=sum(n>1 for n in (survival_ids.count(a) for a in sset))
    report["exact_normalized_ID_overlap"]=len(gen_candidates&sset)
    report["share_survival_IDs_matched_exactly"]=len(gen_candidates&sset)/len(sset) if sset else None
    report["identical_ID_strings_are_not_automatically_independent_mothers"]=True
    report["linkage_decision"]="CANDIDATE_ID_LINK_REQUIRES_ORIGINAL_ROW_SEMANTICS" if (gen_candidates&sset) else "NO_EXACT_ID_LINK_SOURCE_CROSSWALK_REQUIRED"
    return report

def main():
    p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);a=p.parse_args()
    report=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k in ("status","linkage_decision","exact_normalized_ID_overlap","survival_rows_excluding_header","survival_unique_seedling_ID_labels")},indent=2))

if __name__=="__main__":main()
