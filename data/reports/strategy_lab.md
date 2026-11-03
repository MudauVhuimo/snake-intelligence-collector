# Snake26 strategy laboratory — LEGACY POOLED EXPLORATION

**Important:** This legacy diagnostic pools on-arrival trials and actual league
replays. It is NOT valid evidence that a strategy works in the league.
Use [Joined Research](joint_analysis.md) and
[Mode-Separated Replay Behavior](behavior_by_mode.md) instead.
The static reachable-space search is capped: many genuinely different
moves tie at the cap. Thus a very high 'widest-space choice' percentage
does NOT establish that a snake uses a space-maximizing algorithm.

Updated UTC: 2026-11-03T04:07:20+00:00
Unique replays analyzed: **141** (duplicate hashes skipped: 69; unreadable: 0)
Sampling: every **25th** turn per match, not independent observations.

## What the data can and cannot tell us

This is **behavioral observation**, not a live match simulator. Candidate moves use a conservative **static occupancy** approximation: snake tails may vacate, opponents move simultaneously, and outcomes could change. Therefore percentages are descriptive proxies, not guaranteed-safe decisions or win probabilities.

A prerecorded opponent does **not** respond to changes made by our bot; fixed historical moves cannot provide a valid full counterfactual match. To benchmark wins, we need to run live executables against locally available opponents or compare equivalent seed/opponent setups.

## Mixed trial/league samples: diagnostic only

| Group | Sampled moves | Food-nearest choices | Widest-space choices | Clear food/space tradeoffs | Space favored in tradeoffs |
|---|---:|---:|---:|---:|---:|
| Current top-10 | 7949 | 68.8% | 99.4% | 80 | 67.5% |
| Other student bots | 20139 | 71.4% | 99.3% | 225 | 70.2% |
| Built-in benchmarks | 15274 | 87.3% | 99.2% | 107 | 28.0% |

**Interpretation guardrail:** Built-in `~` bots are reported separately. Top-ten means the *latest* Division 1 top-ten ranking, not necessarily the same code version in old seasons. Groups have unequal and possibly biased opponents. Do not infer causation or an optimal policy from this table.

## Individual behavior fingerprints

| Team | Replays | Sampled moves | Food-nearest | Widest-space | Food/space conflicts | Space chosen in conflicts |
|---|---:|---:|---:|---:|---:|---:|
| `421462-alexander-palmer` | 25 | 1943 | 72.5% | 99.3% | 20 | 65.0% |
| `413538-lelethuthando-nikelo` | 13 | 1013 | 65.7% | 99.5% | 9 | 77.8% |
| `424820-elisha-mundalamo` | 13 | 992 | 70.3% | 99.7% | 10 | 80.0% |
| `427064-khodani-netili` | 10 | 772 | 66.7% | 99.6% | 12 | 75.0% |
| `404721-khensani-maluleke` | 10 | 766 | 71.6% | 99.2% | 8 | 50.0% |
| `403339-david-ndambo` | 9 | 701 | 63.3% | 99.9% | 3 | 100.0% |
| `419342-ayeshan-puckree` | 8 | 613 | 63.4% | 99.7% | 3 | 100.0% |
| `428786-marvellous-sambo` | 6 | 466 | 69.8% | 98.7% | 7 | 28.6% |
| `427039-sameeha-miabala` | 5 | 374 | 69.0% | 99.4% | 4 | 75.0% |
| `429782-maseeha-seedat` | 4 | 309 | 70.9% | 99.0% | 4 | 50.0% |
| `421349-phathutshedzo-mudzanani` | 16 | 1255 | 73.9% | 99.5% | 9 | 55.6% |
| `388060-tshepang-tshabalala` | 15 | 1150 | 66.0% | 99.5% | 13 | 84.6% |
| `388828-ngcebo-methula` | 13 | 994 | 69.4% | 99.4% | 10 | 60.0% |
| `409997-utayan-naidoo` | 12 | 932 | 64.2% | 98.6% | 17 | 52.9% |
| `402334-angile-saho` | 12 | 926 | 74.1% | 99.0% | 17 | 70.6% |
| `408070-collen-mthombeni` | 12 | 923 | 66.8% | 99.2% | 4 | 50.0% |
| `428954-njabulo-ndlozi` | 9 | 694 | 64.2% | 100.0% | 6 | 100.0% |
| `406000-mulimisi-rammela` | 9 | 689 | 65.1% | 99.1% | 5 | 40.0% |
| `419926-mphile-nchabeleng` | 9 | 669 | 72.7% | 99.7% | 5 | 80.0% |
| `389160-lwandle-ramanugu` | 8 | 613 | 79.3% | 98.5% | 4 | 50.0% |
| `423239-zeeshaan-bham` | 8 | 603 | 67.5% | 98.8% | 8 | 50.0% |
| `419636-jason-chen` | 7 | 542 | 71.3% | 100.0% | 7 | 100.0% |
| `408008-bradley-buys` | 7 | 531 | 66.1% | 99.4% | 8 | 75.0% |
| `421538-tshifhiwa-bvumbi` | 6 | 474 | 74.5% | 99.1% | 4 | 50.0% |
| `409987-sbongakonke-shange` | 6 | 473 | 71.5% | 99.8% | 9 | 88.9% |
| `423436-ntobeko-zondi` | 6 | 460 | 65.3% | 99.5% | 3 | 66.7% |
| `428464-madalitso-mnqanqeni` | 6 | 459 | 71.8% | 98.4% | 5 | 60.0% |
| `427417-phophi-shavhani` | 6 | 453 | 79.1% | 99.1% | 5 | 100.0% |
| `410193-vhugala-makhwathane` | 6 | 450 | 64.0% | 99.1% | 9 | 55.6% |
| `408501-asher-urison` | 5 | 393 | 68.8% | 99.2% | 6 | 66.7% |

