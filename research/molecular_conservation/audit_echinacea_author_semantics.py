#!/usr/bin/env python3
"""Read public author documentation and verify source keys, never numerical effects."""
import csv,io,hashlib,json,re
from collections import Counter
from urllib.parse import quote
from audit_echinacea_longterm_sources import get,js,href,BASE,HANDLES,FIG

def official_drum(handle):
    item=js(BASE+"/pid/find?id="+quote(handle,safe=""))
    if item["handle"]!=handle:raise ValueError("handle mismatch")
    entries={}
    for b in js(href(item,"bundles"))["_embedded"]["bundles"]:
        if b.get("name")=="ORIGINAL":
            for f in js(href(b,"bitstreams"))["_embedded"]["bitstreams"]:
                entries[f["name"]]=href(f,"content")
    return entries
def rows(raw):return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
def pinned(entries,name,sha=None):
    raw,_=get(entries[name])
    actual=hashlib.sha256(raw).hexdigest()
    if sha and actual!=sha:raise ValueError("digest mismatch: "+name)
    return raw
def docs(raw,terms):
    # Expose only author field-definition lines, never records, IDs or site coordinates.
    text=raw.decode("utf-8-sig",errors="replace")
    result=[]
    for line in text.splitlines():
        s=line.strip()
        if len(s)>600:continue
        if any(re.search(r"\b"+re.escape(t)+r"\b",s,re.I) for t in terms):
            if re.search(r"latitude|longitude|coordinates?|\bGPS\b",s,re.I):continue
            result.append(s)
    return result[:65]
def unique_key_stats(data,fields):
    k=[tuple(str(r.get(f,"")).strip() for f in fields) for r in data]
    c=Counter(k)
    return {"rows":len(data),"unique_keys":len(c),"duplicated_key_count":sum(n>1 for n in c.values()),
            "empty_key_rows":sum(any(v in ("","NA","NaN") for v in a) for a in k)},set(k)
def ech01():
    files=official_drum(HANDLES["ECH01"])
    f=rows(pinned(files,"offspring_fitness_data.csv","7e5bcc2a9fab0b559cae58c2cfeaba11d50cd2d2f445159939bf0f6e54a6c7a6"))
    p=rows(pinned(files,"fitness_predictors.csv","d3d1d4ab1c95ba872995873af13f10ebcd44a8a2af5dcd4259967f792191b3fd"))
    a,x=unique_key_stats(f,["cgPlaId"]);b,y=unique_key_stats(p,["cgPlaId"])
    doc=pinned(files,"readme.txt","553e6bf732740079b3bf43e78ea1837426d779c99730b876ff13d5ebf2d291b8")
    return {"offspring_key_audit":a,"predictor_key_audit":b,"matched_offspring_ids":len(x&y),
            "predictor_only_ids":len(y-x),"fitness_only_ids":len(x-y),
            "parent_pair_unique_count":unique_key_stats(p,["cgPlaId.dam","cgPlaId.sire"])[0],
            "maternal_unique_count":unique_key_stats(p,["cgPlaId.dam"])[0]["unique_keys"],
            "author_documentation":docs(doc,["cgPlaId","parentDist","diffStartDir","ld2006","ld2022","ld","fl","hdCt","achCt"])}
def ech02():
    files=official_drum(HANDLES["ECH02"])
    m=rows(pinned(files,"mating_potential.csv","495635aa8c822ab8a251f9f6375e9f8d847ef9dc9b017b64d3becebda9a12193"))
    s=rows(pinned(files,"seedling_demography.csv","5d305c5742e894b03d9f88a77f0c5095f066a8a1d3612124a6a0e80410a062c6"))
    a,x=unique_key_stats(m,["focalCd","site","year"])
    b,y=unique_key_stats(s,["focalCd","site","slingYr"])
    # This is only an equality test for candidate source labels. Meaning of year and
    # slingYr requires the author documentation; no cross-year assumption here.
    doc=pinned(files,"readme.txt","df234c2369cd669a5d1314a9c433f00893dcb040334fee848366cce8a5c0db3b")
    return {"mating_key":a,"candidate_seedling_key":b,"exact_candidate_key_overlap":len(x&y),
            "mating_sites":len({r["site"] for r in m}),
            "seedling_identity_candidate":unique_key_stats(s,["focalCd","site","slingYr","slingCd"])[0],
            "source_status_categories":sorted({str(r.get("status","")) for r in s}),
            "author_documentation":docs(doc,["focalCd","slingCd","slingYr","status","newLD","matingPotential1","matingPotential2","slingCt","radius","hdCt.n","hdCt.o"])}
def ech03():
    m=js("https://api.figshare.com/v2/articles/"+str(FIG))
    if m["id"]!=FIG or m["doi"]!="10.6084/m9.figshare.23994528.v1":raise ValueError("DOI mismatch")
    files={f["name"]:f["download_url"] for f in m["files"]}
    d=rows(pinned(files,"burnRemsPopData.csv","28911e8c2a83bddbb75124dfcb0bf12add21c199b54bc3e308a41c47bf3fa675"))
    doc=pinned(files,"burnRemsPopMetadata.txt","135c13432a6d31b5249bc527ecc7f20a87ccab4e5b674a005650a4e6265b2a8e")
    counts={}
    for k in ["burnSite","year","burned","popSize","census","propFl","nFl","meanHdCt","nSdSet","meanSdSet","meanSp1","meanSp2","nOMP","meanOMP","nSync","meanSync","nn7.hmean","meanFecundity"]:
        counts[k]=sum(str(r.get(k,"")).strip() not in ("","NA","NaN","NULL") for r in d)
    return {"scene_key_audit":unique_key_stats(d,["burnSite","year"])[0],
            "distinct_sites":len({r["burnSite"] for r in d}),
            "distinct_years":len({r["year"] for r in d}),
            "burned_code_categories":sorted({r["burned"] for r in d}),
            "nonmissing_fields":counts,
            "author_documentation":docs(doc,["burnSite","year","burned","popSize","census","propFl","nFl","meanHdCt","nSdSet","meanSdSet","meanSp1","meanSp2","nOMP","meanOMP","nSync","meanSync","nn7.hmean","meanFecundity"])}
def main():
    result={"no_model_fitted":True,"raw_rows_exported":False,"key_semantics_require_source_documentation":True}
    for name,func in [("ECH01",ech01),("ECH02",ech02),("ECH03",ech03)]:
        try:result[name]=dict(status="source_design_inspected",**func())
        except Exception as e:result[name]={"status":"source_stop","error":type(e).__name__}
    print(json.dumps(result,indent=2,ensure_ascii=False))
if __name__=="__main__":main()
