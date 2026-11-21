#!/usr/bin/env python3
"""Pinned CropPol coverage receipt, with no biological effect calculation."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
from http.client import HTTPException
import io
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

MANIFEST = json.loads(Path(__file__).with_name("CP001_PINNED_SOURCE.json").read_text())
EXPECTED_COLUMNS = MANIFEST["expected_columns"]
MISSING = {"", "na", "nan", "n/a", "null"}
NUMERIC = re.compile(r"^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$")
# Bounded vocabulary fixed before source retrieval. Unrecognized labels are not
# echoed. These aliases summarize coding only; they do not certify units or taxa.
SAFE_CATEGORIES = {
    "yield_units": {
        "kg/ha": "kg/ha", "kg per ha": "kg/ha", "kg per hectare": "kg/ha",
        "kg ha-1": "kg/ha", "kg ha^-1": "kg/ha",
        "kg/plant": "kg/plant", "kg per plant": "kg/plant",
        "fruits/plant": "fruits/plant", "fruits per plant": "fruits/plant",
        "fruit per plant": "fruits/plant", "fruit per branch": "fruits/branch",
        "fruits/branch": "fruits/branch", "fruits per branch": "fruits/branch",
        "fruit set": "fruit_set", "fruit_set": "fruit_set",
        "fruit set (%)": "fruit_set", "% fruit set": "fruit_set",
        "seed set": "seed_set", "seed_set": "seed_set",
        "seed set (%)": "seed_set", "% seed set": "seed_set",
        "seeds/fruit": "seeds/fruit", "seeds per fruit": "seeds/fruit",
        "seeds/plant": "seeds/plant", "seeds per plant": "seeds/plant",
    },
    "use_visits_or_abundance": {
        "visits": "visits", "visitation": "visits", "visitation_rate": "visits",
        "visitation rate": "visits", "abundance": "abundance",
    },
    "taxa_recorded": {
        "all": "all", "all insects": "all_insects", "bees": "bees",
        "all bees": "bees", "wild bees": "wild_bees", "wildbees": "wild_bees",
        "honey bees": "honeybees", "honeybees": "honeybees",
        "wild insects": "wild_insects", "non-bees": "non_bees", "nonbees": "non_bees",
    },
}
VISITS = tuple(c for c in EXPECTED_COLUMNS if c == "visitation_rate" or c.startswith("visit_"))
ABUNDANCE = tuple(c for c in EXPECTED_COLUMNS if c == "abundance" or c.startswith("ab_"))
COUNTS = ("fruits_per_plant", "seeds_per_fruit", "seeds_per_plant")
OTHER_NUMERIC = (
    "yield", "yield2", "yield_treatments_no_pollinators",
    "yield_treatments_pollen_supplement", "yield_treatments_no_pollinators2",
    "yield_treatments_pollen_supplement2", "fruits_per_plant", "fruit_weight",
    "seeds_per_fruit", "seeds_per_plant", "seed_weight", "plant_density",
    "observed_pollinator_richness", "other_pollinator_richness",
    "total_sampled_area", "total_sampled_time", "field_size",
)
NUMERIC_COLUMNS = OTHER_NUMERIC + VISITS + ABUNDANCE
META_COLUMNS = ("study_id", "study_id2", "site_id", "sampling_year", "crop", "country")
LABEL_COLUMNS = ("yield_units", "use_visits_or_abundance", "taxa_recorded")


def is_missing(value: str) -> bool:
    return value.strip().casefold() in MISSING


class SourceIdentityError(ValueError):
    """Downloaded bytes do not match the immutable source contract."""


class PinnedSourceRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Pinned source redirects are forbidden")


def verify_bytes(raw: bytes, expected_size: int, expected_blob: str) -> str:
    if len(raw) != expected_size:
        raise SourceIdentityError("Pinned source byte length mismatch")
    header = b"blob " + str(len(raw)).encode("ascii") + b"\0"
    if hashlib.sha1(header + raw).hexdigest() != expected_blob:
        raise SourceIdentityError("Pinned Git blob hash mismatch")
    return hashlib.sha256(raw).hexdigest()


def fetch_verified_source() -> bytes:
    req = Request(MANIFEST["url"], headers={"User-Agent": "egwee-CP001-source-coverage/1.0"})
    with build_opener(PinnedSourceRedirectHandler()).open(req, timeout=40) as response:
        if response.geturl() != MANIFEST["url"] or urlparse(response.geturl()).scheme != "https":
            raise ValueError("Source response did not retain the exact pinned HTTPS URL")
        raw = response.read(MANIFEST["expected_bytes"] + 1)
    verify_bytes(raw, MANIFEST["expected_bytes"], MANIFEST["expected_git_blob_sha1"])
    return raw


def key_summary(rows: list[dict]) -> dict:
    def complete(row, fields):
        return all(not is_missing(row[f]) for f in fields)

    def unique(fields):
        return {tuple(r[f] for f in fields) for r in rows if complete(r, fields)}

    key_fields = ("study_id", "site_id", "sampling_year")
    keys = Counter(tuple(r[f] for f in key_fields) for r in rows if complete(r, key_fields))
    mapping = defaultdict(set)
    for r in rows:
        if complete(r, ("study_id", "study_id2")):
            mapping[r["study_id"]].add(r["study_id2"])
    duplicated = [n for n in keys.values() if n > 1]
    return {
        "rows": len(rows),
        "distinct_study_id": len(unique(("study_id",))),
        "provisional_study_id2_groups": len(unique(("study_id2",))),
        "distinct_study_year_keys": len(unique(("study_id", "sampling_year"))),
        "distinct_site_keys": len(unique(("study_id", "site_id"))),
        "distinct_site_year_keys": len(keys),
        "distinct_crops": len(unique(("crop",))),
        "distinct_countries": len(unique(("country",))),
        "rows_missing_candidate_key": sum(not complete(r, key_fields) for r in rows),
        "rows_missing_study_id2": sum(is_missing(r["study_id2"]) for r in rows),
        "duplicate_site_year_keys": len(duplicated),
        "rows_in_duplicate_site_year_keys": sum(duplicated),
        "extra_rows_beyond_unique_keys": sum(n - 1 for n in duplicated),
        "study_ids_mapping_to_multiple_study_id2": sum(len(v) > 1 for v in mapping.values()),
    }


def category_label(field: str, value: str) -> str:
    value = " ".join(value.split()).casefold()
    if is_missing(value):
        return "<missing>"
    return SAFE_CATEGORIES[field].get(value, "<unreviewed_label>")


def inspect_csv(raw: bytes) -> dict:
    reader = csv.reader(io.StringIO(raw.decode("utf-8-sig"), newline=""), strict=True)
    header = next(reader, None)
    if header != EXPECTED_COLUMNS:
        raise ValueError("Original source header differs from the frozen 68-column contract")
    position = {name: i for i, name in enumerate(header)}
    availability = {name: {"observed_numeric": 0, "missing": 0, "invalid_nonmissing": 0}
                    for name in NUMERIC_COLUMNS}
    categories = {name: Counter() for name in LABEL_COLUMNS}
    all_meta = []
    coverage_rows = {name: [] for name in (
        "primary_yield_with_units", "primary_yield_any_visit_with_units",
        "primary_yield_total_visit_with_units", "primary_yield_any_abundance_with_units",
        "primary_yield_richness_with_units", "seed_or_fruit_count_any_visit",
    )}
    for cells in reader:
        if not cells:
            continue
        if len(cells) != len(header):
            raise ValueError("Original source row width differs from the frozen header")
        # Retain only counting keys; no contact/email or coordinate values enter outputs.
        meta = {name: cells[position[name]].strip() for name in META_COLUMNS}
        all_meta.append(meta)
        observed = {}
        for name in NUMERIC_COLUMNS:
            value = cells[position[name]].strip()
            state = ("missing" if is_missing(value) else
                     "observed_numeric" if NUMERIC.fullmatch(value) else "invalid_nonmissing")
            availability[name][state] += 1
            observed[name] = state == "observed_numeric"
        for name in LABEL_COLUMNS:
            categories[name][category_label(name, cells[position[name]])] += 1
        has_yield = observed["yield"] and not is_missing(cells[position["yield_units"]])
        has_visit = any(observed[name] for name in VISITS)
        has_abundance = any(observed[name] for name in ABUNDANCE)
        flags = {
            "primary_yield_with_units": has_yield,
            "primary_yield_any_visit_with_units": has_yield and has_visit,
            "primary_yield_total_visit_with_units": has_yield and observed["visitation_rate"],
            "primary_yield_any_abundance_with_units": has_yield and has_abundance,
            "primary_yield_richness_with_units": has_yield and observed["observed_pollinator_richness"],
            "seed_or_fruit_count_any_visit": any(observed[name] for name in COUNTS) and has_visit,
        }
        for name, selected in flags.items():
            if selected:
                coverage_rows[name].append(meta)
    if not all_meta:
        raise ValueError("Original source has no data rows")
    return {
        "status": "SOURCE_COVERAGE_VERIFIED_NOT_MODEL_ADMISSION",
        "model_admission": False,
        "biological_effect_estimated": False,
        "original_rows_or_IDs_redistributed": False,
        "numeric_cell_magnitudes_or_relationships_computed": False,
        "numeric_cells_checked_for_syntax_and_presence_only": True,
        "column_count": len(header),
        "schema_verified": True,
        "schema_sha256": hashlib.sha256(",".join(header).encode("utf-8")).hexdigest(),
        "schema_fingerprint_encoding": "UTF-8 comma-joined ordered headers, no trailing newline",
        "keys": key_summary(all_meta),
        "availability": availability,
        "coverage": {name: key_summary(rows) for name, rows in coverage_rows.items()},
        "categorical_inventory": {name: dict(sorted(counts.items())) for name, counts in categories.items()},
        "independent_study_count_verified": False,
        "endpoint_unit_equivalence_verified": False,
        "sampling_selector_semantics_verified": False,
        "coverage_counts_are_presence_only": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = {"source_repository": MANIFEST["source_repository"], "release": MANIFEST["release"],
              "commit": MANIFEST["commit"], "path": MANIFEST["path"],
              "model_admission": False, "biological_effect_estimated": False,
              "original_rows_or_IDs_redistributed": False,
              "source_identity_verified": False, "schema_verified": False}
    stage = "access"
    try:
        raw = fetch_verified_source()
        # Recheck at the boundary, including when a caller supplies downloaded bytes.
        stage = "identity"
        digest = verify_bytes(raw, MANIFEST["expected_bytes"], MANIFEST["expected_git_blob_sha1"])
        result.update({"source_actual_sha256": digest, "source_actual_bytes": len(raw),
                       "source_git_blob_sha1": MANIFEST["expected_git_blob_sha1"],
                       "source_identity_verified": True})
        stage = "schema"
        result.update(inspect_csv(raw))
        code = 0
    except (OSError, HTTPException, ValueError, UnicodeError, csv.Error) as exc:
        result.update({"status": "SOURCE_ACCESS_OR_SCHEMA_STOP",
                       "stop_stage": "identity" if isinstance(exc, SourceIdentityError) else stage,
                       "stop_type": type(exc).__name__})
        if isinstance(exc, HTTPError):
            result["stop_http"] = exc.code
        # No exception string is copied: source cells and URLs cannot leak via errors.
        code = 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    brief = {k: result[k] for k in ("status", "source_identity_verified", "model_admission")}
    for k in ("stop_type", "stop_http", "stop_stage", "keys", "coverage"):
        if k in result:
            brief[k] = result[k]
    print("CP001_ORIGINAL_SOURCE_COVERAGE " + json.dumps(brief, sort_keys=True), flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
