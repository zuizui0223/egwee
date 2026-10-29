from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIGDIR = ROOT / "manuscript/figures"
TABLEDIR = ROOT / "manuscript/tables"
ML020_EFFECTS = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_effects_v1.csv"
WANDOO_EFFECTS = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv"
CARDIO_EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_effects_v1.csv"
BERGSDORF_EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_effects_v1.csv"
IF_CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
MATING_FUNCTION_CENSUS = ROOT / "evidence/meta_extraction/ecological_mating_function_programme_census_v1.csv"
PROCESS_FUNCTION_CENSUS = ROOT / "evidence/meta_extraction/ecological_process_function_programme_census_v1.csv"
IF_SIGN_GEOMETRY = ROOT / "evidence/meta_extraction/if_sign_geometry_census_v1.csv"
IF_SIGN_UNCERTAINTY = ROOT / "evidence/meta_extraction/if_sign_uncertainty_v1.csv"
QUALITATIVE_EXTERNAL_IF = ROOT / "evidence/meta_extraction/qualitative_external_if_audit_v1.csv"
PROXY_FAILURE = ROOT / "evidence/meta_extraction/scale_stable_quantity_function_proxy_failure_v1.csv"
IF_TRANSLATION_MAP = ROOT / "evidence/meta_extraction/if_translation_map_v1.csv"
IF_RELIABILITY = ROOT / "evidence/meta_extraction/if_reliability_sufficiency_v1.csv"
SF06_RESULT = ROOT / "evidence/meta_extraction/sf06_translation_residual_result_v1.json"
SCALE_EFFECTS = ROOT / "evidence/meta_extraction/estimand_scale_sensitivity_v1.csv"
SCALE_SUMMARY = ROOT / "evidence/meta_extraction/estimand_scale_cluster_summary_v2.csv"
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
REGISTRY_ML020 = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_extension_ml020.csv"
SYNTHESIS = ROOT / "scripts/synthesize_state_separation.py"
DISPLAY_TOL = 5e-8


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def canonical_result() -> dict:
    proc = subprocess.run(
        [sys.executable, str(SYNTHESIS)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    line = next(
        (x for x in proc.stdout.splitlines() if x.startswith("EGWEE_STATE_SEPARATION ")),
        None,
    )
    if line is None:
        raise AssertionError("canonical synthesis did not emit EGWEE_STATE_SEPARATION")
    result = json.loads(line.split(" ", 1)[1])
    assert result["n_primary_independent_clusters"] == 5
    assert result["n_primary_effects"] == 17
    assert abs(float(result["primary_combined_p"]) - 0.01212432) < DISPLAY_TOL
    return result


def svg_text(x: float, y: float, text: str, *, size: int = 13, anchor: str = "start", weight: str = "normal") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial,Helvetica,sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}">{escape(text)}</text>'
    )


def write_svg(path: Path, width: int, height: int, body: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        *body,
        '</svg>',
    ]
    path.write_text("\n".join(content) + "\n", encoding="utf-8")


def figure1_coverage() -> None:
    width, height = 980, 470
    left, top = 285, 105
    cell_w, cell_h = 100, 58
    layers = ["I", "C", "F", "G adult", "G mating", "G offspring"]
    cluster_rows = [
        ("ML001", "Serapias lingua", {"C": "1", "F": "1", "G adult": "1"}),
        ("ML002", "Brosimum alicastrum", {"C": "1", "F": "1"}),
        ("ML003", "Spondias purpurea", {"C": "1", "G adult": "1", "G offspring": "2 cohorts"}),
        ("ML014", "Eucalyptus socialis", {"F": "1", "G mating": "1"}),
        ("ML020", "Chaco programme", {"I": "3 spp", "F": "3 spp"}),
    ]
    body: list[str] = [svg_text(30, 35, "Figure 1. Primary direct-effect evidence geometry", size=18, weight="bold")]
    body.append(svg_text(30, 60, "Filled cells are admitted primary layers; ML020 species share one programme cluster.", size=12))

    for j, layer in enumerate(layers):
        x = left + j * cell_w + cell_w / 2
        body.append(svg_text(x, top - 20, layer, anchor="middle", weight="bold"))

    for i, (cid, system, coverage) in enumerate(cluster_rows):
        y = top + i * cell_h
        body.append(svg_text(30, y + 24, cid, weight="bold"))
        body.append(svg_text(88, y + 24, system, size=12))
        for j, layer in enumerate(layers):
            x = left + j * cell_w
            present = layer in coverage
            fill = "#d9d9d9" if present else "white"
            body.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="{fill}" stroke="black" stroke-width="1"/>'
            )
            if present:
                body.append(svg_text(x + cell_w / 2, y + 34, coverage[layer], anchor="middle", size=12, weight="bold"))

    y0 = top + len(cluster_rows) * cell_h + 28
    body.append(svg_text(30, y0, "Independent denominator: 5 programme/study clusters; marginal effects: 17.", size=12, weight="bold"))
    body.append(svg_text(30, y0 + 22, "Missing cells are missing layers, not zero biological effects.", size=12))
    write_svg(FIGDIR / "figure1_primary_evidence_geometry.svg", width, height, body)


def log_x(p: float, xmin: float, xmax: float, x0: float, x1: float) -> float:
    lp = math.log10(p)
    lmin, lmax = math.log10(xmin), math.log10(xmax)
    return x0 + (lp - lmin) / (lmax - lmin) * (x1 - x0)


