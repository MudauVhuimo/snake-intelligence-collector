# Snake26 — Evidence-gated algorithm rulebook

Generated UTC: 2026-11-02T08:44:00+00:00

**Purpose:** build a NEW snake from cross-competitor research, NOT
fix the existing submission or clone a particular league leader.
Strong snakes (including Palmer), mid-field snakes, struggling
snakes and benchmark specialists are all evidence sources.

Registered questions: **8**. Open: **2**. Observed association: **6**. Controlled / promoted: **0**.

## Candidate decisions and evidence stages

| ID | Decision | Applicable evidence | Stage | Why still provisional |
|---|---|---|---|---|
| SAFETY-01 | Avoid provably fatal next actions | both | Open question | Inspect actual current 2026 engine collision order and run replay-transition tests; recorded head-to-head victim events are all shorter or equal to the cited opponent (444 shorter, 28 equal), but they do not alone establish all engine mechanics. |
| DANGER-02 | Estimate head threat jointly with escape-space scarcity | league | Observed association | Test empirically observed head-to-head and opponent next-move frequencies by body length, exact heading, position, and contested apple state in fresh whole league games; compare calibrated risk predictors and agent ablations. |
| ROUTE-03 | Preserve future routes rather than maximize immediate free neighbors | league | Observed association | Validate whether opponent-aware route scores improve independent later-season league AUC (the current +0.015 held-out advantage is uncertain), then compare simpler frozen flood-fill, moving-tail and head-cone features in controlled opponent-diverse ablations. |
| FOOD-04 | Target contest-adjusted safe food, not simply nearest apple | trial | Observed association | Run food appearance event study on actual league student-student contests, with action-level routes and apple-capture outcomes. |
| RETENTION-05 | Optimize retained growth and competitive placement, not raw apple count | league | Observed association | Estimate food capture, death/reset hazard and final retained length conditional on body length, phase, opponents and available actions. |
| CONTEST-06 | Use relative strength and opponent paths when contesting cells | league | Observed association | Separate opportunities from decisions, stratify by exact relative body length, opponent heading and alive-at-next-frame censoring, audit 2026 head-to-head collision transitions and contested apples, then validate across fresh league seasons. |
| ADAPT-07 | Change priorities with body size, density and game phase | both | Open question | Estimate interaction effects on risk/retained reward by length, density and phase; test controlled small ablations on fresh seeds. |
| ROBUST-08 | Promote only decisions that transfer to diverse league opposition | both | Observed association | Design a frozen diverse peer-opponent panel and held-out seeds; benchmark first-place frequency, retained growth, death rate and timeout. |

## State-to-action hypotheses, counterexamples and falsification tests

### SAFETY-01 — Avoid provably fatal next actions

**Evidence stage:** 0 — Open question. **Domain:** mechanics. **Scope:** both.

**When:** A move collides under engine-verified simultaneous-turn, moving-tail and head-on rules.

**Then, HYPOTHESIS only:** Remove only actions verified fatal, not cells that appear blocked on a frozen frame.

**Known counterexample / limitation:** A current tail cell may vacate before collision resolution; a frozen occupancy map may incorrectly ban it.

**Next needed measurement:** Inspect actual current 2026 engine collision order and run replay-transition tests; recorded head-to-head victim events are all shorter or equal to the cited opponent (444 shorter, 28 equal), but they do not alone establish all engine mechanics.

**Falsify if:** Rule-based predicted next-state legality disagrees with validated replay transitions.

**Supporting reports:** [opponent_cones](opponent_cones.md)

### DANGER-02 — Estimate head threat jointly with escape-space scarcity

**Evidence stage:** 1 — Observed association. **Domain:** survival. **Scope:** league.

**When:** An opponent head is <=3 toroidal cells away, especially with <=1 presently unoccupied neighboring cell.

**Then, HYPOTHESIS only:** Include opponent-head reach and locally available escape directions as joint danger features; do not automatically flee.

**Known counterexample / limitation:** Simple one-step head cones cover normal observed movements, but adding them to route-area predictors improved held-out league AUC only marginally with interval crossing zero. A geometric reach cone includes collision-impossible moves and can overstate actual opponent risk.

**Next needed measurement:** Test empirically observed head-to-head and opponent next-move frequencies by body length, exact heading, position, and contested apple state in fresh whole league games; compare calibrated risk predictors and agent ablations.

**Falsify if:** In matched held-out league states the joint features do not predict death or loss of safe routes over simpler baselines.

**Supporting reports:** [threat_windows](threat_windows.md), [opponent_cones](opponent_cones.md)

### ROUTE-03 — Preserve future routes rather than maximize immediate free neighbors

**Evidence stage:** 1 — Observed association. **Domain:** mobility. **Scope:** league.

**When:** Multiple apparently safe moves lead to different future reachable regions or narrow corridors.

**Then, HYPOTHESIS only:** Prefer moves that maintain tail-aware future connectivity when the near-term cost is reasonable.

**Known counterexample / limitation:** Moving-tail search showed only a small, uncertain held-out AUC gain over frozen flood-fill; top, middle and bottom snakes selected highest-score modeled moves at similar rates. High predicted reachable area is NOT a proven best first action.

**Next needed measurement:** Validate whether opponent-aware route scores improve independent later-season league AUC (the current +0.015 held-out advantage is uncertain), then compare simpler frozen flood-fill, moving-tail and head-cone features in controlled opponent-diverse ablations.

**Falsify if:** Dynamic connectivity fails to predict survival or gives poorer league results than a static or simpler heuristic.

