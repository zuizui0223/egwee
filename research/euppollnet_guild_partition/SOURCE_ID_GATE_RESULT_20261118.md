# Corrected EuPPollNet original source + guild-ID coverage gate — 2026-11-18

## Stage A: official author-source schema PASS (before signed guild results)

- Source commit: \`joseblanuza/EuPPollNet@31716d21d5aad8c27c1d91dd0620149ef42e8836\`.
- Published correction: Lanuza et al. (2025), \`10.1111/geb.70054\`. The ORIGINAL 1,162,109 interaction count was incorrect; corrected dataset recovered exactly **623,476 source interaction rows**.
- Three original files received from immutable GitHub raw URLs, their full bytes SHA256 pinned and original row counts checked, without interpreting values:
  - \`Interaction_data.csv.gz\` — 623,476 rows, original SHA256 \`6e4e5399338d530462d8683b53a5e564d48e287e423be420c07d8046815ef38a\`; UTF-8 fails lossless decoding, original file is readable with lossless \`latin-1\` fallback.
  - \`Flower_counts.csv\` — **199,692** records, SHA256 \`aaf0474d42ca477e20db75205191f9e64fcd19f78c3e75ae3d66df77a1cefb0a\`, lossless \`cp1252\` fallback.
  - \`Metadata.csv\` — **80** rows, SHA256 \`adb396f31e7e7e3257425872b92d56c1051ca05849c6228a39675a71364d4833\`, UTF-8 BOM.
- Identical source header/unit contracts validated by original-source CI https://github.com/zuizui0223/egwee/actions/runs/44222755823.

## Stage B: study/network ID and guild eligibility PASS (effects not inspected)

An independent next CI stage, https://github.com/zuizui0223/egwee/actions/runs/44223447301, confirmed:
- **54** source study identifiers, collapsed to **52** biological source programmes by clustering IDs 23–25 as one source.
- **1,864** unique native study×network×year keys (matches corrected source paper); **0** networks had mixed/ambiguous sampling-method keys.
- **129,915** source interaction rows classified as wild bees, **39,652** as syrphid hoverflies, **453,909** as nonfocal or unclassified. Honeybee \`Apis mellifera\` is excluded from the wild-bee category.
- **311** networks satisfy frozen structural eligibility: at least 20 wild-bee and 20 syrphid visits, and at least 3 pooled plant taxa, inside one original survey network. The number of source programmes among these networks will be reported with main result; don't treat all 52 as eligible unless confirmed.
- The source \`Interaction\` field passed its exact single-record interpretation guard: **no flagged non-unit focal interactions**, and no missing site/year keys were reported. Source rows and fitted network effects have **not** been redistributed or computed in these gate stages.

The above guild row cardinalities are *measurement coverage*, not independent community replicates or ecological effect signs. Source plant/guild counts were inspected only for frozen eligibility after the protocol commit \`bb9b3607\`; JSD effects and bootstrap signs were not opened.

## Next execution contract

Now that the source and identity gates pass, run the previously frozen 199-iteration within-network multivariate-hypergeometric shuffle-null JSD correction, then equal-programme estimation and 2,000 programme bootstraps. Interpret only observed floral-visitor guild partition, not natural pollen transfer/seed production. The independent flower census is available but heterogeneous in methods and is *not part of the main null*.

No inference about functional transfer to seed set or the unrelated theory egwe is possible here.
