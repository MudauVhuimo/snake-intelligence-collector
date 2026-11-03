# Snake26: are risk and food opportunities state-dependent?

Generated UTC: 2026-11-03T19:57:17+00:00

## Study design and missingness

For each living STUDENT at turns divisible by 25, use only features
visible at that turn: body length, full occupied-cell fraction (including
obstacles), nearest opponent head distance and turn phase. Require 10
consecutive future frames and classify actual death events (not being
alive at the final frame after respawn). Count actual apple events only
UNTIL first death. Cohorts below are DESCRIPTIVE; they do not measure
what a changed decision would do. Student peer league and fixed trials
are never pooled for inferential comparisons.

Density bands fixed BEFORE viewing results: <15%, 15-<30%, >=30%.
Phases: turns 0-499, 500-1499, 1500+; length bands: 5-24, 25-49, 50-99, 100+.
All density is instantaneous arena occupancy, not a measured
probability of a path becoming blocked.

Unique peer league replays: **97**; trial replays: **82**.
Observed complete 10-turn windows: **37276**;
league **30719**,
trials **6557**.
Duplicate replay payloads removed: **71**.

## Stratified actual outcomes

Death percentage is DIED within next 10 turns / eligible windows;
food rate is confirmed eats before any death / 100 eligible windows.
Nearby repeated windows and the same students make the raw fractions
correlated. **No cross-row causal effect claim**.

### Body length

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ | 7044 | 97 | 57 | 0.81% | 12.11 |
| league | 25-49 | 6698 | 97 | 33 | 0.49% | 16.14 |
| league | 5-24 | 6732 | 97 | 23 | 0.34% | 16.93 |
| league | 50-99 | 10245 | 97 | 58 | 0.57% | 13.79 |
| trial | 100+ | 3668 | 82 | 5 | 0.14% | 17.09 |
| trial | 25-49 | 760 | 82 | 1 | 0.13% | 28.03 |
| trial | 5-24 | 643 | 82 | 0 | 0.00% | 24.42 |
| trial | 50-99 | 1486 | 82 | 2 | 0.13% | 25.57 |

### Arena occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | high_>=30% | 2991 | 66 | 40 | 1.34% | 9.70 |
| league | low_<15% | 7231 | 97 | 9 | 0.12% | 20.44 |
| league | mid_15-30% | 20497 | 97 | 122 | 0.60% | 13.27 |
| trial | high_>=30% | 2 | 1 | 0 | 0.00% | 50.00 |
| trial | low_<15% | 3528 | 82 | 3 | 0.09% | 24.01 |
| trial | mid_15-30% | 3027 | 81 | 5 | 0.17% | 17.48 |

### Game phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | early_0-499 | 7701 | 97 | 8 | 0.10% | 20.17 |
| league | late_1500+ | 7671 | 97 | 58 | 0.76% | 11.24 |
| league | middle_500-1499 | 15347 | 97 | 105 | 0.68% | 13.50 |
| trial | early_0-499 | 1640 | 82 | 1 | 0.06% | 26.28 |
| trial | late_1500+ | 1639 | 82 | 3 | 0.18% | 16.78 |
| trial | middle_500-1499 | 3278 | 82 | 4 | 0.12% | 20.47 |

### Length × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / high_>=30% | 1648 | 66 | 22 | 1.33% | 9.71 |
| league | 100+ / low_<15% | 53 | 19 | 1 | 1.89% | 18.87 |
| league | 100+ / mid_15-30% | 5343 | 97 | 34 | 0.64% | 12.78 |
| league | 25-49 / high_>=30% | 318 | 42 | 6 | 1.89% | 9.12 |
| league | 25-49 / low_<15% | 2960 | 97 | 3 | 0.10% | 20.68 |
| league | 25-49 / mid_15-30% | 3420 | 97 | 24 | 0.70% | 12.87 |
| league | 5-24 / high_>=30% | 225 | 33 | 3 | 1.33% | 12.44 |
| league | 5-24 / low_<15% | 3343 | 97 | 5 | 0.15% | 20.85 |
| league | 5-24 / mid_15-30% | 3164 | 96 | 15 | 0.47% | 13.12 |
| league | 50-99 / high_>=30% | 800 | 61 | 9 | 1.12% | 9.12 |
| league | 50-99 / low_<15% | 875 | 96 | 0 | 0.00% | 18.17 |
| league | 50-99 / mid_15-30% | 8570 | 97 | 49 | 0.57% | 13.78 |
| trial | 100+ / low_<15% | 858 | 76 | 1 | 0.12% | 17.25 |
| trial | 100+ / mid_15-30% | 2808 | 81 | 4 | 0.14% | 17.02 |
| trial | 25-49 / low_<15% | 753 | 82 | 1 | 0.13% | 27.49 |
| trial | 5-24 / low_<15% | 643 | 82 | 0 | 0.00% | 24.42 |
| trial | 50-99 / low_<15% | 1274 | 82 | 1 | 0.08% | 26.30 |
| trial | 50-99 / mid_15-30% | 212 | 40 | 1 | 0.47% | 21.23 |

