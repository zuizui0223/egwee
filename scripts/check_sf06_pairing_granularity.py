from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = ROOT / "evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv"
NOTE = ROOT / "manuscript/SF06_PAIRING_GRANULARITY_BOUNDARY_2026-10-07.md"

OVERLAP = {
    "aizen & feinsinger (1994) ecology 75:330- 351",
    "angoh et al. (2021) south african journal of botany 141:196- 199",
    "chen & zuo (2019) frontiers in plant science 10:327",
    "chen et al. (2019) science of the total environment 654:1056- 1063",
    "chiapero et al. (2021) forest ecology and management 492:119215",
    "da silva elias et al. (2012) journal of tropical ecology 28:317- 320",
    "gonzález-varo et al. (2009) biological conservation 142:1058- 1065",
    "kolb (2008) biological conservation 141:2540- 2549",
    "lopes & buzato (2007) oecologia 154:305- 314",
}


def audit(rows):
    ll = sum(float(r['d_I']) < 0 and float(r['d_F']) < 0 for r in rows)
    ln = sum(float(r['d_I']) < 0 and float(r['d_F']) >= 0 for r in rows)
    nl = sum(float(r['d_I']) >= 0 and float(r['d_F']) < 0 for r in rows)
    nn = sum(float(r['d_I']) >= 0 and float(r['d_F']) >= 0 for r in rows)
    mismatch = min(ll, ln) + min(nl, nn)
    baseline = len(rows) - max(ll + nl, ln + nn)
    return len(rows), ll, ln, nl, nn, mismatch, baseline


def loo(rows, key):
    return min(
        audit([r for r in rows if r[key] != value])[5]
        for value in {r[key] for r in rows}
    )


def main() -> None:
    with PAIRS.open(newline='', encoding='utf-8') as fh:
        rows = [
            r for r in csv.DictReader(fh)
            if r['land_use_factor_normalized'] == 'habitat fragmentation'
            and r['n_I_rows_combined'] == '1'
            and r['n_F_rows_combined'] == '1'
        ]

    assert audit(rows) == (50, 31, 9, 7, 3, 12, 12)
    assert loo(rows, 'source_publication_key') == 8
    assert loo(rows, 'species') == 11

    ext = [r for r in rows if r['source_publication_key'] not in OVERLAP]
    assert audit(ext) == (27, 16, 6, 4, 1, 7, 7)
    assert loo(ext, 'source_publication_key') == 5
    assert loo(ext, 'species') == 6

    note = NOTE.read_text(encoding='utf-8')
    assert '**12/50**' in note
    assert '**7/27**' in note
    assert 'publication × species × land-use stratum' in note

    print('SF06_PAIRING_GRANULARITY: PASS')


if __name__ == '__main__':
    main()
