# Snake26 strategy laboratory

Updated UTC: 2026-11-01T23:18:18+00:00
Unique replays analyzed: **68** (duplicate hashes skipped: 58; unreadable: 0)
Sampling: every **25th** turn per match, not independent observations.

## What the data can and cannot tell us

This is **behavioral observation**, not a live match simulator. Candidate moves use a conservative **static occupancy** approximation: snake tails may vacate, opponents move simultaneously, and outcomes could change. Therefore percentages are descriptive proxies, not guaranteed-safe decisions or win probabilities.

A prerecorded opponent does **not** respond to changes made by our bot; fixed historical moves cannot provide a valid full counterfactual match. To benchmark wins, we need to run live executables against locally available opponents or compare equivalent seed/opponent setups.

## Current top-ten versus other observed snakes

| Group | Sampled moves | Food-nearest choices | Widest-space choices | Clear food/space tradeoffs | Space favored in tradeoffs |
|---|---:|---:|---:|---:|---:|
| Current top-10 | 3249 | 67.6% | 99.5% | 34 | 70.6% |
| Other student bots | 10054 | 72.2% | 99.4% | 102 | 68.6% |
| Built-in benchmarks | 7629 | 87.8% | 99.2% | 53 | 26.4% |

**Interpretation guardrail:** Built-in `~` bots are reported separately. Top-ten means the *latest* Division 1 top-ten ranking, not necessarily the same code version in old seasons. Groups have unequal and possibly biased opponents. Do not infer causation or an optimal policy from this table.

## Individual behavior fingerprints

| Team | Replays | Sampled moves | Food-nearest | Widest-space | Food/space conflicts | Space chosen in conflicts |
|---|---:|---:|---:|---:|---:|---:|
| `403339-david-ndambo` | 8 | 623 | 62.6% | 100.0% | 3 | 100.0% |
| `413538-lelethuthando-nikelo` | 7 | 546 | 66.6% | 99.8% | 4 | 100.0% |
| `388828-ngcebo-methula` | 7 | 539 | 69.9% | 99.6% | 5 | 80.0% |
| `427064-khodani-netili` | 5 | 381 | 70.1% | 99.2% | 8 | 62.5% |
| `421349-phathutshedzo-mudzanani` | 4 | 314 | 70.6% | 99.3% | 3 | 33.3% |
| `421462-alexander-palmer` | 3 | 236 | 67.4% | 100.0% | 1 | 100.0% |
| `424820-elisha-mundalamo` | 3 | 230 | 70.0% | 99.1% | 3 | 66.7% |
| `428786-marvellous-sambo` | 2 | 156 | 66.9% | 98.0% | 3 | 33.3% |
| `419926-mphile-nchabeleng` | 2 | 150 | 68.3% | 100.0% | 2 | 100.0% |
| `427039-sameeha-miabala` | 1 | 74 | 68.6% | 97.1% | 2 | 50.0% |
| `402334-angile-saho` | 8 | 619 | 74.2% | 99.2% | 11 | 90.9% |
| `408070-collen-mthombeni` | 7 | 534 | 69.1% | 99.4% | 2 | 50.0% |
| `409987-sbongakonke-shange` | 6 | 473 | 71.5% | 99.8% | 9 | 88.9% |
| `409997-utayan-naidoo` | 6 | 466 | 63.7% | 98.7% | 5 | 40.0% |
| `404721-khensani-maluleke` | 6 | 460 | 74.0% | 99.3% | 2 | 0.0% |
| `388060-tshepang-tshabalala` | 5 | 388 | 68.9% | 99.5% | 2 | 50.0% |
| `409598-langelihle-funeka` | 4 | 315 | 90.2% | 100.0% | 4 | 100.0% |
| `423546-ndabenhle-shabangu` | 4 | 314 | 67.4% | 99.7% | 1 | 100.0% |
| `386901-amanda-huo` | 4 | 312 | 76.9% | 99.7% | 4 | 100.0% |
| `419636-jason-chen` | 4 | 308 | 71.5% | 100.0% | 5 | 100.0% |
| `428954-njabulo-ndlozi` | 4 | 308 | 62.6% | 100.0% | 1 | 100.0% |
| `419342-ayeshan-puckree` | 4 | 305 | 63.3% | 99.7% | 1 | 100.0% |
| `405469-adham-soror` | 3 | 237 | 88.7% | 100.0% | 6 | 100.0% |
| `408501-asher-urison` | 3 | 236 | 63.9% | 99.6% | 4 | 75.0% |
| `426895-mpho-ramasakona` | 3 | 235 | 68.1% | 98.2% | 2 | 50.0% |
| `429782-maseeha-seedat` | 3 | 231 | 70.0% | 99.1% | 4 | 50.0% |
| `389160-lwandle-ramanugu` | 3 | 230 | 76.4% | 99.1% | 2 | 50.0% |
| `423135-mpho-muremi` | 3 | 229 | 61.5% | 99.5% | 3 | 66.7% |
| `410193-vhugala-makhwathane` | 3 | 225 | 63.3% | 98.6% | 4 | 25.0% |
| `423239-zeeshaan-bham` | 3 | 223 | 63.6% | 98.6% | 3 | 66.7% |

