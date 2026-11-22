#!/usr/bin/env python3
"""CP003 immutable CropPol field-versus-taxonomic sampling effort cross-grain audit.

Zero ecological correlations or fitted models. Source sample rows describe
pollinator taxa/methods and MUST NOT be summed as independent sampling sites.
All identifiers, dates, raw predictor magnitudes, outcomes and free text stay
only in memory; printed/artifact JSON is aggregate-only.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
from decimal import Decimal
import hashlib
from http.client import HTTPException
import io
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request,build_opener

import audit_cp001_source_coverage as cp001
import audit_cp002_measurement_sources as cp002

SAMPLE_PIN={
 "repo":"ibartomeus/CropPol",
 "commit":"febec7dcc088ccf1bd721c41ce8dda87a2dcba1a",
 "path":"Final_Data/CropPol_sampling_data.csv",
 "size":22084522,
 "blob":"b7ab3fd92da0be5e8ec41b6ada50c2da7d4756c2",
 "sha256":"aafba5d3dfbab2c93f3a60e31181d2c5b33535cc2c8f33b85495facb42382f30",
}
SAMPLE_PIN["url"]="https://raw.githubusercontent.com/"+SAMPLE_PIN["repo"]+"/"+SAMPLE_PIN["commit"]+"/"+SAMPLE_PIN["path"]
SAMPLING_HEADER=(
 "study_id","site_id","sampling_method","pollinator","identified_to","guild",
 "abundance","total_sampled_area","total_sampled_time","total_sampled_flowers",
 "description","notes",
)
EFFORT_FIELDS=("total_sampled_time","total_sampled_area","total_sampled_flowers")
FRAMES=("all_fields","strict_direct_timed_visit","strict_harvest_mass_area")
EXPECTED={"all_fields":3448,"strict_direct_timed_visit":452,"strict_harvest_mass_area":121}

def norm(s):
    return cp002.norm(s)
def missing(s):
    return cp001.is_missing(s)
def value(s):
    return cp002.number(s)

def verify_sample_bytes(raw):
    actual=cp001.verify_bytes(raw,SAMPLE_PIN["size"],SAMPLE_PIN["blob"])
    if actual!=SAMPLE_PIN["sha256"]:
        raise cp001.SourceIdentityError("Pinned published sampling SHA256 mismatch")
    return actual

def fetch_sample():
    req=Request(SAMPLE_PIN["url"],headers={"User-Agent":"egwee-cp003-pinned-sampling-effort-20261122/1.0"})
    with build_opener(cp001.PinnedSourceRedirectHandler()).open(req,timeout=65) as resp:
        if resp.geturl()!=SAMPLE_PIN["url"] or urlparse(resp.geturl()).scheme!="https":
            raise cp001.SourceIdentityError("Pinned original sampling URL redirected")
        data=resp.read(SAMPLE_PIN["size"]+1)
    verify_sample_bytes(data)
    return data

def tabular_rows(raw,expected):
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""),restkey="_extra",restval="")
    if tuple(reader.fieldnames or ())!=expected:raise ValueError("Source header differs from immutable original")
    for row in reader:
        if not row:continue
        if "_extra" in row or any(k not in row for k in expected):
            raise ValueError("Malformed source row width")
        yield row

class SampleSummary:
    __slots__=("n","methods","missing_method","status")
    def __init__(self):
        self.n=0
        self.methods=set()
        self.missing_method=0
        self.status={f:{"positive":set(),"n_missing":0,"n_zero":0,"n_negative":0,"n_invalid":0} for f in EFFORT_FIELDS}
    def add(self,row):
        self.n+=1
        method=norm(row["sampling_method"])
        if missing(method):self.missing_method+=1
        else:self.methods.add(method)
        for f in EFFORT_FIELDS:
            s=row[f]
            st=self.status[f]
            if missing(s):st["n_missing"]+=1;continue
            n=value(s)
            if n is None:st["n_invalid"]+=1
            elif n<0:st["n_negative"]+=1
            elif n==0:st["n_zero"]+=1
            else:st["positive"].add(n)
    def tier(self,field):
        st=self.status[field]
        if st["n_invalid"] or st["n_negative"] or st["n_zero"] or len(st["positive"])!=1:
            return "not_unique_positive"
        if len(self.methods)!=1 or self.missing_method>0:
            return "method_ambiguous"
        if st["n_missing"]:return "possible_partial_only"
        return "unique_complete"
    def unique_number(self,field):
        st=self.status[field]
        return next(iter(st["positive"])) if len(st["positive"])==1 else None

def sampling_summary(raw,expected_rows=54191):
    sampling={}
    n=0
    miss_key=0
    valid_abundance=0
    for row in tabular_rows(raw,SAMPLING_HEADER):
        n+=1
        k=(row["study_id"].strip(),row["site_id"].strip())
        if any(missing(x) for x in k):
            miss_key+=1
            continue
        if k not in sampling:sampling[k]=SampleSummary()
        sampling[k].add(row)
        a=value(row["abundance"])
        valid_abundance+=a is not None and a>=0
    if n!=expected_rows:raise ValueError("Original sampling row count drift")
    return sampling,{"sampling_taxon_method_rows":n,
                     "rows_missing_study_site_key":miss_key,
                     "nonnegative_numeric_taxon_abundance_rows":valid_abundance,
                     "distinct_complete_sampling_site_keys":len(sampling),
                     "same_taxon_row_not_independent_census_or_field":True}

def field_frames(raw,expected=(3448,452,121)):
    rows=list(tabular_rows(raw,tuple(cp001.EXPECTED_COLUMNS)))
    if len(rows)!=expected[0]:raise ValueError("Original field row count drift")
    for i,row in enumerate(rows):
        row["_group"]=(("observed",row["study_id2"]) if not missing(row["study_id2"])
                       else ("unresolved",str(i)))
    components,_=cp002.source_components(rows,set(cp002.RULES["vetted_original_dois"]))
    keys=Counter((r["study_id"].strip(),r["site_id"].strip()) for r in rows)
    all_rows=[]
    strict=[]
    harvest=[]
    for r in rows:
        r["_component"]=components[r["_group"]]
        k=(r["study_id"].strip(),r["site_id"].strip())
        all_rows.append((k,r))
        # Precisely match CP002 strict frame definitions (no outcome signs).
        attrs=("study_id","study_id2","site_id","sampling_year","crop")
        complete=all(not missing(r[f]) for f in attrs)
        yf=cp002.endpoint("yield_units",r["yield_units"])
        direct=complete and cp002.number(r["yield"]) is not None and yf in cp002.DIRECT
        y=cp002.number(r["yield"])
        if direct and y<0:direct=False
        if direct and norm(r["yield_units"]) in cp002.RULES["primary_true_percentage_labels"] and y>100:
            direct=False
        v=cp002.number(r["visitation_rate"])
        timed_unit=cp002.RULES["visit_units"].get(norm(r["visitation_rate_units"]),{}).get("timed",False)
        method=cp002.safe_label("visit_methods",r["sampling_visitation"])
        taxa=cp002.safe_label("taxa_scopes",r["taxa_recorded"])
        selected=(direct and v is not None and v>=0 and timed_unit
                  and method=="active_observation_compatible"
                  and taxa not in ("missing","unresolved","none")
                  and cp002.safe_label("selectors",r["use_visits_or_abundance"])=="use_visits")
        if selected:
            strict.append((k,r))
            if yf=="harvest_mass_area":harvest.append((k,r))
    if (len(all_rows),len(strict),len(harvest)) != expected:
        raise ValueError("CP002 source admission frame changed; no row imputation allowed")
    return {"all_fields":all_rows,
            "strict_direct_timed_visit":strict,
            "strict_harvest_mass_area":harvest},keys

def global_sampling_quality(sampling,fieldkey_counts):
    tall=Counter()
    sample_rows=Counter()
    for k,s in sampling.items():
        sample_rows["all_sample_taxon_rows_complete_key"]+=s.n
        nc=fieldkey_counts.get(k,0)
        label="unmatched" if nc==0 else "year_ambiguous" if nc>1 else "unique_one_field"
        tall["keys_"+label]+=1
        sample_rows["taxon_rows_"+label]+=s.n
        if s.n>1:tall["keys_with_repeated_taxon_or_method_rows"]+=1
        if len(s.methods)>1:tall["keys_with_multiple_observation_method_labels"]+=1
        if s.missing_method:tall["keys_with_missing_sampling_method_rows"]+=1
        for f in EFFORT_FIELDS:
            st=s.status[f]
            tall[f+"_keys_"+s.tier(f)]+=1
            if len(st["positive"])>1:tall[f+"_keys_conflicting_positive_values"]+=1
            if st["n_missing"]:tall[f+"_keys_with_some_missing"]+=1
            if st["n_zero"]:tall[f+"_keys_with_some_explicit_zero"]+=1
            if st["n_negative"] or st["n_invalid"]:tall[f+"_keys_with_invalid_effort"]+=1
    return {"keys":dict(sorted(tall.items())),
            "rows":dict(sorted(sample_rows.items())),
            "original_source_effort_repeated_taxa_never_summed":True}

def source_frame_summary(pairs,fullkeys,sampling):
    count=Counter()
    groups={}
    for k,r in pairs:
        component=r["_component"]
        count["source_field_rows"]+=1
        groups[component]=1
        old_rows=fullkeys[k]
        if old_rows!=1:
            count["field_rows_with_shared_study_site_multiple_year_or_other_field"]+=1
            continue
        count["field_rows_unique_study_site_across_full_source"]+=1
        s=sampling.get(k)
        if s is None:
            count["field_rows_no_source_sampling_key"]+=1
            continue
        count["field_rows_with_source_sampling_taxa"]+=1
        if s.n>1:count["field_rows_with_multitaxon_sampling_rows"]+=1
        if len(s.methods)!=1 or s.missing_method:count["field_rows_with_method_ambiguity"]+=1
        for f in EFFORT_FIELDS:
            t=s.tier(f)
            count[f+"_tier_"+t]+=1
            field_original=None if f=="total_sampled_flowers" else value(r[f])
            if f!="total_sampled_flowers":
                if field_original is not None and field_original>0:
                    count[f+"_field_original_positive"]+=1
                elif field_original is not None and field_original==0:
                    count[f+"_field_original_explicit_zero"]+=1
                elif field_original is not None and field_original<0:
                    count[f+"_field_original_negative"]+=1
                else:count[f+"_field_original_missing_or_invalid"]+=1
            if t=="unique_complete":
                count[f+"_unique_complete_sampling_effort"]+=1
                src_num=s.unique_number(f)
                if f!="total_sampled_flowers":
                    if field_original is None:
                        count[f+"_possible_new_field_effort_without_overwrite"]+=1
                    elif field_original>0 and field_original==src_num:
                        count[f+"_cross_table_exact_positive_concordant"]+=1
                    elif field_original>0 and field_original!=src_num:
                        count[f+"_cross_table_disagreement"]+=1
            elif t=="possible_partial_only":
                count[f+"_partial_source_only_not_recovered"]+=1
    return {"rows":len(pairs),
            "candidate_source_components":len(groups),
            "metadata_and_effort_counts":dict(sorted(count.items())),
            "source_matched_time_is_survey_effort_not_standing_flower_density":True,
            "recovered_effort_not_inserted_in_original_field_dataset":True}

def audit(field_raw,sampling_raw):
    cp001.verify_bytes(field_raw,cp001.MANIFEST["expected_bytes"],cp001.MANIFEST["expected_git_blob_sha1"])
    sha=verify_sample_bytes(sampling_raw)
    frames,fullkeys=field_frames(field_raw)
    sampling,sampling_info=sampling_summary(sampling_raw)
    sample_quality=global_sampling_quality(sampling,fullkeys)
    repeated_keys=sum(x>1 for x in fullkeys.values())
    out={
        "status":"EFFORT_SOURCE_KEYS_AUDITED_NOT_MODEL_ADMISSION",
        "source_pinned_commit":SAMPLE_PIN["commit"],
        "source_sampling_original_file_size":len(sampling_raw),
        "source_sampling_git_blob_sha1":SAMPLE_PIN["blob"],
        "source_sampling_sha256":sha,
        "source_field_original_sha256":hashlib.sha256(field_raw).hexdigest(),
        "source_sampling_header_fields":len(SAMPLING_HEADER),
        "original_sample":sampling_info,
        "original_field": {
            "rows":len(frames["all_fields"]),
            "distinct_full_field_study_site_keys":len(fullkeys),
            "keys_repeated_in_field_original_across_years_or_rows":repeated_keys,
            "field_original_rows_with_repeat_study_site_key":sum(v for v in fullkeys.values() if v>1),
        },
        "sampling_source_quality":sample_quality,
        "frames":{f:source_frame_summary(frames[f],fullkeys,sampling) for f in FRAMES},
        "all_counts_are_source_structure_not_biological_prediction":True,
        "independent_source_components_confirmed":False,
        "sampling_method_match_to_visitation_measure_confirmed":False,
        "plant_density_or_field_size_recovered_from_sampling":False,
        "numeric_outcomes_correlations_or_model_scores_computed":False,
        "raw_identifiers_taxa_methods_numeric_values_or_source_rows_redistributed":False,
        "decision":"ORIGINAL_EFFORT_MATCH_CANDIDATES_REQUIRE_METHOD_AND_YEAR_VALIDATION",
    }
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",required=True,type=Path)
    args=ap.parse_args()
    result={"status":"SOURCE_NOT_YET_RETRIEVED","model_admission":False,
       "raw_identifiers_taxa_methods_numeric_values_or_source_rows_redistributed":False}
    stage="field"
    try:
        field_raw=cp001.fetch_verified_source()
        stage="sampling"
        sample_raw=fetch_sample()
        stage="grain"
        result=audit(field_raw,sample_raw)
        code=0
    except (OSError,HTTPException,ValueError,UnicodeError,csv.Error) as ex:
        result.update(status="ORIGINAL_SOURCE_OR_GRAIN_STOP",
                      source_stop_stage=stage,
                      source_stop_type=type(ex).__name__,
                      model_admission=False)
        if isinstance(ex,HTTPError):result["source_stop_http"]=ex.code
        code=2
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    print("CP003_ORIGINAL_SAMPLING_EFFORT_AUDIT "+json.dumps({
       "status":result["status"],"sampling":result.get("original_sample"),
       "all_field_year_keys":result.get("original_field"),
       "frame_counts":result.get("frames"),
       "stop_type":result.get("source_stop_type"),
    },sort_keys=True),flush=True)
    return code

if __name__=="__main__":raise SystemExit(main())
