# Snake26 strategy laboratory — LEGACY POOLED EXPLORATION

**Important:** This legacy diagnostic pools on-arrival trials and actual league
replays. It is NOT valid evidence that a strategy works in the league.
Use [Joined Research](joint_analysis.md) and
[Mode-Separated Replay Behavior](behavior_by_mode.md) instead.
The static reachable-space search is capped: many genuinely different
moves tie at the cap. Thus a very high 'widest-space choice' percentage
does NOT establish that a snake uses a space-maximizing algorithm.

Updated UTC: 2026-11-06T11:03:24+00:00
Unique replays analyzed: **188** (duplicate hashes skipped: 72; unreadable: 0)
Sampling: every **25th** turn per match, not independent observations.

## What the data can and cannot tell us

This is **behavioral observation**, not a live match simulator. Candidate moves use a conservative **static occupancy** approximation: snake tails may vacate, opponents move simultaneously, and outcomes could change. Therefore percentages are descriptive proxies, not guaranteed-safe decisions or win probabilities.

A prerecorded opponent does **not** respond to changes made by our bot; fixed historical moves cannot provide a valid full counterfactual match. To benchmark wins, we need to run live executables against locally available opponents or compare equivalent seed/opponent setups.

## Mixed trial/league samples: diagnostic only

| Group | Sampled moves | Food-nearest choices | Widest-space choices | Clear food/space tradeoffs | Space favored in tradeoffs |
|---|---:|---:|---:|---:|---:|
| Current top-10 | 10319 | 68.7% | 99.3% | 106 | 67.0% |
| Other student bots | 27518 | 70.9% | 99.3% | 313 | 72.8% |
| Built-in benchmarks | 19899 | 87.5% | 99.2% | 146 | 30.8% |

**Interpretation guardrail:** Built-in `~` bots are reported separately. Top-ten means the *latest* Division 1 top-ten ranking, not necessarily the same code version in old seasons. Groups have unequal and possibly biased opponents. Do not infer causation or an optimal policy from this table.

## Individual behavior fingerprints

| Team | Replays | Sampled moves | Food-nearest | Widest-space | Food/space conflicts | Space chosen in conflicts |
|---|---:|---:|---:|---:|---:|---:|
| `421462-alexander-palmer` | 43 | 3339 | 70.4% | 99.3% | 36 | 72.2% |
| `408070-collen-mthombeni` | 17 | 1308 | 66.7% | 99.1% | 7 | 71.4% |
| `424820-elisha-mundalamo` | 16 | 1222 | 69.6% | 99.7% | 10 | 80.0% |
| `413538-lelethuthando-nikelo` | 15 | 1170 | 65.3% | 99.4% | 11 | 63.6% |
| `404721-khensani-maluleke` | 12 | 923 | 72.5% | 99.2% | 9 | 44.4% |
| `410193-vhugala-makhwathane` | 10 | 751 | 63.6% | 98.6% | 14 | 57.1% |
| `427039-sameeha-miabala` | 10 | 750 | 68.2% | 98.9% | 8 | 50.0% |
| `408501-asher-urison` | 7 | 548 | 69.6% | 99.4% | 7 | 71.4% |
| `420790-damian-nel` | 2 | 156 | 70.5% | 99.3% | 2 | 100.0% |
| `424283-mmathabo-riba` | 2 | 152 | 66.2% | 100.0% | 2 | 100.0% |
| `421349-phathutshedzo-mudzanani` | 19 | 1488 | 73.9% | 99.5% | 10 | 60.0% |
| `427064-khodani-netili` | 19 | 1463 | 67.4% | 99.6% | 20 | 80.0% |
| `388060-tshepang-tshabalala` | 16 | 1228 | 66.1% | 99.5% | 14 | 85.7% |
| `419342-ayeshan-puckree` | 14 | 1073 | 63.2% | 99.7% | 6 | 100.0% |
| `409997-utayan-naidoo` | 13 | 1007 | 63.9% | 98.6% | 19 | 52.6% |
| `402334-angile-saho` | 13 | 1005 | 73.6% | 99.1% | 19 | 73.7% |
| `389160-lwandle-ramanugu` | 13 | 994 | 79.6% | 98.3% | 11 | 54.5% |
| `388828-ngcebo-methula` | 13 | 994 | 69.4% | 99.4% | 10 | 60.0% |
| `423239-zeeshaan-bham` | 13 | 984 | 65.1% | 99.0% | 16 | 68.8% |
| `403339-david-ndambo` | 12 | 931 | 63.3% | 99.7% | 7 | 85.7% |
| `428786-marvellous-sambo` | 12 | 926 | 70.5% | 99.2% | 14 | 57.1% |
| `423436-ntobeko-zondi` | 11 | 846 | 65.9% | 99.5% | 4 | 50.0% |
| `406000-mulimisi-rammela` | 11 | 837 | 65.3% | 99.1% | 6 | 33.3% |
| `421538-tshifhiwa-bvumbi` | 10 | 790 | 74.8% | 99.3% | 6 | 50.0% |
| `419926-mphile-nchabeleng` | 10 | 741 | 73.0% | 99.3% | 6 | 66.7% |
| `426895-mpho-ramasakona` | 9 | 699 | 74.3% | 98.7% | 7 | 42.9% |
| `428954-njabulo-ndlozi` | 9 | 694 | 64.2% | 100.0% | 6 | 100.0% |
| `408008-bradley-buys` | 9 | 684 | 67.8% | 99.5% | 8 | 75.0% |
| `423258-muhammed-dar` | 8 | 614 | 68.0% | 99.7% | 7 | 100.0% |
| `409987-sbongakonke-shange` | 7 | 552 | 70.0% | 99.8% | 13 | 92.3% |

