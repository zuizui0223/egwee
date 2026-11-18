#!/usr/bin/env python3
"""Stage B source key/taxon coverage gate, BEFORE estimating JSD outcomes."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import estimate_guild_partition as e


def audit():
    nets, row_counts, study_ids=e.harvest()
    programmes={e.programme_of(s) for s in study_ids}
    methods=Counter()
    method_ambiguous=0
    counts_condition=0
    for data in nets.values():
        if len(data["methods"])!=1 or "" in data["methods"]:
            method_ambiguous+=1
            continue
        methods[next(iter(data["methods"]))]+=1
        plants=data["guild_plant_counts"]
        bee=sum(x[0] for x in plants.values())
        hover=sum(x[1] for x in plants.values())
        if len(plants)>=3 and bee>=20 and hover>=20:
            counts_condition+=1
    return {
        "status":"SOURCE_KEY_AND_GUILD_IDENTITY_PASS",
        "source_study_identifiers":len(study_ids),
        "source_programme_labels_after_23_24_25_dedup":len(programmes),
        "site_year_network_key_count":len(nets),
        "network_keys_with_ambiguous_method":method_ambiguous,
        "network_keys_eligible_by_frozen_20_20_3_coverage_only":counts_condition,
        "source_original_sample_rows":row_counts["source_interaction_rows"],
        "source_row_count_detail":dict(row_counts),
        "sampling_method_network_count":dict(sorted(methods.items())),
        "JSD_effect_or_sign_computed":False,
        "raw_rows_redistributed":False,
        "source_sha":e.EXPECTED_FILE_SHA256,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.self_test:
        assert e.year_of("2017-04-06")==2017
        assert e.programme_of("23_X")==e.programme_of("25_Y")
        assert e.programme_of("26_Z")!=e.programme_of("25_Y")
        print("EUPPOLLNET_SOURCE_KEYS_SYNTHETIC_PASS")
        return 0
    if a.output is None:
        p.error("--output required")
    result={"phase":"source_ID_and_guild_coverage_only"}
    try:
        result.update(audit())
    except Exception as err:
        result["status"]="SOURCE_KEY_STOP"
        result["reason"]=type(err).__name__+": "+str(err)[:400]
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("EUPPOLLNET_SOURCE_KEY_GATE "+json.dumps(result,sort_keys=True),flush=True)
    return 0 if result["status"]=="SOURCE_KEY_AND_GUILD_IDENTITY_PASS" else 1


if __name__=="__main__":
    sys.exit(main())
