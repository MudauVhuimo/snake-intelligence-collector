# Snake26 strategy laboratory — LEGACY POOLED EXPLORATION

**Important:** This legacy diagnostic pools on-arrival trials and actual league
replays. It is NOT valid evidence that a strategy works in the league.
Use [Joined Research](joint_analysis.md) and
[Mode-Separated Replay Behavior](behavior_by_mode.md) instead.
The static reachable-space search is capped: many genuinely different
moves tie at the cap. Thus a very high 'widest-space choice' percentage
does NOT establish that a snake uses a space-maximizing algorithm.

Updated UTC: 2026-11-02T00:42:38+00:00
Unique replays analyzed: **96** (duplicate hashes skipped: 64; unreadable: 0)
Sampling: every **25th** turn per match, not independent observations.

## What the data can and cannot tell us

This is **behavioral observation**, not a live match simulator. Candidate moves use a conservative **static occupancy** approximation: snake tails may vacate, opponents move simultaneously, and outcomes could change. Therefore percentages are descriptive proxies, not guaranteed-safe decisions or win probabilities.

A prerecorded opponent does **not** respond to changes made by our bot; fixed historical moves cannot provide a valid full counterfactual match. To benchmark wins, we need to run live executables against locally available opponents or compare equivalent seed/opponent setups.

## Mixed trial/league samples: diagnostic only

| Group | Sampled moves | Food-nearest choices | Widest-space choices | Clear food/space tradeoffs | Space favored in tradeoffs |
|---|---:|---:|---:|---:|---:|
| Current top-10 | 5010 | 68.8% | 99.4% | 50 | 68.0% |
| Other student bots | 13890 | 71.7% | 99.3% | 159 | 71.7% |
| Built-in benchmarks | 10660 | 87.4% | 99.2% | 76 | 31.6% |

**Interpretation guardrail:** Built-in `~` bots are reported separately. Top-ten means the *latest* Division 1 top-ten ranking, not necessarily the same code version in old seasons. Groups have unequal and possibly biased opponents. Do not infer causation or an optimal policy from this table.

## Individual behavior fingerprints

| Team | Replays | Sampled moves | Food-nearest | Widest-space | Food/space conflicts | Space chosen in conflicts |
|---|---:|---:|---:|---:|---:|---:|
| `421462-alexander-palmer` | 14 | 1092 | 73.0% | 99.6% | 7 | 71.4% |
| `388828-ngcebo-methula` | 10 | 766 | 69.1% | 99.3% | 8 | 62.5% |
| `388060-tshepang-tshabalala` | 9 | 697 | 67.3% | 99.6% | 7 | 85.7% |
| `403339-david-ndambo` | 8 | 623 | 62.6% | 100.0% | 3 | 100.0% |
| `424820-elisha-mundalamo` | 7 | 529 | 69.1% | 99.6% | 6 | 83.3% |
| `427064-khodani-netili` | 5 | 381 | 70.1% | 99.2% | 8 | 62.5% |
| `426895-mpho-ramasakona` | 4 | 312 | 71.0% | 98.0% | 3 | 33.3% |
| `428786-marvellous-sambo` | 3 | 234 | 68.0% | 98.2% | 4 | 25.0% |
| `423436-ntobeko-zondi` | 3 | 230 | 66.2% | 100.0% | 1 | 100.0% |
| `427039-sameeha-miabala` | 2 | 146 | 66.4% | 98.6% | 3 | 66.7% |
| `413538-lelethuthando-nikelo` | 10 | 779 | 66.2% | 99.7% | 4 | 100.0% |
| `409997-utayan-naidoo` | 9 | 699 | 64.7% | 98.2% | 14 | 50.0% |
| `402334-angile-saho` | 9 | 696 | 73.7% | 98.9% | 15 | 80.0% |
| `408070-collen-mthombeni` | 9 | 692 | 67.9% | 99.1% | 3 | 33.3% |
| `404721-khensani-maluleke` | 9 | 690 | 71.9% | 99.1% | 8 | 50.0% |
| `419926-mphile-nchabeleng` | 8 | 591 | 72.6% | 99.8% | 4 | 100.0% |
| `421349-phathutshedzo-mudzanani` | 7 | 551 | 75.7% | 99.4% | 4 | 25.0% |
| `419636-jason-chen` | 7 | 542 | 71.3% | 100.0% | 7 | 100.0% |
| `409987-sbongakonke-shange` | 6 | 473 | 71.5% | 99.8% | 9 | 88.9% |
| `428954-njabulo-ndlozi` | 6 | 463 | 62.5% | 100.0% | 5 | 100.0% |
| `419342-ayeshan-puckree` | 5 | 382 | 64.9% | 99.7% | 2 | 100.0% |
| `423135-mpho-muremi` | 5 | 382 | 62.8% | 99.5% | 6 | 83.3% |
| `410193-vhugala-makhwathane` | 5 | 375 | 65.8% | 99.2% | 6 | 50.0% |
| `409598-langelihle-funeka` | 4 | 315 | 90.2% | 100.0% | 4 | 100.0% |
| `423546-ndabenhle-shabangu` | 4 | 314 | 67.4% | 99.7% | 1 | 100.0% |
| `386901-amanda-huo` | 4 | 312 | 76.9% | 99.7% | 4 | 100.0% |
| `427417-phophi-shavhani` | 4 | 298 | 78.4% | 98.9% | 4 | 100.0% |
| `423239-zeeshaan-bham` | 4 | 297 | 65.4% | 98.3% | 5 | 40.0% |
| `422777-thandile-mamiana` | 3 | 237 | 65.5% | 99.1% | 5 | 80.0% |
| `405469-adham-soror` | 3 | 237 | 88.7% | 100.0% | 6 | 100.0% |

