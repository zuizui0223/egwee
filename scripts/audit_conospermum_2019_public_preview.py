from __future__ import annotations

import re
import subprocess

BASE = "https://datadryad.org"
FILE_ID = 155093


def curl_text(path_or_url: str) -> tuple[int, str, str]:
    url = path_or_url if path_or_url.startswith("http") else BASE + path_or_url
    proc = subprocess.run(
        [
            "curl", "-L", "--silent", "--show-error",
            "-A", "Mozilla/5.0 egwee-conospermum-exposure-audit/1.0",
            "-w", "\n__HTTP_STATUS__:%{http_code}",
            url,
        ],
        capture_output=True,
        check=False,
    )
    raw = proc.stdout.decode("utf-8", errors="replace")
    m = re.search(r"\n__HTTP_STATUS__:(\d{3})\s*$", raw)
    status = int(m.group(1)) if m else 0
    text = raw[: m.start()] if m else raw
    stderr = proc.stderr.decode("utf-8", errors="replace")
    return status, text, stderr


def compact(text: str, limit: int = 12000) -> str:
    return re.sub(r"\s+", " ", text)[:limit]


def main() -> None:
    landing_path = "/dataset/doi%3A10.5061%2Fdryad.4cg374r"
    landing_status, landing, landing_err = curl_text(landing_path)
    assert landing_status == 200, (landing_status, landing_err)

    needle = f"preview_check{FILE_ID}"
    i = landing.find(needle)
    assert i >= 0, "public landing page no longer exposes preview_check for target CSV"
    context = landing[max(0, i - 1200): i + 1800]
    print(f"CONO2019_LANDING_CONTEXT text={compact(context)!r}")

    # The landing page itself is enough to establish that the public dataset
    # describes this CSV as population statistics + reproductive output. The
    # preview endpoint is then tested only as a possible ordinary route to the
    # exact population-level exposure values.
    assert "Population's statistics" in landing or "Population&#39;s statistics" in landing

    m = re.search(r'data-load=["\']([^"\']*preview_check/155093\.js)["\']', context)
    assert m, context
    check_path = m.group(1)
    print(f"CONO2019_PREVIEW_CHECK_PATH path={check_path!r}")

    status, js, err = curl_text(check_path)
    print(
        f"CONO2019_PREVIEW_CHECK_RESULT status={status} stderr={err!r} "
        f"text={compact(js)!r}"
    )

    if status != 200:
        # This is an allowed terminal qualification outcome. It means the
        # source-defined connectivity variable is documented, but exact values
        # are not reconstructable from this ordinary public preview route.
        print(
            "CONOSPERMUM_2019_PUBLIC_PREVIEW_AUDIT PASS; "
            "source_exposure_values_not_reconstructable"
        )
        return

    candidate_paths = []
    for value in re.findall(r'["\']([^"\']+)["\']', js):
        if "preview" in value.lower() or "data_file" in value.lower():
            candidate_paths.append(value.replace("\\/", "/"))
    candidate_paths = list(dict.fromkeys(candidate_paths))
    print(f"CONO2019_PREVIEW_CANDIDATES paths={candidate_paths!r}")

    followed = False
    for path in candidate_paths[:10]:
        if not (path.startswith("/") or path.startswith("http")):
            continue
        p_status, text, p_err = curl_text(path)
        print(
            f"CONO2019_PREVIEW_FOLLOW path={path!r} status={p_status} "
            f"stderr={p_err!r} text={compact(text)!r}"
        )
        if p_status == 200:
            followed = True

    print(
        "CONOSPERMUM_2019_PUBLIC_PREVIEW_AUDIT PASS; "
        + ("preview_route_reachable" if followed else "source_exposure_values_not_reconstructable")
    )


if __name__ == "__main__":
    main()
