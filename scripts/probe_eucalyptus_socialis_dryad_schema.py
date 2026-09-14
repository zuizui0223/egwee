from __future__ import annotations

import csv
import json
import re
import urllib.parse
import urllib.request
from typing import Any

DOI = "10.5061/dryad.bs42p"
DATASET_API = "https://datadryad.org/api/v2/datasets/" + urllib.parse.quote("doi:" + DOI, safe="")
UA = "Mozilla/5.0 egwee-eucalyptus-socialis-ml014-schema/1.0"
TARGETS = {"MECBreedfamily.csv", "MECBreedprogeny.csv"}


def request_bytes(url: str) -> tuple[int, str, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.status, resp.headers.get("content-type", ""), resp.read()


def get_json(url: str) -> dict[str, Any]:
    status, ctype, payload = request_bytes(url)
    if status != 200:
        raise RuntimeError(f"GET {url} -> {status}")
    try:
        return json.loads(payload.decode("utf-8-sig"))
    except Exception as exc:
        raise RuntimeError(f"expected JSON from {url}; type={ctype!r} bytes={len(payload)}") from exc


def absolute(href: str) -> str:
    return urllib.parse.urljoin("https://datadryad.org", href)


def iter_links(obj: Any):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "href" and isinstance(value, str):
                yield value
            yield from iter_links(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from iter_links(value)


def embedded_items(obj: dict[str, Any], token: str) -> list[dict[str, Any]]:
    emb = obj.get("_embedded", {})
    if not isinstance(emb, dict):
        return []
    for key, value in emb.items():
        if token.lower() in key.lower() and isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
    return []


def resolve_version(dataset: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    hrefs = list(iter_links(dataset))
    current = [h for h in hrefs if re.search(r"/api/v2/versions/\d+/?$", h)]
    if current:
        url = absolute(current[0])
        return url, get_json(url)
    version_collections = [h for h in hrefs if "/api/v2/datasets/" in h and "/versions" in h]
    if not version_collections:
        raise RuntimeError(f"Dryad dataset metadata has no version relation; links={hrefs}")
    collection = get_json(absolute(version_collections[0]))
    versions = embedded_items(collection, "version")
    if not versions:
        raise RuntimeError("Dryad versions collection is empty")
    versions.sort(key=lambda x: int(x.get("versionNumber", x.get("id", 0)) or 0))
    chosen = versions[-1]
    links = list(iter_links(chosen))
    exact = [h for h in links if re.search(r"/api/v2/versions/\d+/?$", h)]
    if exact:
        url = absolute(exact[0])
        return url, get_json(url)
    vid = chosen.get("id")
    if vid is None:
        raise RuntimeError("cannot resolve Dryad version id")
    url = f"https://datadryad.org/api/v2/versions/{vid}"
    return url, get_json(url)


def resolve_files(version_url: str, version: dict[str, Any]) -> list[dict[str, Any]]:
    hrefs = list(iter_links(version))
    file_links = [h for h in hrefs if "/files" in h]
    listing = get_json(absolute(file_links[0])) if file_links else get_json(version_url.rstrip("/") + "/files")
    files = embedded_items(listing, "file")
    if files:
        return files
    for value in listing.values():
        if isinstance(value, list) and value and all(isinstance(x, dict) for x in value):
            return value
    raise RuntimeError(f"could not identify files in Dryad response keys={list(listing)}")


def file_name(item: dict[str, Any]) -> str:
    for key in ("path", "name", "filename"):
        value = item.get(key)
        if isinstance(value, str) and value:
            return value.rsplit("/", 1)[-1]
    return ""


def candidate_download_urls(item: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for href in iter_links(item):
        low = href.lower()
        if "download" in low or "file_stream" in low:
            out.append(absolute(href))
    fid = item.get("id")
    if fid is not None:
        out.extend([
            f"https://datadryad.org/stash/downloads/file_stream/{fid}",
            f"https://datadryad.org/downloads/file_stream/{fid}",
            f"https://datadryad.org/api/v2/files/{fid}/download",
        ])
    return list(dict.fromkeys(out))


def download_file(item: dict[str, Any]) -> tuple[str, bytes]:
    errors: list[str] = []
    for url in candidate_download_urls(item):
        try:
            status, ctype, payload = request_bytes(url)
            if status == 200 and payload:
                head = payload[:200].lstrip().lower()
                if b"<html" in head or b"<!doctype html" in head:
                    errors.append(f"{url}: html type={ctype!r} bytes={len(payload)}")
                    continue
                return url, payload
            errors.append(f"{url}: status={status} type={ctype!r} bytes={len(payload)}")
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")
    raise RuntimeError("; ".join(errors))


def header_only(payload: bytes) -> tuple[list[str], int]:
    text = payload.decode("utf-8-sig")
    physical = [line for line in text.splitlines() if line.strip()]
    if not physical:
        raise RuntimeError("empty CSV")
    header = next(csv.reader([physical[0]]))
    return [c.strip() for c in header], max(0, len(physical) - 1)


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
    dataset = get_json(DATASET_API)
    print("SOCIALIS_DRYAD_DATASET " f"doi={DOI!r} id={dataset.get('id')!r} title={dataset.get('title')!r}")
    version_url, version = resolve_version(dataset)
    print("SOCIALIS_DRYAD_VERSION " f"url={version_url!r} id={version.get('id')!r} version={version.get('versionNumber')!r}")
    files = resolve_files(version_url, version)
    by_name = {file_name(f): f for f in files}
    print(f"SOCIALIS_DRYAD_FILES names={sorted(by_name)!r}")
    missing = TARGETS - set(by_name)
    if missing:
        raise AssertionError(f"missing expected Dryad files: {sorted(missing)}")

    headers: dict[str, list[str]] = {}
    for name in sorted(TARGETS):
        item = by_name[name]
        print("SOCIALIS_DRYAD_FILE " f"name={name!r} id={item.get('id')!r} size={item.get('size')!r}")
        url, payload = download_file(item)
        header, n_lines = header_only(payload)
        headers[name] = header
        print("SOCIALIS_SCHEMA " f"file={name!r} physical_data_lines={n_lines} columns={header!r} download={url!r}")

    fam = norm(headers["MECBreedfamily.csv"])
    prog = norm(headers["MECBreedprogeny.csv"])
    fam_id, fam_context, fam_rp = family_keys(fam), context_keys(fam), rp_keys(fam)
    fam_growth, prog_id, prog_growth = growth_keys(fam), family_keys(prog), growth_keys(prog)
    print(f"SOCIALIS_FAMILY_SCHEMA_NORMALIZED keys={sorted(fam)!r}")
    print(f"SOCIALIS_PROGENY_SCHEMA_NORMALIZED keys={sorted(prog)!r}")
    print(
        "SOCIALIS_SCHEMA_GATE "
        f"family_id_keys={fam_id!r} context_keys={fam_context!r} rp_keys={fam_rp!r} "
        f"family_growth_keys={fam_growth!r} progeny_id_keys={prog_id!r} progeny_growth_keys={prog_growth!r}"
    )
    if not fam_id or not fam_context or not fam_rp:
        raise AssertionError("family table does not expose locked family/context/r_p structure")
    if not fam_growth and not (prog_id and prog_growth):
        raise AssertionError("growth is not recoverable either at family level or by family aggregation from progeny table")
    print("SOCIALIS_SCHEMA_GATE PASS numeric_outcome_rows_not_parsed")


if __name__ == "__main__":
    main()
