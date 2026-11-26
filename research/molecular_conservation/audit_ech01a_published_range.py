#!/usr/bin/env python3
"""ECH01A source range diagnostic; no reproductive outcomes inspected or fitted."""
import json,math,hashlib
from collections import Counter
from audit_echinacea_author_semantics import official_drum,pinned,rows
from audit_echinacea_longterm_sources import HANDLES
from run_ech01a_maternal_holdout import HASHES,ismiss,clean
def run():
    d={"status":"SOURCE_RANGE_DIAGNOSTIC_PENDING","no_outcome_values_examined":True,"no_model_fitted":True,"raw_records_exported":False}
    try:
        f=official_drum(HANDLES["ECH01"])
        p=rows(pinned(f,"fitness_predictors.csv",HASHES["fitness_predictors.csv"]))
        r=[x for x in p if not ismiss(x["parentDist"])]
        if len(p)!=438 or len(r)!=436:raise ValueError("cohort mismatch")
        dist=[float(x["parentDist"]) for x in r];delta=[float(x["diffStartDir"]) for x in r]
        if not all(math.isfinite(v) for v in dist+delta):raise ValueError("nonfinite")
        d.update(status="SOURCE_RANGE_DIAGNOSTIC_COMPLETE",n=len(r),
                 source_distance_range_m=[min(dist),max(dist)],
                 source_signed_difference_range_days=[min(delta),max(delta)],
                 distance_above_published_rounded_maximum=sum(x>9014 for x in dist),
                 distance_below_zero=sum(x<0 for x in dist),
                 distance_outside_round_to_integer_9014=sum(round(x)>9014 or x<0 for x in dist),
                 signed_difference_outside_published_range=sum(not -13<=x<=12 for x in delta),
                 signed_difference_not_integer=sum(x!=int(x) for x in delta),
                 fruit_position_category_counts=dict(Counter(clean(x["ach_pos"]) for x in r)))
    except Exception as e:d.update(status="SOURCE_RANGE_DIAGNOSTIC_STOP",reason=type(e).__name__)
    return d
if __name__=="__main__":print(json.dumps(run(),indent=2))
