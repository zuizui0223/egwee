from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

TITLE = "Test the state before interpreting the residual: four empirical gates for ecological state indicators"
EXPECTED_SYSTEMS = [
    "Honshu-Izu",
    "Zurich BetterBlooms",
    "Toronto community gardens",
    "Oenothera harringtonii",
    "Eschscholzia californica",
    "Mallorca carob",
    "Campanula americana",
]
EXPECTED_GATES = [
    "measurement_adequacy",
    "representation_preservation",
    "residual_context",
    "cross_study_identifiability",
]
FORBIDDEN_DOWNSTREAM_TOKENS = (
    "0.2543",
    "+5.33",
    "+5.20",
    "35/35",
    "48/48",
    "33/33",
    "49/49",
)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text(x: float, y: float, value: str, *, size: int = 14, anchor: str = "middle", weight: str = "normal") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-family="sans-serif" font-size="{size}" font-weight="{weight}">{html.escape(value)}</text>'
    )


def validate_sources(root: Path) -> tuple[dict, dict, dict]:
    registry = _load_json(root / "manuscript/natural_data_gate_registry.json")
    six = _load_json(root / "manuscript/unreachable_six_systems.json")
    spec = _load_json(root / "manuscript/natural_data_figure_spec.json")

    if registry.get("schema_version") != 1:
        raise RuntimeError("gate registry schema drifted")
    if registry.get("shared_order") != EXPECTED_GATES:
        raise RuntimeError("four-gate order drifted")
    systems = registry.get("systems", [])
    if [row.get("system") for row in systems] != EXPECTED_SYSTEMS:
        raise RuntimeError("seven-system registry membership/order drifted")
    if {row.get("line") for row in systems} != {1, 2, 3, 4}:
        raise RuntimeError("four empirical branches are not all represented")
    if registry["cross_study"]["locked_outcome"] != "cross_origin_convergence_not_identifiable_from_existing_archives":
        raise RuntimeError("cross-study STOP drifted")

    six_rows = six.get("systems", [])
    if len(six_rows) != 6:
        raise RuntimeError("downstream-inference table must contain six system rows")
    if six["excluded_positive_system"]["system"] != "Oenothera harringtonii":
        raise RuntimeError("positive missing-coordinate system drifted")
    if {row["system"] for row in six_rows} != set(EXPECTED_SYSTEMS) - {"Oenothera harringtonii"}:
        raise RuntimeError("six-system inference-boundary membership drifted")

    if spec.get("source_registry") != "manuscript/natural_data_gate_registry.json":
        raise RuntimeError("figure spec no longer points to gate registry")
    if spec["figure_2"]["order"] != EXPECTED_SYSTEMS:
        raise RuntimeError("figure-2 system order drifted")
    return registry, six, spec


