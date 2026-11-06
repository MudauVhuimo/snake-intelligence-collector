# Snake26: observed collision and movement mechanics audit

Generated UTC: 2026-11-06T11:05:51+00:00

## Evidence and limits

Source: deduplicated REAL 2026 league/trial replay payloads, consecutive
frames and explicit death/eat events. Outcomes use actual participants.
This audit does **NOT** simulate hypothetical alternatives; it cannot
establish that any unchosen action would be safe or certainly fatal.
A replay victim event is not a complete head-on collision record.
The authoritative engine's simultaneous action resolution is still the
source of truth. Verify game-specific collision order against that
engine before declaring a Java next-move filter 'provably safe'.

Unique league replays: **102**;
unique trials: **79**;
duplicate payloads removed: **69**;
unreadable replays: **0**.

## Verified observed outcomes by environment

| Audit | Peer league | On-arrival trials |
|---|---:|---:|
| Previously living snake-turns | 807743 | 621709 |
| Normal surviving one-cell head moves | 807314 | 619752 |
| Invalid observed head motion | 0 | 0 |
| Observed toroidal wrap moves | 23113 | 17644 |
| Surviving move into OWN old tail coordinate | 9388 | 2358 |
| Surviving move into OPPONENT old tail coordinate | 9288 | 576 |
| Survivors with recorded eat event | 11918 | 9564 |
| Eat without previous-frame apple | 0 | 0 |
| Explicit recorded death events | 426 | 1957 |
| Self-collision victim events | 195 | 431 |
| Body/obstacle collision victim events | 154 | 872 |
| Head-to-head victim events | 77 | 654 |
| Head-on victim shorter than attributed rival | 77 | 616 |
| Head-on victim equal to attributed rival | 0 | 38 |
| Head-on victim longer than attributed rival | 0 | 0 |
| Head-on attribution peer unavailable | 0 | 0 |
| Unexplained missing living head next frame | 3 | 0 |

## Eating growth length changes among observed survivors

| Next-frame body segment count minus previous | League | Trials |
|---|---:|---:|
| +5 | 11918 | 9564 |

## Interpretation for SAFETY-01

- Wrap movements are observable one-step transitions on a torus.
- A surviving old-tail entry falsifies any simplistic permanent
  rule that bans every currently occupied tail cell.
- Head-on victim length comparisons are OBSERVATIONAL support for
  length priority, not a complete formal proof of tie/collision order.
- Opponent tails may advance simultaneously; do not assume a tail
  vacates if food growth or a collision changes the same turn.
- An explicit cause labels a recorded death, not the unavailable
  attempted destination of the dead snake.
- Before gameplay implementation, run targeted move-pair tests
  against the exact downloaded 2026 native engine or documented
  official mechanics to validate guaranteed vs merely possible danger.

**This closes the missing descriptive evidence gap only; no action
has been certified safe in all game states.**
