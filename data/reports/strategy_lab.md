# Snake26 strategy laboratory

Updated UTC: 2026-11-01T21:56:06+00:00
Unique replays analyzed: **22** (duplicate hashes skipped: 32; unreadable: 0)
Sampling: every **25th** turn per match, not independent observations.

## What the data can and cannot tell us

This is **behavioral observation**, not a live match simulator. Candidate moves use a conservative **static occupancy** approximation: snake tails may vacate, opponents move simultaneously, and outcomes could change. Therefore percentages are descriptive proxies, not guaranteed-safe decisions or win probabilities.

A prerecorded opponent does **not** respond to changes made by our bot; fixed historical moves cannot provide a valid full counterfactual match. To benchmark wins, we need to run live executables against locally available opponents or compare equivalent seed/opponent setups.

## Current top-ten versus other observed snakes

| Group | Sampled moves | Food-nearest choices | Widest-space choices | Clear food/space tradeoffs | Space favored in tradeoffs |
|---|---:|---:|---:|---:|---:|
| Current top-10 | 1936 | 68.4% | 99.3% | 20 | 55.0% |
| Other student bots | 3468 | 69.0% | 99.4% | 40 | 72.5% |
| Built-in benchmarks | 1391 | 88.4% | 98.8% | 14 | 21.4% |

**Interpretation guardrail:** Built-in `~` bots are reported separately. Top-ten means the *latest* Division 1 top-ten ranking, not necessarily the same code version in old seasons. Groups have unequal and possibly biased opponents. Do not infer causation or an optimal policy from this table.

## Individual behavior fingerprints

| Team | Replays | Sampled moves | Food-nearest | Widest-space | Food/space conflicts | Space chosen in conflicts |
|---|---:|---:|---:|---:|---:|---:|
| `403339-david-ndambo` | 5 | 389 | 64.2% | 100.0% | 1 | 100.0% |
| `388828-ngcebo-methula` | 5 | 388 | 72.4% | 99.7% | 3 | 66.7% |
| `421349-phathutshedzo-mudzanani` | 3 | 235 | 72.3% | 99.1% | 3 | 33.3% |
| `421462-alexander-palmer` | 2 | 157 | 68.5% | 100.0% | 1 | 100.0% |
| `428786-marvellous-sambo` | 2 | 156 | 66.9% | 98.0% | 3 | 33.3% |
| `419342-ayeshan-puckree` | 2 | 154 | 60.1% | 99.3% | 1 | 100.0% |
| `424820-elisha-mundalamo` | 2 | 153 | 70.8% | 98.6% | 2 | 50.0% |
| `427064-khodani-netili` | 2 | 151 | 73.8% | 98.6% | 4 | 50.0% |
| `426895-mpho-ramasakona` | 1 | 79 | 62.2% | 100.0% | 0 | — |
| `427039-sameeha-miabala` | 1 | 74 | 68.6% | 97.1% | 2 | 50.0% |
| `423546-ndabenhle-shabangu` | 3 | 235 | 63.4% | 99.6% | 1 | 100.0% |
| `413538-lelethuthando-nikelo` | 2 | 158 | 69.0% | 100.0% | 1 | 100.0% |
| `419636-jason-chen` | 2 | 157 | 72.8% | 100.0% | 4 | 100.0% |
| `408501-asher-urison` | 2 | 157 | 64.1% | 100.0% | 2 | 100.0% |
| `409997-utayan-naidoo` | 2 | 157 | 62.7% | 100.0% | 1 | 100.0% |
| `420285-kgotlelelo-aphane` | 2 | 157 | 79.1% | 97.3% | 4 | 0.0% |
| `402334-angile-saho` | 2 | 157 | 72.7% | 98.7% | 4 | 100.0% |
| `386901-amanda-huo` | 2 | 156 | 78.4% | 100.0% | 0 | — |
| `403501-mashau-mudzanani` | 2 | 154 | 74.8% | 99.3% | 1 | 100.0% |
| `423436-ntobeko-zondi` | 2 | 152 | 65.3% | 100.0% | 0 | — |
| `429782-maseeha-seedat` | 2 | 152 | 68.5% | 99.3% | 3 | 66.7% |
| `388060-tshepang-tshabalala` | 2 | 152 | 70.5% | 100.0% | 0 | — |
| `423258-muhammed-dar` | 2 | 152 | 67.6% | 100.0% | 2 | 100.0% |
| `423135-mpho-muremi` | 2 | 152 | 63.7% | 99.3% | 3 | 66.7% |
| `404721-khensani-maluleke` | 2 | 151 | 66.4% | 98.0% | 2 | 0.0% |
| `408070-collen-mthombeni` | 2 | 150 | 66.7% | 100.0% | 0 | — |
| `410193-vhugala-makhwathane` | 2 | 149 | 59.4% | 99.3% | 1 | 0.0% |
| `423239-zeeshaan-bham` | 2 | 147 | 67.8% | 97.9% | 3 | 66.7% |
| `421538-tshifhiwa-bvumbi` | 1 | 79 | 71.8% | 98.7% | 2 | 100.0% |
| `409987-sbongakonke-shange` | 1 | 79 | 77.2% | 100.0% | 2 | 100.0% |

