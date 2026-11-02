# Snake26 strategy laboratory — LEGACY POOLED EXPLORATION

**Important:** This legacy diagnostic pools on-arrival trials and actual league
replays. It is NOT valid evidence that a strategy works in the league.
Use [Joined Research](joint_analysis.md) and
[Mode-Separated Replay Behavior](behavior_by_mode.md) instead.
The static reachable-space search is capped: many genuinely different
moves tie at the cap. Thus a very high 'widest-space choice' percentage
does NOT establish that a snake uses a space-maximizing algorithm.

Updated UTC: 2026-11-02T06:08:59+00:00
Unique replays analyzed: **113** (duplicate hashes skipped: 67; unreadable: 0)
Sampling: every **25th** turn per match, not independent observations.

## What the data can and cannot tell us

This is **behavioral observation**, not a live match simulator. Candidate moves use a conservative **static occupancy** approximation: snake tails may vacate, opponents move simultaneously, and outcomes could change. Therefore percentages are descriptive proxies, not guaranteed-safe decisions or win probabilities.

A prerecorded opponent does **not** respond to changes made by our bot; fixed historical moves cannot provide a valid full counterfactual match. To benchmark wins, we need to run live executables against locally available opponents or compare equivalent seed/opponent setups.

## Mixed trial/league samples: diagnostic only

| Group | Sampled moves | Food-nearest choices | Widest-space choices | Clear food/space tradeoffs | Space favored in tradeoffs |
|---|---:|---:|---:|---:|---:|
| Current top-10 | 6758 | 69.6% | 99.4% | 73 | 72.6% |
| Other student bots | 15473 | 71.4% | 99.3% | 171 | 68.4% |
| Built-in benchmarks | 12498 | 87.3% | 99.2% | 89 | 30.3% |

**Interpretation guardrail:** Built-in `~` bots are reported separately. Top-ten means the *latest* Division 1 top-ten ranking, not necessarily the same code version in old seasons. Groups have unequal and possibly biased opponents. Do not infer causation or an optimal policy from this table.

## Individual behavior fingerprints

| Team | Replays | Sampled moves | Food-nearest | Widest-space | Food/space conflicts | Space chosen in conflicts |
|---|---:|---:|---:|---:|---:|---:|
| `421462-alexander-palmer` | 20 | 1555 | 73.1% | 99.5% | 11 | 72.7% |
| `388828-ngcebo-methula` | 12 | 918 | 69.7% | 99.4% | 8 | 62.5% |
| `402334-angile-saho` | 10 | 774 | 74.5% | 99.1% | 15 | 80.0% |
| `403339-david-ndambo` | 9 | 701 | 63.3% | 99.9% | 3 | 100.0% |
| `419926-mphile-nchabeleng` | 9 | 669 | 72.7% | 99.7% | 5 | 80.0% |
| `424820-elisha-mundalamo` | 8 | 608 | 68.5% | 99.7% | 6 | 83.3% |
| `428954-njabulo-ndlozi` | 7 | 540 | 63.1% | 100.0% | 6 | 100.0% |
| `427064-khodani-netili` | 7 | 537 | 65.2% | 99.4% | 9 | 66.7% |
| `428786-marvellous-sambo` | 4 | 310 | 69.6% | 98.0% | 7 | 28.6% |
| `427039-sameeha-miabala` | 2 | 146 | 66.4% | 98.6% | 3 | 66.7% |
| `413538-lelethuthando-nikelo` | 12 | 935 | 65.6% | 99.4% | 7 | 71.4% |
| `388060-tshepang-tshabalala` | 11 | 849 | 66.6% | 99.5% | 8 | 87.5% |
| `408070-collen-mthombeni` | 10 | 769 | 67.6% | 99.2% | 3 | 33.3% |
| `409997-utayan-naidoo` | 9 | 699 | 64.7% | 98.2% | 14 | 50.0% |
| `404721-khensani-maluleke` | 9 | 690 | 71.9% | 99.1% | 8 | 50.0% |
| `421349-phathutshedzo-mudzanani` | 7 | 551 | 75.7% | 99.4% | 4 | 25.0% |
| `419636-jason-chen` | 7 | 542 | 71.3% | 100.0% | 7 | 100.0% |
| `419342-ayeshan-puckree` | 7 | 536 | 63.6% | 99.8% | 3 | 100.0% |
| `409987-sbongakonke-shange` | 6 | 473 | 71.5% | 99.8% | 9 | 88.9% |
| `428464-madalitso-mnqanqeni` | 6 | 459 | 71.8% | 98.4% | 5 | 60.0% |
| `406000-mulimisi-rammela` | 5 | 383 | 63.7% | 98.9% | 5 | 40.0% |
| `423135-mpho-muremi` | 5 | 382 | 62.8% | 99.5% | 6 | 83.3% |
| `410193-vhugala-makhwathane` | 5 | 375 | 65.8% | 99.2% | 6 | 50.0% |
| `421538-tshifhiwa-bvumbi` | 4 | 316 | 73.6% | 99.0% | 3 | 66.7% |
| `422453-mauricetshepo-frost` | 4 | 315 | 77.2% | 99.0% | 4 | 50.0% |
| `409598-langelihle-funeka` | 4 | 315 | 90.2% | 100.0% | 4 | 100.0% |
| `423546-ndabenhle-shabangu` | 4 | 314 | 67.4% | 99.7% | 1 | 100.0% |
| `426895-mpho-ramasakona` | 4 | 312 | 71.0% | 98.0% | 3 | 33.3% |
| `386901-amanda-huo` | 4 | 312 | 76.9% | 99.7% | 4 | 100.0% |
| `429782-maseeha-seedat` | 4 | 309 | 70.9% | 99.0% | 4 | 50.0% |