def figure2_influence(result: dict) -> None:
    width, height = 980, 500
    x0, x1 = 340, 910
    xmin, xmax = 0.0025, 0.3
    full = float(result["primary_combined_p"])
    loo = {r["dropped_cluster"]: float(r["combined_p"]) for r in result["primary_leave_one_cluster_out"]}
    expected = {
        "ML001": 0.18194352880824005,
        "ML002": 0.01276794,
        "ML003": 0.01407214,
        "ML014": 0.02116199,
        "ML020": 0.00384724,
    }
    for key, val in expected.items():
        assert abs(loo[key] - val) < 5e-8, (key, loo[key], val)

    entries = [
        ("Full five-cluster synthesis", full),
        ("Omit ML001 Serapias", loo["ML001"]),
        ("Omit ML002 Brosimum", loo["ML002"]),
        ("Omit ML003 Spondias", loo["ML003"]),
        ("Omit ML014 E. socialis", loo["ML014"]),
        ("Omit ML020 Chaco", loo["ML020"]),
    ]
    body: list[str] = [svg_text(30, 35, "Figure 2. Historical Hedges-g leave-one-cluster-out influence", size=18, weight="bold")]
    body.append(svg_text(30, 60, "Registered primary estimand only; Figure 4 shows that this robustness classification is not scale-invariant.", size=11))

    axis_y = 420
    body.append(f'<line x1="{x0}" y1="{axis_y}" x2="{x1}" y2="{axis_y}" stroke="black" stroke-width="1.5"/>')
    ticks = [0.003, 0.01, 0.05, 0.1, 0.3]
    for tick in ticks:
        x = log_x(tick, xmin, xmax, x0, x1)
        body.append(f'<line x1="{x:.1f}" y1="{axis_y}" x2="{x:.1f}" y2="{axis_y + 7}" stroke="black"/>')
        body.append(svg_text(x, axis_y + 25, f"{tick:g}", anchor="middle", size=11))
    body.append(svg_text((x0 + x1) / 2, axis_y + 52, "Combined Fisher p-value (log scale)", anchor="middle", size=12, weight="bold"))

    threshold_x = log_x(0.05, xmin, xmax, x0, x1)
    body.append(f'<line x1="{threshold_x:.1f}" y1="88" x2="{threshold_x:.1f}" y2="{axis_y}" stroke="black" stroke-dasharray="5,5"/>')
    body.append(svg_text(threshold_x + 6, 92, "0.05", size=10))

    for i, (label, pval) in enumerate(entries):
        y = 115 + i * 48
        x = log_x(pval, xmin, xmax, x0, x1)
        body.append(svg_text(30, y + 5, label, size=12, weight="bold" if i == 1 else "normal"))
        body.append(f'<circle cx="{x:.1f}" cy="{y}" r="6" fill="black"/>')
        body.append(svg_text(min(x + 12, x1 - 75), y + 5, f"p={pval:.4g}", size=11))

    write_svg(FIGDIR / "figure2_leave_one_out_influence.svg", width, height, body)


def draw_effect_pair_panel(
    body: list[str],
    *,
    px: float,
    py: float,
    pw: float,
    ph: float,
    title: str,
    subtitle: str,
    pairs: list[tuple[str, float, float]],
    lo: float,
    hi: float,
    ticks: list[float],
    footer: str,
) -> None:
    label_w = 145
    x0 = px + label_w
    x1 = px + pw - 24
    axis_y = py + ph - 48
    plot_top = py + 70
    plot_bottom = axis_y - 28

    def sx(v: float) -> float:
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    body.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="white" stroke="black" stroke-width="1"/>')
    body.append(svg_text(px + 12, py + 24, title, size=14, weight="bold"))
    body.append(svg_text(px + 12, py + 45, subtitle, size=10))

    if lo <= 0 <= hi:
        zx = sx(0.0)
        body.append(f'<line x1="{zx:.1f}" y1="{plot_top - 8:.1f}" x2="{zx:.1f}" y2="{axis_y:.1f}" stroke="black" stroke-dasharray="4,4"/>')

    body.append(f'<line x1="{x0:.1f}" y1="{axis_y:.1f}" x2="{x1:.1f}" y2="{axis_y:.1f}" stroke="black" stroke-width="1.2"/>')
    for tick in ticks:
        tx = sx(tick)
        body.append(f'<line x1="{tx:.1f}" y1="{axis_y:.1f}" x2="{tx:.1f}" y2="{axis_y + 5:.1f}" stroke="black"/>')
        body.append(svg_text(tx, axis_y + 20, f"{tick:g}", anchor="middle", size=9))

    n = len(pairs)
    if n == 1:
        ys = [(plot_top + plot_bottom) / 2]
    else:
        step = (plot_bottom - plot_top) / (n - 1)
        ys = [plot_top + i * step for i in range(n)]

    for y, (label, i_eff, f_eff) in zip(ys, pairs):
        xi = sx(i_eff)
        xf = sx(f_eff)
        body.append(svg_text(px + 12, y + 4, label, size=10, weight="bold"))
        body.append(f'<line x1="{xi:.1f}" y1="{y:.1f}" x2="{xf:.1f}" y2="{y:.1f}" stroke="black" stroke-width="1.5"/>')
        body.append(f'<circle cx="{xi:.1f}" cy="{y:.1f}" r="5" fill="white" stroke="black" stroke-width="1.5"/>')
        body.append(f'<rect x="{xf - 5:.1f}" y="{y - 5:.1f}" width="10" height="10" fill="black"/>')
        body.append(svg_text(xi, y - 9, f"I {i_eff:+.2f}", anchor="middle", size=9))
        body.append(svg_text(xf, y + 18, f"F {f_eff:+.2f}", anchor="middle", size=9))

    body.append(svg_text(px + 12, py + ph - 12, footer, size=9))