### Length × phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / late_1500+ | 3071 | 96 | 22 | 0.72% | 11.23 |
| league | 100+ / middle_500-1499 | 3966 | 96 | 35 | 0.88% | 12.81 |
| league | 25-49 / early_0-499 | 3274 | 97 | 3 | 0.09% | 20.19 |
| league | 25-49 / late_1500+ | 1368 | 86 | 14 | 1.02% | 10.96 |
| league | 25-49 / middle_500-1499 | 2056 | 94 | 16 | 0.78% | 13.13 |
| league | 5-24 / early_0-499 | 2968 | 97 | 4 | 0.13% | 21.23 |
| league | 5-24 / late_1500+ | 1666 | 94 | 9 | 0.54% | 12.12 |
| league | 5-24 / middle_500-1499 | 2098 | 93 | 10 | 0.48% | 14.68 |
| league | 50-99 / early_0-499 | 1452 | 97 | 1 | 0.07% | 18.04 |
| league | 50-99 / late_1500+ | 1566 | 82 | 13 | 0.83% | 10.54 |
| league | 50-99 / middle_500-1499 | 7227 | 97 | 44 | 0.61% | 13.64 |
| trial | 100+ / late_1500+ | 1415 | 78 | 3 | 0.21% | 15.55 |
| trial | 100+ / middle_500-1499 | 2250 | 79 | 2 | 0.09% | 18.09 |
| trial | 25-49 / early_0-499 | 630 | 82 | 1 | 0.16% | 27.94 |
| trial | 25-49 / late_1500+ | 54 | 9 | 0 | 0.00% | 25.93 |
| trial | 25-49 / middle_500-1499 | 76 | 14 | 0 | 0.00% | 30.26 |
| trial | 5-24 / early_0-499 | 536 | 82 | 0 | 0.00% | 22.95 |
| trial | 5-24 / late_1500+ | 46 | 10 | 0 | 0.00% | 26.09 |
| trial | 5-24 / middle_500-1499 | 61 | 10 | 0 | 0.00% | 36.07 |
| trial | 50-99 / early_0-499 | 471 | 74 | 0 | 0.00% | 28.03 |
| trial | 50-99 / late_1500+ | 124 | 12 | 0 | 0.00% | 23.39 |
| trial | 50-99 / middle_500-1499 | 891 | 80 | 2 | 0.22% | 24.58 |

### Head proximity × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | far_8_plus / high_>=30% | 2238 | 66 | 20 | 0.89% | 10.55 |
| league | far_8_plus / low_<15% | 5679 | 97 | 4 | 0.07% | 20.76 |
| league | far_8_plus / mid_15-30% | 14599 | 97 | 45 | 0.31% | 14.39 |
| league | middle_4_7 / high_>=30% | 503 | 57 | 9 | 1.79% | 8.35 |
| league | middle_4_7 / low_<15% | 1199 | 97 | 2 | 0.17% | 19.93 |
| league | middle_4_7 / mid_15-30% | 4166 | 97 | 33 | 0.79% | 10.78 |
| league | near_0_3 / high_>=30% | 250 | 48 | 11 | 4.40% | 4.80 |
| league | near_0_3 / low_<15% | 353 | 69 | 3 | 0.85% | 17.00 |
| league | near_0_3 / mid_15-30% | 1732 | 97 | 44 | 2.54% | 9.76 |
| trial | far_8_plus / low_<15% | 2476 | 82 | 1 | 0.04% | 23.18 |
| trial | far_8_plus / mid_15-30% | 2237 | 81 | 3 | 0.13% | 16.05 |
| trial | middle_4_7 / low_<15% | 728 | 81 | 0 | 0.00% | 26.24 |
| trial | middle_4_7 / mid_15-30% | 585 | 78 | 1 | 0.17% | 24.27 |
| trial | near_0_3 / low_<15% | 324 | 78 | 2 | 0.62% | 25.31 |
| trial | near_0_3 / mid_15-30% | 205 | 71 | 1 | 0.49% | 13.66 |

## Palmer as reference subset, not population replacement

Palmer league windows: **2798** / **30719** league windows;
death events in next 10: **6**;
observed apple events before death: **520**.
Selected games/versions are not a matched estimate of Palmer's
causal strategy or an appropriate single-opponent benchmark.

## What this can and cannot conclude

- State/length/density/phase interactions are measurable; raw group
  differences justify TESTING an adaptive score, not choosing weights.
- A crowded phase may correlate with long bodies and better peers;
  the rate differences do NOT isolate density itself.
- Small cells, rare deaths and repeated snapshots can yield unstable
  risks. Censoring at match end is handled by requiring full followup.
- To advance beyond observation, fit/validate pre-action interaction
  predictors on whole held-out seasons/games, then compare adaptive
  versus fixed-weight Java agents on fresh paired seeds.

[Auditable window-level export](../derived/adaptive_state_windows.csv).
**No new game-playing policy has been proved by these observations.**
