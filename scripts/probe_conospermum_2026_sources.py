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


def dataset_url(doi: str) -> str:
    encoded = urllib.parse.quote(f"doi:{doi}", safe="")
    return f"{BASE}/api/v2/datasets/{encoded}"


def dataset_json(doi: str) -> tuple[str, dict]:
    url = dataset_url(doi)
    return url, get_json(url)


def normalize_link(value: str) -> str:
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if value.startswith("/api/"):
        return BASE + value
    raise ValueError(value)


def relation(payload: dict, key: str) -> str:
    links = payload.get("_links")
    assert isinstance(links, dict), sorted(payload)
    value = links.get(key)
    assert isinstance(value, dict) and isinstance(value.get("href"), str), (key, links)
    return normalize_link(value["href"])


def embedded_files(payload: dict) -> list[dict]:
    embedded = payload.get("_embedded")
    assert isinstance(embedded, dict), payload
    for key in ("stash:files", "files"):
        items = embedded.get(key)
        if isinstance(items, list):
            return [item for item in items if isinstance(item, dict)]
    raise AssertionError((sorted(embedded), payload))


def item_name(item: dict) -> str:
    return str(item.get("path") or item.get("name") or item.get("fileName") or item.get("filename") or "")


def source_snapshot(doi: str) -> tuple[dict, dict, list[dict]]:
    """Three JSON requests max: dataset -> current version -> current files."""
    _, dataset = dataset_json(doi)
    version_url = relation(dataset, "stash:version")
    version = get_json(version_url)
    files_url = relation(version, "stash:files")
    files_payload = get_json(files_url)
    files = embedded_files(files_payload)
    return dataset, version, files


def main() -> None:
    for label, doi in DATASETS.items():
        dataset, version, files = source_snapshot(doi)
        print(
            f"DRYAD_SOURCE label={label!r} doi={doi!r} dataset_id={dataset.get('id')!r} "
            f"version_number={version.get('versionNumber')!r} version_link={relation(dataset, 'stash:version')!r}"
        )
        print(f"DRYAD_FILES label={label!r} n={len(files)} names={[item_name(item) for item in files]!r}")
        for item in files:
            links = item.get("_links") if isinstance(item.get("_links"), dict) else {}
            print(
                f"DRYAD_FILE label={label!r} name={item_name(item)!r} size={item.get('size')!r} "
                f"mime={item.get('mimeType')!r} download={links.get('stash:download')!r}"
            )

        expected = (
            {"Paternity_dataset_unformatted.xlsx", "Seedlings_scoring_unformatted.xlsx"}
            if label == "paternity_2026"
            else {"fruit_and_seed_set.csv"}
        )
        names = {item_name(item) for item in files}
        missing = expected - names
        assert not missing, (label, missing, names)

    print("CONOSPERMUM_2026_SOURCE_PROBE PASS")


if __name__ == "__main__":
    main()
