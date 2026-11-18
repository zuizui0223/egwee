#!/usr/bin/env python3
"""QPF004 local original-data identity and XLSX structure gate.

Run ONLY after user supplies the exact original Dryad 10.7280/D19X0D ZIP.
Verify the officially published 2020 source files' names, lengths and SHA256
before inspecting any XLSX sheet dimensions. PDF contents are NEVER opened or
interpreted here; their original bytes only receive SHA/CRC checks.

Source-only structural mode:
- no plant, ramet, flower, genotype, pollen, seed, visitor IDs or outcomes;
- no first-row text printed (a first row may actually be source observations);
- only workbook XML sheet counts, cell-address width and row counts;
- no data/model fitted or original workbooks redistributed.
"""
from __future__ import annotations
import argparse
from io import BytesIO
import hashlib
import json
from pathlib import Path
import re
import zipfile
from xml.etree import ElementTree as ET

ORIGINAL_FILES = {
    "gallagher&campbell_phenologyExperimentData.xlsx": {
        "bytes":96329,
        "sha256":"51263c0cabe9dd04dbf716a4594e7d700c5235dd3f85a65ab51f43fcef828411",
        "year":2015,
        "design":"phenology manipulation, field visitation and per-plant seed set",
    },
    "gallagher&campbell_pollinatorEffectivenessData.xlsx":{
        "bytes":77873,
        "sha256":"bbfcbbaf43b53b0ef835b891bd8932ae3761a383e4ecb1f38440a4ba9d477c38",
        "year":2016,
        "design":"marked single-visit flower/ramet pollen and seed assays",
    },
    "gallagher&campbell_nonSpatialData_phenologyExperiment.pdf":{
        "bytes":236709,
        "sha256":"14d97ecbf68da07252293c751987789d768181bba23da38a9b036dac0cd19972",
        "year":2015,
        "design":"original metadata PDF; only bytes/sha verified; content NOT read",
    },
    "gallagher&campbell_nonSpatialData_pollinatorEffectiveness.pdf":{
        "bytes":206337,
        "sha256":"f12e0588619e4a795d7f56a3d42f11cd4b7328716a901041e95f90c67e54ca7f",
        "year":2016,
        "design":"original metadata PDF; only bytes/sha verified; content NOT read",
    }
}
NS="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
MAX_SOURCE_ZIP_BYTES=4*1024*1024

def verify_original_files(source_zip:Path, expected=ORIGINAL_FILES) -> dict[str,bytes]:
    raw=source_zip.read_bytes()
    if len(raw)>MAX_SOURCE_ZIP_BYTES:
        raise ValueError("Original ZIP exceeds bounded file audit size")
    with zipfile.ZipFile(BytesIO(raw)) as z:
        if z.testzip() is not None:
            raise ValueError("Original source ZIP CRC check failed")
        entries=[r for r in z.infolist() if not r.is_dir()]
        if len(entries)!=len(expected):
            raise ValueError("Original source has an unregistered number of real files")
        byname={}
        for member in entries:
            if ".." in member.filename.replace("\\","/").split("/"):
                raise ValueError("Untrusted original path traversal")
            name=member.filename.replace("\\","/").split("/")[-1]
            if name in byname or name not in expected:
                raise ValueError("Duplicate or unregistered original file name")
            if member.file_size != expected[name]["bytes"]:
                raise ValueError("Original Dryad file size mismatch")
            data=z.read(member)
            if hashlib.sha256(data).hexdigest()!=expected[name]["sha256"]:
                raise ValueError("Original Dryad file SHA256 mismatch")
            byname[name]=data
        if set(byname)!=set(expected):
            raise ValueError("Source ZIP lacks one or more original published files")
    return byname

def colindex(ref:str)->int:
    match=re.match(r"^[A-Z]+",ref)
    if match is None:
        raise ValueError("Unexpected source worksheet cell address")
    n=0
    for c in match.group():
        n=n*26+ord(c)-64
    return n

def workbook_shape(original_bytes:bytes)->list[dict]:
    if not zipfile.is_zipfile(BytesIO(original_bytes)):
        raise ValueError("Source XLSX is not Excel OOXML")
    out=[]
    with zipfile.ZipFile(BytesIO(original_bytes)) as z:
        if z.testzip() is not None:
            raise ValueError("Original XLSX member CRC failed")
        paths=sorted(
            [x for x in z.namelist()
             if re.fullmatch(r"xl/worksheets/sheet[0-9]+[.]xml",x)],
            key=lambda s:int(re.search(r"sheet([0-9]+)",s).group(1))
        )
        if not paths or len(paths)>50:
            raise ValueError("Original source XLSX worksheet roster malformed")
        for path in paths:
            root=ET.fromstring(z.read(path))
            rows=root.findall(".//"+NS+"sheetData/"+NS+"row")
            maxcol=0
            first_cells=0
            count_cells=0
            for i,r in enumerate(rows):
                cells=r.findall(NS+"c")
                if i==0:
                    first_cells=len(cells)
                for c in cells:
                    count_cells+=1
                    maxcol=max(maxcol,colindex(c.attrib.get("r","")))
            out.append({
                "worksheet_xml":path,
                "physical_source_rows":len(rows),
                "max_source_column_index":maxcol,
                "nonempty_cell_nodes":count_cells,
                "first_physical_row_cell_count":first_cells,
                "first_row_values_or_biological_data_read":False,
            })
    return out

def audit(source_zip:Path)->dict:
    files=verify_original_files(source_zip)
    shapes={}
    for name in ORIGINAL_FILES:
        if not name.casefold().endswith(".xlsx"):
            continue
        shapes[name]=workbook_shape(files[name])
    return {
        "audit_id":"QPF004_uploaded_original_Dryad_2020_structural_gate",
        "status":"EXACT_ORIGINAL_ALL4_FILES_VERIFIED_SCHEMA_ONLY",
        "original_dataset_doi":"10.7280/D19X0D",
        "original_paper_doi":"10.1002/ajb2.1439",
        "correct_species":"Mertensia ciliata",
        "original_source_zip_sha256":hashlib.sha256(source_zip.read_bytes()).hexdigest(),
        "original_file_manifest":[
            {"name":name,"bytes":d["bytes"],"official_sha256":d["sha256"],
             "source_year":d["year"]}
            for name,d in ORIGINAL_FILES.items()
        ],
        "original_two_workbooks_worksheet_structure":shapes,
        "pdf_contents_read":False,
        "first_row_or_biological_values_read":False,
        "original_field_plant_ramet_flower_ID_joins_verified":False,
        "separate_2015_2016_cohort_design_preserved":True,
        "new_original_QPF_effects_fitted":False,
        "individual_raw_source_redistributed":False,
        "decision":"NEXT_VERIFY_BIOLOGICAL_KEYS_PER_EXPERIMENT_BEFORE_OUTCOME",
    }

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-zip",required=True,type=Path)
    ap.add_argument("--output",required=True,type=Path)
    args=ap.parse_args()
    result=audit(args.source_zip)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",
                           encoding="utf-8")
    print(json.dumps({
        "decision":result["decision"],
        "source":result["correct_species"],
        "worksheets":result["original_two_workbooks_worksheet_structure"],
        "raw_values_opened":False,
    },indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
