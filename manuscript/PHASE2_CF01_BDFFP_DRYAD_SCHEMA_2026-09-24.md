# CFTQ0065 BDFFP Dryad schema gate — 2026-09-24

## Source

- article: doi:10.1002/eap.2093
- public data: doi:10.5061/dryad.612jm640h
- Dryad version: **3** (id=None)
- recovery contract: `CF01_BDFFP_SEED_RAIN_2020_RECOVERY_CONTRACT.md`

This gate uses Dryad's public metadata plus per-file public download routes. It inspects
workbook structure and exposure/unit identifiers only; it does not summarize response values.

## Archive result

- public files indexed: **4**
- all four declared workbooks present in public metadata: **yes**
- public file-byte access: **blocked**
- plot identifier hint present in recovered schema: **not-yet-readable**
- fragment exposure hint present in recovered schema: **not-yet-readable**
- dispersed-seed endpoint file indexed: **yes**
- undispersed-seed endpoint file indexed: **yes**
- numerical EGWEE effect calculation opened: **false**

## Access STOP

Dryad public metadata exposes the expected file identities, but the public byte-download
routes available to the workflow return access failures. This is an **access/recoverability
boundary, not an ecological null and not a failed C-F result**.

No figure digitisation, published fold-change substitution, endpoint substitution,
authentication bypass, or lower-level pseudo-replication is used to rescue the programme.
Reopen only if Dryad public file bytes become reproducibly available or an authoritative
public mirror of the same deposited files is identified.

## Indexed files

- `density.rich.data.xlsx`: id=None; declared bytes=13432
- `dispersed.matrix.xlsx`: id=None; declared bytes=32978
- `functional.diversity.xlsx`: id=None; declared bytes=10658
- `undispersed.matrix.xlsx`: id=None; declared bytes=34985

## Gate

Proceed to numerical recovery only if the public workbooks support all of:

1. exactly the source plot frame can be reconstructed without using traps as n;
2. fragment/control status is joined before opening endpoint values;
3. dispersed and undispersed density are available on the same plot frame;
4. the frozen all-fragment-versus-continuous contrast can be calculated without
   selecting fragment sizes or response subsets from outcomes.

Otherwise retain the programme as design-valid but quantitatively blocked.

## 17 October 2026 public access recheck

The published Dryad public landing page remains available and still indexes all **four** declared workbooks for Hooper & Ashton (2020), https://doi.org/10.5061/dryad.612jm640h. A renewed ordinary public-file access check (no credentials, scraping bypass or alternate outcome extraction) on 2026-10-17 reached the file stream links but received **HTTP 403 Forbidden** for the relevant density, dispersed and undispersed spreadsheet streams (visible file stream references 243392, 243394, 243395). The unmodified dataset page still lists the workbooks with declared sizes.

**Terminal gate remains unchanged:** `blocked_public_dryad_file_bytes_not_recoverable`. No source workbook values were read; no plot-level Hedges-g/C–F covariance was computed, no abstract-level 3×/6× fold changes were substituted for plot effects, and the 11 independent plot units remain a *prospective design* rather than an EGWEE admitted quantitative family. This recheck does **not** reopen the completed CF01 search or revise the frozen 2/5 direct C–F programme count. Reopen only after reproducible direct public bytes or an authoritative public archive mirror for the exact deposited files can be verified.
