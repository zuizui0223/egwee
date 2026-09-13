from __future__ import annotations

import json
import urllib.parse
import urllib.request

DATASETS = {
    "paternity_2026": "10.5061/dryad.95x69p907",
    "reproduction_2019": "10.5061/dryad.4cg374r",
}


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "egwee-conospermum-2026-audit/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


def dataset_json(doi: str) -> tuple[str, dict]:
    encoded = urllib.parse.quote(f"doi:{doi}", safe="")
    candidates = [
        f"https://datadryad.org/api/v2/datasets/{encoded}",
        f"https://datadryad.org/api/v2/datasets/doi:{doi}",
    ]
    errors: list[str] = []
    for url in candidates:
        try:
            return url, get_json(url)
        except Exception as exc:  # diagnostic probe
            errors.append(f"{url} -> {type(exc).__name__}: {exc}")
    raise RuntimeError("; ".join(errors))


def walk_links(obj: object, path: str = "") -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            child = f"{path}.{key}" if path else key
            if isinstance(value, str) and value.startswith("http"):
                found.append((child, value))
            else:
                found.extend(walk_links(value, child))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            found.extend(walk_links(value, f"{path}[{i}]"))
    return found


def find_file_payload(dataset: dict) -> list[dict]:
    # Dryad API versions have changed. Follow any API links that plausibly expose
    # versions/files, but never use search results to choose a biological effect.
    urls: list[str] = []
    for path, url in walk_links(dataset):
        low = f"{path} {url}".lower()
        if any(token in low for token in ("version", "file")):
            urls.append(url)
    resource_id = dataset.get("id") or dataset.get("identifier")
    if resource_id is not None:
        urls.extend([
            f"https://datadryad.org/api/v2/datasets/{resource_id}/versions",
            f"https://datadryad.org/api/v2/versions/{resource_id}/files",
        ])

    visited: set[str] = set()
    queue = urls[:]
    files: list[dict] = []
    while queue and len(visited) < 20:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            payload = get_json(url)
        except Exception as exc:
            print(f"DRYAD_FOLLOW_FAIL url={url!r} error={type(exc).__name__}:{exc}")
            continue

        candidates: list[object] = []
        if isinstance(payload, dict):
            candidates.extend(payload.get("_embedded", {}).values() if isinstance(payload.get("_embedded"), dict) else [])
            for key in ("files", "stash:files", "versions", "stash:versions"):
                if key in payload:
                    candidates.append(payload[key])
        for candidate in candidates:
            if isinstance(candidate, list):
                for item in candidate:
                    if isinstance(item, dict):
                        text = json.dumps(item).lower()
                        if any(ext in text for ext in (".xlsx", ".csv", ".txt", ".zip")):
                            files.append(item)
                        for _, link in walk_links(item):
                            if "api/v2" in link and link not in visited:
                                queue.append(link)
            elif isinstance(candidate, dict):
                for _, link in walk_links(candidate):
                    if "api/v2" in link and link not in visited:
                        queue.append(link)
        for _, link in walk_links(payload):
            if "api/v2" in link and any(t in link.lower() for t in ("version", "file")) and link not in visited:
                queue.append(link)
    return files


def main() -> None:
    for label, doi in DATASETS.items():
        url, dataset = dataset_json(doi)
        print(f"DRYAD_DATASET label={label!r} doi={doi!r} api_url={url!r}")
        print(f"DRYAD_DATASET_KEYS label={label!r} keys={sorted(dataset)!r}")
        files = find_file_payload(dataset)
        print(f"DRYAD_FILES label={label!r} n={len(files)}")
        for item in files:
            name = item.get("path") or item.get("name") or item.get("fileName") or item.get("filename")
            size = item.get("size") or item.get("filesize") or item.get("fileSize")
            links = walk_links(item)
            print(f"DRYAD_FILE label={label!r} name={name!r} size={size!r} links={links!r}")

        expected = (
            {"Paternity_dataset_unformatted.xlsx", "Seedlings_scoring_unformatted.xlsx"}
            if label == "paternity_2026"
            else {"fruit_and_seed_set.csv"}
        )
        names = {
            str(item.get("path") or item.get("name") or item.get("fileName") or item.get("filename"))
            for item in files
        }
        missing = expected - names
        assert not missing, (label, missing, names)

    print("CONOSPERMUM_2026_SOURCE_PROBE PASS")


if __name__ == "__main__":
    main()