def figure3_if_sign_geometry() -> None:
    census = rows(IF_SIGN_GEOMETRY)
    uncertainty = rows(IF_SIGN_UNCERTAINTY)
    proxy = rows(PROXY_FAILURE)

    assert len(census) == len(uncertainty) == 18
    assert len({r["programme_id"] for r in census}) == 8
    assert len(proxy) == 3

    proxy_ids = {r["programme_id"] for r in proxy}
    assert proxy_ids == {
        "ML015",
        "P2_CF01_CARDIOPETALUM_2012",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
    }

    point_opp = [r for r in uncertainty if r["point_opposite_sign"] == "yes"]
    both_resolved = [r for r in uncertainty if r["discordance_strength"] == "both_endpoints_resolved_opposite"]
    one_resolved = [r for r in uncertainty if r["discordance_strength"] == "one_endpoint_resolved_opposite"]
    both_unresolved = [r for r in uncertainty if r["discordance_strength"] == "both_endpoints_unresolved_opposite"]
    assert len(point_opp) == 6
    assert len({r["programme_id"] for r in point_opp}) == 5
    assert len(both_resolved) == 0
    assert len(one_resolved) == 2
    assert len(both_unresolved) == 4

    multi: dict[str, list[str]] = {}
    for r in census:
        multi.setdefault(r["programme_id"], []).append(r["sign_geometry"])
    multi = {k: v for k, v in multi.items() if len(v) > 1}
    assert len(multi) == 4
    assert sum(len(set(v)) > 1 for v in multi.values()) == 3

    programme_label = {
        "ML015": "Eucalyptus wandoo",
        "P2_CF01_CARDIOPETALUM_2012": "Cardiopetalum",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006": "Kakamega Acanthopale",
    }

    width, height = 1240, 760
    body: list[str] = [
        svg_text(30, 34, "Figure 3. Scale-stable interaction–function proxy failure and sign uncertainty", size=18, weight="bold"),
        svg_text(30, 58, "Resolved matched mismatches are separated from descriptive opposite-sign point estimates.", size=11),
        svg_text(35, 100, "A. Representation-stable downstream mismatches", size=14, weight="bold"),
        svg_text(35, 124, "In all three programmes, reproductive function is more negatively affected than measured interaction/pollen quantity.", size=10),
        svg_text(35, 160, "Programme", size=11, weight="bold"),
        svg_text(270, 160, "Region / family", size=11, weight="bold"),
        svg_text(535, 160, "Interaction metric", size=11, weight="bold"),
        svg_text(785, 160, "Reproductive metric", size=11, weight="bold"),
        svg_text(1040, 160, "Robustness basis", size=11, weight="bold"),
    ]

    y = 194
    for row in proxy:
        pid = row["programme_id"]
        label = programme_label[pid]
        region_family = f'{row["region"]} / {row["plant_family"]}'
        interaction = row["interaction_metric"].replace("_", " ")
        function = row["function_metric"].replace("_", " ")
        basis = (
            "sign inversion + resolved I–F"
            if pid == "ML015"
            else "g + lnRR resolved"
            if pid == "P2_CF01_BERGSDORF_KAKAMEGA_2006"
            else "gradient I–F resolved"
        )
        body.append(svg_text(35, y, label, size=10, weight="bold"))
        body.append(svg_text(270, y, region_family, size=9))
        body.append(svg_text(535, y, interaction, size=9))
        body.append(svg_text(785, y, function, size=9))
        body.append(svg_text(1040, y, basis, size=9))
        y += 48

    body.append(svg_text(35, y + 8, "Stable resolved upstream I–F programmes: 0", size=10, weight="bold"))
    body.append(svg_text(35, y + 32, "Complete registered I–F denominator: 8 programmes; all 8 interaction endpoints are quantity-level.", size=10))
    body.append(svg_text(35, y + 54, "Direct effective-mating-quality endpoints on the same I–F frame: 0 / 8.", size=10))

    section_y = y + 100
    body.append(f'<line x1="30" y1="{section_y - 22:.1f}" x2="1210" y2="{section_y - 22:.1f}" stroke="black" stroke-width="1.2"/>')
    body.append(svg_text(35, section_y, "B. Opposite-sign point geometry: useful, but mostly unresolved", size=14, weight="bold"))

    stats = [
        ("Opposite-sign point estimates", "6 / 18 panels", "5 independent programmes"),
        ("Both endpoint directions resolved opposite", "0 / 6", "no confirmed marginal sign reversal"),
        ("One endpoint resolved, one unresolved", "2 / 6", "Wandoo; Kakamega Acanthopale"),
        ("Both endpoint directions unresolved", "4 / 6", "Sevenello ×2; Zurich; milkweed"),
        ("Multi-panel programmes with >1 point topology", "3 / 4", "descriptive within-exposure heterogeneity"),
    ]
    sy = section_y + 38
    for label, value, note in stats:
        body.append(svg_text(55, sy, label, size=10))
        body.append(svg_text(570, sy, value, size=11, weight="bold"))
        body.append(svg_text(760, sy, note, size=9))
        sy += 42

    body.append(svg_text(35, sy + 12, "Interpretation", size=13, weight="bold"))
    body.append(svg_text(35, sy + 38, "The repeated resolved failure mode is one-sided in the audited corpus: interaction quantity can look better than reproductive function.", size=10, weight="bold"))
    body.append(svg_text(35, sy + 62, "Reverse I− / F+ point patterns exist, but current endpoint uncertainty does not establish resolved compensation.", size=10))
    body.append(svg_text(35, sy + 86, "Counts are descriptive; panels nested within programmes are not independent sign trials and no prevalence is estimated.", size=9))

    write_svg(FIGDIR / "figure3_if_sign_geometry.svg", width, height, body)

