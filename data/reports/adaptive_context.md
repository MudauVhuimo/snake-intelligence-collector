# Snake26: are risk and food opportunities state-dependent?

Generated UTC: 2026-11-03T15:21:36+00:00

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

Unique peer league replays: **91**; trial replays: **78**.
Observed complete 10-turn windows: **35039**;
league **28802**,
trials **6237**.
Duplicate replay payloads removed: **71**.

## Stratified actual outcomes

Death percentage is DIED within next 10 turns / eligible windows;
food rate is confirmed eats before any death / 100 eligible windows.
Nearby repeated windows and the same students make the raw fractions
correlated. **No cross-row causal effect claim**.

### Body length

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ | 6633 | 91 | 51 | 0.77% | 11.99 |
| league | 25-49 | 6222 | 91 | 32 | 0.51% | 16.46 |
| league | 5-24 | 6341 | 91 | 22 | 0.35% | 16.69 |
| league | 50-99 | 9606 | 91 | 56 | 0.58% | 13.67 |
| trial | 100+ | 3496 | 78 | 4 | 0.11% | 17.11 |
| trial | 25-49 | 721 | 78 | 1 | 0.14% | 27.32 |
| trial | 5-24 | 606 | 78 | 0 | 0.00% | 24.75 |
| trial | 50-99 | 1414 | 78 | 2 | 0.14% | 25.46 |

### Arena occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | high_>=30% | 2863 | 62 | 35 | 1.22% | 9.81 |
| league | low_<15% | 6815 | 91 | 9 | 0.13% | 20.34 |
| league | mid_15-30% | 19124 | 91 | 117 | 0.61% | 13.19 |
| trial | low_<15% | 3376 | 78 | 3 | 0.09% | 23.82 |
| trial | mid_15-30% | 2861 | 77 | 4 | 0.14% | 17.51 |

### Game phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | early_0-499 | 7221 | 91 | 8 | 0.11% | 20.01 |
| league | late_1500+ | 7191 | 91 | 57 | 0.79% | 11.25 |
| league | middle_500-1499 | 14390 | 91 | 96 | 0.67% | 13.45 |
| trial | early_0-499 | 1560 | 78 | 1 | 0.06% | 26.09 |
| trial | late_1500+ | 1559 | 78 | 2 | 0.13% | 16.87 |
| trial | middle_500-1499 | 3118 | 78 | 4 | 0.13% | 20.37 |

### Length × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / high_>=30% | 1582 | 62 | 18 | 1.14% | 9.73 |
| league | 100+ / low_<15% | 45 | 16 | 1 | 2.22% | 22.22 |
| league | 100+ / mid_15-30% | 5006 | 91 | 32 | 0.64% | 12.60 |
| league | 25-49 / high_>=30% | 294 | 40 | 5 | 1.70% | 9.86 |
| league | 25-49 / low_<15% | 2793 | 91 | 3 | 0.11% | 20.69 |
| league | 25-49 / mid_15-30% | 3135 | 91 | 24 | 0.77% | 13.30 |
| league | 5-24 / high_>=30% | 224 | 32 | 3 | 1.34% | 12.05 |
| league | 5-24 / low_<15% | 3138 | 91 | 5 | 0.16% | 20.59 |
| league | 5-24 / mid_15-30% | 2979 | 90 | 14 | 0.47% | 12.92 |
| league | 50-99 / high_>=30% | 763 | 57 | 9 | 1.18% | 9.31 |
| league | 50-99 / low_<15% | 839 | 90 | 0 | 0.00% | 18.12 |
| league | 50-99 / mid_15-30% | 8004 | 91 | 47 | 0.59% | 13.62 |
| trial | 100+ / low_<15% | 827 | 73 | 1 | 0.12% | 17.05 |
| trial | 100+ / mid_15-30% | 2669 | 77 | 3 | 0.11% | 17.12 |
| trial | 25-49 / low_<15% | 716 | 78 | 1 | 0.14% | 26.96 |
| trial | 5-24 / low_<15% | 606 | 78 | 0 | 0.00% | 24.75 |
| trial | 50-99 / low_<15% | 1227 | 78 | 1 | 0.08% | 26.08 |
| trial | 50-99 / mid_15-30% | 187 | 37 | 1 | 0.53% | 21.39 |

