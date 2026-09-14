from __future__ import annotations

import csv
import re
import urllib.request

UA = "Mozilla/5.0 egwee-eucalyptus-socialis-ml014-schema/1.0"
BASE = "https://shared.tern.org.au/attachment/c5278af9-b0c9-4572-8eb4-9ce3058f1b2a/"
TARGETS = {
    "MECBreedfamily.csv": ["MECBreedfamily.csv", "MECBreedingfamily.csv"],
    "MECBreedprogeny.csv": ["MECBreedprogeny.csv", "MECBreedingprogeny.csv"],
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/csv,*/*"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = resp.read()
        if resp.status != 200 or not payload:
            raise RuntimeError(f"GET {url} -> {resp.status}, bytes={len(payload)}")
        head = payload[:200].lstrip().lower()
        if b"<html" in head or b"<!doctype html" in head:
            raise RuntimeError(f"GET {url} returned HTML, bytes={len(payload)}")
        return payload


def header_only(payload: bytes) -> tuple[list[str], int]:
    text = payload.decode("utf-8-sig")
    physical = [line for line in text.splitlines() if line.strip()]
    if not physical:
        raise RuntimeError("empty CSV")
    # Schema gate deliberately parses only the header record. Numeric outcome rows remain unopened.
    header = next(csv.reader([physical[0]]))
    return [c.strip() for c in header], max(0, len(physical) - 1)


def download_one(candidates: list[str]) -> tuple[str, bytes]:
    errors: list[str] = []
    for name in candidates:
        url = BASE + name
        try:
            return url, fetch(url)
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")
    raise RuntimeError("; ".join(errors))


def norm(header: list[str]) -> dict[str, str]:
    return {re.sub(r"[^a-z0-9]+", "", h.lower()): h for h in header}


def family_keys(n: dict[str, str]) -> list[str]:
    return [k for k in n if "family" in k or "mother" in k or k in {"id", "tree", "treeid", "fam", "familyid", "motherid"}]


def context_keys(n: dict[str, str]) -> list[str]:
    return [k for k in n if "group" in k or "landscape" in k or "context" in k or "site" in k or "density" in k]


def rp_keys(n: dict[str, str]) -> list[str]:
    return [k for k in n if k == "rp" or "correlatedpaternity" in k or ("paternity" in k and "cor" in k)]


def growth_keys(n: dict[str, str]) -> list[str]:
    return [k for k in n if "growth" in k or "height" in k]


def main() -> None:
    headers: dict[str, list[str]] = {}
    for canonical, candidates in TARGETS.items():
        url, payload = download_one(candidates)
        header, n_rows_physical = header_only(payload)
        headers[canonical] = header
        print(f"SOCIALIS_TERN_SCHEMA file={canonical!r} physical_data_lines={n_rows_physical} columns={header!r} download={url!r}")

    fam = norm(headers["MECBreedfamily.csv"])
    prog = norm(headers["MECBreedprogeny.csv"])
    fam_id = family_keys(fam)
    fam_context = context_keys(fam)
    fam_rp = rp_keys(fam)
    fam_growth = growth_keys(fam)
    prog_id = family_keys(prog)
    prog_growth = growth_keys(prog)
    print(f"SOCIALIS_FAMILY_SCHEMA_NORMALIZED keys={sorted(fam)!r}")
    print(f"SOCIALIS_PROGENY_SCHEMA_NORMALIZED keys={sorted(prog)!r}")
    print(
        "SOCIALIS_TERN_SCHEMA_GATE "
        f"family_id_keys={fam_id!r} context_keys={fam_context!r} rp_keys={fam_rp!r} "
        f"family_growth_keys={fam_growth!r} progeny_id_keys={prog_id!r} progeny_growth_keys={prog_growth!r}"
    )
    if not fam_id or not fam_context or not fam_rp:
        raise AssertionError("family table does not expose locked family/context/r_p structure")
    if not fam_growth and not (prog_id and prog_growth):
        raise AssertionError("growth is not recoverable either at family level or by family aggregation from progeny table")
    print("SOCIALIS_TERN_SCHEMA_GATE PASS numeric_outcome_rows_not_parsed")


if __name__ == "__main__":
    main()
