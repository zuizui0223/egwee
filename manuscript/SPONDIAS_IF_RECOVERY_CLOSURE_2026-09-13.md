# Spondias I/F recovery closure — effect-unit firewall preserved

## Decision

`ML003 / PS001 Spondias purpurea` remains admitted as a covariance-aware `C/G_adult` multilayer cluster. Publicly recoverable pollinator-interaction (`I`) and reproductive-function (`F`) evidence is biologically informative but is **not effect-unit-valid for promotion into the primary Hedges-g cluster stream** under the locked cluster contract.

Machine-readable decision:

- `I`: `model_supported_cluster_inadmissible`
- `F`: `model_supported_cluster_inadmissible`
- `ML003`: remains `C/G_adult`
- covariance-aware C-F denominator: remains `k=2`

This is an effect-unit/representation boundary, not a biological null.

## Supplement recovery

The Elsevier package for Cristobal-Perez et al. (2021), PII `S0006320721000598`, exposes one supplementary file:

- `1-s2.0-S0006320721000598-mmc1.docx`

The CI probe found no additional `mmc2`/`mmc3` package in the tested document/workbook/archive formats.

The recovered document contains exactly two appendices:

1. Appendix A: site-level numbers of males/females and sex ratio for Chamela, Careyes, Ranchitos, Mesa and Nacastillo;
2. Appendix B: site × developmental-stage genetic diversity summaries (`N`, `Na`, `Ne`, `Ho`, `He`, `F`).

Neither appendix contains site-level pollinator visitation or fruit-set values. Therefore the supplement does not supply the missing five-site `I` or `F` vector required to extend the covariance block.

## Main-paper evidence

The paper nevertheless gives strong biological evidence for both layers.

### I — pollinator visitation

The methods sampled five male and five female trees per site (10 trees per site) across the same two continuous and three fragmented sites. The analysis used a generalized linear mixed model with habitat condition and plant sex as fixed effects and **site nested within habitat condition as a random factor**.

The paper reports lower visitation under fragmentation (`F_1,4 = 89.25`, `p <= 0.0025`).

This establishes source-model evidence that `I` differs between habitat conditions. It does not expose one independent site-level visitation estimate plus compatible uncertainty for each of the five sites.

### F — fruit set

Female fitness was measured on 10 female individuals per site, with ten 50-cm branches per individual; fruit set was fruits / flowers. The paper fit a binomial-logit mixed model with habitat condition as a fixed factor and **site nested within habitat condition as a random factor**, and reports higher fruit set in continuous habitat.

Figure 2 gives habitat-level back-transformed means ± SEM. Those summaries cannot be promoted to the primary cluster effect by treating trees, branches or displayed habitat means as independent fragmentation replicates.

## Why no Hedges-g rescue is allowed

The primary multilayer contract defines the independent synthesis unit at the study/species × fragmentation contrast × campaign/window × independent-unit cluster level. For ML003 that unit is the **five study sites**: two continuous versus three fragmented.

Creating `I` or `F` Hedges g from tree/branch observations, habitat-level model means, or Figure-2 SEM would either:

- replace the five independent sites with nested biological observations as `n`;
- ignore the site-within-habitat random effect;
- or invent site-level sampling covariance that the source does not report.

Any of those would violate the effect-unit firewall already used to admit C and G_adult.

## Scientific interpretation

The source supports a coherent biological chain in Spondias:

`fragmentation -> lower visitation (I) -> lower fruit set (F) / altered pollen movement (C)`

while standing adult genetic structure (`G_adult`) does not align in the same deterioration direction in the admitted five-site contrast.

For the quantitative covariance-aware synthesis, however, only `C/G_adult` is currently reconstructable on a common independent-site scale. Therefore Spondias strengthens the broad **cross-layer state-separation** result but does not increase the narrower C-F denominator.

## Final gate

`SPONDIAS_IF_RECOVERY = CLOSED_NO_EFFECT_UNIT_VALID_SITE_VECTOR`

Do not reopen by digitizing Figure 2, using tree/branch counts as fragmentation `n`, converting the reported GLIMMIX F statistics into an SMD, or assigning zero covariance. Reopen only if an author/raw-data release supplies the five-site I/F values or an exact source-model covariance representation compatible with the locked cluster unit.
