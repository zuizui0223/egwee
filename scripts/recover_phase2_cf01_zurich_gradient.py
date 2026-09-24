from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import statistics as stats
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPOSURE = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_exposure_v1.csv"
VISITATION = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_visitation_source_v1.csv"
SOURCE_MANIFEST = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_source_manifest_v1.json"
ENVIDAT_SCHEMA = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_envidat_schema_v1.json"
CONTRACT = ROOT / "manuscript/CF01_ZURICH_2026_GRADIENT_RECOVERY_CONTRACT.md"

VALUES = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_garden_values_v1.csv"
EFFECTS = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_gradient_effects_v1.csv"
COVARIANCE = ROOT / "evidence/meta_extraction/phase2_cf01_zurich_gradient_covariance_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF01_ZURICH_GRADIENT_RECOVERY_2026-09-24.md"

PROGRAMME = "P2_CF01_ZURICH_2026"
ARTICLE_DOI = "10.1111/1365-2664.70384"
DATA_DOI = "10.16904/envidat.676"
SOURCE_COMMIT = "d6361f6874398e797322afe07a8fea85a3c7e927"

PLANTS = {
    "Daucus_carota": {
        "f_file": "daucus_carota_seed_set.csv",
        "f_endpoint": "mean_seeds_per_umbel",
        "f_kind": "mean",
        "value": "n_seeds",
        "exclude_ids": {"39"},
    },
    "Raphanus_sativus": {
        "f_file": "raphanus_sativus_fruit_set.csv",
        "f_endpoint": "fruit_set",
        "f_kind": "ratio",
        "success": "n_flowers_with_fruits",
        "failure": "n_flowers_without_fruits",
        "exclude_ids": {"39"},
    },
    "Onobrychis_viciifolia": {
        "f_file": "onobrychis_viciifolia_fruit_set.csv",
        "f_endpoint": "fruit_set",
        "f_kind": "ratio",
        "success": "n_flowers_with_fruits",
        "failure": "n_flowers_without_fruits",
        "exclude_ids": {"19", "28", "39", "52"},
        "require_nonzero": "n_inflorescences_assessed",
    },
    "Symphytum_officinale": {
        "f_file": "symphytum_officinale_fruit_set.csv",
        "f_endpoint": "fruit_set",
        "f_kind": "ratio",
        "success": "n_flowers_with_seeds",
        "failure": "n_flowers_without_seeds",
        "exclude_ids": {"39"},
    },
}

Z95 = 1.959963984540054


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def basename(name: str) -> str:
    return name.rstrip("/").split("/")[-1]


def zip_csv_rows(zf: zipfile.ZipFile, short_name: str) -> tuple[list[dict[str, str]], bytes]:
    matches = [n for n in zf.namelist() if basename(n) == short_name]
    assert len(matches) == 1, (short_name, matches)
    raw = zf.read(matches[0])
    text = raw.decode("utf-8-sig", errors="strict")
    return list(csv.DictReader(io.StringIO(text))), raw


def number(value: str) -> float | None:
    text = (value or "").strip()
    if text == "" or text.casefold() in {"na", "nan", "null"}:
        return None
    try:
        x = float(text)
    except ValueError:
        return None
    return x if math.isfinite(x) else None


def pearson(x: list[float], y: list[float]) -> float:
    assert len(x) == len(y) >= 4
    mx, my = stats.mean(x), stats.mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    sx = math.sqrt(sum(v * v for v in dx))
    sy = math.sqrt(sum(v * v for v in dy))
    assert sx > 0 and sy > 0
    return sum(a * b for a, b in zip(dx, dy)) / (sx * sy)


def residuals(x: list[float], y: list[float]) -> list[float]:
    assert len(x) == len(y) >= 4
    mx, my = stats.mean(x), stats.mean(y)
    denom = sum((v - mx) ** 2 for v in x)
    assert denom > 0
    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / denom
    intercept = my - slope * mx
    return [b - (intercept + slope * a) for a, b in zip(x, y)]


