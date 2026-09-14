from __future__ import annotations

import io
import re
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

PMCID = "PMC3489046"
SUPP_URL = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{PMCID}/supplementaryFiles"
EXPECTED = {
    "ele0015-0444-SD1.doc",
    "ele0015-0444-SD2.doc",
    "ele0015-0444-SD3.doc",
}
UA = "Mozilla/5.0 egwee-swietenia-macrophylla-ml016-schema/1.0"


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
    # Schema audit only: do not surface numeric outcome rows in this first gate.
    text = re.sub(r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?(?:[Ee][-+]?\d+)?", "<NUM>", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:360]


def extract_doc_text(path: Path) -> str:
    if shutil.which("antiword") is None:
        raise RuntimeError("antiword is required for legacy .doc schema inspection")
    proc = subprocess.run(
        ["antiword", str(path)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="replace",
    )
    return proc.stdout


def candidate_schema_lines(text: str) -> list[tuple[int, str]]:
    terms = (
        "family",
        "families",
        "population",
        "provenance",
        "isolated",
        "forest",
        "growth",
        "correlated paternity",
        "paternity",
        "r p",
        "rp",
        "outcross",
    )
    hits: list[tuple[int, str]] = []
    for i, raw in enumerate(text.splitlines(), start=1):
        line = re.sub(r"\s+", " ", raw).strip()
        low = line.lower()
        n = sum(term in low for term in terms)
        if n >= 2:
            hits.append((i, line))
    return hits


def family_pair_signature(text: str) -> dict[str, bool]:
    low = text.lower()
    return {
        "has_family": "family" in low or "families" in low,
        "has_growth": "growth" in low,
        "has_rp_or_correlated_paternity": (
            "correlated paternity" in low
            or bool(re.search(r"\br\s*[_ ]?p\b", low))
        ),
        "has_context": "isolated" in low and "forest" in low,
        "has_provenance": "provenance" in low,
    }


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
            for expected in sorted(EXPECTED):
                member = next(n for n in zf.namelist() if Path(n).name == expected)
                out = root / expected
                out.write_bytes(zf.read(member))
                text = extract_doc_text(out)
                sig = family_pair_signature(text)
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

    candidates = [
        name for name, sig in signatures.items()
        if sig["has_family"] and sig["has_growth"] and sig["has_rp_or_correlated_paternity"]
    ]
    print(f"MACROPHYLLA_FAMILY_PAIR_CANDIDATES files={candidates!r}")
    if candidates:
        print(
            "MACROPHYLLA_SCHEMA_GATE CANDIDATE_FAMILY_PAIR_REPRESENTATION_FOUND "
            "numeric_family_rows_remain_uncommitted_until_exact_mapping_is_frozen"
        )
    else:
        print(
            "MACROPHYLLA_SCHEMA_GATE NO_FAMILY_PAIRED_RP_GROWTH_TABLE_DETECTED "
            "do_not_backsolve_covariance_from_group_or_regression_summaries"
        )


if __name__ == "__main__":
    main()