def figure4_estimand_scale_sensitivity() -> None:
    effects = rows(SCALE_EFFECTS)
    summary = rows(SCALE_SUMMARY)
    assert len(effects) == 17
    assert len(summary) == 7
    assert sum(float(r["hedges_g"]) < 0 for r in effects) == 17
    assert sum(float(r["oriented_lnRR"]) < 0 for r in effects) == 17

    ml001 = {r["endpoint_id"]: r for r in effects if r["cluster_id"] == "ML001"}
    assert set(ml001) == {"F", "C", "G"}
    g_order = sorted(ml001, key=lambda e: abs(float(ml001[e]["hedges_g"])), reverse=True)
    r_order = sorted(ml001, key=lambda e: abs(float(ml001[e]["oriented_lnRR"])), reverse=True)
    assert g_order == ["G", "C", "F"]
    assert r_order == ["C", "F", "G"]

    by = {(r["row_type"], r["row_id"]): r for r in summary}
    omit = by[("fisher", "OMIT_ML001")]

    width, height = 1240, 760
    body: list[str] = [
        svg_text(30, 36, "Figure 4. Relative response geometry is estimand-scale dependent", size=18, weight="bold"),
        svg_text(30, 60, "Hedges g is the historical primary estimand; lnRR is a mandatory post hoc sensitivity, not a replacement truth.", size=11),
    ]

    # Panel A: Serapias ordering on two separate scales.
    body.append(svg_text(35, 105, "A. Serapias response ordering reverses", size=14, weight="bold"))
    body.append(svg_text(55, 132, "Hedges g |absolute magnitude|", size=11, weight="bold"))
    body.append(svg_text(355, 132, "oriented lnRR |absolute magnitude|", size=11, weight="bold"))
    y = 165
    for rank, ep in enumerate(g_order, start=1):
        body.append(svg_text(65, y, f"{rank}. {ep}: {float(ml001[ep]['hedges_g']):+.3f}", size=12))
        y += 28
    y = 165
    for rank, ep in enumerate(r_order, start=1):
        body.append(svg_text(365, y, f"{rank}. {ep}: {float(ml001[ep]['oriented_lnRR']):+.3f}", size=12))
        y += 28
    body.append(svg_text(55, 260, "C–F lnRR contrast: p=0.6364 using raw-unit multivariate delta covariance.", size=10))

    # Panel B: omit-ML001 robustness under scales/dependence.
    body.append(svg_text(650, 105, "B. Omit-Serapias Fisher conclusion changes", size=14, weight="bold"))
    x0, x1 = 790, 1190
    y0 = 145
    xmin, xmax = 1e-5, 1.0
    labels = [
        ("Hedges g primary", float(omit["hedges_g_p"])),
        ("lnRR + raw-delta cov", float(omit["lnRR_raw_delta_cov_p"])),
        ("lnRR + zero cov", float(omit["lnRR_zero_cov_p"])),
        ("lnRR + Cauchy max-var", float(omit["lnRR_cauchy_maxvar_p"])),
    ]
    threshold_x = log_x(0.05, xmin, xmax, x0, x1)
    body.append(f'<line x1="{threshold_x:.1f}" y1="{y0 - 20}" x2="{threshold_x:.1f}" y2="{y0 + 145}" stroke="black" stroke-dasharray="5,4"/>')
    body.append(svg_text(threshold_x, y0 - 27, "p=0.05", anchor="middle", size=9))
    body.append(f'<line x1="{x0}" y1="{y0 + 135}" x2="{x1}" y2="{y0 + 135}" stroke="black"/>')
    for tick in (1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0):
        tx = log_x(tick, xmin, xmax, x0, x1)
        body.append(f'<line x1="{tx:.1f}" y1="{y0 + 132}" x2="{tx:.1f}" y2="{y0 + 140}" stroke="black"/>')
        body.append(svg_text(tx, y0 + 156, f"{tick:g}", anchor="middle", size=8))
    for i, (label, p) in enumerate(labels):
        yy = y0 + i * 32
        px = log_x(max(xmin, min(xmax, p)), xmin, xmax, x0, x1)
        body.append(svg_text(650, yy + 4, label, size=10))
        body.append(f'<circle cx="{px:.1f}" cy="{yy:.1f}" r="5" fill="black"/>')
        body.append(svg_text(px + 8, yy + 4, f"{p:.3g}", size=9))

    # Panel C: scale-stable signs.
    body.append(f'<line x1="30" y1="340" x2="1210" y2="340" stroke="black"/>')
    body.append(svg_text(35, 380, "C. Scale-stable qualitative direction", size=14, weight="bold"))
    body.append(svg_text(55, 415, "Primary direct effects", size=11, weight="bold"))
    body.append(svg_text(245, 415, "Hedges g", size=11, weight="bold"))
    body.append(svg_text(430, 415, "oriented lnRR", size=11, weight="bold"))
    body.append(svg_text(55, 450, "negative / deterioration-oriented", size=11))
    body.append(svg_text(255, 450, "17 / 17", size=15, weight="bold"))
    body.append(svg_text(455, 450, "17 / 17", size=15, weight="bold"))
    body.append(svg_text(55, 482, "positive / improvement-oriented", size=11))
    body.append(svg_text(268, 482, "0", size=15, weight="bold"))
    body.append(svg_text(468, 482, "0", size=15, weight="bold"))
    body.append(svg_text(650, 420, "Interpretation", size=12, weight="bold"))
    body.append(svg_text(650, 448, "Direction of deterioration is stable;", size=11))
    body.append(svg_text(650, 472, "relative amplitude / separation is not.", size=11))

    # Panel D: exploratory ecology.
    body.append(f'<line x1="30" y1="525" x2="1210" y2="525" stroke="black"/>')
    body.append(svg_text(35, 562, "D. Ecological hypothesis generated by lnRR, not confirmed by this corpus", size=14, weight="bold"))
    body.append(svg_text(55, 595, "Brosimum: connectivity ≈ -0.54 → progeny vigour ≈ -0.20", size=11))
    body.append(svg_text(55, 622, "E. socialis: mating support ≈ -0.90 → family growth ≈ -0.06", size=11))
    body.append(svg_text(55, 649, "Spondias: adult H_O ≈ -0.15; juvenile ≈ -0.54; seed ≈ -0.40", size=11))
    body.append(svg_text(55, 685, "Hypothesis: fragmentation effects may be filtered, buffered or delayed across biological transitions and cohorts.", size=11, weight="bold"))
    body.append(svg_text(55, 712, "Counterexample: Chaco fruit-set changes can equal or exceed pollen-tube changes; no universal attenuation gradient is claimed.", size=10))

    write_svg(FIGDIR / "figure4_estimand_scale_sensitivity.svg", width, height, body)



