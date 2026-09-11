from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/meta_extraction/PS003_serapias_gradient_effects_v1.csv"

AREA = [3578.25, 2540.20, 64.20, 3451.22, 2962.40, 55.80, 65.54, 4585.30, 2542.60]
FRUIT = [13.58, 20.30, 5.20, 14.23, 15.60, 5.50, 5.10, 14.68, 16.75]
IMMIGRATION = [28.68, 32.02, 9.38, 28.34, 27.49, 11.11, 7.14, 30.53, 28.64]


def pearson(x: list[float], y: list[float]) -> float:
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    denx = math.sqrt(sum((a - mx) ** 2 for a in x))
    deny = math.sqrt(sum((b - my) ** 2 for b in y))
    return num / (denx * deny)


def fisher_z(r: float) -> float:
    return 0.5 * math.log((1 + r) / (1 - r))


def main() -> None:
    with OUT.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 2
    by_layer = {r["layer"]: r for r in rows}

    severity_log = [-math.log(a) for a in AREA]
    severity_raw = [-a for a in AREA]

    expected = {
        "F": (FRUIT, -1.541221490243804, -1.08641103700365),
        "C": (IMMIGRATION, -2.30404497310119, -1.614612326341287),
    }
    for layer, (y, z_log_expected, z_raw_expected) in expected.items():
        row = by_layer[layer]
        r_log = pearson(severity_log, y)
        z_log = fisher_z(r_log)
        r_raw = pearson(severity_raw, y)
        z_raw = fisher_z(r_raw)
        assert abs(z_log - z_log_expected) < 1e-9
        assert abs(z_raw - z_raw_expected) < 1e-9
        assert abs(float(row["raw_effect_fisher_z"]) - z_log) < 1e-8
        assert abs(float(row["sensitivity_fisher_z_untransformed_area"]) - z_raw) < 1e-8
        assert abs(float(row["raw_variance"]) - (1 / 6)) < 1e-8
        assert row["effect_unit_status"] == "fisher_z_admissible"
        assert int(row["n_independent"]) == 9

    print("PS003 Serapias population-level gradient extraction: PASS")


if __name__ == "__main__":
    main()
