# Palmer's real league danger decisions — replay casebook

One selected example from EACH unique archived league game containing
a sampled dangerous Palmer position. For reproducibility, selection
uses the **earliest dangerous snapshot** in that game, NOT a winning
or particularly impressive escape. No hypothetical moves are drawn.
A danger snapshot means head distance <=3 cells or <=1 free neighbor.
All observed x/y motions are on the real toroidal board. The first
move style reports straight/turn/reverse relative to actual body
orientation; unknown means we cannot determine orientation.
A recorded death before +30 remains a death after respawn.
If no frame or an unexplained absence is observed, +30 is censored.

| Archived league replay | Turn | Length | Start head distance | Free exits 0 to +3 | Actual first move | Death-free +30? | Comparable peer in same game |
|---|---:|---:|---:|---|---|---|---|
| [game-76004.rep.gz](../replays/2026-11-03-185906-season/game-76004.rep.gz) | 350 | 35 | 6 | 1 → 3 | -x / turn | alive | no matching baseline peer |
| [game-75004.rep.gz](../replays/2026-11-03-185906-season/game-75004.rep.gz) | 525 | 95 | 15 | 1 → 3 | -y / turn | alive | 389160-lwandle-ramanugu |
| [game-73001.rep.gz](../replays/2026-11-03-185906-season/game-73001.rep.gz) | 500 | 70 | 5 | 1 → 2 | -y / turn | alive | no matching baseline peer |
| [game-76004.rep.gz](../replays/2026-11-03-145900-season/game-76004.rep.gz) | 350 | 40 | 3 | 3 → 2 | +y / straight | alive | 408501-asher-urison |
| [game-75004.rep.gz](../replays/2026-11-03-145900-season/game-75004.rep.gz) | 400 | 70 | 3 | 3 → 3 | -y / turn | alive | 423258-muhammed-dar |
| [game-73001.rep.gz](../replays/2026-11-03-145900-season/game-73001.rep.gz) | 150 | 20 | 2 | 3 → 3 | +y / turn | alive | 423436-ntobeko-zondi |
| [game-76007.rep.gz](../replays/2026-11-03-115900-season/game-76007.rep.gz) | 25 | 15 | 1 | 2 → 3 | -x / turn | alive | 426650-babongile-mafantiri |
| [game-75005.rep.gz](../replays/2026-11-03-115900-season/game-75005.rep.gz) | 925 | 100 | 1 | 2 → 3 | +x / turn | alive | 423436-ntobeko-zondi |
| [game-73000.rep.gz](../replays/2026-11-03-115900-season/game-73000.rep.gz) | 450 | 60 | 3 | 2 → 1 | +y / turn | alive | 428786-marvellous-sambo |
| [game-72002.rep.gz](../replays/2026-11-03-115900-season/game-72002.rep.gz) | 325 | 25 | 2 | 3 → 3 | +x / straight | alive | 421538-tshifhiwa-bvumbi |
| [game-71004.rep.gz](../replays/2026-11-03-045900-season/game-71004.rep.gz) | 250 | 30 | 2 | 3 → 3 | +x / turn | alive | 423239-zeeshaan-bham |
| [game-74000.rep.gz](../replays/2026-11-03-025900-season/game-74000.rep.gz) | 625 | 90 | 3 | 3 → 3 | -y / straight | alive | 402334-angile-saho |
| [game-73005.rep.gz](../replays/2026-11-03-025900-season/game-73005.rep.gz) | 25 | 5 | 3 | 3 → 3 | -y / straight | alive | 400861-sibusisomlungisi-dlamini |
| [game-72004.rep.gz](../replays/2026-11-03-025900-season/game-72004.rep.gz) | 375 | 85 | 2 | 2 → 1 | -x / turn | alive | 413538-lelethuthando-nikelo |
| [game-71004.rep.gz](../replays/2026-11-03-025900-season/game-71004.rep.gz) | 625 | 60 | 1 | 2 → 2 | -x / turn | alive | 424820-elisha-mundalamo |
| [game-76004.rep.gz](../replays/2026-11-02-045859-season/game-76004.rep.gz) | 525 | 75 | 8 | 1 → 3 | -y / straight | alive | 429782-maseeha-seedat |
| [game-75004.rep.gz](../replays/2026-11-02-045859-season/game-75004.rep.gz) | 750 | 110 | 1 | 2 → 2 | -y / turn | alive | no matching baseline peer |
| [game-74007.rep.gz](../replays/2026-11-02-045859-season/game-74007.rep.gz) | 125 | 35 | 3 | 3 → 2 | -y / turn | alive | 388060-tshepang-tshabalala |
| [game-73001.rep.gz](../replays/2026-11-02-045859-season/game-73001.rep.gz) | 525 | 60 | 3 | 3 → 2 | -y / straight | alive | 403339-david-ndambo |
| [game-72007.rep.gz](../replays/2026-11-02-045859-season/game-72007.rep.gz) | 550 | 50 | 2 | 3 → 3 | -y / straight | alive | 413538-lelethuthando-nikelo |
| [game-71004.rep.gz](../replays/2026-11-02-045859-season/game-71004.rep.gz) | 125 | 20 | 2 | 3 → 2 | -y / straight | alive | 388828-ngcebo-methula |
| [game-74007.rep.gz](../replays/2026-11-01-235859-season/game-74007.rep.gz) | 850 | 120 | 2 | 3 → 2 | +x / turn | alive | 403754-vhuimo-mudau |
| [game-73001.rep.gz](../replays/2026-11-01-235859-season/game-73001.rep.gz) | 700 | 105 | 3 | 2 → 1 | +x / turn | alive | 413538-lelethuthando-nikelo |
| [game-72007.rep.gz](../replays/2026-11-01-235859-season/game-72007.rep.gz) | 250 | 45 | 1 | 2 → 3 | -y / straight | alive | 404721-khensani-maluleke |
| [game-71004.rep.gz](../replays/2026-11-01-235859-season/game-71004.rep.gz) | 525 | 70 | 2 | 2 → 2 | -y / straight | alive | 388828-ngcebo-methula |
| [game-76004.rep.gz](../replays/2026-11-01-225859-season/game-76004.rep.gz) | 200 | 10 | 3 | 3 → 3 | -x / straight | alive | 404721-khensani-maluleke |
| [game-75004.rep.gz](../replays/2026-11-01-225859-season/game-75004.rep.gz) | 575 | 75 | 2 | 3 → 2 | +y / straight | alive | 424820-elisha-mundalamo |
| [game-74007.rep.gz](../replays/2026-11-01-225859-season/game-74007.rep.gz) | 375 | 60 | 3 | 3 → 3 | +y / straight | alive | 388060-tshepang-tshabalala |
| [game-71004.rep.gz](../replays/2026-11-01-215859-season/game-71004.rep.gz) | 200 | 40 | 3 | 3 → 3 | +y / straight | alive | 408008-bradley-buys |
| [game-72007.rep.gz](../replays/2026-11-01-205859-season/game-72007.rep.gz) | 375 | 45 | 2 | 3 → 3 | -x / straight | alive | 402334-angile-saho |
| [game-72003.rep.gz](../replays/2026-11-01-205859-season/game-72003.rep.gz) | 525 | 90 | 2 | 3 → 2 | -y / turn | alive | 423546-ndabenhle-shabangu |
| [game-71001.rep.gz](../replays/2026-11-01-205859-season/game-71001.rep.gz) | 525 | 60 | 3 | 3 → 3 | +x / turn | alive | 428786-marvellous-sambo |
| [game-71004.rep.gz](../replays/2026-10-24-135900-season/game-71004.rep.gz) | 575 | 75 | 2 | 3 → 3 | +x / turn | alive | 427417-phophi-shavhani |
| [game-71004.rep.gz](../replays/2026-10-24-115859-season/game-71004.rep.gz) | 525 | 110 | 3 | 3 → 3 | +y / turn | alive | 419342-ayeshan-puckree |
| [game-71000.rep.gz](../replays/2026-10-23-235858-season/game-71000.rep.gz) | 250 | 40 | 2 | 2 → 3 | +x / turn | alive | 403501-mashau-mudzanani |

## How to compare a genuine decision sequence

Use the [per-game CSV](../derived/palmer_league_casebook.csv), which
contains each real replay's measured head distance, unoccupied
neighbor count and apple captures at turns 0, 1, 3, 10, 20, 30.
Cells may be empty after a death or when followup is censored.
The optional matched peer shares the same replay, length band,
head-proximity band and confined/unconfined category. Their starting
turn, exact body, apples, and opponent positions may still differ.
These are descriptive case studies, not a learned or proven policy.
No competition snake code has been altered.
