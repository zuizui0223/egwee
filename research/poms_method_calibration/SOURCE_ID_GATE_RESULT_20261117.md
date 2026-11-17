# PoMS source-exact same-site same-date gate — 2026-11-17

**Verified PASS before any bee, hoverfly or flower-count outcome fields were accessed.**

- GitHub Actions: https://github.com/zuizui0223/egwee/actions/runs/44011755768
- Source dataset DOIs: `10.5285/5841bfae-471b-498c-af89-c30e5140d6c5` (pan) and `10.5285/d706088c-9d48-4be5-b156-6ed6ad5e0618` (FIT).
- Source exact site key = (`country`, `sample_projection`, `x1km_square`), exact date = original `date` string. No fuzzy coordinates or temporal tolerance. The two sources share these named fields.
- Source sample-level IDs: pan 7,050 unique, 1-km FIT 3,053 unique; all location/date/year keys complete.
- Pan 1,422 distinct site×date events, FIT 1,263; intersection **1,221** (unmatched pan 201; unmatched FIT 42).
- Intersected events span **95 distinct site keys**, 2017–2023: `121,126,193,80,212,241,248` matches by year respectively.
- **6,056** pan trap sample rows and **2,985** 1-km FIT observation rows lie in matched site-date events. Pan trap samples per event 1–6; FIT 1–10.
- Source insect occurrence foreign keys: **24,175/24,175** match a pan sample. Pan flower occurrence: **12,847/12,858** match a pan sample; **11 orphan flower rows** cannot be joined and must be excluded from flower-exposure calculation.
- Frozen coverage thresholds of >=20 sites, >=80 site-dates, >=3 years all passed *without inspecting bee/fly counts, floral metric values or effect signs*.

## Source integrity: dynamically regenerated EIDC ZIP wrapper

The published ZIP wrapper SHA256 changes on repeated requests without changes to declared CSV member sizes or row counts. Therefore stable source identity is locked at **SHA256 of each uncompressed original CSV member**, not the dynamic ZIP wrapper. On a new source download any member mismatch fails closed.

- pan samples: `70f3429e5ed9022d3d7b80fc3f24c589ecc5faff608393bc53febfac49788277`
- pan insects: `2423bc370f388a0dafd05c4bd3a7af7491909311ffe6bf4d6607a3697213dcb9`
- pan flowers: `53daa167282092b7081190de00e020b4e2635fa5e7d4fc63d3454f7c338951ba`
- 1-km FIT: `29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52`
- public FIT (excluded from paired analysis): `bcd2ef780d3208a5a4aba5c191178900ccef705e5b569dc0160b27d00652dc3c`

The initial ZIP-hash-only access STOP runs (44011587491, 44011694179) were **file-packaging identity problems**, not biological errors or failed site matching. Their logs are retained; no outcome-search repair was performed.

## Next gated computation

The site-date crosswalk has passed. Freeze outcome definitions, structural-zero handling, site-year terms and site-block confidence interval *before opening numeric count fields*. Do not read the self-selected public FIT rows for effect modeling. Preserve published raw source files outside the repository; upload derivative output only.
