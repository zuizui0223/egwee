from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_table1_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_effects_v1.csv"
COV = ROOT / "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_covariance_v1.json"
RESULT = ROOT / "manuscript/PHASE2_CF01_CARDIOPETALUM_GRADIENT_RECOVERY_2026-09-24.md"
Z975 = 1.959963984540054


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pearson(x: list[float], y: list[float]) -> float:
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    return sum(a * b for a, b in zip(dx, dy)) / math.sqrt(
        sum(a * a for a in dx) * sum(b * b for b in dy)
    )


def residuals(y: list[float], x: list[float]) -> list[float]:
    mx = sum(x) / len(x)
    my = sum(y) / len(y)
    denom = sum((v - mx) ** 2 for v in x)
    beta = sum((xx - mx) * (yy - my) for xx, yy in zip(x, y)) / denom
    alpha = my - beta * mx
    return [yy - (alpha + beta * xx) for xx, yy in zip(x, y)]


def effect(x: list[float], y: list[float]) -> dict[str, float]:
    r = pearson(x, y)
    assert -1 < r < 1
    return {"r": r, "z": math.atanh(r), "variance": 1.0 / (len(x) - 3)}


def pnorm2(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def main() -> None:
    src = rows(SOURCE)
    assert [r["fragment_id"] for r in src] == [f"F{i}" for i in range(1, 11)]
    assert len(src) == 10
    assert src[-1]["seed_set_per_flower_mean"] == ""

    area = [float(r["area_ha"]) for r in src]
    distance = [float(r["distance_nearest_fragment_m"]) for r in src]
    x = [-math.log(a) for a in area]
    x_iso = [math.log(d) for d in distance]
    i = [float(r["pollinator_abundance_per_flower_mean"]) for r in src]
    f = [float(r["fruit_set_mean"]) for r in src]
    fo = [float(r["follicles_per_flower_mean"]) for r in src]

    seed_rows = [r for r in src if r["seed_set_per_flower_mean"]]
    seed_x = [-math.log(float(r["area_ha"])) for r in seed_rows]
    seed = [float(r["seed_set_per_flower_mean"]) for r in seed_rows]

    i_eff = effect(x, i)
    f_eff = effect(x, f)
    fo_eff = effect(x, fo)
    seed_eff = effect(seed_x, seed)
    i_iso = effect(x_iso, i)
    f_iso = effect(x_iso, f)

    rho = pearson(residuals(i, x), residuals(f, x))
    cov = rho * math.sqrt(i_eff["variance"] * f_eff["variance"])
    det = i_eff["variance"] * f_eff["variance"] - cov * cov
    assert det > 0

    delta = i_eff["z"] - f_eff["z"]
    var_delta = i_eff["variance"] + f_eff["variance"] - 2 * cov
    assert var_delta > 0
    se = math.sqrt(var_delta)
    zstat = delta / se
    p = pnorm2(zstat)
    ci = [delta - Z975 * se, delta + Z975 * se]

    EFFECTS.parent.mkdir(parents=True, exist_ok=True)
    with EFFECTS.open("w", newline="", encoding="utf-8") as fh:
        fields = [
            "programme_id", "endpoint_role", "layer", "endpoint", "effect_stream",
            "n_independent", "exposure", "r", "fisher_z", "variance",
            "primary_or_sensitivity", "source_location",
        ]
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for role, layer, endpoint, n, exposure, e, tier in (
            ("I_primary", "I_interaction", "pollinator_abundance_per_flower", 10, "negative_log_fragment_area_ha", i_eff, "primary"),
            ("F_primary", "F_reproductive_function", "fruit_set_per_flower", 10, "negative_log_fragment_area_ha", f_eff, "primary"),
            ("F_sensitivity_follicles", "F_reproductive_function", "follicles_set_per_flower", 10, "negative_log_fragment_area_ha", fo_eff, "sensitivity"),
            ("F_sensitivity_seed", "F_reproductive_function", "seed_set_per_flower", 9, "negative_log_fragment_area_ha", seed_eff, "sensitivity"),
            ("I_sensitivity_isolation", "I_interaction", "pollinator_abundance_per_flower", 10, "log_nearest_fragment_distance_m", i_iso, "sensitivity"),
            ("F_sensitivity_isolation", "F_reproductive_function", "fruit_set_per_flower", 10, "log_nearest_fragment_distance_m", f_iso, "sensitivity"),
        ):
            w.writerow({
                "programme_id": "P2_CF01_CARDIOPETALUM_2012",
                "endpoint_role": role,
                "layer": layer,
                "endpoint": endpoint,
                "effect_stream": "fisher_z_gradient",
                "n_independent": n,
                "exposure": exposure,
                "r": f"{e['r']:.12f}",
                "fisher_z": f"{e['z']:.12f}",
                "variance": f"{e['variance']:.12f}",
                "primary_or_sensitivity": tier,
                "source_location": "Elias et al. 2012 Table 1",
            })

    cov_result = {
        "programme_id": "P2_CF01_CARDIOPETALUM_2012",
        "status": "gradient_generalisation_multilayer_cluster_retrospective",
        "source_table": "Elias et al. 2012 Table 1",
        "fragment_ids": [r["fragment_id"] for r in src],
        "n_independent_fragments": 10,
        "primary_exposure": "negative_log_fragment_area_ha",
        "I_endpoint": "pollinator_abundance_per_flower",
        "F_endpoint": "fruit_set_per_flower",
        "I_fisher_z": i_eff["z"],
        "F_fisher_z": f_eff["z"],
        "I_variance": i_eff["variance"],
        "F_variance": f_eff["variance"],
        "residual_rho_IF": rho,
        "cov_IF": cov,
        "covariance_determinant": det,
        "delta_I_minus_F": delta,
        "se_delta": se,
        "z_delta": zstat,
        "p_delta_two_sided": p,
        "ci95_delta": ci,
        "sensitivities": {
            "follicles_per_flower": fo_eff,
            "seed_set_per_flower": seed_eff,
            "isolation_I": i_iso,
            "isolation_F": f_iso,
        },
        "primary_hedges_increment": 0,
        "retrospective_recovery": True,
    }
    COV.write_text(json.dumps(cov_result, indent=2) + "\n", encoding="utf-8")

    RESULT.write_text(
        f"""# CFTQ0166 Cardiopetalum retrospective gradient recovery — 2026-09-24

## Admission

`P2_CF01_CARDIOPETALUM_2012` is admitted as **one retrospective gradient/generalisation
I-F programme**.

The source Table 1 values and published directions were visible before the deterministic recovery
rule was written. This is therefore retrospective generalisation evidence, not prospective
confirmation.

## Effect unit

- independent forest fragments: **10**
- independent unit: **forest fragment**
- marked plants / flowers / beetles / density plots / fruits / seeds: nested below fragment

## Locked variables

- fragmentation severity: **−log(fragment area ha)**; higher = smaller fragment
- I: pollinator abundance per flower (ABP)
- F: fruit set per flower (F)

## Primary effects

- I: r = **{i_eff['r']:+.3f}**, Fisher z = **{i_eff['z']:+.3f}**
- F: r = **{f_eff['r']:+.3f}**, Fisher z = **{f_eff['z']:+.3f}**
- marginal Fisher-z variance = **{i_eff['variance']:.6f}**

The interaction layer changes relatively weakly across fragment area, whereas realized reproductive
function declines strongly toward smaller fragments.

## I-F response geometry

- residual rho(I,F) = **{rho:+.3f}**
- working Cov(z_I,z_F) = **{cov:+.6f}**
- covariance determinant = **{det:.6f}**
- I − F = **{delta:+.3f}**
- SE = **{se:.3f}**
- 95% CI = **[{ci[0]:+.3f}, {ci[1]:+.3f}]**
- two-sided p = **{p:.5f}**

The interval excludes zero. Under this retrospective fragment-area recovery, pollinator abundance
and reproductive function are therefore **non-exchangeable**: reproduction deteriorates much more
strongly than the measured beetle-pollinator abundance.

## Sensitivities

On the source table:

- follicle set per flower: Fisher z = **{fo_eff['z']:+.3f}** (n=10)
- seed set per flower: Fisher z = **{seed_eff['z']:+.3f}** (n=9; F10 remains source-missing)
- isolation exposure, I: Fisher z = **{i_iso['z']:+.3f}**
- isolation exposure, F: Fisher z = **{f_iso['z']:+.3f}**

Both alternate reproductive endpoints retain substantially stronger negative fragment-area
responses than I. The nearest-fragment-distance sensitivity also keeps F more negative than I.
These are robustness descriptions, not substitutes for the locked primary endpoints.

## Ecological interpretation

This programme provides a direct natural example of **interaction persistence with reproductive
collapse**. Beetle abundance in flowers is not sufficient to predict realized reproductive
function across fragment sizes. Fragmentation can leave the observed pollinator-presence layer
comparatively intact while local mating quality, pollen exchange, resource limitation, or other
downstream reproductive constraints deteriorate.

This complements the Aextoxicon process anchor, where incoming seed movement can remain substantial
despite low local fecundity.

## Scope

- gradient/generalisation programme increment: **+1**
- primary Fisher-z marginal effects: **+2**
- direct Hedges-g I-F increment: **0**
- Phase-1 five-cluster synthesis: unchanged
- EGWE/NEE finite-operator validation: none
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF01_CARDIOPETALUM_OK "
        f"n=10 I_z={i_eff['z']:.8f} F_z={f_eff['z']:.8f} "
        f"delta={delta:.8f} p={p:.8f} cov_pd=true retrospective=true"
    )


if __name__ == "__main__":
    main()
