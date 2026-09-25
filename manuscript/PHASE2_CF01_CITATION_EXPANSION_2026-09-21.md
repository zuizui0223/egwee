# Phase-2 CF01 citation expansion — 2026-09-21

## Expansion rule

Every bibliographically resolved CF01 seed is expanded uniformly through the OpenAlex citation graph.

- backward direction: every ID in the seed work's `referenced_works`;
- forward direction: every work returned by the OpenAlex `cites:<seed>` relation;
- frozen publication cutoff: **2026-09-18**;
- search ranking used for inclusion: **no**;
- effect direction or significance used for inclusion: **no**.

## Current materialization

- seed manifest units: **363**;
- bibliographically resolved seed units: **296**;
- unique resolved OpenAlex works expanded: **292**;
- duplicate resolved-work groups retained as shared provenance: **4**;
- unresolved seeds retained but not expanded: **67**;
- unique discovered candidate works: **17472**;
- citation edges: **34020**;
- already-existing CF01 seeds rediscovered: **262**;
- new candidates dated on/before cutoff and ready for title/abstract/method screening: **16907**;
- post-cutoff candidates retained as excluded audit records: **2**;
- candidates with unknown publication date requiring cutoff adjudication: **1**;
- candidates whose OpenAlex metadata could not be resolved: **300**.

Any seed-resolution or forward-query failure remains visible in the summary and does not silently remove the seed from the systematic denominator.

## Next operation

Deduplicate the eligible new candidate works against the current 363-seed manifest by OpenAlex ID/DOI, then run outcome-blind title/abstract/method screening for EGWEE fragmentation relevance and prespecified layer geometry.
