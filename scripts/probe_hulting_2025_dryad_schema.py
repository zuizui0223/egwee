from __future__ import annotations

import json
import urllib.parse
import urllib.request

DOI = "10.5061/dryad.bnzs7h4mb"
ROOT = "https://datadryad.org/api/v2"
UA = "egwee-hulting-2025-schema/1.0"


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def href(obj: dict, *keys: str) -> str | None:
    for key in keys:
        value = obj.get("_links", {}).get(key)
        if isinstance(value, dict) and value.get("href"):
            h = value["href"]
            return "https://datadryad.org" + h if h.startswith("/") else h
    return None


def main() -> None:
    key = urllib.parse.quote(f"doi:{DOI}", safe="")
    ds_url = f"{ROOT}/datasets/{key}"
    ds = get_json(ds_url)
    version_url = href(ds, "stash:version", "version")
    if not version_url:
        versions = get_json(ds_url + "/versions")
        vals = versions.get("_embedded", {}).get("stash:versions", [])
        if not vals:
            raise RuntimeError("no Dryad version")
        version_url = href(vals[0], "self")
    version = get_json(version_url)
    files_url = href(version, "stash:files", "files") or f"{ROOT}/versions/{version['id']}/files"
    page = get_json(files_url)
    files = page.get("_embedded", {}).get("stash:files", page.get("files", []))
    out = []
    for item in files:
        out.append({
            "path": item.get("path") or item.get("name"),
            "size": item.get("size"),
            "mimeType": item.get("mimeType"),
            "digest": item.get("digest"),
            "self": href(item, "self"),
        })
    print("HULTING_2025_DRYAD_SCHEMA " + json.dumps({"doi": DOI, "n_files": len(out), "files": out}, sort_keys=True))
    print("HULTING_2025_DRYAD_SCHEMA_GATE PASS metadata_only_no_file_bytes_opened")


if __name__ == "__main__":
    main()
