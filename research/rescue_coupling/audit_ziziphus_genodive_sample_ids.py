#!/usr/bin/env python3
"""Source-pinned GenoDive sample-ID audit, without reading microsatellite allele values.

Parse the published population-genetic native text file, check declared number
of individuals and study populations, and compare sample-name labels with
published survival file whitelisted identifiers. Do not infer a biological join
from label overlap and do not inspect survival outcomes or marker allele calls.
"""
from __future__ import annotations
from collections import Counter
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import urllib.request

ARTICLE_ID=30290722
SOURCE_FILE_ID=58525312
SOURCE_FILENAME="Copy of Genodive All Populations.2025"
SURVIVAL_FILE="ziziphus.survival.txt"
FIGSHARE=f"https://api.figshare.com/v2/articles/{ARTICLE_ID}"
SIZE_LIMIT=400000

def fetch(url: str, limit: int=SIZE_LIMIT)->bytes:
    req=urllib.request.Request(url,headers={"User-Agent":"EGWEE-public-genodive-id-audit/0.1", "Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=40) as response:
        data=response.read(limit+1)
        if len(data)>limit:
            raise ValueError("source exceeded bounded size for identifier-only audit")
        return data

def norm(v: str|None)->str:
    return (v or "").strip().casefold()

def read_native_identifiers(data:bytes)->dict:
    try:
        text=data.decode("utf-8-sig")
        encoding="utf-8"
    except UnicodeDecodeError:
        text=data.decode("latin-1")
        encoding="latin-1"
    lines=text.splitlines()
    out={"encoding":encoding,"total_lines":len(lines),"parse_status":"not_classified"}
    if len(lines)<4:
        return out | {"parse_status":"TOO_FEW_LINES"}
    nums=re.split(r"[\t ,]+",lines[1].strip())
    if len(nums)<5 or not all(re.fullmatch(r"\d+",x) for x in nums[:5]):
        return out | {"parse_status":"NOT_STANDARD_GENODIVE_SECOND_LINE"}
    count,pops,loci,ploidy,digits=map(int,nums[:5])
    if not(0<count<200000 and 0<pops<500 and 0<loci<500 and 0<ploidy<=20 and 0<digits<9):
        return out | {"parse_status":"OUT_OF_RANGE_GENODIVE_HEADER"}
    if len(lines)<pops+3:
        return out | {"parse_status":"TRUNCATED_POPULATION_BLOCK"}
    tab=lambda x:next(csv.reader([x],delimiter="\t"))
    # The Genodive population-name block is metadata, not genotype calls.
    # Some population lines may also encode optional group names after tabs.
    population_names={norm(tab(line)[0]) for line in lines[2:2+pops] if norm(tab(line)[0])}
    header=tab(lines[2+pops])
    # Strict parser: 3 or 4 non-marker columns (pop / optional clone / individual)
    sample_idx=None
    for i,name in enumerate(header[:5]):
        if norm(name) in ("ind","individual","individuals","individual name","individuals name","sample","samples","sample id","name"):
            sample_idx=i
            break
    if sample_idx is None:
        return out | {
            "parse_status":"INDIVIDUAL_COLUMN_UNIDENTIFIED",
            "declared_individuals":count,"declared_populations":pops,
            "declared_loci":loci,"field_count":len(header),
            "safe_header_first_three":header[:3]
        }
    if sample_idx not in (1,2):
        return out | {"parse_status":"UNEXPECTED_SAMPLE_POSITION",
                      "declared_individuals":count,
                      "safe_header_first_three":header[:3]}
    first_marker_col=sample_idx+1
    record_lines=[x for x in lines[3+pops:] if x.strip()]
    records=[]
    for line in record_lines:
        cols=tab(line)
        if len(cols)<=sample_idx:
            return out | {"parse_status":"MALFORMED_SAMPLE_ROW",
                          "declared_individuals":count,"observed_rows_before_failure":len(records)}
        # Only retain pop and sample identifier positions; NEVER inspect loci columns.
        records.append((norm(cols[0]),norm(cols[sample_idx])))
    sample_names=[x[1] for x in records if x[1]]
    observed=Counter(sample_names)
    return out | {
        "parse_status":"GENODIVE_SAMPLE_NAMES_ONLY_VERIFIED",
        "declared_individuals":count,
        "declared_populations":pops,
        "declared_loci":loci,
        "declared_max_ploidy":ploidy,
        "allele_code_digit_count":digits,
        "sample_field_position":sample_idx,
        "genotype_fields_not_read":True,
        "observed_sample_records":len(records),
        "declared_observed_count_consistent":len(records)==count,
        "nonempty_sample_name_records":len(sample_names),
        "distinct_sample_name_labels":len(observed),
        "sample_names_reused":sum(n>1 for n in observed.values()),
        "_private_sample_names":set(observed),
        "_private_pop_sample_records":set(records),
        "_private_population_names":population_names,
        "distinct_named_populations":len(population_names)
    }

def audit()->dict:
    meta=json.loads(fetch(FIGSHARE).decode("utf-8"))
    doi=meta.get("doi","").lower().removeprefix("https://doi.org/")
    if not doi.startswith("10.6084/m9.figshare.30290722"):
        raise ValueError("wrong Figshare article DOI")
    index={f["name"]:f for f in meta.get("files",[])}
    if SOURCE_FILENAME not in index or SURVIVAL_FILE not in index:
        raise ValueError("published source files absent")
    gen=index[SOURCE_FILENAME]
    if gen.get("id")!=SOURCE_FILE_ID:
        raise ValueError("Published Genodive file ID drift")
    binary=fetch(gen["download_url"])
    survival=fetch(index[SURVIVAL_FILE]["download_url"])
    if gen.get("supplied_md5") and hashlib.md5(binary).hexdigest()!=gen["supplied_md5"]:
        raise ValueError("Published native file digest drift")
    parsed=read_native_identifiers(binary)
    sample_names=parsed.pop("_private_sample_names",set())
    pop_sample=parsed.pop("_private_pop_sample_records",set())
    popnames=parsed.pop("_private_population_names",set())
    result={
        "status":"PUBLISHED_GENODIVE_SOURCE_IDENTIFIER_AUDIT",
        "article_doi":doi,
        "source_name":SOURCE_FILENAME,
        "source_id":SOURCE_FILE_ID,
        "source_sha256":hashlib.sha256(binary).hexdigest(),
        "survival_sha256":hashlib.sha256(survival).hexdigest(),
        "outcome_values_read":False,
        "microsatellite_alleles_read":False,
        "source_raw_data_redistributed":False,
        **parsed,
    }
    if result["parse_status"]=="GENODIVE_SAMPLE_NAMES_ONLY_VERIFIED":
        reader=csv.DictReader(io.StringIO(survival.decode("utf-8-sig")),delimiter="\t")
        wanted={"popcode","plant_id","genotype","Rgenotype"}
        if not wanted.issubset(set(reader.fieldnames or [])):
            raise ValueError("source survival identifier schema changed")
        whitelist=[{k:norm(x[k]) for k in wanted} for x in reader]
        result["whitelisted_survival_record_count"]=len(whitelist)
        result["overlap_sample_to_survival_labels"]={
            k:len(sample_names & {row[k] for row in whitelist if row[k]})
            for k in ["plant_id","genotype","Rgenotype"]
        }
        result["overlap_pop_and_sample_to_popcode_plantid"] = len(
            pop_sample & {(row["popcode"],row["plant_id"]) for row in whitelist})
        result["exact_genodive_population_name_to_survival_popcode"] = len(
            popnames & {row["popcode"] for row in whitelist if row["popcode"]})
        result["genodive_population_names_not_exposed_in_artifact"]=True
        result["join_verdict"]="UNVERIFIED_SEMANTIC_CROSSWALK_REQUIRED"
    else:
        result["join_verdict"]="FORMAT_STOP_SOURCE_DESCRIPTION_REQUIRED"
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    result=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
