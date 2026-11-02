# Snake26: are risk and food opportunities state-dependent?

Generated UTC: 2026-11-02T16:18:27+00:00

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

Unique peer league replays: **65**; trial replays: **58**.
Observed complete 10-turn windows: **25219**;
league **20582**,
trials **4637**.
Duplicate replay payloads removed: **67**.

## Stratified actual outcomes

Death percentage is DIED within next 10 turns / eligible windows;
food rate is confirmed eats before any death / 100 eligible windows.
Nearby repeated windows and the same students make the raw fractions
correlated. **No cross-row causal effect claim**.

### Body length

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ | 4624 | 65 | 30 | 0.65% | 11.68 |
| league | 25-49 | 4497 | 65 | 21 | 0.47% | 16.34 |
| league | 5-24 | 4629 | 65 | 14 | 0.30% | 16.33 |
| league | 50-99 | 6832 | 65 | 40 | 0.59% | 13.69 |
| trial | 100+ | 2706 | 58 | 3 | 0.11% | 17.66 |
| trial | 25-49 | 512 | 58 | 1 | 0.20% | 29.10 |
| trial | 5-24 | 430 | 58 | 0 | 0.00% | 25.58 |
| trial | 50-99 | 989 | 58 | 1 | 0.10% | 27.60 |

### Arena occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | high_>=30% | 1796 | 42 | 19 | 1.06% | 9.97 |
| league | low_<15% | 4878 | 65 | 8 | 0.16% | 20.13 |
| league | mid_15-30% | 13908 | 65 | 78 | 0.56% | 12.98 |
| trial | low_<15% | 2401 | 58 | 3 | 0.12% | 25.03 |
| trial | mid_15-30% | 2236 | 57 | 2 | 0.09% | 18.29 |

### Game phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | early_0-499 | 5161 | 65 | 5 | 0.10% | 19.96 |
| league | late_1500+ | 5137 | 65 | 33 | 0.64% | 11.04 |
| league | middle_500-1499 | 10284 | 65 | 67 | 0.65% | 13.31 |
| trial | early_0-499 | 1160 | 58 | 1 | 0.09% | 27.16 |
| trial | late_1500+ | 1159 | 58 | 1 | 0.09% | 17.77 |
| trial | middle_500-1499 | 2318 | 58 | 3 | 0.13% | 21.10 |

### Length × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / high_>=30% | 951 | 42 | 8 | 0.84% | 9.67 |
| league | 100+ / low_<15% | 37 | 11 | 1 | 2.70% | 27.03 |
| league | 100+ / mid_15-30% | 3636 | 65 | 21 | 0.58% | 12.05 |
| league | 25-49 / high_>=30% | 200 | 28 | 4 | 2.00% | 11.50 |
| league | 25-49 / low_<15% | 2022 | 65 | 3 | 0.15% | 20.62 |
| league | 25-49 / mid_15-30% | 2275 | 65 | 14 | 0.62% | 12.97 |
| league | 5-24 / high_>=30% | 142 | 21 | 2 | 1.41% | 11.97 |
| league | 5-24 / low_<15% | 2243 | 65 | 4 | 0.18% | 20.46 |
| league | 5-24 / mid_15-30% | 2244 | 65 | 8 | 0.36% | 12.48 |
| league | 50-99 / high_>=30% | 503 | 37 | 5 | 0.99% | 9.34 |
| league | 50-99 / low_<15% | 576 | 64 | 0 | 0.00% | 16.67 |
| league | 50-99 / mid_15-30% | 5753 | 65 | 35 | 0.61% | 13.77 |
| trial | 100+ / low_<15% | 584 | 54 | 1 | 0.17% | 17.47 |
| trial | 100+ / mid_15-30% | 2122 | 57 | 2 | 0.09% | 17.72 |
| trial | 25-49 / low_<15% | 510 | 58 | 1 | 0.20% | 28.63 |
| trial | 5-24 / low_<15% | 430 | 58 | 0 | 0.00% | 25.58 |
| trial | 50-99 / low_<15% | 877 | 58 | 1 | 0.11% | 27.71 |
| trial | 50-99 / mid_15-30% | 112 | 26 | 0 | 0.00% | 26.79 |

