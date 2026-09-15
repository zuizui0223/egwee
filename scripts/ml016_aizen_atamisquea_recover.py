"""Recover ML016 Atamisquea from site-level Appendix-I means.

This script intentionally uses the four landscape sites as the primary n.
Plant-level n/SD are not fragmentation replicates.
"""

import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "evidence/meta_extraction/ml016_aizen_atamisquea_source_rows_v1.csv"
OUT = ROOT / "evidence/meta_extraction/ml016_aizen_atamisquea_effects_v1.csv"


def hedges_g_ls(x_frag, x_ref):
    """Independent-groups Hedges g with large-sample SMD variance.

    Mirrors metafor SMD conventions for the equal-variance direct stream:
    d=(m1-m2)/sp, g=J*d, J=1-3/(4*df-1).
    LS variance is n1+n2/(n1*n2) + g^2/(2*(n1+n2)).
    """
    x1 = np.asarray(x_frag, dtype=float)
    x2 = np.asarray(x_ref, dtype=float)
    n1, n2 = len(x1), len(x2)
    df = n1 + n2 - 2
    s1 = x1.std(ddof=1)
    s2 = x2.std(ddof=1)
    sp = math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / df)
    d = (x1.mean() - x2.mean()) / sp
    J = 1 - 3 / (4 * df - 1)
    g = J * d
    vi = (n1 + n2) / (n1 * n2) + g**2 / (2 * (n1 + n2))
    return g, vi


def main():
    d = pd.read_csv(SRC)
    rows = []
    wide = {}
    for layer in ["I", "F"]:
        z = d[d.layer == layer]
        ref = z[z.habitat == "continuous"].sort_values("site")
        frag = z[z.habitat == "small_fragment"].sort_values("site")
        assert ref.site.tolist() == frag.site.tolist() == [1, 2, 3, 5]
        g, vi = hedges_g_ls(frag.site_mean, ref.site_mean)
        rows.append({
            "cluster_id": "ML016",
            "study_id": "PS021",
            "species": "Atamisquea emarginata",
            "layer": layer,
            "effect_family": "hedges_g_direct",
            "contrast": "small_fragment_vs_continuous",
            "n_fragment_sites": 4,
            "n_reference_sites": 4,
            "g_oriented": g,
            "variance": vi,
            "se": math.sqrt(vi),
        })
        wide[layer] = (frag.site_mean.to_numpy(), ref.site_mean.to_numpy())

    out = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)

    # Paired-site response contrasts preserve matching and are used only for
    # dependence diagnostics, not to increase n.
    dI = wide["I"][0] - wide["I"][1]
    dF = wide["F"][0] - wide["F"][1]
    rho = float(np.corrcoef(dI, dF)[0, 1])
    print(out.to_string(index=False))
    print(f"paired_site_delta_corr={rho:.12f}")


if __name__ == "__main__":
    main()
