# Snake26: are risk and food opportunities state-dependent?

Generated UTC: 2026-11-03T04:09:40+00:00

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

Unique peer league replays: **75**; trial replays: **66**.
Observed complete 10-turn windows: **29054**;
league **23777**,
trials **5277**.
Duplicate replay payloads removed: **69**.

## Stratified actual outcomes

Death percentage is DIED within next 10 turns / eligible windows;
food rate is confirmed eats before any death / 100 eligible windows.
Nearby repeated windows and the same students make the raw fractions
correlated. **No cross-row causal effect claim**.

### Body length

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ | 5394 | 75 | 39 | 0.72% | 11.77 |
| league | 25-49 | 5161 | 75 | 26 | 0.50% | 16.33 |
| league | 5-24 | 5283 | 75 | 15 | 0.28% | 16.58 |
| league | 50-99 | 7939 | 75 | 47 | 0.59% | 13.64 |
| trial | 100+ | 3033 | 66 | 3 | 0.10% | 17.51 |
| trial | 25-49 | 602 | 66 | 1 | 0.17% | 28.07 |
| trial | 5-24 | 499 | 66 | 0 | 0.00% | 25.45 |
| trial | 50-99 | 1143 | 66 | 2 | 0.17% | 26.86 |

### Arena occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | high_>=30% | 2252 | 51 | 25 | 1.11% | 9.90 |
| league | low_<15% | 5621 | 75 | 8 | 0.14% | 20.07 |
| league | mid_15-30% | 15904 | 75 | 94 | 0.59% | 13.12 |
| trial | low_<15% | 2779 | 66 | 3 | 0.11% | 24.51 |
| trial | mid_15-30% | 2498 | 65 | 3 | 0.12% | 18.13 |

### Game phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | early_0-499 | 5961 | 75 | 6 | 0.10% | 19.85 |
| league | late_1500+ | 5935 | 75 | 42 | 0.71% | 11.27 |
| league | middle_500-1499 | 11881 | 75 | 79 | 0.66% | 13.34 |
| trial | early_0-499 | 1320 | 66 | 1 | 0.08% | 26.52 |
| trial | late_1500+ | 1319 | 66 | 1 | 0.08% | 17.44 |
| trial | middle_500-1499 | 2638 | 66 | 4 | 0.15% | 21.00 |

### Length × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / high_>=30% | 1211 | 51 | 11 | 0.91% | 9.66 |
| league | 100+ / low_<15% | 40 | 13 | 1 | 2.50% | 25.00 |
| league | 100+ / mid_15-30% | 4143 | 75 | 27 | 0.65% | 12.26 |
| league | 25-49 / high_>=30% | 233 | 33 | 4 | 1.72% | 11.16 |
| league | 25-49 / low_<15% | 2329 | 75 | 3 | 0.13% | 20.22 |
| league | 25-49 / mid_15-30% | 2599 | 75 | 19 | 0.73% | 13.31 |
| league | 5-24 / high_>=30% | 178 | 26 | 2 | 1.12% | 12.36 |
| league | 5-24 / low_<15% | 2584 | 75 | 4 | 0.15% | 20.63 |
| league | 5-24 / mid_15-30% | 2521 | 75 | 9 | 0.36% | 12.73 |
| league | 50-99 / high_>=30% | 630 | 46 | 8 | 1.27% | 9.21 |
| league | 50-99 / low_<15% | 668 | 74 | 0 | 0.00% | 17.07 |
| league | 50-99 / mid_15-30% | 6641 | 75 | 39 | 0.59% | 13.72 |
| trial | 100+ / low_<15% | 679 | 62 | 1 | 0.15% | 17.23 |
| trial | 100+ / mid_15-30% | 2354 | 65 | 2 | 0.08% | 17.59 |
| trial | 25-49 / low_<15% | 597 | 66 | 1 | 0.17% | 27.64 |
| trial | 5-24 / low_<15% | 499 | 66 | 0 | 0.00% | 25.45 |
| trial | 50-99 / low_<15% | 1004 | 66 | 1 | 0.10% | 27.09 |
| trial | 50-99 / mid_15-30% | 139 | 29 | 1 | 0.72% | 25.18 |

