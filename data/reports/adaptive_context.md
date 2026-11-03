# Snake26: are risk and food opportunities state-dependent?

Generated UTC: 2026-11-03T06:59:43+00:00

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

Unique peer league replays: **80**; trial replays: **70**.
Observed complete 10-turn windows: **30966**;
league **25369**,
trials **5597**.
Duplicate replay payloads removed: **70**.

## Stratified actual outcomes

Death percentage is DIED within next 10 turns / eligible windows;
food rate is confirmed eats before any death / 100 eligible windows.
Nearby repeated windows and the same students make the raw fractions
correlated. **No cross-row causal effect claim**.

### Body length

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ | 5780 | 80 | 42 | 0.73% | 11.90 |
| league | 25-49 | 5530 | 80 | 29 | 0.52% | 16.20 |
| league | 5-24 | 5646 | 80 | 17 | 0.30% | 16.58 |
| league | 50-99 | 8413 | 80 | 49 | 0.58% | 13.74 |
| trial | 100+ | 3188 | 70 | 3 | 0.09% | 17.35 |
| trial | 25-49 | 645 | 70 | 1 | 0.16% | 27.60 |
| trial | 5-24 | 528 | 70 | 0 | 0.00% | 25.38 |
| trial | 50-99 | 1236 | 70 | 2 | 0.16% | 26.38 |

### Arena occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | high_>=30% | 2408 | 55 | 28 | 1.16% | 9.84 |
| league | low_<15% | 6030 | 80 | 8 | 0.13% | 20.13 |
| league | mid_15-30% | 16931 | 80 | 101 | 0.60% | 13.14 |
| trial | low_<15% | 2984 | 70 | 3 | 0.10% | 24.33 |
| trial | mid_15-30% | 2613 | 69 | 3 | 0.11% | 17.80 |

### Game phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | early_0-499 | 6360 | 80 | 6 | 0.09% | 19.81 |
| league | late_1500+ | 6332 | 80 | 45 | 0.71% | 11.47 |
| league | middle_500-1499 | 12677 | 80 | 86 | 0.68% | 13.33 |
| trial | early_0-499 | 1400 | 70 | 1 | 0.07% | 26.36 |
| trial | late_1500+ | 1399 | 70 | 1 | 0.07% | 17.16 |
| trial | middle_500-1499 | 2798 | 70 | 4 | 0.14% | 20.80 |

### Length × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / high_>=30% | 1291 | 55 | 12 | 0.93% | 9.68 |
| league | 100+ / low_<15% | 41 | 14 | 1 | 2.44% | 24.39 |
| league | 100+ / mid_15-30% | 4448 | 80 | 29 | 0.65% | 12.43 |
| league | 25-49 / high_>=30% | 268 | 37 | 5 | 1.87% | 9.70 |
| league | 25-49 / low_<15% | 2463 | 80 | 3 | 0.12% | 20.63 |
| league | 25-49 / mid_15-30% | 2799 | 80 | 21 | 0.75% | 12.93 |
| league | 5-24 / high_>=30% | 195 | 29 | 3 | 1.54% | 12.82 |
| league | 5-24 / low_<15% | 2786 | 80 | 4 | 0.14% | 20.42 |
| league | 5-24 / mid_15-30% | 2665 | 80 | 10 | 0.38% | 12.83 |
| league | 50-99 / high_>=30% | 654 | 50 | 8 | 1.22% | 9.33 |
| league | 50-99 / low_<15% | 740 | 79 | 0 | 0.00% | 17.16 |
| league | 50-99 / mid_15-30% | 7019 | 80 | 41 | 0.58% | 13.79 |
| trial | 100+ / low_<15% | 732 | 66 | 1 | 0.14% | 17.49 |
| trial | 100+ / mid_15-30% | 2456 | 69 | 2 | 0.08% | 17.30 |
| trial | 25-49 / low_<15% | 640 | 70 | 1 | 0.16% | 27.19 |
| trial | 5-24 / low_<15% | 528 | 70 | 0 | 0.00% | 25.38 |
| trial | 50-99 / low_<15% | 1084 | 70 | 1 | 0.09% | 26.75 |
| trial | 50-99 / mid_15-30% | 152 | 31 | 1 | 0.66% | 23.68 |

