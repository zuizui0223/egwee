from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
POP = ROOT / "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_population_table_v1.csv"
MATING = ROOT / "evidence/meta_extraction/if_wandoo_mating_table7_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def zscore(x: np.ndarray) -> np.ndarray:
    return (x - np.mean(x)) / np.std(x, ddof=1)


def corr(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(x, y)[0, 1])


def main() -> None:
    pop = rows(POP)
    mating = rows(MATING)
    assert len(pop) == 19
    assert len(mating) == 6
    assert {r["population"] for r in mating} == {"R", "F", "C", "E", "B", "A"}

    size = np.array([float(r["population_size"]) for r in pop])
    isolation = np.array([float(r["isolation"]) for r in pop])
    shape = np.array([float(r["shape"]) for r in pop])

    exposure = np.column_stack((-np.log10(size), np.sqrt(isolation), np.log10(shape)))
    exposure_z = np.column_stack([zscore(exposure[:, j]) for j in range(3)])
    eigval, eigvec = np.linalg.eigh(np.cov(exposure_z, rowvar=False, ddof=1))
    pc1 = eigvec[:, int(np.argmax(eigval))]
    if float(np.sum(pc1)) < 0:
        pc1 = -pc1
    severity = zscore(exposure_z @ pc1)

    pop_by_name = {r["population"]: (r, float(severity[i])) for i, r in enumerate(pop)}
    mating_by_name = {r["population"]: r for r in mating}

    mating_names = [r["population"] for r in mating]
    x_all = np.array([pop_by_name[n][1] for n in mating_names])
    tm_all = np.array([float(mating_by_name[n]["tm"]) for n in mating_names])

    overlap = [
        n for n in mating_names
        if pop_by_name[n][0]["pollen_tubes"] != ""
        and pop_by_name[n][0]["seeds_per_fruit_y2"] != ""
    ]
    assert overlap == ["F", "C", "E", "B", "A"]

    x = np.array([pop_by_name[n][1] for n in overlap])
    q = np.array([float(pop_by_name[n][0]["pollen_tubes"]) for n in overlap])
    e = np.array([float(mating_by_name[n]["tm"]) for n in overlap])
    rp = np.array([float(mating_by_name[n]["rp"]) for n in overlap])
    f = np.array([float(pop_by_name[n][0]["seeds_per_fruit_y2"]) for n in overlap])

    result = {
        "status": "post_hoc_mechanistic_triangulation_only",
        "n_mating_populations": len(mating_names),
        "n_common_Q_E_F_populations": len(overlap),
        "common_populations": overlap,
        "temporal_alignment": {
            "Q_pollen_tubes": "year_2",
            "E_tm": "seed_progeny_from_year_1",
            "F_seeds_per_fruit": "year_2",
            "synchronous_Q_E_F": False,
        },
        "correlations": {
            "fragmentation_severity_vs_tm_all6": corr(x_all, tm_all),
            "fragmentation_severity_vs_Q_overlap5": corr(x, q),
            "fragmentation_severity_vs_tm_overlap5": corr(x, e),
            "fragmentation_severity_vs_F_overlap5": corr(x, f),
            "Q_vs_tm_overlap5": corr(q, e),
            "tm_vs_F_overlap5": corr(e, f),
            "Q_vs_F_overlap5": corr(q, f),
            "Q_vs_correlated_paternity_overlap5": corr(q, rp),
        },
        "claim_ceiling": (
            "The five-population overlap is descriptive and temporally non-synchronous. "
            "It may triangulate an interaction-quantity -> mating-quality -> reproductive-function "
            "mechanism but cannot establish mediation, prevalence, or a fragmentation effect on tm."
        ),
    }

    expected = result["correlations"]
    assert abs(expected["fragmentation_severity_vs_tm_all6"] - (-0.4885664829516528)) < 1e-10
    assert abs(expected["Q_vs_tm_overlap5"] - (-0.5235190904043141)) < 1e-10
    assert abs(expected["tm_vs_F_overlap5"] - 0.6942287370032689) < 1e-10
    assert abs(expected["Q_vs_F_overlap5"] - (-0.2671523602943783)) < 1e-10

    print("WANDOO_MATING_PROVENANCE_TRIANGULATION " + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
