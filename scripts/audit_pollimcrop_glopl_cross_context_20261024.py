#!/usr/bin/env python3
"""Cross-domain same-experiment reproductive-stage response census.

Empirical EGWEE exploratory analysis: wild GloPL (Bennett et al. 2018) and
crop PolLimCrop (Siopa et al. 2023). Do not pool their mismatched measurement
units or treat case rows as independent publication/study replications.

Both primary comparisons compare two recorded source means from the EXACT same
pollen-supplementation experimental case; a mismatch is NOT an established
causal reproductive tradeoff. Source encoding and denominator gates fail closed.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CROP = ROOT / "evidence/meta_extraction/pollimcrop_2023/1PUB_PolLimCrop_dataset.csv"
GLOPL = ROOT / "evidence/meta_extraction/glopl_2018/GloPL_with_id.csv"
ORIGINAL_CROP_MD5 = "29de02524b8625e8a72777463ac03348"
CROP_BYTES_PUBLISHED = 484888
GLOPL_STORED_BLOB = "0809eaeee54e4375d26bacfe002787241f8ff72e"
PROSPECTIVE_FRAGMENTATION_DENOMINATORS_CHANGED = False
CROP_VARIABLES = ("FS", "SS", "SN", "FW", "SW")


def crop_rows():
    raw = CROP.read_bytes()
    md5 = hashlib.md5(raw).hexdigest()
    # Source metadata separately preserve the published MD5. Do not assert that
    # UTF-8 text retrieval guarantees publisher-byte identity.
    with CROP.open("r", encoding="utf-8-sig", newline="") as fh:
        physical = fh.read().splitlines()
    assert len(physical) == 1169, len(physical)
    def extract(physical_line):
        # Figshare supplies each semicolon CSV record inside an extra pair of
        # outer double quotes; quoted coordinates have doubled inner quotes.
        assert physical_line.startswith('"') and physical_line.endswith('"')
        internal = physical_line[1:-1].replace('""', '"')
        return next(csv.reader([internal], delimiter=";", quotechar='"'))
    columns = extract(physical[0])
    assert len(columns) == 66 and len(set(columns)) == 66
    assert columns[0] == "line" and columns[18] == "FS_SUP_m"
    cases = []
    for ix, rec in enumerate(physical[1:], 1):
        cells = extract(rec)
        assert len(cells) == 66, (ix, len(cells))
        cases.append(dict(zip(columns, cells)))
    assert len(cases) == 1168
    ids = [int(r["line"]) for r in cases]
    assert len(set(ids)) == len(ids) and sorted(set(range(1, 1170)) - set(ids)) == [256]
    assert len({r["article_code"] for r in cases}) == 293
    assert len({r["species"].strip() for r in cases}) == 106
    assert len({r["crop_name"].strip() for r in cases}) > 80
    return cases, {"utf8_stored_bytes": len(raw), "stored_md5": md5,
                   "figshare_original_size": CROP_BYTES_PUBLISHED,
                   "figshare_original_md5": ORIGINAL_CROP_MD5,
                   "byte_identical_to_figshare": md5 == ORIGINAL_CROP_MD5,
                   "source_physical_records": len(cases),
                   "missing_original_line_id": [256],
                   "distinct_article_code_strings": 293,
                   "distinct_species_strings": 106}


def glopl_rows():
    blob = GLOPL.read_bytes()
    sha = hashlib.sha1(f"blob {len(blob)}\0".encode("ascii") + blob).hexdigest()
    assert sha == GLOPL_STORED_BLOB, sha
    with GLOPL.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2969
    assert len({r["unique_study_number"] for r in rows}) == 927
    return rows, sha


def number(s):
    if s is None or s.strip() in {"", "NA", "NaN", "nan", "N/A"}:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def direction(row, endpoint, domain):
    if domain == "crop":
        supplement, natural = (
            number(row[f"{endpoint}_SUP_m"]), number(row[f"{endpoint}_NAT_m"]))
    else:
        supplement, natural = (
            number(row[f"Sup_X_{endpoint}"]), number(row[f"Natural_X_{endpoint}"]))
    if supplement is None or natural is None or min(supplement,natural)<0:
        return None
    difference = supplement - natural
    return (1 if difference>0 else (-1 if difference<0 else 0))


def case_pair(rows, endpoint_a, endpoint_b, domain, allowed=None):
    result = []
    for row in rows:
        if allowed is not None and not allowed(row):
            continue
        a = direction(row,endpoint_a,domain)
        b = direction(row,endpoint_b,domain)
        if a is None or b is None:
            continue
        result.append((row,a,b))
    return result


def doi(value):
    match = re.search(r"10\.\d{4,9}/[A-Za-z0-9._;()\-:/]+", value or "")
    return match.group(0).rstrip(".;)]").lower() if match else None


def safe_z(row,endpoint,domain):
    if domain == "crop":
        mu1,mu0 = number(row[f"{endpoint}_SUP_m"]),number(row[f"{endpoint}_NAT_m"])
        n1,n0 = number(row[f"{endpoint}_SUP_n"]),number(row[f"{endpoint}_NAT_n"])
        sd1,sd0 = number(row[f"{endpoint}_SUP_sd"]),number(row[f"{endpoint}_NAT_sd"])
    else:
        mu1,mu0 = number(row[f"Sup_X_{endpoint}"]),number(row[f"Natural_X_{endpoint}"])
        n1,n0 = number(row[f"Sup_N_{endpoint}"]),number(row[f"Natural_N_{endpoint}"])
        sd1,sd0 = number(row[f"Sup_SD_{endpoint}"]),number(row[f"Natural_SD_{endpoint}"])
    values=[mu1,mu0,n1,n0,sd1,sd0]
    if any(v is None for v in values) or min(mu1,mu0,sd1,sd0)<0 or min(n1,n0)<=1:
        return None
    se = (sd1*sd1/n1+sd0*sd0/n0)**.5
    return abs(mu1-mu0)/se if se>0 else None


def summarise(rows, A, B, domain, key):
    valid = case_pair(rows,A,B,domain)
    nz = [(r,a,b) for r,a,b in valid if a*b != 0]
    discord = [(r,a,b) for r,a,b in nz if a != b]
    publication = defaultdict(list)
    for r,a,b in nz:
        publication[r[key]].append(int(a!=b))
    study_means = {pub:sum(vals)/len(vals) for pub,vals in publication.items()}
    vals = np.asarray(list(study_means.values()),float)
    rng = np.random.default_rng(20261024)
    bootstrap = np.mean(vals[rng.integers(0,len(vals),size=(20000,len(vals)))],axis=1)
    n = len(nz)
    table=Counter(("+" if a>0 else "-")+("+" if b>0 else "-") for _,a,b in nz)
    approx=[r for r,_,_ in discord if safe_z(r,A,domain) is not None
            and safe_z(r,B,domain) is not None]
    nominal=[r for r in approx if safe_z(r,A,domain)>=1.96
             and safe_z(r,B,domain)>=1.96]
    bonf=[r for r in approx if safe_z(r,A,domain)>=2.2414
          and safe_z(r,B,domain)>=2.2414]
    return {
        "response_a":A,"response_b":B,
        "same_case_both_numeric_including_zero":len(valid),
        "same_case_both_nonzero":n,
        "two_by_two":dict(table),
        "discordant":len(discord),
        "case_fraction":len(discord)/n,
        "publications":len(publication),
        "publications_with_discordance":sum(any(v) for v in publication.values()),
        "families_with_discordance":len({r["family" if domain=="crop" else "Family"]
                                       for r,_,_ in discord}),
        "publication_equal_fraction":float(vals.mean()),
        "publication_cluster_percentile95":
            [float(v) for v in np.quantile(bootstrap,[.025,.975])],
        "omission_publication_equal_range":
            [float(min((vals.sum()-v)/(len(vals)-1) for v in vals)),
             float(max((vals.sum()-v)/(len(vals)-1) for v in vals))],
        "rough_precision_screen": {
            "both_se_available":len(approx),
            "both_z_above_1_96":len(nominal),
            "publications_nominal":len({r[key] for r in nominal}),
            "both_z_above_2_2414":len(bonf),
            "publications_bonf":len({r[key] for r in bonf}),
            "warning":"naive independent-arm SD/N z values, not covariance-complete or multiplicity-across-case certainties; unequal biological sampling grains, pseudoreplication and response boundedness"
        },
    },discord



def crop_same_case_triple(rows):
    """Post hoc selection from the ten scanned crop endpoint pairs.

    Three outcomes from *the same* experimental record prevent a change in
    crop/source composition from masquerading as an endpoint contrast. Study-
    level resampling, not case-level resampling, supplies sensitivity intervals.
    """
    eligible=[
        r for r in rows
        if all(direction(r,k,"crop") not in (None,0) for k in ("FS","SN","FW"))
    ]
    assert len(eligible)==178
    def flags(r):
        return (int(direction(r,"FS","crop")!=direction(r,"SN","crop")),
                int(direction(r,"FS","crop")!=direction(r,"FW","crop")))
    def measure(source):
        by_source=defaultdict(list)
        for r in source:
            sn,fw=flags(r)
            by_source[r["article_code"]].append(fw-sn)
        diffs=np.asarray([np.mean(v) for v in by_source.values()],float)
        rng=np.random.default_rng(20261024)
        bootstrap=np.mean(diffs[rng.integers(0,len(diffs),
                        size=(20000,len(diffs)))],axis=1)
        signs=rng.choice((-1,1),size=(20000,len(diffs)))
        null=np.mean(signs*diffs[None,:],axis=1)
        observed=float(np.mean(diffs))
        delta=np.asarray([flags(r)[1]-flags(r)[0] for r in source],float)
        return {
            "n_same_case_three_nonzero":len(source),
            "source_publications":len(by_source),
            "FS_SN_discordant":sum(flags(r)[0] for r in source),
            "FS_FW_discordant":sum(flags(r)[1] for r in source),
            "FW_only_discordant":int(sum(x==1 for x in delta)),
            "SN_only_discordant":int(sum(x==-1 for x in delta)),
            "row_difference":float(delta.mean()),
            "publication_equal_difference":observed,
            "publication_cluster_bootstrap_percentile95":
                [float(v) for v in np.quantile(bootstrap,[.025,.975])],
            "exploratory_publication_signflip_p":
                float((1+np.sum(abs(null)>=abs(observed)-1e-12))/
                      (len(null)+1)),
            "publications_positive_negative_zero": {
                "positive":int(np.sum(diffs>0)),
                "negative":int(np.sum(diffs<0)),
                "zero":int(np.sum(diffs==0))
            },
        }
    all_rows=measure(eligible)
    no_apple=measure([r for r in eligible if r["species"].strip()!="Malus domestica"])
    no_ros=measure([r for r in eligible if r["family"]!="Rosaceae"])
    counts=Counter(r["article_code"] for r in eligible)
    biggest=max(counts,key=counts.get)
    no_largest=measure([r for r in eligible if r["article_code"]!=biggest])
    # SD/N availability and standardised treatment-difference resolution differ
    # among seed counts versus fruit weights; numbers are screens, not causes.
    sd=[r for r in eligible if all(safe_z(r,k,"crop") is not None
                                  for k in ("FS","SN","FW"))]
    z1=[r for r in sd if all(safe_z(r,k,"crop")>=1
                            for k in ("FS","SN","FW"))]
    z196=[r for r in sd if all(safe_z(r,k,"crop")>=1.96
                              for k in ("FS","SN","FW"))]
    all_rows.update({
        "sensitivity_without_Malus_domestica":no_apple,
        "sensitivity_without_Rosaceae":no_ros,
        "sensitivity_without_largest_publication":no_largest,
        "largest_publication":biggest,
        "complete_three_SD_N":measure(sd),
        "all_three_z_above_1":measure(z1),
        "all_three_z_above_1_96":measure(z196),
        "precision_note":"Endpoint SD/N and normal-reference z screens differ in observation level; filtering by z is outcome-selected and very small, and cannot certify a resource-mediated tradeoff.",
        "post_hoc_multiple_testing_note":"This triple comparison was noticed after examining ten endpoint pairs. The publication sign-flip p is an exploratory diagnostic, not pre-registered multiplicity-adjusted evidence."
    })
    assert (all_rows["n_same_case_three_nonzero"],
            all_rows["source_publications"],
            all_rows["FS_SN_discordant"],
            all_rows["FS_FW_discordant"],
            all_rows["FW_only_discordant"],
            all_rows["SN_only_discordant"])==(178,45,51,81,48,18)
    assert (no_apple["n_same_case_three_nonzero"],
            no_ros["n_same_case_three_nonzero"],
            no_largest["n_same_case_three_nonzero"])==(64,59,122)
    assert (len(sd),len(z1),len(z196))==(99,28,11)
    assert (measure(z196)["FS_SN_discordant"],
            measure(z196)["FS_FW_discordant"])==(2,2)
    return all_rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path)
    ap.add_argument("--discordant-cases",type=Path)
    args=ap.parse_args()
    crops,source=crop_rows()
    glopl,gsha=glopl_rows()
    shared_doi=sorted({doi(r["DOI_citation"]) for r in crops
                       if doi(r["DOI_citation"])} &
                      {doi(r["DOI"]) for r in glopl if doi(r["DOI"])})
    assert shared_doi == [
        "10.1093/aob/mcr293",
        "10.1111/j.1744-7909.2008.00800.x",
        "10.1590/s0006-87052009000100002",
    ], shared_doi
    wild,wd=summarise(glopl,"FS","SPFR","wild","unique_study_number")
    crop,cd=summarise(crops,"FS","SN","crop","article_code")
    crops_independent=[r for r in crops if doi(r["DOI_citation"]) not in shared_doi]
    crop_no_overlap,co=summarise(crops_independent,"FS","SN","crop","article_code")
    fruit_weight,fw=summarise(crops,"FS","FW","crop","article_code")
    crop_no_apple,aa=summarise([r for r in crops if r["species"].strip()!="Malus domestica"],"FS","SN","crop","article_code")
    crop_no_ros,ab=summarise([r for r in crops if r["family"]!="Rosaceae"],"FS","SN","crop","article_code")
    all_crop_pairs={}
    for i,A in enumerate(CROP_VARIABLES):
        for B in CROP_VARIABLES[i+1:]:
            p,_=summarise(crops,A,B,"crop","article_code")
            all_crop_pairs[f"{A}-{B}"]={
                "nonzero":p["same_case_both_nonzero"],
                "opposite":p["discordant"],
                "publications":p["publications"],
                "publication_equal_fraction":p["publication_equal_fraction"]}
    # The fixed primary endpoints are wild FS/SPFR vs crop FS/SN.
    assert (wild["same_case_both_nonzero"],wild["discordant"],wild["publications"])==(313,81,84)
    assert (crop["same_case_both_nonzero"],crop["discordant"],crop["publications"])==(300,75,72)
    assert (crop_no_overlap["same_case_both_nonzero"],crop_no_overlap["discordant"])==(299,75)
    assert (fruit_weight["same_case_both_nonzero"],fruit_weight["discordant"])==(292,117)
    assert (crop_no_ros["same_case_both_nonzero"],crop_no_ros["discordant"])==(108,24)
    assert (crop_no_apple["same_case_both_nonzero"],crop_no_apple["discordant"])==(120,25)
    assert crop["two_by_two"]=={"++":188,"+-":36,"-+":39,"--":37}
    assert (crop["rough_precision_screen"]["both_z_above_2_2414"],
            fruit_weight["rough_precision_screen"]["both_z_above_2_2414"])==(4,5)
    by_source=defaultdict(list)
    for r,a,b in case_pair(crops,"FS","SN","crop"):
        if a*b!=0:
            by_source[r["article_code"]].append(int(a!=b))
    largest=max(by_source,key=lambda s:len(by_source[s]))
    crop_omit_max,_=summarise([r for r in crops if r["article_code"]!=largest],
                              "FS","SN","crop","article_code")
    assert (crop_omit_max["same_case_both_nonzero"],
            crop_omit_max["discordant"])==(226,44)

    if args.discordant_cases:
        args.discordant_cases.parent.mkdir(parents=True,exist_ok=True)
        with args.discordant_cases.open("w",newline="",encoding="utf-8") as fd:
            fields=["dataset","row_id","article_code","species","family","FS_natural",
                    "FS_supplement","SN_natural","SN_supplement","source_doi"]
            wr=csv.DictWriter(fd,fieldnames=fields);wr.writeheader()
            for r,_,_ in cd:
                wr.writerow({
                    "dataset":"PolLimCrop_2023",
                    "row_id":r["line"],"article_code":r["article_code"],
                    "species":r["species"],"family":r["family"],
                    "FS_natural":r["FS_NAT_m"],"FS_supplement":r["FS_SUP_m"],
                    "SN_natural":r["SN_NAT_m"],"SN_supplement":r["SN_SUP_m"],
                    "source_doi":doi(r["DOI_citation"]) or ""
                })
    triple=crop_same_case_triple(crops)
    result={
        "status":"EXPLORATORY wild-vs-crop stage topology; not a common estimand",
        "provenance_crop":source,
        "provenance_glopl_stored_blob":gsha,
        "cross_dataset_shared_DOIs":shared_doi,
        "taxonomic_caveat":"GloPL SPFR is seeds per existing fruit; PolLimCrop SN is reported seed number and denominator may vary by study",
        "wild_GloPL_FS_SPFR":wild,
        "crop_PolLimCrop_FS_SN":crop,
        "crop_excluding_shared_publication_DOIs":crop_no_overlap,
        "crop_PolLimCrop_FS_FW":fruit_weight,
        "crop_same_case_FS_SN_FW_triple":triple,
        "crop_without_Malus_domestica":crop_no_apple,
        "crop_without_Rosaceae":crop_no_ros,
        "crop_largest_source":largest,
        "crop_without_largest_source":crop_omit_max,
        "crop_all_pairs":all_crop_pairs,
        "no_registered_fragmentation_meta_corpus_changes":
            not PROSPECTIVE_FRAGMENTATION_DENOMINATORS_CHANGED,
        "interpretation":"same intervention may give opposite source mean response directions across reproductive components within cases in wild and crops; missingness/selection/covariance prevent mechanism and population prevalence inference"
    }
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
                               encoding="utf-8")
    print("CROSSDOMAIN_CROP_SOURCE",json.dumps(source,ensure_ascii=False))
    print("CROSSDOMAIN_OVERLAP_DOIS",shared_doi)
    print("CROSSDOMAIN_TRIPLE",json.dumps({k:v for k,v in triple.items() if not k.startswith("sensitivity_")},sort_keys=True))
    for label,item in (("GloPL",wild),("PolLimCrop_FS_SN",crop),
                       ("crop_DOI_disjoint",crop_no_overlap),
                       ("crop_FS_FW",fruit_weight),
                       ("crop_no_Rosaceae",crop_no_ros),
                       ("crop_no_apple",crop_no_apple),
                       ("crop_no_largest_source",crop_omit_max)):
        print("CROSSDOMAIN",label,"n",item["same_case_both_nonzero"],
              "opp",item["discordant"],"publications",item["publications"],
              "source_equal",round(item["publication_equal_fraction"],6),
              "boot95",item["publication_cluster_percentile95"],
              "rough_double_z_2_24",item["rough_precision_screen"]["both_z_above_2_2414"])


if __name__=="__main__":
    main()
