#!/usr/bin/env python3
"""Source-hashed, pre-outcome field-Q/F join audit for public Clarkia source.

The post-Dryad-blocker independent GitHub source is a *source-access feasibility
pilot*, not one of the six prospectively frozen Dryad sources and not a
confirmation of a Q/P/F effect. Never read seed counts or fit a response model.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import csv
import hashlib
from io import StringIO
import json
from pathlib import Path
from urllib.request import Request, urlopen

REPO = "jensculrich/urban_pollinator_occupancy_model"
COMMIT = "4f0b9d53b4901337e441d2d1dae0f2b31c6e8280"
URL_BASE = "https://raw.githubusercontent.com/" + REPO + "/" + COMMIT + "/"
SOURCES = {
  "flower_seed": (
    "pollen_limitation_experiment/data/clarkia_pollination_data_2022.csv",
    "24519badb45cb75f38169660f50ab3bc15a117a3", 200000),
  "plant_visitors": (
    "pollen_limitation_experiment/data/pollinator_data.csv",
    "ef6bdc4ee01d745af51186b4e3416db6360a1195", 1000000),
  "clarkia_visitation": (
    "pollen_limitation_experiment/data/clarkia_visitation.csv",
    "30adee5bc7d1bb8dcad22f5ec59e1bb871db23e9", 10000),
  "sites": (
    "data/land_cover_by_site_reduced.csv",
    "c421a2a2fc0a095ed5a49dbafee24357831ad111", 10000),
}

def fetch_rows(key: str):
    path, expected, max_bytes = SOURCES[key]
    request = Request(URL_BASE + path, headers={
       "User-Agent": "egwee-source-feasibility-audit/1.0",
       "Accept": "text/csv",
    })
    with urlopen(request, timeout=30) as response:
        data = response.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValueError("Unapproved source size")
    got = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    if got != expected:
        raise ValueError("Immutable original Git blob SHA mismatch: " + key)
    rows = list(csv.DictReader(StringIO(data.decode("utf-8-sig"), newline="")))
    if not rows:
        raise ValueError("Missing source records: " + key)
    return rows, got

def norm(x) -> str:
    return " ".join(str(x).strip().lower().split())

def run():
    rs = {}
    sha = {}
    for key in SOURCES:
        rs[key], sha[key] = fetch_rows(key)
    field = rs["flower_seed"]
    sites = {norm(r["site"]) for r in rs["sites"]}
    source_outcome_sites = {norm(r["SITE"]) for r in field}
    missing = sorted(source_outcome_sites - sites)
    if missing:
        raise ValueError("Reported Clarkia experimental sites missing original site list")

    # Only structural condition flags, field site and plant/flower treatment
    # identifier are inspected. SEEDS_PRODUCED, PL, PL_INDEX are never read.
    paired = defaultdict(list)
    outcome_row_unique = set()
    for r in field:
        site, pot, plant, flower_trt = (norm(r[k]) for k in
                                       ("SITE", "POT_NUMBER", "PLANT_NUMBER", "FLOWER_TREATMENT"))
        unique = (site, pot, plant, flower_trt)
        if unique in outcome_row_unique:
            raise ValueError("Duplicate source flower treatment key")
        outcome_row_unique.add(unique)
        if (norm(r["BOTH_FLOWERS_OPEN_AND_POLLEN_APPLIED"]) == "y"
            and norm(r["BOTH_CAPSULES_RECOVERED"]) == "y"):
            paired[(site,pot,plant)].append(flower_trt)
    structurally_paired = {
        k for k, v in paired.items() if sorted(v) == ["control", "treatment"]
    }
    seed_sites = {k[0] for k in structurally_paired}
    # Source year code 2 = calendar 2022, established in linked original R
    # prep code. Only visit *record detection*; no claim of effort-calibrated
    # floral visitation rate from capture counts.
    poll_2022 = [r for r in rs["plant_visitors"] if norm(r["YEAR"]) == "2"]
    direct = [r for r in poll_2022 if norm(r.get("PLANT_NETTED_FROM_SCI_NAME", ""))
              in {"clarkia amoena", "clarkia amoena douglas ex lindl."}]
    direct_sites = {norm(r["SITE"]) for r in direct}
    direct_matched = [r for r in direct if norm(r["SITE"]) in seed_sites]
    # Survey rounds 4 and 5 bracket the 2022 planted Clarkia experiment but
    # are not guaranteed exact observational days for the experimental plants.
    direct_near = [r for r in direct_matched if norm(r["SAMPLING_ROUND"]) in {"4","5"}]
    local_garden = rs["clarkia_visitation"]
    garden_sites = {norm(r["SITE"]) for r in local_garden}
    field_garden_overlap = garden_sites & seed_sites
    out = {
       "status": "SOURCE_EXACT_ORIGINAL_OBSERVATION_STRUCTURAL_GATE",
       "stage": "post-Dryad access-blocker provenance-first source pilot, NOT primary frozen 6",
       "original_public_source_repo": REPO,
       "pinned_original_source_commit": COMMIT,
       "original_file_blob_sha": sha,
       "original_pollen_limitation_rows": len(field),
       "original_seed_sites": len(source_outcome_sites),
       "source_landscape_sites": len(sites),
       "potentially_complete_control_and_supplement_paired_plants": len(structurally_paired),
       "sites_with_structurally_paired_plants": len(seed_sites),
       "field_pollinator_detection_rows_2022": len(poll_2022),
       "clarkia_focal_visitor_detection_rows_2022": len(direct),
       "clarkia_focal_visitor_sites_2022": len(direct_sites),
       "field_site_matched_clarkia_focal_detections_2022": len(direct_matched),
       "field_site_matched_clarkia_focal_detections_rounds_4_5": len(direct_near),
       "field_sites_with_focal_visitor_detections": len(seed_sites & direct_sites),
       "separate_clarkia_visitation_records": len(local_garden),
       "separate_clarkia_visitation_unique_site_labels": len(garden_sites),
       "separate_clarkia_visitation_same_site_overlap": len(field_garden_overlap),
       "source_observation_effort_verified_and_exposure_normalized": False,
       "individual_level_plant_to_visitor_ID_join_verified": False,
       "direct_stigma_pollen_provenance_P_measured": False,
       "outcome_seed_values_examined": False,
       "source_raw_rows_redistributed": False,
       "biological_effect_estimated": False,
    }
    if len(seed_sites & direct_sites) == 0:
        out["decision"] = "DIRECT_FLOWER_VISIT_SITE_COVERAGE_STOP"
    else:
        out["decision"] = "DIRECT_FLOWER_VISIT_SITE_COVERAGE_PRESENT_EXACT_EFFORT_AND_ID_UNVERIFIED"
    return out

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    x = run()
    a.output.write_text(json.dumps(x, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(x, indent=2))

if __name__ == "__main__":
    main()
