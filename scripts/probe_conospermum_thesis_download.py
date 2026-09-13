from __future__ import annotations

import html
import re
import urllib.parse
import urllib.request

PAGE = "https://ro.ecu.edu.au/theses/2398/"


def get(url: str) -> tuple[int, str, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 egwee-conospermum-thesis-audit/1.0", "Referer": PAGE})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read()


def main() -> None:
    status, ctype, payload = get(PAGE)
    text = payload.decode("utf-8", errors="replace")
    print(f"CONOSPERMUM_THESIS_PAGE status={status} type={ctype!r} bytes={len(payload)}")
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', text, flags=re.I)
    candidates = []
    for raw in hrefs:
        href = html.unescape(raw)
        full = urllib.parse.urljoin(PAGE, href)
        low = full.lower()
        if "viewcontent" in low or low.endswith(".pdf") or "download" in low:
            candidates.append(full)
    for url in dict.fromkeys(candidates):
        try:
            s, ct, body = get(url)
            print(f"CONOSPERMUM_THESIS_CANDIDATE status={s} type={ct!r} bytes={len(body)} magic={body[:12].hex()!r} url={url!r}")
        except Exception as exc:
            print(f"CONOSPERMUM_THESIS_CANDIDATE_ERROR error={type(exc).__name__}:{exc} url={url!r}")


if __name__ == "__main__":
    main()
