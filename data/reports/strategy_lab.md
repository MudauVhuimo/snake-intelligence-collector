# Snake26 strategy laboratory

Updated UTC: 2026-11-01T21:41:01+00:00
Replays analyzed: **30** (unreadable: 0)
Sampling: every **25th** turn per match, not independent observations.

## What the data can and cannot tell us

This is **behavioral observation**, not a live match simulator. Candidate moves use a conservative **static occupancy** approximation: snake tails may vacate, opponents move simultaneously, and outcomes could change. Therefore percentages are descriptive proxies, not guaranteed-safe decisions or win probabilities.

A prerecorded opponent does **not** respond to changes made by our bot; fixed historical moves cannot provide a valid full counterfactual match. To benchmark wins, we need to run live executables against locally available opponents or compare equivalent seed/opponent setups.

## Current top-ten versus other observed snakes

| Group | Sampled moves | Food-nearest choices | Widest-space choices | Clear food/space tradeoffs | Space favored in tradeoffs |
|---|---:|---:|---:|---:|---:|
| Current top-10 | 2929 | 68.0% | 99.1% | 31 | 48.4% |
| Other observed | 6277 | 66.6% | 99.5% | 63 | 61.9% |

**Interpretation guardrail:** Top-ten means the *latest* Division 1 top-ten ranking, not necessarily the same code version in old seasons. Groups have unequal and possibly biased opponents. Do not infer causation or an optimal policy from this table.

## Individual behavior fingerprints

| Team | Replays | Sampled moves | Food-nearest | Widest-space | Food/space conflicts | Space chosen in conflicts |
|---|---:|---:|---:|---:|---:|---:|
| `388828-ngcebo-methula` | 7 | 532 | 69.9% | 100.0% | 0 | — |
| `421349-phathutshedzo-mudzanani` | 5 | 392 | 73.2% | 98.9% | 6 | 33.3% |
| `428786-marvellous-sambo` | 4 | 312 | 66.9% | 98.0% | 6 | 33.3% |
| `419342-ayeshan-puckree` | 4 | 308 | 60.1% | 99.3% | 2 | 100.0% |
| `424820-elisha-mundalamo` | 4 | 305 | 70.4% | 97.9% | 4 | 25.0% |
| `426895-mpho-ramasakona` | 3 | 237 | 62.2% | 100.0% | 0 | — |
| `421462-alexander-palmer` | 3 | 235 | 68.2% | 100.0% | 1 | 100.0% |
| `427064-khodani-netili` | 3 | 229 | 73.8% | 99.1% | 6 | 66.7% |
| `427039-sameeha-miabala` | 3 | 222 | 68.6% | 97.1% | 6 | 50.0% |
| `403339-david-ndambo` | 2 | 157 | 61.8% | 100.0% | 0 | — |
| `423258-muhammed-dar` | 9 | 674 | 65.5% | 100.0% | 4 | 100.0% |
| `410193-vhugala-makhwathane` | 9 | 668 | 62.4% | 98.9% | 7 | 0.0% |
| `428954-njabulo-ndlozi` | 7 | 539 | 65.8% | 100.0% | 7 | 100.0% |
| `409997-utayan-naidoo` | 5 | 393 | 63.5% | 100.0% | 2 | 100.0% |
| `423546-ndabenhle-shabangu` | 5 | 391 | 62.8% | 99.7% | 1 | 100.0% |
| `408501-asher-urison` | 4 | 314 | 64.1% | 100.0% | 4 | 100.0% |
| `403501-mashau-mudzanani` | 4 | 308 | 74.1% | 99.7% | 1 | 100.0% |
| `429782-maseeha-seedat` | 4 | 304 | 68.5% | 99.3% | 6 | 66.7% |
| `388060-tshepang-tshabalala` | 4 | 304 | 70.5% | 100.0% | 0 | — |
| `423135-mpho-muremi` | 4 | 304 | 63.7% | 99.3% | 6 | 66.7% |
| `408070-collen-mthombeni` | 4 | 298 | 66.0% | 100.0% | 0 | — |
| `413538-lelethuthando-nikelo` | 3 | 237 | 70.3% | 100.0% | 2 | 100.0% |
| `420285-kgotlelelo-aphane` | 3 | 236 | 77.5% | 97.3% | 6 | 0.0% |
| `423436-ntobeko-zondi` | 3 | 228 | 62.9% | 100.0% | 0 | — |
| `404721-khensani-maluleke` | 3 | 226 | 66.4% | 98.2% | 3 | 0.0% |
| `419636-jason-chen` | 2 | 157 | 72.8% | 100.0% | 4 | 100.0% |
| `402334-angile-saho` | 2 | 157 | 72.7% | 98.7% | 4 | 100.0% |
| `406000-mulimisi-rammela` | 2 | 154 | 64.5% | 98.7% | 2 | 0.0% |
| `423239-zeeshaan-bham` | 2 | 152 | 64.4% | 97.3% | 2 | 0.0% |
| `386901-amanda-huo` | 1 | 79 | 74.7% | 100.0% | 0 | — |

