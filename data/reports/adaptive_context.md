# Snake26: are risk and food opportunities state-dependent?

Generated UTC: 2026-11-06T11:06:28+00:00

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

Unique peer league replays: **102**; trial replays: **79**.
Observed complete 10-turn windows: **38636**;
league **32317**,
trials **6319**.
Duplicate replay payloads removed: **69**.

## Stratified actual outcomes

Death percentage is DIED within next 10 turns / eligible windows;
food rate is confirmed eats before any death / 100 eligible windows.
Nearby repeated windows and the same students make the raw fractions
correlated. **No cross-row causal effect claim**.

### Body length

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ | 7462 | 102 | 62 | 0.83% | 12.11 |
| league | 25-49 | 6980 | 102 | 33 | 0.47% | 16.26 |
| league | 5-24 | 7059 | 102 | 23 | 0.33% | 16.93 |
| league | 50-99 | 10816 | 102 | 61 | 0.56% | 13.83 |
| trial | 100+ | 3554 | 79 | 4 | 0.11% | 16.77 |
| trial | 25-49 | 733 | 79 | 1 | 0.14% | 27.42 |
| trial | 5-24 | 608 | 79 | 0 | 0.00% | 24.34 |
| trial | 50-99 | 1424 | 79 | 1 | 0.07% | 25.35 |

### Arena occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | high_>=30% | 3227 | 71 | 44 | 1.36% | 9.92 |
| league | low_<15% | 7571 | 102 | 9 | 0.12% | 20.50 |
| league | mid_15-30% | 21519 | 102 | 126 | 0.59% | 13.28 |
| trial | high_>=30% | 2 | 1 | 0 | 0.00% | 50.00 |
| trial | low_<15% | 3371 | 79 | 1 | 0.03% | 23.76 |
| trial | mid_15-30% | 2946 | 78 | 5 | 0.17% | 17.11 |

### Game phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | early_0-499 | 8101 | 102 | 8 | 0.10% | 20.15 |
| league | late_1500+ | 8070 | 102 | 60 | 0.74% | 11.28 |
| league | middle_500-1499 | 16146 | 102 | 111 | 0.69% | 13.55 |
| trial | early_0-499 | 1580 | 79 | 1 | 0.06% | 26.52 |
| trial | late_1500+ | 1580 | 79 | 3 | 0.19% | 15.82 |
| trial | middle_500-1499 | 3159 | 79 | 2 | 0.06% | 20.16 |

### Length × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / high_>=30% | 1788 | 71 | 25 | 1.40% | 9.79 |
| league | 100+ / low_<15% | 57 | 20 | 1 | 1.75% | 19.30 |
| league | 100+ / mid_15-30% | 5617 | 102 | 36 | 0.64% | 12.78 |
| league | 25-49 / high_>=30% | 345 | 45 | 6 | 1.74% | 8.99 |
| league | 25-49 / low_<15% | 3097 | 102 | 3 | 0.10% | 20.70 |
| league | 25-49 / mid_15-30% | 3538 | 102 | 24 | 0.68% | 13.09 |
| league | 5-24 / high_>=30% | 241 | 36 | 3 | 1.24% | 12.45 |
| league | 5-24 / low_<15% | 3507 | 102 | 5 | 0.14% | 20.84 |
| league | 5-24 / mid_15-30% | 3311 | 101 | 15 | 0.45% | 13.11 |
| league | 50-99 / high_>=30% | 853 | 66 | 10 | 1.17% | 9.85 |
| league | 50-99 / low_<15% | 910 | 101 | 0 | 0.00% | 18.57 |
| league | 50-99 / mid_15-30% | 9053 | 102 | 51 | 0.56% | 13.73 |
| trial | 100+ / low_<15% | 828 | 72 | 0 | 0.00% | 17.27 |
| trial | 100+ / mid_15-30% | 2724 | 78 | 4 | 0.15% | 16.59 |
| trial | 25-49 / low_<15% | 726 | 79 | 1 | 0.14% | 26.86 |
| trial | 5-24 / low_<15% | 608 | 79 | 0 | 0.00% | 24.34 |
| trial | 50-99 / low_<15% | 1209 | 79 | 0 | 0.00% | 26.05 |
| trial | 50-99 / mid_15-30% | 215 | 40 | 1 | 0.47% | 21.40 |

