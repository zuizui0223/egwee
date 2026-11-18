#!/usr/bin/env python3
"""LA004: source-internal insect-code glossary & bagged-control denominator audit.

Requires the SHA-pinned original user-supplied Dryad archive. Only outputs
aggregate category counts, rates and control completeness, never pollinator
event sequences, plant IDs, seeds from field plants or source Excel files.
It never refits LA001/LA002 predictive outcomes.
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

PAPER = {
    "source": "Layman et al. (2017) Evolution 71:884-897 Table 2",
    "total_visits": 3748, "n_periods": 121,
    "controls": 17,
    "2014_BF_rate": {"SI": 0.060, "SC": 0.080},
    "2014_Other_rate": {"SI": 0.236, "SC": 0.297},
    "visit_frequency_percent": {"AH": 46.7, "BF": 14.4, "F": 28.7, "Other": 10.2},
}
EXPECTED_GLOSSARY = (
    "F - Fly", "Bf - Bee Fly", "B - Butterfly",
    "H - Honey Bee", "AH - Adrenid / Halictid", "U - Unknown",
)


def audit(source: Path) -> dict:
    if hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA:
        raise ValueError("Dryad original ZIP SHA256 mismatch")
    all_rows = Counter()
    all_tokens = Counter()
    rate = defaultdict(list)
    source_sessions = Counter()
    with ZipFile(source) as archive:
        if archive.testzip() is not None:
            raise ValueError("Source ZIP CRC failure")
        w2014 = sheets(archive, "Pollinator+Data+2014.xlsx")
        w2015 = sheets(archive, "Pollinator+Data+2015.xlsx")
        glossary = tuple(value(w2014["Landersville Field - Temporal"][1], k) for k in range(6))
        if glossary != EXPECTED_GLOSSARY:
            raise ValueError("No literal original 2014 insect code glossary")
        for year, book in ((2014, w2014), (2015, w2015)):
            for site in SITES:
                name = "Quarry Array" if year == 2014 and site == "Quarry" else site
                sheet = book[name]
                first_row = 3 if year == 2014 else 2
                geno = {i: value(sheet[first_row], i + 6) for i in range(1, 33)}
                if Counter(geno.values()) != {"SC": 16, "SI": 16}:
                    raise ValueError("Source array is not 16 SC/16 SI")
                periods = []
                for rownum, row in sorted(sheet.items()):
                    label = value(row, 5)
                    category = value(row, 6)
                    if isinstance(label, str) and label.strip().lower() == "open flowers":
                        periods.append({
                            "open": [value(row, j) for j in range(7, 39)],
                            "events": [], "total": None,
                        })
                    elif isinstance(label, str) and label.strip().lower() == "total":
                        if periods:
                            periods[-1]["total"] = category
                    elif (periods and isinstance(category, str) and category.strip() and
                          (isinstance(label, (int, float)) or str(label).isdigit())):
                        seq = []
                        for col in range(7, 200):
                            x = value(row, col)
                            if x is None:
                                continue
                            if not isinstance(x, (int, float)) or int(x) != x:
                                raise ValueError("Unparseable source position")
                            seq.append(int(x))
                        periods[-1]["events"].append((category, seq))
                complete = [p for p in periods if p["total"] is not None]
                source_sessions[year] += len(complete)
                if any(p["events"] for p in periods if p["total"] is None):
                    raise ValueError("Incomplete period carries events")
                for period in complete:
                    if period["total"] != sum(len(seq) for _, seq in period["events"]):
                        raise ValueError("Source TOTAL differs from position tokens")
                    for taxon, seq in period["events"]:
                        all_rows[(year, taxon)] += 1
                        all_tokens[(year, taxon)] += len(seq)
                    if year != 2014:
                        continue
                    for genotype in ("SI", "SC"):
                        nflowers = sum(
                            period["open"][pos - 1] or 0
                            for pos in range(1, 33) if geno[pos] == genotype
                        )
                        if nflowers <= 0:
                            continue
                        positions = Counter()
                        for taxon, seq in period["events"]:
                            positions[taxon] += sum(
                                1 for pos in seq if pos in geno and geno[pos] == genotype
                            )
                        for label, taxes in (
                            ("bf_casefold", ("Bf", "BF")),
                            ("bf_strict_uppercase", ("BF",)),
                            ("other_casefold", ("B", "U", "L")),
                            ("other_plus_Bf", ("B", "U", "L", "Bf")),
                        ):
                            rate[(genotype, label)].append(
                                2 * sum(positions[t] for t in taxes) / nflowers
                            )
        controls = {}
        em = sheets(archive, "Emasculation+experiment.xlsx")
        for name, field_date, field_fruit in (
            ("Final pass", 1, 2),
            ("Fruit set first pass", None, 1),
        ):
            cases = [v for rno, v in em[name].items()
                     if rno > 1 and value(v, 0) == "Control"]
            controls[name] = {
                "n_source_controls": len(cases),
                "n_fruit_outcomes_present": sum(
                    value(case, field_fruit) is not None for case in cases
                ),
                "n_with_dates": (
                    sum(value(case, field_date) is not None for case in cases)
                    if field_date is not None else None
                ),
                "n_fruits": (
                    sum(value(case, field_fruit) == 1 for case in cases)
                    if name == "Final pass"
                    else sum(value(case, field_fruit) == "yes" for case in cases)
                ),
            }

    if source_sessions != {2014: 45, 2015: 76}:
        raise ValueError("Source period denominator changed")
    for key, expected in {
        (2014, "Bf"): (44, 205),
        (2014, "BF"): (3, 4),
        (2014, "B"): (7, 34),
        (2015, "BF"): (85, 780),
    }.items():
        if (all_rows[key], all_tokens[key]) != expected:
            raise ValueError("Raw case-sensitive visitor counts changed")
    if any(x["n_source_controls"] != 21 or
           x["n_fruit_outcomes_present"] != 21 or
           x["n_fruits"] != 1 for x in controls.values()):
        raise ValueError("Original assay controls or endpoints changed")
    if controls["Final pass"]["n_with_dates"] != 21:
        raise ValueError("Original control date completeness changed")
    total_tokens = sum(all_tokens.values())
    if total_tokens != 6702 or sum(all_rows.values()) != 2850:
        raise ValueError("Original insect-row and flower-position denominator changed")
    groups = Counter()
    for (_, taxon), n in all_tokens.items():
        code = taxon.upper()
        groups[code if code in ("AH", "BF", "F") else "Other"] += n
    if groups != {"AH": 3414, "BF": 989, "F": 1910, "Other": 389}:
        raise ValueError("Source category totals drifted")
    return {
        "analysis_id": "LA004_source_internal_glossary_and_controls",
        "status": "BF_LOWERCASE_SOURCE_CODE_RESOLVED_PUBLISHED_VISIT_COUNT_STILL_UNRESOLVED",
        "source_sha256": SOURCE_SHA,
        "original_glossary_location":
            "Pollinator+Data+2014.xlsx / Landersville Field - Temporal / row 1",
        "source_glossary_literal_labels": list(glossary),
        "source_explicit_fact": "Bf is defined as Bee Fly, B as Butterfly",
        "remaining_codebook_limit":
            "Main-array uppercase BF is not independently defined by this temporal-sheet legend",
        "visit_source_periods": dict(source_sessions),
        "source_insect_rows": sum(all_rows.values()),
        "source_position_tokens": total_tokens,
        "source_case_sensitive": {
            f"{year}:{taxon}": {
                "insect_rows": all_rows[(year, taxon)],
                "plant_position_tokens": all_tokens[(year, taxon)],
            } for year, taxon in ((2014, "Bf"), (2014, "BF"),
                                  (2014, "B"), (2015, "BF"))
        },
        "source_casefold_category_share": {
            group: {"count": groups[group],
                    "percent_of_raw_position_tokens": 100 * groups[group] / total_tokens,
                    "published_percent_of_visits": PAPER["visit_frequency_percent"][group]}
            for group in ("AH", "BF", "F", "Other")
        },
        "source_2014_mapping_sensitivity_rates": {
            genotype: {label: fmean(rate[(genotype, label)])
                       for label in ("bf_casefold", "bf_strict_uppercase",
                                     "other_casefold", "other_plus_Bf")}
            for genotype in ("SI", "SC")
        },
        "original_assay_control_grain": controls,
        "paper": PAPER,
        "unresolved": [
            "3,748 published visits neither 2,850 insect rows nor 6,702 position tokens",
            "2014 main-array uppercase BF is not separately assigned in the original temporal codebook",
            "No source-backed rule selects 17 from 21 completely dated, outcome-coded controls",
            "No downstream seed/outcome analysis was opened or revised"
        ],
        "no_original_individual_observations_exported": True,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-zip", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    result = audit(args.source_zip)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps({
        "codebook": result["source_explicit_fact"],
        "source_case_counts": result["source_case_sensitive"],
        "controls": result["original_assay_control_grain"],
        "status": result["status"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
