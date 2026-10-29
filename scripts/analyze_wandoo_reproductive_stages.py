"""Fixed retrospective Wandoo reproductive-stage comparison.

Read source snapshots, reconstruct Tables 1/6 without hand-entering numerical CSV
values, check the independent PDF text extraction and legacy overlap, then fit
the complete model set in the accompanying pre-computation design.

No network access or GitHub mutation. Population is the independent unit.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
from pathlib import Path

import numpy as np
import scipy
from scipy import stats
from scipy.linalg import qr, solve_triangular

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "evidence/meta_extraction"
PREFIX = "wandoo_reproductive_stages_20261019"
SOURCE = BASE / f"{PREFIX}_source_tables.txt"
DESIGN = BASE / f"{PREFIX}_design.md"
TABLE1 = BASE / f"{PREFIX}_table1.csv"
TABLE6 = BASE / f"{PREFIX}_table6.csv"
LEGACY = BASE / "PS019_eucalyptus_wandoo_2018_population_table_v1.csv"
DOI = "10.3389/fevo.2018.00039"
SOURCE_SHA = "5a6754d2ca4053d8ecce54f57c28e965ea015fec"
COMMON = ["J", "K", "F", "C", "E", "G", "B", "I", "A", "H", "D"]
NATIVE = ["J", "L", "K", "F", "C", "E", "G", "B", "I", "A", "H", "D"]
ORDER = ["J", "L", "S", "K", "O", "R", "F", "C", "N", "E", "G", "B", "I", "Q", "M", "A", "P", "H", "D"]
UNMEASURED = {"S", "O", "R", "N", "Q", "M", "P"}
ENV_KEYS = [
    "population_size", "isolation", "shape", "weed_cover_pct", "ec_ms_per_m",
    "ph", "total_n_pct", "phosphorus_mg_per_kg", "potassium_mg_per_kg", "organic_c_pct",
]
REPRO = [
    "flowers_per_branch_y2", "flowers_per_branch_y3",
    "fruits_per_branch_y2", "fruits_per_branch_y3",
    "fruit_flower_ratio_y2", "seeds_per_fruit_y1", "seeds_per_fruit_y2",
]
POLLEN = "pollen_tubes_y2"
ENDPOINTS = ["fruits_per_branch_y2", "fruit_flower_ratio_y2", "seeds_per_fruit_y2"]
MODELS = {
    "I_only": None,
    "I_plus_log10_size": "log10_population_size",
    "I_plus_log10_ec": "log10_ec_ms_per_m",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_text(rows: list[dict]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def section(text: str, name: str) -> list[str]:
    body = text.split("## " + name, 1)[1].split("\n## ", 1)[0]
    return [line for line in body.splitlines() if re.match(r"^[A-Z](?:  \|| )", line)]


def blank(value: str) -> str:
    return "" if value in {"–", "—", "-"} else value


def mean_se(value: str) -> tuple[str, str]:
    if blank(value) == "":
        return "", ""
    found = re.fullmatch(r"(\d+(?:\.\d+)?) \((\d+(?:\.\d+)?)\)", value)
    if not found:
        raise AssertionError(f"Cannot parse source mean (SE): {value!r}")
    return found.group(1), found.group(2)


def parse_pdf_table6(line: str) -> dict[str, str]:
    tokens = re.findall(r"\d+(?:\.\d+)?|[–—-]", line[1:])
    result = {"population": line[0], "n_reproductive": blank(tokens[0])}
    cursor = 1
    for endpoint in REPRO:
        if blank(tokens[cursor]) == "":
            result[endpoint + "_mean"] = result[endpoint + "_se"] = ""
            cursor += 1
        else:
            result[endpoint + "_mean"] = tokens[cursor]
            result[endpoint + "_se"] = tokens[cursor + 1]
            cursor += 2
    result["n_pollen"] = blank(tokens[cursor])
    cursor += 1
    if blank(tokens[cursor]) == "":
        result[POLLEN + "_mean"] = result[POLLEN + "_se"] = ""
        cursor += 1
    else:
        result[POLLEN + "_mean"] = tokens[cursor]
        result[POLLEN + "_se"] = tokens[cursor + 1]
        cursor += 2
    assert cursor == len(tokens), (line, cursor, tokens)
    return result


def reconstruct() -> tuple[list[dict[str, str]], list[dict[str, str]], dict]:
    source = SOURCE.read_text(encoding="utf-8")
    html1 = section(source, "HTML Table 1")
    html6 = section(source, "HTML Table 6")
    pdf1 = section(source, "PDF Table 1")
    pdf6 = section(source, "PDF Table 6")
    assert len(html1) == len(html6) == len(pdf1) == len(pdf6) == 19
    first, sixth = [], []
    for line in html1:
        parts = [part.strip() for part in line.split("|")]
        assert len(parts) == 12, line
        result = {"population": parts[0]}
        result.update(zip(ENV_KEYS, parts[2:]))
        result["remnant_type"] = parts[1].replace(" [c]", "")
        result["remnant_type_note"] = "large_reserve_source_footnote_c" if "[c]" in parts[1] else ""
        result.update(source_table="Table 1", source_pdf_page="4", source_doi=DOI)
        first.append(result)
    for line in html6:
        parts = [part.strip() for part in line.split("|")]
        assert len(parts) == 11, line
        result = {"population": parts[0], "n_reproductive": blank(parts[1]), "n_pollen": blank(parts[9])}
        for endpoint, token in zip(REPRO, parts[2:9]):
            result[endpoint + "_mean"], result[endpoint + "_se"] = mean_se(token)
        result[POLLEN + "_mean"], result[POLLEN + "_se"] = mean_se(parts[10])
        result["measurement_status"] = "not_measured_logistical" if not result["n_reproductive"] else "measured"
        result["seed_per_fruit_status"] = (
            "undefined_no_fruits" if result["population"] == "L" else result["measurement_status"]
        )
        result.update(source_table="Table 6", source_pdf_page="9", source_doi=DOI)
        sixth.append(result)
    assert [r["population"] for r in first] == [r["population"] for r in sixth] == ORDER

    pdf1_by, pdf6_by = {}, {}
    for line in pdf1:
        tokens = line.split()
        assert len(tokens[-10:]) == len(ENV_KEYS)
        for token in tokens[-10:]:
            float(token)
        pdf1_by[tokens[0]] = dict(zip(ENV_KEYS, tokens[-10:]))
    for line in pdf6:
        parsed = parse_pdf_table6(line)
        pdf6_by[parsed["population"]] = parsed
    assert list(pdf1_by) == list(pdf6_by) == ORDER
    checked = 0
    for row in first:
        for key in ENV_KEYS:
            assert row[key] == pdf1_by[row["population"]][key], (row["population"], key)
            checked += 1
    for row in sixth:
        for key, value in pdf6_by[row["population"]].items():
            assert row[key] == value, (row["population"], key, row[key], value)
            if key != "population":
                checked += 1

    by6 = {row["population"]: row for row in sixth}
    native = [r["population"] for r in sixth if r["n_reproductive"]]
    common = [r["population"] for r in sixth if r["seeds_per_fruit_y2_mean"]]
    assert native == NATIVE and common == COMMON
    assert {r["population"] for r in sixth if not r["n_reproductive"]} == UNMEASURED
    ell = by6["L"]
    for endpoint in ("fruits_per_branch_y2", "fruits_per_branch_y3", "fruit_flower_ratio_y2"):
        assert float(ell[endpoint + "_mean"]) == 0 and float(ell[endpoint + "_se"]) == 0
    assert ell["n_reproductive"] == "3" and ell["n_pollen"] == "4"
    assert float(ell[POLLEN + "_mean"]) == 6.7
    for endpoint in ("seeds_per_fruit_y1", "seeds_per_fruit_y2"):
        assert ell[endpoint + "_mean"] == ell[endpoint + "_se"] == ""
    for row in sixth:
        for endpoint in REPRO + [POLLEN]:
            value, uncertainty = row[endpoint + "_mean"], row[endpoint + "_se"]
            assert bool(value) == bool(uncertainty)
            if value:
                assert float(value) >= 0 and float(uncertainty) >= 0
                if endpoint == "fruit_flower_ratio_y2":
                    assert float(value) <= 1

    legacy = read_csv(LEGACY)
    assert [r["population"] for r in legacy] == ORDER
    by1 = {r["population"]: r for r in first}
    legacy_checks = 0
    for old in legacy:
        pop = old["population"]
        for key in ("population_size", "isolation", "shape"):
            assert float(old[key]) == float(by1[pop][key])
            legacy_checks += 1
        for oldkey, newkey in (("pollen_tubes", POLLEN + "_mean"), ("seeds_per_fruit_y2", "seeds_per_fruit_y2_mean")):
            value = by6[pop][newkey]
            assert bool(old[oldkey]) == bool(value)
            if value:
                assert float(old[oldkey]) == float(value)
            legacy_checks += 1
    checks = {
        "html_pdf_source_token_checks": checked,
        "legacy_value_or_missingness_checks": legacy_checks,
        "source_populations": 19,
        "source_native_reproductive_populations": 12,
        "common_complete_seed_populations": 11,
        "L_seed_per_fruit_zero_imputed": False,
        "source_SE_retained_not_used_as_population_weights": True,
        "pdf_pages_checked_text_layer": [4, 9],
    }
    return first, sixth, checks


def assert_close(a, b, label: str) -> None:
    if not np.allclose(a, b, rtol=1e-9, atol=1e-9):
        raise AssertionError(f"Independent mathematical check failed: {label}: {a} != {b}")


def fit_ols(x: np.ndarray, y: np.ndarray) -> dict:
    beta, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    assert rank == x.shape[1], "Rank-deficient fixed model; do not silently change the model."
    n, p = x.shape
    df = n - p
    assert df > 0
    predicted = x @ beta
    residual = y - predicted
    sse = float(residual @ residual)
    tss = float(np.sum((y - np.mean(y)) ** 2))
    covariance = np.linalg.inv(x.T @ x) * (sse / df)
    se = np.sqrt(np.diag(covariance))
    t_values = beta / se
    p_values = 2 * stats.t.sf(np.abs(t_values), df)
    critical = stats.t.ppf(0.975, df)
    low, high = beta - critical * se, beta + critical * se
    leverage = np.einsum("ij,jk,ik->i", x, np.linalg.inv(x.T @ x), x)
    assert np.all(leverage < 1 - 1e-10)
    loo_predictions = np.empty(n)
    for held in range(n):
        keep = np.arange(n) != held
        coef, _, loo_rank, _ = np.linalg.lstsq(x[keep], y[keep], rcond=None)
        assert loo_rank == p
        loo_predictions[held] = x[held] @ coef
    loo_error = y - loo_predictions
    assert_close(loo_error, residual / (1 - leverage), "direct LOO vs analytical PRESS")
    # Independent QR implementation avoids using normal equations or the SVD
    # least-squares solver used above. The t/F identity checks the tail areas.
    q_ref, r_ref = qr(x, mode="economic")
    beta_ref = solve_triangular(r_ref, q_ref.T @ y)
    predicted_ref = x @ beta_ref
    residual_ref = y - predicted_ref
    inverse_r = solve_triangular(r_ref, np.eye(p))
    se_ref = np.sqrt(np.diag(inverse_r @ inverse_r.T) * float(residual_ref @ residual_ref) / df)
    p_ref = stats.f.sf((beta_ref / se_ref)**2, 1, df)
    for left, right, label in (
        (beta, beta_ref, "OLS coefficient"),
        (se, se_ref, "OLS SE"),
        (p_values, p_ref, "OLS t/F tail-area identity"),
        (predicted, predicted_ref, "OLS fitted mean"),
        (leverage, np.sum(q_ref**2, axis=1), "leverage"),
        (np.column_stack((low, high)), np.column_stack((beta_ref-critical*se_ref, beta_ref+critical*se_ref)), "OLS 95% CI"),
    ):
        assert_close(left, right, label)
    reverse_coef = np.linalg.lstsq(x[::-1], y[::-1], rcond=None)[0]
    assert_close(beta, reverse_coef, "row-order invariance")
    return {
        "beta": beta, "se": se, "p": p_values, "low": low, "high": high,
        "predicted": predicted, "residual": residual, "leverage": leverage,
        "loo_predictions": loo_predictions, "loo_error": loo_error,
        "sse": sse, "df": df, "r2": 1 - sse/tss,
        "adjusted_r2": 1 - (sse/df)/(tss/(n-1)),
        "loo_mse": float(np.mean(loo_error**2)),
    }


def holm(values: list[float]) -> list[float]:
    order = np.argsort(values)
    answer = np.zeros(len(values))
    running = 0.0
    for index, original in enumerate(order):
        running = max(running, (len(values) - index) * values[original])
        answer[original] = min(1.0, running)
    assert np.all(answer >= np.asarray(values))
    assert np.all(np.diff(answer[order]) >= -1e-15)
    # Check adjusted-p rejection decisions against the step-down procedure.
    for alpha in (0.01, 0.05, 0.1, 0.2):
        reject = np.zeros(len(values), dtype=bool)
        for index, original in enumerate(order):
            if values[original] > alpha / (len(values) - index):
                break
            reject[original] = True
        assert np.array_equal(answer <= alpha, reject)
    return answer.tolist()


def correlation(x, y) -> float:
    return float(np.corrcoef(x, y)[0, 1])


def analyse(first, sixth, input_checks) -> tuple[dict, list[dict], list[dict], list[dict], list[dict]]:
    by1, by6 = {r["population"]: r for r in first}, {r["population"]: r for r in sixth}
    fit_rows, coefficient_rows, prediction_rows = [], [], []
    for frame, names, endpoints in (
        ("common11", COMMON, ENDPOINTS),
        ("native12", NATIVE, ENDPOINTS[:2]),
    ):
        interaction = np.array([float(by6[n][POLLEN + "_mean"]) for n in names])
        context = {
            "log10_population_size": np.log10([float(by1[n]["population_size"]) for n in names]),
            "log10_ec_ms_per_m": np.log10([float(by1[n]["ec_ms_per_m"]) for n in names]),
        }
        for endpoint in endpoints:
            y = np.array([float(by6[n][endpoint + "_mean"]) for n in names])
            base = fit_ols(np.column_stack((np.ones(len(names)), interaction)), y)
            for model, added in MODELS.items():
                columns = [np.ones(len(names)), interaction]
                terms = ["intercept", POLLEN]
                if added:
                    columns.append(context[added])
                    terms.append(added)
                x = np.column_stack(columns)
                fit = base if added is None else fit_ols(x, y)
                idx = len(terms) - 1
                scale = float(np.std(x[:, idx], ddof=1) / np.std(y, ddof=1)) if added else None
                partial = (base["sse"] - fit["sse"]) / base["sse"] if added else None
                if added:
                    assert_close(partial, (fit["beta"][idx]/fit["se"][idx])**2 /
                                 ((fit["beta"][idx]/fit["se"][idx])**2 + fit["df"]), "partial R2 identity")
                negative = int(np.sum(fit["loo_predictions"] < 0))
                above_one = int(np.sum(fit["loo_predictions"] > 1)) if endpoint == "fruit_flower_ratio_y2" else 0
                maxhat = int(np.argmax(fit["leverage"]))
                fit_rows.append({
                    "frame": frame, "endpoint": endpoint, "source_year": "y2", "model": model,
                    "n": len(names), "n_parameters": len(terms), "df_residual": fit["df"],
                    "r_squared": fit["r2"], "adjusted_r_squared": fit["adjusted_r2"],
                    "in_sample_mse": fit["sse"]/len(names), "loo_mse": fit["loo_mse"],
                    "loo_rmse": math.sqrt(fit["loo_mse"]),
                    "loo_mse_fractional_gain": 1 - fit["loo_mse"]/base["loo_mse"],
                    "added_predictor": added or "", "added_coef": float(fit["beta"][idx]) if added else "",
                    "added_se": float(fit["se"][idx]) if added else "",
                    "added_ci95_low": float(fit["low"][idx]) if added else "",
                    "added_ci95_high": float(fit["high"][idx]) if added else "",
                    "added_p": float(fit["p"][idx]) if added else "", "added_p_holm_primary": "",
                    "added_partial_r_squared": partial if added else "",
                    "added_coef_standardized": float(fit["beta"][idx])*scale if added else "",
                    "added_ci95_low_standardized": float(fit["low"][idx])*scale if added else "",
                    "added_ci95_high_standardized": float(fit["high"][idx])*scale if added else "",
                    "maximum_leverage": float(fit["leverage"][maxhat]),
                    "maximum_leverage_population": names[maxhat],
                    "loo_predictions_below_zero": negative, "loo_predictions_above_one": above_one,
                    "independent_unit": "population",
                })
                for j, term in enumerate(terms):
                    coefficient_rows.append({
                        "frame": frame, "endpoint": endpoint, "model": model, "term": term,
                        "coefficient": float(fit["beta"][j]), "se": float(fit["se"][j]),
                        "ci95_low": float(fit["low"][j]), "ci95_high": float(fit["high"][j]),
                        "p_unadjusted": float(fit["p"][j]), "df_residual": fit["df"],
                    })
                for j, population in enumerate(names):
                    keep = np.arange(len(names)) != j
                    extrapolates = bool(added and (x[j, -1] < np.min(x[keep, -1]) or x[j, -1] > np.max(x[keep, -1])))
                    pred = float(fit["loo_predictions"][j])
                    out_of_bounds = pred < 0 or (endpoint == "fruit_flower_ratio_y2" and pred > 1)
                    prediction_rows.append({
                        "frame": frame, "endpoint": endpoint, "model": model, "population": population,
                        "observed": float(y[j]), "predicted_loo": pred,
                        "error_loo_observed_minus_predicted": float(fit["loo_error"][j]),
                        "squared_error_loo": float(fit["loo_error"][j]**2),
                        "predicted_full": float(fit["predicted"][j]), "leverage_full": float(fit["leverage"][j]),
                        "loo_training_n": len(names)-1, "outside_physical_bounds": out_of_bounds,
                        "added_predictor_extrapolation": extrapolates,
                    })
    primary_rows = [r for r in fit_rows if r["frame"] == "common11" and r["added_predictor"]]
    assert len(primary_rows) == 6 and len(fit_rows) == 15 and len(prediction_rows) == 171
    for row, adjusted in zip(primary_rows, holm([r["added_p"] for r in primary_rows])):
        row["added_p_holm_primary"] = adjusted

    descriptive = []
    for frame, names in (("common11", COMMON), ("native12", NATIVE)):
        for endpoint in ("seeds_per_fruit_y1", "seeds_per_fruit_y2", "fruits_per_branch_y2", "fruits_per_branch_y3"):
            if frame == "native12" and endpoint.startswith("seeds"):
                continue
            y = [float(by6[n][endpoint + "_mean"]) for n in names]
            size = np.log10([float(by1[n]["population_size"]) for n in names])
            ec = np.log10([float(by1[n]["ec_ms_per_m"]) for n in names])
            descriptive.append({
                "frame": frame, "endpoint": endpoint, "n": len(names),
                "mean": float(np.mean(y)), "minimum": min(y), "maximum": max(y),
                "r_with_log10_size": correlation(size, y), "r_with_log10_ec": correlation(ec, y),
                "synchronous_with_pollen_y2": endpoint.endswith("y2"),
                "inferential_p_computed": False,
            })
    across_year = {}
    for endpoint, year_a, year_b in (("seeds_per_fruit", "y1", "y2"), ("fruits_per_branch", "y2", "y3")):
        across_year[endpoint + "_common11_r"] = correlation(
            [float(by6[n][f"{endpoint}_{year_a}_mean"]) for n in COMMON],
            [float(by6[n][f"{endpoint}_{year_b}_mean"]) for n in COMMON],
        )

    # A legacy-overlap mathematical check; not another newly selected model.
    def zscore(a):
        return (a - np.mean(a))/np.std(a, ddof=1)
    exposure = np.column_stack((
        -np.log10([float(r["population_size"]) for r in first]),
        np.sqrt([float(r["isolation"]) for r in first]),
        np.log10([float(r["shape"]) for r in first]),
    ))
    z = np.column_stack([zscore(exposure[:, j]) for j in range(3)])
    eigvals, eigvecs = np.linalg.eigh(np.cov(z, rowvar=False, ddof=1))
    pc = eigvecs[:, np.argmax(eigvals)]
    if pc.sum() < 0:
        pc = -pc
    severity = zscore(z @ pc)
    common_severity = severity[[ORDER.index(n) for n in COMMON]]
    pc_r = [
        correlation(common_severity, [float(by6[n][POLLEN + "_mean"]) for n in COMMON]),
        correlation(common_severity, [float(by6[n]["seeds_per_fruit_y2_mean"]) for n in COMMON]),
    ]
    assert_close(pc_r, [0.598169060460899, -0.704374898488142], "legacy PC1 overlap")
    context_correlations = {}
    for frame, names in (("common11", COMMON), ("native12", NATIVE)):
        context_correlations[frame] = correlation(
            np.log10([float(by1[n]["population_size"]) for n in names]),
            np.log10([float(by1[n]["ec_ms_per_m"]) for n in names]),
        )
    result = {
        "analysis_date": "2026-10-19", "source_baseline_sha": SOURCE_SHA,
        "design_file": DESIGN.name, "design_sha256": sha(DESIGN),
        "design_is_outcome_blind_preregistration": False,
        "source_doi": DOI, "source_url": "https://www.frontiersin.org/journals/ecology-and-evolution/articles/10.3389/fevo.2018.00039/full",
        "source_table_snapshot_sha256": sha(SOURCE),
        "table1_sha256": sha(TABLE1), "table6_sha256": sha(TABLE6), "analysis_script_sha256": sha(Path(__file__)),
        "input_validation": input_checks,
        "frames": {"common11": COMMON, "native12": NATIVE},
        "models": fit_rows, "non_synchronous_and_year_context": descriptive,
        "across_year_descriptive_correlations": across_year,
        "log_size_log_ec_correlations_descriptive": context_correlations,
        "legacy_pc1_overlap_r_I_F": pc_r,
        "mathematical_validation": {
            "independent_scipy_QR_OLS_comparisons": 15,
            "direct_LOO_PRESS_identity_models": 15,
            "row_order_invariance_models": 15,
            "partial_R2_identity_models": 10,
            "Holm_stepdown_decisions_verified": True,
            "all_checks_passed": True,
        },
        "software": {"numpy": np.__version__, "scipy": scipy.__version__},
        "claim_limits": [
            "Retrospective single-system conditional association, not causal mediation.",
            "Size and EC are separate additions, never jointly adjusted; independent pathways are not identified.",
            "Common11 excludes the no-fruit population L and is conditional on fruit establishment.",
            "Native12 is a same-system fruit-stage sensitivity, not independent replication.",
            "Published maternal-plant means have measurement error; residual context information is not uniquely an unmeasured mechanism.",
            "Primary raw scales; LOO supplementary and internal, with no clipping of unphysical predictions.",
            "Nominal coefficient intervals are not Holm-adjusted simultaneous intervals.",
            "Different significance across stages does not itself test a between-stage coefficient difference.",
            "No synchronous pollen data outside y2; no multiplication of marginal means to total seed output.",
            "The original paper already reported marginal salinity/fruit and size/seed patterns.",
        ],
    }
    return result, fit_rows, coefficient_rows, prediction_rows, descriptive


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--extract-only", action="store_true", help="Reconstruct source CSVs and validate HTML/PDF/legacy overlap; no models.")
    mode.add_argument("--write-results", action="store_true", help="Verify source CSVs, compute and verify all fixed models, write results.")
    mode.add_argument("--check", action="store_true", help="Recompute and verify all committed/generated outputs without changing files.")
    args = parser.parse_args()
    first, sixth, checks = reconstruct()
    expected_inputs = {TABLE1: csv_text(first), TABLE6: csv_text(sixth)}
    if args.extract_only:
        for path, text in expected_inputs.items():
            path.write_text(text, encoding="utf-8")
        print("WANDOO_STAGE_SOURCE_OK " + json.dumps(checks, sort_keys=True))
        return
    for path, expected in expected_inputs.items():
        assert path.read_text(encoding="utf-8") == expected, f"Source CSV diverged from HTML/PDF snapshot: {path}"
    result, fits, coefs, predictions, descriptive = analyse(first, sixth, checks)
    outputs = {
        BASE / f"{PREFIX}_results.json": json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n",
        BASE / f"{PREFIX}_model_fits.csv": csv_text(fits),
        BASE / f"{PREFIX}_coefficients.csv": csv_text(coefs),
        BASE / f"{PREFIX}_loo_predictions.csv": csv_text(predictions),
        BASE / f"{PREFIX}_year_descriptive.csv": csv_text(descriptive),
    }
    for path, expected in outputs.items():
        if args.write_results:
            path.write_text(expected, encoding="utf-8")
        else:
            assert path.read_text(encoding="utf-8") == expected, f"Stored output is not reproducible: {path}"
    compact = [
        {key: row[key] for key in ("frame", "endpoint", "model", "r_squared", "added_coef", "added_p", "added_p_holm_primary", "loo_mse_fractional_gain", "loo_predictions_below_zero")}
        for row in fits if row["added_predictor"]
    ]
    print("WANDOO_STAGE_ANALYSIS_OK " + json.dumps({
        "mode": "write" if args.write_results else "check",
        "input_validation": checks, "mathematical_validation": result["mathematical_validation"],
        "fits": compact,
    }, sort_keys=True))


if __name__ == "__main__":
    main()

