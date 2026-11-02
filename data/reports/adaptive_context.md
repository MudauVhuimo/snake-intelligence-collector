# Snake26: are risk and food opportunities state-dependent?

Generated UTC: 2026-11-02T23:43:04+00:00

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

Unique peer league replays: **71**; trial replays: **62**.
Observed complete 10-turn windows: **27456**;
league **22499**,
trials **4957**.
Duplicate replay payloads removed: **67**.

## Stratified actual outcomes

Death percentage is DIED within next 10 turns / eligible windows;
food rate is confirmed eats before any death / 100 eligible windows.
Nearby repeated windows and the same students make the raw fractions
correlated. **No cross-row causal effect claim**.

### Body length

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ | 5106 | 71 | 36 | 0.71% | 11.83 |
| league | 25-49 | 4850 | 71 | 24 | 0.49% | 16.62 |
| league | 5-24 | 5020 | 71 | 15 | 0.30% | 16.55 |
| league | 50-99 | 7523 | 71 | 44 | 0.58% | 13.56 |
| trial | 100+ | 2888 | 62 | 3 | 0.10% | 17.52 |
| trial | 25-49 | 555 | 62 | 1 | 0.18% | 28.65 |
| trial | 5-24 | 456 | 62 | 0 | 0.00% | 25.66 |
| trial | 50-99 | 1058 | 62 | 1 | 0.09% | 27.22 |

### Arena occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | high_>=30% | 2116 | 48 | 25 | 1.18% | 9.88 |
| league | low_<15% | 5349 | 71 | 8 | 0.15% | 20.12 |
| league | mid_15-30% | 15034 | 71 | 86 | 0.57% | 13.14 |
| trial | low_<15% | 2583 | 62 | 3 | 0.12% | 24.78 |
| trial | mid_15-30% | 2374 | 61 | 2 | 0.08% | 18.11 |

### Game phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | early_0-499 | 5641 | 71 | 6 | 0.11% | 19.96 |
| league | late_1500+ | 5616 | 71 | 39 | 0.69% | 11.32 |
| league | middle_500-1499 | 11242 | 71 | 74 | 0.66% | 13.33 |
| trial | early_0-499 | 1240 | 62 | 1 | 0.08% | 26.85 |
| trial | late_1500+ | 1239 | 62 | 1 | 0.08% | 17.51 |
| trial | middle_500-1499 | 2478 | 62 | 3 | 0.12% | 20.98 |

### Length × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / high_>=30% | 1142 | 48 | 11 | 0.96% | 9.63 |
| league | 100+ / low_<15% | 37 | 11 | 1 | 2.70% | 27.03 |
| league | 100+ / mid_15-30% | 3927 | 71 | 24 | 0.61% | 12.32 |
| league | 25-49 / high_>=30% | 208 | 31 | 4 | 1.92% | 11.54 |
| league | 25-49 / low_<15% | 2235 | 71 | 3 | 0.13% | 20.45 |
| league | 25-49 / mid_15-30% | 2407 | 71 | 17 | 0.71% | 13.50 |
| league | 5-24 / high_>=30% | 165 | 24 | 2 | 1.21% | 12.12 |
| league | 5-24 / low_<15% | 2445 | 71 | 4 | 0.16% | 20.61 |
| league | 5-24 / mid_15-30% | 2410 | 71 | 9 | 0.37% | 12.74 |
| league | 50-99 / high_>=30% | 601 | 43 | 8 | 1.33% | 9.15 |
| league | 50-99 / low_<15% | 632 | 70 | 0 | 0.00% | 16.61 |
| league | 50-99 / mid_15-30% | 6290 | 71 | 36 | 0.57% | 13.67 |
| trial | 100+ / low_<15% | 637 | 58 | 1 | 0.16% | 17.27 |
| trial | 100+ / mid_15-30% | 2251 | 61 | 2 | 0.09% | 17.59 |
| trial | 25-49 / low_<15% | 553 | 62 | 1 | 0.18% | 28.21 |
| trial | 5-24 / low_<15% | 456 | 62 | 0 | 0.00% | 25.66 |
| trial | 50-99 / low_<15% | 937 | 62 | 1 | 0.11% | 27.43 |
| trial | 50-99 / mid_15-30% | 121 | 27 | 0 | 0.00% | 25.62 |

