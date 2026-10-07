from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / 'evidence/meta_extraction/sf06_translation_residual_result_v1.json'
NOTE = ROOT / 'manuscript/SF06_COMPATIBILITY_TRANSLATION_SENSITIVITY_2026-10-07.md'


def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9), (a, b)


def main() -> None:
    r = json.loads(RESULT.read_text(encoding='utf-8'))
    p = r['primary']
    n = r['primary_nonoverlap_sensitivity']

    close(p['gamma_SC'], 0.06390397386984187)
    close(p['publication_balanced_model_dF_on_dI_plus_SC']['params'][2], 0.12113574188648264)
    close(p['delta_model_F_minus_I_on_SC']['params'][1], -0.17506971989739678)
    close(p['interaction_model_dF_on_dI_SC_dIxSC']['params'][2], -0.054519151060488644)
    close(p['interaction_model_dF_on_dI_SC_dIxSC']['params'][3], -0.2548284323033124)
    close(p['zero_covariance_weighted_delta_sensitivity']['gamma_SC'], -0.3836969036712302)

    close(n['gamma_SC'], 0.15654750486589272)
    close(n['zero_covariance_weighted_delta_sensitivity']['gamma_SC'], -0.5467428936219938)
    assert n['zero_covariance_weighted_delta_sensitivity']['p_two_sided'] < 0.05

    note = NOTE.read_text(encoding='utf-8')
    assert 'compatibility is a vulnerability correlate' in note
    assert 'not a robustly identified translation modifier' in note

    print('SF06_COMPATIBILITY_TRANSLATION_SENSITIVITY: PASS')


if __name__ == '__main__':
    main()
