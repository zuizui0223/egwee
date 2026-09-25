from __future__ import annotations

import csv
import io
import json
import urllib.request
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_figshare_manifest_v1.json"
OUT = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_schema_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF01_SEVENELLO_SCHEMA_2026-09-25.md"

UA = "egwee-sevenello-schema/1.1"
CSV_FILES = ("landscape_bees.csv", "local_seeds.csv", "landscape_seeds.csv")
README = "Readme Open Access Data Sevenello_et_al.docx"

STRUCTURAL_TOKENS = (
    "reserve", "remnant", "site", "transect", "species", "sp",
    "position", "edge", "core", "crop", "area", "size", "plot",
    "quadrat", "treatment", "year", "location", "habitat",
)
RESPONSE_TOKENS = (
    "bee", "seed", "fruit", "pollen", "visit", "rich", "abund",
    "divers", "viab", "flower", "repro",
)


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read()


def structural_header(name: str) -> bool:
    low = name.strip().casefold()
    if not low:
        return False
    return any(t in low for t in STRUCTURAL_TOKENS) and not any(
        t in low for t in RESPONSE_TOKENS
    )


def response_header(name: str) -> bool:
    low = name.strip().casefold()
    return any(t in low for t in RESPONSE_TOKENS)


def csv_schema(raw: bytes) -> dict:
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    headers = reader.fieldnames or []
    structural = [h for h in headers if structural_header(h)]
    responses = [h for h in headers if response_header(h)]

    values = {h: set() for h in structural}
    row_count = 0
    for row in reader:
        row_count += 1
        for h in structural:
            value = (row.get(h) or "").strip()
            if value:
                values[h].add(value)

    return {
        "rows": row_count,
        "columns": headers,
        "structural_columns": structural,
        "response_candidate_columns_header_only": responses,
        "structural_values": {h: sorted(v)[:200] for h, v in values.items()},
    }


def docx_paragraphs(raw: bytes) -> list[str]:
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    out = []
    for p in root.findall(".//w:p", ns):
        text = "".join(t.text or "" for t in p.findall(".//w:t", ns)).strip()
        if text:
            out.append(text)
    return out


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_name = {f["name"]: f for f in manifest["files"]}
    assert all(name in by_name for name in (*CSV_FILES, README))

    schemas = {}
    for name in CSV_FILES:
        raw = download(by_name[name]["download_url"])
        assert len(raw) == int(by_name[name]["size"])
        schemas[name] = csv_schema(raw)

    readme_raw = download(by_name[README]["download_url"])
    assert len(readme_raw) == int(by_name[README]["size"])
    paragraphs = docx_paragraphs(readme_raw)

    readme_structural = []
    for paragraph in paragraphs:
        low = paragraph.casefold()
        if any(t in low for t in (
            "remnant", "transect", "position", "edge", "core",
            "crop", "area", "site", "reserve"
        )):
            readme_structural.append(paragraph[:500])

    result = {
        "schema_version": 1,
        "candidate": "CFTQ0001",
        "programme_id": "P2_CF01_SEVENELLO_2026",
        "dataset_doi": manifest["dataset_doi"],
        "files": schemas,
        "readme_structural_dictionary_lines": readme_structural[:100],
        "effect_outcomes_opened": False,
        "numeric_effects_calculated": False,
        "next_gate": (
            "freeze one fragmentation estimand and common independent-unit frame from "
            "structural fields before inspecting bee/seed response values"
        ),
    }

    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# CFTQ0001 Sevenello schema gate — 2026-09-25",
        "",
        "This gate downloaded the public files but read only headers and structural/exposure cells.",
        "Bee, visitation, pollen and seed response values were not read or summarized.",
        "",
        "## CSV schemas",
        "",
    ]
    for name in CSV_FILES:
        schema = schemas[name]
        lines += [
            f"### {name}",
            "",
            f"- rows: **{schema['rows']}**",
            "- columns: " + ", ".join(schema["columns"]),
            "- structural columns: " + (", ".join(schema["structural_columns"]) or "none"),
            "- response-candidate headers only: "
            + (", ".join(schema["response_candidate_columns_header_only"]) or "none"),
            "",
        ]
        for key, vals in schema["structural_values"].items():
            lines.append(f"- {key} structural values: {', '.join(vals)}")
        lines.append("")

    lines += [
        "## Gate",
        "",
        "Before any response value is opened, use the schema to freeze:",
        "",
        "1. the primary fragmentation component (binary edge/core or a continuous remnant-size stream);",
        "2. remnant/reserve/transect nesting and the true independent unit;",
        "3. the species-panel rule and common-frame/missingness rule;",
        "4. one I endpoint and one F endpoint whose values will then be opened mechanically.",
        "",
    ]
    STATUS.write_text("\n".join(lines), encoding="utf-8")

    print(
        "PHASE2_CF01_SEVENELLO_SCHEMA_OK "
        + " ".join(f"{name}={schemas[name]['rows']}" for name in CSV_FILES)
        + " effects_opened=false"
    )


if __name__ == "__main__":
    main()