def table1(result: dict) -> None:
    registry = rows(REGISTRY) + rows(REGISTRY_ML020)
    by_id = {r["cluster_id"]: r for r in registry}
    primary_ids = ["ML001", "ML002", "ML003", "ML014", "ML020"]
    p_by_id = {r["cluster_id"]: float(r["cluster_p_bonferroni"]) for r in result["primary_clusters"]}
    names = {
        "ML001": "Serapias lingua",
        "ML002": "Brosimum alicastrum",
        "ML003": "Spondias purpurea",
        "ML014": "Eucalyptus socialis",
        "ML020": "Aizen-Feinsinger Chaco programme",
    }
    interpretation = {
        "ML001": "strongly unequal process responses; influential",
        "ML002": "no individual-cluster rejection",
        "ML003": "cohort/representation-dependent response; no individual rejection",
        "ML014": "concordant deterioration with unequal strength; no individual rejection",
        "ML020": "concordant I/F deterioration; programme p=1.0",
    }
    TABLEDIR.mkdir(parents=True, exist_ok=True)
    out = TABLEDIR / "table1_primary_cluster_summary.csv"
    fields = [
        "cluster_id", "system", "independent_unit_frame", "fragmentation_contrast",
        "admitted_primary_layers", "n_marginal_effects", "covariance_status", "cluster_p", "interpretation",
    ]
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for cid in primary_ids:
            r = by_id[cid]
            writer.writerow({
                "cluster_id": cid,
                "system": names[cid],
                "independent_unit_frame": r["independent_unit_frame"],
                "fragmentation_contrast": r["fragmentation_contrast"],
                "admitted_primary_layers": r["admissible_primary_layers"],
                "n_marginal_effects": r["n_admissible_primary_effects"],
                "covariance_status": r["covariance_status"],
                "cluster_p": f"{p_by_id[cid]:.8f}",
                "interpretation": interpretation[cid],
            })



def table2_estimand_scale_sensitivity() -> None:
    summary = rows(SCALE_SUMMARY)
    assert len(summary) == 7
    TABLEDIR.mkdir(parents=True, exist_ok=True)
    out = TABLEDIR / "table2_estimand_scale_sensitivity.csv"
    fields = [
        "row_type", "row_id", "hedges_g_p", "lnRR_raw_delta_cov_p",
        "lnRR_zero_cov_p", "lnRR_cauchy_maxvar_p", "interpretation",
    ]
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in summary:
            writer.writerow({k: row[k] for k in fields})


def table_s4_process_function_census() -> None:
    census = rows(PROCESS_FUNCTION_CENSUS)
    assert len(census) == 12
    TABLEDIR.mkdir(parents=True, exist_ok=True)
    out = TABLEDIR / "table_s4_process_function_census.csv"
    fields = list(census[0].keys())
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(census)


def table_s5_if_sign_geometry() -> None:
    census = rows(IF_SIGN_GEOMETRY)
    assert len(census) == 18
    assert len({r["programme_id"] for r in census}) == 8
    assert sum(r["interaction_sign"] != r["function_sign"] for r in census) == 6
    TABLEDIR.mkdir(parents=True, exist_ok=True)
    out = TABLEDIR / "table_s5_if_sign_geometry.csv"
    fields = list(census[0].keys())
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(census)


def table_s6_qualitative_external_if_audit() -> None:
    audit = rows(QUALITATIVE_EXTERNAL_IF)
    assert len(audit) == 8
    assert len({r["audit_id"] for r in audit}) == 8
    assert sum(r["qualitative_geometry"] == "qualitative_hidden_function_loss" for r in audit) == 1
    assert sum(r["qualitative_geometry"] == "resilient_no_detected_loss" for r in audit) == 2
    assert sum(r["qualitative_geometry"] == "concordant_population_size_effect" for r in audit) == 1
    TABLEDIR.mkdir(parents=True, exist_ok=True)
    out = TABLEDIR / "table_s6_qualitative_external_if_audit.csv"
    fields = list(audit[0].keys())
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(audit)



