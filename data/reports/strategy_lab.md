# Snake26 strategy laboratory — LEGACY POOLED EXPLORATION

**Important:** This legacy diagnostic pools on-arrival trials and actual league
replays. It is NOT valid evidence that a strategy works in the league.
Use [Joined Research](joint_analysis.md) and
[Mode-Separated Replay Behavior](behavior_by_mode.md) instead.
The static reachable-space search is capped: many genuinely different
moves tie at the cap. Thus a very high 'widest-space choice' percentage
does NOT establish that a snake uses a space-maximizing algorithm.

Updated UTC: 2026-11-02T23:40:27+00:00
Unique replays analyzed: **133** (duplicate hashes skipped: 67; unreadable: 0)
Sampling: every **25th** turn per match, not independent observations.

## What the data can and cannot tell us

This is **behavioral observation**, not a live match simulator. Candidate moves use a conservative **static occupancy** approximation: snake tails may vacate, opponents move simultaneously, and outcomes could change. Therefore percentages are descriptive proxies, not guaranteed-safe decisions or win probabilities.

A prerecorded opponent does **not** respond to changes made by our bot; fixed historical moves cannot provide a valid full counterfactual match. To benchmark wins, we need to run live executables against locally available opponents or compare equivalent seed/opponent setups.

## Mixed trial/league samples: diagnostic only

| Group | Sampled moves | Food-nearest choices | Widest-space choices | Clear food/space tradeoffs | Space favored in tradeoffs |
|---|---:|---:|---:|---:|---:|
| Current top-10 | 8319 | 69.9% | 99.5% | 69 | 69.6% |
| Other student bots | 18234 | 71.1% | 99.3% | 209 | 70.8% |
| Built-in benchmarks | 14344 | 87.4% | 99.2% | 102 | 28.4% |

**Interpretation guardrail:** Built-in `~` bots are reported separately. Top-ten means the *latest* Division 1 top-ten ranking, not necessarily the same code version in old seasons. Groups have unequal and possibly biased opponents. Do not infer causation or an optimal policy from this table.

## Individual behavior fingerprints

| Team | Replays | Sampled moves | Food-nearest | Widest-space | Food/space conflicts | Space chosen in conflicts |
|---|---:|---:|---:|---:|---:|---:|
| `421462-alexander-palmer` | 21 | 1632 | 72.7% | 99.4% | 12 | 75.0% |
| `421349-phathutshedzo-mudzanani` | 16 | 1255 | 73.9% | 99.5% | 9 | 55.6% |
| `388828-ngcebo-methula` | 13 | 994 | 69.4% | 99.4% | 10 | 60.0% |
| `413538-lelethuthando-nikelo` | 12 | 935 | 65.6% | 99.4% | 7 | 71.4% |
| `424820-elisha-mundalamo` | 11 | 841 | 69.5% | 99.8% | 7 | 85.7% |
| `403339-david-ndambo` | 9 | 701 | 63.3% | 99.9% | 3 | 100.0% |
| `419926-mphile-nchabeleng` | 9 | 669 | 72.7% | 99.7% | 5 | 80.0% |
| `423239-zeeshaan-bham` | 8 | 603 | 67.5% | 98.8% | 8 | 50.0% |
| `427039-sameeha-miabala` | 5 | 374 | 69.0% | 99.4% | 4 | 75.0% |
| `408501-asher-urison` | 4 | 315 | 67.8% | 99.3% | 4 | 75.0% |
| `388060-tshepang-tshabalala` | 14 | 1077 | 66.7% | 99.5% | 11 | 90.9% |
| `409997-utayan-naidoo` | 12 | 932 | 64.2% | 98.6% | 17 | 52.9% |
| `402334-angile-saho` | 11 | 853 | 74.7% | 99.1% | 15 | 80.0% |
| `408070-collen-mthombeni` | 11 | 847 | 66.6% | 99.1% | 4 | 50.0% |
| `404721-khensani-maluleke` | 10 | 766 | 71.6% | 99.2% | 8 | 50.0% |
| `428954-njabulo-ndlozi` | 9 | 694 | 64.2% | 100.0% | 6 | 100.0% |
| `427064-khodani-netili` | 8 | 615 | 65.9% | 99.5% | 10 | 70.0% |
| `419342-ayeshan-puckree` | 8 | 613 | 63.4% | 99.7% | 3 | 100.0% |
| `406000-mulimisi-rammela` | 8 | 612 | 65.5% | 99.0% | 5 | 40.0% |
| `419636-jason-chen` | 7 | 542 | 71.3% | 100.0% | 7 | 100.0% |
| `408008-bradley-buys` | 7 | 531 | 66.1% | 99.4% | 8 | 75.0% |
| `421538-tshifhiwa-bvumbi` | 6 | 474 | 74.5% | 99.1% | 4 | 50.0% |
| `409987-sbongakonke-shange` | 6 | 473 | 71.5% | 99.8% | 9 | 88.9% |
| `428786-marvellous-sambo` | 6 | 466 | 69.8% | 98.7% | 7 | 28.6% |
| `389160-lwandle-ramanugu` | 6 | 462 | 77.3% | 98.4% | 4 | 50.0% |
| `428464-madalitso-mnqanqeni` | 6 | 459 | 71.8% | 98.4% | 5 | 60.0% |
| `427417-phophi-shavhani` | 6 | 453 | 79.1% | 99.1% | 5 | 100.0% |
| `403501-mashau-mudzanani` | 5 | 385 | 70.7% | 99.7% | 4 | 100.0% |
| `423258-muhammed-dar` | 5 | 384 | 67.7% | 99.4% | 3 | 100.0% |
| `423436-ntobeko-zondi` | 5 | 382 | 65.7% | 99.5% | 2 | 50.0% |

