#!/usr/bin/env python3
"""Read only PUBLIC categorical study-design labels, never outcomes, in 2026 Lupinus field source."""
from collections import Counter
import hashlib,json
from pathlib import Path
import sys
from urllib.parse import urlparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"rescue_coupling"))
from audit_lupinus_id_linkage import data_to_sparse_rows,download
ARTICLE=29606180
NAME="Lupinus_angustifolius_data_field.xlsx"
CATS={"population","line","year","site","treatment","block","origin"}
OTHER={"id","genotype","family","sister"}
def run():
    rec={"status":"SOURCE_STOP","source_article_id":ARTICLE,
         "raw_data_redistributed":False,"phenotype_values_read":False,
         "snp_values_read":False,"effect_estimated":False,
         "mate_interaction_observed":False}
    m=json.loads(download(f"https://api.figshare.com/v2/articles/{ARTICLE}").decode("utf8"))
    d=str(m.get("doi","")).casefold().removeprefix("https://doi.org/")
    if not(d=="10.6084/m9.figshare.29606180" or d.startswith("10.6084/m9.figshare.29606180.v")):
        raise ValueError("wrong source")
    f=next((x for x in m.get("files",[]) if x.get("name")==NAME),None)
    if not f:raise ValueError("missing source file")
    url=f.get("download_url")
    if not url or urlparse(url).hostname not in ("figshare.com","api.figshare.com","ndownloader.figshare.com"):
        raise ValueError("unverified download origin")
    buf=download(url)
    head,rows=data_to_sparse_rows(buf,"xl/worksheets/sheet2.xml",CATS|OTHER)
    if not {"id","population","line","genotype"}.issubset(head):
        raise ValueError("missing source design fields")
    out={"sha256":hashlib.sha256(buf).hexdigest(),"rows":len(rows),
         "source_design_headers":head,"categorical_cardinality":{},
         "categories_with_at_least_5_observations":{},
         "nonempty_identifier_rows":sum(str(x.get("id","")).strip()!="" for x in rows),
         "unique_identifier_labels":len(set(str(x.get("id","")).strip() for x in rows if str(x.get("id","")).strip())),
         "unique_genotype_label_count":len(set(str(x.get("genotype","")).strip() for x in rows if str(x.get("genotype","")).strip()))}
    for c in sorted(CATS):
        if c not in head:continue
        count=Counter(str(x.get(c,"")).strip() for x in rows if str(x.get(c,"")).strip())
        out["categorical_cardinality"][c]=len(count)
        if c in {"population","line","year","site","treatment","origin"}:
            out["categories_with_at_least_5_observations"][c]={
                k:n for k,n in sorted(count.items()) if n>=5 and len(k)<=60}
    rec.update(out)
    rec["status"]="PUBLIC_DESIGN_CATEGORIES_VERIFIED_NO_OUTCOME_VALUES"
    rec["decision"]="LOCK_ENDPOINT_AND_TREATMENT_CONTRAST_BEFORE_READING_SEED_VALUES"
    return rec

if __name__=="__main__":
    from urllib.error import HTTPError, URLError
    try:r=run()
    except (HTTPError,URLError,ValueError,KeyError,TypeError) as e:
        r={"status":"SOURCE_STOP","error_type":type(e).__name__,
           "phenotype_values_read":False,"snp_values_read":False,
           "effect_estimated":False,"raw_data_redistributed":False,
           "decision":"SOURCE_DESIGN_SCHEMA_STOP"}
        if isinstance(e,HTTPError):r["http_status"]=e.code
    print(json.dumps(r,indent=2,ensure_ascii=False))
