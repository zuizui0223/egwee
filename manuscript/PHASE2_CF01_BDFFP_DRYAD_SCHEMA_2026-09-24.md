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