## Observed deaths by cause

Counts are actual `died` replay events, unlike static-space estimates.

| Group | Self-collision | Body collision | Head-to-head | Other |
|---|---:|---:|---:|---:|
| Current top-10 | 4 | 4 | 2 | 0 |
| Other observed | 15 | 16 | 8 | 0 |

Use the death causes to decide whether to first test tail-reachability, body-avoidance, or head-to-head threat rules. Compare on equivalent unseen matches, not raw unadjusted death totals.

## Replay-backed tactical situations

A tradeoff means the most food-directed static-free move had a reachable-space estimate at least 10 tiles smaller than another static-free option. Space scores are **bounded probes**, not exact guarantees.

| Replay | Turn | Snake | Body length | Actual move | Food distance after move | Space score (chosen/best) | Favored space? |
|---|---:|---|---:|---|---:|---:|---|
| [`game-72003.rep`](../replays/2026-11-01-205859-season/game-72003.rep.gz) | 1875 | `421462-alexander-palmer` | 220 | LEFT | 17 | 240/240 | yes |
| [`game-71006.rep`](../replays/2026-11-01-205859-season/game-71006.rep.gz) | 1375 | `419342-ayeshan-puckree` | 135 | RIGHT | 18 | 155/155 | yes |
| [`game-71006.rep`](../replays/2026-11-01-195859-season/game-71006.rep.gz) | 1375 | `419342-ayeshan-puckree` | 135 | RIGHT | 18 | 155/155 | yes |
| [`game-71007.rep`](../replays/2026-11-01-205859-season/game-71007.rep.gz) | 1175 | `427064-khodani-netili` | 115 | DOWN | 19 | 135/135 | yes |
| [`game-71005.rep`](../replays/2026-11-01-195859-season/game-71005.rep.gz) | 1200 | `419636-jason-chen` | 115 | UP | 23 | 135/135 | yes |
| [`game-71005.rep`](../replays/2026-11-01-195859-season/game-71005.rep.gz) | 1225 | `419636-jason-chen` | 115 | LEFT | 15 | 135/135 | yes |
| [`game-71007.rep`](../replays/2026-10-18-235859-season/game-71007.rep.gz) | 1175 | `427064-khodani-netili` | 115 | DOWN | 19 | 135/135 | yes |
| [`game-72001.rep`](../replays/2026-11-01-205859-season/game-72001.rep.gz) | 700 | `413538-lelethuthando-nikelo` | 110 | RIGHT | 20 | 130/130 | yes |
| [`game-71007.rep`](../replays/2026-11-01-205859-season/game-71007.rep.gz) | 1125 | `427064-khodani-netili` | 110 | DOWN | 20 | 130/130 | yes |
| [`game-72001.rep`](../replays/2026-11-01-195859-season/game-72001.rep.gz) | 700 | `413538-lelethuthando-nikelo` | 110 | RIGHT | 20 | 130/130 | yes |
| [`game-71007.rep`](../replays/2026-10-18-235859-season/game-71007.rep.gz) | 1125 | `427064-khodani-netili` | 110 | DOWN | 20 | 130/130 | yes |
| [`game-72000.rep`](../replays/2026-11-01-205859-season/game-72000.rep.gz) | 1725 | `423135-mpho-muremi` | 95 | UP | 24 | 85/85 | yes |
| [`game-72000.rep`](../replays/2026-10-14-133830-season/game-72000.rep.gz) | 1725 | `423135-mpho-muremi` | 95 | UP | 24 | 85/85 | yes |
| [`game-72000.rep`](../replays/2026-11-01-205859-season/game-72000.rep.gz) | 1600 | `423135-mpho-muremi` | 90 | LEFT | 20 | 110/110 | yes |
| [`game-71005.rep`](../replays/2026-11-01-195859-season/game-71005.rep.gz) | 1375 | `419926-mphile-nchabeleng` | 90 | UP | 28 | 110/110 | yes |
| [`game-72000.rep`](../replays/2026-10-14-133830-season/game-72000.rep.gz) | 1600 | `423135-mpho-muremi` | 90 | LEFT | 20 | 110/110 | yes |
| [`game-71007.rep`](../replays/2026-11-01-205859-season/game-71007.rep.gz) | 1950 | `429782-maseeha-seedat` | 85 | UP | 16 | 105/105 | yes |
| [`game-71007.rep`](../replays/2026-10-18-235859-season/game-71007.rep.gz) | 1950 | `429782-maseeha-seedat` | 85 | UP | 16 | 105/105 | yes |
| [`game-72002.rep`](../replays/2026-11-01-205859-season/game-72002.rep.gz) | 1525 | `408501-asher-urison` | 75 | RIGHT | 19 | 95/95 | yes |
| [`game-71000.rep`](../replays/2026-11-01-205859-season/game-71000.rep.gz) | 650 | `428954-njabulo-ndlozi` | 75 | RIGHT | 24 | 95/95 | yes |
| [`game-72002.rep`](../replays/2026-11-01-195859-season/game-72002.rep.gz) | 1525 | `408501-asher-urison` | 75 | RIGHT | 19 | 95/95 | yes |
| [`game-71000.rep`](../replays/2026-10-14-155859-season/game-71000.rep.gz) | 650 | `428954-njabulo-ndlozi` | 75 | RIGHT | 24 | 95/95 | yes |
| [`game-71000.rep`](../replays/2026-10-14-145859-season/game-71000.rep.gz) | 650 | `428954-njabulo-ndlozi` | 75 | RIGHT | 24 | 95/95 | yes |
| [`game-71000.rep`](../replays/2026-10-14-135857-season/game-71000.rep.gz) | 650 | `428954-njabulo-ndlozi` | 75 | RIGHT | 24 | 95/95 | yes |

## Experiments we can implement and benchmark

1. **Food-versus-space planner:** Assign each candidate move a weighted score for distance to food and bounded flood-fill space. Compare against current Java bot, using the same fresh seeds.
2. **Danger override:** When a candidate leads to constrained reachable space, temporarily prioritize escape over food; test ablation with/without the override.
3. **Opponent-pressure rule:** Test threat-aware movement when an opponent head is within three toroidal tiles. The current report counts proximity but does not yet recover opponent intent.
4. **Policy imitation experiment:** Use replay states as labeled observations for relative actions, holding out entire matches and seasons for validation. High next-move accuracy alone is *not* proof of better game performance.

Only promote a strategy if it improves **held-out match outcomes** and survival with equivalent opponent setups. Collect more samples before trusting patterns from individual snakes.
