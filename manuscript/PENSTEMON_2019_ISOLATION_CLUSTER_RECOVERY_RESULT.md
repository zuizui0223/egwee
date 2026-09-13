# C07 / candidate ML010 — *Penstemon hirsutus* 2019 recovery result

## Terminal state

`source_parentage_assignments_not_reconstructable`

No quantitative C/G_offspring effect was admitted and the independent cross-system denominator does not increase.

## What the schema gate established

The public data record contains exactly the two microsatellite files expected from the source:

- `NatVsRoof_Microsats_FinalData.csv`: 142 rows × 22 columns, individual/population identifiers plus 10 paired microsatellite loci;
- `Parentage_Microsats_FinalData.csv`: 239 rows × 20 columns, individual/population identifiers plus 9 paired microsatellite loci.

The experimental parentage file contains genotype columns and `popNum`, but no source assignment-output fields such as assigned father, paternity class, LOD, confidence or CERVUS output.

This matches the source data description: the public archive provides microsatellite data, while the article states that other study data are available from the corresponding author on request.

## Why C is not reconstructed

The publication generated paternity classifications with CERVUS 3.0.7 using source-specific maximum-likelihood, confidence and tie-breaking rules. The prospective contract prohibited replacing those source classifications with a newly implemented parentage algorithm after opening the genotype archive.

The publication reports the study-wide summary (`48%` self, `27%` within-roof, `25%` between-roof) and plots roof-level proportions, but it does not publish an exact roof-level assignment/count table from which the locked C endpoint can be reconstructed without figure digitization.

Therefore:

- the source demonstrates realized between-roof pollen movement;
- the exact roof-level C vector required for a ten-roof isolation effect is not recoverable from ordinary public source data;
- nonsignificant site-property tests are not converted to zero effects;
- Figure 4 is not digitized to manufacture the missing roof-level counts.

## G_offspring boundary

The offspring microsatellite file is structurally sufficient to support a roof-level genetic-state reconstruction because it contains population labels and nine diploid loci.

However, the purpose of this recovery gate is an independent **multilayer** C/G_offspring cluster. Once the source-consistent C layer failed before quantitative outcome opening, quantitative genotype values were not mined merely to add another single-layer row. G_offspring is therefore recorded as `structurally_reconstructable_but_not_opened_after_multilayer_gate_failure`.

A future reopening may calculate G only if the source parentage assignments/counts also become available under the same ten-roof frame, or if a separately preregistered synthesis has a legitimate use for single-layer G evidence.

## Design separation retained

The paper's three natural-prairie versus three established-green-roof adult-genetic comparison remains a different design. It can support descriptive or single-layer G_adult evidence but is not joined to the ten experimental roofs to create a synthetic C/G cluster.

## Reopen condition

Reopen ML010 only if an ordinary source route provides one of:

- offspring-level source parentage assignments;
- exact maternal-roof counts for self / within-roof / between-roof paternity under the published classification;
- source code/output sufficient to reproduce those classifications without substituting a new parentage model.

If reopened, the already locked exposure remains `z(mean_distance_to_other_roofs)`, the independent unit remains roof population, and parents/offspring/loci remain nested.

Do not rescue with a new CERVUS implementation, geographic nearest-father assignment, figure digitization, study-wide 25% between-roof pollen flow, or the separate natural-versus-roof design.