#!/usr/bin/env python3
"""ECH02: author-defined focal circle join and follow-up coverage only."""
from collections import Counter,defaultdict
import json,re,math
from audit_echinacea_author_semantics import official_drum,pinned,rows
from audit_echinacea_longterm_sources import HANDLES
HASHES={"mating_potential.csv":"495635aa8c822ab8a251f9f6375e9f8d847ef9dc9b017b64d3becebda9a12193",
"seedling_demography.csv":"5d305c5742e894b03d9f88a77f0c5095f066a8a1d3612124a6a0e80410a062c6",
"readme.txt":"df234c2369cd669a5d1314a9c433f00893dcb040334fee848366cce8a5c0db3b",
"aster_analysis.R":"a705ea419a08e37bee863a16b7bf901f877fe87e4251c414a001f34bd738b143"}
MISS={"","na","nan","none","null"}
def c(v):return str(v if v is not None else "").strip()
def missing(v):return c(v).lower() in MISS
def integer(v):
    try:x=float(c(v))
    except ValueError:return None
    return int(x) if math.isfinite(x) and x==int(x) else None
def audit(m,s):
    if len(m)!=1278 or len(s)!=11321:raise ValueError("source counts changed")
    mp={c(r["focalCd"]):r for r in m}
    if len(mp)!=len(m) or any(missing(k) for k in mp):raise ValueError("focalCd not unique")
    groups=defaultdict(list)
    for r in s:
        if missing(r["focalCd"]) or missing(r["slingCd"]):raise ValueError("missing focal/seedling key")
        groups[c(r["focalCd"])].append(r)
    common=set(mp)&set(groups)
    seedids=defaultdict(set)
    pairkeys=Counter()
    mismatches=Counter()
    age_status=defaultdict(Counter)
    for r in s:
        k=c(r["focalCd"]); sid=c(r["slingCd"]);cohort=integer(r["slingYr"]);year=integer(r["year"])
        seedids[sid].add((k,cohort));pairkeys[(sid,year)]+=1
        if cohort is None or year is None:mismatches["missing_or_invalid_year"]+=1;continue
        age=year-cohort
        if age<0:mismatches["negative_age"]+=1
        if k in mp:
            if integer(mp[k]["year"])!=cohort-1:mismatches["joined_rows_mating_year_not_cohort_minus_one"]+=1
            if c(mp[k]["site"])!=c(r["site"]):mismatches["joined_rows_literal_site_disagreement"]+=1
            # Report observed records only. A missing follow-up is not a death.
            if age in (0,7,8):
                ld=integer(r["newLD"])
                age_status[age]["observed_records"]+=1
                if ld in (0,1):age_status[age]["known_alive_status"]+=1
                else:age_status[age]["unknown_alive_status"]+=1
                if ld==1:age_status[age]["alive"]+=1
    circ=Counter()
    for k,r in mp.items():
        n=integer(r["slingCt"])
        if n is None or n<0:circ["missing_or_invalid_source_emergence_count"]+=1;continue
        ids={c(x["slingCd"]) for x in groups.get(k,[])}
        circ["source_emergence_count_equals_tracked_ids"]+=int(n==len(ids))
        circ["source_emergence_count_differs_from_tracked_ids"]+=int(n!=len(ids))
        if not ids:
            circ["no_tracked_seedling_source_slingCt_zero" if n==0 else "no_tracked_seedling_source_slingCt_positive"]+=1
    return {"mating_bouts":len(m),"seedling_records":len(s),"unique_seedling_ids":len(seedids),
            "seedling_ids_with_conflicting_circle_or_cohort":sum(len(v)!=1 for v in seedids.values()),
            "duplicate_seedling_observation_year_keys":sum(n>1 for n in pairkeys.values()),
            "unique_seedling_circles":len(groups),"matched_circles":len(common),
            "mating_only_circles":len(set(mp)-set(groups)),"seedling_only_circles":len(set(groups)-set(mp)),
            "matched_seedling_rows":sum(len(groups[k]) for k in common),
            "site_label_count_mating":len({c(r["site"]) for r in m}),
            "joined_mismatch_counts":dict(mismatches),"circle_emergence_coverage":dict(circ),
            "age_followup_observed_only":{str(k):dict(v) for k,v in age_status.items()}}
def run():
    d={"status":"SOURCE_GATE_PENDING","raw_records_exported":False,"model_fitted":False,
       "missing_followup_imputed":False,"original_author_code_executed":False}
    try:
        entries=official_drum(HANDLES["ECH02"])
        raw={k:pinned(entries,k,v) for k,v in HASHES.items()}
        code=raw["aster_analysis.R"].decode("utf-8-sig")
        doc=raw["readme.txt"].decode("utf-8-sig")
        if "by = 'focalCd'" not in code or "year prior to the seedling search year" not in doc:
            raise ValueError("author key semantics unavailable")
        d["source_sha256"]=HASHES
        d.update(audit(rows(raw["mating_potential.csv"]),rows(raw["seedling_demography.csv"])))
        # Only scalar author age settings, no location labels.
        d["author_max_age_settings"]=re.findall(r"(?m)^\s*max\.age\s*(?:<-|=)\s*(\d+)",code)
        d["status"]="SOURCE_FOCAL_JOIN_AUDITED"
    except Exception as e:d.update(status="SOURCE_STOP",reason=type(e).__name__)
    return d
if __name__=="__main__":print(json.dumps(run(),indent=2))
