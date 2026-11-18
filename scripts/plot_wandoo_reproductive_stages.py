#!/usr/bin/env python3
"""Render the fixed Wandoo common-11 conditional associations.

Run analyze_wandoo_reproductive_stages.py first. This renderer only rescales
its existing coefficients and nominal confidence limits; it does not fit or
select additional models. Each x-unit is one SD of the named log10 predictor,
and each y-effect is measured in SD of the published population-mean outcome.
"""

import os
from pathlib import Path
from tempfile import gettempdir

os.environ.setdefault("MPLCONFIGDIR", str(Path(gettempdir()) / "egwee-mplconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT / "evidence/meta_extraction/wandoo_reproductive_stages_20261019"
OUT = ROOT / "manuscript/figures"
ENDPOINTS = [
    ("fruits_per_branch_y2", "Fruit production", "Fruits per branch"),
    ("fruit_flower_ratio_y2", "Fruit establishment", "Mean fruit:flower ratio"),
    ("seeds_per_fruit_y2", "Seed filling", "Seeds per formed fruit"),
]
MODELS = [
    ("I_plus_log10_size", "Population size", "population_size", "#287A9F", "s"),
    ("I_plus_log10_ec", "Soil conductivity (EC)", "ec_ms_per_m", "#C05739", "o"),
]


def main():
    env = pd.read_csv(str(PREFIX) + "_table1.csv")
    stages = pd.read_csv(str(PREFIX) + "_table6.csv")
    fits = pd.read_csv(str(PREFIX) + "_model_fits.csv")
    joined = env.merge(stages, on="population", validate="one_to_one")
    common = joined.loc[joined["seeds_per_fruit_y2_mean"].notna()].copy()
    if set(common.population) != set("JKFCEGBIAHD"):
        raise ValueError("Figure requires the fixed common-11 population frame")

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.spines.left": False, "axes.edgecolor": "#D0D6DC",
        "svg.hashsalt": "egwee-wandoo-20261019",
    })
    fig, ax = plt.subplots(figsize=(11.5, 7.2))
    fig.subplots_adjust(left=0.29, right=0.77, top=0.74, bottom=0.29)
    ax.axvline(0, color="#667482", linewidth=1, zorder=0)
    ax.set_facecolor("white")
    ax.grid(axis="x", color="#E8EDF1", linewidth=0.7)
    y_ticks, y_labels, plotted = [], [], []
    for index, (endpoint, stage, unit) in enumerate(ENDPOINTS):
        centre = 4 - 2 * index
        y_ticks.append(centre)
        y_labels.append(stage + "\n" + unit)
        for m_index, (model, label, variable, colour, marker) in enumerate(MODELS):
            row = fits.loc[(fits.frame == "common11") &
                           (fits.endpoint == endpoint) & (fits.model == model)]
            if len(row) != 1:
                raise ValueError(f"Expected one existing result for {endpoint}/{model}")
            r = row.iloc[0]
            scale = np.log10(common[variable]).std(ddof=1) / common[endpoint + "_mean"].std(ddof=1)
            estimate = r.added_coef * scale
            lo, hi = r.added_ci95_low * scale, r.added_ci95_high * scale
            y = centre + (0.23 if m_index == 0 else -0.23)
            ax.errorbar(estimate, y, xerr=[[estimate-lo], [hi-estimate]],
                        fmt=marker, color=colour, markersize=7, capsize=4,
                        elinewidth=1.8, label=label if index == 0 else None, zorder=3)
            p = float(r.added_p_holm_primary)
            ax.text(1.055, y, f"{p:.3f}", transform=ax.get_yaxis_transform(),
                    va="center", ha="left", color=colour, fontsize=11)
            plotted.extend([lo, hi])
    ax.set_yticks(y_ticks, y_labels)
    ax.tick_params(axis="y", length=0, pad=17)
    ax.set_ylim(-0.75, 4.8)
    ax.set_xlim(min(plotted)-0.18, max(plotted)+0.18)
    ax.set_xlabel("Conditional association (standardized coefficient)", labelpad=12)
    ax.text(1.055, 4.72, "Holm p", transform=ax.get_yaxis_transform(),
            ha="left", va="bottom", color="#3E4C59", fontsize=10, fontweight="bold")
    fig.text(0.075, 0.94, "Wandoo: environment and reproductive stage",
             fontsize=19, weight="bold", color="#172B3A")
    fig.text(0.075, 0.886, "Same 11 populations, year 2  |  Each association adjusts for pollen-tube count",
             fontsize=11.5, color="#50616F")
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.074, 0.845),
               frameon=False, ncol=2, columnspacing=2.5, handlelength=1.8)
    fig.text(0.075, 0.115,
             "Bars: nominal 95% t intervals, not simultaneous intervals. Holm p values cover all six additions.\n"
             "Size and EC enter separate models; this does not establish independent causal pathways or a stage-difference test.\n"
             "Population L has zero fruit and undefined seeds/fruit. Its inclusion in the fruit-stage sensitivity is reported separately.",
             fontsize=9.5, color="#50616F", linespacing=1.6)
    fig.text(0.075, 0.03,
             "Source: Llorens et al. (2018), Tables 1 & 6  |  EGWEE exploratory reanalysis, 2026-10-19",
             fontsize=9, color="#687986")
    OUT.mkdir(parents=True, exist_ok=True)
    stem = OUT / "wandoo_reproductive_stages_20261019"
    fig.savefig(stem.with_suffix(".png"), dpi=180, facecolor="white", metadata={"Software": "EGWEE"})
    fig.savefig(stem.with_suffix(".svg"), facecolor="white", metadata={"Date": None, "Creator": "EGWEE"})
    plt.close(fig)
    print(stem.with_suffix(".png").relative_to(ROOT))
    print(stem.with_suffix(".svg").relative_to(ROOT))


if __name__ == "__main__":
    main()
