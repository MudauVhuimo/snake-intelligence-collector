# Snake26 strategy laboratory

Updated UTC: 2026-11-01T22:18:25+00:00
Unique replays analyzed: **37** (duplicate hashes skipped: 41; unreadable: 0)
Sampling: every **25th** turn per match, not independent observations.

## What the data can and cannot tell us

This is **behavioral observation**, not a live match simulator. Candidate moves use a conservative **static occupancy** approximation: snake tails may vacate, opponents move simultaneously, and outcomes could change. Therefore percentages are descriptive proxies, not guaranteed-safe decisions or win probabilities.

A prerecorded opponent does **not** respond to changes made by our bot; fixed historical moves cannot provide a valid full counterfactual match. To benchmark wins, we need to run live executables against locally available opponents or compare equivalent seed/opponent setups.

## Current top-ten versus other observed snakes

| Group | Sampled moves | Food-nearest choices | Widest-space choices | Clear food/space tradeoffs | Space favored in tradeoffs |
|---|---:|---:|---:|---:|---:|
| Current top-10 | 2166 | 67.8% | 99.4% | 23 | 60.9% |
| Other student bots | 5793 | 71.7% | 99.4% | 63 | 73.0% |
| Built-in benchmarks | 3479 | 87.7% | 98.9% | 39 | 28.2% |

**Interpretation guardrail:** Built-in `~` bots are reported separately. Top-ten means the *latest* Division 1 top-ten ranking, not necessarily the same code version in old seasons. Groups have unequal and possibly biased opponents. Do not infer causation or an optimal policy from this table.

## Individual behavior fingerprints

| Team | Replays | Sampled moves | Food-nearest | Widest-space | Food/space conflicts | Space chosen in conflicts |
|---|---:|---:|---:|---:|---:|---:|
| `388828-ngcebo-methula` | 6 | 463 | 70.7% | 99.8% | 4 | 75.0% |
| `403339-david-ndambo` | 5 | 389 | 64.2% | 100.0% | 1 | 100.0% |
| `421462-alexander-palmer` | 3 | 236 | 67.4% | 100.0% | 1 | 100.0% |
| `421349-phathutshedzo-mudzanani` | 3 | 235 | 72.3% | 99.1% | 3 | 33.3% |
| `427064-khodani-netili` | 3 | 227 | 69.3% | 99.1% | 6 | 66.7% |
| `428786-marvellous-sambo` | 2 | 156 | 66.9% | 98.0% | 3 | 33.3% |
| `419342-ayeshan-puckree` | 2 | 154 | 60.1% | 99.3% | 1 | 100.0% |
| `424820-elisha-mundalamo` | 2 | 153 | 70.8% | 98.6% | 2 | 50.0% |
| `426895-mpho-ramasakona` | 1 | 79 | 62.2% | 100.0% | 0 | — |
| `427039-sameeha-miabala` | 1 | 74 | 68.6% | 97.1% | 2 | 50.0% |
| `402334-angile-saho` | 7 | 540 | 74.5% | 99.0% | 9 | 88.9% |
| `388060-tshepang-tshabalala` | 5 | 388 | 68.9% | 99.5% | 2 | 50.0% |
| `423546-ndabenhle-shabangu` | 4 | 314 | 67.4% | 99.7% | 1 | 100.0% |
| `405469-adham-soror` | 3 | 237 | 88.7% | 100.0% | 6 | 100.0% |
| `386901-amanda-huo` | 3 | 234 | 77.4% | 100.0% | 3 | 100.0% |
| `419636-jason-chen` | 3 | 234 | 70.8% | 100.0% | 4 | 100.0% |
| `429782-maseeha-seedat` | 3 | 231 | 70.0% | 99.1% | 4 | 50.0% |
| `423135-mpho-muremi` | 3 | 229 | 61.5% | 99.5% | 3 | 66.7% |
| `408070-collen-mthombeni` | 3 | 228 | 68.3% | 100.0% | 0 | — |
| `410193-vhugala-makhwathane` | 3 | 225 | 63.3% | 98.6% | 4 | 25.0% |
| `413538-lelethuthando-nikelo` | 2 | 158 | 69.0% | 100.0% | 1 | 100.0% |
| `408501-asher-urison` | 2 | 157 | 64.1% | 100.0% | 2 | 100.0% |
| `409997-utayan-naidoo` | 2 | 157 | 62.7% | 100.0% | 1 | 100.0% |
| `420285-kgotlelelo-aphane` | 2 | 157 | 79.1% | 97.3% | 4 | 0.0% |
| `403501-mashau-mudzanani` | 2 | 154 | 74.8% | 99.3% | 1 | 100.0% |
| `406000-mulimisi-rammela` | 2 | 153 | 63.8% | 98.0% | 2 | 0.0% |
| `423436-ntobeko-zondi` | 2 | 152 | 65.3% | 100.0% | 0 | — |
| `423258-muhammed-dar` | 2 | 152 | 67.6% | 100.0% | 2 | 100.0% |
| `404721-khensani-maluleke` | 2 | 151 | 66.4% | 98.0% | 2 | 0.0% |
| `423239-zeeshaan-bham` | 2 | 147 | 67.8% | 97.9% | 3 | 66.7% |

