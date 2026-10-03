from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
PKG = BUILD / "anonymous_review_package"
ZIP = BUILD / "anonymous_review_package.zip"

FILES = [
    "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md",
    "manuscript/JOURNAL_OF_ECOLOGY_FIGURE_TABLE_PLAN.md",
    "manuscript/COVARIANCE_ROBUSTNESS_RESULT.md",
    "manuscript/ESTIMAND_SCALE_SENSITIVITY_RESULT_2026-09-27.md",
    "manuscript/ESTIMAND_SCALE_ROBUSTNESS_2026-09-29.md",
    "manuscript/BOTTLENECK_SCALE_ROBUSTNESS_2026-09-29.md",
    "manuscript/SCALE_STABLE_QUANTITY_FUNCTION_PROXY_FAILURE_2026-09-29.md",
    "manuscript/TRANSITION_SPECIFIC_FILTERING_AUDIT_2026-09-29.md",
    "manuscript/IF_SIGN_GEOMETRY_2026-09-29.md",
    "manuscript/IF_SIGN_UNCERTAINTY_2026-10-01.md",
    "manuscript/IF_PROXY_FAILURE_NOVELTY_AUDIT_2026-10-01.md",
    "manuscript/QUALITATIVE_EXTERNAL_IF_AUDIT_2026-10-03.md",
    "manuscript/META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-29_EFFECT_SCALE.md",
    "manuscript/ECOLOGICAL_IF_DIRECTION_CENSUS_2026-09-27.md",
    "manuscript/ECOLOGICAL_PROCESS_FUNCTION_CENSUS_2026-09-27.md",
    "manuscript/ECOLOGICAL_BOTTLENECK_DIRECTION_INFLUENCE_2026-09-27.md",
    "manuscript/tables/table_s1_cluster_recovery_flow.csv",
    "manuscript/tables/table_s2_covariance_robustness.csv",
    "manuscript/tables/table_s3_primary_marginal_effects.csv",
    "scripts/synthesize_state_separation.py",
    "scripts/check_covariance_robustness.py",
    "scripts/check_estimand_scale_sensitivity.py",
    "scripts/check_estimand_scale_robustness.py",
    "scripts/check_bottleneck_scale_robustness.py",
    "scripts/check_scale_stable_quantity_function_proxy_failure.py",
    "scripts/check_transition_specific_filtering.py",
    "scripts/check_if_sign_geometry.py",
    "scripts/check_if_sign_uncertainty.py",
    "scripts/check_qualitative_external_if_audit.py",
    "scripts/check_ecological_if_programme_census.py",
    "scripts/check_ecological_process_function_programme_census.py",
    "scripts/check_ecological_bottleneck_direction_influence.py",
    "scripts/check_primary_effect_supplement.py",
    "scripts/build_primary_effect_forest.py",
    "scripts/build_journal_of_ecology_figures.py",
    "evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv",
    "evidence/meta_extraction/PS003_serapias_site_table_v1.csv",
    "evidence/meta_extraction/PS004_brosimum_site_table_v1.csv",
    "evidence/meta_extraction/PS001_spondias_paternity_site_table_v1.csv",
    "evidence/meta_extraction/PS001_spondias_appendixB_genetic_site_table_v1.csv",
    "evidence/meta_extraction/PS003_serapias_primary_covariance_v1.csv",
    "evidence/meta_extraction/PS004_brosimum_extraction_v1.csv",
    "evidence/meta_extraction/PS004_brosimum_primary_covariance_v1.csv",
    "evidence/meta_extraction/PS001_spondias_site_effects_v1.csv",
    "evidence/meta_extraction/PS001_spondias_primary_pairwise_covariance_v2.csv",
    "evidence/meta_extraction/PS020_eucalyptus_socialis_effects_v1.csv",
    "evidence/meta_extraction/PS020_eucalyptus_socialis_primary_covariance_v1.csv",
    "evidence/meta_extraction/PS020_eucalyptus_socialis_sufficient_stats_v1.json",
    "evidence/meta_extraction/PS022_aizen_feinsinger_effects_v1.csv",
    "evidence/meta_extraction/PS022_aizen_feinsinger_site_means_v1.csv",
    "evidence/meta_extraction/PS022_aizen_feinsinger_covariance_v1.csv",
    "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv",
    "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_covariance_v1.csv",
    "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_effects_v1.csv",
    "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_effects_v1.csv",
    "evidence/meta_extraction/phase2_cf01_sevenello_transect_values_v1.csv",
    "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_site_values_v1.csv",
    "evidence/meta_extraction/estimand_scale_sensitivity_v1.csv",
    "evidence/meta_extraction/estimand_scale_fisher_sensitivity_v1.csv",
    "evidence/meta_extraction/estimand_scale_cluster_summary_v1.csv",
    "evidence/meta_extraction/estimand_scale_robustness_v1.csv",
    "evidence/meta_extraction/bottleneck_scale_robustness_v1.csv",
    "evidence/meta_extraction/scale_stable_quantity_function_proxy_failure_v1.csv",
    "evidence/meta_extraction/transition_filtering_topology_v1.csv",
    "evidence/meta_extraction/phase2_gpair_synthesis_v1.json",
    "evidence/meta_extraction/if_sign_geometry_census_v1.csv",
    "evidence/meta_extraction/if_sign_uncertainty_v1.csv",
    "evidence/meta_extraction/qualitative_external_if_audit_v1.csv",
    "evidence/meta_extraction/phase2_if_quantitative_gate_v1.csv",
    "evidence/meta_extraction/PS014_hulting_extraction_v1.csv",
    "evidence/meta_extraction/estimand_scale_cluster_summary_v2.csv",
    "evidence/meta_extraction/estimand_scale_fisher_sensitivity_v2.csv",
    "evidence/meta_extraction/exploratory_transition_filtering_v1.csv",
    "evidence/meta_extraction/ecological_if_programme_census_v1.csv",
    "evidence/meta_extraction/ecological_mating_function_programme_census_v1.csv",
    "evidence/meta_extraction/ecological_process_function_programme_census_v1.csv",
    "evidence/meta_extraction/phase2_cf01_sevenello_direct_covariance_v1.json",
    "evidence/meta_extraction/phase2_cf01_bergsdorf_kakamega_direct_covariance_v1.json",
    "evidence/meta_extraction/phase2_cf01_cardiopetalum_gradient_covariance_v1.json",
    "evidence/meta_extraction/phase2_cf01_zurich_gradient_covariance_v1.json",
    "evidence/meta_extraction/phase2_cf01_milkweed_urban_gradient_covariance_v1.json",
    "evidence/meta_extraction/phase2_cf01_pritchard_gradient_dependence_v1.json",
    "evidence/meta_extraction/multilayer_cluster_registry_v1.csv",
    "evidence/meta_extraction/multilayer_cluster_registry_extension_ml020.csv",
]

