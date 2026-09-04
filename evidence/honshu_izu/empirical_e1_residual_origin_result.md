# E1 result — Honshu–Izu ecological partial-state residual-origin test

## Decision

**`ecological_partial_state_convergence_supported` at the tested ecological layer, with an explicit state-strength caveat.**

The preregistered question was whether mainland distance adds transferable information about direct pollination function after a measured functional interaction state is supplied. It did not.

This decision is **not** a claim that the measured state is complete. The functional-state model itself only modestly improved over the coarse richness comparator, and the archive lacks synchronized genetics, process-specific pollen/seed connectivity, reproductive assurance and ecological-memory variables. The result therefore supports only the narrower statement that **mainland distance did not improve transfer to unseen sites after the preregistered `I/T` partial state**.

## Source and synchronization gate

The public source was locked before analysis to Hiraiwa & Ushimaru (2024), Figshare `10.6084/m9.figshare.25025000.v1`.

The discovery workflow recovered:

- `data_main.csv`: 40 rows = 8 sites × 5 seasons, including `richness`, `FDQ`, `FEve`, `TM_z`, `dist` and `area`;
- `data_pollen.csv`: 572 direct pollination-function observations with `pollen_z`, plant identity, season and trait-matching fields;
- `data_sp_plant.csv`: the species-level table used to resolve the pollen-table site aliases without using `pollen_z`;
- original `code.R`, including the published network, trait-matching and pollen-receipt model calls.

The pollen table used short site aliases. They were mapped to the 8 `data_main` sites using shared `TM_sp` and then exact site-season `FDQ/FEve` values, **without using the response variable**:

`ishihama→hitachi`, `ibaraki→hitachinaka`, `chiba→tateyama`, `oshima→oshima`, `nii→niijima`, `kozu→kozu`, `miyake→miyake`, `hachijo→hachijo`.

All 572 observations then joined uniquely to the 40 site-season state rows with no missing primary variables.

## Frozen model sequence

All three models used season and focal-plant structure. Numeric predictors were scaled from training sites only.

- **C0 coarse state:** pollinator species richness.
- **C1 functional state:** community trait matching `TM_z` + pollinator functional diversity `FDQ` + functional evenness `FEve`.
- **C2 residual origin:** `C1 + dist`, where `dist` is distance from the mainland.

Validation was **leave-one-site-out**: every observation from one whole site was held out in each of 8 folds.

## Predictive result

### Aggregate held-out error

| model | row-weighted MSE | mean site MSE |
|---|---:|---:|
| C0 richness | 1.10963 | 1.11150 |
| C1 `TM_z + FDQ + FEve` | **1.08774** | **1.08912** |
| C2 `C1 + mainland distance` | 1.13209 | 1.12985 |

C1 improved row-weighted MSE over C0 by only **0.02189**, and beat C0 in **4/8** site folds. Thus the measured ecological state is useful but not a strong or complete compression.

Adding mainland distance to C1 did not improve transfer:

- C2 beat C1 in only **3/8** held-out sites;
- row-weighted MSE changed by **+0.04436**, i.e. **+4.08% worse**;
- mean-site MSE changed by **+0.04073**.

The strongest extrapolation penalty was Hachijo (`dist=178`): C1 MSE `0.6212` versus C2 `0.8660`. Small improvements occurred at Hitachi, Miyake and Niijima, but they did not form a transferable cross-site gain.

### Residual distance pattern

Across the eight held-out site means, the Spearman association between residual and mainland distance was approximately `-0.390` for C1 and `+0.073` after adding distance in C2. Thus the distance term can flatten a monotonic residual trend while still **worsening held-out predictive accuracy**, particularly when extrapolating to the most distant island.

For the preregistered predictive question, this is not evidence that distance is a useful residual state variable.

## Ecological interpretation

The published paper established a clear upstream chain in which island geography filters pollinator functional diversity and trait matching, and trait matching is associated with pollination function. This direct held-out test adds a different result:

> **Once `TM_z`, `FDQ`, `FEve`, season and focal plant are supplied, mainland distance does not provide transferable predictive improvement for pollen receipt across unseen sites in this dataset.**

This supports the manuscript's state-based framing over a raw island-distance regime definition at the **ecological partial-state** layer.

However, it would be incorrect to write that `TM_z + FDQ + FEve` is the complete Honshu–Izu functional-fragmentation state. C1 only modestly outperformed the richness comparator, and important state axes are absent: focal-plant genetics and mating state, pollen/seed connectivity, reproductive assurance, resource/demographic alignment and ecological history.

The correct next inference is therefore:

1. **distance itself is not recovered as a transferable residual predictor after the fixed ecological state;**
2. **the ecological partial state remains incomplete;**
3. the highest-value addition is synchronized focal-plant adult/offspring genetics and parentage/pollen-flow at the same 40-network site-seasons.

That addition would distinguish whether island history truly disappears after conditioning on a joint eco-genetic state or whether it is currently standing in for unmeasured connectivity/mating/history processes.

## Urban–island connection

E1 and the Zurich E2 test now ask the same empirical question in two different fragmentation settings:

- **Izu:** does mainland distance add information after functional diversity and trait matching?
- **Zurich:** does urban/local context add information after the function-specific pollinator interaction state?

In both cases the habitat/context variable is added **last** and judged by held-out prediction rather than by whether it has a marginal association on its own. This is the direct empirical counterpart of the state-sufficiency framework.

The two results do not yet establish full urban–island convergence because neither archive contains the complete synchronized `D/I/T/C/R/G_by_cohort/M/A` state. They do show how to search for convergence without treating `urban` or `island` as the regime itself.

## Provenance

- Figshare DOI: `10.6084/m9.figshare.25025000.v1`;
- discovery workflow run: `32698949654`, success;
- discovery artifact: `9510855695`;
- discovery artifact digest: `sha256:5589e73dcf417122f844d8abe5583d8fa16a848838d206ef6ea4af75c987fb23`;
- analysis runner blob: `0cd94722d2559ab868c58dc46314809a68f4fd3c`;
- analysis branch head before result lock: `bcc4a87ee71201d1014c0020172a13cc9f5e753c`.

While the updated Actions run was queued, the committed deterministic runner was executed against the successful locked discovery artifact to reproduce these numbers. The workflow remains an independent reproduction gate. No third-party raw data are committed.
