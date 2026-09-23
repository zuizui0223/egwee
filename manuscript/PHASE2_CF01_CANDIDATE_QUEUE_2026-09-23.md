# Phase-2 CF01 candidate deduplication queue — 2026-09-23

## Purpose

The citation graph is deduplicated against the frozen 363-unit CF01 seed manifest before
ecological screening or numerical extraction.

No effect direction, magnitude, variance, p-value or significance field is used.

## Identity firewall

A discovered candidate is treated as an existing seed when it matches a seed by:

- exact OpenAlex work ID;
- exact DOI; or
- exact normalized title plus publication year.

A candidate that only shares first-author surname + publication year with a still-unresolved
seed is not auto-collapsed and is not sent directly to ecological screening. It enters
pending_seed_identity_adjudication.

Only candidates dated on/before the frozen cutoff and with no detected seed identity collision
enter pending_title_abstract_methods_screen.

## Current counts

- seed manifest units: **363**;
- discovered candidate works: **17472**;
- existing-seed rediscoveries after identity firewall: **263**;
- unresolved-seed identity adjudications: **55**;
- new candidates ready for title/abstract/method screening: **16851**.

Other candidates retain their inherited post-cutoff/date/metadata status.

## Next operation

Retrieve outcome-blind bibliographic abstract metadata for the pending_title_abstract_methods_screen
set, then screen for EGWEE habitat-fragmentation relevance and prespecified layer geometry.
