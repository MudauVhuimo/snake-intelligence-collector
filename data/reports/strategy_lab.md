# Snake26 strategy laboratory — LEGACY POOLED EXPLORATION

**Important:** This legacy diagnostic pools on-arrival trials and actual league
replays. It is NOT valid evidence that a strategy works in the league.
Use [Joined Research](joint_analysis.md) and
[Mode-Separated Replay Behavior](behavior_by_mode.md) instead.
The static reachable-space search is capped: many genuinely different
moves tie at the cap. Thus a very high 'widest-space choice' percentage
does NOT establish that a snake uses a space-maximizing algorithm.

Updated UTC: 2026-11-03T12:25:56+00:00
Unique replays analyzed: **159** (duplicate hashes skipped: 71; unreadable: 0)
Sampling: every **25th** turn per match, not independent observations.

## What the data can and cannot tell us

This is **behavioral observation**, not a live match simulator. Candidate moves use a conservative **static occupancy** approximation: snake tails may vacate, opponents move simultaneously, and outcomes could change. Therefore percentages are descriptive proxies, not guaranteed-safe decisions or win probabilities.

A prerecorded opponent does **not** respond to changes made by our bot; fixed historical moves cannot provide a valid full counterfactual match. To benchmark wins, we need to run live executables against locally available opponents or compare equivalent seed/opponent setups.

## Mixed trial/league samples: diagnostic only

| Group | Sampled moves | Food-nearest choices | Widest-space choices | Clear food/space tradeoffs | Space favored in tradeoffs |
|---|---:|---:|---:|---:|---:|
| Current top-10 | 9927 | 68.8% | 99.4% | 99 | 68.7% |
| Other student bots | 21753 | 71.4% | 99.3% | 245 | 70.2% |
| Built-in benchmarks | 17128 | 87.5% | 99.2% | 126 | 29.4% |

**Interpretation guardrail:** Built-in `~` bots are reported separately. Top-ten means the *latest* Division 1 top-ten ranking, not necessarily the same code version in old seasons. Groups have unequal and possibly biased opponents. Do not infer causation or an optimal policy from this table.

## Individual behavior fingerprints

| Team | Replays | Sampled moves | Food-nearest | Widest-space | Food/space conflicts | Space chosen in conflicts |
|---|---:|---:|---:|---:|---:|---:|
| `421462-alexander-palmer` | 30 | 2323 | 71.3% | 99.3% | 21 | 66.7% |
| `427064-khodani-netili` | 15 | 1155 | 67.9% | 99.5% | 17 | 76.5% |
| `424820-elisha-mundalamo` | 14 | 1069 | 70.7% | 99.7% | 10 | 80.0% |
| `413538-lelethuthando-nikelo` | 13 | 1013 | 65.7% | 99.5% | 9 | 77.8% |
| `388828-ngcebo-methula` | 13 | 994 | 69.4% | 99.4% | 10 | 60.0% |
| `404721-khensani-maluleke` | 11 | 845 | 72.1% | 99.1% | 9 | 44.4% |
| `419342-ayeshan-puckree` | 10 | 767 | 64.2% | 99.7% | 5 | 100.0% |
| `423436-ntobeko-zondi` | 9 | 690 | 65.3% | 99.7% | 3 | 66.7% |
| `423239-zeeshaan-bham` | 9 | 678 | 67.1% | 98.8% | 9 | 55.6% |
| `408501-asher-urison` | 5 | 393 | 68.8% | 99.2% | 6 | 66.7% |
| `421349-phathutshedzo-mudzanani` | 17 | 1332 | 74.4% | 99.5% | 9 | 55.6% |
| `388060-tshepang-tshabalala` | 15 | 1150 | 66.0% | 99.5% | 13 | 84.6% |
| `408070-collen-mthombeni` | 14 | 1077 | 66.5% | 99.2% | 4 | 50.0% |
| `409997-utayan-naidoo` | 12 | 932 | 64.2% | 98.6% | 17 | 52.9% |
| `402334-angile-saho` | 12 | 926 | 74.1% | 99.0% | 17 | 70.6% |
| `406000-mulimisi-rammela` | 11 | 837 | 65.3% | 99.1% | 6 | 33.3% |
| `421538-tshifhiwa-bvumbi` | 10 | 790 | 74.8% | 99.3% | 6 | 50.0% |
| `403339-david-ndambo` | 10 | 778 | 63.1% | 99.9% | 4 | 100.0% |
| `428786-marvellous-sambo` | 10 | 772 | 69.7% | 99.1% | 12 | 50.0% |
| `410193-vhugala-makhwathane` | 10 | 751 | 63.6% | 98.6% | 14 | 57.1% |
| `419926-mphile-nchabeleng` | 10 | 741 | 73.0% | 99.3% | 6 | 66.7% |
| `428954-njabulo-ndlozi` | 9 | 694 | 64.2% | 100.0% | 6 | 100.0% |
| `389160-lwandle-ramanugu` | 9 | 690 | 79.0% | 98.4% | 8 | 62.5% |
| `419636-jason-chen` | 7 | 542 | 71.3% | 100.0% | 7 | 100.0% |
| `408008-bradley-buys` | 7 | 531 | 66.1% | 99.4% | 8 | 75.0% |
| `427039-sameeha-miabala` | 7 | 524 | 67.1% | 99.0% | 6 | 66.7% |
| `409987-sbongakonke-shange` | 6 | 473 | 71.5% | 99.8% | 9 | 88.9% |
| `426895-mpho-ramasakona` | 6 | 467 | 73.5% | 98.5% | 4 | 50.0% |
| `428464-madalitso-mnqanqeni` | 6 | 459 | 71.8% | 98.4% | 5 | 60.0% |
| `427417-phophi-shavhani` | 6 | 453 | 79.1% | 99.1% | 5 | 100.0% |

