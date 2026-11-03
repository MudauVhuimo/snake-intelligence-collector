# Snake26: are risk and food opportunities state-dependent?

Generated UTC: 2026-11-03T12:28:38+00:00

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

Unique peer league replays: **85**; trial replays: **74**.
Observed complete 10-turn windows: **32806**;
league **26889**,
trials **5917**.
Duplicate replay payloads removed: **71**.

## Stratified actual outcomes

Death percentage is DIED within next 10 turns / eligible windows;
food rate is confirmed eats before any death / 100 eligible windows.
Nearby repeated windows and the same students make the raw fractions
correlated. **No cross-row causal effect claim**.

### Body length

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ | 6186 | 85 | 45 | 0.73% | 11.83 |
| league | 25-49 | 5811 | 85 | 30 | 0.52% | 16.35 |
| league | 5-24 | 5944 | 85 | 18 | 0.30% | 16.57 |
| league | 50-99 | 8948 | 85 | 52 | 0.58% | 13.70 |
| trial | 100+ | 3343 | 74 | 3 | 0.09% | 17.20 |
| trial | 25-49 | 679 | 74 | 1 | 0.15% | 27.10 |
| trial | 5-24 | 559 | 74 | 0 | 0.00% | 25.40 |
| trial | 50-99 | 1336 | 74 | 2 | 0.15% | 25.37 |

### Arena occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | high_>=30% | 2635 | 59 | 31 | 1.18% | 9.83 |
| league | low_<15% | 6393 | 85 | 8 | 0.13% | 20.29 |
| league | mid_15-30% | 17861 | 85 | 106 | 0.59% | 13.08 |
| trial | low_<15% | 3164 | 74 | 3 | 0.09% | 23.83 |
| trial | mid_15-30% | 2753 | 73 | 3 | 0.11% | 17.65 |

### Game phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | early_0-499 | 6741 | 85 | 7 | 0.10% | 19.88 |
| league | late_1500+ | 6712 | 85 | 50 | 0.74% | 11.28 |
| league | middle_500-1499 | 13436 | 85 | 88 | 0.65% | 13.37 |
| trial | early_0-499 | 1480 | 74 | 1 | 0.07% | 26.08 |
| trial | late_1500+ | 1479 | 74 | 1 | 0.07% | 16.90 |
| trial | middle_500-1499 | 2958 | 74 | 4 | 0.14% | 20.42 |

### Length × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / high_>=30% | 1426 | 59 | 15 | 1.05% | 9.75 |
| league | 100+ / low_<15% | 41 | 14 | 1 | 2.44% | 24.39 |
| league | 100+ / mid_15-30% | 4719 | 85 | 29 | 0.61% | 12.35 |
| league | 25-49 / high_>=30% | 275 | 38 | 5 | 1.82% | 9.45 |
| league | 25-49 / low_<15% | 2624 | 85 | 3 | 0.11% | 20.62 |
| league | 25-49 / mid_15-30% | 2912 | 85 | 22 | 0.76% | 13.15 |
| league | 5-24 / high_>=30% | 210 | 31 | 3 | 1.43% | 12.38 |
| league | 5-24 / low_<15% | 2938 | 85 | 4 | 0.14% | 20.52 |
| league | 5-24 / mid_15-30% | 2796 | 85 | 11 | 0.39% | 12.73 |
| league | 50-99 / high_>=30% | 724 | 54 | 8 | 1.10% | 9.39 |
| league | 50-99 / low_<15% | 790 | 84 | 0 | 0.00% | 18.10 |
| league | 50-99 / mid_15-30% | 7434 | 85 | 44 | 0.59% | 13.65 |
| trial | 100+ / low_<15% | 771 | 69 | 1 | 0.13% | 16.99 |
| trial | 100+ / mid_15-30% | 2572 | 73 | 2 | 0.08% | 17.26 |
| trial | 25-49 / low_<15% | 674 | 74 | 1 | 0.15% | 26.71 |
| trial | 5-24 / low_<15% | 559 | 74 | 0 | 0.00% | 25.40 |
| trial | 50-99 / low_<15% | 1160 | 74 | 1 | 0.09% | 25.95 |
| trial | 50-99 / mid_15-30% | 176 | 34 | 1 | 0.57% | 21.59 |

