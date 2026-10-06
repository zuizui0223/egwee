from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np
import statsmodels.api as sm

NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
RESPONSES = ("Female fitness", "Male fitness", "Pollination")
EXPECTED_RESPONSE_COUNTS = {
    "Female fitness": 312,
    "Male fitness": 105,
    "Pollination": 83,
}

ROOT = Path(__file__).resolve().parents[1]
PAIR_MANIFEST = ROOT / "evidence/meta_extraction/phase2_sf06_translation_pair_manifest_v1.csv"
SOURCE_SUMMARY = ROOT / "evidence/meta_extraction/phase2_sf06_source_frame_summary_v1.json"

FROZEN_EGWEE_IF_OVERLAP_PUBLICATIONS = {
    "aizen & feinsinger (1994) ecology 75:330- 351",
    "angoh et al. (2021) south african journal of botany 141:196- 199",
    "chen & zuo (2019) frontiers in plant science 10:327",
    "chen et al. (2019) science of the total environment 654:1056- 1063",
    "chiapero et al. (2021) forest ecology and management 492:119215",
    "da silva elias et al. (2012) journal of tropical ecology 28:317- 320",
    "gonzález-varo et al. (2009) biological conservation 142:1058- 1065",
    "kolb (2008) biological conservation 141:2540- 2549",
    "lopes & buzato (2007) oecologia 154:305- 314",
}


def q(tag: str) -> str:
    return f"{{{NS}}}{tag}"


def cell_text(cell: ET.Element) -> str:
    text = " ".join(
        (t.text or "").strip()
        for t in cell.iter(q("t"))
        if (t.text or "").strip()
    )
    return " ".join(text.split())


def norm_minus(s: str) -> str:
    return s.replace("−", "-").replace("–", "-")