## Observed deaths by cause

Counts are actual `died` replay events, unlike static-space estimates.

| Group | Self-collision | Body collision | Head-to-head | Other |
|---|---:|---:|---:|---:|
| Current top-10 | 23 | 17 | 7 | 0 |
| Other student bots | 85 | 65 | 35 | 0 |
| Built-in benchmarks | 344 | 820 | 508 | 0 |

Use the death causes to decide whether to first test tail-reachability, body-avoidance, or head-to-head threat rules. Compare on equivalent unseen matches, not raw unadjusted death totals.

## Replay-backed tactical situations

A tradeoff means the most food-directed static-free move had a reachable-space estimate at least 10 tiles smaller than another static-free option. Space scores are **bounded probes**, not exact guarantees.

| Replay | Turn | Snake | Body length | Actual move | Food distance after move | Space score (chosen/best) | Favored space? |
|---|---:|---|---:|---|---:|---:|---|
| [`game-75004.rep`](../replays/2026-11-02-045859-season/game-75004.rep.gz) | 1925 | `421462-alexander-palmer` | 235 | UP | 9 | 255/255 | yes |
| [`trials/422453-mauricetshepo-frost/trial-910000.rep`](../replays/2026-11-02-045859-season/trials/422453-mauricetshepo-frost/trial-910000.rep.gz) | 1850 | `422453-mauricetshepo-frost` | 230 | UP | 18 | 250/250 | yes |
| [`game-75006.rep`](../replays/2026-11-02-145901-season/game-75006.rep.gz) | 1925 | `423239-zeeshaan-bham` | 200 | LEFT | 21 | 220/220 | yes |
| [`trials/403501-mashau-mudzanani/trial-912000.rep`](../replays/2026-11-02-145901-season/trials/403501-mashau-mudzanani/trial-912000.rep.gz) | 1575 | `403501-mashau-mudzanani` | 180 | UP | 27 | 200/200 | yes |
| [`game-76004.rep`](../replays/2026-11-02-045859-season/game-76004.rep.gz) | 1600 | `421462-alexander-palmer` | 180 | LEFT | 22 | 200/200 | yes |
| [`trials/403501-mashau-mudzanani/trial-912000.rep`](../replays/2026-11-02-145901-season/trials/403501-mashau-mudzanani/trial-912000.rep.gz) | 1450 | `403501-mashau-mudzanani` | 170 | RIGHT | 22 | 144/144 | yes |
| [`trials/422453-mauricetshepo-frost/trial-911000.rep`](../replays/2026-11-02-045859-season/trials/422453-mauricetshepo-frost/trial-911000.rep.gz) | 1025 | `422453-mauricetshepo-frost` | 160 | DOWN | 21 | 180/180 | yes |
| [`game-71000.rep`](../replays/2026-11-02-045859-season/game-71000.rep.gz) | 1475 | `428786-marvellous-sambo` | 160 | DOWN | 9 | 180/180 | yes |
| [`trials/403501-mashau-mudzanani/trial-912000.rep`](../replays/2026-11-02-145901-season/trials/403501-mashau-mudzanani/trial-912000.rep.gz) | 1100 | `403501-mashau-mudzanani` | 150 | DOWN | 20 | 170/170 | yes |
| [`game-72003.rep`](../replays/2026-11-02-225901-season/game-72003.rep.gz) | 1575 | `421349-phathutshedzo-mudzanani` | 145 | RIGHT | 26 | 165/165 | yes |
| [`game-72003.rep`](../replays/2026-11-02-145901-season/game-72003.rep.gz) | 1500 | `424820-elisha-mundalamo` | 145 | DOWN | 2 | 165/165 | yes |
| [`trials/408008-bradley-buys/trial-911000.rep`](../replays/2026-11-02-225901-season/trials/408008-bradley-buys/trial-911000.rep.gz) | 1100 | `408008-bradley-buys` | 140 | LEFT | 5 | 160/160 | yes |
| [`game-74002.rep`](../replays/2026-11-02-145901-season/game-74002.rep.gz) | 1950 | `427039-sameeha-miabala` | 135 | DOWN | 28 | 155/155 | yes |
| [`game-75004.rep`](../replays/2026-11-02-045859-season/game-75004.rep.gz) | 1175 | `388060-tshepang-tshabalala` | 135 | UP | 21 | 155/155 | yes |
| [`game-76004.rep`](../replays/2026-11-02-045859-season/game-76004.rep.gz) | 1000 | `421462-alexander-palmer` | 130 | LEFT | 16 | 150/150 | yes |
| [`game-76004.rep`](../replays/2026-11-02-045859-season/game-76004.rep.gz) | 1850 | `427064-khodani-netili` | 130 | LEFT | 24 | 150/150 | yes |
| [`game-75000.rep`](../replays/2026-11-02-225901-season/game-75000.rep.gz) | 1250 | `408008-bradley-buys` | 120 | RIGHT | 10 | 140/140 | yes |
| [`game-73001.rep`](../replays/2026-11-02-045859-season/game-73001.rep.gz) | 1050 | `419342-ayeshan-puckree` | 115 | UP | 10 | 135/135 | yes |
| [`game-72007.rep`](../replays/2026-11-01-235859-season/game-72007.rep.gz) | 1275 | `404721-khensani-maluleke` | 115 | RIGHT | 31 | 100/100 | yes |
| [`game-75006.rep`](../replays/2026-11-02-145901-season/game-75006.rep.gz) | 1250 | `389160-lwandle-ramanugu` | 110 | DOWN | 6 | 130/130 | yes |
| [`game-73001.rep`](../replays/2026-11-01-235859-season/game-73001.rep.gz) | 700 | `421462-alexander-palmer` | 105 | RIGHT | 32 | 44/44 | yes |
| [`game-76007.rep`](../replays/2026-11-02-225901-season/game-76007.rep.gz) | 1200 | `419222-asisipho-ngaba` | 100 | DOWN | 25 | 120/120 | yes |
| [`game-73005.rep`](../replays/2026-11-02-225901-season/game-73005.rep.gz) | 925 | `423239-zeeshaan-bham` | 100 | LEFT | 12 | 120/120 | yes |
| [`game-74007.rep`](../replays/2026-11-02-045859-season/game-74007.rep.gz) | 1475 | `406000-mulimisi-rammela` | 100 | LEFT | 26 | 83/83 | yes |

## Historical hypotheses for later investigation (NO implementation yet)

1. **Food-versus-space planner:** Assign each candidate move a weighted score for distance to food and bounded flood-fill space. Compare against current Java bot, using the same fresh seeds.
2. **Danger override:** When a candidate leads to constrained reachable space, temporarily prioritize escape over food; test ablation with/without the override.
3. **Opponent-pressure rule:** Test threat-aware movement when an opponent head is within three toroidal tiles. The current report counts proximity but does not yet recover opponent intent.
4. **Policy imitation experiment:** Use replay states as labeled observations for relative actions, holding out entire matches and seasons for validation. High next-move accuracy alone is *not* proof of better game performance.

Only promote a strategy if it improves **held-out match outcomes** and survival with equivalent opponent setups. Collect more samples before trusting patterns from individual snakes.
