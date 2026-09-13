from __future__ import annotations

import io
import math
import re
import urllib.request

import numpy as np
import pandas as pd

URL = "https://pmc.ncbi.nlm.nih.gov/articles/PMC3670206/"
UA = "Mozilla/5.0 egwee-magnolia-2013-recovery/1.0"


def fetch_table1() -> pd.DataFrame:
    req = urllib.request.Request(URL, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=60) as r:
        html = r.read()
    tables = pd.read_html(io.BytesIO(html), match="Immigration rate by pollen")
    if len(tables) != 1:
        raise RuntimeError(f"expected exactly one Table 1 match, got {len(tables)}")
    df = tables[0]
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [" ".join(str(x) for x in tup if str(x) != "nan").strip() for tup in df.columns]
    else:
        df.columns = [str(x).strip() for x in df.columns]
    return df


def num(x) -> float | None:
    if pd.isna(x):
        return None
    m = re.search(r"[-+]?\d+(?:\.\d+)?", str(x).replace(",", ""))
    return float(m.group()) if m else None


def parse_pop(label: str) -> tuple[str, int] | None:
    m = re.match(r"^([A-Za-z]+)\s*\((\d+)\)$", str(label).strip())
    return (m.group(1), int(m.group(2))) if m else None


def fisher_z(r: float) -> float:
    if not (-1 < r < 1):
        raise RuntimeError(f"correlation at boundary: {r}")
    return math.atanh(r)


def main() -> None:
    df = fetch_table1()
    print(f"MAGNOLIA_TABLE1_NORMALIZED rows={len(df)} cols={list(df.columns)!r}")

    pop_col = next(c for c in df.columns if "Population" in c and "population size" in c)
    parent_col = next(c for c in df.columns if "Seed parents" in c)
    seed_col = next(c for c in df.columns if "Seed production rate" in c)
    npat_col = next(c for c in df.columns if "samples for paternity" in c)
    immig_col = next(c for c in df.columns if "Immigration rate by pollen" in c)

    current: tuple[str, int] | None = None
    records: list[dict[str, float | int | str]] = []
    group_rows: list[dict[str, object]] = []
    for _, row in df.iterrows():
        parsed = parse_pop(row[pop_col])
        if parsed:
            current = parsed
        if current is None:
            continue
        group_rows.append({"pop": current[0], "pop_size": current[1], "row": row})

    pops = []
    for pop in list(dict.fromkeys(x["pop"] for x in group_rows)):
        rr = [x for x in group_rows if x["pop"] == pop]
        means = [x for x in rr if str(x["row"][parent_col]).strip() == "Mean (Total)"]
        if len(means) != 1:
            raise RuntimeError(f"population {pop}: expected one Mean (Total), found {len(means)}")
        x = means[0]
        row = x["row"]
        f_mean = num(row[seed_col])
        n_paternity = num(row[npat_col])
        c_rate_pct = num(row[immig_col])
        if f_mean is None or n_paternity is None or c_rate_pct is None:
            raise RuntimeError(f"population {pop}: missing mean/total values")

        # QA reconstruct immigrant count from individual rows when counts are present in the immigration cell.
        individual_rows = [y["row"] for y in rr if str(y["row"][parent_col]).strip() != "Mean (Total)"]
        n_sum = 0.0
        immigrant_count_sum = 0.0
        count_rows = 0
        for ir in individual_rows:
            n = num(ir[npat_col])
            if n is not None:
                n_sum += n
            text = str(ir[immig_col])
            # pandas may flatten percentage and parenthesized count into one string, e.g. '11.8 (2)'.
            cm = re.search(r"\((\d+)\)", text)
            if cm:
                immigrant_count_sum += int(cm.group(1))
                count_rows += 1
        # Some HTML layouts split parenthesized counts into separate columns; the source Mean(Total)
        # percentage remains canonical. Only compare reconstructed counts when they are visible.
        qa_rate = 100.0 * immigrant_count_sum / n_sum if n_sum > 0 and count_rows else None

        pops.append({
            "population": pop,
            "population_size": int(x["pop_size"]),
            "F_seed_production_pct": f_mean,
            "C_immigration_pct": c_rate_pct,
            "paternity_n_total": int(n_paternity),
            "qa_immigration_pct_from_visible_counts": qa_rate,
        })

    if len(pops) < 4:
        raise RuntimeError(f"too few common populations: {len(pops)}")
    if len({p['population'] for p in pops}) != len(pops):
        raise RuntimeError("duplicate populations")

    sev = np.array([-math.log(float(p["population_size"])) for p in pops])
    c = np.array([float(p["C_immigration_pct"]) for p in pops])
    f = np.array([float(p["F_seed_production_pct"]) for p in pops])
    r_c = float(np.corrcoef(sev, c)[0, 1])
    r_f = float(np.corrcoef(sev, f)[0, 1])
    z_c, z_f = fisher_z(r_c), fisher_z(r_f)
    var = 1.0 / (len(pops) - 3)

    sev_z = (sev - sev.mean()) / sev.std(ddof=0)
    X = np.column_stack([np.ones(len(pops)), sev_z])
    res_c = c - X @ np.linalg.lstsq(X, c, rcond=None)[0]
    res_f = f - X @ np.linalg.lstsq(X, f, rcond=None)[0]
    r_res = float(np.corrcoef(res_c, res_f)[0, 1])
    cov = r_res * var
    det = var * var - cov * cov
    if not det > 1e-12:
        raise RuntimeError(f"working covariance not positive definite: det={det}")

    for p in pops:
        qa = p["qa_immigration_pct_from_visible_counts"]
        qa_text = "NA" if qa is None else f"{qa:.6f}"
        print(
            "MAGNOLIA_POP "
            f"population={p['population']} population_size={p['population_size']} "
            f"C_immigration_pct={p['C_immigration_pct']:.6f} F_seed_production_pct={p['F_seed_production_pct']:.6f} "
            f"paternity_n={p['paternity_n_total']} qa_C_from_visible_counts={qa_text}"
        )
    print(
        "MAGNOLIA_EFFECTS "
        f"n={len(pops)} r_C={r_c:.12f} z_C={z_c:.12f} var_C={var:.12f} "
        f"r_F={r_f:.12f} z_F={z_f:.12f} var_F={var:.12f} "
        f"residual_r_CF={r_res:.12f} covariance_CF={cov:.12f} det={det:.12f}"
    )
    print("MAGNOLIA_POPULATION_CLUSTER_RECOVERY PASS")


if __name__ == "__main__":
    main()
