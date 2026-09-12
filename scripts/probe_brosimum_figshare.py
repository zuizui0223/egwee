from __future__ import annotations

import json
import urllib.request

ARTICLE_ID = 22130177
API = f"https://api.figshare.com/v2/articles/{ARTICLE_ID}"


def main() -> None:
    request = urllib.request.Request(
        API,
        headers={"User-Agent": "egwee-public-data-audit/1.0"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)

    files = payload.get("files", [])
    assert files, "Figshare API returned no files"
    print(f"BROSIMUM_FIGSHARE article_id={ARTICLE_ID} title={payload.get('title')!r}")
    print(f"BROSIMUM_FIGSHARE n_files={len(files)}")
    for item in files:
        print(
            "BROSIMUM_FILE "
            f"name={item.get('name')!r} size={item.get('size')} "
            f"id={item.get('id')} md5={item.get('computed_md5')}"
        )


if __name__ == "__main__":
    main()