def figure5_direction_translation_synthesis() -> None:
    effects = rows(SCALE_EFFECTS)
    data = rows(IF_TRANSLATION_MAP)
    reliability = rows(IF_RELIABILITY)
    sf06 = json.loads(SF06_RESULT.read_text(encoding="utf-8"))

    assert len(effects) == 17
    assert sum(float(r["hedges_g"]) < 0 for r in effects) == 17
    assert sum(float(r["oriented_lnRR"]) < 0 for r in effects) == 17
    assert len(data) == 16
    assert sum(r["evidence_tier"] == "quantitative" for r in data) == 8
    assert sum(r["evidence_tier"] == "qualitative" for r in data) == 8
    assert len(reliability) == 3
    assert all(float(r["null_misfit_p"]) < 0.01 for r in reliability)
    assert all(float(r["artifact_downstream_probability"]) < 0.03 for r in reliability)

    topo = sf06["scale_stable_external_topology"]
    topo_ext = sf06["scale_stable_external_topology_nonoverlap_sensitivity"]
    sf06_primary = sf06["primary"]["primary_model_dF_on_dI_plus_SC"]
    counts = topo["component_consensus_sign"]["counts"]
    assert counts == {
        "lower": {"lower": 35, "nonlower": 9},
        "nonlower": {"lower": 7, "nonlower": 3},
    }
    assert topo["component_consensus_sign"]["n_used"] == 54
    assert topo["component_consensus_sign"]["minimum_deterministic_mismatches"] == 12
    assert topo["minimum_mismatch_across_publication_deletions"] == 8
    assert topo["minimum_mismatch_across_species_deletions"] == 11
    assert topo["decision"] == "external_sign_translation_nonidentifiability_supported"
    assert topo_ext["component_consensus_sign"]["n_used"] == 31
    assert topo_ext["component_consensus_sign"]["minimum_deterministic_mismatches"] == 7
    assert topo_ext["minimum_mismatch_across_publication_deletions"] == 5
    assert topo_ext["minimum_mismatch_across_species_deletions"] == 6
    assert topo_ext["decision"] == "external_sign_translation_nonidentifiability_supported"
    beta = float(sf06_primary["params"][1])
    beta_p = float(sf06_primary["p_two_sided"][1])
    assert abs(beta - 0.19042084675810994) < 1e-10
    assert abs(beta_p - 0.005307440248158357) < 1e-10

    label = {
        "ML020": "Chaco",
        "P2_CF01_SEVENELLO_2026": "Sevenello",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006": "Kakamega",
        "ML015": "Wandoo",
        "P2_CF01_CARDIOPETALUM_2012": "Cardiopetalum",
        "P2_CF01_ZURICH_2026": "Zurich",
        "P2_CF01_MILKWEED_URBAN_2023": "Milkweed",
        "P2_CF01_PRITCHARD_2005": "Pritchard",
        "QIF001": "Erica",
        "QIF002": "Haloxylon",
        "QIF003": "Caragana",
        "QIF004": "Lithraea",
        "QIF005": "Myrtus",
        "QIF006": "Phyteuma",
        "QIF007": "Psychotria",
        "QIF008": "Hulting",
    }

    def i_class(value: str) -> str:
        if value == "lower":
            return "Interaction lower"
        if value == "no_detected_loss":
            return "No detected I loss"
        if value in {"higher", "higher_or_shifted"}:
            return "Interaction higher / shifted"
        if value == "mixed":
            return "Mixed within programme"
        raise AssertionError(value)

    def f_class(value: str) -> str:
        if value == "lower":
            return "Function lower"
        if value in {"no_detected_loss", "similar"}:
            return "Function similar / no detected loss"
        if value == "higher":
            return "Function higher"
        if value == "mixed":
            return "Mixed within programme"
        raise AssertionError(value)

    rows_order = [
        "Interaction lower",
        "No detected I loss",
        "Interaction higher / shifted",
        "Mixed within programme",
    ]
    cols_order = [
        "Function lower",
        "Function similar / no detected loss",
        "Function higher",
        "Mixed within programme",
    ]
    cells: dict[tuple[str, str], list[str]] = {}
    for r in data:
        key = (i_class(r["interaction_signal"]), f_class(r["function_signal"]))
        prefix = "Q" if r["evidence_tier"] == "quantitative" else "B"
        cells.setdefault(key, []).append(f'{prefix}: {label[r["programme_id"]]}')

    for signal in ("lower", "no_detected_loss"):
        states = {f_class(r["function_signal"]) for r in data if r["interaction_signal"] == signal}
        assert len(states) >= 2
    states = {
        f_class(r["function_signal"])
        for r in data
        if r["interaction_signal"] in {"higher", "higher_or_shifted"}
    }
    assert len(states) >= 2

    width, height = 1280, 1450
    body: list[str] = [
        svg_text(30, 34, "Figure 5. Directional coherence does not imply diagnostic sufficiency", size=18, weight="bold"),
        svg_text(30, 60, "Broad declines and positive coupling can coexist with many-to-many interaction → reproductive-function states.", size=11),
        svg_text(35, 102, "A. Coarse-scale directional coherence", size=14, weight="bold"),
        svg_text(55, 132, "Primary direct effects negative on oriented Hedges g", size=11),
        svg_text(570, 132, "17 / 17", size=16, weight="bold"),
        svg_text(55, 164, "Same primary effects negative on oriented lnRR", size=11),
        svg_text(570, 164, "17 / 17", size=16, weight="bold"),
        svg_text(720, 132, "Interpretation", size=12, weight="bold"),
        svg_text(720, 158, "Fragmentation-associated deterioration is directionally coherent", size=10),
        svg_text(720, 180, "in the admitted direct corpus, without implying equal amplitudes.", size=10),
    ]

    body.append(f'<line x1="30" y1="210" x2="1250" y2="210" stroke="black" stroke-width="1.2"/>')
    body.append(svg_text(35, 245, "B. Frozen 16-programme interaction → reproductive-function translation map", size=14, weight="bold"))
    body.append(svg_text(35, 268, "Q = quantitatively admitted; B = source-explicit qualitative but quantitatively blocked. Cell occupancy is existence, not prevalence.", size=10))

    left, top = 245, 330
    cell_w, cell_h = 245, 100
    for j, col in enumerate(cols_order):
        x = left + j * cell_w + cell_w / 2
        body.append(svg_text(x, top - 25, col, anchor="middle", size=9, weight="bold"))

    for i, row_name in enumerate(rows_order):
        y = top + i * cell_h
        body.append(svg_text(25, y + 44, row_name, size=10, weight="bold"))
        for j, col in enumerate(cols_order):
            x = left + j * cell_w
            body.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="white" stroke="black" stroke-width="1"/>')
            vals = cells.get((row_name, col), [])
            ty = y + 20
            for item in vals:
                body.append(svg_text(x + 10, ty, item, size=8))
                ty += 16

    footer_y = top + len(rows_order) * cell_h + 25
    body.append(svg_text(35, footer_y, "Matched-programme result", size=13, weight="bold"))
    body.append(svg_text(35, footer_y + 24, "The same observed interaction state is compatible with multiple reproductive-function states.", size=11, weight="bold"))
    body.append(svg_text(35, footer_y + 46, "The many-to-many structure survives deletion of every single programme in the frozen mixed-tier universe.", size=10))

    panel_c_y = footer_y + 92
    body.append(f'<line x1="30" y1="{panel_c_y - 22}" x2="1250" y2="{panel_c_y - 22}" stroke="black" stroke-width="1.2"/>')
    body.append(svg_text(35, panel_c_y, "C. External public-S1 validation + source-disjoint sensitivity", size=14, weight="bold"))
    body.append(svg_text(35, panel_c_y + 24, "Aguilar et al. (2025) publication × species × land-use strata; corrected sign consensus.", size=10))

    c_left, c_top = 235, panel_c_y + 75
    c_w, c_h = 180, 68
    c_cols = ["F lower", "F nonlower"]
    c_rows = ["I lower", "I nonlower"]
    c_vals = [[35, 9], [7, 3]]
    for j, col in enumerate(c_cols):
        body.append(svg_text(c_left + j * c_w + c_w / 2, c_top - 18, col, anchor="middle", size=10, weight="bold"))
    for i, row_name in enumerate(c_rows):
        y = c_top + i * c_h
        body.append(svg_text(70, y + 40, row_name, size=11, weight="bold"))
        for j in range(2):
            x = c_left + j * c_w
            body.append(f'<rect x="{x}" y="{y}" width="{c_w}" height="{c_h}" fill="white" stroke="black" stroke-width="1.1"/>')
            body.append(svg_text(x + c_w / 2, y + 42, str(c_vals[i][j]), anchor="middle", size=18, weight="bold"))

    sx = 660
    sy = c_top + 5
    body.append(svg_text(sx, sy, "54 consensus pairs; minimum mismatches = 12", size=11, weight="bold"))
    body.append(svg_text(sx, sy + 24, "Publication LOO minimum = 8; species LOO minimum = 11", size=10))
    body.append(svg_text(sx, sy + 48, "Source-publication-disjoint: 7 / 31 mismatches; LOO minimum = 5", size=10))
    body.append(svg_text(sx, sy + 72, f"Coupling: pair beta={beta:+.3f} (p={beta_p:.3f}); pub-balanced beta=+0.200 (p=0.104)", size=10))
    body.append(svg_text(sx, sy + 96, "Best sign lookup errors = baseline errors = 12 → incremental sign gain = 0", size=10, weight="bold"))
    body.append(svg_text(sx, sy + 120, "Association can be real while the upstream state remains non-identifying.", size=10))

    panel_d_y = c_top + 2 * c_h + 70
    body.append(f'<line x1="30" y1="{panel_d_y - 22}" x2="1250" y2="{panel_d_y - 22}" stroke="black" stroke-width="1.2"/>')
    body.append(svg_text(35, panel_d_y, "D. Resolved false reassurance survives a simple reliability-artifact stress test", size=14, weight="bold"))

    rel_label = {
        "ML015_Wandoo": "Wandoo",
        "P2_CARDIOPETALUM": "Cardiopetalum",
        "P2_KAKAMEGA_AP": "Kakamega Acanthopale",
    }
    for k, row in enumerate(reliability):
        y = panel_d_y + 34 + 31 * k
        label_text = rel_label[row["programme"]]
        p = float(row["null_misfit_p"])
        ri = float(row["R_I"])
        rf = float(row["R_F"])
        body.append(svg_text(55, y, label_text, size=10, weight="bold"))
        body.append(svg_text(250, y, f"R_I={ri:.3f}; R_F={rf:.3f}", size=10))
        body.append(svg_text(500, y, f"equal-latent attenuation misfit p={p:.4f}", size=10))
    body.append(svg_text(55, panel_d_y + 140, "All three descriptive null-misfit p-values are <0.01; anchor selection was post hoc, so this is not a joint confirmatory test.", size=10))
    body.append(svg_text(55, panel_d_y + 164, "Resolved matched-programme surprise: retained interaction quantity can understate reproductive impairment.", size=10, weight="bold"))

    write_svg(FIGDIR / "figure5_direction_translation_synthesis.svg", width, height, body)