### Length × phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / late_1500+ | 2047 | 64 | 9 | 0.44% | 10.65 |
| league | 100+ / middle_500-1499 | 2573 | 64 | 21 | 0.82% | 12.51 |
| league | 25-49 / early_0-499 | 2200 | 65 | 2 | 0.09% | 20.18 |
| league | 25-49 / late_1500+ | 937 | 60 | 10 | 1.07% | 11.31 |
| league | 25-49 / middle_500-1499 | 1360 | 63 | 9 | 0.66% | 13.60 |
| league | 5-24 / early_0-499 | 1988 | 65 | 3 | 0.15% | 20.98 |
| league | 5-24 / late_1500+ | 1090 | 62 | 5 | 0.46% | 12.02 |
| league | 5-24 / middle_500-1499 | 1551 | 63 | 6 | 0.39% | 13.41 |
| league | 50-99 / early_0-499 | 969 | 65 | 0 | 0.00% | 17.44 |
| league | 50-99 / late_1500+ | 1063 | 54 | 9 | 0.85% | 10.54 |
| league | 50-99 / middle_500-1499 | 4800 | 65 | 31 | 0.65% | 13.62 |
| trial | 100+ / late_1500+ | 1020 | 54 | 1 | 0.10% | 16.57 |
| trial | 100+ / middle_500-1499 | 1685 | 57 | 2 | 0.12% | 18.34 |
| trial | 25-49 / early_0-499 | 445 | 58 | 1 | 0.22% | 27.87 |
| trial | 25-49 / middle_500-1499 | 43 | 9 | 0 | 0.00% | 39.53 |
| trial | 5-24 / early_0-499 | 358 | 58 | 0 | 0.00% | 24.30 |
| trial | 5-24 / middle_500-1499 | 47 | 7 | 0 | 0.00% | 36.17 |
| trial | 50-99 / early_0-499 | 356 | 54 | 0 | 0.00% | 29.21 |
| trial | 50-99 / late_1500+ | 90 | 7 | 0 | 0.00% | 25.56 |
| trial | 50-99 / middle_500-1499 | 543 | 57 | 1 | 0.18% | 26.89 |

### Head proximity × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | far_8_plus / high_>=30% | 1338 | 42 | 9 | 0.67% | 11.06 |
| league | far_8_plus / low_<15% | 3776 | 65 | 4 | 0.11% | 20.50 |
| league | far_8_plus / mid_15-30% | 9904 | 65 | 32 | 0.32% | 14.02 |
| league | middle_4_7 / high_>=30% | 318 | 35 | 6 | 1.89% | 7.23 |
| league | middle_4_7 / low_<15% | 852 | 65 | 2 | 0.23% | 19.25 |
| league | middle_4_7 / mid_15-30% | 2845 | 65 | 19 | 0.67% | 11.04 |
| league | near_0_3 / high_>=30% | 140 | 29 | 4 | 2.86% | 5.71 |
| league | near_0_3 / low_<15% | 250 | 46 | 2 | 0.80% | 17.60 |
| league | near_0_3 / mid_15-30% | 1159 | 65 | 27 | 2.33% | 8.80 |
| trial | far_8_plus / low_<15% | 1706 | 58 | 1 | 0.06% | 24.21 |
| trial | far_8_plus / mid_15-30% | 1656 | 57 | 1 | 0.06% | 16.43 |
| trial | middle_4_7 / low_<15% | 475 | 57 | 0 | 0.00% | 27.58 |
| trial | middle_4_7 / mid_15-30% | 438 | 56 | 0 | 0.00% | 26.71 |
| trial | near_0_3 / low_<15% | 220 | 55 | 2 | 0.91% | 25.91 |
| trial | near_0_3 / mid_15-30% | 142 | 50 | 1 | 0.70% | 14.08 |

## Palmer as reference subset, not population replacement

Palmer league windows: **1439** / **20582** league windows;
death events in next 10: **2**;
observed apple events before death: **267**.
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
