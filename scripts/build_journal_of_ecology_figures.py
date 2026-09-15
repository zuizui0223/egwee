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
REGISTRY = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_v1.csv"
REGISTRY_ML020 = ROOT / "evidence/meta_extraction/multilayer_cluster_registry_extension_ml020.csv"
SYNTHESIS = ROOT / "scripts/synthesize_state_separation.py"


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
    assert abs(float(result["primary_combined_p"]) - 0.012124324105113144) < 1e-12
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


def figure3_ml020() -> None:
    effect_rows = rows(ML020_EFFECTS)
    by_species: dict[str, dict[str, float]] = {}
    for row in effect_rows:
        by_species.setdefault(row["species"], {})[row["endpoint_id"]] = float(row["oriented_effect"])
    expected_species = {"Atamisquea emarginata", "Cercidium australe", "Prosopis nigra"}
    assert set(by_species) == expected_species

    width, height = 700, 650
    x0, x1, y0, y1 = 105, 630, 540, 80
    lo, hi = -1.35, 0.05

    def sx(v: float) -> float:
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    def sy(v: float) -> float:
        return y0 - (v - lo) / (hi - lo) * (y0 - y1)

    body: list[str] = [svg_text(30, 35, "Figure 3. ML020: interaction and reproductive function decline together", size=18, weight="bold")]
    body.append(svg_text(30, 60, "Three dependent species subsystems in one replicated Chaco programme; programme p = 1.0.", size=12))

    body.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="black" stroke-width="1.5"/>')
    body.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="black" stroke-width="1.5"/>')
    # one-to-one line
    body.append(f'<line x1="{sx(lo):.1f}" y1="{sy(lo):.1f}" x2="{sx(hi):.1f}" y2="{sy(hi):.1f}" stroke="black" stroke-dasharray="6,5"/>')
    body.append(svg_text(sx(-0.15), sy(-0.15) - 8, "F = I", size=10))

    for tick in [-1.2, -0.9, -0.6, -0.3, 0.0]:
        x = sx(tick)
        y = sy(tick)
        body.append(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0 + 6}" stroke="black"/>')
        body.append(svg_text(x, y0 + 24, f"{tick:.1f}", anchor="middle", size=10))
        body.append(f'<line x1="{x0 - 6}" y1="{y:.1f}" x2="{x0}" y2="{y:.1f}" stroke="black"/>')
        body.append(svg_text(x0 - 12, y + 4, f"{tick:.1f}", anchor="end", size=10))

    body.append(svg_text((x0 + x1) / 2, 605, "Fragmentation effect on I (pollen tubes), Hedges g", anchor="middle", size=12, weight="bold"))
    body.append(
        f'<text x="28" y="{(y0 + y1) / 2:.1f}" font-family="Arial,Helvetica,sans-serif" font-size="12" font-weight="bold" text-anchor="middle" transform="rotate(-90 28 {(y0 + y1) / 2:.1f})">Fragmentation effect on F (fruit set), Hedges g</text>'
    )

    labels = {
        "Atamisquea emarginata": "Atamisquea",
        "Cercidium australe": "Cercidium",
        "Prosopis nigra": "Prosopis",
    }
    for species in sorted(by_species):
        vals = by_species[species]
        ix = vals["I_pollen_tubes"]
        fy = vals["F_fruit_set"]
        x, y = sx(ix), sy(fy)
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="black"/>')
        body.append(svg_text(x + 10, y - 8, labels[species], size=11, weight="bold"))

    body.append(svg_text(385, 110, "Both layers deteriorate", size=11))
    write_svg(FIGDIR / "figure3_ml020_concordant_decline.svg", width, height, body)


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
        "ML001": "clear within-system state separation; influential",
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


def main() -> None:
    result = canonical_result()
    figure1_coverage()
    figure2_influence(result)
    figure3_ml020()
    table1(result)
    expected = [
        FIGDIR / "figure1_primary_evidence_geometry.svg",
        FIGDIR / "figure2_leave_one_out_influence.svg",
        FIGDIR / "figure3_ml020_concordant_decline.svg",
        TABLEDIR / "table1_primary_cluster_summary.csv",
    ]
    assert all(p.is_file() and p.stat().st_size > 500 for p in expected[:3])
    assert expected[3].is_file() and expected[3].stat().st_size > 200
    print("JOURNAL_OF_ECOLOGY_FIGURES_OK " + " ".join(str(p.relative_to(ROOT)) for p in expected))


if __name__ == "__main__":
    main()
