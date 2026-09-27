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
    body: list[str] = [svg_text(30, 35, "Figure 2. Leave-one-cluster-out influence defines the claim ceiling", size=18, weight="bold")]
    body.append(svg_text(30, 60, "Only omission of ML001 removes rejection at α = 0.05.", size=12))

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


def figure3_response_regimes() -> None:
    chaco_rows = rows(ML020_EFFECTS)
    chaco: dict[str, dict[str, float]] = {}
    for row in chaco_rows:
        chaco.setdefault(row["species"], {})[row["layer"]] = float(row["oriented_effect"])
    assert set(chaco) == {"Atamisquea emarginata", "Cercidium australe", "Prosopis nigra"}

    wandoo_rows = rows(WANDOO_EFFECTS)
    wandoo = {r["layer"]: float(r["oriented_effect"]) for r in wandoo_rows}
    assert {"I", "F"} <= set(wandoo)

    cardio_rows = [r for r in rows(CARDIO_EFFECTS) if r["primary_or_sensitivity"] == "primary"]
    cardio = {r["layer"]: float(r["fisher_z"]) for r in cardio_rows}
    assert {"I_interaction", "F_reproductive_function"} <= set(cardio)

    berg_rows = [
        r for r in rows(BERGSDORF_EFFECTS)
        if r["panel_id"] == "AP_2001" and r["primary_or_sensitivity"] == "primary"
    ]
    berg = {r["layer"]: float(r["hedges_g"]) for r in berg_rows}
    assert {"I_interaction", "F_reproductive_function"} <= set(berg)

    width, height = 1240, 760
    body: list[str] = [
        svg_text(30, 34, "Figure 3. Fragmentation produces coupled and decoupled interaction–function responses", size=18, weight="bold"),
        svg_text(30, 58, "Each panel retains its registered effect scale; effect magnitudes are not compared across panels.", size=11),
    ]

    draw_effect_pair_panel(
        body,
        px=30, py=85, pw=575, ph=285,
        title="A. Chaco: coupled decline",
        subtitle="Hedges g; small fragments minus continuous forest",
        pairs=[
            ("Atamisquea", chaco["Atamisquea emarginata"]["I_interaction"], chaco["Atamisquea emarginata"]["F_reproductive_function"]),
            ("Cercidium", chaco["Cercidium australe"]["I_interaction"], chaco["Cercidium australe"]["F_reproductive_function"]),
            ("Prosopis", chaco["Prosopis nigra"]["I_interaction"], chaco["Prosopis nigra"]["F_reproductive_function"]),
        ],
        lo=-1.3, hi=0.1, ticks=[-1.2, -0.8, -0.4, 0.0],
        footer="Three dependent species; programme Bonferroni p = 1.0.",
    )

    draw_effect_pair_panel(
        body,
        px=635, py=85, pw=575, ph=285,
        title="B. Eucalyptus wandoo: pollen quantity–function decoupling",
        subtitle="Fisher z along response-free fragmentation severity",
        pairs=[("E. wandoo", wandoo["I"], wandoo["F"])],
        lo=-1.1, hi=0.9, ticks=[-1.0, -0.5, 0.0, 0.5],
        footer="Pollen tubes increase while seed production declines; I-F p = 0.0008565.",
    )

    draw_effect_pair_panel(
        body,
        px=30, py=405, pw=575, ph=285,
        title="C. Cardiopetalum: pollinator persistence–function decoupling",
        subtitle="Fisher z along decreasing fragment area",
        pairs=[("Cardiopetalum", cardio["I_interaction"], cardio["F_reproductive_function"])],
        lo=-1.9, hi=0.1, ticks=[-1.8, -1.2, -0.6, 0.0],
        footer="Pollinator abundance changes weakly while fruit set declines; I-F p = 0.00316.",
    )

    draw_effect_pair_panel(
        body,
        px=635, py=405, pw=575, ph=285,
        title="D. Kakamega Acanthopale: visitation–function decoupling",
        subtitle="Hedges g; fragment sites minus main-forest sites",
        pairs=[("Acanthopale", berg["I_interaction"], berg["F_reproductive_function"])],
        lo=-3.2, hi=0.8, ticks=[-3.0, -2.0, -1.0, 0.0],
        footer="Visitation is maintained/slightly higher while fruit set falls; I-F p = 0.00163.",
    )

    body.append(f'<circle cx="445" cy="726" r="5" fill="white" stroke="black" stroke-width="1.5"/>')
    body.append(svg_text(458, 730, "Interaction / pollen quantity", size=10))
    body.append(f'<rect x="662" y="721" width="10" height="10" fill="black"/>')
    body.append(svg_text(678, 730, "Reproductive function", size=10))
    write_svg(FIGDIR / "figure3_ecological_response_regimes.svg", width, height, body)



