from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "evidence/meta_extraction/phase2_sf05_table_s1_sheet02_sys_rev.csv"
SEEDS = ROOT / "manuscript/meta_analysis_primary_study_seed_v1.csv"
OUT = ROOT / "evidence/meta_extraction/phase2_sf05_primary_study_universe_v1.csv"
GAP = ROOT / "evidence/meta_extraction/phase2_sf05_source_frame_gap_v1.csv"
SUMMARY = ROOT / "evidence/meta_extraction/phase2_sf05_source_frame_summary_v1.json"
NOTE = ROOT / "manuscript/PHASE2_SF05_MATERIALIZATION_2026-09-18.md"

DOI_RE = re.compile(r"(?:https?://doi\.org/|doi:\s*)?(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)", re.I)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def norm_doi(text: str) -> str:
    m = DOI_RE.search(text or "")
    if not m:
        return ""
    return m.group(1).rstrip(".,);]").lower()


def uniq(values):
    return sorted({v.strip() for v in values if v and v.strip() and v.strip() != "NA"})


def hint_layers(reference: str) -> list[str]:
    t = reference.lower()
    hints = {"G_adult_FSGS"}
    if any(k in t for k in (
        "pollen dispersal", "gene dispersal", "gene flow", "pollen flow",
        "mating system", "outcross", "parentage", "pollen-mediated",
    )):
        hints.add("C_screen")
    if any(k in t for k in (
        "reproductive success", "reproduction", "fitness", "fruit set",
        "seed set", "seed production",
    )):
        hints.add("F_screen")
    if any(k in t for k in ("pollinator abundance", "pollinator visitation", "pollinator")):
        hints.add("I_screen")
    if any(k in t for k in ("seedling", "juvenile", "embryo", "age class", "life cycle")):
        hints.add("G_offspring_screen")
    if any(k in t for k in ("population density", "density", "population size", "demograph")):
        hints.add("D_screen")
    return sorted(hints)