## Observed deaths by cause

Counts are actual `died` replay events, unlike static-space estimates.

| Group | Self-collision | Body collision | Head-to-head | Other |
|---|---:|---:|---:|---:|
| Current top-10 | 4 | 5 | 2 | 0 |
| Other student bots | 17 | 19 | 9 | 0 |
| Built-in benchmarks | 36 | 83 | 49 | 0 |

Use the death causes to decide whether to first test tail-reachability, body-avoidance, or head-to-head threat rules. Compare on equivalent unseen matches, not raw unadjusted death totals.

## Replay-backed tactical situations

A tradeoff means the most food-directed static-free move had a reachable-space estimate at least 10 tiles smaller than another static-free option. Space scores are **bounded probes**, not exact guarantees.

| Replay | Turn | Snake | Body length | Actual move | Food distance after move | Space score (chosen/best) | Favored space? |
|---|---:|---|---:|---|---:|---:|---|
| [`game-72003.rep`](../replays/2026-11-01-205859-season/game-72003.rep.gz) | 1875 | `421462-alexander-palmer` | 220 | LEFT | 17 | 240/240 | yes |
| [`trials/388828-ngcebo-methula/trial-912000.rep`](../replays/2026-11-01-205859-season/trials/388828-ngcebo-methula/trial-912000.rep.gz) | 1950 | `388828-ngcebo-methula` | 200 | UP | 17 | 220/220 | yes |
| [`game-72005.rep`](../replays/2026-11-01-205859-season/game-72005.rep.gz) | 1775 | `423239-zeeshaan-bham` | 165 | UP | 2 | 185/185 | yes |
| [`game-71006.rep`](../replays/2026-11-01-205859-season/game-71006.rep.gz) | 1375 | `419342-ayeshan-puckree` | 135 | RIGHT | 18 | 155/155 | yes |
| [`game-72005.rep`](../replays/2026-11-01-205859-season/game-72005.rep.gz) | 1175 | `423239-zeeshaan-bham` | 125 | DOWN | 30 | 145/145 | yes |
| [`game-71051.rep`](../replays/2026-11-01-205859-season/game-71051.rep.gz) | 1850 | `421538-tshifhiwa-bvumbi` | 125 | LEFT | 22 | 145/145 | yes |
| [`trials/403339-david-ndambo/trial-911000.rep`](../replays/2026-11-01-205859-season/trials/403339-david-ndambo/trial-911000.rep.gz) | 775 | `403339-david-ndambo` | 115 | RIGHT | 14 | 135/135 | yes |
| [`game-71007.rep`](../replays/2026-11-01-205859-season/game-71007.rep.gz) | 1175 | `427064-khodani-netili` | 115 | DOWN | 19 | 135/135 | yes |
| [`game-71005.rep`](../replays/2026-11-01-195859-season/game-71005.rep.gz) | 1200 | `419636-jason-chen` | 115 | UP | 23 | 135/135 | yes |
| [`game-71005.rep`](../replays/2026-11-01-195859-season/game-71005.rep.gz) | 1225 | `419636-jason-chen` | 115 | LEFT | 15 | 135/135 | yes |
| [`game-72001.rep`](../replays/2026-11-01-205859-season/game-72001.rep.gz) | 700 | `413538-lelethuthando-nikelo` | 110 | RIGHT | 20 | 130/130 | yes |
| [`game-71007.rep`](../replays/2026-11-01-205859-season/game-71007.rep.gz) | 1125 | `427064-khodani-netili` | 110 | DOWN | 20 | 130/130 | yes |
| [`game-71051.rep`](../replays/2026-11-01-205859-season/game-71051.rep.gz) | 1050 | `421538-tshifhiwa-bvumbi` | 100 | UP | 28 | 120/120 | yes |
| [`game-72000.rep`](../replays/2026-11-01-205859-season/game-72000.rep.gz) | 1725 | `423135-mpho-muremi` | 95 | UP | 24 | 85/85 | yes |
| [`game-72000.rep`](../replays/2026-11-01-205859-season/game-72000.rep.gz) | 1600 | `423135-mpho-muremi` | 90 | LEFT | 20 | 110/110 | yes |
| [`game-71005.rep`](../replays/2026-11-01-195859-season/game-71005.rep.gz) | 1375 | `419926-mphile-nchabeleng` | 90 | UP | 28 | 110/110 | yes |
| [`game-71051.rep`](../replays/2026-11-01-205859-season/game-71051.rep.gz) | 975 | `409987-sbongakonke-shange` | 85 | RIGHT | 9 | 105/105 | yes |
| [`game-71051.rep`](../replays/2026-11-01-205859-season/game-71051.rep.gz) | 1000 | `409987-sbongakonke-shange` | 85 | LEFT | 23 | 66/66 | yes |
| [`game-71007.rep`](../replays/2026-11-01-205859-season/game-71007.rep.gz) | 1950 | `429782-maseeha-seedat` | 85 | UP | 16 | 105/105 | yes |
| [`game-72005.rep`](../replays/2026-11-01-205859-season/game-72005.rep.gz) | 625 | `388828-ngcebo-methula` | 75 | DOWN | 18 | 95/95 | yes |
| [`game-72002.rep`](../replays/2026-11-01-205859-season/game-72002.rep.gz) | 1525 | `408501-asher-urison` | 75 | RIGHT | 19 | 95/95 | yes |
| [`game-71000.rep`](../replays/2026-11-01-205859-season/game-71000.rep.gz) | 650 | `428954-njabulo-ndlozi` | 75 | RIGHT | 24 | 95/95 | yes |
| [`game-72004.rep`](../replays/2026-11-01-205859-season/game-72004.rep.gz) | 525 | `424820-elisha-mundalamo` | 70 | LEFT | 26 | 90/90 | yes |
| [`game-72001.rep`](../replays/2026-11-01-205859-season/game-72001.rep.gz) | 1075 | `423258-muhammed-dar` | 70 | RIGHT | 34 | 90/90 | yes |

## Experiments we can implement and benchmark

1. **Food-versus-space planner:** Assign each candidate move a weighted score for distance to food and bounded flood-fill space. Compare against current Java bot, using the same fresh seeds.
2. **Danger override:** When a candidate leads to constrained reachable space, temporarily prioritize escape over food; test ablation with/without the override.
3. **Opponent-pressure rule:** Test threat-aware movement when an opponent head is within three toroidal tiles. The current report counts proximity but does not yet recover opponent intent.
4. **Policy imitation experiment:** Use replay states as labeled observations for relative actions, holding out entire matches and seasons for validation. High next-move accuracy alone is *not* proof of better game performance.

Only promote a strategy if it improves **held-out match outcomes** and survival with equivalent opponent setups. Collect more samples before trusting patterns from individual snakes.
