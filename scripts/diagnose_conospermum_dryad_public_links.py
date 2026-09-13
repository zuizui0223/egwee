from __future__ import annotations

import html
import re
import subprocess
from urllib.parse import quote

DATASETS = {
    "paternity_2026": "10.5061/dryad.95x69p907",
    "reproduction_2019": "10.5061/dryad.4cg374r",
}
TARGET_NAMES = {
    "paternity_2026": ["Paternity_dataset_unformatted.xlsx", "Seedlings_scoring_unformatted.xlsx"],
    "reproduction_2019": ["fruit_and_seed_set.csv"],
}


def curl_text(url: str) -> str:
    proc = subprocess.run(
        [
            "curl", "-L", "--fail", "--silent", "--show-error",
            "-A", "Mozilla/5.0 egwee-dryad-public-link-audit/1.0",
            url,
        ],
        check=False,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout.decode("utf-8", errors="replace")


def contexts(text: str, needle: str, radius: int = 800) -> list[str]:
    out: list[str] = []
    lower = text.lower()
    start = 0
    nlow = needle.lower()
    while True:
        i = lower.find(nlow, start)
        if i < 0:
            break
        out.append(text[max(0, i-radius):min(len(text), i+len(needle)+radius)])
        start = i + len(needle)
    return out


def main() -> None:
    for label, doi in DATASETS.items():
        encoded = quote(f"doi:{doi}", safe="")
        urls = [
            f"https://datadryad.org/dataset/{encoded}",
            f"https://datadryad.org/stash/dataset/{encoded}",
        ]
        page = ""
        used = ""
        for url in urls:
            try:
                page = curl_text(url)
                used = url
                break
            except Exception as exc:
                print(f"DRYAD_PAGE_FAIL label={label!r} url={url!r} error={type(exc).__name__}:{exc}")
        assert page, label
        decoded = html.unescape(page)
        print(f"DRYAD_PAGE label={label!r} url={used!r} bytes={len(page.encode('utf-8'))}")

        stream_ids = sorted(set(re.findall(r"(?:stash/)?downloads/file_stream/(\d+)", decoded)))
        api_ids = sorted(set(re.findall(r"api/v2/files/(\d+)", decoded)))
        print(f"DRYAD_PAGE_STREAM_IDS label={label!r} ids={stream_ids!r}")
        print(f"DRYAD_PAGE_API_FILE_IDS label={label!r} ids={api_ids!r}")

        for name in TARGET_NAMES[label]:
            snippets = contexts(decoded, name)
            print(f"DRYAD_FILENAME_CONTEXT label={label!r} name={name!r} n={len(snippets)}")
            for j, snippet in enumerate(snippets[:4], start=1):
                compact = re.sub(r"\s+", " ", snippet)
                print(f"DRYAD_CONTEXT label={label!r} name={name!r} idx={j} text={compact!r}")
                ids = sorted(set(re.findall(r"(?:stash/)?downloads/file_stream/(\d+)", compact)))
                hrefs = sorted(set(re.findall(r"href=[\"']([^\"']+)[\"']", compact)))
                print(f"DRYAD_CONTEXT_LINKS label={label!r} name={name!r} stream_ids={ids!r} hrefs={hrefs!r}")

    print("CONOSPERMUM_DRYAD_PUBLIC_LINK_DIAGNOSIS PASS")


if __name__ == "__main__":
    main()