BANNED = [
    "zuizui0223",
    "zhang ruiqi",
    "zhang rachel",
    "rachelzhang0223",
    "github.com/zuizui0223",
    "@gmail.com",
    "egwee",
    "nee theory",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def scrub_text(text: str) -> str:
    text = text.replace("EGWEE_STATE_SEPARATION", "STATE_SEPARATION")
    text = text.replace("EGWEE_ML020", "ML020_RESULT")
    text = text.replace("EGWEE", "SYNTHESIS")
    text = text.replace("NEE theory", "eco-genetic theory")
    return text


def copy_scrubbed(rel: str) -> None:
    src = ROOT / rel
    if not src.is_file():
        raise AssertionError(f"missing review-package source: {rel}")
    dst = PKG / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in {".py", ".md", ".csv", ".txt", ".json"}:
        dst.write_text(scrub_text(src.read_text(encoding="utf-8")), encoding="utf-8")
    else:
        shutil.copy2(src, dst)


def write_readme() -> None:
    text = """# Anonymous review package\n\nThis package contains the analysis-ready tables and minimal code needed to reproduce the historical five-cluster Hedges-g synthesis, the mandatory Hedges-g versus lnRR estimand-scale audit, covariance sensitivity/certification, the exploratory process-function censuses, separate continuous-gradient evidence, the four main manuscript figures, the complete registered-cluster recovery flow, and all 17 admitted primary marginal effects. It intentionally excludes version-control history, author metadata and identity-bearing title-page material.\n\n## Reproduce the synthesis\n\n```bash\npython scripts/synthesize_state_separation.py\n```\n\nThe command prints a machine-readable `STATE_SEPARATION` record containing the primary five-cluster Fisher result and leave-one-cluster-out diagnostics.\n\n## Reproduce authoritative estimand-scale sensitivity

```bash
python scripts/check_estimand_scale_robustness.py
python scripts/check_bottleneck_scale_robustness.py
```

The first command reconstructs oriented lnRR from aligned independent units, including multivariate delta covariance, validates the Serapias rank reversal, compares full/omit-ML001 Fisher conclusions, and verifies 17/17 negative primary direct effects on both scales. The second checks which process–function geometries persist across scale representations. ML014 retrieves the same public TERN family table used by the source recovery; network access is therefore required for that one raw-unit reconstruction.

## Reproduce exploratory ecological leads

```bash
python scripts/check_scale_stable_quantity_function_proxy_failure.py
python scripts/check_transition_specific_filtering.py
```

These checks verify the three cross-context downstream proxy-failure programmes, the 8/8 quantity-only measurement gap, the cross-scale movement/mating point ordering, and the five-programme negative adult–offspring lag result. They are exploratory ecological synthesis checks, not confirmatory prevalence tests.

## Reproduce the frozen qualitative external I-F audit

```bash
python scripts/check_qualitative_external_if_audit.py
```

This checks all eight already-screened but quantitatively blocked I-F programmes in the frozen denominator. The source-reported geometries include buffering, resilience, concordant response and one qualitative hidden-function-loss programme. No detected effects are not recoded as zero/equality, and the category counts are not prevalence estimates.

The earlier `check_estimand_scale_sensitivity.py` carried-rho analysis is retained as provenance only and is not the authoritative lnRR covariance reconstruction.

## Reproduce the covariance sensitivity\n\n```bash\npython scripts/check_covariance_robustness.py\n```\n\nThis verifies the frozen paired-covariance result, the zero-covariance working sensitivity and the pairwise Cauchy–Schwarz covariance-free certification bound against Supplementary Table S2 and the manuscript.\n\n## Reproduce the process-function bottleneck census and I-F subset\n\n```bash\npython scripts/check_ecological_process_function_programme_census.py\npython scripts/check_ecological_if_programme_census.py\n```\n\nThis first verifies the complete 12-programme paired process-function registry: 11 pair-testable, four resolved mismatches (three downstream F-dominant and one upstream process-dominant), seven unresolved and one not-testable programme. The second verifies the eight-programme I-F subset and its measurement gap: all eight current I endpoints are quantity-only measures and none directly measures effective mating quality. Both censuses are descriptive and do not pool Hedges-g and Fisher-z effects.\n\n## Reproduce bottleneck-direction influence\n\n```bash\npython scripts/check_ecological_bottleneck_direction_influence.py\n```\n\nThis verifies that the two-direction resolved pattern is not leave-one-programme-out robust: omitting ML001 removes the only upstream resolved programme and leaves three downstream F-dominant resolved programmes.\n\n## Audit all 17 primary marginal effects\n\n```bash\npython scripts/check_primary_effect_supplement.py\npython scripts/build_primary_effect_forest.py\n```\n\nThe first command reconstructs Supplementary Table S3 from the source effect files and verifies each Hedges-g value, sampling variance, independent-unit count, standard error and marginal 95% confidence interval. The second generates Supplementary Figure S1, using an explicitly separate horizontal scale for the extreme ML001 Serapias effects so the other 14 effects remain legible. The dual scale is display-only and does not alter inference.\n\n## Reproduce the main figures and Tables 1–2\n\n```bash\npython scripts/build_journal_of_ecology_figures.py\n```\n\nOutputs are written under `manuscript/figures/` and `manuscript/tables/`. Supplementary Table S1 records all 16 formal cluster attempts and their terminal admission/closure status. Supplementary Table S2 records the three dependence regimes. Supplementary Table S3 records all 17 primary marginal effects. Supplementary Table S6 records the complete frozen qualitative blocked I-F denominator.\n\n## Scope\n\nThe package contains analysis-ready evidence rather than every raw source file from the original publications. Source studies and DOIs are documented in the anonymous manuscript and evidence tables.\n"""
    (PKG / "README_REVIEW_PACKAGE.md").write_text(text, encoding="utf-8")


def patch_anonymous_scripts() -> None:
    synthesis = PKG / "scripts/synthesize_state_separation.py"
    figures = PKG / "scripts/build_journal_of_ecology_figures.py"
    stext = synthesis.read_text(encoding="utf-8")
    ftext = figures.read_text(encoding="utf-8")
    if "EGWEE_STATE_SEPARATION" in stext or "EGWEE_STATE_SEPARATION" in ftext:
        raise AssertionError("internal synthesis prefix survived scrub")
    ftext = ftext.replace('x.startswith("EGWEE_STATE_SEPARATION ")', 'x.startswith("STATE_SEPARATION ")')
    figures.write_text(ftext, encoding="utf-8")


def audit_identity() -> None:
    for path in PKG.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".py", ".md", ".csv", ".txt", ".json"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace").casefold()
        for token in BANNED:
            if token.casefold() in text:
                raise AssertionError(f"identity/internal token {token!r} in {path.relative_to(PKG)}")


def verify_reproduction() -> None:
    proc = subprocess.run(
        [sys.executable, "scripts/synthesize_state_separation.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    line = next((x for x in proc.stdout.splitlines() if x.startswith("STATE_SEPARATION ")), None)
    if line is None:
        raise AssertionError(proc.stdout)
    if '"n_primary_independent_clusters": 5' not in line:
        raise AssertionError("anonymous package synthesis did not recover five primary clusters")

    scale_audit = subprocess.run(
        [sys.executable, "scripts/check_estimand_scale_robustness.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    if "ESTIMAND_SCALE_AUDIT " not in scale_audit.stdout:
        raise AssertionError(scale_audit.stdout)

    bottleneck_scale = subprocess.run(
        [sys.executable, "scripts/check_bottleneck_scale_robustness.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    if "BOTTLENECK_SCALE_AUDIT " not in bottleneck_scale.stdout:
        raise AssertionError(bottleneck_scale.stdout)

    cov = subprocess.run(
        [sys.executable, "scripts/check_covariance_robustness.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    if "COVARIANCE_ROBUSTNESS " not in cov.stdout:
        raise AssertionError(cov.stdout)

    process_function_census = subprocess.run(
        [sys.executable, "scripts/check_ecological_process_function_programme_census.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    if "ECOLOGICAL_PROCESS_FUNCTION_CENSUS_OK programmes=12 testable=11 resolved=4 unresolved=7 not_testable=1 resolved_downstream_F=3 resolved_upstream_process=1 quantity_I=8 movement_mating=4" not in process_function_census.stdout:
        raise AssertionError(process_function_census.stdout)

    bottleneck_influence = subprocess.run(
        [sys.executable, "scripts/check_ecological_bottleneck_direction_influence.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    if "ECOLOGICAL_BOTTLENECK_INFLUENCE_OK programmes=12 full_directions=2 direction_diversity_lost_only_if_drop=ML001 without_ML001_resolved=3 without_ML001_direction=downstream_F_only" not in bottleneck_influence.stdout:
        raise AssertionError(bottleneck_influence.stdout)

    sign_geometry = subprocess.run(
        [sys.executable, "scripts/check_if_sign_geometry.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    if "IF_SIGN_GEOMETRY_OK panels=18 programmes=8 discordant_panels=6 discordant_programmes=5 hidden_function_loss_programmes=2 buffered_or_gain_programmes=3 multi_panel_programmes=4 within_program_heterogeneous=3" not in sign_geometry.stdout:
        raise AssertionError(sign_geometry.stdout)

    sign_uncertainty = subprocess.run(
        [sys.executable, "scripts/check_if_sign_uncertainty.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    if "IF_SIGN_UNCERTAINTY_OK panels=18 point_opposite=6 programmes_point_opposite=5 both_resolved_opposite=0 one_resolved_opposite=2 both_unresolved_opposite=4" not in sign_uncertainty.stdout:
        raise AssertionError(sign_uncertainty.stdout)

    qualitative_external = subprocess.run(
        [sys.executable, "scripts/check_qualitative_external_if_audit.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    if "QUALITATIVE_EXTERNAL_IF_AUDIT_OK programmes=8 quantitative_blocked=8 qualitative_nonmonotonic=5 resilient_no_detected_loss=2 concordant_size_effect=1 hidden_function_loss=1 no_prevalence_inference=true" not in qualitative_external.stdout:
        raise AssertionError(qualitative_external.stdout)

    census = subprocess.run(
        [sys.executable, "scripts/check_ecological_if_programme_census.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    if "ECOLOGICAL_IF_CENSUS_OK programmes=8 pair_testable=7 resolved=3 unresolved=4 not_testable=1 resolved_F_more_negative=3 resolved_I_more_negative=0 quantity_only_I=8 effective_mating_I=0" not in census.stdout:
        raise AssertionError(census.stdout)

    primary = subprocess.run(
        [sys.executable, "scripts/check_primary_effect_supplement.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    if "PRIMARY_EFFECT_SUPPLEMENT_OK rows=17 clusters=5" not in primary.stdout:
        raise AssertionError(primary.stdout)

    forest = subprocess.run(
        [sys.executable, "scripts/build_primary_effect_forest.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    if "PRIMARY_EFFECT_FOREST_OK rows=17" not in forest.stdout:
        raise AssertionError(forest.stdout)

    subprocess.run(
        [sys.executable, "scripts/build_journal_of_ecology_figures.py"],
        cwd=PKG,
        check=True,
        capture_output=True,
        text=True,
    )
    for rel in (
        "manuscript/figures/figure1_primary_evidence_geometry.svg",
        "manuscript/figures/figure2_leave_one_out_influence.svg",
        "manuscript/figures/figure3_if_sign_geometry.svg",
        "manuscript/figures/figure4_estimand_scale_sensitivity.svg",
        "manuscript/figures/figure_s1_all_primary_marginal_effects.svg",
        "manuscript/tables/table1_primary_cluster_summary.csv",
        "manuscript/tables/table2_estimand_scale_sensitivity.csv",
        "manuscript/tables/table_s4_process_function_census.csv",
        "manuscript/tables/table_s5_if_sign_geometry.csv",
        "manuscript/tables/table_s6_qualitative_external_if_audit.csv",
        "manuscript/tables/table_s1_cluster_recovery_flow.csv",
        "manuscript/tables/table_s2_covariance_robustness.csv",
        "manuscript/tables/table_s3_primary_marginal_effects.csv",
    ):
        path = PKG / rel
        if not path.is_file() or path.stat().st_size == 0:
            raise AssertionError(f"missing reproduced/review output: {rel}")


def write_manifest() -> None:
    paths = sorted(p for p in PKG.rglob("*") if p.is_file())
    lines = ["sha256  path"]
    for path in paths:
        lines.append(f"{sha256(path)}  {path.relative_to(PKG).as_posix()}")
    (PKG / "MANIFEST_SHA256.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_zip() -> None:
    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(p for p in PKG.rglob("*") if p.is_file()):
            zf.write(path, path.relative_to(PKG))


def main() -> None:
    if PKG.exists():
        shutil.rmtree(PKG)
    PKG.mkdir(parents=True)
    for rel in FILES:
        copy_scrubbed(rel)
    write_readme()
    patch_anonymous_scripts()
    audit_identity()
    verify_reproduction()
    write_manifest()
    audit_identity()
    make_zip()
    if ZIP.stat().st_size < 1000:
        raise AssertionError("anonymous review zip unexpectedly small")
    print(f"ANONYMOUS_REVIEW_PACKAGE_OK files={sum(1 for p in PKG.rglob('*') if p.is_file())} zip_bytes={ZIP.stat().st_size}")


if __name__ == "__main__":
    main()
