from __future__ import annotations

import csv
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
    m = re.match(r"^[+-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:[Ee][+-]?\\d+)?", s)
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


def ivw(rows: list[dict]) -> tuple[float, float]:
    vals = [(r["hedges_d"], r["variance"]) for r in rows]
    vals = [(d, v) for d, v in vals if d is not None and v is not None and v > 0]
    if not vals:
        raise ValueError("no finite effect+variance rows")
    w = np.array([1.0 / v for _, v in vals], dtype=float)
    d = np.array([x for x, _ in vals], dtype=float)
    return float(np.sum(w * d) / np.sum(w)), float(1.0 / np.sum(w))


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


def analyse(pairs: list[dict], label: str) -> dict:
    primary = [r for r in pairs if r["compatibility"] in {"SC", "SI"}]
    if len(primary) < 10:
        raise RuntimeError(f"{label}: too few SC/SI pairs: {len(primary)}")

    y = np.array([r["d_F"] for r in primary], dtype=float)
    dI = np.array([r["d_I"] for r in primary], dtype=float)
    sc = np.array([1.0 if r["compatibility"] == "SC" else 0.0 for r in primary])
    groups = [r["source_publication"] for r in primary]

    X = np.column_stack([np.ones(len(primary)), dI, sc])
    main = cluster_fit(y, X, groups)

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
            "n_publications": len({r["source_publication"] for r in rr}),
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

    with zipfile.ZipFile(source) as zf:
        root = ET.fromstring(zf.read("word/document.xml"))
    tables = root.findall(".//" + q("tbl"))
    assert len(tables) == 7, len(tables)

    parsed = []
    for table in tables[1:]:
        for row in table.findall("./" + q("tr")):
            cells = [cell_text(c) for c in row.findall("./" + q("tc"))]
            if not any(cells):
                continue
            parsed.append(parse_metadata(cells))
    assert len(parsed) == 426, len(parsed)

    # Only rows with numeric d and variance can contribute.
    usable = [
        r for r in parsed
        if r["hedges_d"] is not None and r["variance"] is not None and r["variance"] > 0
        and r["response"] in {"Pollination", "Female fitness"}
    ]

    grouped = defaultdict(lambda: defaultdict(list))
    meta = {}
    for r in usable:
        key = (r["source_publication"], r["species"], normalize_land_use(r["land_use_factor"]))
        grouped[key][r["response"]].append(r)
        meta[key] = r

    pairs = []
    for key, rr in grouped.items():
        if not {"Pollination", "Female fitness"} <= set(rr):
            continue
        dI, vI = ivw(rr["Pollination"])
        dF, vF = ivw(rr["Female fitness"])
        base = meta[key]
        comp_vals = {x["compatibility"] for xs in rr.values() for x in xs if x["compatibility"]}
        compatibility = next(iter(comp_vals)) if len(comp_vals) == 1 else "MIXED_METADATA"
        pairs.append({
            "source_publication": key[0],
            "species": key[1],
            "land_use_factor_normalized": key[2],
            "compatibility": compatibility,
            "family": base["family"],
            "pollination_context": base["pollination_context"],
            "d_I": dI,
            "var_I": vI,
            "d_F": dF,
            "var_F": vF,
            "delta_F_minus_I": dF - dI,
            "n_I_rows_combined": len(rr["Pollination"]),
            "n_F_rows_combined": len(rr["Female fitness"]),
        })

    pairs.sort(key=lambda r: (r["source_publication"], r["species"], r["land_use_factor_normalized"]))
    frag = [r for r in pairs if r["land_use_factor_normalized"] == "habitat fragmentation"]

    result = {
        "status": "post_publication_prospectively_specified_reanalysis_of_previously_unopened_row_level_effect_cells",
        "source_rows": len(parsed),
        "usable_pollination_or_female_rows": len(usable),
        "all_exact_paired_units": len(pairs),
        "habitat_fragmentation_exact_paired_units": len(frag),
        "primary": analyse(frag, "habitat_fragmentation_only"),
        "sensitivity_all_land_use": analyse(pairs, "all_land_use_factors"),
    }

    out_csv = outdir / "sf06_translation_residual_pairs_v1.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(pairs[0]))
        writer.writeheader()
        writer.writerows(pairs)

    out_json = outdir / "sf06_translation_residual_result_v1.json"
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    p = result["primary"]
    lines = [
        "# SF06 pollination→female-fitness translation-residual result — 2026-10-06",
        "",
        f"Exact paired units (all land-use): **{len(pairs)}**.",
        f"Exact paired habitat-fragmentation units: **{len(frag)}**.",
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
        "gamma_SC": p["gamma_SC"],
        "ci95": p["gamma_SC_ci95"],
        "p_two_sided": p["gamma_SC_p_two_sided"],
        "decision": p["decision"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
