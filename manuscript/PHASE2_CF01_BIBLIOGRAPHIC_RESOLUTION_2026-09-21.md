# Phase-2 CF01 bibliographic resolution — 2026-09-21

## Route

The 363-unit partial CF01 seed manifest was resolved through one uniform public bibliographic route: **OpenAlex**.

No effect-size or significance field is queried or used.

- seed units: **363**;
- exact-DOI seeds: **83**;
- citation-only seeds: **280**;
- resolved total: **296**;
- resolved by exact DOI: **83**;
- resolved by fail-closed citation search: **213**;
- resolved through Crossref bibliographic match → OpenAlex exact DOI: **213**;
- unresolved: **67**;
- resolution rate: **81.5%**.

## Fail-closed matching rule

DOI-bearing seeds are resolved only through exact DOI lookup.

Citation-only seeds use Crossref bibliographic lookup and then require an exact DOI handoff to OpenAlex. They require:

1. exact first-author surname;
2. exact publication year;
3. plus first-page agreement, strong title agreement, or volume agreement with a clear ranking margin.

Ambiguous results remain unresolved rather than being assigned to the highest search result.

## Next operation

Only resolved units are eligible for automated backward/forward citation materialization. Unresolved units remain in the search denominator and must be resolved through a second bibliographic route or manual bibliographic adjudication; they are not silently dropped.
