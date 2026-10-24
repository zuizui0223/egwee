# CFTQ0103 southern-Thailand orchard access gate — 2026-09-24

## Decision

CFTQ0103 is a **design-valid direct I-F candidate** but is currently
**quantitatively blocked by orchard-level data recoverability**.

The frozen contract remains `CF01_THAI_ORCHARD_2016_RECOVERY_CONTRACT.md`.

## Design retained

The primary source defines:

- 10 matched mixed-fruit orchard pairs;
- one near-forest orchard (<1 km) and one far-from-forest orchard (>7 km) per pair;
- three mandatory crop panels: rambutan, durian and mango;
- direct flower visitation and fruit-set measurements;
- orchard as the EGWEE fragmentation unit.

The published species-level qualitative results were already visible before recovery. Therefore the
contract forbids choosing only rambutan, replacing forest proximity with cave proximity for durian,
or switching the I/F endpoint after seeing results.

## Public-source audit

### Full article

A public full-text copy is recoverable through UC Berkeley eScholarship. It documents the sampling
design and reports GLMM results plus selected aggregate response summaries.

It does **not** expose the complete orchard-level flower-visitation and fruit-set vectors for all
three mandatory crops that are required to reconstruct:

1. the marginal orchard-level Hedges-g effects on the locked far-versus-near contrast; and
2. the within-crop I-F working covariance on the same independent-unit frame.

Lower-level tree, inflorescence, flower, visit or fruit observations cannot be promoted to orchard n.

### Other public routes

- Cambridge Core confirms the article identity/design but does not expose a raw orchard table.
- Zenodo record **14817704** is publicly indexed, but its attached files are marked **restricted**.
- GitHub DOI/title search yields bibliographic/index records, not an authoritative orchard-level
  source dataset.

No authoritative public source with the complete mandatory three-crop orchard-level I/F frame was
recovered in this audit.

## STOP

Current state:

`design_valid_public_orchard_level_IF_data_not_recoverable`

Consequences:

- direct I-F programme increment: **0**;
- direct I-F coverage remains **1/5 (ML020 only)**;
- no orchard-level effect is calculated;
- no figure digitisation is used;
- published GLMM coefficients/p-values are not reverse-engineered into Hedges g;
- the apparently strongest crop is not selected as a substitute for the complete three-crop
  contract.

This is an **access/recoverability boundary, not an ecological null and not a failed I-F biological
effect**.

Reopen only if an authoritative public or author-provided source exposes orchard-level visitation
and fruit-set values for rambutan, durian and mango under the frozen forest-proximity contract.
