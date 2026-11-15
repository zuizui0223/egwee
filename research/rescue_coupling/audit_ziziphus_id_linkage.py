#!/usr/bin/env python3
"""Cross-file IDENTIFIER feasibility for public Pseudoziziphus Figshare files.

Never read survival status, survival durations, microsatellite allele cells,
effect values or directions. The genotype workbook has a first row with unlabeled
leading columns, so a raw string match is only a possible crosswalk, not a verified ID.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re, urllib.request, zipfile
from io import BytesIO, StringIO
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

ARTICLE = 30290722
API = f"https://api.figshare.com/v2/articles/{ARTICLE}"
FILE_GENOTYPES = "Zc_parentgenotypedata.xlsx"
FILE_SURVIVAL = "ziziphus.survival.txt"
MAX = 2_000_000
NS = {"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent":"EGWEE-Pseudoziziphus-ID-scan/0.1", "Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=35) as r:
        content=r.read(MAX+1)
        if len(content)>MAX: raise ValueError("File exceeds ID audit size limit")
        return content

def clean(v: str|None) -> str:
    return (v or "").strip().casefold()

def genotype_first_four_columns(raw: bytes):
    with zipfile.ZipFile(BytesIO(raw)) as z:
        assert z.testzip() is None
        strs=[]
        if "xl/sharedStrings.xml" in z.namelist():
            root=ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si",NS):
                strs.append("".join(t.text or "" for t in si.findall(".//m:t",NS)))
        root=ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        rows=root.findall(".//m:sheetData/m:row",NS)
        result=[]
        for row in rows:
            d={}
            for c in row.findall("m:c",NS):
                m=re.match(r"([A-Z]+)\d+",c.attrib.get("r",""))
                if not m: continue
                col=0
                for ch in m.group(1):col=col*26+ord(ch)-ord("A")+1
                col-=1
                if col>3: continue # genomic calls start in columns beyond first four
                v=c.find("m:v",NS)
                if c.attrib.get("t")=="s" and v is not None:
                    val=strs[int(v.text)]
                elif c.attrib.get("t")=="inlineStr":
                    val="".join(t.text or "" for t in c.findall(".//m:t",NS))
                else:
                    val=v.text if v is not None else ""
                d[col]=val
            result.append(d)
        return result

def audit():
    metadata=json.loads(get(API).decode("utf-8"))
    article_doi=metadata.get("doi","").lower().removeprefix("https://doi.org/")
    if not article_doi.startswith("10.6084/m9.figshare.30290722"):
        raise ValueError("DOI/version mismatch")
    files={f["name"]:f for f in metadata.get("files",[])}
    if FILE_GENOTYPES not in files or FILE_SURVIVAL not in files:
        raise ValueError("Required original files missing")
    raw_gen=get(files[FILE_GENOTYPES]["download_url"])
    raw_surv=get(files[FILE_SURVIVAL]["download_url"])
    text=raw_surv.decode("utf-8-sig")
    reader=csv.DictReader(StringIO(text),delimiter="\t")  # published .txt is TSV, not CSV
    needed=["plant_id","genotype","Rgenotype","intro_yr","intro_type","popcode"]
    if not set(needed)<=set(reader.fieldnames or []):
        raise ValueError(f"Required identifier fields absent: {set(needed)-set(reader.fieldnames or [])}")
    # Whitelist-only: do not dereference survival or any response variable.
    ids=[{k:row[k] for k in needed} for row in reader]
    # Plant IDs are LOCAL identifiers in a restoration programme with multiple
    # population codes. Neither plant_id alone nor each longitudinal row is
    # admissibly an independent individual.
    plants=Counter(clean(r["plant_id"]) for r in ids if clean(r["plant_id"]))
    counts={k:len({clean(r[k]) for r in ids if clean(r[k])}) for k in needed}
    composite=[
        (clean(r["popcode"]),clean(r["plant_id"]))
        for r in ids if clean(r["popcode"]) and clean(r["plant_id"])
    ]
    composite_counts=Counter(composite)
    genotype_by_composite=defaultdict(set)
    for r in ids:
        if clean(r["popcode"]) and clean(r["plant_id"]) and clean(r["genotype"]):
            genotype_by_composite[(clean(r["popcode"]),clean(r["plant_id"]))].add(clean(r["genotype"]))
    candidate=genotype_first_four_columns(raw_gen)
    candidate_sets={
       f"unlabeled_column_{i+1}":{clean(row.get(i)) for row in candidate if clean(row.get(i))}
       for i in range(4)
    }
    surv_group_sets={
       k:{clean(r[k]) for r in ids if clean(r[k])}
       for k in ("genotype","Rgenotype","plant_id")
    }
    possible_overlap={
       c:{k:len(v&s) for k,s in surv_group_sets.items()}
       for c,v in candidate_sets.items()
    }
    head=candidate[0] if candidate else {}
    first_labels={str(i+1):str(head.get(i,""))[:40] for i in range(4)}
    explicit_fields={"genotype","plant_id","clone","plant id","sample","sample id","individual"}
    named_column_verified=any(clean(val) in explicit_fields for val in first_labels.values())
    return {
      "status":"ZIZIPHUS_IDENTIFIER_AND_TREATMENT_SCHEMA_ONLY",
      "source_article_id":ARTICLE,
      "source_doi":article_doi,
      "genotype_source_sha256":hashlib.sha256(raw_gen).hexdigest(),
      "survival_source_sha256":hashlib.sha256(raw_surv).hexdigest(),
      "survival_long_records":len(ids),
      "plant_id_label_nonempty_rows":sum(plants.values()),
      "plant_id_label_missing_rows":len(ids)-sum(plants.values()),
      "unique_plant_id_labels_NOT_individuals":len(plants),
      "popcode_plant_id_composite_nonempty_rows":len(composite),
      "popcode_plant_id_composite_missing_rows":len(ids)-len(composite),
      "unique_popcode_plant_id_composite_keys":len(composite_counts),
      "composite_keys_with_repeated_records":sum(n>1 for n in composite_counts.values()),
      "max_rows_per_composite_key":max(composite_counts.values()) if composite_counts else 0,
      "survival_file_identifier_cardinality":counts,
      "composite_keys_with_multiple_genotype_labels":sum(len(v)>1 for v in genotype_by_composite.values()),
      "composite_key_is_a_candidate_not_yet_a_verified_independent_unit":True,
      "genotype_source_xml_rows":len(candidate),
      "genotype_source_first_four_header_labels":first_labels,
      "source_first_four_columns_explicitly_identified_as_sample_ID":named_column_verified,
      "potential_label_overlap_UNVALIDATED":possible_overlap,
      "biological_outcome_fields_read":False,
      "genotype_allele_fields_read":False,
      "outcome_values_read":False,
      "raw_data_redistributed":False,
      "decision":"VERIFY_RAW_ID_CROSSWALK_FROM_SOURCE_DICTIONARY" if not named_column_verified else "CHECK_SEMANTIC_ID_MAPPING_BEFORE_JOIN",
      "warning":"Neither 1,185 longitudinal records nor repeated local plant_id labels define independent individuals. Verify popcode × plant_id composite semantics before modeling. Raw text overlap with unlabeled genotype columns is not an admissible genomic-survival join or effect-size calculation."
    }

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=Path,required=True)
    x=a.parse_args()
    result=audit()
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({key:result[key] for key in (
      "status","survival_long_records","plant_id_label_nonempty_rows",
      "unique_plant_id_labels_NOT_individuals","unique_popcode_plant_id_composite_keys",
      "composite_keys_with_repeated_records","genotype_source_xml_rows","decision")},indent=2))
