# Post-primary date-concurrency and shared-host checks — frozen exploratory design
2026-11-18 | drafted AFTER reading the strong positive primary site-year partition result in \`PRIMARY_RESULT_20261118.md\`.
**This is a retrospective robustness diagnostic**, not a second preregistered discovery or independent validation dataset.

## Why

Observed primary: +0.232323 nats above finite-sample guild-shuffle expectation, 39/39 eligible source programmes with positive programme means (311 networks). Site×year pooling does not prove bees and syrphids are choosing different flowers *at the same time*. Bee/syrphid flight seasons, phenology, detection and plant sampling times may differ. Also guilds may differ because one uses flowers never recorded with the other; that can be distinguished from within-shared-plant differential allocation.

## Locked data and comparator

Same corrected original EuPPollNet author Github commit \`31716d21d5aad8c27c1d91dd0620149ef42e8836\`, file SHA256 \`6e4e5399338d530462d8683b53a5e564d48e287e423be420c07d8046815ef38a\`, source fields/taxon definitions, Apis mellifera exclusion, original author source-independent study regrouping 23–25. Do not reselect source based on results.

### A. Strict same-date guild partition

Each source Study_id×Network_id×exact Date (valid ISO/calendar original string, not rounded days) is its own observation unit, with recorded survey method required nonambiguous. Require >=10 wild-bee visits, >=10 syrphid visits and >=3 visited flowering taxa on **that date**; this relaxed per-date threshold is fixed now before reading *same-date* effects. Compute JSD for visit allocation across plants, subtract mean of **199** exact multivariate-hypergeometric guild-shuffle null draws conditioning on same-date pooled plant-visit totals; seed 20261120. Whole-programme equal mean then 2,000 programme bootstrap replicates seed 20261121, reporting interval, positive-programme count, eligible date and programme counts. If fewer than 20 eligible source-defined study-network-date units or 5 independent programmes, return \`COVERAGE_STOP\`. This diagnostic reduces calendar-day phenology confounding but does not certify same hour/same flower individuals.

### B. Shared visited taxa only, same source network

Retain only plant taxa that have **at least one visit from each guild within the same network-year**; then require >=3 shared plant taxa and >=20 visits per guild *after* filtering. Recompute same corrected JSD, 199 shuffles seed 20261122, 2,000 whole-study bootstrap seed 20261123, 20 networks/5 programme coverage. This asks whether use proportions diverge among taxa known to be visited by both guilds, not whether they occupy completely separate plant sets.

Both share the source's 623,476 original rows. No site/plant raw rows stored. Do not combine A+B as 2 independent confirmations; no multiple-testing significance search. Compare each to original as qualitative robustness, mindful unequal observation units.

## Claim ceiling

Strong result in A suggests partition survives calendar-day conditioning; weak/coverage STOP means original site-year effect **may be a phenology/method aggregate**, not proven contemporaneous preference. B can indicate whether both guilds allocate different fractions to common visited hosts, but does not test plant availability because flower-count survey units vary. Neither estimates pollen deposition, seed setting, mating compatibility, competition or fragmentation cause. Journal-level generality requires external source replication or true functional response outcomes.
