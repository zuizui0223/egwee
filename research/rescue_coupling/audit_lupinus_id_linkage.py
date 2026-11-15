#!/usr/bin/env python3
"""Outcome-blind ID-only join audit for published Lupinus Figshare phenotypes + VCF metadata.

Reads only identifier/treatment/group columns; does NOT inspect onset/seed outcomes,
genotype calls, association statistics, effect directions or fitness values.
"""
from __future__ import annotations
import argparse
from collections import Counter
from io import BytesIO
import hashlib
import json
from pathlib import Path
import re
import urllib.request
import zipfile
from xml.etree import ElementTree as ET

NS={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
LIMIT=10*1024*1024

def download(u: str)->bytes:
    req=urllib.request.Request(u,headers={"User-Agent":"EGWEE-Lupinus-ID-audit/0.1","Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=35) as r:
        b=r.read(LIMIT+1)
        if len(b)>LIMIT: raise ValueError("source file exceeds safe limit")
        return b

def data_to_sparse_rows(blob: bytes, sheet_name:str, allow_fields:set[str]) -> tuple[list[str], list[dict]]:
    with zipfile.ZipFile(BytesIO(blob)) as z:
        s=[]
        if "xl/sharedStrings.xml" in z.namelist():
            shared=ET.fromstring(z.read("xl/sharedStrings.xml"))
            for e in shared.findall("m:si",NS):
                s.append("".join(n.text or "" for n in e.findall(".//m:t",NS)))
        root=ET.fromstring(z.read(sheet_name))
        rows=root.findall(".//m:sheetData/m:row",NS)
        def cells(row, wanted: set[int]|None=None):
            out={}
            for cell in row.findall("m:c",NS):
                addr=cell.attrib.get("r","")
                match=re.match(r"([A-Z]+)\d+",addr)
                if not match:continue
                col=0
                for ch in match.group(1):col=col*26+ord(ch)-ord("A")+1
                col-=1
                if wanted is not None and col not in wanted:continue
                v=cell.find("m:v",NS)
                if cell.attrib.get("t")=="s" and v is not None:
                    value=s[int(v.text)]
                elif cell.attrib.get("t")=="inlineStr":
                    value="".join(n.text or "" for n in cell.findall(".//m:t",NS))
                else:
                    value=v.text if v is not None else ""
                out[col]=value
            return out
        head=cells(rows[0]);header={i:str(n).strip() for i,n in head.items()}
        selected={i:n for i,n in header.items() if n in allow_fields}
        if not selected:raise ValueError("No declared identifier fields in source worksheet")
        out=[{name:values.get(idx,"") for idx,name in selected.items()}
             for row in rows[1:] if (values:=cells(row,set(selected.keys())))]
        return [selected[i] for i in sorted(selected)],out

def clean_id(s):
    # Only case/whitespace normalization. No speculative ID mapping.
    return str(s).strip().casefold()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    article_id=28304024
    m=json.loads(download(f"https://api.figshare.com/v2/articles/{article_id}").decode("utf-8"))
    files={f["name"]:f for f in m.get("files",[])}
    names=("data_Lupinusangustifolius_geneflow.xlsx","Metadata_VCF_SNPs_geneflow_Lupinus.xlsx")
    for n in names:
        if n not in files: raise ValueError("Published source missing "+n)
    phy=download(files[names[0]]["download_url"])
    geno=download(files[names[1]]["download_url"])
    ph_header, ph=data_to_sparse_rows(phy,"xl/worksheets/sheet2.xml",{"id","genotype","population","line","sister","year"})
    gen_header, samples=data_to_sparse_rows(geno,"xl/worksheets/sheet11.xml",{"Sample(s)"})
    if "id" not in ph_header or "Sample(s)" not in gen_header:raise ValueError("Required source ID field absent")
    ph_ids=[clean_id(x.get("id","")) for x in ph if clean_id(x.get("id",""))]
    gen_ids=[clean_id(x.get("Sample(s)","")) for x in samples if clean_id(x.get("Sample(s)",""))]
    ph_unique=set(ph_ids);gen_unique=set(gen_ids)
    exact=ph_unique & gen_unique
    def counts(col):
        return dict(sorted(Counter(str(x.get(col,"")) for x in ph if x.get(col,"") not in (None,"")).items()))
    out={
        "status":"LUPINUS_ID_ONLY_NO_OUTCOME_VALUES",
        "source_doi":"10.6084/m9.figshare.28304024",
        "published_metadata_url":"https://api.figshare.com/v2/articles/28304024",
        "phenotype_file_sha256":hashlib.sha256(phy).hexdigest(),
        "vcf_metadata_file_sha256":hashlib.sha256(geno).hexdigest(),
        "observed_phenotype_xml_rows_excluding_header":len(ph),
        "phenotype_identifier_nonempty_rows":len(ph_ids),
        "phenotype_unique_identifiers":len(ph_unique),
        "repeated_phenotype_identifier_count":sum(n>1 for n in Counter(ph_ids).values()),
        "vcf_metadata_xml_rows_excluding_header":len(samples),
        "vcf_metadata_identifier_nonempty_rows":len(gen_ids),
        "vcf_metadata_unique_identifiers":len(gen_unique),
        "exact_case_whitespace_normalized_id_overlap":len(exact),
        "fraction_of_vcf_metadata_ids_matched_exactly":len(exact)/len(gen_unique) if gen_unique else None,
        "phenotype_group_fields_available":ph_header,
        "metadata_group_fields_available":gen_header,
        "phenotype_treatment_group_levels":{k:counts(k) for k in ["genotype","population","line","year"] if k in ph_header},
        "outcome_fields_present_in_same_phenotype_sheet":["number_of_seeds","seed_weight","flowering_onset","shoot_growth"],
        "outcome_values_read":False,
        "vcf_genotypes_read":False,
        "raw_files_redistributed":False,
        "no_speculative_matching_policy":True,
        "decision":"ID_LINKAGE_REQUIRES_SOURCE_CROSSWALK" if len(exact)==0 else "EXACT_ID_MATCHES_EXIST_CHECK_UNIT_AND_LAG_BEFORE_EFFECTS"
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:out[k] for k in ["status","observed_phenotype_xml_rows_excluding_header","phenotype_unique_identifiers","vcf_metadata_unique_identifiers","exact_case_whitespace_normalized_id_overlap","decision"]},indent=2))

if __name__=="__main__":
    main()