def figure_s2_if_translation_map() -> None:
    data = rows(IF_TRANSLATION_MAP)
    assert len(data) == 16
    assert sum(r["evidence_tier"] == "quantitative" for r in data) == 8
    assert sum(r["evidence_tier"] == "qualitative" for r in data) == 8

    label = {
        "ML020": "Chaco",
        "P2_CF01_SEVENELLO_2026": "Sevenello",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006": "Kakamega",
        "ML015": "Wandoo",
        "P2_CF01_CARDIOPETALUM_2012": "Cardiopetalum",
        "P2_CF01_ZURICH_2026": "Zurich",
        "P2_CF01_MILKWEED_URBAN_2023": "Milkweed",
        "P2_CF01_PRITCHARD_2005": "Pritchard",
        "QIF001": "Erica",
        "QIF002": "Haloxylon",
        "QIF003": "Caragana",
        "QIF004": "Lithraea",
        "QIF005": "Myrtus",
        "QIF006": "Phyteuma",
        "QIF007": "Psychotria",
        "QIF008": "Hulting",
    }

    def i_class(value: str) -> str:
        if value == "lower":
            return "Interaction lower"
        if value == "no_detected_loss":
            return "No detected I loss"
        if value in {"higher", "higher_or_shifted"}:
            return "Interaction higher / shifted"
        if value == "mixed":
            return "Mixed within programme"
        raise AssertionError(value)

    def f_class(value: str) -> str:
        if value == "lower":
            return "Function lower"
        if value in {"no_detected_loss", "similar"}:
            return "Function similar / no detected loss"
        if value == "higher":
            return "Function higher"
        if value == "mixed":
            return "Mixed within programme"
        raise AssertionError(value)

    rows_order = [
        "Interaction lower",
        "No detected I loss",
        "Interaction higher / shifted",
        "Mixed within programme",
    ]
    cols_order = [
        "Function lower",
        "Function similar / no detected loss",
        "Function higher",
        "Mixed within programme",
    ]
    cells: dict[tuple[str, str], list[str]] = {}
    for r in data:
        key = (i_class(r["interaction_signal"]), f_class(r["function_signal"]))
        prefix = "Q" if r["evidence_tier"] == "quantitative" else "B"
        cells.setdefault(key, []).append(f'{prefix}: {label[r["programme_id"]]}')

    assert {"Function lower", "Function higher", "Function similar / no detected loss"} <= {
        f_class(r["function_signal"]) for r in data if r["interaction_signal"] == "lower"
    }
    assert {"Function lower", "Function similar / no detected loss"} <= {
        f_class(r["function_signal"]) for r in data if r["interaction_signal"] == "no_detected_loss"
    }
    assert {"Function lower", "Function similar / no detected loss"} <= {
        f_class(r["function_signal"]) for r in data if r["interaction_signal"] in {"higher", "higher_or_shifted"}
    }

    width, height = 1280, 780
    left, top = 245, 145
    cell_w, cell_h = 245, 125
    body: list[str] = [
        svg_text(30, 34, "Supplementary Figure S2. Frozen interaction–function translation map", size=18, weight="bold"),
        svg_text(30, 60, "Same qualitative interaction signals map to multiple reproductive-function states across the frozen evidence universe.", size=11),
        svg_text(30, 82, "Q = quantitatively admitted programme; B = quantitatively blocked but source-explicit qualitative programme.", size=10),
    ]

    for j, col in enumerate(cols_order):
        x = left + j * cell_w + cell_w / 2
        body.append(svg_text(x, top - 36, col, anchor="middle", size=10, weight="bold"))

    for i, row_name in enumerate(rows_order):
        y = top + i * cell_h
        body.append(svg_text(25, y + 54, row_name, size=10, weight="bold"))
        for j, col in enumerate(cols_order):
            x = left + j * cell_w
            body.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" fill="white" stroke="black" stroke-width="1"/>'
            )
            vals = cells.get((row_name, col), [])
            ty = y + 24
            for item in vals:
                body.append(svg_text(x + 10, ty, item, size=9))
                ty += 18

    footer_y = top + len(rows_order) * cell_h + 35
    body.append(svg_text(30, footer_y, "Interpretation", size=12, weight="bold"))
    body.append(svg_text(30, footer_y + 24, "Cell occupancy demonstrates existence of multiple I→F translations; it is not a frequency or prevalence estimate.", size=10))
    body.append(svg_text(30, footer_y + 46, "No-detected-effect categories are not recoded as zero or equality, and B programmes do not increment the quantitative denominator.", size=10))
    write_svg(FIGDIR / "figure_s2_if_translation_map.svg", width, height, body)


