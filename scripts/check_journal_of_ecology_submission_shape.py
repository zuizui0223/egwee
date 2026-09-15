from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md"
METADATA = ROOT / "manuscript/meta_analysis_submission_metadata.md"


def words(text: str) -> list[str]:
    # Stable repository-side approximation for submission shaping. This is not
    # intended to reproduce the publisher's production word counter exactly.
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"\[[^\]]*\]\([^\)]*\)", " ", text)
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’._–—/-]*", text)


def section(text: str, start: str, end: str | None) -> str:
    a = text.index(start) + len(start)
    b = text.index(end, a) if end else len(text)
    return text[a:b].strip()


def main() -> None:
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    metadata = METADATA.read_text(encoding="utf-8")

    assert manuscript.startswith(
        "# Testing whether fragmentation acts as a single biological state:"
    )
    for heading in (
        "## Abstract",
        "## Keywords",
        "## Introduction",
        "## Materials and Methods",
        "## Results",
        "## Discussion",
        "## Conclusion",
    ):
        assert heading in manuscript, heading

    abstract = section(manuscript, "## Abstract", "## Keywords")
    abstract_words = len(words(abstract))
    assert abstract_words <= 350, abstract_words
    numbered = re.findall(r"(?m)^([1-5])\. ", abstract)
    assert numbered == ["1", "2", "3", "4", "5"], numbered
    assert "5. **Synthesis.**" in abstract

    keywords = section(manuscript, "## Keywords", "## Introduction")
    keyword_items = [x.strip() for x in keywords.split(";") if x.strip()]
    assert 1 <= len(keyword_items) <= 8, keyword_items
    assert keyword_items == sorted(keyword_items, key=str.casefold), keyword_items

    intro = manuscript.index("## Introduction")
    methods = manuscript.index("## Materials and Methods")
    results = manuscript.index("## Results")
    discussion = manuscript.index("## Discussion")
    conclusion = manuscript.index("## Conclusion")
    assert intro < methods < results < discussion < conclusion

    main_text = manuscript[intro:]
    main_words = len(words(main_text))
    assert main_words <= 8000, main_words

    # Journal shaping may never weaken the canonical empirical claim.
    for token in (
        "17 marginal effects",
        "p = 0.01212432",
        "p = 0.18194353",
        "p_ML020=1.0",
        "Serapias",
        "sixth cluster",
    ):
        assert token in manuscript, token

    assert "**Primary target journal:** **Journal of Ecology**" in metadata
    assert "Research Article / empirical research synthesis" in metadata
    assert "results_bearing_conditional_state_separation" in metadata

    print(
        "JOURNAL_OF_ECOLOGY_SHAPE_OK "
        f"abstract_words={abstract_words} "
        f"keywords={len(keyword_items)} "
        f"main_words={main_words}"
    )


if __name__ == "__main__":
    main()