def fisher_effect(x: list[float], y: list[float]) -> tuple[float, float, float]:
    r = pearson(x, y)
    assert -1 < r < 1
    z = math.atanh(r)
    variance = 1.0 / (len(x) - 3)
    return r, z, variance


def aggregate_f(rows_in: list[dict[str, str]], spec: dict) -> dict[str, dict[str, float]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows_in:
        gid = (row.get("Id") or "").strip()
        if not gid or gid in spec["exclude_ids"]:
            continue
        req = spec.get("require_nonzero")
        if req:
            val = number(row.get(req, ""))
            if val is None or val == 0:
                continue
        grouped[gid].append(row)

    out: dict[str, dict[str, float]] = {}
    for gid, rr in grouped.items():
        if spec["f_kind"] == "mean":
            vals = [number(r.get(spec["value"], "")) for r in rr]
            vals = [x for x in vals if x is not None]
            if not vals:
                continue
            out[gid] = {
                "F_value": stats.mean(vals),
                "F_n_lower_rows": float(len(vals)),
                "F_success_sum": math.nan,
                "F_total_sum": math.nan,
            }
        else:
            success = [number(r.get(spec["success"], "")) for r in rr]
            failure = [number(r.get(spec["failure"], "")) for r in rr]
            pairs = [
                (a, b)
                for a, b in zip(success, failure)
                if a is not None and b is not None
            ]
            if not pairs:
                continue
            s = sum(a for a, _ in pairs)
            f = sum(b for _, b in pairs)
            total = s + f
            if total <= 0:
                continue
            out[gid] = {
                "F_value": s / total,
                "F_n_lower_rows": float(len(pairs)),
                "F_success_sum": s,
                "F_total_sum": total,
            }
    return out


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: recover_phase2_cf01_zurich_gradient.py ENVIDAT.zip")
    archive = Path(sys.argv[1])

    for path in (EXPOSURE, VISITATION, SOURCE_MANIFEST, ENVIDAT_SCHEMA, CONTRACT, archive):
        assert path.is_file(), path

    source_manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    assert source_manifest["programme_id"] == PROGRAMME
    assert source_manifest["source_commit"] == SOURCE_COMMIT
    assert source_manifest["effect_outcomes_opened"] is False

    exposure_rows = rows(EXPOSURE)
    assert len(exposure_rows) == 24
    exposure = {r["garden_id"]: float(r["Urban_500"]) for r in exposure_rows}
    assert len(exposure) == 24
    assert all(0 <= x <= 1 for x in exposure.values())
    assert next(r for r in exposure_rows if r["garden_id"] == "39")["source_exclusion_status"] == "source_excluded_low_sampling"

    visitation_rows = rows(VISITATION)
    assert len(visitation_rows) == 24 * 4
    visit: dict[tuple[str, str], float] = {}
    for r in visitation_rows:
        key = (r["garden_id"], r["phytometer"])
        assert key not in visit
        count = float(r["raw_all_pollinator_count"])
        minutes = float(r["sampling_effort_min"])
        expected = count / (minutes / 60 / 9)
        assert abs(float(r["capture_rate_per_9h"]) - expected) < 1e-10
        visit[key] = expected

    envidat_schema = json.loads(ENVIDAT_SCHEMA.read_text(encoding="utf-8"))
    assert envidat_schema["garden_ids"] == [r["garden_id"] for r in exposure_rows]
    expected_archive_sha = envidat_schema["archive_sha256"]
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == expected_archive_sha

    garden_value_rows = []
    effect_rows = []
    covariance_blocks = {}

    with zipfile.ZipFile(archive) as zf:
        for plant, spec in PLANTS.items():
            f_rows, raw = zip_csv_rows(zf, spec["f_file"])
            expected_file = envidat_schema["csv_files"][spec["f_file"]]
            assert hashlib.sha256(raw).hexdigest() == expected_file["sha256"]
            assert len(f_rows) == expected_file["data_rows"]

            f_by_garden = aggregate_f(f_rows, spec)
            common = sorted(
                gid for gid in exposure
                if gid not in spec["exclude_ids"]
                and (gid, plant) in visit
                and gid in f_by_garden
            , key=int)
            assert len(common) >= 4, (plant, common)

            x = [exposure[g] for g in common]
            i = [visit[(g, plant)] for g in common]
            f = [f_by_garden[g]["F_value"] for g in common]

            r_i, z_i, v_i = fisher_effect(x, i)
            r_f, z_f, v_f = fisher_effect(x, f)

            ri = residuals(x, i)
            rf = residuals(x, f)
            rho_if = pearson(ri, rf)
            cov = rho_if * math.sqrt(v_i * v_f)
            eig_low = 0.5 * ((v_i + v_f) - math.sqrt((v_i - v_f) ** 2 + 4 * cov ** 2))
            eig_high = 0.5 * ((v_i + v_f) + math.sqrt((v_i - v_f) ** 2 + 4 * cov ** 2))
            assert eig_low > 1e-12, (plant, rho_if, eig_low, eig_high)

            delta = z_i - z_f
            delta_var = v_i + v_f - 2 * cov
            assert delta_var > 0
            delta_se = math.sqrt(delta_var)
            delta_stat = delta / delta_se
            p = math.erfc(abs(delta_stat) / math.sqrt(2))
            ci_low = delta - Z95 * delta_se
            ci_high = delta + Z95 * delta_se

            for gid in common:
                fv = f_by_garden[gid]
                garden_value_rows.append({
                    "programme_id": PROGRAMME,
                    "phytometer": plant,
                    "garden_id": gid,
                    "Urban_500": f"{exposure[gid]:.12g}",
                    "I_all_pollinator_capture_rate_per_9h": f"{visit[(gid, plant)]:.12g}",
                    "F_endpoint": spec["f_endpoint"],
                    "F_value": f"{fv['F_value']:.12g}",
                    "F_n_lower_rows": str(int(fv["F_n_lower_rows"])),
                    "F_success_sum": "" if math.isnan(fv["F_success_sum"]) else f"{fv['F_success_sum']:.12g}",
                    "F_total_sum": "" if math.isnan(fv["F_total_sum"]) else f"{fv['F_total_sum']:.12g}",
                    "independent_unit": "garden",
                    "source_exclusion_status": "included_common_frame",
                })

            for layer, endpoint, r, z, v in (
                ("I", "all_pollinator_capture_rate_per_9h", r_i, z_i, v_i),
                ("F", spec["f_endpoint"], r_f, z_f, v_f),
            ):
                effect_rows.append({
                    "programme_id": PROGRAMME,
                    "phytometer": plant,
                    "article_doi": ARTICLE_DOI,
                    "dataset_doi": DATA_DOI,
                    "layer": layer,
                    "endpoint": endpoint,
                    "exposure": "Urban_500",
                    "n_independent": str(len(common)),
                    "transform": "source_defined_Urban_500_proportion_higher_more_habitat_loss",
                    "effect_stream": "fisher_z_gradient",
                    "r": f"{r:.12f}",
                    "raw_effect_fisher_z": f"{z:.12f}",
                    "raw_variance": f"{v:.12f}",
                    "orientation_multiplier": "1",
                    "oriented_effect": f"{z:.12f}",
                    "oriented_variance": f"{v:.12f}",
                    "effect_unit_status": "fisher_z_admissible",
                    "independent_unit": "garden",
                    "source_location": (
                        "BetterBlooms jae explanatory/visitation source + "
                        f"EnviDat {spec['f_file']}"
                    ),
                    "effect_unit_note": (
                        "One phytometer endpoint within one Zurich programme; gardens are independent. "
                        "Plant/flower/fruit/pollinator observations are nested and do not increase n."
                    ),
                })

            covariance_blocks[plant] = {
                "garden_ids": common,
                "n_independent": len(common),
                "I_endpoint": "all_pollinator_capture_rate_per_9h",
                "F_endpoint": spec["f_endpoint"],
                "I_r": r_i,
                "F_r": r_f,
                "I_fisher_z": z_i,
                "F_fisher_z": z_f,
                "marginal_variance_I": v_i,
                "marginal_variance_F": v_f,
                "residual_correlation_IF": rho_if,
                "sampling_covariance_proxy_IF": cov,
                "covariance_matrix": [[v_i, cov], [cov, v_f]],
                "eigenvalues_ascending": [eig_low, eig_high],
                "positive_definite": True,
                "I_minus_F": {
                    "delta": delta,
                    "variance": delta_var,
                    "se": delta_se,
                    "z": delta_stat,
                    "p_two_sided": p,
                    "ci95": [ci_low, ci_high],
                },
            }

    assert len(effect_rows) == 8
    assert len(covariance_blocks) == 4
    assert all(x["positive_definite"] for x in covariance_blocks.values())

    with VALUES.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(garden_value_rows[0]))
        w.writeheader()
        w.writerows(garden_value_rows)

    with EFFECTS.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(effect_rows[0]))
        w.writeheader()
        w.writerows(effect_rows)

    covariance = {
        "schema_version": 1,
        "programme_id": PROGRAMME,
        "article_doi": ARTICLE_DOI,
        "dataset_doi": DATA_DOI,
        "source_code_commit": SOURCE_COMMIT,
        "exposure": "Urban_500",
        "dependence_method": (
            "residual-correlation proxy after separate endpoint ~ intercept + Urban_500 fits; "
            "Cov_ij=rho_ij*sqrt(V_i*V_j)"
        ),
        "phytometer_blocks": covariance_blocks,
        "programme_independence_note": (
            "Four phytometer pairs share the same experiment and are not independent programmes."
        ),
    }
    COVARIANCE.write_text(json.dumps(covariance, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = []
    for plant in PLANTS:
        b = covariance_blocks[plant]
        lines.append(
            f"- {plant}: n={b['n_independent']}, I z={b['I_fisher_z']:+.3f}, "
            f"F z={b['F_fisher_z']:+.3f}, I-F={b['I_minus_F']['delta']:+.3f}, "
            f"95% CI [{b['I_minus_F']['ci95'][0]:+.3f}, {b['I_minus_F']['ci95'][1]:+.3f}]"
        )

    STATUS.write_text(
        f"""# CFTQ0018 Zurich gradient recovery — 2026-09-24

## Decision

The Zurich BetterBlooms programme passes the registered continuous-gradient effect-unit gate as one
**gradient/generalisation multilayer programme**.

- source-defined severity: `Urban_500`, proportion impervious surface within 500 m;
- independent unit: garden;
- source gardens: 24;
- source-wide low-effort exclusion: garden 39;
- phytometer-specific source exclusions are preserved;
- effect representation: Fisher z of Pearson r;
- primary Hedges-g programme count increment: **0**.

The four phytometer species are repeated endpoint panels within the same experimental programme and
are not four independent studies.

## Recovered phytometer pairs

{chr(10).join(lines)}

Negative Fisher z means lower biological support/function with increasing densification/habitat
loss. No pair is selected or discarded based on its direction or interval.

## Dependence

For each phytometer, I and F share the same common garden frame. The working I/F covariance is
reconstructed from residual correlations after separate linear fits on `Urban_500`. All four 2x2
working covariance blocks are positive definite.

This covariance is an approximate reconstructed proxy, not an exact analytic sampling covariance.

## Scope

This programme enters only the separately analysed Fisher-z gradient/generalisation stream.

It does not:

- convert the urban gradient into a binary fragmented/reference contrast;
- increment direct I-F Hedges-g coverage;
- treat four phytometers as four independent programmes;
- alter the frozen Phase-1 five-cluster Fisher synthesis.
""",
        encoding="utf-8",
    )

    print(
        "PHASE2_CF01_ZURICH_GRADIENT_OK "
        + " ".join(
            f"{plant}:n={covariance_blocks[plant]['n_independent']}"
            for plant in PLANTS
        )
        + " covariance_blocks=4 all_PD=true primary_Hedges_increment=0"
    )


if __name__ == "__main__":
    main()
