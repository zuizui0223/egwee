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
    "scripts/synthesize_state_separation.py",
    "scripts/build_journal_of_ecology_figures.py",
    "evidence/meta_extraction/PS003_serapias_binary_effects_v1.csv",
    "evidence/meta_extraction/PS003_serapias_primary_covariance_v1.csv",
    "evidence/meta_extraction/PS004_brosimum_extraction_v1.csv",
    "evidence/meta_extraction/PS004_brosimum_primary_covariance_v1.csv",
    "evidence/meta_extraction/PS001_spondias_site_effects_v1.csv",
    "evidence/meta_extraction/PS001_spondias_primary_pairwise_covariance_v2.csv",
    "evidence/meta_extraction/PS020_eucalyptus_socialis_effects_v1.csv",
    "evidence/meta_extraction/PS020_eucalyptus_socialis_primary_covariance_v1.csv",
    "evidence/meta_extraction/PS022_aizen_feinsinger_effects_v1.csv",
    "evidence/meta_extraction/PS022_aizen_feinsinger_covariance_v1.csv",
    "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_effects_v1.csv",
    "evidence/meta_extraction/PS019_eucalyptus_wandoo_2018_gradient_covariance_v1.csv",
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
    # Remove internal project labels from reviewer-facing executable output while
    # preserving all numerical and methodological semantics.
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
    text = """# Anonymous review package\n\nThis package contains the analysis-ready tables and minimal code needed to reproduce the five-cluster direct state-separation synthesis, the separate continuous-gradient generalisation, and the three main submission figures. It intentionally excludes version-control history, author metadata and identity-bearing title-page material.\n\n## Reproduce the synthesis\n\n```bash\npython scripts/synthesize_state_separation.py\n```\n\nThe command prints a machine-readable `STATE_SEPARATION` record containing the primary five-cluster Fisher result and leave-one-cluster-out diagnostics.\n\n## Reproduce the figures and Table 1\n\n```bash\npython scripts/build_journal_of_ecology_figures.py\n```\n\nOutputs are written under `manuscript/figures/` and `manuscript/tables/`.\n\n## Scope\n\nThe package contains analysis-ready evidence rather than every raw source file from the original publications. Source studies and DOIs are documented in the anonymous manuscript and evidence tables.\n"""
    (PKG / "README_REVIEW_PACKAGE.md").write_text(text, encoding="utf-8")


def patch_anonymous_scripts() -> None:
    synthesis = PKG / "scripts/synthesize_state_separation.py"
    figures = PKG / "scripts/build_journal_of_ecology_figures.py"
    stext = synthesis.read_text(encoding="utf-8")
    ftext = figures.read_text(encoding="utf-8")
    if "EGWEE_STATE_SEPARATION" in stext or "EGWEE_STATE_SEPARATION" in ftext:
        raise AssertionError("internal synthesis prefix survived scrub")
    # The figure builder in the source repository parses the internal output
    # prefix; convert that parser to the anonymous prefix too.
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
        "manuscript/figures/figure3_ml020_concordant_decline.svg",
        "manuscript/tables/table1_primary_cluster_summary.csv",
    ):
        path = PKG / rel
        if not path.is_file() or path.stat().st_size == 0:
            raise AssertionError(f"missing reproduced output: {rel}")


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