def table_s7_if_translation_map() -> None:
    data = rows(IF_TRANSLATION_MAP)
    assert len(data) == 16
    TABLEDIR.mkdir(parents=True, exist_ok=True)
    out = TABLEDIR / "table_s7_if_translation_map.csv"
    fields = [
        "evidence_tier",
        "programme_id",
        "system",
        "source_id",
        "interaction_signal",
        "function_signal",
        "translation_topology",
        "resolution_status",
        "interpretation",
    ]
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for r in data:
            writer.writerow({k: r[k] for k in fields})

def main() -> None:
    result = canonical_result()
    figure1_coverage()
    figure2_influence(result)
    figure3_if_sign_geometry()
    figure4_estimand_scale_sensitivity()
    figure5_direction_translation_synthesis()
    table1(result)
    table2_estimand_scale_sensitivity()
    table_s4_process_function_census()
    table_s5_if_sign_geometry()
    table_s6_qualitative_external_if_audit()
    figure_s2_if_translation_map()
    table_s7_if_translation_map()
    expected = [
        FIGDIR / "figure1_primary_evidence_geometry.svg",
        FIGDIR / "figure2_leave_one_out_influence.svg",
        FIGDIR / "figure3_if_sign_geometry.svg",
        FIGDIR / "figure4_estimand_scale_sensitivity.svg",
        FIGDIR / "figure5_direction_translation_synthesis.svg",
        TABLEDIR / "table1_primary_cluster_summary.csv",
        TABLEDIR / "table2_estimand_scale_sensitivity.csv",
        TABLEDIR / "table_s4_process_function_census.csv",
        TABLEDIR / "table_s5_if_sign_geometry.csv",
        TABLEDIR / "table_s6_qualitative_external_if_audit.csv",
    ]
    assert all(p.is_file() and p.stat().st_size > 500 for p in expected[:5])
    assert expected[5].is_file() and expected[5].stat().st_size > 200
    assert expected[6].is_file() and expected[6].stat().st_size > 400
    assert expected[7].is_file() and expected[7].stat().st_size > 400
    assert expected[8].is_file() and expected[8].stat().st_size > 400
    assert expected[9].is_file() and expected[9].stat().st_size > 500
    print("JOURNAL_OF_ECOLOGY_FIGURES_OK " + " ".join(str(p.relative_to(ROOT)) for p in expected))


if __name__ == "__main__":
    main()
