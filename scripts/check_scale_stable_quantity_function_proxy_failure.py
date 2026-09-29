from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IF_CENSUS = ROOT / "evidence/meta_extraction/ecological_if_programme_census_v1.csv"
SCALE_GEOM = ROOT / "evidence/meta_extraction/bottleneck_scale_robustness_v1.csv"
PROXY = ROOT / "evidence/meta_extraction/scale_stable_quantity_function_proxy_failure_v1.csv"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    if_rows = rows(IF_CENSUS)
    geom = rows(SCALE_GEOM)
    proxy = rows(PROXY)

    assert len(if_rows) == 8
    assert {r["interaction_measurement_class"] for r in if_rows} == {"quantity_only"}
    assert sum(r["interaction_measurement_class"] == "quantity_only" for r in if_rows) == 8

    stable_downstream = {
        r["programme_id"]
        for r in geom
        if r["cross_scale_status"] in {"stable_downstream", "native_gradient_downstream"}
    }
    assert stable_downstream == {
        "ML015",
        "P2_CF01_CARDIOPETALUM_2012",
        "P2_CF01_BERGSDORF_KAKAMEGA_2006",
    }

    # No programme has a scale/representation-stable resolved upstream label.
    stable_upstream = {
        r["programme_id"]
        for r in geom
        if r["cross_scale_status"] in {"stable_upstream", "native_gradient_upstream"}
    }
    assert stable_upstream == set()

    proxy_ids = {r["programme_id"] for r in proxy}
    assert proxy_ids == stable_downstream
    assert len(proxy) == 3

    by = {r["programme_id"]: r for r in proxy}
    assert by["ML015"]["region"] == "Western Australia"
    assert by["ML015"]["plant_family"] == "Myrtaceae"
    assert "bird_and_insect" in by["ML015"]["pollination_biology"]

    assert by["P2_CF01_CARDIOPETALUM_2012"]["region"] == "Brazilian cerrado"
    assert by["P2_CF01_CARDIOPETALUM_2012"]["plant_family"] == "Annonaceae"
    assert "beetle" in by["P2_CF01_CARDIOPETALUM_2012"]["pollination_biology"]

    assert by["P2_CF01_BERGSDORF_KAKAMEGA_2006"]["region"] == "Western Kenya"
    assert by["P2_CF01_BERGSDORF_KAKAMEGA_2006"]["plant_family"] == "Acanthaceae"
    assert by["P2_CF01_BERGSDORF_KAKAMEGA_2006"]["growth_form"] == "shrub"

    print(
        "SCALE_STABLE_PROXY_FAILURE_OK "
        "IF_programmes=8 quantity_only=8 effective_mating=0 "
        "stable_downstream=3 stable_upstream=0 "
        "continents=3 families=3"
    )


if __name__ == "__main__":
    main()
