# Eschscholzia post-review F typo sensitivity STOP

## Decision

**`stop_pre_model_unexpected_second_metadata_mismatch`**

The prospective secondary sensitivity was fixed at commit `ae0d70a` before execution. It permitted one and only one key-specific correction: array `1||3`, `Habitat`, `Fallow graound -> Fallow ground`.

Metadata preflight found the declared mismatch at `1||3` and the same cross-source mismatch at a second array, `1||4`. The preregistration required a stop if more than one metadata discrepancy was present. The sensitivity therefore stopped before `_prepare_f`, model fitting, held-out scoring or bootstrap.

## Information boundary

- F model fitted: **no**;
- held-out F score calculated: **no**;
- bootstrap run: **no**;
- G, C or R endpoint rerun: **no**;
- pre-stop fields used from the F source: key fields and `Habitat` only.

No F secondary sensitivity estimate exists. The candidate is not expanded post hoc to repair `1||4`.

## Primary result

The locked primary decision remains **`multi_endpoint_not_identifiable`**. This STOP neither rescues nor weakens the primary provenance rule; it shows that even the narrowly proposed reviewer sensitivity was not executable under its prospective one-key contract.