def materialize_manuscript(root: Path) -> str:
    source = (root / "manuscript/natural_data_ecological_indicators_spine.md").read_text(encoding="utf-8")
    if not source.startswith(f"# {TITLE}\n"):
        raise RuntimeError("source manuscript title drifted")

    # Repository-only status/core material is deliberately excluded from the journal manuscript.
    abstract_marker = "## Provisional abstract"
    if abstract_marker not in source:
        raise RuntimeError("source abstract marker missing")
    journal = f"# {TITLE}\n\n" + source.split(abstract_marker, 1)[1]
    journal = "## Abstract" + journal[len(f"# {TITLE}\n\n"):]
    # The previous line reconstructs from the abstract body; restore the title explicitly.
    journal = f"# {TITLE}\n\n" + journal

    old_known = (
        "Environmental and ecological indicator validation is not new. Existing frameworks distinguish design, output and end-use validation; "
        "ecological indicator suites are evaluated for relevance, robustness, redundancy and interpretability; predictive validation with held-out data is established; "
        "and analytical uncertainty is a recognised component of indicator reliability. Variable standardisation is also a standard statistical tool."
    )
    new_known = (
        "Environmental and ecological indicator validation is not new. Established work separates design, output and end-use validation (Bockstaller & Girardin, 2003), "
        "shows why ecological indices themselves require validation (Moriarty et al., 2018), and provides rigorous criteria for selecting and evaluating indicator suites (Bundy et al., 2019). "
        "Recent work also emphasises uncertainty partitioning and practical proxy adequacy (Carstensen et al., 2024; Pacé et al., 2024). Predictor standardisation is likewise a standard statistical tool rather than a methodological novelty (Schielzeth, 2010)."
    )
    if old_known not in journal:
        raise RuntimeError("indicator-literature insertion point drifted")
    journal = journal.replace(old_known, new_known, 1)

    data_sources = (
        "### 2.2 Data sources and frozen analysis records\n\n"
        "The seven analyses reuse public natural-system datasets under frozen, system-specific analysis contracts. Honshu–Izu uses Hiraiwa & Ushimaru (2024; Figshare `10.6084/m9.figshare.25025000.v1`); Zurich uses Reji Chacko, Moretti & Frey (2025; EnviDat `10.16904/envidat.676`); Toronto uses Sookhan, MacIvor & Onuferko (2025; Dryad `10.5061/dryad.b8gtht7r4`); and *Oenothera harringtonii* uses Rhodes, Fant & Skogen (2017; Dryad `10.5061/dryad.p24q3`). The *Eschscholzia californica* branch uses four 2017 NERC Environmental Information Data Centre products (`10.5285/01906784-6742-44bf-b244-a4b63bed8d82`, `10.5285/8caf2d8a-564d-4f2e-a797-174165a83796`, `10.5285/5b400b69-b828-45e8-b04e-7ccbfdb0987f`, `10.5285/7b721c07-bc38-4815-8669-4675867663d0`). Mallorca carob uses the Gómez-Martínez et al. (2025) Zenodo archive (`10.5281/zenodo.13939480`), and *Campanula americana* uses Koski et al. (2018; Dryad `10.5061/dryad.5nj81nf`).\n\n"
        "The project-computed results reported here are not refits selected for this synthesis. Their preregistration, source-lock, endpoint, holdout unit, stop rule, result and claim ceiling are preserved under `evidence/` and routed through `manuscript/natural_data_gate_registry.json`. Third-party raw data are not redistributed by the submission bundle.\n\n"
    )
    marker = "### 2.2 Holdout discipline"
    if marker not in journal:
        raise RuntimeError("methods data-source insertion point drifted")
    journal = journal.replace(marker, data_sources + "### 2.3 Holdout discipline", 1)
    journal = journal.replace("### 2.3 No pooled ecological effect", "### 2.4 No pooled ecological effect", 1)
    journal = journal.replace("### 2.4 Fail-closed outcomes", "### 2.5 Fail-closed outcomes", 1)

    # Repository planning sections are not part of the journal manuscript.
    if "## Figure and table plan" not in journal:
        raise RuntimeError("journal cut point missing")
    journal = journal.split("## Figure and table plan", 1)[0].rstrip() + "\n"

    references = (root / "manuscript/references.md").read_text(encoding="utf-8")
    if not references.startswith("# References"):
        raise RuntimeError("references title drifted")
    references = references.split("\n", 1)[1]
    if "## Citation boundary" in references:
        references = references.split("## Citation boundary", 1)[0]
    references = re.sub(r"^## .+$", "", references, flags=re.MULTILINE)
    journal += "\n## References\n" + references.strip() + "\n"

    for token in FORBIDDEN_DOWNSTREAM_TOKENS:
        if token in journal:
            raise RuntimeError(f"downstream EGC/EGWE headline leaked into natural-data manuscript: {token}")
    for required in (
        "Bockstaller & Girardin, 2003",
        "Moriarty et al., 2018",
        "Bundy et al., 2019",
        "Schielzeth, 2010",
        "10.6084/m9.figshare.25025000.v1",
        "10.16904/envidat.676",
        "10.5061/dryad.b8gtht7r4",
        "10.1111/mec.14115",
        "10.5281/zenodo.13939480",
        "10.5061/dryad.5nj81nf",
    ):
        if required not in journal:
            raise RuntimeError(f"submission manuscript missing required citation/source: {required}")
    return journal


