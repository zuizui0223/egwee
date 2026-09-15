from __future__ import annotations

import csv
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "manuscript/tables/table_s3_primary_marginal_effects.csv"
OUT = ROOT / "manuscript/figures/figure_s1_all_primary_marginal_effects.svg"


def rows() -> list[dict[str, str]]:
    with TABLE.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def text(x: float, y: float, s: str, *, size: int = 11, anchor: str = "start", weight: str = "normal") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial,Helvetica,sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}">{escape(s)}</text>'
    )


def sx(v: float, lo: float, hi: float, x0: float, x1: float) -> float:
    return x0 + (v - lo) / (hi - lo) * (x1 - x0)


def main() -> None:
    rs = rows()
    assert len(rs) == 17
    assert {r["cluster_id"] for r in rs} == {"ML001", "ML002", "ML003", "ML014", "ML020"}

    # ML001 is shown on its own explicit scale because its standardized effects
    # are an order of magnitude larger. All other clusters share the right scale.
    left_lo, left_hi = -42.0, 2.0
    right_lo, right_hi = -6.5, 2.5
    label_x = 25
    left_x0, left_x1 = 445, 690
    right_x0, right_x1 = 760, 1105
    top = 125
    row_h = 35
    height = top + len(rs) * row_h + 110
    width = 1150

    body: list[str] = [
        text(25, 35, "Supplementary Figure S1. All 17 primary marginal fragmentation effects", size=18, weight="bold"),
        text(25, 60, "Points are Hedges g; horizontal lines are marginal 95% CIs. Negative values indicate lower support/function under fragmentation.", size=11),
        text(25, 80, "ML001 Serapias uses the separate left scale; ML002/ML003/ML014/ML020 share the right scale. Marginal CIs are not layer-separation tests.", size=11, weight="bold"),
        text((left_x0 + left_x1) / 2, 105, "ML001 scale", anchor="middle", size=12, weight="bold"),
        text((right_x0 + right_x1) / 2, 105, "Other primary clusters", anchor="middle", size=12, weight="bold"),
    ]

    for tick in (-40, -30, -20, -10, 0):
        x = sx(tick, left_lo, left_hi, left_x0, left_x1)
        body.append(f'<line x1="{x:.1f}" y1="112" x2="{x:.1f}" y2="{height-65}" stroke="#d0d0d0" stroke-width="1"/>')
        body.append(text(x, height - 42, f"{tick:g}", anchor="middle", size=10))
    for tick in (-6, -4, -2, 0, 2):
        x = sx(tick, right_lo, right_hi, right_x0, right_x1)
        body.append(f'<line x1="{x:.1f}" y1="112" x2="{x:.1f}" y2="{height-65}" stroke="#d0d0d0" stroke-width="1"/>')
        body.append(text(x, height - 42, f"{tick:g}", anchor="middle", size=10))

    zero_left = sx(0, left_lo, left_hi, left_x0, left_x1)
    zero_right = sx(0, right_lo, right_hi, right_x0, right_x1)
    body.append(f'<line x1="{zero_left:.1f}" y1="112" x2="{zero_left:.1f}" y2="{height-65}" stroke="black" stroke-width="1.5"/>')
    body.append(f'<line x1="{zero_right:.1f}" y1="112" x2="{zero_right:.1f}" y2="{height-65}" stroke="black" stroke-width="1.5"/>')

    last_cluster = None
    for i, r in enumerate(rs):
        y = top + i * row_h
        cid = r["cluster_id"]
        system = r["system_or_subsystem"]
        endpoint = r["endpoint"]
        layer = r["layer"]
        if last_cluster is not None and cid != last_cluster:
            body.append(f'<line x1="25" y1="{y-row_h/2:.1f}" x2="1110" y2="{y-row_h/2:.1f}" stroke="#888" stroke-width="0.8"/>')
        last_cluster = cid

        label = f"{cid} | {system} | {layer}: {endpoint}"
        body.append(text(label_x, y + 4, label, size=10, weight="bold" if cid == "ML001" else "normal"))

        g = float(r["hedges_g"])
        lo = float(r["ci95_lower"])
        hi = float(r["ci95_upper"])
        if cid == "ML001":
            x0, x1, alo, ahi = left_x0, left_x1, left_lo, left_hi
        else:
            x0, x1, alo, ahi = right_x0, right_x1, right_lo, right_hi
        if not (alo <= lo <= ahi and alo <= hi <= ahi and alo <= g <= ahi):
            raise AssertionError((cid, endpoint, lo, g, hi, alo, ahi))
        xl, xg, xh = (sx(v, alo, ahi, x0, x1) for v in (lo, g, hi))
        body.append(f'<line x1="{xl:.1f}" y1="{y}" x2="{xh:.1f}" y2="{y}" stroke="black" stroke-width="1.8"/>')
        body.append(f'<line x1="{xl:.1f}" y1="{y-4}" x2="{xl:.1f}" y2="{y+4}" stroke="black"/>')
        body.append(f'<line x1="{xh:.1f}" y1="{y-4}" x2="{xh:.1f}" y2="{y+4}" stroke="black"/>')
        body.append(f'<circle cx="{xg:.1f}" cy="{y}" r="4.5" fill="black"/>')

    body.append(text((left_x0 + left_x1) / 2, height - 12, "Hedges g (ML001 separate scale)", anchor="middle", size=11, weight="bold"))
    body.append(text((right_x0 + right_x1) / 2, height - 12, "Hedges g (ML002/ML003/ML014/ML020)", anchor="middle", size=11, weight="bold"))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        *body,
        '</svg>',
    ]
    OUT.write_text("\n".join(svg) + "\n", encoding="utf-8")
    if OUT.stat().st_size < 4000:
        raise AssertionError("supplementary forest unexpectedly small")
    print(f"PRIMARY_EFFECT_FOREST_OK rows={len(rs)} path={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
