# Cross-origin minimal bridge — archive access result

## Decision

**`minimal_bridge_not_runnable_from_current_automated_archive_access`**

The four-system visitation–reproduction bridge was preregistered before raw candidate outcomes were inspected by this project. The response-firewalled acquisition audit then stopped before schema mapping or any reproductive-outcome model was fit.

This is an **archive-access boundary**, not evidence for or against an urban–island ecological difference.

## Locked candidates

The frozen candidate set contains two urban and two island archives:

- `U1_commelina` — Ushimaru et al. urban–rural *Commelina communis*, Dryad `10.5061/dryad.pd775`;
- `U2_chicago` — Zink et al. Chicago phytometer study, Dryad `10.5061/dryad.44j0zpcm6`;
- `I1_hiraiwa2017` — Hiraiwa & Ushimaru continental/oceanic island pollination networks, Dryad `10.5061/dryad.pm29d`;
- `I2_hawaii2019` — Aslan et al. Hawaii dryland pollination, Dryad `10.5061/dryad.tm575v4`.

The set was not changed after the access result.

## What was successfully recovered

Dryad anonymous metadata resolved the exact publication version, file identities, paths, sizes and digests for **all four** locked archives. Thus the acquisition target is now immutable and verifiable.

Examples include:

- `U1`: file IDs `40996–40998` for the three declared CSV products;
- `U2`: seven declared products, including `gopro_obs.csv`, `inperson_obs.csv`, plant fruit/flower tables and seed tables;
- `I1`: `primary_data.xlsx`, file ID `45693`, expected size `93,457` bytes;
- `I2`: the visitation workbook and README, file IDs `22438–22439`.

No result-dependent file selection occurred.

## Why automated raw acquisition stopped

The dedicated transport diagnostic (GitHub Actions run `32979406354`) tested the download links exposed by the same metadata without parsing dataset values.

1. The API `stash:download` links are bearer-token protected. Ordinary probes returned HTTP `401 Unauthorized`; later Hawaii probes reached the public API rate limit (`429`) after the earlier metadata requests.
2. Both the current and legacy browser `file_stream` routes returned HTTP `200`, but the returned body was the anti-bot **“Validating...”** HTML page rather than the declared CSV/XLSX/DOCX content.
3. Therefore **0/4 candidates** had a complete usable public byte-stream probe from the GitHub Actions execution environment.

An earlier schema attempt treated HTTP 200 as a transfer success and consequently tried to parse challenge HTML as CSV/XLSX. That attempt is explicitly invalidated; the offending schema auditor and workflow were removed before merge. The later transport diagnostic checks content type/body signature rather than HTTP status alone.

## What can still be established from public source descriptions

Public archive and article descriptions support the *candidate rationale* but are not substituted for raw-data validation:

- the Chicago archive explicitly describes observation duration, flower counts and visit counts plus open/supplement fruit and seed records;
- the *Commelina* study explicitly reports pollinator visit frequency and reproductive success across 12 urban–rural populations;
- the Hiraiwa–Ushimaru island study reports visit frequency and fruit set analyses in the same island network programme;
- the Hawaii archive description identifies its workbook as raw visitation observations, while the publication reports seed-set responses to pollinator exclusion. Whether those reproduction values are synchronized inside the downloadable archive cannot be assumed without the actual bytes.

Accordingly, none of these descriptions is used to declare a schema pass.

## Scientific status

The stronger cross-origin hypothesis remains as fixed after the main identifiability audit:

`P(F_future | S, island) = P(F_future | S, urban)`

is **not identified by the existing Izu/Zurich pair**.

The new four-archive programme has now recovered an additional, narrower boundary:

> Even after origin replication is prospectively improved to two candidate systems per origin, a valid cross-origin analysis still requires synchronized raw process/function measurements whose exact schema can be inspected before outcomes are modeled.

The project does not replace this requirement with article-level effect signs, generic z-scores, or study-specific summary statistics merely because automated file access is blocked.

## Next admissible step

The candidate set and file manifests are frozen. The next analysis may open only when the exact archive bytes are obtained through a legitimate interactive/user-supplied route and verified against the recorded Dryad size/digest metadata.

Then the order is:

1. inspect schema/README only;
2. freeze exact visitation, effort, reproductive-response and join-key mappings;
3. determine whether the same response semantics exist in at least two island and two urban systems;
4. only then open outcome values and run whole-unit held-out prediction;
5. retain the full-state `D/I/T/C/R/G/A` convergence claim as a separate, stronger future test.