## Observed deaths by cause

Counts are actual `died` replay events, unlike static-space estimates.

| Group | Self-collision | Body collision | Head-to-head | Other |
|---|---:|---:|---:|---:|
| Current top-10 | 26 | 16 | 10 | 0 |
| Other student bots | 89 | 76 | 36 | 0 |
| Built-in benchmarks | 361 | 854 | 537 | 0 |

Use the death causes to decide whether to first test tail-reachability, body-avoidance, or head-to-head threat rules. Compare on equivalent unseen matches, not raw unadjusted death totals.

## Replay-backed tactical situations

A tradeoff means the most food-directed static-free move had a reachable-space estimate at least 10 tiles smaller than another static-free option. Space scores are **bounded probes**, not exact guarantees.

| Replay | Turn | Snake | Body length | Actual move | Food distance after move | Space score (chosen/best) | Favored space? |
|---|---:|---|---:|---|---:|---:|---|
| [`game-75004.rep`](../replays/2026-11-02-045859-season/game-75004.rep.gz) | 1925 | `421462-alexander-palmer` | 235 | UP | 9 | 255/255 | yes |
| [`trials/422453-mauricetshepo-frost/trial-910000.rep`](../replays/2026-11-02-045859-season/trials/422453-mauricetshepo-frost/trial-910000.rep.gz) | 1850 | `422453-mauricetshepo-frost` | 230 | UP | 18 | 250/250 | yes |
| [`game-72004.rep`](../replays/2026-11-03-025900-season/game-72004.rep.gz) | 1675 | `421462-alexander-palmer` | 210 | LEFT | 11 | 230/230 | yes |
| [`game-75006.rep`](../replays/2026-11-02-145901-season/game-75006.rep.gz) | 1925 | `423239-zeeshaan-bham` | 200 | LEFT | 21 | 220/220 | yes |
| [`trials/403501-mashau-mudzanani/trial-912000.rep`](../replays/2026-11-02-145901-season/trials/403501-mashau-mudzanani/trial-912000.rep.gz) | 1575 | `403501-mashau-mudzanani` | 180 | UP | 27 | 200/200 | yes |
| [`game-76004.rep`](../replays/2026-11-02-045859-season/game-76004.rep.gz) | 1600 | `421462-alexander-palmer` | 180 | LEFT | 22 | 200/200 | yes |
| [`trials/403501-mashau-mudzanani/trial-912000.rep`](../replays/2026-11-02-145901-season/trials/403501-mashau-mudzanani/trial-912000.rep.gz) | 1450 | `403501-mashau-mudzanani` | 170 | RIGHT | 22 | 144/144 | yes |
| [`game-73005.rep`](../replays/2026-11-03-025900-season/game-73005.rep.gz) | 1700 | `421462-alexander-palmer` | 165 | LEFT | 27 | 185/185 | yes |
| [`game-71004.rep`](../replays/2026-11-03-025900-season/game-71004.rep.gz) | 1975 | `424820-elisha-mundalamo` | 160 | RIGHT | 6 | 180/180 | yes |
| [`trials/422453-mauricetshepo-frost/trial-911000.rep`](../replays/2026-11-02-045859-season/trials/422453-mauricetshepo-frost/trial-911000.rep.gz) | 1025 | `422453-mauricetshepo-frost` | 160 | DOWN | 21 | 180/180 | yes |
| [`trials/424820-elisha-mundalamo/trial-910000.rep`](../replays/2026-11-03-025900-season/trials/424820-elisha-mundalamo/trial-910000.rep.gz) | 1350 | `424820-elisha-mundalamo` | 155 | RIGHT | 14 | 175/175 | yes |
| [`trials/403501-mashau-mudzanani/trial-912000.rep`](../replays/2026-11-02-145901-season/trials/403501-mashau-mudzanani/trial-912000.rep.gz) | 1100 | `403501-mashau-mudzanani` | 150 | DOWN | 20 | 170/170 | yes |
| [`trials/427064-khodani-netili/trial-911000.rep`](../replays/2026-11-03-025900-season/trials/427064-khodani-netili/trial-911000.rep.gz) | 1375 | `427064-khodani-netili` | 145 | DOWN | 19 | 165/165 | yes |
| [`game-72003.rep`](../replays/2026-11-02-225901-season/game-72003.rep.gz) | 1575 | `421349-phathutshedzo-mudzanani` | 145 | RIGHT | 26 | 165/165 | yes |
| [`game-72003.rep`](../replays/2026-11-02-145901-season/game-72003.rep.gz) | 1500 | `424820-elisha-mundalamo` | 145 | DOWN | 2 | 165/165 | yes |
| [`trials/408008-bradley-buys/trial-911000.rep`](../replays/2026-11-02-225901-season/trials/408008-bradley-buys/trial-911000.rep.gz) | 1100 | `408008-bradley-buys` | 140 | LEFT | 5 | 160/160 | yes |
| [`game-74002.rep`](../replays/2026-11-02-145901-season/game-74002.rep.gz) | 1950 | `427039-sameeha-miabala` | 135 | DOWN | 28 | 155/155 | yes |
| [`game-75004.rep`](../replays/2026-11-02-045859-season/game-75004.rep.gz) | 1175 | `388060-tshepang-tshabalala` | 135 | UP | 21 | 155/155 | yes |
| [`game-76004.rep`](../replays/2026-11-02-045859-season/game-76004.rep.gz) | 1000 | `421462-alexander-palmer` | 130 | LEFT | 16 | 150/150 | yes |
| [`game-76004.rep`](../replays/2026-11-02-045859-season/game-76004.rep.gz) | 1850 | `427064-khodani-netili` | 130 | LEFT | 24 | 150/150 | yes |
| [`game-75000.rep`](../replays/2026-11-02-225901-season/game-75000.rep.gz) | 1250 | `408008-bradley-buys` | 120 | RIGHT | 10 | 140/140 | yes |
| [`game-73001.rep`](../replays/2026-11-02-045859-season/game-73001.rep.gz) | 1050 | `419342-ayeshan-puckree` | 115 | UP | 10 | 135/135 | yes |
| [`game-75006.rep`](../replays/2026-11-02-145901-season/game-75006.rep.gz) | 1250 | `389160-lwandle-ramanugu` | 110 | DOWN | 6 | 130/130 | yes |
| [`game-71004.rep`](../replays/2026-11-03-025900-season/game-71004.rep.gz) | 1200 | `410193-vhugala-makhwathane` | 100 | LEFT | 22 | 120/120 | yes |

## Historical hypotheses for later investigation (NO implementation yet)

1. **Food-versus-space planner:** Assign each candidate move a weighted score for distance to food and bounded flood-fill space. Compare against current Java bot, using the same fresh seeds.
2. **Danger override:** When a candidate leads to constrained reachable space, temporarily prioritize escape over food; test ablation with/without the override.
3. **Opponent-pressure rule:** Test threat-aware movement when an opponent head is within three toroidal tiles. The current report counts proximity but does not yet recover opponent intent.
4. **Policy imitation experiment:** Use replay states as labeled observations for relative actions, holding out entire matches and seasons for validation. High next-move accuracy alone is *not* proof of better game performance.

Only promote a strategy if it improves **held-out match outcomes** and survival with equivalent opponent setups. Collect more samples before trusting patterns from individual snakes.