## Observed deaths by cause

Counts are actual `died` replay events, unlike static-space estimates.

| Group | Self-collision | Body collision | Head-to-head | Other |
|---|---:|---:|---:|---:|
| Current top-10 | 5 | 4 | 3 | 0 |
| Other student bots | 51 | 37 | 17 | 0 |
| Built-in benchmarks | 199 | 435 | 261 | 0 |

Use the death causes to decide whether to first test tail-reachability, body-avoidance, or head-to-head threat rules. Compare on equivalent unseen matches, not raw unadjusted death totals.

## Replay-backed tactical situations

A tradeoff means the most food-directed static-free move had a reachable-space estimate at least 10 tiles smaller than another static-free option. Space scores are **bounded probes**, not exact guarantees.

| Replay | Turn | Snake | Body length | Actual move | Food distance after move | Space score (chosen/best) | Favored space? |
|---|---:|---|---:|---|---:|---:|---|
| [`trials/409997-utayan-naidoo/trial-912000.rep`](../replays/2026-11-01-225859-season/trials/409997-utayan-naidoo/trial-912000.rep.gz) | 1850 | `409997-utayan-naidoo` | 250 | RIGHT | 30 | 184/184 | yes |
| [`game-72003.rep`](../replays/2026-11-01-205859-season/game-72003.rep.gz) | 1875 | `421462-alexander-palmer` | 220 | LEFT | 17 | 240/240 | yes |
| [`trials/388828-ngcebo-methula/trial-912000.rep`](../replays/2026-11-01-205859-season/trials/388828-ngcebo-methula/trial-912000.rep.gz) | 1950 | `388828-ngcebo-methula` | 200 | UP | 17 | 220/220 | yes |
| [`trials/405469-adham-soror/trial-912000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-912000.rep.gz) | 1625 | `405469-adham-soror` | 185 | RIGHT | 15 | 205/205 | yes |
| [`game-71050.rep`](../replays/2026-11-01-225859-season/game-71050.rep.gz) | 1975 | `419636-jason-chen` | 180 | UP | 17 | 72/72 | yes |
| [`trials/402334-angile-saho/trial-912000.rep`](../replays/2026-11-01-205859-season/trials/402334-angile-saho/trial-912000.rep.gz) | 1250 | `402334-angile-saho` | 175 | LEFT | 17 | 195/195 | yes |
| [`game-72005.rep`](../replays/2026-11-01-205859-season/game-72005.rep.gz) | 1775 | `423239-zeeshaan-bham` | 165 | UP | 2 | 185/185 | yes |
| [`game-71054.rep`](../replays/2026-11-01-215859-season/game-71054.rep.gz) | 1500 | `409987-sbongakonke-shange` | 150 | RIGHT | 24 | 170/170 | yes |
| [`trials/405469-adham-soror/trial-912000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-912000.rep.gz) | 1125 | `405469-adham-soror` | 150 | UP | 8 | 170/170 | yes |
| [`game-71000.rep`](../replays/2026-11-01-225859-season/game-71000.rep.gz) | 1275 | `413538-lelethuthando-nikelo` | 145 | RIGHT | 18 | 117/117 | yes |
| [`game-71054.rep`](../replays/2026-11-01-215859-season/game-71054.rep.gz) | 1975 | `421853-mpho-mokoloko` | 130 | UP | 10 | 150/150 | yes |
| [`trials/405469-adham-soror/trial-910000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-910000.rep.gz) | 1575 | `405469-adham-soror` | 130 | UP | 3 | 150/150 | yes |
| [`trials/405469-adham-soror/trial-910000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-910000.rep.gz) | 1650 | `405469-adham-soror` | 130 | RIGHT | 10 | 150/150 | yes |
| [`game-71056.rep`](../replays/2026-11-01-225859-season/game-71056.rep.gz) | 1225 | `408501-asher-urison` | 125 | RIGHT | 14 | 145/145 | yes |
| [`game-72005.rep`](../replays/2026-11-01-205859-season/game-72005.rep.gz) | 1175 | `423239-zeeshaan-bham` | 125 | DOWN | 30 | 145/145 | yes |
| [`trials/405469-adham-soror/trial-912000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-912000.rep.gz) | 925 | `405469-adham-soror` | 120 | DOWN | 11 | 140/140 | yes |
| [`trials/405469-adham-soror/trial-911000.rep`](../replays/2026-11-01-205859-season/trials/405469-adham-soror/trial-911000.rep.gz) | 1900 | `405469-adham-soror` | 115 | RIGHT | 20 | 135/135 | yes |
| [`trials/403339-david-ndambo/trial-911000.rep`](../replays/2026-11-01-205859-season/trials/403339-david-ndambo/trial-911000.rep.gz) | 775 | `403339-david-ndambo` | 115 | RIGHT | 14 | 135/135 | yes |
| [`game-71056.rep`](../replays/2026-11-01-225859-season/game-71056.rep.gz) | 1050 | `400861-sibusisomlungisi-dlamini` | 110 | UP | 18 | 130/130 | yes |
| [`game-71002.rep`](../replays/2026-11-01-225859-season/game-71002.rep.gz) | 1625 | `402334-angile-saho` | 105 | DOWN | 11 | 125/125 | yes |
| [`game-71000.rep`](../replays/2026-11-01-225859-season/game-71000.rep.gz) | 1000 | `388828-ngcebo-methula` | 105 | UP | 23 | 125/125 | yes |
| [`game-71001.rep`](../replays/2026-11-01-215859-season/game-71001.rep.gz) | 1400 | `386901-amanda-huo` | 105 | RIGHT | 28 | 125/125 | yes |
| [`game-71002.rep`](../replays/2026-11-01-225859-season/game-71002.rep.gz) | 1175 | `402334-angile-saho` | 100 | DOWN | 33 | 107/107 | yes |
| [`trials/409598-langelihle-funeka/trial-912000.rep`](../replays/2026-11-01-215859-season/trials/409598-langelihle-funeka/trial-912000.rep.gz) | 775 | `409598-langelihle-funeka` | 100 | RIGHT | 13 | 120/120 | yes |

## Experiments we can implement and benchmark

1. **Food-versus-space planner:** Assign each candidate move a weighted score for distance to food and bounded flood-fill space. Compare against current Java bot, using the same fresh seeds.
2. **Danger override:** When a candidate leads to constrained reachable space, temporarily prioritize escape over food; test ablation with/without the override.
3. **Opponent-pressure rule:** Test threat-aware movement when an opponent head is within three toroidal tiles. The current report counts proximity but does not yet recover opponent intent.
4. **Policy imitation experiment:** Use replay states as labeled observations for relative actions, holding out entire matches and seasons for validation. High next-move accuracy alone is *not* proof of better game performance.

Only promote a strategy if it improves **held-out match outcomes** and survival with equivalent opponent setups. Collect more samples before trusting patterns from individual snakes.