## Observed deaths by cause

Counts are actual `died` replay events, unlike static-space estimates.

| Group | Self-collision | Body collision | Head-to-head | Other |
|---|---:|---:|---:|---:|
| Current top-10 | 13 | 9 | 6 | 0 |
| Other student bots | 63 | 54 | 25 | 0 |
| Built-in benchmarks | 274 | 584 | 346 | 0 |

Use the death causes to decide whether to first test tail-reachability, body-avoidance, or head-to-head threat rules. Compare on equivalent unseen matches, not raw unadjusted death totals.

## Replay-backed tactical situations

A tradeoff means the most food-directed static-free move had a reachable-space estimate at least 10 tiles smaller than another static-free option. Space scores are **bounded probes**, not exact guarantees.

| Replay | Turn | Snake | Body length | Actual move | Food distance after move | Space score (chosen/best) | Favored space? |
|---|---:|---|---:|---|---:|---:|---|
| [`trials/409997-utayan-naidoo/trial-912000.rep`](../replays/2026-11-01-225859-season/trials/409997-utayan-naidoo/trial-912000.rep.gz) | 1850 | `409997-utayan-naidoo` | 250 | RIGHT | 30 | 184/184 | yes |
| [`game-71050.rep`](../replays/2026-11-01-225859-season/game-71050.rep.gz) | 1975 | `419636-jason-chen` | 180 | UP | 17 | 72/72 | yes |
| [`game-72007.rep`](../replays/2026-11-01-235859-season/game-72007.rep.gz) | 1600 | `421462-alexander-palmer` | 175 | RIGHT | 24 | 195/195 | yes |
| [`trials/419926-mphile-nchabeleng/trial-912000.rep`](../replays/2026-11-01-225859-season/trials/419926-mphile-nchabeleng/trial-912000.rep.gz) | 1275 | `419926-mphile-nchabeleng` | 175 | DOWN | 23 | 195/195 | yes |
| [`game-74007.rep`](../replays/2026-11-01-225859-season/game-74007.rep.gz) | 1375 | `421462-alexander-palmer` | 165 | DOWN | 18 | 25/25 | yes |
| [`game-71003.rep`](../replays/2026-11-01-225859-season/game-71003.rep.gz) | 1925 | `403339-david-ndambo` | 165 | LEFT | 31 | 185/185 | yes |
| [`game-72002.rep`](../replays/2026-11-01-225859-season/game-72002.rep.gz) | 1675 | `427039-sameeha-miabala` | 135 | LEFT | 16 | 155/155 | yes |
| [`game-71006.rep`](../replays/2026-11-01-225859-season/game-71006.rep.gz) | 1725 | `388060-tshepang-tshabalala` | 135 | RIGHT | 17 | 148/148 | yes |
| [`game-71056.rep`](../replays/2026-11-01-225859-season/game-71056.rep.gz) | 1225 | `408501-asher-urison` | 125 | RIGHT | 14 | 145/145 | yes |
| [`game-72007.rep`](../replays/2026-11-01-235859-season/game-72007.rep.gz) | 1275 | `404721-khensani-maluleke` | 115 | RIGHT | 31 | 100/100 | yes |
| [`game-76004.rep`](../replays/2026-11-01-225859-season/game-76004.rep.gz) | 1025 | `404721-khensani-maluleke` | 115 | UP | 14 | 135/135 | yes |
| [`game-71005.rep`](../replays/2026-11-01-225859-season/game-71005.rep.gz) | 1325 | `423135-mpho-muremi` | 115 | DOWN | 13 | 135/135 | yes |
| [`game-71005.rep`](../replays/2026-11-01-225859-season/game-71005.rep.gz) | 1375 | `423258-muhammed-dar` | 115 | LEFT | 20 | 19/19 | yes |
| [`game-71056.rep`](../replays/2026-11-01-225859-season/game-71056.rep.gz) | 1050 | `400861-sibusisomlungisi-dlamini` | 110 | UP | 18 | 130/130 | yes |
| [`game-71005.rep`](../replays/2026-11-01-225859-season/game-71005.rep.gz) | 1400 | `409997-utayan-naidoo` | 110 | LEFT | 32 | 130/130 | yes |
| [`game-73001.rep`](../replays/2026-11-01-235859-season/game-73001.rep.gz) | 700 | `421462-alexander-palmer` | 105 | RIGHT | 32 | 44/44 | yes |
| [`game-72005.rep`](../replays/2026-11-01-225859-season/game-72005.rep.gz) | 900 | `427417-phophi-shavhani` | 100 | LEFT | 32 | 120/120 | yes |
| [`game-72005.rep`](../replays/2026-11-01-225859-season/game-72005.rep.gz) | 925 | `427417-phophi-shavhani` | 100 | UP | 21 | 120/120 | yes |
| [`game-71002.rep`](../replays/2026-11-01-225859-season/game-71002.rep.gz) | 1175 | `402334-angile-saho` | 100 | DOWN | 33 | 107/107 | yes |
| [`game-71007.rep`](../replays/2026-11-01-225859-season/game-71007.rep.gz) | 1175 | `428954-njabulo-ndlozi` | 95 | RIGHT | 18 | 115/115 | yes |
| [`game-71056.rep`](../replays/2026-11-01-225859-season/game-71056.rep.gz) | 1975 | `409987-sbongakonke-shange` | 90 | UP | 20 | 110/110 | yes |
| [`game-74007.rep`](../replays/2026-11-01-235859-season/game-74007.rep.gz) | 950 | `403754-vhuimo-mudau` | 85 | RIGHT | 34 | 105/105 | yes |
| [`game-71056.rep`](../replays/2026-11-01-225859-season/game-71056.rep.gz) | 1475 | `409987-sbongakonke-shange` | 85 | DOWN | 16 | 105/105 | yes |
| [`game-71006.rep`](../replays/2026-11-01-225859-season/game-71006.rep.gz) | 1225 | `388060-tshepang-tshabalala` | 85 | UP | 8 | 105/105 | yes |

## Historical hypotheses for later investigation (NO implementation yet)

1. **Food-versus-space planner:** Assign each candidate move a weighted score for distance to food and bounded flood-fill space. Compare against current Java bot, using the same fresh seeds.
2. **Danger override:** When a candidate leads to constrained reachable space, temporarily prioritize escape over food; test ablation with/without the override.
3. **Opponent-pressure rule:** Test threat-aware movement when an opponent head is within three toroidal tiles. The current report counts proximity but does not yet recover opponent intent.
4. **Policy imitation experiment:** Use replay states as labeled observations for relative actions, holding out entire matches and seasons for validation. High next-move accuracy alone is *not* proof of better game performance.

Only promote a strategy if it improves **held-out match outcomes** and survival with equivalent opponent setups. Collect more samples before trusting patterns from individual snakes.