### Length × phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / late_1500+ | 2741 | 84 | 18 | 0.66% | 11.16 |
| league | 100+ / middle_500-1499 | 3440 | 84 | 27 | 0.78% | 12.38 |
| league | 25-49 / early_0-499 | 2864 | 85 | 3 | 0.10% | 20.18 |
| league | 25-49 / late_1500+ | 1154 | 76 | 12 | 1.04% | 11.53 |
| league | 25-49 / middle_500-1499 | 1793 | 82 | 15 | 0.84% | 13.33 |
| league | 5-24 / early_0-499 | 2614 | 85 | 3 | 0.11% | 20.89 |
| league | 5-24 / late_1500+ | 1452 | 82 | 8 | 0.55% | 12.19 |
| league | 5-24 / middle_500-1499 | 1878 | 82 | 7 | 0.37% | 13.95 |
| league | 50-99 / early_0-499 | 1258 | 85 | 1 | 0.08% | 17.17 |
| league | 50-99 / late_1500+ | 1365 | 73 | 12 | 0.88% | 10.33 |
| league | 50-99 / middle_500-1499 | 6325 | 85 | 39 | 0.62% | 13.74 |
| trial | 100+ / late_1500+ | 1309 | 70 | 1 | 0.08% | 15.89 |
| trial | 100+ / middle_500-1499 | 2033 | 71 | 2 | 0.10% | 18.05 |
| trial | 25-49 / early_0-499 | 576 | 74 | 1 | 0.17% | 26.56 |
| trial | 25-49 / middle_500-1499 | 74 | 13 | 0 | 0.00% | 31.08 |
| trial | 5-24 / early_0-499 | 472 | 74 | 0 | 0.00% | 24.15 |
| trial | 5-24 / middle_500-1499 | 59 | 9 | 0 | 0.00% | 33.90 |
| trial | 50-99 / early_0-499 | 431 | 67 | 0 | 0.00% | 27.61 |
| trial | 50-99 / late_1500+ | 113 | 9 | 0 | 0.00% | 23.01 |
| trial | 50-99 / middle_500-1499 | 792 | 73 | 2 | 0.25% | 24.49 |

### Head proximity × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | far_8_plus / high_>=30% | 1968 | 59 | 14 | 0.71% | 10.67 |
| league | far_8_plus / low_<15% | 5024 | 85 | 4 | 0.08% | 20.58 |
| league | far_8_plus / mid_15-30% | 12725 | 85 | 41 | 0.32% | 14.21 |
| league | middle_4_7 / high_>=30% | 439 | 50 | 8 | 1.82% | 8.43 |
| league | middle_4_7 / low_<15% | 1058 | 85 | 2 | 0.19% | 19.85 |
| league | middle_4_7 / mid_15-30% | 3646 | 85 | 28 | 0.77% | 10.61 |
| league | near_0_3 / high_>=30% | 228 | 43 | 9 | 3.95% | 5.26 |
| league | near_0_3 / low_<15% | 311 | 58 | 2 | 0.64% | 17.04 |
| league | near_0_3 / mid_15-30% | 1490 | 85 | 37 | 2.48% | 9.53 |
| trial | far_8_plus / low_<15% | 2223 | 74 | 1 | 0.04% | 22.99 |
| trial | far_8_plus / mid_15-30% | 2035 | 73 | 2 | 0.10% | 15.92 |
| trial | middle_4_7 / low_<15% | 650 | 73 | 0 | 0.00% | 26.00 |
| trial | middle_4_7 / mid_15-30% | 529 | 70 | 0 | 0.00% | 25.33 |
| trial | near_0_3 / low_<15% | 291 | 70 | 2 | 0.69% | 25.43 |
| trial | near_0_3 / mid_15-30% | 189 | 64 | 1 | 0.53% | 14.81 |

## Palmer as reference subset, not population replacement

Palmer league windows: **2159** / **26889** league windows;
death events in next 10: **3**;
observed apple events before death: **392**.
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
