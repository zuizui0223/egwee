#!/usr/bin/env python3
"""Source-only reconciliation of CAMP01 56 pollinator rows vs 53 published populations.
Only identifier/metadata counts; no seed or visit numeric values are interpreted.
"""
from collections import Counter, defaultdict
import hashlib,json
from run_camp01_fixed_site_holdout import REC,DOI,FILES,fetch,csvrows,key,design,norm,Stop

def audit(seed,poll):
    def collect(rows):
        out=defaultdict(list)
        for r in rows:out[key(r)].append(r)
        return out
    s,p=collect(seed),collect(poll)
    common=set(s)&set(p)
    conflicts=0; dates_same=0; dates_different=0;dates_absent=0
    for k in common:
        a={design(r) for r in s[k]};b={design(r) for r in p[k]}
        if len(a)!=1 or a!=b:conflicts+=1
        sd={r.get("date_initiated","").strip() for r in s[k]}-{""}
        pd={r.get("start_date","").strip() for r in p[k]}-{""}
        if not sd or not pd:dates_absent+=1
        elif sd==pd:dates_same+=1
        else:dates_different+=1
    plants=defaultdict(set)
    for r in seed:
        if r.get("individual"):
            plants[(key(r),r["individual"])].add(norm(r["treatment"]))
    paired={k for (k,i),t in plants.items() if t=={"c","s"} or t=={"control","supplemented"}}
    class_counts=Counter()
    for k in set(p)-set(s):
        for r in p[k]:class_counts["/".join(design(r)[1:])]+=1
    return {
        "status":"CAMP01_SOURCE_DESIGN_ONLY",
        "seed_rows":len(seed),"pollinator_rows":len(poll),
        "seed_unique_experimental_population_site_keys":len(s),
        "pollinator_unique_experimental_population_site_keys":len(p),
        "seed_sites":len({k[0] for k in s}),
        "pollinator_sites":len({k[0] for k in p}),
        "matched_experimental_population_site_keys":len(common),
        "matched_sites":len({k[0] for k in common}),
        "seed_only_keys":len(set(s)-set(p)),
        "pollinator_only_keys":len(set(p)-set(s)),
        "pollinator_duplicate_keys":sum(len(r)>1 for r in p.values()),
        "matched_design_conflicts":conflicts,
        "matched_date_strings_same":dates_same,
        "matched_date_strings_different":dates_different,
        "matched_date_strings_absent":dates_absent,
        "seed_treatment_labels":sorted({norm(r["treatment"]) for r in seed}),
        "plant_key_count":len(plants),
        "plant_keys_with_both_treatment_labels":sum(t in ({"c","s"},{"control","supplemented"}) for t in plants.values()),
        "population_keys_with_both_labels_on_same_plant":len(paired),
        "matched_population_keys_with_both_labels_on_same_plant":len(common&paired),
        "pollinator_only_counts_by_autonomy_size":dict(class_counts),
        "raw_rows_exported":False,"outcome_values_interpreted":False,
        "new_model_fitted":False,
        "treatment_code_mapping_verified":False,
        "original_53_inclusion_set_verified":False,
    }

def run():
    try:
        meta=json.loads(fetch("https://zenodo.org/api/records/"+REC,2_000_000))
        if str(meta.get("id"))!=REC or meta.get("doi")!=DOI:raise Stop("SOURCE_ID_MISMATCH")
        mf={f.get("key"):f for f in meta.get("files",[])}
        if set(mf)!=set(FILES):raise Stop("FILE_INVENTORY_CHANGED")
        tabs={};hashes={}
        for fn,md5 in FILES.items():
            links=mf[fn].get("links",{})
            url=links.get("content") or links.get("self")
            raw=fetch(url,2_000_000)
            if hashlib.md5(raw).hexdigest()!=md5:raise Stop("MD5_MISMATCH")
            headers,tabs[fn]=csvrows(raw);hashes[fn]=hashlib.sha256(raw).hexdigest()
        d=audit(tabs["PLdataindividual.csv"],tabs["pollinator.csv"])
        d["source_sha256"]=hashes
        return d
    except Exception as e:
        return {"status":"CAMP01_SOURCE_DESIGN_STOP","reason":str(e) if isinstance(e,Stop) else type(e).__name__,"raw_rows_exported":False,"outcome_values_interpreted":False,"new_model_fitted":False}
if __name__=="__main__":print(json.dumps(run(),indent=2))
