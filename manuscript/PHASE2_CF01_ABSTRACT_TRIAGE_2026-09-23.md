# Phase-2 CF01 outcome-blind abstract triage — 2026-09-23

## Purpose

This is a workload-ordering layer, not an inclusion filter.

For candidates already cleared by the CF01 seed-identity firewall, OpenAlex title/abstract
metadata are scanned for habitat-fragmentation terms and prespecified EGWEE layer terms.

No effect magnitude, direction, variance, p-value or significance field is queried.

## Current materialization

- candidate queue units: **17472**;
- candidates ready for ecological title/abstract/method screening: **16851**;
- OpenAlex abstract metadata resolved: **16851**;
- ready candidates with abstract text available: **11493**;
- metadata batch failures retained: **0**.

Triage counts:

- fragmentation_no_registered_layer_hint: **1226**
- layer_hint_no_fragmentation_term: **7223**
- low_metadata_relevance_needs_screen: **6289**
- not_in_ecological_screening_set: **621**
- priority_multilayer_fragmentation: **1120**
- priority_single_layer_fragmentation: **993**

## Interpretation

priority_multilayer_fragmentation is screened first because its metadata contain both a
fragmentation term and at least two prespecified layer hints. It is not automatically included.

Likewise, low_metadata_relevance_needs_screen is not automatically excluded. Every candidate in
the ecological screening set remains part of the search denominator until title/abstract/method
screening assigns a documented decision.

## Next operation

Process the priority_multilayer_fragmentation group first, then the remaining ready candidates,
recording explicit exposure, layer, independent-unit and duplicate-programme decisions.
