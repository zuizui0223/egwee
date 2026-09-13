from __future__ import annotations

import json
import urllib.parse
import urllib.request

BASE = "https://datadryad.org"
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
        f"{BASE}/api/v2/datasets/{encoded}",
        f"{BASE}/api/v2/datasets/doi:{doi}",
    ]
    errors: list[str] = []
    for url in candidates:
        try:
            return url, get_json(url)
        except Exception as exc:
            errors.append(f"{url} -> {type(exc).__name__}: {exc}")
    raise RuntimeError("; ".join(errors))


def normalize_link(value: str) -> str | None:
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if value.startswith("/api/"):
        return BASE + value
    return None


def walk_links(obj: object, path: str = "") -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            child = f"{path}.{key}" if path else key
            if isinstance(value, str):
                normalized = normalize_link(value)
                if normalized is not None:
                    found.append((child, normalized))
                    continue
            found.extend(walk_links(value, child))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            found.extend(walk_links(value, f"{path}[{i}]"))
    return found


def is_file_item(item: dict) -> bool:
    text = json.dumps(item).lower()
    return any(ext in text for ext in (".xlsx", ".csv", ".txt", ".zip", ".md"))


def find_file_payload(dataset: dict) -> list[dict]:
    """Resolve file metadata through Dryad's returned relations.

    Dataset ids and version ids are distinct. We may derive the dataset->versions
    collection from the dataset id, but we never assume that dataset id is a
    version id. Version->files routes are derived only from returned version ids
    or returned links.
    """
    urls: list[str] = []
    for path, url in walk_links(dataset):
        low = f"{path} {url}".lower()
        if any(token in low for token in ("version", "file")):
            urls.append(url)

    dataset_id = dataset.get("id")
    if isinstance(dataset_id, int) or (isinstance(dataset_id, str) and dataset_id.isdigit()):
        urls.append(f"{BASE}/api/v2/datasets/{dataset_id}/versions")

    print(f"DRYAD_DATASET_LINKS links={walk_links(dataset)!r}")

    visited: set[str] = set()
    queue = list(dict.fromkeys(urls))
    files: list[dict] = []
    file_keys: set[str] = set()

    while queue and len(visited) < 50:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            payload = get_json(url)
        except Exception as exc:
            print(f"DRYAD_FOLLOW_FAIL url={url!r} error={type(exc).__name__}:{exc}")
            continue

        print(
            f"DRYAD_FOLLOW_OK url={url!r} "
            f"keys={sorted(payload) if isinstance(payload, dict) else type(payload).__name__!r}"
        )

        # Returned relations are authoritative; relative /api links are normalized.
        for _, link in walk_links(payload):
            if "api/v2" in link and any(t in link.lower() for t in ("version", "file")) and link not in visited:
                queue.append(link)

        containers: list[object] = []
        if isinstance(payload, dict):
            embedded = payload.get("_embedded")
            if isinstance(embedded, dict):
                containers.extend(embedded.values())
            for key in ("files", "stash:files", "versions", "stash:versions"):
                if key in payload:
                    containers.append(payload[key])

            # When this is a returned version object, use that version id to form
            # the documented version->files route. This is never the dataset id.
            version_id = payload.get("id")
            if "version" in url.lower() and not url.lower().endswith("/files"):
                if isinstance(version_id, int) or (isinstance(version_id, str) and str(version_id).isdigit()):
                    queue.append(f"{BASE}/api/v2/versions/{version_id}/files")

        for container in containers:
            items = container if isinstance(container, list) else [container]
            for item in items:
                if not isinstance(item, dict):
                    continue
                if is_file_item(item):
                    key = str(item.get("id") or item.get("path") or item.get("name") or item)
                    if key not in file_keys:
                        files.append(item)
                        file_keys.add(key)
                    continue

                # Items returned by a versions collection may not expose links;
                # a returned version id is sufficient to address its files route.
                item_id = item.get("id")
                if "versions" in url.lower() and not url.lower().endswith("/files"):
                    if isinstance(item_id, int) or (isinstance(item_id, str) and str(item_id).isdigit()):
                        queue.append(f"{BASE}/api/v2/versions/{item_id}/files")
                for _, link in walk_links(item):
                    if "api/v2" in link and link not in visited:
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
            print(f"DRYAD_FILE label={label!r} name={name!r} size={size!r} id={item.get('id')!r} links={links!r}")

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