## Observed deaths by cause

Counts are actual `died` replay events, unlike static-space estimates.

| Group | Self-collision | Body collision | Head-to-head | Other |
|---|---:|---:|---:|---:|
| Current top-10 | 4 | 5 | 2 | 0 |
| Other student bots | 22 | 24 | 13 | 0 |
| Built-in benchmarks | 82 | 209 | 126 | 0 |

Use the death causes to decide whether to first test tail-reachability, body-avoidance, or head-to-head threat rules. Compare on equivalent unseen matches, not raw unadjusted death totals.

## Replay-backed tactical situations

A tradeoff means the most food-directed static-free move had a reachable-space estimate at least 10 tiles smaller than another static-free option. Space scores are **bounded probes**, not exact guarantees.

| Replay | Turn | Snake | Body length | Actual move | Food distance after move | Space score (chosen/best) | Favored space? |
|---|---:|---|---:|---|---:|---:|---|
| [`game-72003.rep`](../replays/2026-11-01-205859-season/game-72003.rep.gz) | 1875 | `421462-alexander-palmer` | 220 | LEFT | 17 | 240/240 | yes |
| [`trials/388828-ngcebo-methula/trial-912000.rep`](../replays/2026-11-01-205859-season/trials/388828-ngcebo-methula/trial-912000.rep.gz) | 1950 | `388828-ngcebo-methula` | 200 | UP | 17 | 220/220 | yes |
| [`trials/405469-adham-soror/trial-912000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-912000.rep.gz) | 1625 | `405469-adham-soror` | 185 | RIGHT | 15 | 205/205 | yes |
| [`trials/402334-angile-saho/trial-912000.rep`](../replays/2026-11-01-205859-season/trials/402334-angile-saho/trial-912000.rep.gz) | 1250 | `402334-angile-saho` | 175 | LEFT | 17 | 195/195 | yes |
| [`game-72005.rep`](../replays/2026-11-01-205859-season/game-72005.rep.gz) | 1775 | `423239-zeeshaan-bham` | 165 | UP | 2 | 185/185 | yes |
| [`trials/405469-adham-soror/trial-912000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-912000.rep.gz) | 1125 | `405469-adham-soror` | 150 | UP | 8 | 170/170 | yes |
| [`game-71006.rep`](../replays/2026-11-01-205859-season/game-71006.rep.gz) | 1375 | `419342-ayeshan-puckree` | 135 | RIGHT | 18 | 155/155 | yes |
| [`trials/405469-adham-soror/trial-910000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-910000.rep.gz) | 1575 | `405469-adham-soror` | 130 | UP | 3 | 150/150 | yes |
| [`trials/405469-adham-soror/trial-910000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-910000.rep.gz) | 1650 | `405469-adham-soror` | 130 | RIGHT | 10 | 150/150 | yes |
| [`game-72005.rep`](../replays/2026-11-01-205859-season/game-72005.rep.gz) | 1175 | `423239-zeeshaan-bham` | 125 | DOWN | 30 | 145/145 | yes |
| [`game-71105.rep`](../replays/2026-11-01-205859-season/game-71105.rep.gz) | 1425 | `419222-asisipho-ngaba` | 125 | LEFT | 31 | 145/145 | yes |
| [`game-71051.rep`](../replays/2026-11-01-205859-season/game-71051.rep.gz) | 1850 | `421538-tshifhiwa-bvumbi` | 125 | LEFT | 22 | 145/145 | yes |
| [`trials/405469-adham-soror/trial-912000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-912000.rep.gz) | 925 | `405469-adham-soror` | 120 | DOWN | 11 | 140/140 | yes |
| [`trials/405469-adham-soror/trial-911000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-911000.rep.gz) | 1900 | `405469-adham-soror` | 115 | RIGHT | 20 | 135/135 | yes |
| [`trials/403339-david-ndambo/trial-911000.rep`](../replays/2026-11-01-205859-season/trials/403339-david-ndambo/trial-911000.rep.gz) | 775 | `403339-david-ndambo` | 115 | RIGHT | 14 | 135/135 | yes |
| [`game-71007.rep`](../replays/2026-11-01-205859-season/game-71007.rep.gz) | 1175 | `427064-khodani-netili` | 115 | DOWN | 19 | 135/135 | yes |
| [`game-71005.rep`](../replays/2026-11-01-195859-season/game-71005.rep.gz) | 1200 | `419636-jason-chen` | 115 | UP | 23 | 135/135 | yes |
| [`game-71005.rep`](../replays/2026-11-01-195859-season/game-71005.rep.gz) | 1225 | `419636-jason-chen` | 115 | LEFT | 15 | 135/135 | yes |
| [`game-72001.rep`](../replays/2026-11-01-205859-season/game-72001.rep.gz) | 700 | `413538-lelethuthando-nikelo` | 110 | RIGHT | 20 | 130/130 | yes |
| [`game-71007.rep`](../replays/2026-11-01-205859-season/game-71007.rep.gz) | 1125 | `427064-khodani-netili` | 110 | DOWN | 20 | 130/130 | yes |
| [`game-72007.rep`](../replays/2026-11-01-205859-season/game-72007.rep.gz) | 1250 | `410193-vhugala-makhwathane` | 100 | DOWN | 29 | 120/120 | yes |
| [`game-71051.rep`](../replays/2026-11-01-205859-season/game-71051.rep.gz) | 1050 | `421538-tshifhiwa-bvumbi` | 100 | UP | 28 | 120/120 | yes |
| [`game-71005.rep`](../replays/2026-11-01-205859-season/game-71005.rep.gz) | 1100 | `427064-khodani-netili` | 100 | DOWN | 12 | 120/120 | yes |
| [`game-72000.rep`](../replays/2026-11-01-205859-season/game-72000.rep.gz) | 1725 | `423135-mpho-muremi` | 95 | UP | 24 | 85/85 | yes |

## Experiments we can implement and benchmark

1. **Food-versus-space planner:** Assign each candidate move a weighted score for distance to food and bounded flood-fill space. Compare against current Java bot, using the same fresh seeds.
2. **Danger override:** When a candidate leads to constrained reachable space, temporarily prioritize escape over food; test ablation with/without the override.
3. **Opponent-pressure rule:** Test threat-aware movement when an opponent head is within three toroidal tiles. The current report counts proximity but does not yet recover opponent intent.
4. **Policy imitation experiment:** Use replay states as labeled observations for relative actions, holding out entire matches and seasons for validation. High next-move accuracy alone is *not* proof of better game performance.

Only promote a strategy if it improves **held-out match outcomes** and survival with equivalent opponent setups. Collect more samples before trusting patterns from individual snakes.
