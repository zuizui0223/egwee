#!/usr/bin/env python3
"""Audit primary Zenodo genotype/fitness file schemas WITHOUT inspecting values.

The Dianthus paper supplies separate published genotype and fitness data records.
The Arnica 2020 programme also provides independent original genotype and fitness records. This script
does not conflate those systems, perform ID joins, read locus genotypes, read
fitness outcomes or infer causal genomic rescue.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, re, urllib.request, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

RECORDS = [
  {"id":4650464,"role":"Dianthus_2021_individual_microsatellites","doi":"10.5281/zenodo.4650464","study":"Dianthus_deltoides_2021"},
  {"id":4650488,"role":"Dianthus_2021_F0_F1_fitness","doi":"10.5281/zenodo.4650488","study":"Dianthus_deltoides_2021"},
  {"id":3881439,"role":"Arnica_2020_F0_F1_fitness","doi":"10.5281/zenodo.3881439","study":"Arnica_montana_2020"},
  {"id":3881466,"role":"Arnica_2020_individual_microsatellites","doi":"10.5281/zenodo.3881466","study":"Arnica_montana_2020"}
]
MAX_METADATA=2*1024*1024
MAX_FILE=4*1024*1024
NS={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

def request(url:str,maxsize:int)->bytes:
    req=urllib.request.Request(url,headers={"User-Agent":"EGWEE-source-provenance/0.1","Accept":"application/json,*/*"})
    with urllib.request.urlopen(req,timeout=35) as resp:
        buf=resp.read(maxsize+1)
        if len(buf)>maxsize:raise ValueError("source exceeds maximum safe size")
        return buf

def workbook_sheets(binary:bytes)->list[dict]:
    with zipfile.ZipFile(io.BytesIO(binary)) as z:
        if z.testzip() is not None:raise ValueError("XLSX CRC invalid")
        shared=[]
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si",NS):
                shared.append("".join((n.text or "") for n in si.findall(".//m:t",NS)))
        out=[]
        sheet_names=sorted((name for name in z.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml",name)),
                           key=lambda x:int(re.search(r"sheet(\d+)",x).group(1)))
        for name in sheet_names[:25]:
            root=ET.fromstring(z.read(name))
            allrows=root.findall(".//m:sheetData/m:row",NS)
            header=[]
            if allrows:
                for cell in allrows[0].findall("m:c",NS):
                    value=cell.find("m:v",NS)
                    typ=cell.attrib.get("t")
                    if typ=="s" and value is not None:header.append(shared[int(value.text)])
                    elif typ=="inlineStr":header.append("".join((t.text or "") for t in cell.findall(".//m:t",NS)))
                    elif typ=="str" and value is not None:header.append(value.text or "")
                    else:header.append("<non-text-header>")
            out.append({"sheet":name,"xml_nonempty_rows":len(allrows),
                        "first_row_header_fields":header[:100],"header_count":len(header),
                        "phenotype_or_allele_values_read":False})
        return out

def inspect_file(name:str,binary:bytes)->dict:
    low=name.lower()
    if low.endswith(".xlsx"):
        if not zipfile.is_zipfile(io.BytesIO(binary)):raise ValueError("not a valid XLSX archive")
        return {"kind":"xlsx","sheets":workbook_sheets(binary)}
    if low.endswith(".csv") or low.endswith(".tsv"):
        line=binary.splitlines()[0].decode("utf-8-sig") if binary.splitlines() else ""
        header=next(csv.reader([line],delimiter="\t" if low.endswith(".tsv") else ","))
        return {"kind":"delimited","first_row_fields":header[:100],"column_count":len(header),
                "physical_lines":len(binary.splitlines()),"outcome_values_read":False}
    return {"kind":"not_parsed_unknown_format"}

def file_list(metadata:dict)->list[dict]:
    files=metadata.get("files",[])
    if isinstance(files,list):
        return [{"name":f.get("key") or f.get("filename"),
                 "size":f.get("size"),
                 "download_url":(f.get("links") or {}).get("self") or f.get("download"),
                 "checksum":f.get("checksum")}
                for f in files]
    if isinstance(files,dict):
        arr=[]
        for k,f in (files.get("entries") or {}).items():
            arr.append({"name":k,"size":f.get("size"),"download_url":(f.get("links") or {}).get("content"),"checksum":f.get("checksum")})
        return arr
    return []

def audit_one(source:dict)->dict:
    row={"id":source["id"],"study_programme":source["study"],"role":source["role"],
         "expected_doi":source["doi"],"outcome_values_read":False,"raw_data_redistributed":False}
    try:
        m=json.loads(request(f"https://zenodo.org/api/records/{source['id']}",MAX_METADATA).decode("utf-8"))
        got=str(m.get("doi") or (m.get("pids",{}).get("doi",{}).get("identifier")) or "")
        if got.casefold()!=source["doi"].casefold():
            raise ValueError("Source DOI differs from specified immutable record: "+got)
        row["metadata"]="verified"
        row["title"]=m.get("metadata",{}).get("title")
        row["published_on"]=m.get("metadata",{}).get("publication_date")
        files=file_list(m)
        row["files"]=[]
        for f in files:
            rec={"name":f["name"],"bytes_declared":f["size"],"source_checksum":f["checksum"]}
            if f["name"] and f["size"] is not None and int(f["size"])<=MAX_FILE and f["download_url"] and f["name"].lower().endswith((".xlsx",".csv",".tsv")):
                try:
                    raw=request(f["download_url"],MAX_FILE)
                    rec["bytes_downloaded"]=len(raw)
                    rec["sha256"]=hashlib.sha256(raw).hexdigest()
                    rec["schema"]=inspect_file(f["name"],raw)
                    rec["status"]="source_schema_verified"
                except Exception as e:
                    rec["status"]="file_access_stop"
                    rec["reason"]=str(e)[:200]
            else:
                rec["status"]="metadata_only_large_or_unsupported"
            row["files"].append(rec)
        row["decision"]="PUBLIC_SOURCE_SCHEMAS_ONLY_NO_GENETIC_FUNCTION_LINK_ESTIMATED"
    except Exception as e:
        row["metadata"]="access_stop"
        row["error"]=str(e)[:220]
        row["decision"]="ZENODO_SOURCE_ACCESS_STOP"
    return row

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    recs=[audit_one(s) for s in RECORDS]
    result={"status":"PUBLIC_ZENODO_SCHEMA_ONLY_NO_OUTCOME_VALUES","source_record_count":len(recs),
            "independent_study_programmes":len({x["study"] for x in RECORDS}),
            "records":recs,"raw_data_redistributed":False,"alleles_read":False,"fitness_effects_computed":False}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"records":[{"id":r["id"],"status":r["metadata"],"files":len(r.get("files",[]))} for r in recs]},indent=2))
if __name__=="__main__":
    main()
