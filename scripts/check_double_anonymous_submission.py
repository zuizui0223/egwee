from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"


def main() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    lowered = text.casefold()

    banned = [
        "egwee",
        "nee theory",
        "nee operators",
        "zuizui0223",
        "github.com/zuizui0223",
        "zhang ruiqi",
        "zhang rachel",
        "rachelzhang0223",
        "@tohoku",
        "@gmail.com",
        "our previous study",
        "in our previous study",
        "**status:**",
    ]
    for token in banned:
        if token.casefold() in lowered:
            raise AssertionError(f"anonymous manuscript contains identifying/internal token: {token!r}")

    # Identity-bearing declarations belong on the separate title page, not in
    # the reviewer-facing main manuscript.
    for heading in (
        "## Author Contributions",
        "## Acknowledgements",
        "## Acknowledgments",
        "## Conflict of Interest",
    ):
        if heading.casefold() in lowered:
            raise AssertionError(f"identity-bearing section must be on title page: {heading}")

    assert "## References" in text
    assert "Relationship to eco-genetic fragmentation theory" in text
    assert "specific finite-model" not in lowered or "specific finite-model operator" in lowered

    print("DOUBLE_ANONYMOUS_MANUSCRIPT_OK")


if __name__ == "__main__":
    main()