### Length × phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / late_1500+ | 2927 | 90 | 21 | 0.72% | 11.21 |
| league | 100+ / middle_500-1499 | 3699 | 90 | 30 | 0.81% | 12.63 |
| league | 25-49 / early_0-499 | 3072 | 91 | 3 | 0.10% | 20.25 |
| league | 25-49 / late_1500+ | 1228 | 80 | 14 | 1.14% | 11.64 |
| league | 25-49 / middle_500-1499 | 1922 | 88 | 15 | 0.78% | 13.48 |
| league | 5-24 / early_0-499 | 2791 | 91 | 4 | 0.14% | 20.96 |
| league | 5-24 / late_1500+ | 1567 | 88 | 9 | 0.57% | 12.06 |
| league | 5-24 / middle_500-1499 | 1983 | 87 | 9 | 0.45% | 14.32 |
| league | 50-99 / early_0-499 | 1351 | 91 | 1 | 0.07% | 17.62 |
| league | 50-99 / late_1500+ | 1469 | 77 | 13 | 0.88% | 10.14 |
| league | 50-99 / middle_500-1499 | 6786 | 91 | 42 | 0.62% | 13.65 |
| trial | 100+ / late_1500+ | 1348 | 74 | 2 | 0.15% | 15.73 |
| trial | 100+ / middle_500-1499 | 2145 | 75 | 2 | 0.09% | 18.00 |
| trial | 25-49 / early_0-499 | 601 | 78 | 1 | 0.17% | 27.12 |
| trial | 25-49 / late_1500+ | 46 | 8 | 0 | 0.00% | 23.91 |
| trial | 25-49 / middle_500-1499 | 74 | 13 | 0 | 0.00% | 31.08 |
| trial | 5-24 / early_0-499 | 503 | 78 | 0 | 0.00% | 23.26 |
| trial | 5-24 / late_1500+ | 42 | 9 | 0 | 0.00% | 26.19 |
| trial | 5-24 / middle_500-1499 | 61 | 10 | 0 | 0.00% | 36.07 |
| trial | 50-99 / early_0-499 | 453 | 71 | 0 | 0.00% | 28.04 |
| trial | 50-99 / late_1500+ | 123 | 11 | 0 | 0.00% | 23.58 |
| trial | 50-99 / middle_500-1499 | 838 | 76 | 2 | 0.24% | 24.34 |

### Head proximity × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | far_8_plus / high_>=30% | 2146 | 62 | 16 | 0.75% | 10.62 |
| league | far_8_plus / low_<15% | 5367 | 91 | 4 | 0.07% | 20.64 |
| league | far_8_plus / mid_15-30% | 13631 | 91 | 44 | 0.32% | 14.35 |
| league | middle_4_7 / high_>=30% | 475 | 53 | 8 | 1.68% | 8.63 |
| league | middle_4_7 / low_<15% | 1113 | 91 | 2 | 0.18% | 19.86 |
| league | middle_4_7 / mid_15-30% | 3882 | 91 | 32 | 0.82% | 10.61 |
| league | near_0_3 / high_>=30% | 242 | 46 | 11 | 4.55% | 4.96 |
| league | near_0_3 / low_<15% | 335 | 64 | 3 | 0.90% | 17.01 |
| league | near_0_3 / mid_15-30% | 1611 | 91 | 41 | 2.55% | 9.62 |
| trial | far_8_plus / low_<15% | 2385 | 78 | 1 | 0.04% | 22.94 |
| trial | far_8_plus / mid_15-30% | 2109 | 77 | 2 | 0.09% | 15.93 |
| trial | middle_4_7 / low_<15% | 688 | 77 | 0 | 0.00% | 26.16 |
| trial | middle_4_7 / mid_15-30% | 553 | 74 | 1 | 0.18% | 24.77 |
| trial | near_0_3 / low_<15% | 303 | 74 | 2 | 0.66% | 25.41 |
| trial | near_0_3 / mid_15-30% | 199 | 68 | 1 | 0.50% | 14.07 |

## Palmer as reference subset, not population replacement

Palmer league windows: **2478** / **28802** league windows;
death events in next 10: **4**;
observed apple events before death: **456**.
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
