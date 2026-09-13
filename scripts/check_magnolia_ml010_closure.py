from __future__ import annotations
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'evidence/meta_extraction/multilayer_cluster_registry_v1.csv'
RES=ROOT/'manuscript/MAGNOLIA_ML010_CLUSTER_RECOVERY_RESULT.md'
def main():
    with REG.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    by={r['cluster_id']:r for r in rows}
    assert by['ML009']['species']=='Pistacia lentiscus'
    m=by['ML010']
    assert m['study_ids']=='PS002' and m['species']=='Magnolia stellata'
    assert m['fragmentation_contrast']=='source_defined_summed_adult_genet_basal_area'
    assert int(m['n_admissible_primary_effects'])==0
    assert m['cluster_status']=='source_population_size_values_not_recoverable'
    adm=[r for r in rows if r['cluster_status']=='admissible_multilayer_cluster']
    assert {r['cluster_id'] for r in adm}=={'ML001','ML002','ML003'}
    assert sum(int(r['n_admissible_primary_effects']) for r in adm)==9
    text=RES.read_text(encoding='utf-8')
    assert 'No C/F effect or covariance was calculated' in text
    assert '85, 97, 46, 16, 23 and 4' in text
    print('Magnolia ML010 closure: PASS; Pistacia ML009 preserved; admissible state remains 3 clusters / 9 effects')
if __name__=='__main__': main()
