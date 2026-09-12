from __future__ import annotations

import urllib.error
import urllib.request

PII = "S0006320721000598"
BASE = "https://ars.els-cdn.com/content/image"
EXTENSIONS = ("docx", "xlsx", "pdf", "zip", "doc", "xls")
INDICES = (1, 2, 3)


def probe(url: str) -> tuple[int | None, str, int | None, bytes]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 egwee-supplement-audit/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            chunk = response.read(64)
            content_type = response.headers.get("Content-Type", "")
            content_length = response.headers.get("Content-Length")
            length = int(content_length) if content_length and content_length.isdigit() else None
            return response.status, content_type, length, chunk
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Content-Type", ""), None, b""
    except Exception as exc:
        print(f"SPONDIAS_SUPPLEMENT_ERROR url={url!r} error={type(exc).__name__}:{exc}")
        return None, "", None, b""


def main() -> None:
    found: list[str] = []
    for index in INDICES:
        for ext in EXTENSIONS:
            url = f"{BASE}/1-s2.0-{PII}-mmc{index}.{ext}"
            status, content_type, length, chunk = probe(url)
            print(
                "SPONDIAS_SUPPLEMENT_PROBE "
                f"status={status!r} type={content_type!r} length={length!r} "
                f"magic={chunk[:12].hex()!r} url={url!r}"
            )
            if status == 200 and chunk:
                found.append(url)
    print(f"SPONDIAS_SUPPLEMENT_FOUND n={len(found)} urls={found!r}")


if __name__ == "__main__":
    main()