**Supporting reports:** [escape_autopsies](escape_autopsies.md), [long_horizon_survival](long_horizon_survival.md), [route_space](route_space.md), [opponent_cones](opponent_cones.md)

### FOOD-04 — Target contest-adjusted safe food, not simply nearest apple

**Evidence stage:** 1 — Observed association. **Domain:** growth. **Scope:** trial.

**When:** Two snakes can reach a visible apple, and static safe-path ordering differs from toroidal geometric distance.

**Then, HYPOTHESIS only:** Estimate safe arrival times, contested landing-head risks, and post-apple escape space before committing.

**Known counterexample / limitation:** Static path distances can misidentify future routes because opponent and own body cells move; trial relationships may not transfer to league.

**Next needed measurement:** Run food appearance event study on actual league student-student contests, with action-level routes and apple-capture outcomes.

**Falsify if:** Contest-aware arrival calculations do not improve held-out league prediction or controlled capture/retained-growth rates.

**Supporting reports:** [path_geometry](path_geometry.md), [food_races](food_races.md)

### RETENTION-05 — Optimize retained growth and competitive placement, not raw apple count

**Evidence stage:** 1 — Observed association. **Domain:** reward. **Scope:** league.

**When:** An apple is available, but pursuit adds measurable collision or enclosure risk.

**Then, HYPOTHESIS only:** Value apple gain against probability-weighted loss of existing length and reduced opportunity to place first.

**Known counterexample / limitation:** Final length and placement are both outcomes; correlation cannot establish how much risk to accept or whether chasing was deliberate.

**Next needed measurement:** Estimate food capture, death/reset hazard and final retained length conditional on body length, phase, opponents and available actions.

**Falsify if:** Risk-adjusted scoring fails to increase league-like first-place outcomes relative to food-first and safety-first policies.

**Supporting reports:** [league_sweet_spot](league_sweet_spot.md), [league_vs_trials](league_vs_trials.md)

### CONTEST-06 — Use relative strength and opponent paths when contesting cells

**Evidence stage:** 1 — Observed association. **Domain:** opponents. **Scope:** league.

**When:** An opponent can approach the same cell or apple in the next few turns.

**Then, HYPOTHESIS only:** Measure each possible move's exposure to reachable opponent heads and relative length; consider state-dependent confrontation versus retreat, but do not infer intent, legality or an approved attack rule.

**Known counterexample / limitation:** Top-ranked snakes entered possible head-contest cells more frequently overall, but once conditioned on having a shorter-only contest opportunity, top 68.2% and bottom 73.7% (only 19 eligible bottom moves). Growth and opportunity confound apparent aggression; dead-on-first-step choices are missing.

**Next needed measurement:** Separate opportunities from decisions, stratify by exact relative body length, opponent heading and alive-at-next-frame censoring, audit 2026 head-to-head collision transitions and contested apples, then validate across fresh league seasons.

**Falsify if:** Contest-aware decisions degrade league rankings or cannot be predicted across different opponent styles.

**Supporting reports:** [opponent_cones](opponent_cones.md)

### ADAPT-07 — Change priorities with body size, density and game phase

**Evidence stage:** 0 — Open question. **Domain:** adaptation. **Scope:** both.

**When:** Board occupancy, snake length, remaining turns or opponent skill changes materially.

**Then, HYPOTHESIS only:** Use state-dependent tradeoffs rather than fixed food/escape/aggression weights.

**Known counterexample / limitation:** A complex adaptive policy can overfit recurring seeds and specific opponents or exceed runtime budget.

**Next needed measurement:** Estimate interaction effects on risk/retained reward by length, density and phase; test controlled small ablations on fresh seeds.

**Falsify if:** Dynamic policy fails to beat a simpler constant-weight policy across held-out league-like match mixes.

**Supporting reports:** none yet — mechanics or behavioral research needed

### ROBUST-08 — Promote only decisions that transfer to diverse league opposition

**Evidence stage:** 1 — Observed association. **Domain:** validation. **Scope:** both.

**When:** A candidate feature or move rule looks promising on trials or a small set of replayed opponents.

**Then, HYPOTHESIS only:** Require distinct game, season and bot-version holdouts and league-like controlled ablations before promotion.

**Known counterexample / limitation:** A top trial bot can be weak in student competition, and repeated hourly snapshots may reuse one seed and old bot version.

**Next needed measurement:** Design a frozen diverse peer-opponent panel and held-out seeds; benchmark first-place frequency, retained growth, death rate and timeout.

**Falsify if:** The candidate loses performance on previously unused peer opponents or fresh league-like seeds.

**Supporting reports:** [league_vs_trials](league_vs_trials.md), [seasonal_disagreement](seasonal_disagreement.md)

## Promotion gates

0. **Open:** question and measurable variables established.
1. **Observed:** source-linked analysis with denominators, caveats
   and failure cases, kept league and trials separate.
2. **Replicated:** whole unseen games / seasons / opponents; guard
   bot-version leakage and confounding.
3. **Controlled:** new independent Java candidate improves league-like
   competitive scores in a reproducible ablation.
4. **Promoted:** repeated fresh paired-seed evaluation, no major
   regression in survival, retained growth, or runtime.

No stage automatically advances when a dashboard is rebuilt.
Raw replay correlation does not prove a different move would work.

[Full research protocol](../../docs/ALGORITHM_RESEARCH_PROTOCOL.md).
[All-student cohort comparison](competitive_cohorts.md).
[Controlled league/trial comparison](league_vs_trials.md).

**No Java competitor code is modified by this report.**
