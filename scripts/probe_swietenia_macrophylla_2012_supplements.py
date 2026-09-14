from __future__ import annotations

import io
import re
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

PMCID = "PMC3489046"
SUPP_URL = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/supplementaryFiles"
EXPECTED = {
    "ele0015-0444-SD1.doc",
    "ele0015-0444-SD2.doc",
    "ele0015-0444-SD3.doc",
}
UA = "Mozilla/5.0 egwee-swietenia-macrophylla-ml016-schema/1.2"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        payload = resp.read()
        print(
            "MACROPHYLLA_SUPP_RESPONSE "
            f"status={resp.status} type={resp.headers.get('content-type')!r} bytes={len(payload)}"
        )
        return payload


def redact_numbers(text: str) -> str:
    text = re.sub(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?", "<NUM>", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:700]


def antiword(path: Path, *args: str) -> str:
    if shutil.which("antiword") is None:
        raise RuntimeError("antiword is required for legacy .doc schema inspection")
    proc = subprocess.run(
        ["antiword", *args, str(path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="replace",
    )
    return proc.stdout


def candidate_schema_lines(text: str) -> list[tuple[int, str]]:
    terms = (
        "family", "families", "population", "provenance", "isolated", "forest",
        "growth", "correlated paternity", "paternity", "r p", "rp", "outcross",
    )
    hits: list[tuple[int, str]] = []
    for i, raw in enumerate(text.splitlines(), start=1):
        line = re.sub(r"\s+", " ", raw).strip()
        low = line.lower()
        if sum(term in low for term in terms) >= 2:
            hits.append((i, line))
    return hits


def signature(text: str) -> dict[str, bool]:
    low = text.lower()
    return {
        "has_family": "family" in low or "families" in low,
        "has_population": "population" in low,
        "has_growth": "growth" in low,
        "has_rp_or_correlated_paternity": (
            "correlated paternity" in low or bool(re.search(r"\br\s*[_ ]?p\b", low))
        ),
        "has_context": "isolated" in low and "forest" in low,
        "has_provenance": "provenance" in low,
    }


def docbook_rows(xml_text: str) -> list[list[str]]:
    # antiword -x db emits a DocBook document. Namespace handling varies by package,
    # so parse all row/entry tags by local-name.
    root = ET.fromstring(xml_text)
    rows: list[list[str]] = []
    for elem in root.iter():
        if elem.tag.split("}")[-1].lower() != "row":
            continue
        cells: list[str] = []
        for child in elem.iter():
            if child.tag.split("}")[-1].lower() == "entry":
                text = " ".join(t.strip() for t in child.itertext() if t.strip())
                cells.append(re.sub(r"\s+", " ", text).strip())
        if cells:
            rows.append(cells)
    return rows


def main() -> None:
    payload = fetch(SUPP_URL)
    if not zipfile.is_zipfile(io.BytesIO(payload)):
        raise RuntimeError("Europe PMC supplementaryFiles response is not a ZIP archive")

    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        names = [Path(n).name for n in zf.namelist() if not n.endswith("/")]
        print(f"MACROPHYLLA_SUPP_FILES names={sorted(names)!r}")
        missing = EXPECTED - set(names)
        if missing:
            raise AssertionError(f"missing expected supplements: {sorted(missing)}")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            signatures: dict[str, dict[str, bool]] = {}
            texts: dict[str, str] = {}
            paths: dict[str, Path] = {}
            for expected in sorted(EXPECTED):
                member = next(n for n in zf.namelist() if Path(n).name == expected)
                out = root / expected
                out.write_bytes(zf.read(member))
                paths[expected] = out
                text = antiword(out)
                texts[expected] = text
                sig = signature(text)
                signatures[expected] = sig
                hits = candidate_schema_lines(text)
                print(
                    "MACROPHYLLA_SUPP_SCHEMA "
                    f"file={expected!r} text_lines={len(text.splitlines())} "
                    f"signature={sig!r} candidate_schema_lines={len(hits)}"
                )
                for line_no, line in hits[:30]:
                    print(
                        "MACROPHYLLA_SCHEMA_LINE "
                        f"file={expected!r} line={line_no} text={redact_numbers(line)!r}"
                    )

            sd3 = texts["ele0015-0444-SD3.doc"]
            for line_no, raw in enumerate(sd3.splitlines(), start=1):
                line = re.sub(r"\s+", " ", raw).strip()
                if line:
                    print(
                        "MACROPHYLLA_SD3_REDACTED "
                        f"line={line_no} text={redact_numbers(line)!r}"
                    )

            # Preserve actual table cell boundaries. All numerical values remain redacted.
            try:
                db = antiword(paths["ele0015-0444-SD3.doc"], "-x", "db")
                rows = docbook_rows(db)
            except Exception as exc:
                print(f"MACROPHYLLA_DOCBOOK_ERROR type={type(exc).__name__!r} message={str(exc)!r}")
                rows = []
            print(f"MACROPHYLLA_SD3_DOCBOOK_ROWS n={len(rows)}")
            for i, cells in enumerate(rows, start=1):
                print(
                    "MACROPHYLLA_SD3_TABLE_ROW "
                    f"row={i} cells={[redact_numbers(c) for c in cells]!r}"
                )

    candidates = [
        name for name, sig in signatures.items()
        if sig["has_family"] and sig["has_growth"] and sig["has_rp_or_correlated_paternity"]
    ]
    print(f"MACROPHYLLA_PAIR_REPRESENTATION_CANDIDATES files={candidates!r}")
    print(
        "MACROPHYLLA_SCHEMA_GATE STRUCTURE_EXPOSED_NUMERIC_VALUES_REDACTED "
        "next_decision=family_or_population_common_frame_vs_dependence_block"
    )


if __name__ == "__main__":
    main()
