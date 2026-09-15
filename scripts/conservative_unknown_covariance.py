from __future__ import annotations

import math


def two_sided_normal_p(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2.0))


def worst_case_difference_test(
    effect_a: float,
    variance_a: float,
    effect_b: float,
    variance_b: float,
) -> dict[str, float]:
    """Conservative two-endpoint contrast when sampling covariance is unknown.

    For d = effect_a - effect_b and marginal variances v_a, v_b,
    Cauchy-Schwarz implies cov >= -sqrt(v_a*v_b).  The largest possible
    variance of d is therefore (sqrt(v_a) + sqrt(v_b))**2.  Testing with
    that variance yields the largest two-sided Normal p-value over every
    admissible correlation rho in [-1, 1].
    """
    for name, value in {"variance_a": variance_a, "variance_b": variance_b}.items():
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and > 0, got {value!r}")
    for name, value in {"effect_a": effect_a, "effect_b": effect_b}.items():
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite, got {value!r}")

    difference = effect_a - effect_b
    se_max = math.sqrt(variance_a) + math.sqrt(variance_b)
    variance_max = se_max * se_max
    z_worst = difference / se_max
    p_worst = two_sided_normal_p(z_worst)

    return {
        "difference": difference,
        "variance_max": variance_max,
        "se_max": se_max,
        "z_worst": z_worst,
        "p_two_sided_worst": p_worst,
        "rho_for_variance_max": -1.0,
    }


def contrast_variance(variance_a: float, variance_b: float, rho: float) -> float:
    if not -1.0 <= rho <= 1.0:
        raise ValueError("rho must lie in [-1, 1]")
    covariance = rho * math.sqrt(variance_a * variance_b)
    return variance_a + variance_b - 2.0 * covariance