## Observed deaths by cause

Counts are actual `died` replay events, unlike static-space estimates.

| Group | Self-collision | Body collision | Head-to-head | Other |
|---|---:|---:|---:|---:|
| Current top-10 | 18 | 16 | 8 | 0 |
| Other student bots | 77 | 57 | 28 | 0 |
| Built-in benchmarks | 313 | 699 | 435 | 0 |

Use the death causes to decide whether to first test tail-reachability, body-avoidance, or head-to-head threat rules. Compare on equivalent unseen matches, not raw unadjusted death totals.

## Replay-backed tactical situations

A tradeoff means the most food-directed static-free move had a reachable-space estimate at least 10 tiles smaller than another static-free option. Space scores are **bounded probes**, not exact guarantees.

| Replay | Turn | Snake | Body length | Actual move | Food distance after move | Space score (chosen/best) | Favored space? |
|---|---:|---|---:|---|---:|---:|---|
| [`trials/409997-utayan-naidoo/trial-912000.rep`](../replays/2026-11-01-225859-season/trials/409997-utayan-naidoo/trial-912000.rep.gz) | 1850 | `409997-utayan-naidoo` | 250 | RIGHT | 30 | 184/184 | yes |
| [`game-75004.rep`](../replays/2026-11-02-045859-season/game-75004.rep.gz) | 1925 | `421462-alexander-palmer` | 235 | UP | 9 | 255/255 | yes |
| [`trials/422453-mauricetshepo-frost/trial-910000.rep`](../replays/2026-11-02-045859-season/trials/422453-mauricetshepo-frost/trial-910000.rep.gz) | 1850 | `422453-mauricetshepo-frost` | 230 | UP | 18 | 250/250 | yes |
| [`game-76004.rep`](../replays/2026-11-02-045859-season/game-76004.rep.gz) | 1600 | `421462-alexander-palmer` | 180 | LEFT | 22 | 200/200 | yes |
| [`game-72007.rep`](../replays/2026-11-01-235859-season/game-72007.rep.gz) | 1600 | `421462-alexander-palmer` | 175 | RIGHT | 24 | 195/195 | yes |
| [`trials/419926-mphile-nchabeleng/trial-912000.rep`](../replays/2026-11-01-225859-season/trials/419926-mphile-nchabeleng/trial-912000.rep.gz) | 1275 | `419926-mphile-nchabeleng` | 175 | DOWN | 23 | 195/195 | yes |
| [`game-74007.rep`](../replays/2026-11-01-225859-season/game-74007.rep.gz) | 1375 | `421462-alexander-palmer` | 165 | DOWN | 18 | 25/25 | yes |
| [`trials/422453-mauricetshepo-frost/trial-911000.rep`](../replays/2026-11-02-045859-season/trials/422453-mauricetshepo-frost/trial-911000.rep.gz) | 1025 | `422453-mauricetshepo-frost` | 160 | DOWN | 21 | 180/180 | yes |
| [`game-71000.rep`](../replays/2026-11-02-045859-season/game-71000.rep.gz) | 1475 | `428786-marvellous-sambo` | 160 | DOWN | 9 | 180/180 | yes |
| [`game-75004.rep`](../replays/2026-11-02-045859-season/game-75004.rep.gz) | 1175 | `388060-tshepang-tshabalala` | 135 | UP | 21 | 155/155 | yes |
| [`game-76004.rep`](../replays/2026-11-02-045859-season/game-76004.rep.gz) | 1000 | `421462-alexander-palmer` | 130 | LEFT | 16 | 150/150 | yes |
| [`game-76004.rep`](../replays/2026-11-02-045859-season/game-76004.rep.gz) | 1850 | `427064-khodani-netili` | 130 | LEFT | 24 | 150/150 | yes |
| [`game-73001.rep`](../replays/2026-11-02-045859-season/game-73001.rep.gz) | 1050 | `419342-ayeshan-puckree` | 115 | UP | 10 | 135/135 | yes |
| [`game-72007.rep`](../replays/2026-11-01-235859-season/game-72007.rep.gz) | 1275 | `404721-khensani-maluleke` | 115 | RIGHT | 31 | 100/100 | yes |
| [`game-76004.rep`](../replays/2026-11-01-225859-season/game-76004.rep.gz) | 1025 | `404721-khensani-maluleke` | 115 | UP | 14 | 135/135 | yes |
| [`game-73001.rep`](../replays/2026-11-01-235859-season/game-73001.rep.gz) | 700 | `421462-alexander-palmer` | 105 | RIGHT | 32 | 44/44 | yes |
| [`game-74007.rep`](../replays/2026-11-02-045859-season/game-74007.rep.gz) | 1475 | `406000-mulimisi-rammela` | 100 | LEFT | 26 | 83/83 | yes |
| [`game-72005.rep`](../replays/2026-11-01-225859-season/game-72005.rep.gz) | 900 | `427417-phophi-shavhani` | 100 | LEFT | 32 | 120/120 | yes |
| [`trials/423158-risima-mashele/trial-912000.rep`](../replays/2026-11-02-045859-season/trials/423158-risima-mashele/trial-912000.rep.gz) | 575 | `423158-risima-mashele` | 85 | LEFT | 13 | 105/105 | yes |
| [`game-74007.rep`](../replays/2026-11-01-235859-season/game-74007.rep.gz) | 950 | `403754-vhuimo-mudau` | 85 | RIGHT | 34 | 105/105 | yes |
| [`game-75004.rep`](../replays/2026-11-02-045859-season/game-75004.rep.gz) | 1575 | `408008-bradley-buys` | 80 | DOWN | 20 | 100/100 | yes |
| [`game-75004.rep`](../replays/2026-11-01-225859-season/game-75004.rep.gz) | 975 | `388060-tshepang-tshabalala` | 80 | DOWN | 20 | 100/100 | yes |
| [`game-75004.rep`](../replays/2026-11-01-225859-season/game-75004.rep.gz) | 1450 | `388060-tshepang-tshabalala` | 80 | DOWN | 22 | 100/100 | yes |
| [`game-72007.rep`](../replays/2026-11-01-235859-season/game-72007.rep.gz) | 525 | `402334-angile-saho` | 75 | DOWN | 12 | 95/95 | yes |

## Historical hypotheses for later investigation (NO implementation yet)

1. **Food-versus-space planner:** Assign each candidate move a weighted score for distance to food and bounded flood-fill space. Compare against current Java bot, using the same fresh seeds.
2. **Danger override:** When a candidate leads to constrained reachable space, temporarily prioritize escape over food; test ablation with/without the override.
3. **Opponent-pressure rule:** Test threat-aware movement when an opponent head is within three toroidal tiles. The current report counts proximity but does not yet recover opponent intent.
4. **Policy imitation experiment:** Use replay states as labeled observations for relative actions, holding out entire matches and seasons for validation. High next-move accuracy alone is *not* proof of better game performance.

Only promote a strategy if it improves **held-out match outcomes** and survival with equivalent opponent setups. Collect more samples before trusting patterns from individual snakes.
