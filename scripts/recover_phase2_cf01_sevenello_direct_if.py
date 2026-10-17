from __future__ import annotations

import csv
import io
import json
import math
import statistics as stats
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_figshare_manifest_v1.json"
CONTRACT = ROOT / "manuscript/CF01_SEVENELLO_2026_DIRECT_IF_RECOVERY_CONTRACT.md"
VALUES = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_transect_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_direct_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_direct_covariance_v1.json"
RESULT = ROOT / "manuscript/PHASE2_CF01_SEVENELLO_DIRECT_IF_RECOVERY_2026-09-25.md"

PROGRAMME = "P2_CF01_SEVENELLO_2026"
PRIMARY_SPECIES = ("GORO", "LARO", "POAR")
SENSITIVITY_SPECIES = ("POGN",)
EXPECTED_N = {
    "GORO": (6, 6),
    "LARO": (8, 8),
    "POAR": (6, 6),
    "POGN": (6, 5),
}
UA = "egwee-sevenello-recovery/1.0"
Z975 = 1.959963984540054

SITE_MAP = {
    "LathamPrivate": "Latham Private",
    "MayaPrivate": "Maya Private",
    "XantippeEast": "Xantippe East",
    "XantippeTank": "Xantippe Tank",
    "WA12427": "WA12427",
    "WA12428": "WA12427",
    "WA12429": "WA12427",
    "WA12430": "WA12427",
}


def download(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read().decode("utf-8-sig")


def norm_site(site: str) -> str:
    return SITE_MAP.get(site, site)


def key(site: str, crop: str, transect: str) -> tuple[str, str, str]:
    return norm_site(site), crop, transect


def pearson(x: list[float], y: list[float]) -> float:
    assert len(x) == len(y) and len(x) >= 4
    mx, my = stats.mean(x), stats.mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    sx = sum(v * v for v in dx)
    sy = sum(v * v for v in dy)
    assert sx > 0 and sy > 0
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(sx * sy)


def centered(values: list[float], groups: list[str]) -> list[float]:
    means = {
        g: stats.mean(v for v, gg in zip(values, groups) if gg == g)
        for g in sorted(set(groups))
    }
    return [v - means[g] for v, g in zip(values, groups)]


def hedges_g_metafor_ls(fragmented: list[float], reference: list[float]) -> tuple[float, float]:
    n1, n2 = len(fragmented), len(reference)
    assert n1 >= 2 and n2 >= 2
    m1, m2 = stats.mean(fragmented), stats.mean(reference)
    s1, s2 = stats.stdev(fragmented), stats.stdev(reference)
    df = n1 + n2 - 2
    pooled = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / df)
    assert pooled > 0
    d = (m1 - m2) / pooled
    j = 1 - 3 / (4 * df - 1)
    g = j * d
    variance = 1 / n1 + 1 / n2 + g**2 / (2 * (n1 + n2))
    return g, variance


