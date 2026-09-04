from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_ecological_indicators_submission as base  # noqa: E402

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def _find_text(root: ET.Element, value: str) -> ET.Element:
    for element in root.iter(f"{{{SVG_NS}}}text"):
        if "".join(element.itertext()) == value:
            return element
    raise RuntimeError(f"SVG text element not found: {value}")


def _fix_figure1(path: Path) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    label = _find_text(root, "study/origin/protocol confounded")
    label.set("x", "1225.0")
    label.set("text-anchor", "end")
    tree.write(path, encoding="unicode", xml_declaration=False)


def _fix_figure2(path: Path) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    machine_id = _find_text(root, "cross_origin_convergence_not_identifiable_from_existing_archives")
    machine_id.set("x", "235.0")
    machine_id.set("text-anchor", "start")
    tree.write(path, encoding="unicode", xml_declaration=False)


def finalize(out: Path) -> None:
    _fix_figure1(out / "figures/figure1_four_gate_workflow.svg")
    _fix_figure2(out / "figures/figure2_system_branch_map.svg")
    base.write_manifest(out)
    base.validate_bundle(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and visually finalize the Ecological Indicators submission bundle")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path(args.repo_root)
    out = Path(args.output)
    base.build(root, out)
    finalize(out)
    print("Ecological Indicators submission bundle built, visual-QA fixes applied, and manifest refreshed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
