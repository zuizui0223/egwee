#!/usr/bin/env python3
"""Source-semantic audit: author text/code only and univariate completeness.
Never execute third-party code or export identities/locations/individual records."""
import json,re,hashlib
from collections import Counter
from audit_echinacea_author_semantics import official_drum,pinned,rows
from audit_echinacea_longterm_sources import HANDLES

def audit01():
    entries=official_drum(HANDLES["ECH01"])
    doc=pinned(entries,"readme.txt","553e6bf732740079b3bf43e78ea1837426d779c99730b876ff13d5ebf2d291b8").decode("utf-8-sig",errors="replace")
    code=pinned(entries,"analysis_code.R")
    text=code.decode("utf-8-sig",errors="replace")
    f=rows(pinned(entries,"offspring_fitness_data.csv","7e5bcc2a9fab0b559cae58c2cfeaba11d50cd2d2f445159939bf0f6e54a6c7a6"))
    p=rows(pinned(entries,"fitness_predictors.csv","d3d1d4ab1c95ba872995873af13f10ebcd44a8a2af5dcd4259967f792191b3fd"))
    f={r["cgPlaId"]:r for r in f}
    if len(p)!=438 or len(f)!=3961 or any(r["cgPlaId"] not in f for r in p):raise ValueError("source key mismatch")
    definitions=[]
    lines=doc.splitlines()
    for i,line in enumerate(lines):
        if re.search(r"Name:\s*(cgPlaId|parentDist|diffStartDir|ld\[|fl\[|hdCt\[|achCt\[|ach_pos|start\.dam|start\.sire|popCd|row\b|pos\b)",line,re.I):
            definitions.append({"field":line.strip(),"definition":next((s.strip() for s in lines[i+1:i+5] if "Description:" in s),"not in next four lines")})
    # Only source transformation expressions, no coordinates/identifiers or external scripts executed.
    excerpts=[]
    for i,line in enumerate(text.splitlines(),1):
        if re.search(r"\b(ld20\d\d|hdCt20\d\d|fl20\d\d|diffStartDir|parentDist|cgPlaId|ach_pos|achCt20\d\d)\b",line) and re.search(r"filter|subset|merge|join|mutate|is\.na|NA|ifelse|select|replace|as\.numeric|colSums|rowSums|==|!=",line):
            if len(line)<300 and not re.search(r"latitude|longitude|coordinates?|\bGPS\b",line,re.I):
                excerpts.append({"line":i,"text":line.strip()})
    categories={}
    # No outcome-predictor relationship read. Count data presence and source status categories only.
    matched=[f[r["cgPlaId"]] for r in p]
    for k in matched[0]:
        if re.fullmatch(r"(ld|fl|hdCt)20\d\d",k):
            c=Counter(str(r[k]).strip() for r in matched)
            if k.startswith(("ld","fl")):categories[k]=dict(c)
            else:categories[k]={"missing":sum(c[x] for x in ("","NA","NaN","NULL")),"explicit_zero":c["0"],"other_nonmissing":sum(c.values())-sum(c[x] for x in ("","NA","NaN","NULL","0"))}
    return {"n_matched":len(matched),"author_readme_field_definitions":definitions,
            "author_code_sha256":hashlib.sha256(code).hexdigest(),
            "author_code_transformations":excerpts[:40],"univariate_year_coverage":categories,
            "predictor_missing_counts":{k:sum(str(r.get(k,"")).strip().lower() in ("","na","nan","null") for r in p) for k in ("parentDist","diffStartDir","cgPlaId.dam","cgPlaId.sire","ach_pos","start.dam","start.sire","popCd.dam","popCd.sire")}}
def audit02():
    entries=official_drum(HANDLES["ECH02"])
    doc=pinned(entries,"readme.txt","df234c2369cd669a5d1314a9c433f00893dcb040334fee848366cce8a5c0db3b").decode("utf-8-sig",errors="replace")
    code=pinned(entries,"aster_analysis.R")
    lines=doc.splitlines();definitions=[]
    for i,line in enumerate(lines):
        if re.search(r"Name:\s*(focalCd|slingCd|slingYr|year\b|site\b|slingCt|newLD|status\b)",line,re.I):
            definitions.append({"field":line.strip(),"definition":next((s.strip() for s in lines[i+1:i+5] if "Description:" in s),"not in next four lines")})
    excerpts=[]
    for i,line in enumerate(code.decode("utf-8-sig",errors="replace").splitlines(),1):
        if re.search(r"focalCd|slingYr|slingCt|newLD",line) and re.search(r"join|merge|mutate|filter|subset|paste|year\s*[-+]|slingYr\s*[-+]|is\.na|==",line):
            if len(line)<300 and not re.search(r"latitude|longitude|coordinates?|\bGPS\b",line,re.I):excerpts.append({"line":i,"text":line.strip()})
    return {"author_readme_field_definitions":definitions,"author_code_sha256":hashlib.sha256(code).hexdigest(),"author_code_transformations":excerpts[:35]}
def main():
    out={"no_model_fitted":True,"source_code_executed":False,"raw_records_exported":False}
    for name,fn in [("ECH01",audit01),("ECH02",audit02)]:
        try:out[name]=dict(status="SOURCE_SEMANTICS_INSPECTED",**fn())
        except Exception as e:out[name]={"status":"SOURCE_STOP","reason":type(e).__name__}
    print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