### Length × phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / late_1500+ | 2399 | 74 | 14 | 0.58% | 10.92 |
| league | 100+ / middle_500-1499 | 2990 | 74 | 25 | 0.84% | 12.47 |
| league | 25-49 / early_0-499 | 2544 | 75 | 3 | 0.12% | 19.93 |
| league | 25-49 / late_1500+ | 1051 | 68 | 12 | 1.14% | 11.70 |
| league | 25-49 / middle_500-1499 | 1566 | 72 | 11 | 0.70% | 13.60 |
| league | 5-24 / early_0-499 | 2306 | 75 | 3 | 0.13% | 20.99 |
| league | 5-24 / late_1500+ | 1254 | 72 | 5 | 0.40% | 12.36 |
| league | 5-24 / middle_500-1499 | 1723 | 72 | 7 | 0.41% | 13.76 |
| league | 50-99 / early_0-499 | 1106 | 75 | 0 | 0.00% | 17.36 |
| league | 50-99 / late_1500+ | 1231 | 63 | 11 | 0.89% | 10.48 |
| league | 50-99 / middle_500-1499 | 5602 | 75 | 36 | 0.64% | 13.60 |
| trial | 100+ / late_1500+ | 1164 | 62 | 1 | 0.09% | 16.24 |
| trial | 100+ / middle_500-1499 | 1868 | 64 | 2 | 0.11% | 18.31 |
| trial | 25-49 / early_0-499 | 508 | 66 | 1 | 0.20% | 27.56 |
| trial | 25-49 / middle_500-1499 | 65 | 12 | 0 | 0.00% | 32.31 |
| trial | 5-24 / early_0-499 | 418 | 66 | 0 | 0.00% | 23.92 |
| trial | 5-24 / middle_500-1499 | 53 | 8 | 0 | 0.00% | 35.85 |
| trial | 50-99 / early_0-499 | 393 | 60 | 0 | 0.00% | 27.99 |
| trial | 50-99 / late_1500+ | 98 | 8 | 0 | 0.00% | 25.51 |
| trial | 50-99 / middle_500-1499 | 652 | 65 | 2 | 0.31% | 26.38 |

### Head proximity × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | far_8_plus / high_>=30% | 1690 | 51 | 11 | 0.65% | 10.77 |
| league | far_8_plus / low_<15% | 4376 | 75 | 4 | 0.09% | 20.45 |
| league | far_8_plus / mid_15-30% | 11332 | 75 | 40 | 0.35% | 14.18 |
| league | middle_4_7 / high_>=30% | 380 | 42 | 7 | 1.84% | 8.16 |
| league | middle_4_7 / low_<15% | 963 | 75 | 2 | 0.21% | 19.21 |
| league | middle_4_7 / mid_15-30% | 3272 | 75 | 23 | 0.70% | 11.00 |
| league | near_0_3 / high_>=30% | 182 | 36 | 7 | 3.85% | 5.49 |
| league | near_0_3 / low_<15% | 282 | 52 | 2 | 0.71% | 17.02 |
| league | near_0_3 / mid_15-30% | 1300 | 75 | 31 | 2.38% | 9.15 |
| trial | far_8_plus / low_<15% | 1955 | 66 | 1 | 0.05% | 23.63 |
| trial | far_8_plus / mid_15-30% | 1862 | 65 | 2 | 0.11% | 16.22 |
| trial | middle_4_7 / low_<15% | 562 | 65 | 0 | 0.00% | 26.69 |
| trial | middle_4_7 / mid_15-30% | 478 | 64 | 0 | 0.00% | 26.57 |
| trial | near_0_3 / low_<15% | 262 | 63 | 2 | 0.76% | 26.34 |
| trial | near_0_3 / mid_15-30% | 158 | 57 | 1 | 0.63% | 15.19 |

## Palmer as reference subset, not population replacement

Palmer league windows: **1759** / **23777** league windows;
death events in next 10: **3**;
observed apple events before death: **323**.
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
