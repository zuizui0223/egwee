from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")

    required = (
        "d = (M_frag - M_ref) / s_p",
        "df = n_frag + n_ref - 2",
        "g = J d",
        "J = 1 - 3/(4df - 1)",
        "V(g) = (n_frag+n_ref)/(n_frag n_ref) + g^2/[2(n_frag+n_ref)]",
        "Cov_ij = rho_ij sqrt(V_i V_j)",
        "V(d_ij) = V_i + V_j - 2Cov_ij",
        "p_cluster = min(1, m min(p_ij))",
        "X = -2 sum_k log(p_k)",
        "chi-square reference distribution with `2K` degrees of freedom",
        "does **not** estimate a common mean layer difference",
        "it is not affirmative evidence that biological layers are exchangeable",
        "not evidence that their true fragmentation effects are exactly equal",
    )
    for token in required:
        assert token in text, token

    # The direct and gradient streams must remain separated.
    assert "Hedges-g and Fisher-z effects were never pooled into one primary statistic" in text
    assert "its p-value was never combined with the primary Fisher statistic" in text

    # Canonical scientific claim ceiling is unchanged.
    for token in (
        "p = 0.01212432",
        "p = 0.18194353",
        "p_ML020=1.0",
        "conditional state separation",
    ):
        assert token in text, token

    # Guard against common overclaims that the clarified estimand explicitly rejects.
    forbidden = (
        "Fisher statistic estimates the common",
        "p_ML020=1.0 proves",
        "non-significant evidence of exchangeability",
    )
    lowered = text.casefold()
    for token in forbidden:
        assert token.casefold() not in lowered, token

    print("STATISTICAL_ESTIMAND_CONTRACT_OK")


if __name__ == "__main__":
    main()
