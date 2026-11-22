#!/usr/bin/env python3
"""Source-only 2025–2026 Lupinus lineage/ID compatibility gate.

Reads only source-native ID, population, line, genotype-label, year and block
columns from two published Figshare XLSX files. No phenotype values, SNP variants
or individual IDs exported. Cross-generation labels are NOT the same individual.
"""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys
from urllib.parse import urlparse
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "rescue_coupling"))
from audit_lupinus_id_linkage import data_to_sparse_rows, download  # source-defined ID parser

SOURCES=(
  (28304024, "10.6084/m9.figshare.28304024",
   "data_Lupinusangustifolius_geneflow.xlsx",
   "c8033a1eee55663549e42c22264b830461db320f4f3209718df10b3f4a67df10"),
  (29606180, "10.6084/m9.figshare.29606180",
   "Lupinus_angustifolius_data_field.xlsx", None),
)
FIELDS={"id","plant_id","population","line","genotype","year","site","family",
        "sister","block","cohort","generation","origin"}
REQUIRED={"id","population","line","genotype"}

def metadata_source(article_id):
    meta=json.loads(download(f"https://api.figshare.com/v2/articles/{article_id}").decode("utf-8"))
    return meta

def verified_source(entry):
    aid,doi,name,pinned_sha=entry
    meta=metadata_source(aid)
    md=str(meta.get("doi","")).lower().removeprefix("https://doi.org/")
    if not (md==doi or (md.startswith(doi+".v") and md[len(doi)+2:].isdigit())):
        raise ValueError("Unexpected Figshare source DOI")
    matching=[f for f in meta.get("files",[]) if f.get("name")==name]
    if len(matching)!=1 or matching[0].get("is_link_only"):
        raise ValueError("Expected original single publication workbook unavailable")
    file=matching[0]
    url=file.get("download_url")
    if not url or urlparse(url).scheme!="https" or urlparse(url).hostname not in {
        "figshare.com","ndownloader.figshare.com","api.figshare.com"}:
        raise ValueError("No legitimate publisher-referenced file source")
    raw=download(url)
    digest=hashlib.sha256(raw).hexdigest()
    if pinned_sha and digest!=pinned_sha:
        raise ValueError("Source archive hash changed; do not analyze")
    header,rows=data_to_sparse_rows(raw,"xl/worksheets/sheet2.xml",FIELDS)
    if not REQUIRED.issubset(set(header)):
        raise ValueError("Required individual/provenance columns absent")
    return {"article_id":aid,"doi":md,"original_filename":name,
            "sha256":digest,"header_fields":header,"rows":rows}

def clean(x):
    return str(x or "").strip().casefold()

def summarize(a,b):
    """Only aggregate identifier/lineage counts; never emit source labels/IDs."""
    def keys(source,fields):
        return [tuple(clean(r.get(f)) for f in fields) for r in source["rows"]
                if all(clean(r.get(f)) for f in fields)]
    pair=("population","line")
    a_pairs=set(keys(a,pair));b_pairs=set(keys(b,pair))
    a_id=set(keys(a,("id",)));b_id=set(keys(b,("id",)))
    a_pid=set(keys(a,("population","id")));b_pid=set(keys(b,("population","id")))
    # ID equality across F1/F2 and F3 is not a pedigree relationship; never join.
    group_overlap=a_pairs & b_pairs
    out={
        "status":"SOURCE_ID_AND_LINE_LABELS_ONLY_NO_OUTCOMES",
        "source_articles":[a["article_id"],b["article_id"]],
        "source_shas":[a["sha256"],b["sha256"]],
        "2025_source_rows":len(a["rows"]),
        "2026_source_rows":len(b["rows"]),
        "2025_unique_id_labels":len(a_id),
        "2026_unique_id_labels":len(b_id),
        "2025_unique_population_id_labels":len(a_pid),
        "2026_unique_population_id_labels":len(b_pid),
        "exact_id_label_overlap_across_generations":len(a_id&b_id),
        "exact_population_id_label_overlap_across_generations":len(a_pid&b_pid),
        "2025_unique_population_line_categories":len(a_pairs),
        "2026_unique_population_line_categories":len(b_pairs),
        "shared_population_line_category_count":len(group_overlap),
        "direct_maternal_lineage_link_confirmed":False,
        "same_individual_cross_year_link_confirmed":False,
        "snp_genotypes_read":False,
        "outcome_columns_read":False,
        "phenotype_values_read":False,
        "raw_data_exported":False,
        "independent_original_programmes_count":1,
        "decision":"SOURCE_PEDIGREE_CROSSWALK_REQUIRED_BEFORE_ANY_CROSS_YEAR_EFFECT"
    }
    return out

def main():
    from urllib.error import HTTPError,URLError
    try:
        a,b=(verified_source(s) for s in SOURCES)
        res=summarize(a,b)
    except (HTTPError,URLError,ValueError,KeyError,TypeError,IndexError) as e:
        res={"status":"SOURCE_ID_GATE_STOP","error_type":type(e).__name__,
             "snp_genotypes_read":False,"outcome_columns_read":False,
             "phenotype_values_read":False,"raw_data_exported":False,
             "direct_maternal_lineage_link_confirmed":False,
             "decision":"SOURCE_ACCESS_OR_SCHEMA_STOP"}
        if isinstance(e,HTTPError): res["http_status"]=e.code
    print(json.dumps(res,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
