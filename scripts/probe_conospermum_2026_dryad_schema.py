from __future__ import annotations

import json
import urllib.parse
import urllib.request

DOI = "10.5061/dryad.95x69p907"
ROOT = "https://datadryad.org/api/v2"
UA = "egwee-conospermum-2026-schema/1.1"
TARGETS = {"Seedlings_scoring.xlsx", "Paternity_dataset.xlsx", "README.md"}


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def href(obj: dict, key: str) -> str | None:
    v = obj.get("_links", {}).get(key)
    if isinstance(v, dict):
        return v.get("href")
    return None


def main() -> None:
    key = urllib.parse.quote(f"doi:{DOI}", safe="")
    ds_url = f"{ROOT}/datasets/{key}"
    ds = get_json(ds_url)
    version_url = href(ds, "stash:version") or href(ds, "version")
    if not version_url:
        versions = get_json(ds_url + "/versions")
        items = versions.get("_embedded", {}).get("stash:versions", [])
        if not items:
            raise RuntimeError("no public versions")
        version_url = href(items[0], "self")
    if version_url and version_url.startswith("/"):
        version_url = "https://datadryad.org" + version_url
    version = get_json(version_url)
    files_url = href(version, "stash:files") or href(version, "files")
    if files_url and files_url.startswith("/"):
        files_url = "https://datadryad.org" + files_url
    if not files_url:
        vid = version.get("id")
        files_url = f"{ROOT}/versions/{vid}/files"
    page = get_json(files_url)
    items = page.get("_embedded", {}).get("stash:files", page.get("files", []))
    out = []
    link_debug = []
    for item in items:
        path = item.get("path") or item.get("name")
        out.append({
            "path": path,
            "size": item.get("size"),
            "mimeType": item.get("mimeType"),
            "digest": item.get("digest"),
            "id": item.get("id"),
        })
        if path in TARGETS:
            link_debug.append({
                "path": path,
                "top_level_keys": sorted(item.keys()),
                "links": item.get("_links", {}),
                "downloadUrl": item.get("downloadUrl"),
                "storageStatus": item.get("storageStatus"),
            })
    print("CONOSPERMUM_2026_DRYAD_SCHEMA " + json.dumps({"doi": DOI, "n_files": len(out), "files": out}, sort_keys=True))
    print("CONOSPERMUM_2026_DRYAD_LINK_DEBUG " + json.dumps(link_debug, sort_keys=True))
    print("CONOSPERMUM_2026_SCHEMA_BOUNDARY metadata_links_only_no_file_bytes_opened")


if __name__ == "__main__":
    main()