### Length × phase

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | 100+ / late_1500+ | 2259 | 70 | 12 | 0.53% | 11.02 |
| league | 100+ / middle_500-1499 | 2843 | 70 | 24 | 0.84% | 12.49 |
| league | 25-49 / early_0-499 | 2419 | 71 | 3 | 0.12% | 20.21 |
| league | 25-49 / late_1500+ | 997 | 65 | 11 | 1.10% | 12.04 |
| league | 25-49 / middle_500-1499 | 1434 | 68 | 10 | 0.70% | 13.74 |
| league | 5-24 / early_0-499 | 2174 | 71 | 3 | 0.14% | 21.07 |
| league | 5-24 / late_1500+ | 1204 | 68 | 5 | 0.42% | 12.29 |
| league | 5-24 / middle_500-1499 | 1642 | 68 | 7 | 0.43% | 13.70 |
| league | 50-99 / early_0-499 | 1044 | 71 | 0 | 0.00% | 17.15 |
| league | 50-99 / late_1500+ | 1156 | 59 | 11 | 0.95% | 10.29 |
| league | 50-99 / middle_500-1499 | 5323 | 71 | 33 | 0.62% | 13.56 |
| trial | 100+ / late_1500+ | 1100 | 58 | 1 | 0.09% | 16.36 |
| trial | 100+ / middle_500-1499 | 1787 | 61 | 2 | 0.11% | 18.24 |
| trial | 25-49 / early_0-499 | 482 | 62 | 1 | 0.21% | 27.59 |
| trial | 25-49 / middle_500-1499 | 49 | 10 | 0 | 0.00% | 36.73 |
| trial | 5-24 / early_0-499 | 384 | 62 | 0 | 0.00% | 24.48 |
| trial | 5-24 / middle_500-1499 | 47 | 7 | 0 | 0.00% | 36.17 |
| trial | 50-99 / early_0-499 | 373 | 57 | 0 | 0.00% | 28.42 |
| trial | 50-99 / late_1500+ | 90 | 7 | 0 | 0.00% | 25.56 |
| trial | 50-99 / middle_500-1499 | 595 | 61 | 1 | 0.17% | 26.72 |

### Head proximity × occupancy

| Environment | Stratum | Windows | Unique replay games | Deaths by +10 | Death risk | Apples before death /100 |
|---|---|---:|---:|---:|---:|---:|
| league | far_8_plus / high_>=30% | 1604 | 48 | 11 | 0.69% | 10.91 |
| league | far_8_plus / low_<15% | 4150 | 71 | 4 | 0.10% | 20.53 |
| league | far_8_plus / mid_15-30% | 10750 | 71 | 37 | 0.34% | 14.20 |
| league | middle_4_7 / high_>=30% | 348 | 39 | 7 | 2.01% | 7.18 |
| league | middle_4_7 / low_<15% | 923 | 71 | 2 | 0.22% | 19.28 |
| league | middle_4_7 / mid_15-30% | 3058 | 71 | 21 | 0.69% | 11.09 |
| league | near_0_3 / high_>=30% | 164 | 33 | 7 | 4.27% | 5.49 |
| league | near_0_3 / low_<15% | 276 | 51 | 2 | 0.72% | 16.67 |
| league | near_0_3 / mid_15-30% | 1226 | 71 | 28 | 2.28% | 8.97 |
| trial | far_8_plus / low_<15% | 1823 | 62 | 1 | 0.05% | 24.14 |
| trial | far_8_plus / mid_15-30% | 1765 | 61 | 1 | 0.06% | 16.20 |
| trial | middle_4_7 / low_<15% | 520 | 61 | 0 | 0.00% | 26.35 |
| trial | middle_4_7 / mid_15-30% | 460 | 60 | 0 | 0.00% | 26.52 |
| trial | near_0_3 / low_<15% | 240 | 59 | 2 | 0.83% | 26.25 |
| trial | near_0_3 / mid_15-30% | 149 | 54 | 1 | 0.67% | 14.77 |

## Palmer as reference subset, not population replacement

Palmer league windows: **1439** / **22499** league windows;
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
