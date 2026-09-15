from __future__ import annotations


def ls_smd_variance(g: float, n1: int, n2: int) -> float:
    return (n1 + n2) / (n1 * n2) + (g * g) / (2.0 * (n1 + n2))


def main() -> None:
    # Existing canonical ML014 value: this guards the exact variance semantics
    # used by the primary direct Hedges-g stream.
    got = ls_smd_variance(-1.02391388, 13, 15)
    expected = 0.16231117
    assert abs(got - expected) < 1e-8, (got, expected)
    print(f"ML020_VARIANCE_SEMANTICS_OK {got:.10f}")


if __name__ == "__main__":
    main()
