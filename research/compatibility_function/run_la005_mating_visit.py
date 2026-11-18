#!/usr/bin/env python3
"""LA005: lower-bound detectable nonmaternal allele vs visitor exposure.

Original Layman et al. (2017) Dryad file, source-hash pinned. Parent–offspring
markers are analyzed only under a prospectively committed protocol. Writes
aggregate site/year/SC diagnostics, all site CV scores and source-only
coverage — NO original individual identifiers, allele calls, offspring rows
or third-party source files are ever exported.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from math import exp, isfinite, log, log1p
from pathlib import Path
from statistics import fmean
import subprocess
from zipfile import ZipFile

from run_leavenworthia_LA001 import SOURCE_SHA, SITES, sheets, value, solve
from run_leavenworthia_LA002 import pollinator_sequences_by_plant

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL_FILE = HERE / "LA005_FROZEN_MATING_VISIT_PROTOCOL_20261118.json"
FROZEN_PROTOCOL_COMMIT = "8f185bd271af42a93da32928c2e54132a07c63e7"
SITE_NAME = {i: name for i, name in enumerate(SITES, 1)}
RESULT_STATUS = "ORIGINAL_SOURCE_GENOTYPE_PAIRING_SITE_HOLDOUT_COMPLETED"


def verify_original_freeze() -> dict:
    expected = subprocess.check_output(
        ["git", "show",
         FROZEN_PROTOCOL_COMMIT + ":" +
         "research/compatibility_function/LA005_FROZEN_MATING_VISIT_PROTOCOL_20261118.json"],
        cwd=ROOT,
    )
    if expected != PROTOCOL_FILE.read_bytes():
        raise RuntimeError("LA005 scientific protocol no longer matches its pre-outcome freeze")
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", FROZEN_PROTOCOL_COMMIT, "HEAD"],
        cwd=ROOT, check=True,
    )
    proto = json.loads(expected)
    if (proto["experiment_id"] != "LA005_maternal_nonmaternal_allele_visit_prediction_v1" or
        proto["status"] != "prospective_locked_before_opening_offspring_nonmaternal_allele_outcomes"):
        raise RuntimeError("Incorrect pre-outcome LA005 protocol")
    return proto


def normalized_label(text: str, year: int) -> str:
    """Source-specific, pre-declared maternal suffix conventions."""
    if year == 2014:
        return text.split("_")[-1]
    return text.removesuffix("M")


def typed_loci(record: dict) -> dict[int, tuple[int, int]]:
    typed = {}
    for i in range(6):
        a, b = value(record, 2 + 2 * i), value(record, 3 + 2 * i)
        if (isinstance(a, (int, float)) and isinstance(b, (int, float)) and
            isfinite(float(a)) and isfinite(float(b)) and
            a > 0 and b > 0 and int(a) == a and int(b) == b):
            typed[i] = int(a), int(b)
    return typed


def detected_nonmaternal(child: dict[int, tuple[int,int]],
                         mother: dict[int, tuple[int,int]],
                         min_shared: int = 4) -> int | None:
    """Conservative observed nonmaternal-allele indicator, NOT full paternity."""
    shared = set(mother).intersection(child)
    if len(shared) < min_shared:
        return None
    return int(any(
        child[j][0] not in mother[j] or child[j][1] not in mother[j]
        for j in shared
    ))


def logit_rate(k: int, n: int) -> float:
    """Half-count bounded empirical logit; k=n allowed."""
    if not 0 <= k <= n or n < 1:
        raise ValueError("Invalid lower-bound nonmaternal allele count")
    return log((k + 0.5) / (n - k + 0.5))


def sigmoid(x: float) -> float:
    if x >= 0:
        z = exp(-x)
        return 1 / (1 + z)
    z = exp(x)
    return z / (1 + z)


def load_maternal_records(source_zip: Path) -> tuple[list[dict], dict]:
    proto = verify_original_freeze()
    if hashlib.sha256(source_zip.read_bytes()).hexdigest() != SOURCE_SHA:
        raise ValueError("Original Dryad archive digest mismatch")
    with ZipFile(source_zip) as archive:
        if archive.testzip() is not None:
            raise ValueError("Source ZIP CRC failed")
        field_rows = sheets(archive, "2014+2015+Field+data.xlsx")["Sheet1"]
        field_by_key: dict[tuple, dict] = {}
        for row_no, row in field_rows.items():
            if row_no == 1:
                continue
            ycode, site, pid, sc = value(row, 0), value(row, 1), value(row, 2), value(row, 4)
            if ycode not in (1, 2) or site not in (1, 2, 3, 4):
                raise ValueError("Unexpected year/site coding in original field")
            if not isinstance(pid, str) or sc not in (0, 1):
                raise ValueError("Field source ID/SC marker malformed")
            year = 2013 + int(ycode)
            key = (year, int(site), pid.strip())
            if key in field_by_key:
                raise ValueError("Duplicate field plant key")
            field_by_key[key] = row
        if len(field_by_key) != 256:
            raise ValueError("Original 256 field plants missing")
        visits, visitor_qc = pollinator_sequences_by_plant(archive, field_by_key)
        if len(visits) != 256 or visitor_qc["complete_sessions"] != 121:
            raise ValueError("Original 121 complete visit periods missing")
        blocks: list[dict] = []
        qc = Counter()
        per_site_year = defaultdict(Counter)
        for year in (2014, 2015):
            workbook = sheets(archive, f"Fragment+Analysis+{year}.xlsx")
            for site, place in SITE_NAME.items():
                name = f"Site {site} ({place})"
                rows = workbook[name]
                current = None
                for row_num, source_row in sorted(rows.items()):
                    if row_num < 3:
                        continue
                    label = value(source_row, 0)
                    if not isinstance(label, str):
                        qc["unlabeled_rows"] += 1
                        continue
                    if label.endswith("!"):
                        mother_key = (year, site, normalized_label(label[:-1], year))
                        current = {
                            "key": mother_key,
                            "genotype": value(source_row, 1),
                            "mother_loci": typed_loci(source_row),
                            "offspring": [],
                        }
                        blocks.append(current)
                        qc["maternal_source_rows"] += 1
                        per_site_year[(year, site)]["maternal_rows"] += 1
                    else:
                        qc["offspring_source_rows"] += 1
                        per_site_year[(year, site)]["offspring_rows"] += 1
                        if current is None or normalized_label(label, year) != current["key"][2]:
                            # Seven 2014 site 3 labels are not tied to a
                            # valid mother! Never attribute to prior block.
                            qc["offspring_label_mismatches"] += 1
                            per_site_year[(year, site)]["offspring_label_mismatches"] += 1
                        else:
                            current["offspring"].append(typed_loci(source_row))
        expected_mat_rows = {2014: [31, 32, 28, 32], 2015: [32, 32, 30, 32]}
        expected_children = {2014: [192, 235, 166, 222], 2015: [248, 252, 227, 254]}
        for year in (2014, 2015):
            for site in range(1, 5):
                cnt = per_site_year[(year, site)]
                if (cnt["maternal_rows"] != expected_mat_rows[year][site-1] or
                    cnt["offspring_rows"] != expected_children[year][site-1]):
                    raise ValueError("Source-only mother/progeny row roster has changed")
        by_key = Counter(block["key"] for block in blocks)
        duplicate_keys = {k for k, n in by_key.items() if n != 1}
        matched_raw_keys = {k for k in by_key if k in field_by_key}
        if (len(blocks), len(by_key), len(duplicate_keys), len(matched_raw_keys),
            qc["offspring_source_rows"], qc["offspring_label_mismatches"]) != (
            249, 248, 1, 246, 1796, 7
        ):
            raise ValueError("Source-only 249/248/246 maternal key or 1796/7 offspring gate changed")
        kept = []
        genotyped_progeny = 0
        untyped_progeny = 0
        too_small_mothers = 0
        for block in blocks:
            key = block["key"]
            if key in duplicate_keys:
                qc["duplicate_source_mother_blocks_excluded"] += 1
                continue
            if key not in field_by_key:
                qc["nonmatching_field_mothers_excluded"] += 1
                continue
            source_row = field_by_key[key]
            genetic_status = block["genotype"]
            field_status = "SC" if value(source_row, 4) == 0 else "SI"
            if genetic_status != field_status:
                raise ValueError("Mother SC/SI source genotype mismatch")
            loci = block["mother_loci"]
            if len(loci) < 4:
                raise ValueError("Mother has fewer than 4 typed loci")
            valid = []
            for child in block["offspring"]:
                detected = detected_nonmaternal(
                    child, loci,
                    proto["fixed_key_contract"]["offspring_min_typed_loci"],
                )
                if detected is None:
                    untyped_progeny += 1
                    continue
                valid.append(detected)
                genotyped_progeny += 1
            if len(valid) < proto["fixed_key_contract"]["mother_min_children"]:
                too_small_mothers += 1
                continue
            visit = visits[key]
            if visit["flower_hours"] <= 0:
                raise ValueError("No flower-hour exposure for an eligible source mother")
            flowers, flowering = value(source_row, 5), value(source_row, 9)
            if (not isinstance(flowers, (int, float)) or
                not isinstance(flowering, (int, float)) or
                flowers < 0 or flowering < 0):
                raise ValueError("Source flower or phenology baseline malformed")
            sc = int(genetic_status == "SC")
            year, site, _ = key
            heterozygosity = sum(a != b for a,b in loci.values()) / len(loci)
            kept.append({
                "site": site, "year": year, "SC": sc,
                "n": len(valid), "k": sum(valid),
                "y": logit_rate(sum(valid), len(valid)),
                "empirical_fraction": fmean(valid),
                "baseline": [int(year == 2015), sc, int(year == 2015)*sc,
                             log1p(flowers), flowering/30, heterozygosity],
                "effective": log1p((visit["AH"] + visit["BF"])/visit["flower_hours"]),
            })
            qc["eligible_mothers"] += 1
            per_site_year[(year, site)]["eligible_mothers"] += 1
        if (qc["duplicate_source_mother_blocks_excluded"] != 2 or
            qc["nonmatching_field_mothers_excluded"] != 2):
            raise ValueError("Unmatched or duplicated mother exclusion count changed")
        if len(kept) < 100:
            raise RuntimeError("COVERAGE_STOP: fewer than 100 eligible mother/offspring units")
        by_site = Counter(r["site"] for r in kept)
        if any(by_site[s] < 10 for s in range(1,5)):
            raise RuntimeError("COVERAGE_STOP: a site has fewer than ten eligible mothers")
        safe_receipt = {
            "source_field_plants": len(field_by_key),
            "source_maternal_rows": qc["maternal_source_rows"],
            "source_unique_maternal_keys": len(by_key),
            "source_unique_matched_field_mothers": len(matched_raw_keys),
            "duplicate_mother_keys": len(duplicate_keys),
            "excluded_duplicate_mother_blocks": qc["duplicate_source_mother_blocks_excluded"],
            "excluded_nonmatching_field_mothers": qc["nonmatching_field_mothers_excluded"],
            "source_progeny_rows": qc["offspring_source_rows"],
            "excluded_offspring_label_mismatches": qc["offspring_label_mismatches"],
            "typed_offspring_in_unique_matched_mother_blocks_before_min_child_gate": genotyped_progeny,
            "offspring_in_admitted_mothers": sum(r["n"] for r in kept),
            "excluded_offspring_insufficient_joint_loci": untyped_progeny,
            "excluded_mothers_fewer_than_four_children": too_small_mothers,
            "eligible_mother_units": len(kept),
            "eligible_mothers_per_site": {SITE_NAME[s]: by_site[s] for s in range(1,5)},
            "year_site_source_roster": {
                f"{yr}:{SITE_NAME[site]}": dict(per_site_year[(yr,site)])
                for yr in (2014,2015) for site in range(1,5)
            },
            "original_visit_observation_windows": visitor_qc["complete_sessions"],
        }
        return kept, safe_receipt


def ridge_prediction(train: list[dict], test: list[dict], additional_visits: bool) -> list[float]:
    def feats(r: dict) -> list[float]:
        return r["baseline"] + ([r["effective"]] if additional_visits else [])
    raw = [feats(r) for r in train]
    p = len(raw[0])
    mean = [fmean(v[j] for v in raw) for j in range(p)]
    sd = []
    for j in range(p):
        v = (fmean((x[j]-mean[j])**2 for x in raw))**0.5
        sd.append(v if v>1e-10 else 1)
    x = [[1.0] + [(v[j]-mean[j])/sd[j] for j in range(p)] for v in raw]
    gram = [[sum(v[j]*v[k] for v in x)+(1 if j==k and j>0 else 0)
             for k in range(p+1)] for j in range(p+1)]
    rhs = [sum(v[j]*r["y"] for v,r in zip(x,train)) for j in range(p+1)]
    beta=solve(gram,rhs)
    return [sigmoid(beta[0]+sum(beta[j+1]*(feats(r)[j]-mean[j])/sd[j]
                                for j in range(p))) for r in test]


def analyze(source: Path) -> dict:
    rows, qc = load_maternal_records(source)
    folds = []
    for site in range(1, 5):
        train=[r for r in rows if r["site"]!=site]
        test=[r for r in rows if r["site"]==site]
        if len(train)+len(test)!=len(rows) or len(test)<10:
            raise RuntimeError("Coverage stopped during source-heldout prediction")
        a=ridge_prediction(train,test,False)
        b=ridge_prediction(train,test,True)
        def score(pred):
            errors=[p-r["empirical_fraction"] for p,r in zip(pred,test)]
            return {"brier_mother":fmean(e*e for e in errors),
                    "mae_mother":fmean(abs(e) for e in errors)}
        m0,m1=score(a),score(b)
        folds.append({
            "site":SITE_NAME[site],"n_mothers":len(test),
            "source_progeny_n":sum(r["n"] for r in test),
            "M0":m0,"M1":m1,
            "M0_minus_M1_brier":m0["brier_mother"]-m1["brier_mother"],
        })
    if sum(f["n_mothers"] for f in folds)!=len(rows):
        raise RuntimeError("Holdout sum does not equal eligible mother denominator")
    pooled={
        model:{metric:sum(f["n_mothers"]*f[model][metric] for f in folds)/len(rows)
               for metric in ("brier_mother","mae_mother")}
        for model in ("M0","M1")
    }
    delta=pooled["M0"]["brier_mother"]-pooled["M1"]["brier_mother"]
    wins=sum(f["M0_minus_M1_brier"]>0 for f in folds)
    # Secondary descriptive SC/SI groups: no plant-level p-values and no
    # source row, maternal ID or genotype arrays leave memory.
    group_descriptives=[]
    for year in (2014,2015):
        for sc in (0,1):
            sample=[r for r in rows if r["year"]==year and r["SC"]==sc]
            group_descriptives.append({
                "year":year,"group":"SC" if sc else "SI",
                "n_mothers":len(sample),
                "n_genotyped_children":sum(r["n"] for r in sample),
                "mean_detected_nonmaternal_allele_fraction":fmean(r["empirical_fraction"] for r in sample),
                "mean_effective_source_visit_rate":fmean(exp(r["effective"])-1 for r in sample),
            })
    return {
        "analysis_id":"LA005_maternal_nonmaternal_allele_visit_prediction_v1",
        "status":RESULT_STATUS,"source_archive_sha256":SOURCE_SHA,
        "frozen_protocol_commit":FROZEN_PROTOCOL_COMMIT,
        "source_grain_receipt":qc,
        "independent_site_folds":4,
        "holdout_folds":folds,"pooled":pooled,
        "primary_M0_minus_M1_brier":delta,
        "positive_site_fold_count":wins,
        "decision":("BOUNDED_WITHIN_STUDY_VISIT_TO_DETECTABLE_OUTCROSSING_INCREMENT"
                    if delta>0 and wins>=3 else
                    "NO_ROBUST_MATING_PROXY_SITE_TRANSFER_INCREMENT"),
        "secondary_descriptive_source_classes":group_descriptives,
        "limitations":[
            "Detectable nonmaternal allele is a lower-bound proxy, not the exact outcrossing rate",
            "Genotype/allele typing errors are not excluded by this source-only marker test",
            "Single original four-site programme; no out-of-study replication",
            "2014 site3 duplicate maternal key excluded entirely and 7 nonmatching offspring IDs unassigned",
            "SC marker is fully confounded with experimental SC/SI status",
            "AH/BF visitor rate uses source position records, not published 3748 cleaned visits",
            "No verified compatible pollen or independently assigned paternal genotype",
            "Original 2017 authors already reported outcrossing differences; no new ecology law",
            "No source genotype, field plant or individual offspring data redistributed",
        ],
    }


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--source-zip",required=True,type=Path)
    parser.add_argument("--output",required=True,type=Path)
    a=parser.parse_args()
    result=analyze(a.source_zip)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
                        encoding="utf-8")
    print(json.dumps({
        "analysis":result["analysis_id"],
        "mothers":result["source_grain_receipt"]["eligible_mother_units"],
        "genotyped_children":result["source_grain_receipt"]["offspring_in_admitted_mothers"],
        "Brier_M0":result["pooled"]["M0"]["brier_mother"],
        "Brier_M1":result["pooled"]["M1"]["brier_mother"],
        "delta":result["primary_M0_minus_M1_brier"],
        "site_wins":result["positive_site_fold_count"],
        "decision":result["decision"],
    },indent=2))


if __name__=="__main__":
    main()
