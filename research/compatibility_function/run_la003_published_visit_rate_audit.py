#!/usr/bin/env python3
"""LA003: original-source numerical visit-unit audit against Layman 2017 Table 2.

Source-only audit. No field-plant seed/fitness outcome, alleles, genotypes or
original insect/plant records are written to outputs. A current original Dryad
ZIP is required locally; GitHub CI uses source-withheld invariants only.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
from statistics import fmean
from zipfile import ZipFile

from run_leavenworthia_LA001 import SOURCE_SHA, SITES, sheets, value

PUBLISHED_VISITS = 3748
PUBLISHED_PERIODS = 121
# Published Table 2 total rows sometimes differ by .001 from rounded sums.
PUBLISHED_TOTAL_RATES = {2014: {"SI": 2.008, "SC": 2.245},
                         2015: {"SI": 1.068, "SC": 1.167}}
PUBLISHED_RATES = {
    2014: {"SI": {"AH": 1.479, "BF": .060, "F": .233, "Other": .236},
           "SC": {"AH": 1.678, "BF": .080, "F": .191, "Other": .297}},
    2015: {"SI": {"AH": .428, "BF": .184, "F": .400, "Other": .056},
           "SC": {"AH": .504, "BF": .204, "F": .405, "Other": .055}},
}


def source_period_rate(n_position_tokens: int, n_open_flowers: float) -> float:
    """A 30-minute observed rate per open flower per hour, no imputation."""
    if n_position_tokens < 0 or n_open_flowers <= 0:
        raise ValueError("Rate undefined for negative visits or no open flowers")
    return 2 * n_position_tokens / n_open_flowers


def audit(source: Path) -> dict:
    if hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA:
        raise ValueError("Wrong original Dryad archive SHA256")
    result = {}
    all_events = Counter()
    all_positions = Counter()
    total = Counter()
    site_receipts = []
    with ZipFile(source) as outer:
        if outer.testzip() is not None:
            raise ValueError("Original Dryad ZIP CRC failed")
        for year in (2014, 2015):
            wb = sheets(outer, f"Pollinator+Data+{year}.xlsx")
            case_events, case_positions = Counter(), Counter()
            year_count = Counter()
            per_group_rate = defaultdict(list)
            for site in SITES:
                tab = wb["Quarry Array" if year == 2014 and site == "Quarry" else site]
                genotypes = {
                    i: value(tab[3 if year == 2014 else 2], i + 6)
                    for i in range(1, 33)
                }
                if Counter(genotypes.values()) != Counter({"SC": 16, "SI": 16}):
                    raise ValueError("Unexpected array genotype header")
                periods = []
                for row_no, row in sorted(tab.items()):
                    event_id, taxon = value(row, 5), value(row, 6)
                    if isinstance(event_id, str) and event_id.strip().lower() == "open flowers":
                        periods.append({"flower": [value(row, c) for c in range(7, 39)],
                                        "events": [], "total": None})
                    elif isinstance(event_id, str) and event_id.strip().lower() == "total":
                        if periods:
                            periods[-1]["total"] = taxon
                    elif periods and isinstance(taxon, str) and taxon.strip() and (
                        isinstance(event_id, (int, float)) or str(event_id).isdigit()
                    ):
                        positions = []
                        for c in range(7, 200):
                            token = value(row, c)
                            if token is None:
                                continue
                            if not isinstance(token, (float, int)) or int(token) != token:
                                raise ValueError("Unexpected noninteger source plant position")
                            positions.append(int(token))
                        periods[-1]["events"].append((taxon, positions))
                complete = [p for p in periods if p["total"] is not None]
                if any(p["events"] for p in periods if p["total"] is None):
                    raise ValueError("Unfinished period contains insect event")
                year_count["open_flower_rows"] += len(periods)
                year_count["complete_periods"] += len(complete)
                site_visits = 0
                site_events = 0
                for period in complete:
                    token_count = sum(len(seq) for _, seq in period["events"])
                    if not isinstance(period["total"], (int, float)) or int(period["total"]) != token_count:
                        raise ValueError("Original source TOTAL does not match position-token count")
                    year_count["event_rows"] += len(period["events"])
                    year_count["position_tokens"] += token_count
                    year_count["dedup_positions_per_event"] += sum(
                        len(set(seq)) for _, seq in period["events"]
                    )
                    site_events += len(period["events"])
                    site_visits += token_count
                    group_counts = {"SI": Counter(), "SC": Counter()}
                    for raw_code, sequence in period["events"]:
                        case_events[raw_code] += 1
                        case_positions[raw_code] += len(sequence)
                        all_events[raw_code] += 1
                        all_positions[raw_code] += len(sequence)
                        category = raw_code.upper()
                        if category not in ("AH", "BF", "F"):
                            category = "Other"
                        for pos in sequence:
                            if not 1 <= pos <= 32:
                                year_count["outside_position_1to32"] += 1
                                continue
                            year_count["in_range_position_tokens"] += 1
                            open_flower_n = period["flower"][pos - 1]
                            if open_flower_n is None or open_flower_n <= 0:
                                year_count["visits_to_position_with_zero_open_flower"] += 1
                            group_counts[genotypes[pos]][category] += 1
                    for genotype in ("SI", "SC"):
                        open_n = sum(
                            period["flower"][pos - 1] or 0
                            for pos in range(1, 33) if genotypes[pos] == genotype
                        )
                        if open_n <= 0:
                            continue
                        for category in ("AH", "BF", "F", "Other"):
                            per_group_rate[(genotype, category)].append(
                                source_period_rate(group_counts[genotype][category], open_n)
                            )
                        per_group_rate[(genotype, "Total")].append(
                            source_period_rate(sum(group_counts[genotype].values()), open_n)
                        )
                site_receipts.append({
                    "year": year, "site": site,
                    "completed_periods": len(complete),
                    "source_event_rows": site_events,
                    "source_position_tokens": site_visits,
                })
            if year_count["complete_periods"] != (45 if year == 2014 else 76):
                raise ValueError("Completed source periods no longer match 2014/15 source")
            out = {"source_counts": dict(year_count),
                   "case_sensitive_event_rows": dict(sorted(case_events.items())),
                   "case_sensitive_position_tokens": dict(sorted(case_positions.items())),
                   "rates": {}}
            for genotype in ("SI", "SC"):
                r = {}
                for category in ("AH", "BF", "F", "Other", "Total"):
                    observed = fmean(per_group_rate[(genotype, category)])
                    paper = (PUBLISHED_TOTAL_RATES[year][genotype]
                             if category == "Total" else PUBLISHED_RATES[year][genotype][category])
                    r[category] = {
                        "source_position_token_rate_mean": observed,
                        "published_table2_rate": paper,
                        "difference_source_minus_published": observed - paper,
                        "source_nonzero_flower_periods": len(per_group_rate[(genotype, category)]),
                    }
                out["rates"][genotype] = r
            result[str(year)] = out
            total.update(year_count)
    # Fail closed on fixed, source-only full periods/event/position denominators.
    if tuple(total.get(k, 0) for k in (
        "complete_periods", "event_rows", "position_tokens", "in_range_position_tokens",
        "visits_to_position_with_zero_open_flower", "outside_position_1to32"
    )) != (121, 2850, 6702, 6701, 38, 1):
        raise ValueError("Source visit-unit denominators do not match original archive")
    return {
        "analysis": "LA003_source_only_published_visit_unit_audit",
        "status": "PARTIAL_RATE_RECONSTRUCTION_WITH_UNRESOLVED_TOTAL_VISIT_UNITS",
        "source_archive_sha256": SOURCE_SHA,
        "published_paper_doi": "10.1111/evo.13167",
        "published_paper_figure": "Table 2",
        "paper_reported_visits": PUBLISHED_VISITS,
        "paper_reported_half_hour_periods": PUBLISHED_PERIODS,
        "source_counting_units": dict(total),
        "years": result,
        "site_year_aggregate": site_receipts,
        "raw_2014_Bf_and_BF_codes_not_assumed_taxonomically_distinct": True,
        "code_note": "main.cpp, Individual.h, Locus.h are population-genetic simulation code; no published Table 2 source cleaning script.",
        "no_raw_plant_records_exported": True,
        "claim_boundary": [
            "Original source per-period per-flower rates partly reproduce published Table 2.",
            "The published total 3748 is neither raw 2850 insect rows, 6702 tokens, nor 5064 event-wise distinct plant-position entries.",
            "Some 2014 Bf/BF classification and original inclusion rules remain unclear.",
            "This is only a measurement provenance audit, not a new ecological or seed-production test.",
            "Prior LA001/LA002 negative whole-site results are NOT revised."
        ]
    }


def main() -> None:
    a = argparse.ArgumentParser()
    a.add_argument("--source-zip", type=Path, required=True)
    a.add_argument("--output", type=Path, required=True)
    args = a.parse_args()
    result = audit(args.source_zip)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"], "n_source": result["source_counting_units"],
        "source_2014_SC_all_rate": result["years"]["2014"]["rates"]["SC"]["Total"]["source_position_token_rate_mean"],
        "paper_2014_SC_all_rate": result["years"]["2014"]["rates"]["SC"]["Total"]["published_table2_rate"],
    }, indent=2))


if __name__ == "__main__":
    main()
