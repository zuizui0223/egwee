from __future__ import annotations

import json
import urllib.error
import urllib.request

PII = "S000632072030882X"
ELSEVIER_BASE = "https://ars.els-cdn.com/content/image"
EXTENSIONS = ("docx", "xlsx", "pdf", "zip", "doc", "xls", "csv")
INDICES = (1, 2, 3, 4)
URLS = (
    "https://ro.ecu.edu.au/theses/2398/",
    "https://ro.ecu.edu.au/ecuworkspost2013/9247/",
    "https://research-repository.uwa.edu.au/en/publications/habitat-fragmentation-restricts-insect-pollinators-and-pollen-qua/",
)


def request(url: str) -> tuple[int | None, str, int | None, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 egwee-conospermum-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            chunk = r.read(256)
            length = r.headers.get("Content-Length")
            return r.status, r.headers.get("Content-Type", ""), int(length) if length and length.isdigit() else None, chunk
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type", ""), None, b""
    except Exception as exc:
        print(f"CONOSPERMUM_SOURCE_ERROR url={url!r} error={type(exc).__name__}:{exc}")
        return None, "", None, b""


def main() -> None:
    found = []
    for idx in INDICES:
        for ext in EXTENSIONS:
            url = f"{ELSEVIER_BASE}/1-s2.0-{PII}-mmc{idx}.{ext}"
            status, content_type, length, chunk = request(url)
            print("CONOSPERMUM_SUPPLEMENT_PROBE " + json.dumps({
                "status": status, "type": content_type, "length": length,
                "magic": chunk[:16].hex(), "url": url,
            }, sort_keys=True))
            if status == 200 and chunk:
                found.append(url)
    print("CONOSPERMUM_SUPPLEMENT_FOUND " + json.dumps(found))

    for url in URLS:
        status, content_type, length, chunk = request(url)
        print("CONOSPERMUM_REPOSITORY_PROBE " + json.dumps({
            "status": status, "type": content_type, "length": length,
            "prefix": chunk[:80].decode("utf-8", errors="replace"), "url": url,
        }, sort_keys=True))


if __name__ == "__main__":
    main()
