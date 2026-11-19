# QPF007 post-outcome pair-equal and independent-chain diagnostic

**2026-11-19, retrospective diagnostic created AFTER opening the preregistered co10 genetic-offspring-weighted fixed-margin result.** Original `T10` 688 positive/741 outcrossed genotyped seedlings, 0.928475 observed vs 0.802345 source-marginal null, excess +0.126130, one-sided Monte Carlo p≈0.0005, 15/16 original sessions with positive excess. That original statistical target and previously chosen 2000 draws, source model, main and broader egwee programmes remain unchanged.

## Why this new post-outcome check matters

A genetically assigned mother–father pair may contribute multiple sampled offspring. The original statistic weights highly fecund or disproportionately sampled genetic pairs many times, potentially overstating breadth of mother–father **distinct partner** coverage. The source consists of **303 distinct outcrossed mother–father pairs**, but 741 genotyped outcrossed offspring. Original Barbot et al. 2026 already describe and quantify observational/genetic mating skew; we must not describe that broad finding as ours.

## Fixed diagnostic (not a second confirmatory test)

Only original source ID/carryover-10 contact values certified by source SHA on the already locked 16-session maternal roster, parentage table and R code. Identical source exclusions: outcross genetic assignments only, source missing pair ≠ ecological zero, no unrecorded self identity promoted, same `import_nb_visit_co10` sign >0. Current **new outcome** is fraction of **distinct** genetically observed outcross pairs with documented source positive contact. Deduplicate within session `(mother,father)` first; count missing pair, recorded source zero and recorded contact. No reranking by visit value.

Fixed-margin null exactly as parent analysis: swap father labels among outcross offspring within their original experimental session, preserving every mother and father genotyped-offspring count, reject any resulting self pair. Then deduplicate after each null draw, and measure source-positive pair fraction. Two additional fixed, independent `random.Random` chains (seeds **20261121** and **20261122**), **2000 draws per chain**, **1500 attempted warm-up swaps per exchangeable session**, **100 attempts between samples**; original nonexchangeable group held unchanged. No new odds or p-threshold, no hypothesis-promoting significant pair fraction if stronger than original. Display observed minus null mean, null 95% reference quantiles, Monte Carlo p for context, per-source-session mean excess and how many of 16 groups positive.

Also recompute original **offspring-weighted** source statistic in these two independently seeded chains to audit null mixing. Show each chain's expected score and the largest absolute between-chain variation; report `MC_CONVERGENCE_WARNING` if absolute chain null-mean difference >0.01 on either unit. That threshold is an audit tolerance only, not an outcome selection condition or claimed biological effect.

Biological claim ceiling: One published greenhouse-cage *Brassica rapa* experiment, not independent natural ecological study; observed pollinator movements provide carryover-assumed contact *evidence*, not verified deposited donor-specific pollen; CERVUS best paternal assignments at 80% and genotyped-offspring sampling; structural missing pair rows do not imply negative contact. This alternative weighting is POST HOC and no new preregistered generality.

No raw published parentage observations, plant/offspring names, or genotype values redistributed. Report derivative-only aggregate; do not alter original preregistered co10 result or other egwee source programmes.
