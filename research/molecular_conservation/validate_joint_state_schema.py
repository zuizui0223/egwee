#!/usr/bin/env python3
"""Fail-closed pre-outcome join-key contract for molecular × pollination × seed data.
Reads only supplied JSON schema manifests; never opens biological data tables.
"""
import argparse
import json
from pathlib import Path

REQUIRED = ("genetics", "interaction", "function")
KEYS = ("population_id", "mother_id", "year", "cohort_id")

def audit(doc):
    if doc.get("schema_version") != 1:
        return {"decision": "STOP_INVALID_MANIFEST"}
    layers = doc.get("layers", {})
    if not all(k in layers for k in REQUIRED):
        return {"decision": "STOP_MISSING_LAYER"}
    if any(not isinstance(layers[k].get("columns"), list) for k in REQUIRED):
        return {"decision": "STOP_MISSING_COLUMN_SCHEMA"}
    if any(not layers[k].get("original_sha256") for k in REQUIRED):
        return {"decision": "STOP_UNVERIFIED_SOURCE_PROVENANCE"}
    # All declared keys must be source-provided in each layer, never inferred from row order.
    common = set.intersection(*(set(layers[k]["columns"]) for k in REQUIRED))
    join = [k for k in KEYS if k in common]
    if not {"population_id", "year"}.issubset(join):
        return {"decision": "STOP_NO_SAME_POPULATION_YEAR", "common_keys": join}
    if not ("mother_id" in join or "cohort_id" in join):
        return {"decision": "STOP_NO_SHARED_MOTHER_OR_COHORT", "common_keys": join}
    if not doc.get("source_declares_key_semantics", False):
        return {"decision": "STOP_UNVERIFIED_KEY_SEMANTICS", "common_keys": join}
    if not doc.get("source_declares_temporal_order", False):
        return {"decision": "STOP_UNVERIFIED_TEMPORAL_ORDER", "common_keys": join}
    if not doc.get("outcome_observation_denominator_declared", False):
        return {"decision": "STOP_MISSING_OUTCOME_DENOMINATOR", "common_keys": join}
    return {"decision": "SCHEMA_ONLY_ELIGIBLE_FOR_ID_AUDIT", "common_keys": join,
            "note": "Not an empirical join, not a model fit, not a verified outcome."}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("manifest", type=Path)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    result = audit(json.loads(a.manifest.read_text()))
    if a.output:
        a.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