def main() -> None:
    src = rows(SRC)
    seeds = rows(SEEDS)
    seed_by_doi = {norm_doi(r["doi"]): r["study_id"] for r in seeds if norm_doi(r["doi"])}

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in src:
        paper = r["Paper"].strip()
        if paper:
            grouped[paper].append(r)

    assert len(grouped) == 65, f"expected 65 source-selected studies, got {len(grouped)}"
    assert len(src) == 177, f"expected 177 population rows, got {len(src)}"

    fields = [
        "source_frame", "source_paper_id", "citation", "year", "first_author",
        "reference", "doi", "species", "n_species", "n_population_rows",
        "source_selected_systematic_review_65", "source_meta_analysis_31",
        "source_outcome_filter_status", "existing_egwee_study_ids",
        "countries", "biomes", "life_forms", "life_cycles", "mating_systems",
        "self_incompatibility", "pollination_classes", "pollination_vectors",
        "seed_dispersal_classes", "seed_dispersal_vectors", "cohorts",
        "disturbance_classes", "disturbance_codes", "time_since_disturbance",
        "title_method_screen_hints", "potential_multilayer_screen",
        "screening_status", "screening_note",
    ]

    out_rows = []
    n_meta = 0
    n_hints = 0
    n_linked = 0
    for paper, rs in sorted(grouped.items(), key=lambda kv: int(float(kv[0]))):
        references = uniq(r["reference"] for r in rs)
        citations = uniq(r["citation"] for r in rs)
        years = uniq(r["year"] for r in rs)
        authors = uniq(r["first.author"] for r in rs)
        dois = uniq(norm_doi(x) for x in references)
        species = uniq(r["species"] for r in rs)
        meta = any((r["meta"] or "").strip().upper() == "Y" for r in rs)
        if meta:
            n_meta += 1
        hints = hint_layers(" ".join(references))
        multilayer = len([h for h in hints if h != "G_adult_FSGS"]) > 0
        if multilayer:
            n_hints += 1
        existing = sorted({seed_by_doi[d] for d in dois if d in seed_by_doi})
        if existing:
            n_linked += 1

        out_rows.append({
            "source_frame": "SF05",
            "source_paper_id": paper,
            "citation": " | ".join(citations),
            "year": " | ".join(years),
            "first_author": " | ".join(authors),
            "reference": " | ".join(references),
            "doi": " | ".join(dois),
            "species": ";".join(species),
            "n_species": str(len(species)),
            "n_population_rows": str(len(rs)),
            "source_selected_systematic_review_65": "yes",
            "source_meta_analysis_31": "yes" if meta else "no",
            "source_outcome_filter_status": "retained_after_source_FSGS_significance_and_outlier_filters",
            "existing_egwee_study_ids": ";".join(existing),
            "countries": ";".join(uniq(r["country"] for r in rs)),
            "biomes": ";".join(uniq(r["biome"] for r in rs)),
            "life_forms": ";".join(uniq(r["life.form"] for r in rs)),
            "life_cycles": ";".join(uniq(r["life.cycle"] for r in rs)),
            "mating_systems": ";".join(uniq(r["mating.sys"] for r in rs)),
            "self_incompatibility": ";".join(uniq(r["S.I."] for r in rs)),
            "pollination_classes": ";".join(uniq(r["pol.clas"] for r in rs)),
            "pollination_vectors": ";".join(uniq(r["pol.v"] for r in rs)),
            "seed_dispersal_classes": ";".join(uniq(r["d.clas"] for r in rs)),
            "seed_dispersal_vectors": ";".join(uniq(r["d.vec"] for r in rs)),
            "cohorts": ";".join(uniq(r["cohort"] for r in rs)),
            "disturbance_classes": ";".join(uniq(r["dist.clas"] for r in rs)),
            "disturbance_codes": ";".join(uniq(r["dist.code"] for r in rs)),
            "time_since_disturbance": ";".join(uniq(r["time.from.dist"] for r in rs)),
            "title_method_screen_hints": ";".join(hints),
            "potential_multilayer_screen": "yes" if multilayer else "no",
            "screening_status": "bibliographic_materialized_not_effect_screened",
            "screening_note": "Hints are title/method metadata only; no C/I/F/G_offspring effect eligibility or direction has been opened.",
        })

    assert n_meta == 31, f"expected 31 source meta-analysis studies, got {n_meta}"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)

    gap_rows = [
        ["database_search", 343, 0, "source_reports_count_only", "reconstruct outcome-blind search universe from reproducible bibliographic search where feasible"],
        ["nonduplicate_records", 243, 0, "source_reports_count_only", "reconstruct before quantitative outcome screening"],
        ["source_eligible_records", 200, 0, "source_reports_count_only", "do not assume absence from Table S1 means EGWEE ineligibility"],
        ["habitat_status_plus_Sp", 74, 65, "nine identities missing from published Table S1", "recover at least the nine source-omitted identities before calling SF05 screening complete"],
        ["source_outcome_excluded_non_significant_FSGS", 6, 0, "outcome_based_source_exclusion", "must be restored to EGWEE candidate screening if identities are recovered"],
        ["source_outcome_excluded_outlier_Sp", 3, 0, "outcome_based_source_exclusion", "must be restored to EGWEE candidate screening if identities are recovered"],
        ["published_Table_S1_systematic_review_subset", 65, 65, "complete_for_source_selected_subset_only", "use as bibliographic seed subset, not as the outcome-blind denominator"],
        ["published_meta_analysis_subset", 31, 31, "complete_for_source_meta_subset", "retain source membership as metadata only"],
    ]
    with GAP.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["source_frame", "stage", "reported_n", "materialized_identity_n", "status", "egwee_action"])
        for row in gap_rows:
            w.writerow(["SF05", *row])

    summary = {
        "source_frame": "SF05",
        "source_article": "Miguel-Penaloza et al. 2023 AoB PLANTS plad019",
        "source_doi": "10.1093/aobpla/plad019",
        "source_reported_flow": {
            "database_hits": 343,
            "nonduplicate": 243,
            "source_eligible": 200,
            "habitat_status_plus_Sp": 74,
            "source_outcome_excluded_non_significant_FSGS": 6,
            "source_outcome_excluded_outlier_Sp": 3,
            "published_systematic_review_subset": 65,
            "published_meta_analysis_subset": 31,
        },
        "materialized": {
            "population_rows": len(src),
            "unique_source_selected_studies": len(out_rows),
            "unique_source_meta_analysis_studies": n_meta,
            "title_method_multilayer_screen_hints": n_hints,
            "linked_existing_egwee_seed_studies": n_linked,
        },
        "denominator_status": "incomplete_outcome_blind_source_frame",
        "minimum_missing_identity_count": 9,
        "reason": "published Table S1 begins after six non-significant-FSGS and three outlier-Sp exclusions",
        "effect_outcomes_opened_for_egwee_phase2": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    NOTE.write_text(
        "# Phase-2 SF05 materialization — 2026-09-18\n\n"
        "## Current state\n\n"
        "SF05 is the 2023 AoB PLANTS FSGS synthesis (doi:10.1093/aobpla/plad019). "
        "Its public Supporting Table S1 has been materialized without spreadsheet recalculation and reduced to a study-level bibliographic screening universe.\n\n"
        "The workbook contains 177 population rows belonging to 65 source-selected systematic-review papers; "
        "31 of those papers are marked by the source as entering its quantitative meta-analysis.\n\n"
        "## Outcome-blind denominator warning\n\n"
        "The published article reports the flow 343 -> 243 nonduplicate -> 200 source-eligible -> "
        "74 with habitat status + Sp -> 65 systematic-review papers. The final step is outcome-dependent: "
        "six studies with non-significant FSGS and three studies with outlier Sp were removed before Table S1.\n\n"
        "Therefore the 65 materialized identities are not EGWEE's outcome-blind SF05 denominator. "
        "They are a recoverable seed subset. At minimum, the nine outcome-excluded identities must be restored "
        "to candidate screening if they can be recovered; ideally the broader 243/200 record frame is reconstructed "
        "through the registered reproducible search route.\n\n"
        "No non-significant FSGS study will be coded as zero, and no source outlier exclusion is inherited as an EGWEE eligibility rule.\n\n"
        "## What has and has not been opened\n\n"
        "Materialized now:\n"
        "- citation/DOI/species and source study membership;\n"
        "- disturbance, cohort, life-form, mating-system, pollination/dispersal metadata already present in Table S1;\n"
        "- title/method screening hints used only to prioritize full-text multilayer screening;\n"
        "- links to already registered EGWEE studies when a DOI matches.\n\n"
        "Not opened for Phase 2:\n"
        "- no new C/I/F/G-offspring effect size;\n"
        "- no new layer-pair contrast;\n"
        "- no candidate is admitted because of effect direction, significance or apparent support for state separation.\n\n"
        "## Next screening\n\n"
        "Screen title/method candidates for additional same-system layers, with particular attention to fragmentation papers "
        "that also measured pollen/gene dispersal, mating, cohorts, density or reproductive function. Every candidate receives "
        "the same same-exposure and independent-unit gate before quantitative extraction.\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
