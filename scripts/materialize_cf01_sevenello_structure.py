from __future__ import annotations

import csv
import io
import json
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_figshare_manifest_v1.json"
BEE_UNITS = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_bee_structural_units_v1.csv"
PLANT_UNITS = ROOT / "evidence/meta_extraction/phase2_cf01_sevenello_plant_structural_units_v1.csv"
SUMMARY = ROOT / "manuscript/PHASE2_CF01_SEVENELLO_STRUCTURE_2026-09-25.md"

UA = "egwee-sevenello-structure/1.0"


def download(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read().decode("utf-8-sig")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_name = {f["name"]: f for f in manifest["files"]}

    bees = list(csv.DictReader(io.StringIO(download(by_name["landscape_bees.csv"]["download_url"]))))
    seeds = list(csv.DictReader(io.StringIO(download(by_name["landscape_seeds.csv"]["download_url"]))))

    # Structural-only bee table: do not read any bee response column.
    bee_rows = [
        {
            "site": r["site"],
            "crop": r["crop"],
            "transect": r["transect"],
            "area_km2": r["area"],
        }
        for r in bees
    ]
    assert len(bee_rows) == len({(r["site"], r["crop"], r["transect"]) for r in bee_rows})

    BEE_UNITS.parent.mkdir(parents=True, exist_ok=True)
    with BEE_UNITS.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["site", "crop", "transect", "area_km2"])
        w.writeheader()
        w.writerows(sorted(bee_rows, key=lambda r: (r["site"], r["crop"], r["transect"])))

    # Structural-only plant occupancy: species/site/crop/transect plus lower-level
    # row/treatment counts. No flower or seed response values are read.
    groups: dict[tuple[str, str, str, str], Counter[str]] = defaultdict(Counter)
    for r in seeds:
        key = (r["species"], r["site"], r["crop_type"], r["transect"])
        groups[key][r["treat"]] += 1

    treatment_names = sorted({t for counts in groups.values() for t in counts})
    plant_rows = []
    for (species, site, crop, transect), counts in sorted(groups.items()):
        row = {
            "species": species,
            "site": site,
            "crop": crop,
            "transect": transect,
            "n_individual_rows": sum(counts.values()),
        }
        for treatment in treatment_names:
            row[f"n_treat_{treatment}"] = counts[treatment]
        plant_rows.append(row)

    plant_fields = ["species", "site", "crop", "transect", "n_individual_rows"] + [
        f"n_treat_{t}" for t in treatment_names
    ]
    with PLANT_UNITS.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=plant_fields)
        w.writeheader()
        w.writerows(plant_rows)

    bee_sites = sorted({r["site"] for r in bee_rows})
    bee_units = sorted({(r["site"], r["crop"]) for r in bee_rows})
    edge_core_pairs = sorted({
        (site, crop)
        for site, crop in bee_units
        if {r["transect"] for r in bee_rows if r["site"] == site and r["crop"] == crop} == {"Edge", "Core"}
    })
    plant_sites = sorted({r["site"] for r in plant_rows})
    species_counts = {
        sp: {
            "site_crop_units": len({(r["site"], r["crop"]) for r in plant_rows if r["species"] == sp}),
            "transect_rows": sum(1 for r in plant_rows if r["species"] == sp),
        }
        for sp in sorted({r["species"] for r in plant_rows})
    }

    lines = [
        "# CFTQ0001 Sevenello structural-unit audit — 2026-09-25",
        "",
        "This audit uses only source identifiers, exposure fields and treatment labels/counts.",
        "No bee abundance, flower-number or seed-production values are read.",
        "",
        "## Bee structural frame",
        "",
        f"- public bee transect rows: **{len(bee_rows)}**",
        f"- unique source site labels: **{len(bee_sites)}**",
        f"- unique site × crop sampling units: **{len(bee_units)}**",
        f"- site × crop units with both Edge and Core rows: **{len(edge_core_pairs)}**",
        f"- unique remnant-area values: **{len({r['area_km2'] for r in bee_rows})}**",
        "",
        "Source site labels: " + ", ".join(bee_sites),
        "",
        "Edge/Core-paired site × crop units:",
    ]
    for site, crop in edge_core_pairs:
        area = next(r["area_km2"] for r in bee_rows if r["site"] == site and r["crop"] == crop)
        lines.append(f"- {site} | {crop} | area={area} km2")

    lines += [
        "",
        "## Plant structural frame",
        "",
        f"- public individual treatment rows: **{len(seeds)}**",
        f"- species × site × crop × transect structural rows: **{len(plant_rows)}**",
        f"- plant-site labels: **{len(plant_sites)}**",
        f"- treatment labels: {', '.join(treatment_names)}",
        "",
    ]
    for sp, counts in species_counts.items():
        lines.append(
            f"- {sp}: site×crop units={counts['site_crop_units']}; "
            f"transect rows={counts['transect_rows']}"
        )

    lines += [
        "",
        "## Gate",
        "",
        "The independent-unit contract must reconcile the article's 11 independently sampled remnants /",
        "21 total transects with the public response tables before effects are opened. Any missing bee",
        "transect or site alias must be handled as source missingness/identity, not silently imputed.",
        "",
    ]
    SUMMARY.write_text("\n".join(lines), encoding="utf-8")

    print(
        "PHASE2_CF01_SEVENELLO_STRUCTURE_OK "
        f"bee_rows={len(bee_rows)} site_labels={len(bee_sites)} "
        f"site_crop_units={len(bee_units)} edge_core_pairs={len(edge_core_pairs)} "
        f"plant_structural_rows={len(plant_rows)} effects_opened=false"
    )


if __name__ == "__main__":
    main()