## Observed deaths by cause

Counts are actual `died` replay events, unlike static-space estimates.

| Group | Self-collision | Body collision | Head-to-head | Other |
|---|---:|---:|---:|---:|
| Current top-10 | 37 | 23 | 13 | 0 |
| Other student bots | 95 | 85 | 36 | 0 |
| Built-in benchmarks | 403 | 933 | 606 | 0 |

Use the death causes to decide whether to first test tail-reachability, body-avoidance, or head-to-head threat rules. Compare on equivalent unseen matches, not raw unadjusted death totals.

## Replay-backed tactical situations

A tradeoff means the most food-directed static-free move had a reachable-space estimate at least 10 tiles smaller than another static-free option. Space scores are **bounded probes**, not exact guarantees.

| Replay | Turn | Snake | Body length | Actual move | Food distance after move | Space score (chosen/best) | Favored space? |
|---|---:|---|---:|---|---:|---:|---|
| [`game-72004.rep`](../replays/2026-11-03-025900-season/game-72004.rep.gz) | 1675 | `421462-alexander-palmer` | 210 | LEFT | 11 | 230/230 | yes |
| [`game-74002.rep`](../replays/2026-11-03-055900-season/game-74002.rep.gz) | 1850 | `419222-asisipho-ngaba` | 200 | RIGHT | 27 | 217/217 | yes |
| [`game-73005.rep`](../replays/2026-11-03-025900-season/game-73005.rep.gz) | 1700 | `421462-alexander-palmer` | 165 | LEFT | 27 | 185/185 | yes |
| [`game-75006.rep`](../replays/2026-11-03-055900-season/game-75006.rep.gz) | 1650 | `427064-khodani-netili` | 160 | LEFT | 14 | 180/180 | yes |
| [`game-71004.rep`](../replays/2026-11-03-025900-season/game-71004.rep.gz) | 1975 | `424820-elisha-mundalamo` | 160 | RIGHT | 6 | 180/180 | yes |
| [`game-76007.rep`](../replays/2026-11-03-115900-season/game-76007.rep.gz) | 1750 | `426650-babongile-mafantiri` | 155 | LEFT | 18 | 175/175 | yes |
| [`trials/424820-elisha-mundalamo/trial-910000.rep`](../replays/2026-11-03-025900-season/trials/424820-elisha-mundalamo/trial-910000.rep.gz) | 1350 | `424820-elisha-mundalamo` | 155 | RIGHT | 14 | 175/175 | yes |
| [`game-71004.rep`](../replays/2026-11-03-045900-season/game-71004.rep.gz) | 1500 | `428786-marvellous-sambo` | 150 | RIGHT | 18 | 160/160 | yes |
| [`trials/427064-khodani-netili/trial-911000.rep`](../replays/2026-11-03-025900-season/trials/427064-khodani-netili/trial-911000.rep.gz) | 1375 | `427064-khodani-netili` | 145 | DOWN | 19 | 165/165 | yes |
| [`trials/408008-bradley-buys/trial-911000.rep`](../replays/2026-11-02-225901-season/trials/408008-bradley-buys/trial-911000.rep.gz) | 1100 | `408008-bradley-buys` | 140 | LEFT | 5 | 160/160 | yes |
| [`game-74002.rep`](../replays/2026-11-03-055900-season/game-74002.rep.gz) | 1750 | `427064-khodani-netili` | 135 | UP | 26 | 155/155 | yes |
| [`game-71000.rep`](../replays/2026-11-03-105900-season/game-71000.rep.gz) | 1375 | `403339-david-ndambo` | 130 | RIGHT | 5 | 150/150 | yes |
| [`game-72002.rep`](../replays/2026-11-03-115900-season/game-72002.rep.gz) | 1975 | `410193-vhugala-makhwathane` | 120 | RIGHT | 2 | 100/100 | yes |
| [`game-72003.rep`](../replays/2026-11-03-055900-season/game-72003.rep.gz) | 1625 | `427064-khodani-netili` | 120 | UP | 14 | 140/140 | yes |
| [`game-75000.rep`](../replays/2026-11-02-225901-season/game-75000.rep.gz) | 1250 | `408008-bradley-buys` | 120 | RIGHT | 10 | 140/140 | yes |
| [`game-73000.rep`](../replays/2026-11-03-115900-season/game-73000.rep.gz) | 850 | `421462-alexander-palmer` | 100 | LEFT | 14 | 120/120 | yes |
| [`game-71001.rep`](../replays/2026-11-03-055900-season/game-71001.rep.gz) | 1475 | `389160-lwandle-ramanugu` | 100 | LEFT | 18 | 110/110 | yes |
| [`game-71004.rep`](../replays/2026-11-03-025900-season/game-71004.rep.gz) | 1200 | `410193-vhugala-makhwathane` | 100 | LEFT | 22 | 120/120 | yes |
| [`game-76007.rep`](../replays/2026-11-02-225901-season/game-76007.rep.gz) | 1200 | `419222-asisipho-ngaba` | 100 | DOWN | 25 | 120/120 | yes |
| [`game-73005.rep`](../replays/2026-11-02-225901-season/game-73005.rep.gz) | 925 | `423239-zeeshaan-bham` | 100 | LEFT | 12 | 120/120 | yes |
| [`game-72002.rep`](../replays/2026-11-03-115900-season/game-72002.rep.gz) | 1175 | `410193-vhugala-makhwathane` | 95 | LEFT | 11 | 115/115 | yes |
| [`trials/419342-ayeshan-puckree/trial-912000.rep`](../replays/2026-11-03-105900-season/trials/419342-ayeshan-puckree/trial-912000.rep.gz) | 650 | `419342-ayeshan-puckree` | 95 | DOWN | 31 | 115/115 | yes |
| [`trials/426895-mpho-ramasakona/trial-910000.rep`](../replays/2026-11-03-055900-season/trials/426895-mpho-ramasakona/trial-910000.rep.gz) | 1200 | `~survivor` | 90 | RIGHT | 27 | 110/110 | yes |
| [`game-73000.rep`](../replays/2026-11-03-115900-season/game-73000.rep.gz) | 1400 | `428786-marvellous-sambo` | 85 | UP | 24 | 27/27 | yes |

## Historical hypotheses for later investigation (NO implementation yet)

1. **Food-versus-space planner:** Assign each candidate move a weighted score for distance to food and bounded flood-fill space. Compare against current Java bot, using the same fresh seeds.
2. **Danger override:** When a candidate leads to constrained reachable space, temporarily prioritize escape over food; test ablation with/without the override.
3. **Opponent-pressure rule:** Test threat-aware movement when an opponent head is within three toroidal tiles. The current report counts proximity but does not yet recover opponent intent.
4. **Policy imitation experiment:** Use replay states as labeled observations for relative actions, holding out entire matches and seasons for validation. High next-move accuracy alone is *not* proof of better game performance.

Only promote a strategy if it improves **held-out match outcomes** and survival with equivalent opponent setups. Collect more samples before trusting patterns from individual snakes.
