#!/usr/bin/env python3
"""Source-only independent-paternity biological-grain receipt, LVP001/RHP001.

This verifies official source metadata and source bytes when fetchable, parses
ONLY structural row counts and first row header labels, and never analyzes
genotype, offspring paternity, visit quantity, reproductive or phenotype data.

No source original rows/files/IDs published to GitHub artifacts.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
from io import BytesIO,StringIO
import json
from pathlib import Path,PurePosixPath
import re
from urllib.parse import quote,urljoin,urlparse
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
import zipfile

DRYAD="https://datadryad.org"
ZENODO="https://zenodo.org"
LVP_DOI="10.5061/dryad.tdz08kqdr"
RHP_DOI="10.5061/dryad.p24q3"
RHP_RECORD=4942351
LVP_FILES=("Leventhal_et_al_2026.zip","README.md")
RHP_FILES=("amPollinators.csv","genotypes.xlsx","multiplePaternity.csv","obs.csv",
           "overallPollinators.csv","pmPollinators.csv","pollenDispersal.csv",
           "pollinatorBouts.csv","Rhodes et al. 2017.R")
LVP_KEY_SUFFIXES=(
    "data-raw/b30phenZerosJune7-2013.csv",
    "data-raw/compphenZerosJune7-2013.csv",
    "data-raw/fwphenZerosJune7-2013.csv",
    "data-raw/tkphenZerosJune7-2013.csv",
    "data-raw/clump_coord.csv","data-raw/even_coord.csv",
    "data-raw/PollinatorVisitationDatafiles/PollinatorObservation_Comp&B30_editedForTimeSlices2.csv",
    "data-raw/PollinatorVisitationDatafiles/PollinatorObservation_FarWest&Track_editedForTimeSlices2.csv",
)
META_MAX=3*1024*1024
ZIP_MAX=4*1024*1024
RHP_FILE_MAX=256*1024
ZIP_ENTRIES_MAX=1500
ZIP_EXTRACT_MAX=2*1024*1024
ZIP_TOTAL_UNCOMPRESSED_MAX=200*1024*1024
SAFE_HEADER=re.compile(r"^[A-Za-z][\w .()/%+&-]{0,85}$")

def official_url(href,allowed):
    if not href:raise ValueError("Missing source advertised HTTPS link")
    url=urljoin(allowed,href)
    parsed=urlparse(url)
    if parsed.scheme!="https" or parsed.hostname!=urlparse(allowed).hostname:
        raise ValueError("Unapproved source download host")
    if allowed==DRYAD and not parsed.path.startswith("/api/v2/"):
        raise ValueError("Unapproved non-official Dryad API file path")
    return url

def fetch(href,allowed,limit):
    url=official_url(href,allowed)
    req=Request(url,headers={"User-Agent":"egwee-source-only-independent-paternity-gate/1.0",
                             "Accept":"application/json,application/octet-stream,application/zip,text/plain,*/*"})
    with urlopen(req,timeout=42) as response:
        final=response.geturl()
        # Prevent accidental silent redirects to third party targets.
        if urlparse(final).hostname!=urlparse(allowed).hostname:
            raise ValueError("Source download redirected outside approved host")
        body=response.read(limit+1)
        if len(body)>limit:
            raise ValueError("Source exceeds bounded retrieval size")
        return body

def source_error(ex):
    out={"error_type":type(ex).__name__}
    if isinstance(ex,HTTPError):out["http_status"]=ex.code
    else:out["bounded_reason"]=str(ex)[:170]
    return out

def dryad_rel(doc,rel):
    obj=(doc.get("_links") or {}).get(rel) or {}
    return obj.get("href") if isinstance(obj,dict) else None

def get_dryad_files(dataset,api):
    verhref=dryad_rel(dataset,"stash:version")
    if not verhref:
        records=json.loads(fetch(api+"/versions",DRYAD,META_MAX))
        versions=(records.get("_embedded") or {}).get("stash:versions") or []
        if not versions:raise ValueError("No publisher version link")
        verhref=dryad_rel(versions[-1],"self")
    if not verhref:raise ValueError("Version endpoint unspecified")
    version=json.loads(fetch(verhref,DRYAD,META_MAX))
    path=dryad_rel(version,"stash:files")
    if not path:raise ValueError("No publisher file inventory link")
    files=json.loads(fetch(path,DRYAD,META_MAX))
    return (files.get("_embedded") or {}).get("stash:files") or []

def safe_table_metadata(raw,filename):
    # Do not interpret original numerical response values; count only lines
    # and inspect text of the first line, which may or may not be a header.
    text=None
    for enc in ("utf-8-sig","cp1252","latin-1"):
        try:text=raw.decode(enc,"strict");break
        except UnicodeDecodeError:pass
    if text is None:raise ValueError("Source has no lossless text encoding")
    lines=[x for x in text.splitlines() if x.strip()]
    if not lines:raise ValueError("Blank original source")
    first=lines[0]
    sep=max(("\t",",",";"),key=first.count)
    row=next(csv.reader([first],delimiter=sep))
    plausible=len(row)>=2 and len(row)<=180 and all(SAFE_HEADER.fullmatch(c.strip()) for c in row)
    headers=[c.strip() for c in row] if plausible else []
    return {"original_filename":filename,
            "total_nonblank_physical_lines":len(lines),
            "first_row_header_like":plausible,
            "first_row_field_count":len(row),
            "safe_header_labels_only":headers[:180],
            "delimiter_kind":{"\t":"tab",",":"comma",";":"semicolon"}[sep],
            "source_numeric_outcomes_interpreted":False}

def zip_manifest(raw):
    if not zipfile.is_zipfile(BytesIO(raw)):
        raise ValueError("Original zipped author study is not ZIP")
    with zipfile.ZipFile(BytesIO(raw)) as z:
        info=[x for x in z.infolist() if not x.is_dir()]
        if len(info)>ZIP_ENTRIES_MAX:raise ValueError("Unexpected ZIP source entry count")
        if sum(x.file_size for x in info)>ZIP_TOTAL_UNCOMPRESSED_MAX:
            raise ValueError("Original archive uncompressed size exceeds bound")
        names={i.filename:i for i in info}
        inspected=[]
        for suffix in LVP_KEY_SUFFIXES:
            choices=[n for n in names if n.endswith("/"+suffix) or n==suffix]
            if len(choices)!=1:
                inspected.append({"source_expected_path":suffix,
                                  "status":"EXPECTED_EXACT_SUFFIX_MISSING_OR_AMBIGUOUS",
                                  "number_of_matches":len(choices)})
                continue
            name=choices[0]
            item=names[name]
            status={"source_expected_path":suffix,
                    "relative_archive_filename":suffix,
                    "size_uncompressed_bytes":item.file_size,
                    "status":"NOT_OPENED"}
            if item.file_size>ZIP_EXTRACT_MAX:
                status["status"]="ENTRY_TOO_LARGE_FOR_HEADER_GATE"
            else:
                blob=z.read(name)
                status.update(safe_table_metadata(blob,suffix))
                status["source_original_entry_sha256"]=hashlib.sha256(blob).hexdigest()
                status["status"]="ORIGINAL_SOURCE_HEADER_AND_ROWS_VERIFIED"
            inspected.append(status)
        # Entry listing only; never open genotype/derived chain contents.
        pedigree_paths=sorted(PurePosixPath(name).name for name in names
                               if "/data/pedigree_assignment/" in "/"+name
                               and name.lower().endswith(".csv"))
        visit_paths=sorted(PurePosixPath(name).name for name in names
                           if "PollinatorVisitationDatafiles/" in name
                           and name.lower().endswith(".csv"))
        return {
           "n_original_archive_entries":len(info),
           "sum_declared_original_uncompressed_bytes":sum(x.file_size for x in info),
           "original_pedigree_csv_filenames_only":pedigree_paths[:35],
           "original_visit_csv_filenames_only":visit_paths[:20],
           "targeted_original_source_header_audit":inspected,
           "source_individual_phenotype_or_genotype_values_examined":False,
        }

def one_lvp():
    result={"programme_id":"LVP001",
            "source_doi":LVP_DOI,
            "source_url":"https://doi.org/"+LVP_DOI,
            "status":"SOURCE_NOT_CHECKED",
            "no_source_raw_rows_redistributed":True,
            "original_outcome_coefficients_computed":False,
            "source_parentage_join_verified":False,
            "source_visitor_directional_partner_trajectories_verified":False,
            "independent_published_programmes_from_this_source":1}
    api=DRYAD+"/api/v2/datasets/"+quote("doi:"+LVP_DOI,safe="")
    try:
        meta=json.loads(fetch(api,DRYAD,META_MAX))
        if str(meta.get("identifier","")).casefold()!="doi:"+LVP_DOI:
            raise ValueError("Dryad identifier does not match source DOI")
        result["original_metadata_verified"]=True
        result["source_published_title"]=str(meta.get("title",""))[:180]
        files=get_dryad_files(meta,api)
        result["original_published_file_inventory_count"]=len(files)
        names={str(f.get("path","")).split("/")[-1]:f for f in files}
        result["original_expected_file_name_presence"]={k:(k in names) for k in LVP_FILES}
        if any(x not in names for x in LVP_FILES):
            raise ValueError("Original source missing ZIP or README")
        result["status"]="SOURCE_METADATA_AND_FILES_VERIFIED"
    except (HTTPError,URLError,ValueError,KeyError,TypeError,json.JSONDecodeError) as ex:
        result.update(source_error(ex))
        result["status"]="SOURCE_METADATA_OR_FILE_INVENTORY_STOP"
        return result
    for name in LVP_FILES:
        f=names[name]
        receipt={"original_filename":name,"advertised_size":f.get("size"),
                 "original_advertised_digest":f.get("digest"),
                 "status":"ORIGINAL_FILE_FETCH_NOT_ATTEMPTED"}
        try:
            source_rel=dryad_rel(f,"stash:download")
            if not source_rel:raise ValueError("File metadata has no publisher download link")
            raw=fetch(source_rel,DRYAD,ZIP_MAX if name.endswith(".zip") else RHP_FILE_MAX)
            receipt["source_sha256"]=hashlib.sha256(raw).hexdigest()
            receipt["source_size_verified"]=len(raw)==f.get("size")
            if not receipt["source_size_verified"]:
                raise ValueError("Original source size mismatch")
            digest=f.get("digest")
            dtype=f.get("digestType")
            if digest:
                if not isinstance(dtype,str):raise ValueError("Original digest type unspecified")
                if dtype.casefold()=="md5":
                    if hashlib.md5(raw).hexdigest().casefold()!=str(digest).casefold():
                        raise ValueError("Dryad original file MD5 mismatch")
                elif dtype.casefold()=="sha256":
                    if receipt["source_sha256"].casefold()!=str(digest).casefold():
                        raise ValueError("Dryad original file SHA256 mismatch")
                else:
                    receipt["unrecognized_original_digest_type"]=str(dtype)[:45]
            if name.endswith(".zip"):receipt["archive"]=zip_manifest(raw)
            else:receipt.update(safe_table_metadata(raw,name))
            receipt["status"]="SOURCE_ORIGINAL_SCHEMA_PASS"
        except (HTTPError,URLError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as ex:
            receipt.update(source_error(ex))
            receipt["status"]="PUBLIC_ORIGINAL_SOURCE_ACCESS_OR_HEADER_STOP"
        result.setdefault("files",[]).append(receipt)
    result["original_retrieved_files"]=sum(x["status"]=="SOURCE_ORIGINAL_SCHEMA_PASS"
                                          for x in result["files"])
    result["status"]=("ALL_ORIGINAL_SOURCE_HEADERS_VERIFIED" if
        result["original_retrieved_files"]==2 else
        "PUBLIC_ORIGINAL_SOURCE_ACCESS_STOP")
    result["decision"]=("PARENTAGE_EXACT_KEY_FREEZE_NEEDED" if
        result["original_retrieved_files"]==2 else
        "DO_NOT_INFER_PARENTAGE_OR_VISIT_IDENTITY")
    return result

def one_rhp():
    result={"programme_id":"RHP001",
            "source_doi":RHP_DOI,
            "zenodo_mirror_record":RHP_RECORD,
            "source_url":"https://zenodo.org/records/4942351",
            "status":"SOURCE_NOT_CHECKED",
            "no_source_raw_rows_redistributed":True,
            "original_outcome_coefficients_computed":False,
            "same_mother_father_observed_contact_verified":False,
            "independent_published_programmes_from_this_source":1}
    try:
        meta=json.loads(fetch(ZENODO+f"/api/records/{RHP_RECORD}",ZENODO,META_MAX))
        if int(meta.get("id",-1))!=RHP_RECORD:
            raise ValueError("Wrong published Zenodo source mirror record")
        documented=str(meta.get("doi","") or "")
        # Mirror stores an original Dryad DOI, not a new source study.
        if documented and documented.casefold()!=RHP_DOI:
            raise ValueError("Zenodo mirror DOI mismatches original Dryad identifier")
        fentries=meta.get("files") or {}
        if isinstance(fentries,dict):entries=fentries.get("entries") or {}
        else:entries=fentries
        if isinstance(entries,list):entries={f["key"]:f for f in entries}
        if not isinstance(entries,dict):raise ValueError("No Zenodo file inventory")
        result["original_metadata_verified"]=True
        result["original_published_file_inventory_count"]=len(entries)
        result["original_source_expected_names_present"]={
          n:n in entries for n in RHP_FILES}
        if not all(n in entries for n in RHP_FILES):
            raise ValueError("Original mirror lacks one or more 9 advertised files")
        result["status"]="SOURCE_METADATA_AND_FILES_VERIFIED"
    except (HTTPError,URLError,ValueError,KeyError,TypeError,json.JSONDecodeError) as ex:
        result.update(source_error(ex))
        result["status"]="SOURCE_METADATA_OR_FILE_INVENTORY_STOP"
        return result
    for name in RHP_FILES:
        entry=entries[name]
        receipt={"original_filename":name,"advertised_size":entry.get("size"),
                 "status":"NOT_ACCESSED"}
        try:
            href=(entry.get("links") or {}).get("content") or (entry.get("links") or {}).get("self")
            if not href:raise ValueError("No published original Zenodo source file URL")
            raw=fetch(href,ZENODO,RHP_FILE_MAX)
            if len(raw)!=entry.get("size"):
                raise ValueError("Zenodo file declared-size mismatch")
            digest=str(entry.get("checksum") or "")
            if digest:
                alg,_,hashvalue=digest.partition(":")
                if alg.lower()=="md5":
                    if hashlib.md5(raw).hexdigest()!=hashvalue.lower():
                        raise ValueError("Zenodo original publisher MD5 mismatch")
                elif alg.lower()=="sha256":
                    if hashlib.sha256(raw).hexdigest()!=hashvalue.lower():
                        raise ValueError("Zenodo original publisher SHA256 mismatch")
                else:raise ValueError("Unrecognized original Zenodo digest")
            receipt["source_sha256"]=hashlib.sha256(raw).hexdigest()
            receipt["original_checksum_verified"]=bool(digest)
            if name.lower().endswith(".csv"):
                receipt.update(safe_table_metadata(raw,name))
            elif name.lower().endswith(".xlsx"):
                if not zipfile.is_zipfile(BytesIO(raw)):
                    raise ValueError("Original source XLSX not a ZIP")
                with zipfile.ZipFile(BytesIO(raw)) as z:
                    receipt["original_xlsx_worksheet_count"]=sum(
                        x.startswith("xl/worksheets/") and x.endswith(".xml")
                        for x in z.namelist())
                receipt["genotype_worksheet_values_examined"]=False
            elif name.lower().endswith(".r"):
                receipt["original_R_source_bytes_verified"]=True
                receipt["author_original_R_code_executed"]=False
            receipt["status"]="SOURCE_ORIGINAL_SCHEMA_PASS"
        except (HTTPError,URLError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as ex:
            receipt.update(source_error(ex))
            receipt["status"]="PUBLIC_ORIGINAL_SOURCE_ACCESS_OR_HEADER_STOP"
        result.setdefault("files",[]).append(receipt)
    result["original_retrieved_files"]=sum(x["status"]=="SOURCE_ORIGINAL_SCHEMA_PASS"
                                          for x in result["files"])
    result["status"]=("ALL_ORIGINAL_SOURCE_HEADERS_VERIFIED" if
       result["original_retrieved_files"]==9 else
       "PUBLIC_ORIGINAL_SOURCE_ACCESS_STOP")
    result["decision"]=("RHP_MATERNAL_FAMILY_EXACT_KEY_FREEZE_REQUIRED" if
       result["original_retrieved_files"]==9 else
       "NO_SOURCE_REPRESENTATION_OR_EFFECT_INFERENCE")
    return result

def synthetic():
    t=safe_table_metadata(b"plantID,treatment,isolation20,correlatedPaternity\nA,c,1,0.5\n",
                          "multiplePaternity.csv")
    assert t["first_row_header_like"] and t["total_nonblank_physical_lines"]==2
    assert official_url("/api/v2/test",DRYAD)=="https://datadryad.org/api/v2/test"
    assert official_url("https://zenodo.org/api/records/4942351",ZENODO).endswith("4942351")
    try:official_url("https://other.example/file",DRYAD)
    except ValueError:pass
    else:raise AssertionError("Untrusted file download host accepted")
    print("EGWEE_TWO_INDEPENDENT_PARENTAGE_SOURCE_STRUCTURAL_SYNTHETIC_PASS")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--output",type=Path)
    a=ap.parse_args()
    if a.self_test:synthetic();return 0
    if a.output is None:ap.error("--output required")
    results=[one_lvp(),one_rhp()]
    output={
      "status":"TWO_CANDIDATE_PROGRAMME_SOURCE_AUDIT_COMPLETE",
      "n_independent_original_publication_programmes":2,
      "published_programmes":results,
      "direct_contact_v_genetic_parentage_study_n_verified":sum(
          r.get("source_visitor_directional_partner_trajectories_verified",False)
          or r.get("same_mother_father_observed_contact_verified",False) for r in results),
      "previous_Barbot_one_study_father_contact_result_changed":False,
      "no_original_genotypes_parentage_values_individual_IDs_or_source_data_redistributed":True,
      "any_new_biological_effect_estimated":False,
      "decision":"STOP_DIRECT_REPLICATION_UNTIL_PARTNER_CONTACT_KEYS_VERIFIED"
    }
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(output,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    brief={"status":output["status"],"direct_contact_v_genetic_parentage_study_n_verified":
           output["direct_contact_v_genetic_parentage_study_n_verified"],
           "programmes":[{
              "id":x["programme_id"],"status":x["status"],
              "original_retrieved_files":x.get("original_retrieved_files"),
              "error_type":x.get("error_type"),
              "files":[{
                  "name":f["original_filename"],"status":f["status"],
                  "http_status":f.get("http_status"),
                  "entry_n":f.get("archive",{}).get("n_original_archive_entries"),
                  "headings":f.get("safe_header_labels_only"),
                  "n_physical_lines":f.get("total_nonblank_physical_lines")
              } for f in x.get("files",[])]
           } for x in results]}
    print("EGWEE_INDEPENDENT_ORIGINAL_PARENTAGE_SOURCE_AUDIT "+
          json.dumps(brief,sort_keys=True),flush=True)
    return 0

if __name__=="__main__":raise SystemExit(main())