def normal_p(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_name = {f["name"]: f for f in manifest["files"]}

    bee_rows = list(csv.DictReader(io.StringIO(download(by_name["landscape_bees.csv"]["download_url"]))))
    seed_rows = list(csv.DictReader(io.StringIO(download(by_name["landscape_seeds.csv"]["download_url"]))))

    # One source bee value per normalized transect.
    bees: dict[tuple[str, str, str], float] = {}
    raw_aliases: dict[tuple[str, str, str], str] = {}
    for r in bee_rows:
        k = key(r["site"], r["crop"], r["transect"])
        assert k not in bees, ("duplicate normalized bee key", k)
        bees[k] = float(r["all_bees"])
        raw_aliases[k] = r["site"]
    assert len(bees) == 20

    # One mean natural/open seed-production value per species x transect.
    # Missingness handling is frozen in the 2026-09-25 amendment: literal NA/blank
    # plant rows are excluded, never recoded as zero.
    fvals: dict[tuple[str, str, str, str], list[float]] = defaultdict(list)
    planned: Counter[tuple[str, str, str, str]] = Counter()
    for r in seed_rows:
        if r["treat"] != "OP":
            continue
        site = norm_site(r["site"])
        fkey = (r["species"], site, r["crop_type"], r["transect"])
        planned[fkey] += 1
        raw = (r["total_seeds"] or "").strip()
        if raw in {"", "NA"}:
            continue
        fvals[fkey].append(float(raw))

    assert planned and all(n == 10 for n in planned.values())
    assert all(fvals.get(k) for k in planned), "entire OP transect missing after amendment"
    fmean = {k: stats.mean(fvals[k]) for k in planned}

    panel_rows: dict[str, list[dict[str, object]]] = {}
    for species in (*PRIMARY_SPECIES, *SENSITIVITY_SPECIES):
        rows = []
        for (sp, site, crop, transect), f_value in sorted(fmean.items()):
            if sp != species:
                continue
            k = (site, crop, transect)
            if k not in bees:
                continue
            rows.append(
                {
                    "programme_id": PROGRAMME,
                    "species": species,
                    "site": site,
                    "crop": crop,
                    "transect": transect,
                    "bee_source_site_label": raw_aliases[k],
                    "I_all_bees": bees[k],
                    "F_mean_total_seeds_OP": f_value,
                    "n_OP_planned": planned[(sp, site, crop, transect)],
                    "n_OP_nonmissing": len(fvals[(sp, site, crop, transect)]),
                    "primary_or_sensitivity": (
                        "primary" if species in PRIMARY_SPECIES else "sensitivity"
                    ),
                }
            )
        panel_rows[species] = rows

        n_edge = sum(r["transect"] == "Edge" for r in rows)
        n_core = sum(r["transect"] == "Core" for r in rows)
        assert (n_edge, n_core) == EXPECTED_N[species], (
            species, n_edge, n_core, rows
        )

    # Verify the one known structural I missingness in POGN.
    assert ("POGN", "Maya", "Wheat", "Core") in fmean
    assert ("Maya", "Wheat", "Core") not in bees
    assert len(panel_rows["POGN"]) == 11

    VALUES.parent.mkdir(parents=True, exist_ok=True)
    value_fields = [
        "programme_id", "species", "site", "crop", "transect",
        "bee_source_site_label", "I_all_bees", "F_mean_total_seeds_OP",
        "n_OP_planned", "n_OP_nonmissing", "primary_or_sensitivity",
    ]
    with VALUES.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=value_fields)
        w.writeheader()
        for species in (*PRIMARY_SPECIES, *SENSITIVITY_SPECIES):
            for row in panel_rows[species]:
                w.writerow(row)

    effects = []
    cov_blocks = {}
    primary_ps = []

    for species in (*PRIMARY_SPECIES, *SENSITIVITY_SPECIES):
        rows = panel_rows[species]
        groups = [str(r["transect"]) for r in rows]
        i_values = [float(r["I_all_bees"]) for r in rows]
        f_values = [float(r["F_mean_total_seeds_OP"]) for r in rows]

        i_edge = [x for x, g in zip(i_values, groups) if g == "Edge"]
        i_core = [x for x, g in zip(i_values, groups) if g == "Core"]
        f_edge = [x for x, g in zip(f_values, groups) if g == "Edge"]
        f_core = [x for x, g in zip(f_values, groups) if g == "Core"]

        gi, vi = hedges_g_metafor_ls(i_edge, i_core)
        gf, vf = hedges_g_metafor_ls(f_edge, f_core)

        rho = pearson(centered(i_values, groups), centered(f_values, groups))
        cov = rho * math.sqrt(vi * vf)
        det = vi * vf - cov * cov
        assert det > 0, (species, det)

        delta = gi - gf
        dvar = vi + vf - 2 * cov
        assert dvar > 0
        dse = math.sqrt(dvar)
        z = delta / dse
        p = normal_p(z)
        lo = delta - Z975 * dse
        hi = delta + Z975 * dse

        tier = "primary" if species in PRIMARY_SPECIES else "sensitivity"
        if tier == "primary":
            primary_ps.append(p)

        effects.extend(
            [
                {
                    "programme_id": PROGRAMME,
                    "species": species,
                    "layer": "I",
                    "endpoint": "all_bees_per_transect",
                    "effect_stream": "hedges_g_direct",
                    "fragmented_group": "Edge",
                    "reference_group": "Core",
                    "n_fragmented": len(i_edge),
                    "n_reference": len(i_core),
                    "hedges_g": f"{gi:.12f}",
                    "variance": f"{vi:.12f}",
                    "primary_or_sensitivity": tier,
                    "orientation_note": "negative = lower total bee abundance at Edge than Core",
                },
                {
                    "programme_id": PROGRAMME,
                    "species": species,
                    "layer": "F",
                    "endpoint": "mean_total_viable_seeds_per_OP_plant",
                    "effect_stream": "hedges_g_direct",
                    "fragmented_group": "Edge",
                    "reference_group": "Core",
                    "n_fragmented": len(f_edge),
                    "n_reference": len(f_core),
                    "hedges_g": f"{gf:.12f}",
                    "variance": f"{vf:.12f}",
                    "primary_or_sensitivity": tier,
                    "orientation_note": "negative = lower natural open seed production at Edge than Core",
                },
            ]
        )

        cov_blocks[species] = {
            "primary_or_sensitivity": tier,
            "n_edge": len(i_edge),
            "n_core": len(i_core),
            "transect_keys": [
                f"{r['site']}|{r['crop']}|{r['transect']}" for r in rows
            ],
            "I_g": gi,
            "F_g": gf,
            "I_variance": vi,
            "F_variance": vf,
            "residual_correlation_IF": rho,
            "sampling_covariance_proxy_IF": cov,
            "covariance_determinant": det,
            "positive_definite": True,
            "I_minus_F": {
                "delta": delta,
                "variance": dvar,
                "se": dse,
                "z": z,
                "p_two_sided": p,
                "ci95": [lo, hi],
            },
        }

    programme_p = min(1.0, len(PRIMARY_SPECIES) * min(primary_ps))
    result = {
        "programme_id": PROGRAMME,
        "status": "direct_IF_three_panel_covariance_aware",
        "primary_species": list(PRIMARY_SPECIES),
        "sensitivity_species": list(SENSITIVITY_SPECIES),
        "primary_fragmentation_contrast": "Edge_minus_Core",
        "I_endpoint": "all_bees_per_transect",
        "F_endpoint": "mean_total_viable_seeds_per_OP_plant",
        "covariance_method": "group_centered_transect_pair_proxy",
        "panels": cov_blocks,
        "programme_internal_bonferroni_p": programme_p,
        "direct_IF_programme_increment": 1,
        "phase1_frozen_synthesis_increment": 0,
        "retrospective_recovery": True,
    }
    COV.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    effect_fields = [
        "programme_id", "species", "layer", "endpoint", "effect_stream",
        "fragmented_group", "reference_group", "n_fragmented", "n_reference",
        "hedges_g", "variance", "primary_or_sensitivity", "orientation_note",
    ]
    with EFFECTS.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=effect_fields)
        w.writeheader()
        w.writerows(effects)

    lines = [
        "# CFTQ0001 Sevenello direct I-F recovery — 2026-09-25",
        "",
        "## Admission",
        "",
        "The frozen raw-data recovery succeeded for all three primary species panels.",
        "",
        "- programme status: **direct I-F three-panel covariance-aware**",
        "- programme count increment in pair-specific direct I-F coverage: **+1**",
        "- Phase-1 frozen five-cluster synthesis increment: **0**",
        f"- internal three-panel Bonferroni p: **{programme_p:.6g}**",
        "",
        "## Primary panels",
        "",
    ]
    for species in PRIMARY_SPECIES:
        b = cov_blocks[species]
        pair = b["I_minus_F"]
        lines += [
            f"### {species}",
            "",
            f"- n Edge/Core: **{b['n_edge']} / {b['n_core']}**",
            f"- I Hedges g: **{b['I_g']:+.3f}**",
            f"- F Hedges g: **{b['F_g']:+.3f}**",
            f"- rho(I,F): **{b['residual_correlation_IF']:+.3f}**",
            f"- I - F: **{pair['delta']:+.3f}**",
            f"- 95% CI: **[{pair['ci95'][0]:+.3f}, {pair['ci95'][1]:+.3f}]**",
            f"- p: **{pair['p_two_sided']:.4g}**",
            "",
        ]

    b = cov_blocks["POGN"]
    pair = b["I_minus_F"]
    lines += [
        "## POGN sensitivity",
        "",
        "POGN remains sensitivity only because Edge/Core are not source-paired in the same remnants",
        "and one plant transect (Maya/Wheat/Core) has no public bee row.",
        "",
        f"- n Edge/Core common I-F frame: **{b['n_edge']} / {b['n_core']}**",
        f"- I Hedges g: **{b['I_g']:+.3f}**",
        f"- F Hedges g: **{b['F_g']:+.3f}**",
        f"- I - F: **{pair['delta']:+.3f}**",
        f"- p: **{pair['p_two_sided']:.4g}**",
        "",
        "## Scope",
        "",
        "This programme can increase the pair-specific direct I-F coverage gate from 1/5 to 2/5.",
        "It does not reopen or modify the frozen Phase-1 five-cluster Fisher synthesis and does not",
        "validate an EGWE/NEE finite operator.",
        "",
    ]
    RESULT.write_text("\n".join(lines), encoding="utf-8")

    print(
        "PHASE2_CF01_SEVENELLO_OK "
        + " ".join(
            f"{sp}_I={cov_blocks[sp]['I_g']:.8f} "
            f"{sp}_F={cov_blocks[sp]['F_g']:.8f} "
            f"{sp}_p={cov_blocks[sp]['I_minus_F']['p_two_sided']:.8f}"
            for sp in PRIMARY_SPECIES
        )
        + f" programme_p={programme_p:.8f} direct_IF_increment=1"
    )


if __name__ == "__main__":
    main()
