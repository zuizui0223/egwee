from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "evidence/meta_extraction/PS022_aizen_feinsinger_site_means_v1.csv"


def main() -> None:
    with PATH.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 24
    assert Counter(r["species"] for r in rows) == {
        "Atamisquea emarginata": 8,
        "Cercidium australe": 8,
        "Prosopis nigra": 8,
    }
    by = defaultdict(list)
    for r in rows:
        key = (r["species"], r["condition"])
        by[key].append(int(r["site_id"]))
        assert float(r["I_pollen_tubes"]) >= 0
        assert float(r["F_fruit_set"]) >= 0
    for key, sites in by.items():
        assert sorted(sites) == [1, 2, 3, 5], (key, sites)
    assert {r["condition"] for r in rows} == {"continuous", "small"}
    print("ML020_SOURCE_ROWS_OK")


if __name__ == "__main__":
    main()
