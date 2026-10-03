from __future__ import annotations

import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_figshare_manifest_v1.json"
STATUS = ROOT / "manuscript/PHASE2_CF01_SEVENELLO_FIGSHARE_MANIFEST_2026-09-25.md"

ARTICLE_ID = 31072189
API = f"https://api.figshare.com/v2/articles/{ARTICLE_ID}"
UA = "egwee-sevenello-schema/1.0"


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def main() -> None:
    payload = fetch_json(API)
    files = payload.get("files", [])
    assert files, "Figshare API returned no files"

    manifest = {
        "schema_version": 1,
        "candidate": "CFTQ0001",
        "programme_id": "P2_CF01_SEVENELLO_2026",
        "article_doi": "10.1007/s10980-026-02305-2",
        "dataset_doi": "10.6084/m9.figshare.31072189",
        "figshare_article_id": ARTICLE_ID,
        "figshare_title": payload.get("title"),
        "figshare_url_public_api": API,
        "n_files": len(files),
        "files": [
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "size": item.get("size"),
                "computed_md5": item.get("computed_md5"),
                "mimetype": item.get("mimetype"),
                "download_url": item.get("download_url"),
            }
            for item in files
        ],
        "effect_outcomes_opened": False,
        "numeric_effects_calculated": False,
        "next_gate": (
            "inspect file schemas/headers only; identify remnant, reserve, transect, species, "
            "edge/core, crop and remnant-size fields before opening response values"
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# CFTQ0001 Sevenello Figshare manifest — 2026-09-25",
        "",
        "## Source",
        "",
        "- article DOI: 10.1007/s10980-026-02305-2",
        "- public dataset DOI: 10.6084/m9.figshare.31072189",
        f"- Figshare article id: **{ARTICLE_ID}**",
        f"- files indexed: **{len(files)}**",
        "",
        "This gate reads public Figshare metadata only. It does not download response tables and does",
        "not inspect bee abundance, visitation, pollen limitation, seed production or effect direction.",
        "",
        "## Files",
        "",
    ]
    for item in files:
        lines.append(
            f"- \`{item.get('name')}\`: bytes={item.get('size')}; "
            f"id={item.get('id')}; md5={item.get('computed_md5')}"
        )
    lines += [
        "",
        "## Next gate",
        "",
        "Inspect file headers/schema only and recover the source hierarchy before any numerical effect:",
        "",
        "1. reserve / remnant identity;",
        "2. edge versus core transect position;",
        "3. crop context;",
        "4. remnant area;",
        "5. species identity and transect occupancy;",
        "6. the nesting/remnant structure needed to prevent plants or quadrats becoming fragmentation n.",
        "",
        "Only after those structural fields are frozen may an I/F endpoint pair be selected under a",
        "candidate-specific recovery contract.",
        "",
    ]
    STATUS.write_text("\n".join(lines), encoding="utf-8")

    print(
        "PHASE2_CF01_SEVENELLO_MANIFEST_OK "
        f"files={len(files)} effects_opened=false"
    )


if __name__ == "__main__":
    main()
