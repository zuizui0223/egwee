# CFTQ0356 Bürger landscape I-F estimand gate — 2026-09-25

## Candidate

Programme identity: `P2_CF01_BUERGER_2004`.

Primary source: Christof Bürger (2004), *Die Bedeutung der Landschaftsstruktur für die
Bienendiversität und Bestäubung auf unterschiedlichen räumlichen Skalen*,
doi:10.53846/goediss-1772.

The dissertation directly studies how agricultural landscape structure affects bee communities and
pollination, including a *Brassica napus* seed-set experiment.

## Why this is a real EGWEE candidate

The source reports that:

- landscape composition affects flower-visiting bee diversity/abundance;
- solitary wild bees, bumblebees and honey bees respond at different spatial scales;
- the rapeseed chapter measures seed set under open insect+wind versus wind-only pollination;
- flower-visitor density is linked to seed set, while crop-landscape context also contributes to
  yield variation.

This supplies plausible I and F layers under a source-defined landscape context.

## Why no effect is opened yet

The dissertation contains **five studies/chapters** rather than one obviously shared sampling frame.
The abstract also states that different bee guilds perceive the landscape at different spatial
scales, approximately small scales for solitary wild bees and larger scales for honey bees.

EGWEE therefore cannot choose a guild, radius or chapter after inspecting which relationship is
strongest.

## Frozen estimand gate

No numerical effect is calculated until chapter/publication mapping establishes:

1. the exact landscape/site IDs used in the bee-community chapter(s);
2. the exact landscape/site IDs used in the *Brassica napus* pollination/seed-set chapter;
3. whether those site sets overlap sufficiently for one common I-F programme;
4. one response-free landscape variable;
5. one source-supported radius for that variable;
6. one broad I endpoint on the common site frame;
7. one direct F endpoint on the same frame.

Independent unit = **landscape/site**. Bee observations, nests, flowers, pods, seeds and repeated
samples remain nested below landscape/site.

## Preferred I/F definitions

If a common site frame is recovered:

- I: broad flower-visiting bee abundance/visitation on the fixed landscape exposure;
- F: direct *Brassica napus* seed set / pollination-dependent reproductive output.

Guild-specific responses remain dependent sensitivities unless the source design itself defines
separate independent landscape programmes.

## Terminal outcomes

- `buerger_gradient_IF_covariance_aware`;
- `buerger_chapter_site_overlap_not_recoverable`;
- `buerger_common_landscape_estimand_not_identifiable`;
- `buerger_common_IF_site_frame_not_recoverable`;
- `buerger_site_level_values_not_recoverable`.

## No rescue

Do not:

- choose the bee guild with the strongest published landscape response;
- choose 750 m versus 3000 m by effect size;
- combine bee data from one chapter with seed-set data from a different non-overlapping landscape set;
- count chapters as independent programmes simply because the dissertation contains five studies;
- use crop proportion or semi-natural habitat proportion interchangeably after seeing outcomes;
- treat flowers, nests, pods or seeds as landscape replicates;
- interpret this empirical programme as validation of an EGWE/NEE finite operator.

All terminal outcomes are retained.