### Length × phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / late_1500+ | 3257 | 101 | 24 | 0.74% | 11.18 |
| league | 100+ / middle_500-1499 | 4197 | 101 | 38 | 0.91% | 12.87 |
| league | 25-49 / early_0-499 | 3437 | 102 | 3 | 0.09% | 20.16 |
| league | 25-49 / late_1500+ | 1418 | 91 | 14 | 0.99% | 11.14 |
| league | 25-49 / middle_500-1499 | 2125 | 99 | 16 | 0.75% | 13.36 |
| league | 5-24 / early_0-499 | 3121 | 102 | 4 | 0.13% | 21.24 |
| league | 5-24 / late_1500+ | 1752 | 99 | 9 | 0.51% | 12.04 |
| league | 5-24 / middle_500-1499 | 2186 | 98 | 10 | 0.46% | 14.68 |
| league | 50-99 / early_0-499 | 1535 | 102 | 1 | 0.07% | 17.98 |
| league | 50-99 / late_1500+ | 1643 | 87 | 13 | 0.79% | 10.77 |
| league | 50-99 / middle_500-1499 | 7638 | 102 | 47 | 0.62% | 13.66 |
| trial | 100+ / late_1500+ | 1390 | 76 | 3 | 0.22% | 15.04 |
| trial | 100+ / middle_500-1499 | 2161 | 76 | 1 | 0.05% | 17.91 |
| trial | 25-49 / early_0-499 | 618 | 79 | 1 | 0.16% | 28.16 |
| trial | 25-49 / late_1500+ | 49 | 8 | 0 | 0.00% | 22.45 |
| trial | 25-49 / middle_500-1499 | 66 | 12 | 0 | 0.00% | 24.24 |
| trial | 5-24 / early_0-499 | 517 | 79 | 0 | 0.00% | 23.79 |
| trial | 5-24 / late_1500+ | 43 | 9 | 0 | 0.00% | 23.26 |
| trial | 5-24 / middle_500-1499 | 48 | 8 | 0 | 0.00% | 31.25 |
| trial | 50-99 / early_0-499 | 442 | 71 | 0 | 0.00% | 27.60 |
| trial | 50-99 / late_1500+ | 98 | 10 | 0 | 0.00% | 20.41 |
| trial | 50-99 / middle_500-1499 | 884 | 77 | 1 | 0.11% | 24.77 |

### Head proximity × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | far_8_plus / high_>=30% | 2408 | 71 | 22 | 0.91% | 10.80 |
| league | far_8_plus / low_<15% | 5943 | 102 | 4 | 0.07% | 20.85 |
| league | far_8_plus / mid_15-30% | 15312 | 102 | 47 | 0.31% | 14.41 |
| league | middle_4_7 / high_>=30% | 555 | 62 | 11 | 1.98% | 8.47 |
| league | middle_4_7 / low_<15% | 1261 | 102 | 2 | 0.16% | 19.98 |
| league | middle_4_7 / mid_15-30% | 4403 | 102 | 35 | 0.79% | 10.88 |
| league | near_0_3 / high_>=30% | 264 | 51 | 11 | 4.17% | 4.92 |
| league | near_0_3 / low_<15% | 367 | 73 | 3 | 0.82% | 16.62 |
| league | near_0_3 / mid_15-30% | 1804 | 102 | 44 | 2.44% | 9.59 |
| trial | far_8_plus / low_<15% | 2371 | 79 | 0 | 0.00% | 22.78 |
| trial | far_8_plus / mid_15-30% | 2194 | 78 | 3 | 0.14% | 15.82 |
| trial | middle_4_7 / low_<15% | 699 | 79 | 0 | 0.00% | 26.04 |
| trial | middle_4_7 / mid_15-30% | 562 | 76 | 1 | 0.18% | 22.95 |
| trial | near_0_3 / low_<15% | 301 | 75 | 1 | 0.33% | 26.25 |
| trial | near_0_3 / mid_15-30% | 190 | 69 | 1 | 0.53% | 14.74 |

## Palmer as reference subset, not population replacement

Palmer league windows: **3198** / **32317** league windows;
death events in next 10: **6**;
observed apple events before death: **579**.
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
