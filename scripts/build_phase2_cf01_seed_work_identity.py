from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "evidence/meta_extraction/phase2_cf01_seed_manifest_v1.csv"
RESOLUTION = ROOT / "evidence/meta_extraction/phase2_cf01_bibliographic_resolution_v1.csv"
OUT = ROOT / "evidence/meta_extraction/phase2_cf01_seed_work_identity_v1.csv"
DUPS = ROOT / "evidence/meta_extraction/phase2_cf01_seed_duplicate_work_groups_v1.csv"
SUMMARY = ROOT / "evidence/meta_extraction/phase2_cf01_seed_work_identity_summary_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF01_SEED_WORK_IDENTITY_2026-09-23.md"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def short_id(value: str) -> str:
    return (value or "").rstrip("/").split("/")[-1]


def main() -> None:
    assert SEEDS.is_file(), SEEDS
    assert RESOLUTION.is_file(), RESOLUTION

    seeds = rows(SEEDS)
    resolution = rows(RESOLUTION)
    assert len(seeds) == len(resolution) == 363

    seed_by_id = {r["cf01_seed_id"]: r for r in seeds}
    res_by_id = {r["cf01_seed_id"]: r for r in resolution}
    assert set(seed_by_id) == set(res_by_id)

    by_work: dict[str, list[str]] = defaultdict(list)
    for sid, rr in res_by_id.items():
        if rr["resolution_status"] == "resolved":
            oa = short_id(rr["openalex_id"])
            assert oa, rr
            by_work[oa].append(sid)

    duplicate_groups = {
        oa: sorted(sids)
        for oa, sids in by_work.items()
        if len(sids) > 1
    }

    out = []
    for sid in sorted(seed_by_id):
        seed = seed_by_id[sid]
        rr = res_by_id[sid]
        if rr["resolution_status"] == "resolved":
            oa = short_id(rr["openalex_id"])
            group = sorted(by_work[oa])
            canonical = group[0]
            identity_status = (
                "resolved_duplicate_work"
                if len(group) > 1
                else "resolved_unique_work"
            )
            work_key = f"OPENALEX:{oa}"
        else:
            oa = ""
            group = [sid]
            canonical = sid
            identity_status = "unresolved_seed_identity"
            work_key = f"UNRESOLVED:{sid}"

        out.append({
            "cf01_seed_id": sid,
            "canonical_search_key": seed["canonical_search_key"],
            "input_doi": seed["doi"],
            "input_citation": seed["citation"],
            "resolution_status": rr["resolution_status"],
            "resolution_method": rr["resolution_method"],
            "openalex_id": oa,
            "resolved_doi": rr["resolved_doi"],
            "resolved_title": rr["resolved_title"],
            "work_identity_key": work_key,
            "work_identity_status": identity_status,
            "canonical_seed_id_for_work": canonical,
            "seed_ids_sharing_resolved_work": ";".join(group),
            "n_seed_ids_sharing_resolved_work": str(len(group)),
            "outcome_opened": "no",
        })

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    dup_rows = []
    for oa, sids in sorted(duplicate_groups.items()):
        first = res_by_id[sids[0]]
        dup_rows.append({
            "openalex_id": oa,
            "resolved_doi": first["resolved_doi"],
            "resolved_title": first["resolved_title"],
            "seed_ids": ";".join(sids),
            "n_seed_ids": str(len(sids)),
            "canonical_seed_id": sids[0],
            "identity_action": "expand_work_once_preserve_all_seed_provenance",
            "outcome_opened": "no",
        })

    if dup_rows:
        with DUPS.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(dup_rows[0]))
            w.writeheader()
            w.writerows(dup_rows)
    else:
        DUPS.write_text(
            "openalex_id,resolved_doi,resolved_title,seed_ids,n_seed_ids,canonical_seed_id,identity_action,outcome_opened\n",
            encoding="utf-8",
        )

    resolved_seed_units = sum(r["resolution_status"] == "resolved" for r in resolution)
    unresolved_seed_units = len(seeds) - resolved_seed_units
    unique_resolved_works = len(by_work)
    duplicate_excess_seed_units = sum(len(v) - 1 for v in duplicate_groups.values())
    provisional_work_units = unique_resolved_works + unresolved_seed_units

    summary = {
        "schema_version": 1,
        "manifest_seed_units": len(seeds),
        "resolved_seed_units": resolved_seed_units,
        "unique_resolved_works": unique_resolved_works,
        "duplicate_resolved_work_groups": len(duplicate_groups),
        "duplicate_excess_seed_units": duplicate_excess_seed_units,
        "unresolved_seed_units": unresolved_seed_units,
        "provisional_work_identity_units": provisional_work_units,
        "provisional_definition": (
            "unique resolved OpenAlex works plus each unresolved seed retained separately; "
            "not final until unresolved bibliographic identities are adjudicated"
        ),
        "effect_outcomes_opened": False,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    STATUS.write_text(
        f"""# Phase-2 CF01 seed work identity audit — 2026-09-23

## Why this ledger exists

The 363-row CF01 seed manifest is a frozen **search-seed manifest**, not an assumption that all
363 rows are distinct publications.

Bibliographic resolution is allowed to reveal that two or more seed records point to the same
publication. Those records keep their source provenance but the shared publication is expanded
through the citation graph once.

## Current bibliographic identity state

- manifest seed rows: **{len(seeds)}**;
- resolved seed rows: **{resolved_seed_units}**;
- unique resolved OpenAlex works: **{unique_resolved_works}**;
- resolved-work duplicate groups: **{len(duplicate_groups)}**;
- duplicate excess seed rows: **{duplicate_excess_seed_units}**;
- unresolved seed rows: **{unresolved_seed_units}**;
- provisional work-level units: **{provisional_work_units}**.

The provisional work-level denominator equals unique resolved works plus each unresolved seed
retained separately. It is not final until the unresolved bibliographic identities are
adjudicated.

## Citation-expansion rule

For a duplicate resolved-work group:

- fetch backward references once;
- query forward citations once;
- attach every originating seed ID as provenance to discovered candidate edges;
- never count duplicate seed records as independent ecological programmes.

No effect outcome is opened by this identity audit.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF01_SEED_WORK_IDENTITY_OK "
        f"manifest={len(seeds)} resolved={resolved_seed_units} "
        f"unique_resolved={unique_resolved_works} duplicate_groups={len(duplicate_groups)} "
        f"unresolved={unresolved_seed_units} provisional_units={provisional_work_units} "
        "outcomes_opened=false"
    )


if __name__ == "__main__":
    main()