def write_gate_figure(registry: dict, spec: dict, output: Path) -> None:
    width, height = 1400, 720
    x = [120, 390, 670, 960, 1240]
    labels = [
        "Candidate ecological state / proxy",
        "Gate 1: measurement adequacy",
        "Gate 2: representation preservation",
        "Gate 3: residual context",
        "Gate 4: cross-study identifiability",
    ]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Test the state before interpreting the residual</title>',
        '<desc id="desc">An ordered four-gate workflow requires endpoint-relevant measurement adequacy, information-preserving representation, residual-context testing, and cross-study identifiability. Failed upstream gates stop downstream interpretation.</desc>',
        '<rect width="100%" height="100%" fill="white"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L0,10 L9,5 z" fill="#111"/></marker></defs>',
        _text(700, 48, spec["figure_1"]["title"], size=30, weight="bold"),
        _text(700, 80, "A gate authorises what may be interpreted next; it is not a severity score", size=16),
    ]
    y = 230
    widths = [205, 220, 235, 220, 235]
    for xx, label, ww in zip(x, labels, widths):
        lines.append(f'<rect x="{xx-ww/2:.1f}" y="{y-62}" width="{ww}" height="124" rx="12" fill="white" stroke="#111" stroke-width="2"/>')
        words = label.split()
        # deterministic two/three-line wrapping by length
        if len(label) < 28:
            lines.append(_text(xx, y+5, label, size=16, weight="bold"))
        else:
            split = max(1, len(words)//2)
            first = " ".join(words[:split])
            second = " ".join(words[split:])
            lines.append(_text(xx, y-8, first, size=14, weight="bold"))
            lines.append(_text(xx, y+18, second, size=14, weight="bold"))
    for left, right in zip(x[:-1], x[1:]):
        lines.append(f'<line x1="{left+120}" y1="{y}" x2="{right-125}" y2="{y}" stroke="#111" stroke-width="2" marker-end="url(#arrow)"/>')

    outcomes = [
        (390, 455, "not earned / not estimable", "STOP: do not interpret residual context"),
        (670, 545, "mechanistic distinction erased", "STOP: richer state not analytically supplied"),
        (960, 455, "no transferable gain", "conditional residual non-gain"),
        (1240, 545, "study/origin/protocol confounded", "not_identifiable / STOP"),
    ]
    for xx, yy, edge, box in outcomes:
        lines.append(f'<line x1="{xx}" y1="{y+62}" x2="{xx}" y2="{yy-38}" stroke="#555" stroke-width="1.8" marker-end="url(#arrow)"/>')
        lines.append(_text(xx+8, (y+62+yy-38)/2, edge, size=11, anchor="start"))
        lines.append(f'<rect x="{xx-150}" y="{yy-38}" width="300" height="76" rx="10" fill="white" stroke="#777" stroke-width="1.5"/>')
        lines.append(_text(xx, yy+5, box, size=13, weight="bold"))

    lines.extend([
        _text(700, 655, "Positive diagnosis can also stop the sequence: a missing response-relevant coordinate may be detected upstream.", size=15),
        '</svg>',
    ])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_branch_map(registry: dict, output: Path) -> None:
    systems = registry["systems"]
    width, height = 1500, 910
    left = 360
    gate_x = {
        "measurement_adequacy": 520,
        "representation_preservation": 740,
        "residual_context": 960,
        "cross_study_identifiability": 1180,
    }
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Locked natural-data outcomes on the four-gate workflow</title>',
        '<desc id="desc">Seven natural systems occupy different branches of the four-gate workflow. Positions show the furthest gate reached, while text states the locked outcome. There is no pooled effect-size axis or severity ranking.</desc>',
        '<rect width="100%" height="100%" fill="white"/>',
        _text(750, 42, "Seven locked analyses stop or diagnose at different inferential gates", size=27, weight="bold"),
        _text(750, 72, "Horizontal position is workflow order, not effect magnitude", size=15),
    ]
    for gate, xx in gate_x.items():
        label = gate.replace("_", " ")
        lines.append(_text(xx, 115, label, size=13, weight="bold"))
        lines.append(f'<line x1="{xx}" y1="135" x2="{xx}" y2="800" stroke="#ddd" stroke-width="1"/>')

    y0, dy = 185, 86
    outcome_short = {
        "no_detected_transferable_distance_gain": "no detected distance gain",
        "no_reproducible_positive_residual_context_gain": "no reproducible residual-context gain",
        "no_detected_residual_urban_context_information": "no detected urban-context gain",
        "missing_contemporary_process_coordinate_detected": "missing mating coordinate detected",
        "multi_endpoint_not_identifiable": "primary endpoint/proxy not identifiable",
        "process_measurement_adequacy_not_earned": "proxy adequacy not earned",
        "mechanistic_information_erased_by_preprocessing": "mechanistic distinction erased",
    }
    for i, row in enumerate(systems):
        yy = y0 + i*dy
        lines.append(_text(30, yy+4, row["system"], size=14, anchor="start", weight="bold"))
        for gate in EXPECTED_GATES:
            xx = gate_x[gate]
            lines.append(f'<circle cx="{xx}" cy="{yy}" r="5" fill="white" stroke="#aaa" stroke-width="1.5"/>')
        reached = row["gate_reached"]
        xx = gate_x[reached]
        # shape encodes branch type without implying ordinal severity
        if row["locked_outcome"] == "missing_contemporary_process_coordinate_detected":
            lines.append(f'<rect x="{xx-8}" y="{yy-8}" width="16" height="16" fill="#111"/>')
        else:
            lines.append(f'<circle cx="{xx}" cy="{yy}" r="8" fill="#111"/>')
        lines.append(_text(1225, yy+4, outcome_short[row["locked_outcome"]], size=12, anchor="start"))
        if i < len(systems)-1:
            lines.append(f'<line x1="25" y1="{yy+43}" x2="1475" y2="{yy+43}" stroke="#eee" stroke-width="1"/>')

    lines.extend([
        _text(30, 820, "Synthesis-level boundary:", size=13, anchor="start", weight="bold"),
        _text(190, 820, registry["cross_study"]["locked_outcome"], size=12, anchor="start"),
        _text(30, 855, "This is a design STOP, not an ecological null; systems are not pooled onto a common effect-size axis.", size=13, anchor="start"),
        '</svg>',
    ])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_graphical_abstract(output: Path) -> None:
    width, height = 1200, 560
    labels = ["Measure the state", "Preserve the information", "Test residual context", "Check identifiability"]
    x = [150, 450, 750, 1050]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Test the state before interpreting the residual</title>',
        '<desc id="desc">A four-step fail-closed sequence checks ecological state measurement, analytical representation, residual context, and cross-study identifiability before stronger biological interpretation.</desc>',
        '<rect width="100%" height="100%" fill="white"/>',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L0,10 L9,5 z" fill="#111"/></marker></defs>',
        _text(600, 55, "Test the state before interpreting the residual", size=31, weight="bold"),
        _text(600, 92, "Four empirical gates determine what inference is licensed next", size=17),
    ]
    y = 260
    for xx, label in zip(x, labels):
        lines.append(f'<rect x="{xx-112}" y="{y-58}" width="224" height="116" rx="14" fill="white" stroke="#111" stroke-width="2"/>')
        parts = label.split(" ", 2)
        if len(parts) == 3:
            lines.append(_text(xx, y-8, " ".join(parts[:2]), size=15, weight="bold"))
            lines.append(_text(xx, y+18, parts[2], size=15, weight="bold"))
        else:
            lines.append(_text(xx, y+5, label, size=15, weight="bold"))
    for a, b in zip(x[:-1], x[1:]):
        lines.append(f'<line x1="{a+112}" y1="{y}" x2="{b-118}" y2="{y}" stroke="#111" stroke-width="2" marker-end="url(#arrow)"/>')
    lines.extend([
        _text(600, 410, "Seven locked natural-data analyses occupy distinct branches; no common ecological effect is pooled.", size=15),
        _text(600, 452, "STOP, failed adequacy, missing coordinates and representation collapse are retained as results.", size=15, weight="bold"),
        '</svg>',
    ])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_table1(six: dict, csv_path: Path, md_path: Path) -> None:
    rows = six["systems"]
    fields = [
        "system",
        "gate_reached",
        "locked_outcome",
        "numeric_certificate",
        "unreachable_stronger_inference",
        "blocking_reason",
        "boundary_class",
    ]
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in fields})

    lines = [
        "# Table 1. Downstream inferences not licensed by the frozen evidence",
        "",
        "| System | Furthest gate | Locked certificate | Stronger inference not licensed |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['system']} | {row['gate_reached']} / {row['locked_outcome']} | "
            f"{row['numeric_certificate']} | {row['unreachable_stronger_inference']} |"
        )
    lines += [
        "",
        "*Oenothera harringtonii* is excluded because it positively identifies a missing contemporary coordinate. "
        "The cross-origin STOP is a synthesis-level identifiability boundary, not a seventh system row.",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _copy_text_tree(source: Path, destination: Path) -> None:
    for path in sorted(source.rglob("*.md")):
        target = destination / path.relative_to(source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def validate_highlights(path: Path) -> None:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not 3 <= len(lines) <= 5:
        raise RuntimeError(f"Highlights must contain 3–5 items, found {len(lines)}")
    too_long = [(line, len(line)) for line in lines if len(line) > 85]
    if too_long:
        raise RuntimeError(f"Highlights exceed 85 characters: {too_long}")


def write_manifest(out: Path) -> None:
    rows = []
    for path in sorted(p for p in out.rglob("*") if p.is_file() and p.name != "MANIFEST.sha256"):
        rows.append(f"{_sha256(path)}  {path.relative_to(out).as_posix()}")
    (out / "MANIFEST.sha256").write_text("\n".join(rows) + "\n", encoding="utf-8")


def validate_bundle(out: Path) -> None:
    required = [
        "manuscript/main_text.md",
        "manuscript/references.md",
        "manuscript/cover_letter.md",
        "manuscript/highlights.txt",
        "manuscript/submission_metadata.md",
        "figures/figure1_four_gate_workflow.svg",
        "figures/figure2_system_branch_map.svg",
        "figures/graphical_abstract.svg",
        "tables/table1_downstream_inference_boundaries.csv",
        "tables/table1_downstream_inference_boundaries.md",
        "provenance/natural_data_gate_registry.json",
        "provenance/unreachable_six_systems.json",
        "provenance/natural_data_figure_spec.json",
        "MANIFEST.sha256",
    ]
    missing = [path for path in required if not (out / path).is_file()]
    if missing:
        raise RuntimeError("submission bundle missing files: " + ", ".join(missing))
    manuscript = (out / "manuscript/main_text.md").read_text(encoding="utf-8")
    if not manuscript.startswith(f"# {TITLE}\n"):
        raise RuntimeError("materialized manuscript title drifted")
    if "## Provisional abstract" in manuscript or "## Figure and table plan" in manuscript:
        raise RuntimeError("repository planning prose leaked into submission manuscript")
    if "## Abstract" not in manuscript or "## References" not in manuscript:
        raise RuntimeError("journal manuscript is incomplete")
    for token in FORBIDDEN_DOWNSTREAM_TOKENS:
        if token in manuscript:
            raise RuntimeError(f"downstream series result leaked into EGWEE submission: {token}")
    validate_highlights(out / "manuscript/highlights.txt")


def build(root: Path, out: Path) -> None:
    registry, six, spec = validate_sources(root)
    validate_highlights(root / "manuscript/highlights.txt")
    if out.exists():
        shutil.rmtree(out)
    (out / "manuscript").mkdir(parents=True)
    (out / "figures").mkdir(parents=True)
    (out / "tables").mkdir(parents=True)
    (out / "provenance").mkdir(parents=True)

    manuscript = materialize_manuscript(root)
    (out / "manuscript/main_text.md").write_text(manuscript, encoding="utf-8")
    for source, dest in (
        ("manuscript/references.md", "manuscript/references.md"),
        ("manuscript/cover_letter_ecological_indicators.md", "manuscript/cover_letter.md"),
        ("manuscript/highlights.txt", "manuscript/highlights.txt"),
        ("manuscript/submission_metadata.md", "manuscript/submission_metadata.md"),
        ("manuscript/NATURAL_DATA_PUBLICATION_AUDIT_2026-09-01.md", "provenance/NATURAL_DATA_PUBLICATION_AUDIT_2026-09-01.md"),
        ("manuscript/NATURAL_DATA_VENUE_AUDIT_2026-09-01.md", "provenance/NATURAL_DATA_VENUE_AUDIT_2026-09-01.md"),
        ("manuscript/NATURAL_DATA_NEAREST_NEIGHBOR_AUDIT_2026-09-01.md", "provenance/NATURAL_DATA_NEAREST_NEIGHBOR_AUDIT_2026-09-01.md"),
        ("manuscript/natural_data_gate_registry.json", "provenance/natural_data_gate_registry.json"),
        ("manuscript/unreachable_six_systems.json", "provenance/unreachable_six_systems.json"),
        ("manuscript/natural_data_figure_spec.json", "provenance/natural_data_figure_spec.json"),
    ):
        target = out / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / source, target)

    write_gate_figure(registry, spec, out / "figures/figure1_four_gate_workflow.svg")
    write_branch_map(registry, out / "figures/figure2_system_branch_map.svg")
    write_graphical_abstract(out / "figures/graphical_abstract.svg")
    write_table1(
        six,
        out / "tables/table1_downstream_inference_boundaries.csv",
        out / "tables/table1_downstream_inference_boundaries.md",
    )
    _copy_text_tree(root / "evidence", out / "provenance/evidence")
    write_manifest(out)
    validate_bundle(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the standalone Ecological Indicators submission bundle")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    build(Path(args.repo_root), Path(args.output))
    print("Ecological Indicators submission bundle built and validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