### Length × phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / late_1500+ | 2573 | 79 | 15 | 0.58% | 11.31 |
| league | 100+ / middle_500-1499 | 3202 | 79 | 27 | 0.84% | 12.40 |
| league | 25-49 / early_0-499 | 2694 | 80 | 3 | 0.11% | 20.16 |
| league | 25-49 / late_1500+ | 1129 | 73 | 12 | 1.06% | 11.51 |
| league | 25-49 / middle_500-1499 | 1707 | 77 | 14 | 0.82% | 13.06 |
| league | 5-24 / early_0-499 | 2477 | 80 | 3 | 0.12% | 20.83 |
| league | 5-24 / late_1500+ | 1360 | 77 | 7 | 0.51% | 12.43 |
| league | 5-24 / middle_500-1499 | 1809 | 77 | 7 | 0.39% | 13.88 |
| league | 50-99 / early_0-499 | 1184 | 80 | 0 | 0.00% | 16.98 |
| league | 50-99 / late_1500+ | 1270 | 68 | 11 | 0.87% | 10.71 |
| league | 50-99 / middle_500-1499 | 5959 | 80 | 38 | 0.64% | 13.74 |
| trial | 100+ / late_1500+ | 1229 | 66 | 1 | 0.08% | 16.11 |
| trial | 100+ / middle_500-1499 | 1958 | 67 | 2 | 0.10% | 18.13 |
| trial | 25-49 / early_0-499 | 542 | 70 | 1 | 0.18% | 27.12 |
| trial | 25-49 / middle_500-1499 | 74 | 13 | 0 | 0.00% | 31.08 |
| trial | 5-24 / early_0-499 | 441 | 70 | 0 | 0.00% | 24.04 |
| trial | 5-24 / middle_500-1499 | 59 | 9 | 0 | 0.00% | 33.90 |
| trial | 50-99 / early_0-499 | 416 | 64 | 0 | 0.00% | 27.88 |
| trial | 50-99 / late_1500+ | 113 | 9 | 0 | 0.00% | 23.01 |
| trial | 50-99 / middle_500-1499 | 707 | 69 | 2 | 0.28% | 26.03 |

### Head proximity × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | far_8_plus / high_>=30% | 1810 | 55 | 14 | 0.77% | 10.66 |
| league | far_8_plus / low_<15% | 4712 | 80 | 4 | 0.08% | 20.46 |
| league | far_8_plus / mid_15-30% | 12068 | 80 | 40 | 0.33% | 14.25 |
| league | middle_4_7 / high_>=30% | 398 | 46 | 7 | 1.76% | 8.29 |
| league | middle_4_7 / low_<15% | 1020 | 80 | 2 | 0.20% | 19.61 |
| league | middle_4_7 / mid_15-30% | 3466 | 80 | 26 | 0.75% | 10.73 |
| league | near_0_3 / high_>=30% | 200 | 39 | 7 | 3.50% | 5.50 |
| league | near_0_3 / low_<15% | 298 | 56 | 2 | 0.67% | 16.78 |
| league | near_0_3 / mid_15-30% | 1397 | 80 | 35 | 2.51% | 9.52 |
| trial | far_8_plus / low_<15% | 2093 | 70 | 1 | 0.05% | 23.55 |
| trial | far_8_plus / mid_15-30% | 1946 | 69 | 2 | 0.10% | 15.98 |
| trial | middle_4_7 / low_<15% | 612 | 69 | 0 | 0.00% | 25.98 |
| trial | middle_4_7 / mid_15-30% | 497 | 67 | 0 | 0.00% | 26.16 |
| trial | near_0_3 / low_<15% | 279 | 67 | 2 | 0.72% | 26.52 |
| trial | near_0_3 / mid_15-30% | 170 | 61 | 1 | 0.59% | 14.12 |

## Palmer as reference subset, not population replacement

Palmer league windows: **1839** / **25369** league windows;
death events in next 10: **3**;
observed apple events before death: **342**.
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