def figure4_bottleneck_synthesis() -> None:
    if_rows = rows(IF_CENSUS)
    mf_rows = rows(MATING_FUNCTION_CENSUS)
    assert len(if_rows) == 8
    assert sum(r["if_pair_testable"] == "yes" for r in if_rows) == 7
    assert sum(r["resolved_if_mismatch"] == "yes" for r in if_rows) == 3
    assert {r["resolved_direction"] for r in if_rows if r["resolved_if_mismatch"] == "yes"} == {"F_more_negative_than_I"}
    assert {r["interaction_measurement_class"] for r in if_rows} == {"quantity_only"}
    assert len(mf_rows) == 4
    assert sum(r["resolved_mismatch"] == "yes" for r in mf_rows) == 1
    assert next(r for r in mf_rows if r["resolved_mismatch"] == "yes")["programme_id"] == "ML001"

    width, height = 1240, 720
    body: list[str] = [
        svg_text(30, 36, "Figure 4. Fragmentation can shift the position of the reproductive life-cycle bottleneck", size=18, weight="bold"),
        svg_text(30, 60, "Evidence synthesis only: regimes are descriptive and effect families are not pooled numerically.", size=11),
    ]

    def arrow(x1: float, y: float, x2: float) -> None:
        body.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2 - 10:.1f}" y2="{y:.1f}" stroke="black" stroke-width="1.5"/>')
        body.append(f'<polygon points="{x2 - 10:.1f},{y - 5:.1f} {x2:.1f},{y:.1f} {x2 - 10:.1f},{y + 5:.1f}" fill="black"/>')

    def box(x: float, y: float, w: float, h: float, title: str, subtitle: str, *, dashed: bool = False) -> None:
        dash = ' stroke-dasharray="5,4"' if dashed else ""
        body.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="white" stroke="black" stroke-width="1.4"{dash}/>')
        body.append(svg_text(x + w / 2, y + 25, title, anchor="middle", size=12, weight="bold"))
        body.append(svg_text(x + w / 2, y + 46, subtitle, anchor="middle", size=9))

    def regime(y: float, label: str, note: str, qtxt: str, etxt: str, ftxt: str, *, e_dashed: bool = False) -> None:
        body.append(svg_text(45, y + 20, label, size=14, weight="bold"))
        body.append(svg_text(45, y + 42, note, size=10))
        xq, xe, xf = 410, 690, 970
        bw, bh = 180, 68
        box(xq, y, bw, bh, "Interaction quantity", qtxt)
        arrow(xq + bw, y + bh / 2, xe)
        box(xe, y, bw, bh, "Effective mating", etxt, dashed=e_dashed)
        arrow(xe + bw, y + bh / 2, xf)
        box(xf, y, bw, bh, "Reproductive function", ftxt)

    regime(
        115,
        "A. Coupled / unresolved",
        "Chaco and Sevenello: no resolved I–F mismatch",
        "declines or changes",
        "not directly measured",
        "tracks I within uncertainty",
        e_dashed=True,
    )
    regime(
        270,
        "B. Downstream function-dominant",
        "3 resolved I–F programmes: Wandoo, Cardiopetalum, Kakamega",
        "buffered / less negative",
        "missing in current I–F frame",
        "more negative",
        e_dashed=True,
    )
    regime(
        425,
        "C. Upstream movement/mating-dominant",
        "Serapias resolved; Brosimum and E. socialis point similarly but remain unresolved",
        "not the tested process",
        "movement/mating support more negative",
        "partly buffered / less negative",
        e_dashed=False,
    )

    body.append(f'<line x1="30" y1="535" x2="1210" y2="535" stroke="black" stroke-width="1"/>')
    body.append(svg_text(45, 570, "Current measurement gap", size=14, weight="bold"))
    body.append(svg_text(45, 594, "I–F corpus: 8/8 interaction endpoints are quantity-level; 0/8 directly measure effective mating quality on the same frame.", size=11))
    body.append(svg_text(45, 628, "Fresh localization design", size=14, weight="bold"))
    body.append(svg_text(230, 628, "Q → E → F", size=16, weight="bold"))
    body.append(svg_text(330, 628, "Primary H2-v2 contrast: ΔQE = Q − E; ΔEF locates propagation, compensation, or later filtering.", size=11))
    body.append(svg_text(45, 673, "Interpretation: fragmentation changes response coupling; it does not impose one universal stage of maximum sensitivity.", size=11, weight="bold"))

    write_svg(FIGDIR / "figure4_lifecycle_bottleneck_synthesis.svg", width, height, body)

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



