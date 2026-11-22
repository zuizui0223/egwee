#!/usr/bin/env python3
"""Aggregate-only audit of CropPol measurements and source blocking."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from decimal import Decimal, InvalidOperation
import hashlib
from http.client import HTTPException
import io
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import unquote

import audit_cp001_source_coverage as source

RULE_PATH = Path(__file__).with_name("CP002_METADATA_RULES.json")
RULES = json.loads(RULE_PATH.read_text())
DIRECT = {"reproductive_count_or_set", "harvest_mass_area", "harvest_mass_per_plant",
          "harvest_mass_field", "harvest_mass_fixed_part"}
FRAME_NAMES = (
    "primary_reviewed_direct", "primary_direct_total_visit",
    "primary_direct_timed_observation", "author_use_visits_direct_timed",
    "author_use_abundance_direct", "harvest_mass_area_author_visits",
    "reproductive_author_visits", "primary_organ_quality_total_visit",
)
BASELINE_FRAMES = ("author_use_visits_direct_timed", "harvest_mass_area_author_visits")
BASELINE_FIELDS = ("management", "field_size", "plant_density")


def norm(value: str) -> str:
    return " ".join(value.split()).casefold()


def number(value: str) -> Decimal | None:
    if source.is_missing(value) or not source.NUMERIC.fullmatch(value.strip()):
        return None
    try:
        parsed = Decimal(value)
    except InvalidOperation:
        return None
    return parsed if parsed.is_finite() else None


def endpoint(field: str, label: str) -> str:
    if source.is_missing(label):
        return "missing"
    return RULES["endpoint_labels"][field].get(norm(label), {}).get("family", "unresolved")


def safe_label(field: str, label: str) -> str:
    if source.is_missing(label):
        return "missing"
    return RULES[field].get(norm(label), "unresolved")


def doi_tokens(publication: str) -> set[str]:
    decoded = unquote(publication).casefold()
    tokens = set()
    for token in re.findall(r"10\.[0-9]{4,9}/[^\s;,<>\"']+", decoded):
        token = token.rstrip(".,;:]}>'\"")
        while token.endswith(")") and token.count(")") > token.count("("):
            token = token[:-1]
        tokens.add(token)
    return tokens


def year_stem(study_id: str) -> str:
    # Remove complete year tokens only; author repairs already live in study_id2.
    # Preserve other spelling and suffixes; no fuzzy author-name merging.
    return "_".join(token for token in study_id.split("_")
                    if not re.fullmatch(r"(?:19|20)[0-9]{2}", token))


class Components:
    def __init__(self, keys):
        self.parent = {key: key for key in keys}

    def find(self, key):
        while self.parent[key] != key:
            self.parent[key] = self.parent[self.parent[key]]
            key = self.parent[key]
        return key

    def join(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.parent[max(a, b)] = min(a, b)


def source_components(rows: list[dict], allowed_dois: set[str]):
    groups = sorted({r["_group"] for r in rows})
    observed_groups = {g for g in groups if g[0] == "observed"}
    stems = defaultdict(set)
    dois = defaultdict(set)
    all_dois = set()
    no_doi_rows = 0
    for r in rows:
        found = doi_tokens(r["Publication"])
        all_dois.update(found)
        no_doi_rows += not bool(found)
        if r["_group"] not in observed_groups:
            continue
        if not source.is_missing(r["study_id"]):
            stem = year_stem(r["study_id"])
            if stem:
                stems[stem].add(r["_group"])
        for doi in found & allowed_dois:
            dois[doi].add(r["_group"])

    def build(mappings):
        uf = Components(groups)
        for mapping in mappings:
            for values in mapping.values():
                values = sorted(values)
                for value in values[1:]:
                    uf.join(values[0], value)
        return {g: uf.find(g) for g in groups}

    stem_map, doi_map, union_map = build((stems,)), build((dois,)), build((stems, dois))
    sizes = Counter(union_map[g] for g in observed_groups)
    summary = {
        "provisional_study_id2_groups": len({r["study_id2"] for r in rows
                                            if not source.is_missing(r["study_id2"])}),
        "year_stem_components": len({stem_map[g] for g in observed_groups}),
        "vetted_publication_components": len({doi_map[g] for g in observed_groups}),
        "combined_components": len(sizes),
        "components_including_unresolved_nodes": len(set(union_map.values())),
        "unresolved_source_nodes": len(groups) - len(observed_groups),
        "largest_component_study_id2_groups": max(sizes.values(), default=0),
        "rows_with_no_doi_token": no_doi_rows,
        "distinct_doi_tokens": len(all_dois),
        "vetted_distinct_doi_tokens_present": len(all_dois & allowed_dois),
        "unvetted_distinct_doi_tokens": len(all_dois - allowed_dois),
        "vetted_dois_linking_multiple_study_id2": sum(len(v) > 1 for v in dois.values()),
        "independent_programme_count_verified": False,
        "unvetted_doi_tokens_never_used_as_links": True,
    }
    return union_map, summary


def coverage(rows: list[dict]) -> dict:
    def count(field):
        return len({r[field] for r in rows if not source.is_missing(r[field])})
    return {
        "rows": len(rows), "provisional_study_id2_groups": count("study_id2"),
        "blocking_components": len({r["_component"] for r in rows}),
        "crops": count("crop"), "countries": count("country"),
    }


def baseline_value(row: dict, field: str):
    if field == "management":
        value = safe_label("management", row[field])
        return value if value not in {"missing", "unresolved"} else None
    value = number(row[field])
    return value if value is not None and value > 0 else None


def block_key(row: dict):
    fields = ("crop", "sampling_year", "yield_units", "visitation_rate_units",
              "sampling_visitation", "taxa_recorded")
    if any(source.is_missing(row[f]) for f in fields):
        return None
    return (row["_component"],) + tuple(norm(row[f]) for f in fields)


def baseline_summary(rows: list[dict], fields: tuple[str, ...]) -> dict:
    blocks = defaultdict(list)
    complete_rows = 0
    missing_block_metadata = 0
    for r in rows:
        values = tuple(baseline_value(r, f) for f in fields)
        key = block_key(r)
        if key is not None:
            blocks[key].append((r, values))
            complete_rows += all(v is not None for v in values)
        else:
            missing_block_metadata += 1
    eligible = []
    varying = []
    substantial = []
    duplicate_blocks = 0
    global_duplicate_blocks = 0
    complete_sizes = Counter()
    for key, raw_items in blocks.items():
        raw_keys = {(r["study_id"], r["site_id"], r["sampling_year"]) for r, _ in raw_items}
        duplicate_blocks += len(raw_keys) != len(raw_items)
        items = [(r, values) for r, values in raw_items if all(v is not None for v in values)]
        complete_sizes[str(len(items))] += 1
        if any(r["_key_duplicate_global"] for r, _ in raw_items):
            global_duplicate_blocks += 1
            continue
        keys = {(r["study_id"], r["site_id"], r["sampling_year"]) for r, _ in items}
        if len(keys) != len(items):
            continue
        if len(keys) < 5:
            continue
        eligible.append((key, items))
        frequencies = Counter(v for _, v in items)
        if len(frequencies) > 1:
            varying.append((key, items))
        n = len(items)
        all_pairs = n * (n-1) // 2
        equal_pairs = sum(c*(c-1)//2 for c in frequencies.values())
        if 2 * (all_pairs - equal_pairs) >= all_pairs:
            substantial.append((key, items))
    return {
        "complete_rows": complete_rows, "blocks": len(blocks),
        "rows_missing_block_metadata": missing_block_metadata,
        "block_size_distribution": dict(sorted(Counter(str(len(v)) for v in blocks.values()).items())),
        "complete_case_block_size_distribution": dict(sorted(complete_sizes.items())),
        "blocks_with_duplicate_candidate_keys": duplicate_blocks,
        "blocks_touching_global_duplicate_keys": global_duplicate_blocks,
        "blocks_at_least_five": len(eligible),
        "variable_blocks": len(varying),
        "rows_in_variable_blocks": sum(len(items) for _, items in varying),
        "components_with_variable_blocks": len({key[0] for key, _ in varying}),
        "blocks_at_least_half_pairs_differ": len(substantial),
        "rows_at_least_half_pairs_differ": sum(len(items) for _, items in substantial),
        "candidate_keys_are_not_verified_physical_field_identities": True,
    }


def inspect_csv(raw: bytes, allowed_dois: set[str] | None = None) -> dict:
    reader = csv.reader(io.StringIO(raw.decode("utf-8-sig"), newline=""), strict=True)
    header = next(reader, None)
    if header != source.EXPECTED_COLUMNS:
        raise ValueError("Original source schema differs from the frozen contract")
    rows = []
    for index, cells in enumerate(reader):
        if not cells:
            continue
        if len(cells) != len(header):
            raise ValueError("Original source row width differs from the header")
        r = dict(zip(header, cells))
        # Strings remain transient. No original cells are serialized.
        r = {key: value.strip() for key, value in r.items()}
        r["_group"] = (("observed", r["study_id2"]) if not source.is_missing(r["study_id2"])
                       else ("unresolved", str(index)))
        rows.append(r)
    if not rows:
        raise ValueError("Original source has no data rows")
    allowed = set(RULES["vetted_original_dois"]) if allowed_dois is None else set(allowed_dois)
    components, grouping = source_components(rows, allowed)
    frames = {name: [] for name in FRAME_NAMES}
    families = {"yield": Counter(), "yield2": Counter()}
    categories = {k: Counter() for k in ("selector", "taxa_scope", "visit_method", "visit_unit_family", "management")}
    candidate_keys = Counter()
    for r in rows:
        if all(not source.is_missing(r[f]) for f in ("study_id","site_id","sampling_year")):
            candidate_keys[(r["study_id"],r["site_id"],r["sampling_year"])] += 1
    missing_keys = 0
    invalid_domains = {"primary_direct_negative":0,"primary_percentage_above_100":0,
                       "negative_visitation":0,"negative_abundance":0}
    for r in rows:
        r["_component"] = components[r["_group"]]
        key_names = ("study_id", "study_id2", "site_id", "sampling_year", "crop")
        complete_key = all(not source.is_missing(r[f]) for f in key_names)
        field_key = (r["study_id"],r["site_id"],r["sampling_year"])
        missing_keys += any(source.is_missing(v) for v in field_key)
        r["_key_duplicate_global"] = candidate_keys[field_key] > 1
        primary = endpoint("yield_units", r["yield_units"])
        secondary = endpoint("yield2_units", r["yield2_units"])
        for field, family in (("yield",primary),("yield2",secondary)):
            families[field][family if number(r[field]) is not None else "no_numeric_value"] += 1
        selector = safe_label("selectors", r["use_visits_or_abundance"])
        taxa = safe_label("taxa_scopes", r["taxa_recorded"])
        method = safe_label("visit_methods", r["sampling_visitation"])
        unit = ({"family":"missing","timed":False} if source.is_missing(r["visitation_rate_units"])
                else RULES["visit_units"].get(norm(r["visitation_rate_units"]), {"family":"unresolved","timed":False}))
        for k,v in (("selector",selector),("taxa_scope",taxa),("visit_method",method),
                    ("visit_unit_family",unit["family"]),("management",safe_label("management",r["management"]))):
            categories[k][v] += 1
        y, v, abundance = number(r["yield"]), number(r["visitation_rate"]), number(r["abundance"])
        negative_y = primary in DIRECT and y is not None and y < 0
        percentage = norm(r["yield_units"]) in RULES["primary_true_percentage_labels"]
        invalid_percentage = percentage and y is not None and y > 100
        invalid_domains["primary_direct_negative"] += negative_y
        invalid_domains["primary_percentage_above_100"] += invalid_percentage
        invalid_domains["negative_visitation"] += v is not None and v < 0
        invalid_domains["negative_abundance"] += abundance is not None and abundance < 0
        direct = (complete_key and y is not None and primary in DIRECT
                  and not negative_y and not invalid_percentage)
        total_visit = v is not None and v >= 0
        timed = (total_visit and method == "active_observation_compatible"
                 and unit["timed"] and taxa not in {"missing","unresolved","none"})
        selected_visit = selector == "use_visits" and timed
        selected_abundance = (selector == "use_abundance" and abundance is not None and abundance >= 0
                              and norm(r["sampling_abundance"]) in RULES["abundance_methods"]
                              and taxa not in {"missing","unresolved","none"})
        flags = {
            "primary_reviewed_direct": direct,
            "primary_direct_total_visit": direct and total_visit,
            "primary_direct_timed_observation": direct and timed,
            "author_use_visits_direct_timed": direct and selected_visit,
            "author_use_abundance_direct": direct and selected_abundance,
            "harvest_mass_area_author_visits": direct and primary == "harvest_mass_area" and selected_visit,
            "reproductive_author_visits": direct and primary == "reproductive_count_or_set" and selected_visit,
            "primary_organ_quality_total_visit": complete_key and y is not None and y >= 0
                and primary == "organ_mass_or_quality_component" and total_visit,
        }
        for name, keep in flags.items():
            if keep:
                frames[name].append(r)
    baseline = {}
    for frame_name in BASELINE_FRAMES:
        selected = frames[frame_name]
        baseline[frame_name] = {"all_three": baseline_summary(selected,BASELINE_FIELDS)}
        baseline[frame_name].update({f:baseline_summary(selected,(f,)) for f in BASELINE_FIELDS})
    return {
        "status":"METADATA_AUDITED_NOT_MODEL_ADMISSION",
        "schema_verified":True,
        "schema_sha256":hashlib.sha256(",".join(header).encode()).hexdigest(),
        "model_admission":False, "biological_effect_estimated":False,
        "original_rows_or_IDs_redistributed":False,
        "outcome_magnitudes_or_relationships_computed":False,
        "predictor_only_completeness_and_distinctness_audited":True,
        "total_rows":len(rows), "grouping":grouping,
        "frames":{k:coverage(v) for k,v in frames.items()},
        "outcome_families":{k:dict(sorted(v.items())) for k,v in families.items()},
        "metadata_categories":{k:dict(sorted(v.items())) for k,v in categories.items()},
        "baseline":baseline,
        "invalid_domains":invalid_domains,
        "anomalies":{
            "rows_missing_candidate_keys":missing_keys,
            "duplicate_candidate_keys":sum(n>1 for n in candidate_keys.values()),
            "extra_rows_beyond_candidate_keys":sum(n-1 for n in candidate_keys.values()),
        },
        "unresolved":{
            "independent_programme_identity":True,
            "endpoint_original_construction_and_inferred_pollen_exclusion":True,
            "original_visitation_protocol":True,
            "baseline_covariate_timing_and_derivation":True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",required=True,type=Path)
    args = parser.parse_args()
    manifest = source.MANIFEST
    result = {
        "source_repository":manifest["source_repository"], "release":manifest["release"],
        "commit":manifest["commit"], "path":manifest["path"],
        "source_identity_verified":False, "schema_verified":False,
        "model_admission":False, "biological_effect_estimated":False,
        "original_rows_or_IDs_redistributed":False,
        "rules_sha256":hashlib.sha256(RULE_PATH.read_bytes()).hexdigest(),
    }
    stage = "access"
    try:
        raw = source.fetch_verified_source()
        stage = "identity"
        digest = source.verify_bytes(raw,manifest["expected_bytes"],manifest["expected_git_blob_sha1"])
        result.update(source_actual_sha256=digest,source_actual_bytes=len(raw),
                      source_git_blob_sha1=manifest["expected_git_blob_sha1"],source_identity_verified=True)
        stage = "schema"
        result.update(inspect_csv(raw))
        code = 0
    except (OSError,HTTPException,ValueError,UnicodeError,csv.Error) as exc:
        result.update(status="SOURCE_ACCESS_OR_SCHEMA_STOP",
                      stop_stage="identity" if isinstance(exc,source.SourceIdentityError) else stage,
                      stop_type=type(exc).__name__)
        if isinstance(exc,HTTPError):
            result["stop_http"] = exc.code
        code = 2
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    brief = {k:result[k] for k in ("status","source_identity_verified","model_admission")}
    for k in ("stop_stage","stop_type","stop_http","total_rows","grouping","frames","baseline"):
        if k in result:
            brief[k] = result[k]
    print("CP002_ORIGINAL_MEASUREMENT_SOURCE_AUDIT "+json.dumps(brief,sort_keys=True),flush=True)
    return code

if __name__ == "__main__":
    raise SystemExit(main())