## Observed deaths by cause

Counts are actual `died` replay events, unlike static-space estimates.

| Group | Self-collision | Body collision | Head-to-head | Other |
|---|---:|---:|---:|---:|
| Current top-10 | 35 | 25 | 5 | 0 |
| Other student bots | 126 | 107 | 54 | 0 |
| Built-in benchmarks | 463 | 1068 | 693 | 0 |

Use the death causes to decide whether to first test tail-reachability, body-avoidance, or head-to-head threat rules. Compare on equivalent unseen matches, not raw unadjusted death totals.

## Replay-backed tactical situations

A tradeoff means the most food-directed static-free move had a reachable-space estimate at least 10 tiles smaller than another static-free option. Space scores are **bounded probes**, not exact guarantees.

| Replay | Turn | Snake | Body length | Actual move | Food distance after move | Space score (chosen/best) | Favored space? |
|---|---:|---|---:|---|---:|---:|---|
| [`game-75004.rep`](../replays/2026-11-06-102324-season/game-75004.rep.gz) | 1950 | `421462-alexander-palmer` | 160 | LEFT | 13 | 180/180 | yes |
| [`game-73001.rep`](../replays/2026-11-03-145900-season/game-73001.rep.gz) | 1825 | `421462-alexander-palmer` | 160 | UP | 12 | 180/180 | yes |
| [`game-76004.rep`](../replays/2026-11-03-145900-season/game-76004.rep.gz) | 1900 | `419342-ayeshan-puckree` | 155 | UP | 16 | 175/175 | yes |
| [`game-76007.rep`](../replays/2026-11-03-115900-season/game-76007.rep.gz) | 1750 | `426650-babongile-mafantiri` | 155 | LEFT | 18 | 175/175 | yes |
| [`game-74007.rep`](../replays/2026-11-06-102324-season/game-74007.rep.gz) | 1125 | `421462-alexander-palmer` | 150 | RIGHT | 9 | 170/170 | yes |
| [`game-71004.rep`](../replays/2026-11-06-092316-season/game-71004.rep.gz) | 1600 | `423239-zeeshaan-bham` | 150 | RIGHT | 12 | 170/170 | yes |
| [`game-76004.rep`](../replays/2026-11-03-145900-season/game-76004.rep.gz) | 1850 | `421462-alexander-palmer` | 140 | UP | 20 | 160/160 | yes |
| [`game-73001.rep`](../replays/2026-11-03-145900-season/game-73001.rep.gz) | 1300 | `421462-alexander-palmer` | 140 | UP | 16 | 160/160 | yes |
| [`game-72001.rep`](../replays/2026-11-03-175900-season/game-72001.rep.gz) | 1225 | `421349-phathutshedzo-mudzanani` | 135 | UP | 22 | 155/155 | yes |
| [`game-71002.rep`](../replays/2026-11-03-135900-season/game-71002.rep.gz) | 1750 | `429782-maseeha-seedat` | 135 | RIGHT | 21 | 155/155 | yes |
| [`game-75004.rep`](../replays/2026-11-03-185906-season/game-75004.rep.gz) | 1825 | `426895-mpho-ramasakona` | 120 | RIGHT | 23 | 140/140 | yes |
| [`game-71004.rep`](../replays/2026-11-06-092316-season/game-71004.rep.gz) | 1750 | `409987-sbongakonke-shange` | 110 | UP | 19 | 130/130 | yes |
| [`game-76004.rep`](../replays/2026-11-03-185906-season/game-76004.rep.gz) | 1575 | `421462-alexander-palmer` | 110 | LEFT | 5 | 130/130 | yes |
| [`game-73001.rep`](../replays/2026-11-06-102324-season/game-73001.rep.gz) | 1700 | `429653-elohim-mahungele` | 105 | LEFT | 10 | 125/125 | yes |
| [`game-73001.rep`](../replays/2026-11-06-102324-season/game-73001.rep.gz) | 1825 | `429653-elohim-mahungele` | 105 | RIGHT | 21 | 125/125 | yes |
| [`game-73001.rep`](../replays/2026-11-03-185906-season/game-73001.rep.gz) | 1375 | `389160-lwandle-ramanugu` | 105 | DOWN | 15 | 122/122 | yes |
| [`game-73001.rep`](../replays/2026-11-06-102324-season/game-73001.rep.gz) | 1000 | `402334-angile-saho` | 100 | LEFT | 13 | 120/120 | yes |
| [`game-71004.rep`](../replays/2026-11-06-092316-season/game-71004.rep.gz) | 1675 | `409987-sbongakonke-shange` | 100 | RIGHT | 30 | 120/120 | yes |
| [`game-73001.rep`](../replays/2026-11-03-145900-season/game-73001.rep.gz) | 900 | `423239-zeeshaan-bham` | 100 | UP | 30 | 120/120 | yes |
| [`game-73000.rep`](../replays/2026-11-03-115900-season/game-73000.rep.gz) | 850 | `421462-alexander-palmer` | 100 | LEFT | 14 | 120/120 | yes |
| [`trials/426895-mpho-ramasakona/trial-912000.rep`](../replays/2026-11-03-185906-season/trials/426895-mpho-ramasakona/trial-912000.rep.gz) | 1175 | `~survivor` | 95 | DOWN | 30 | 115/115 | yes |
| [`trials/408008-bradley-buys/trial-912000.rep`](../replays/2026-11-03-185906-season/trials/408008-bradley-buys/trial-912000.rep.gz) | 1850 | `~gauntlet_1` | 95 | RIGHT | 7 | 115/115 | yes |
| [`game-75004.rep`](../replays/2026-11-03-185906-season/game-75004.rep.gz) | 1150 | `429782-maseeha-seedat` | 95 | RIGHT | 14 | 115/115 | yes |
| [`game-71000.rep`](../replays/2026-11-03-145900-season/game-71000.rep.gz) | 800 | `403501-mashau-mudzanani` | 95 | UP | 30 | 115/115 | yes |

## Historical hypotheses for later investigation (NO implementation yet)

1. **Food-versus-space planner:** Assign each candidate move a weighted score for distance to food and bounded flood-fill space. Compare against current Java bot, using the same fresh seeds.
2. **Danger override:** When a candidate leads to constrained reachable space, temporarily prioritize escape over food; test ablation with/without the override.
3. **Opponent-pressure rule:** Test threat-aware movement when an opponent head is within three toroidal tiles. The current report counts proximity but does not yet recover opponent intent.
4. **Policy imitation experiment:** Use replay states as labeled observations for relative actions, holding out entire matches and seasons for validation. High next-move accuracy alone is *not* proof of better game performance.

Only promote a strategy if it improves **held-out match outcomes** and survival with equivalent opponent setups. Collect more samples before trusting patterns from individual snakes.