def table2_process_function_census() -> None:
    census = rows(PROCESS_FUNCTION_CENSUS)
    assert len(census) == 12
    assert sum(r["pair_testable"] == "yes" for r in census) == 11
    assert sum(r["resolved_mismatch"] == "yes" for r in census) == 4
    assert sum(r["resolved_mismatch"] == "no" for r in census) == 7
    assert sum(r["resolved_mismatch"] == "not_testable" for r in census) == 1
    assert sum(r["resolved_direction"] == "F_more_negative_than_process" for r in census) == 3
    assert sum(r["resolved_direction"] == "process_more_negative_than_F" for r in census) == 1
    assert sum(r["measurement_class"] == "quantity_only" for r in census) == 8
    assert sum(r["measurement_class"] == "movement_or_mating_support" for r in census) == 4

    TABLEDIR.mkdir(parents=True, exist_ok=True)
    out = TABLEDIR / "table2_process_function_census.csv"
    fields = [
        "programme_id",
        "system",
        "source_id",
        "process_stage",
        "process_endpoint",
        "measurement_class",
        "effect_family",
        "n_dependent_panels",
        "pair_testable",
        "programme_adjusted_p",
        "census_result",
        "direction_if_resolved",
        "ecological_regime",
        "ecological_interpretation",
    ]
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in census:
            if row["resolved_mismatch"] == "yes":
                result = "resolved mismatch"
                if row["resolved_direction"] == "F_more_negative_than_process":
                    direction = "F more negative than process"
                else:
                    assert row["resolved_direction"] == "process_more_negative_than_F"
                    direction = "process more negative than F"
            elif row["resolved_mismatch"] == "no":
                result = "unresolved mismatch"
                direction = ""
            else:
                result = "not testable"
                direction = ""
            writer.writerow({
                "programme_id": row["programme_id"],
                "system": row["system"],
                "source_id": row["source_id"],
                "process_stage": row["process_stage"],
                "process_endpoint": row["process_endpoint"],
                "measurement_class": row["measurement_class"],
                "effect_family": row["effect_family"],
                "n_dependent_panels": row["n_dependent_panels"],
                "pair_testable": row["pair_testable"],
                "programme_adjusted_p": row["programme_adjusted_p"],
                "census_result": result,
                "direction_if_resolved": direction,
                "ecological_regime": row["ecological_regime"],
                "ecological_interpretation": row["interpretation"],
            })


def main() -> None:
    result = canonical_result()
    figure1_coverage()
    figure2_influence(result)
    figure3_response_regimes()
    figure4_bottleneck_synthesis()
    table1(result)
    table2_process_function_census()
    expected = [
        FIGDIR / "figure1_primary_evidence_geometry.svg",
        FIGDIR / "figure2_leave_one_out_influence.svg",
        FIGDIR / "figure3_ecological_response_regimes.svg",
        FIGDIR / "figure4_lifecycle_bottleneck_synthesis.svg",
        TABLEDIR / "table1_primary_cluster_summary.csv",
        TABLEDIR / "table2_process_function_census.csv",
    ]
    assert all(p.is_file() and p.stat().st_size > 500 for p in expected[:4])
    assert expected[4].is_file() and expected[4].stat().st_size > 200
    assert expected[5].is_file() and expected[5].stat().st_size > 400
    print("JOURNAL_OF_ECOLOGY_FIGURES_OK " + " ".join(str(p.relative_to(ROOT)) for p in expected))


if __name__ == "__main__":
    main()