def first_float(s: str) -> float | None:
    s = norm_minus(s).strip()
    m = re.search(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?", s)
    return float(m.group(0)) if m else None


def leading_float(s: str) -> float | None:
    s = norm_minus(s).strip()
    m = re.match(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?", s)
    return float(m.group(0)) if m else None

def strip_variance_from_source(text: str) -> str:
    text = norm_minus(text).strip()
    text = re.sub(r"^(?:NA|N/?A)\s+", "", text, flags=re.I)
    text = re.sub(r"^[+-]?\s*\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?\s+", "", text)
    return text.strip()


def parse_metadata(cells: list[str]) -> dict[str, str]:
    assert len(cells) >= 11, cells
    metadata = cells[:-2]
    species = metadata[0].strip()
    country = metadata[-1].strip()
    source = strip_variance_from_source(cells[-1])
    assert species and source, cells

    response = None
    response_idx = None
    family = ""
    for idx, value in enumerate(metadata[1:-1], start=1):
        for candidate in RESPONSES:
            if candidate.casefold() in value.casefold():
                response = candidate
                response_idx = idx
                lower = value.casefold()
                pos = lower.find(candidate.casefold())
                prefix = value[:pos].strip()
                if prefix:
                    family = prefix
                elif idx > 1:
                    family = metadata[idx - 1].strip()
                break
        if response is not None:
            break
    assert response is not None and response_idx is not None, cells

    land_use = metadata[response_idx + 1].strip()
    trait_cells = [x.strip() for x in metadata[response_idx + 2 : -1] if x.strip()]
    assert len(trait_cells) >= 4, (cells, trait_cells)

    compatibility = trait_cells[0]
    sexual_expression = trait_cells[1]
    life_form = trait_cells[-2]
    ecosystem_type = trait_cells[-1]
    pollination_context = "; ".join(trait_cells[2:-2])

    if not family and response_idx >= 2:
        family = metadata[response_idx - 1].strip()

    d = first_float(cells[-2])
    variance = leading_float(cells[-1])
    return {
        "species": species,
        "family": family,
        "response": response,
        "land_use_factor": land_use,
        "compatibility": compatibility,
        "sexual_expression": sexual_expression,
        "pollination_context": pollination_context,
        "life_form": life_form,
        "ecosystem_type": ecosystem_type,
        "country": country,
        "source_publication": source,
        "hedges_d": d,
        "variance": variance,
    }


def normalize_land_use(x: str) -> str:
    return " ".join(x.casefold().split())


def normalize_publication(x: str) -> str:
    return " ".join(x.casefold().split())


def ivw(rows: list[dict]) -> tuple[float, float]:
    vals = [(r["hedges_d"], r["variance"]) for r in rows]
    if not rows or any(d is None or v is None or v <= 0 for d, v in vals):
        raise ValueError("incomplete constituent effect or variance")
    w = np.array([1.0 / v for _, v in vals], dtype=float)
    d = np.array([x for x, _ in vals], dtype=float)
    return float(np.sum(w * d) / np.sum(w)), float(1.0 / np.sum(w))


def component_consensus_sign(rows: list[dict]) -> str:
    if not rows or any(r["hedges_d"] is None for r in rows):
        return "missing"
    vals = [r["hedges_d"] for r in rows]
    if all(x < 0 for x in vals):
        return "lower"
    if all(x >= 0 for x in vals):
        return "nonlower"
    return "mixed"


def component_resolved_consensus_sign(rows: list[dict]) -> str:
    states = []
    for r in rows:
        d = r["hedges_d"]
        v = r["variance"]
        if d is None or v is None or v <= 0:
            return "unresolved"
        se = math.sqrt(v)
        lo = d - 1.96 * se
        hi = d + 1.96 * se
        if hi < 0:
            states.append("lower")
        elif lo > 0:
            states.append("nonlower")
        else:
            return "unresolved"
    if states and all(x == "lower" for x in states):
        return "lower"
    if states and all(x == "nonlower" for x in states):
        return "nonlower"
    return "unresolved"


def cluster_fit(y: np.ndarray, X: np.ndarray, groups: list[str]) -> dict:
    codes = {g: i for i, g in enumerate(sorted(set(groups)))}
    grp = np.array([codes[g] for g in groups], dtype=int)
    fit = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": grp, "use_correction": True})
    return {
        "params": [float(x) for x in fit.params],
        "se": [float(x) for x in fit.bse],
        "p_two_sided": [float(x) for x in fit.pvalues],
        "ci95": [[float(a), float(b)] for a, b in fit.conf_int(alpha=0.05)],
        "n": int(fit.nobs),
        "n_publications": len(set(groups)),
        "r2": float(fit.rsquared),
    }


def publication_balanced_fit(y: np.ndarray, X: np.ndarray, groups: list[str]) -> dict:
    counts = defaultdict(int)
    for g in groups:
        counts[g] += 1
    weights = np.array([1.0 / counts[g] for g in groups], dtype=float)
    codes = {g: i for i, g in enumerate(sorted(set(groups)))}
    grp = np.array([codes[g] for g in groups], dtype=int)
    fit = sm.WLS(y, X, weights=weights).fit(
        cov_type="cluster", cov_kwds={"groups": grp, "use_correction": True}
    )
    return {
        "params": [float(x) for x in fit.params],
        "se": [float(x) for x in fit.bse],
        "p_two_sided": [float(x) for x in fit.pvalues],
        "ci95": [[float(a), float(b)] for a, b in fit.conf_int(alpha=0.05)],
        "n": int(fit.nobs),
        "n_publications": len(set(groups)),
        "r2": float(fit.rsquared),
    }


def endpoint_resolved_sign(d: float, variance: float) -> str:
    se = math.sqrt(variance)
    lo = d - 1.96 * se
    hi = d + 1.96 * se
    if hi < 0:
        return "lower"
    if lo > 0:
        return "nonlower"
    return "unresolved"


def deterministic_mismatch(
    rows: list[dict],
    state_source: str = "consensus",
    resolved_only: bool = False,
) -> dict:
    counts = defaultdict(lambda: defaultdict(int))
    used = 0
    for r in rows:
        if state_source == "consensus":
            if resolved_only:
                i_state = r["I_resolved_consensus_sign"]
                f_state = r["F_resolved_consensus_sign"]
                if "unresolved" in {i_state, f_state}:
                    continue
            else:
                i_state = r["I_component_consensus_sign"]
                f_state = r["F_component_consensus_sign"]
                if i_state in {"mixed", "missing"} or f_state in {"mixed", "missing"}:
                    continue
        elif state_source == "ivw_hedges_d":
            if r["d_I"] is None or r["d_F"] is None:
                continue
            if resolved_only:
                if r["var_I"] is None or r["var_F"] is None:
                    continue
                i_state = endpoint_resolved_sign(r["d_I"], r["var_I"])
                f_state = endpoint_resolved_sign(r["d_F"], r["var_F"])
                if "unresolved" in {i_state, f_state}:
                    continue
            else:
                i_state = "lower" if r["d_I"] < 0 else "nonlower"
                f_state = "lower" if r["d_F"] < 0 else "nonlower"
        else:
            raise ValueError(state_source)

        counts[i_state][f_state] += 1
        used += 1

    mismatch = 0
    for f_counts in counts.values():
        total = sum(f_counts.values())
        mismatch += total - max(f_counts.values())

    return {
        "n_used": used,
        "counts": {k: dict(v) for k, v in counts.items()},
        "minimum_deterministic_mismatches": int(mismatch),
        "nonidentifying": bool(mismatch > 0),
    }


def topology_audit(pairs: list[dict], label: str) -> dict:
    point = deterministic_mismatch(pairs, state_source="consensus", resolved_only=False)
    consensus_pairs = [
        r for r in pairs
        if r["I_component_consensus_sign"] not in {"mixed", "missing"}
        and r["F_component_consensus_sign"] not in {"mixed", "missing"}
    ]
    pubs = sorted({r["source_publication_key"] for r in consensus_pairs})
    species = sorted({r["species"].casefold() for r in consensus_pairs})

    loo = {}
    for pub in pubs:
        kept = [r for r in pairs if r["source_publication_key"] != pub]
        loo[pub] = deterministic_mismatch(
            kept, state_source="consensus", resolved_only=False
        )["minimum_deterministic_mismatches"]

    species_loo = {}
    for sp in species:
        kept = [r for r in pairs if r["species"].casefold() != sp]
        species_loo[sp] = deterministic_mismatch(
            kept, state_source="consensus", resolved_only=False
        )["minimum_deterministic_mismatches"]

    loo_min = min(loo.values()) if loo else 0
    species_loo_min = min(species_loo.values()) if species_loo else 0
    n_publications = len(pubs)
    n_species = len(species)
    coverage_gate = point["n_used"] >= 10 and n_species >= 10 and n_publications >= 5
    if (
        coverage_gate
        and point["nonidentifying"]
        and loo_min > 0
        and species_loo_min > 0
    ):
        decision = "external_sign_translation_nonidentifiability_supported"
    elif not coverage_gate:
        decision = "external_sign_translation_nonidentifiability_coverage_insufficient"
    elif point["nonidentifying"]:
        decision = "external_sign_translation_nonidentifiability_influence_sensitive"
    else:
        decision = "external_sign_translation_nonidentifiability_not_supported"

    resolved = deterministic_mismatch(
        pairs, state_source="consensus", resolved_only=True
    )
    ivw = deterministic_mismatch(
        pairs, state_source="ivw_hedges_d", resolved_only=False
    )
    return {
        "label": label,
        "component_consensus_sign": point,
        "consensus_n_publications": n_publications,
        "consensus_n_species": n_species,
        "minimum_coverage_gate_passed": bool(coverage_gate),
        "publication_leave_one_out_minimum_mismatches": loo,
        "minimum_mismatch_across_publication_deletions": int(loo_min),
        "publication_LOO_nonidentifying": bool(loo_min > 0),
        "species_leave_one_out_minimum_mismatches": species_loo,
        "minimum_mismatch_across_species_deletions": int(species_loo_min),
        "species_LOO_nonidentifying": bool(species_loo_min > 0),
        "component_resolved_95pct_sign_sensitivity": resolved,
        "ivw_hedges_d_sign_sensitivity": ivw,
        "decision": decision,
        "interpretation": (
            "Primary structural topology uses constituent-row sign consensus before aggregation; "
            "mixed-sign response sets are excluded. Generality requires both publication- and "
            "species-level leave-one-out persistence. IVW Hedges-d sign is representation-specific "
            "sensitivity only. Mismatch counts are not prevalence or prediction-error estimates."
        ),
    }


def analyse(pairs: list[dict], label: str) -> dict:
    primary = [r for r in pairs if r["compatibility"] in {"SC", "SI"}]
    if len(primary) < 10:
        raise RuntimeError(f"{label}: too few SC/SI pairs: {len(primary)}")

    y = np.array([r["d_F"] for r in primary], dtype=float)
    dI = np.array([r["d_I"] for r in primary], dtype=float)
    sc = np.array([1.0 if r["compatibility"] == "SC" else 0.0 for r in primary])
    groups = [r["source_publication_key"] for r in primary]

    X = np.column_stack([np.ones(len(primary)), dI, sc])
    main = cluster_fit(y, X, groups)
    publication_balanced = publication_balanced_fit(y, X, groups)

    delta = y - dI
    Xd = np.column_stack([np.ones(len(primary)), sc])
    delta_fit = cluster_fit(delta, Xd, groups)

    Xi = np.column_stack([np.ones(len(primary)), dI, sc, dI * sc])
    interaction = cluster_fit(y, Xi, groups)

    var_delta = np.array([r["var_I"] + r["var_F"] for r in primary], dtype=float)
    weights = 1.0 / var_delta
    codes = {g: i for i, g in enumerate(sorted(set(groups)))}
    grp = np.array([codes[g] for g in groups], dtype=int)
    wls = sm.WLS(delta, Xd, weights=weights).fit(
        cov_type="cluster", cov_kwds={"groups": grp, "use_correction": True}
    )

    topology = defaultdict(lambda: defaultdict(int))
    for r in primary:
        if r["d_I"] >= 0 and r["d_F"] < 0:
            t = "false_reassurance_point_geometry"
        elif r["d_I"] < 0 and r["d_F"] >= 0:
            t = "apparent_overwarning_buffering_point_geometry"
        elif r["d_I"] < 0 and r["d_F"] < 0:
            t = "concordant_deterioration"
        else:
            t = "concordant_non_deterioration"
        topology[r["compatibility"]][t] += 1

    by_compat = {}
    for c in ("SI", "SC"):
        rr = [r for r in primary if r["compatibility"] == c]
        by_compat[c] = {
            "n": len(rr),
            "n_publications": len({r["source_publication_key"] for r in rr}),
            "mean_d_I": float(np.mean([r["d_I"] for r in rr])),
            "mean_d_F": float(np.mean([r["d_F"] for r in rr])),
            "mean_delta_F_minus_I": float(np.mean([r["d_F"] - r["d_I"] for r in rr])),
        }

    gamma = main["params"][2]
    lo, hi = main["ci95"][2]
    if gamma > 0 and lo > 0:
        decision = "compatibility_translation_modifier_supported"
    elif gamma > 0:
        decision = "directionally_consistent_unresolved"
    else:
        decision = "compatibility_translation_prediction_not_supported"

    return {
        "label": label,
        "primary_model_dF_on_dI_plus_SC": main,
        "publication_balanced_model_dF_on_dI_plus_SC": publication_balanced,
        "gamma_SC": gamma,
        "gamma_SC_ci95": [lo, hi],
        "gamma_SC_p_two_sided": main["p_two_sided"][2],
        "decision": decision,
        "delta_model_F_minus_I_on_SC": delta_fit,
        "interaction_model_dF_on_dI_SC_dIxSC": interaction,
        "zero_covariance_weighted_delta_sensitivity": {
            "gamma_SC": float(wls.params[1]),
            "se": float(wls.bse[1]),
            "p_two_sided": float(wls.pvalues[1]),
            "ci95": [float(x) for x in wls.conf_int(alpha=0.05)[1]],
        },
        "by_compatibility": by_compat,
        "topology_counts": {k: dict(v) for k, v in topology.items()},
    }


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: test_sf06_compatibility_translation_residual.py INPUT.docx OUTPUT_DIR")
    source = Path(sys.argv[1])
    outdir = Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)

    # Hard pre-outcome gates: no numerical SF06 inference is allowed unless
    # the metadata-only pair universe and source hash are already frozen.
    assert PAIR_MANIFEST.is_file(), PAIR_MANIFEST
    assert SOURCE_SUMMARY.is_file(), SOURCE_SUMMARY

    with PAIR_MANIFEST.open(newline="", encoding="utf-8") as fh:
        frozen_manifest = list(csv.DictReader(fh))
    assert frozen_manifest
    assert all(r["outcome_opened"] == "no" for r in frozen_manifest)
    frozen_keys = {
        (
            r["source_publication_key"],
            r["species"],
            r["land_use_factor_normalized"],
        )
        for r in frozen_manifest
    }

    frozen_summary = json.loads(SOURCE_SUMMARY.read_text(encoding="utf-8"))
    actual_source_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    assert actual_source_sha256 == frozen_summary["source_sha256"], (
        actual_source_sha256,
        frozen_summary["source_sha256"],
    )

    with zipfile.ZipFile(source) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    tables = root.findall(".//" + q("tbl"))
    assert len(tables) == 7, len(tables)

    parsed = []
    table_data_rows = []
    for table in tables:
        n_data = 0
        for row in table.findall("./" + q("tr")):
            cells = [cell_text(c) for c in row.findall("./" + q("tc"))]
            if not any(cells) or len(cells) < 11:
                continue
            metadata = cells[:-2]
            has_response = any(
                candidate.casefold() in value.casefold()
                for value in metadata
                for candidate in RESPONSES
            )
            if not has_response:
                continue
            parsed.append(parse_metadata(cells))
            n_data += 1
        table_data_rows.append(n_data)

    response_counts = defaultdict(int)
    for r in parsed:
        response_counts[r["response"]] += 1
    assert dict(response_counts) == EXPECTED_RESPONSE_COUNTS, (
        dict(response_counts),
        table_data_rows,
    )
    assert len(parsed) == sum(EXPECTED_RESPONSE_COUNTS.values()) == 500

    grouped_all = defaultdict(lambda: defaultdict(list))
    meta = {}
    for r in parsed:
        if r["response"] not in {"Pollination", "Female fitness"}:
            continue
        key = (
            normalize_publication(r["source_publication"]),
            r["species"],
            normalize_land_use(r["land_use_factor"]),
        )
        grouped_all[key][r["response"]].append(r)
        meta[key] = r

    parsed_pair_keys = {
        key for key, rr in grouped_all.items()
        if {"Pollination", "Female fitness"} <= set(rr)
    }
    assert parsed_pair_keys == frozen_keys, {
        "missing_from_analysis_parser": sorted(frozen_keys - parsed_pair_keys),
        "unexpected_in_analysis_parser": sorted(parsed_pair_keys - frozen_keys),
    }

    pairs = []
    for key in sorted(frozen_keys):
        rr = grouped_all[key]
        base = meta[key]
        comp_vals = {x["compatibility"] for xs in rr.values() for x in xs if x["compatibility"]}
        compatibility = next(iter(comp_vals)) if len(comp_vals) == 1 else "MIXED_METADATA"

        i_rows = rr["Pollination"]
        f_rows = rr["Female fitness"]
        numeric_eligible = all(
            r["hedges_d"] is not None and r["variance"] is not None and r["variance"] > 0
            for r in i_rows + f_rows
        )
        if numeric_eligible:
            dI, vI = ivw(i_rows)
            dF, vF = ivw(f_rows)
            delta = dF - dI
        else:
            dI = vI = dF = vF = delta = None

        pairs.append({
            "source_publication": base["source_publication"],
            "source_publication_key": key[0],
            "species": key[1],
            "land_use_factor_normalized": key[2],
            "compatibility": compatibility,
            "family": base["family"],
            "pollination_context": base["pollination_context"],
            "numeric_model_eligible": "yes" if numeric_eligible else "no",
            "d_I": dI,
            "var_I": vI,
            "d_F": dF,
            "var_F": vF,
            "delta_F_minus_I": delta,
            "I_component_consensus_sign": component_consensus_sign(i_rows),
            "F_component_consensus_sign": component_consensus_sign(f_rows),
            "I_resolved_consensus_sign": component_resolved_consensus_sign(i_rows),
            "F_resolved_consensus_sign": component_resolved_consensus_sign(f_rows),
            "n_I_rows_combined": len(i_rows),
            "n_F_rows_combined": len(f_rows),
        })

    pairs.sort(key=lambda r: (r["source_publication_key"], r["species"], r["land_use_factor_normalized"]))
    numeric_pairs = [r for r in pairs if r["numeric_model_eligible"] == "yes"]
    frag = [r for r in pairs if r["land_use_factor_normalized"] == "habitat fragmentation"]
    frag_numeric = [r for r in frag if r["numeric_model_eligible"] == "yes"]
    frag_nonoverlap = [
        r for r in frag
        if r["source_publication_key"] not in FROZEN_EGWEE_IF_OVERLAP_PUBLICATIONS
    ]
    frag_nonoverlap_numeric = [
        r for r in frag_nonoverlap if r["numeric_model_eligible"] == "yes"
    ]

    topology_frag = topology_audit(frag, "habitat_fragmentation_only")
    topology_frag_nonoverlap = topology_audit(
        frag_nonoverlap, "habitat_fragmentation_nonoverlap_with_frozen_EGWEE_IF_map"
    )
    topology_all = topology_audit(pairs, "all_land_use_factors")

    result = {
        "status": "post_publication_prospectively_specified_reanalysis_of_previously_unopened_row_level_effect_cells",
        "source_rows": len(parsed),
        "source_sha256": actual_source_sha256,
        "frozen_manifest_pairs": len(frozen_manifest),
        "all_exact_paired_units": len(pairs),
        "numeric_model_eligible_pairs": len(numeric_pairs),
        "habitat_fragmentation_exact_paired_units": len(frag),
        "habitat_fragmentation_numeric_model_eligible_pairs": len(frag_numeric),
        "scale_stable_external_topology": topology_frag,
        "scale_stable_external_topology_nonoverlap_sensitivity": topology_frag_nonoverlap,
        "scale_stable_external_topology_all_land_use_sensitivity": topology_all,
        "primary": analyse(frag_numeric, "habitat_fragmentation_only"),
        "primary_nonoverlap_sensitivity": (
            analyse(frag_nonoverlap_numeric, "habitat_fragmentation_nonoverlap")
            if len([r for r in frag_nonoverlap_numeric if r["compatibility"] in {"SC", "SI"}]) >= 10
            else {
                "status": "not_estimable_fewer_than_10_SC_SI_pairs",
                "n_pairs": len(frag_nonoverlap_numeric),
                "n_SC_SI_pairs": len([
                    r for r in frag_nonoverlap_numeric if r["compatibility"] in {"SC", "SI"}
                ]),
            }
        ),
        "sensitivity_all_land_use": analyse(numeric_pairs, "all_land_use_factors"),
    }

    out_csv = outdir / "sf06_translation_residual_pairs_v1.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(pairs[0]))
        writer.writeheader()
        writer.writerows(pairs)

    out_json = outdir / "sf06_translation_residual_result_v1.json"
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    p = result["primary"]
    topo = result["scale_stable_external_topology"]
    topo_nonoverlap = result["scale_stable_external_topology_nonoverlap_sensitivity"]
    independent_external = (
        topo["decision"] == "external_sign_translation_nonidentifiability_supported"
        and topo_nonoverlap["decision"] == "external_sign_translation_nonidentifiability_supported"
    )
    lines = [
        "# SF06 pollination→female-fitness translation-residual result — 2026-10-06",
        "",
        "## Scale-stable external sign topology",
        "",
        f"- consensus-sign paired units = **{topo['component_consensus_sign']['n_used']}**",
        f"- consensus-sign unique species = **{topo['consensus_n_species']}**",
        f"- minimum deterministic mismatches = **{topo['component_consensus_sign']['minimum_deterministic_mismatches']}**",
        f"- consensus source publications = **{topo['consensus_n_publications']}**",
        f"- minimum coverage gate passed = **{topo['minimum_coverage_gate_passed']}**",
        f"- minimum mismatches after deleting each whole publication = **{topo['minimum_mismatch_across_publication_deletions']}**",
        f"- minimum mismatches after deleting each whole species = **{topo['minimum_mismatch_across_species_deletions']}**",
        f"- decision = **{topo['decision']}**",
        f"- component-resolved-only pairs = **{topo['component_resolved_95pct_sign_sensitivity']['n_used']}**",
        f"- component-resolved-only minimum mismatches = **{topo['component_resolved_95pct_sign_sensitivity']['minimum_deterministic_mismatches']}**",
        f"- IVW-Hedges-d sign sensitivity mismatches = **{topo['ivw_hedges_d_sign_sensitivity']['minimum_deterministic_mismatches']}**",
        f"- non-overlap consensus-sign pairs = **{topo_nonoverlap['component_consensus_sign']['n_used']}**",
        f"- non-overlap source publications = **{topo_nonoverlap['consensus_n_publications']}**",
        f"- non-overlap minimum mismatches = **{topo_nonoverlap['component_consensus_sign']['minimum_deterministic_mismatches']}**",
        f"- non-overlap LOO minimum mismatches = **{topo_nonoverlap['minimum_mismatch_across_publication_deletions']}**",
        f"- independent external generalization = **{independent_external}**",
        "",
        "These mismatch counts certify only whether pollination sign can deterministically identify female-fitness sign in the external paired set. They are not prevalence or prediction-error estimates.",
        "",
        f"Exact paired units (all land-use): **{len(pairs)}**.",
        f"Exact paired habitat-fragmentation units: **{len(frag)}**.",
        f"Numeric-model-eligible habitat-fragmentation units: **{len(frag_numeric)}**.",
        "",
        "## Primary model",
        "",
        "`d_F = alpha + beta*d_I + gamma*SC`, publication-cluster-robust SE.",
        "",
        f"- gamma_SC = **{p['gamma_SC']:.6f}**",
        f"- 95% CI = **[{p['gamma_SC_ci95'][0]:.6f}, {p['gamma_SC_ci95'][1]:.6f}]**",
        f"- two-sided p = **{p['gamma_SC_p_two_sided']:.6g}**",
        f"- decision = **{p['decision']}**",
        "",
        "This tests whether compatibility predicts female-fitness response after conditioning on the paired pollination response. It does not test the marginal SC-vs-SI effect already reported by the source meta-analysis.",
        "",
        "## Claim boundary",
        "",
        "This is a post-publication, prospectively specified reanalysis of row-level source effects that EGWEE had not previously stored or inspected. It does not change the frozen 16-programme denominator and does not establish effective reproductive assurance from compatibility labels alone.",
        "",
    ]
    (Path("manuscript") / "SF06_TRANSLATION_RESIDUAL_RESULT_2026-10-06.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    print("SF06_TRANSLATION_RESIDUAL " + json.dumps({
        "all_pairs": len(pairs),
        "fragmentation_pairs": len(frag),
        "fragmentation_numeric_pairs": len(frag_numeric),
        "gamma_SC": p["gamma_SC"],
        "ci95": p["gamma_SC_ci95"],
        "p_two_sided": p["gamma_SC_p_two_sided"],
        "decision": p["decision"],
        "topology_decision": topo["decision"],
        "topology_consensus_n": topo["component_consensus_sign"]["n_used"],
        "topology_min_mismatches": topo["component_consensus_sign"]["minimum_deterministic_mismatches"],
        "topology_LOO_min_mismatches": topo["minimum_mismatch_across_publication_deletions"],
        "topology_species_LOO_min_mismatches": topo["minimum_mismatch_across_species_deletions"],
        "nonoverlap_topology_decision": topo_nonoverlap["decision"],
        "nonoverlap_topology_min_mismatches": topo_nonoverlap["component_consensus_sign"]["minimum_deterministic_mismatches"],
        "nonoverlap_topology_LOO_min_mismatches": topo_nonoverlap["minimum_mismatch_across_publication_deletions"],
        "independent_external_generalization": independent_external,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
