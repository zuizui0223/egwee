#!/usr/bin/env python3
"""Attempt SOURCE-DEFINED 2026 Lupinus line-code dictionary from small first worksheet.
No phenotype worksheet, genotype calls or seed values are accessed. Only vetted
single-letter treatment codes and presence of controlled category terms are emitted.
"""
from io import BytesIO
import json,re
from pathlib import Path
import sys
import zipfile
from xml.etree import ElementTree as ET
from urllib.parse import urlparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"rescue_coupling"))
from audit_lupinus_id_linkage import download

ARTICLE=29606180
NAME="Lupinus_angustifolius_data_field.xlsx"
LETTERS={"C","J","L","R","T","X"}
TERM={
    "control":r"\bcontrol\b|\bCFL\b",
    "assisted_gene_flow":r"\bgene.flow\b|\bGFL\b|\bassisted\b",
    "artificial_selection":r"\bselection\b|\bEFL\b",
    "backcross":r"\bbackcross\b|\bBCL\b",
    "selfing":r"\bself[- ]?(pollination|cross|fertiliz)\b|\bSPL\b|\bOUTS\b",
    "outcross":r"\boutcross\b|\bOUT\b",
}
NS={"m":"http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

def analyze_texts(lines):
    detected=[]
    for row_number,txt in enumerate(lines,1):
        if not isinstance(txt,str) or len(txt)>350:continue
        terms=[k for k,p in TERM.items() if re.search(p,txt,re.I)]
        if not terms:continue
        m=re.match(r"^\s*([CJLRTX])\s*[:=\-\. ]\s*(.{4,})",txt,re.I)
        code=m.group(1).upper() if m else None
        detected.append({"source_sheet1_row":row_number,"line_letter":code,
                         "controlled_semantic_keywords":terms})
    unique={x["line_letter"] for x in detected if x["line_letter"]}
    result={"status":"SOURCE_SHEET1_TEXT_CLASSIFICATION_NO_BIOLOGICAL_VALUES",
            "sheet1_physical_text_rows":len(lines),
            "controlled_keyword_rows":detected,
            "unique_coded_lines_detected":len(unique),
            "line_mapping_established":len(unique)>=3,
            "raw_document_text_redistributed":False,
            "individual_or_genetic_values_read":False,
            "phenotype_or_seed_values_read":False,
            "effect_estimated":False}
    result["decision"]=("SOURCE_CODEBOOK_CANDIDATE_REQUIRES_AUTHOR_CHECK"
                        if result["line_mapping_established"]
                        else "NO_VERIFIED_CODEBOOK_IN_SOURCE_SHEET1")
    return result

def run():
    metadata=json.loads(download(f"https://api.figshare.com/v2/articles/{ARTICLE}").decode())
    doi=str(metadata.get("doi","")).lower()
    if "10.6084/m9.figshare.29606180" not in doi:
        raise ValueError("unexpected source DOI")
    f=next((x for x in metadata.get("files",[]) if x.get("name")==NAME),None)
    if not f or not f.get("download_url"):raise ValueError("source file not listed")
    url=f["download_url"]
    if urlparse(url).scheme!="https" or urlparse(url).hostname not in {
        "figshare.com","api.figshare.com","ndownloader.figshare.com"}:
        raise ValueError("Non-source URL")
    raw=download(url)
    lines=[]
    with zipfile.ZipFile(BytesIO(raw)) as z:
        s=[]
        if "xl/sharedStrings.xml" in z.namelist():
            root=ET.fromstring(z.read("xl/sharedStrings.xml"))
            s=["".join(t.text or "" for t in el.findall(".//m:t",NS))
               for el in root.findall("m:si",NS)]
        r=ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
        for row in r.findall(".//m:sheetData/m:row",NS):
            strs=[]
            for cell in row.findall("m:c",NS)[:3]:
                typ=cell.get("t");v=cell.find("m:v",NS)
                if typ=="s" and v is not None:
                    i=int(v.text)
                    if 0<=i<len(s):strs.append(s[i])
                elif typ=="inlineStr":
                    strs.append("".join(x.text or "" for x in cell.findall(".//m:t",NS)))
                elif typ=="str" and v is not None:
                    strs.append(v.text or "")
                # Deliberately skip all numeric/formula cells.
            lines.append(" ".join(strs))
    if len(lines)>30:raise ValueError("Unexpected sheet1 size")
    return analyze_texts(lines)

if __name__=="__main__":
    from urllib.error import HTTPError,URLError
    try: res=run()
    except (HTTPError,URLError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as e:
        res={"status":"SOURCE_TEXT_DOC_GATE_STOP","reason_type":type(e).__name__,
             "raw_document_text_redistributed":False,
             "individual_or_genetic_values_read":False,
             "phenotype_or_seed_values_read":False,
             "effect_estimated":False,"decision":"SOURCE_DOC_ACCESS_STOP"}
    print(json.dumps(res,ensure_ascii=False,indent=2))
