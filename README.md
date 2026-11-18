# tiny-chess-4k

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Rynnnzen/tiny-chess-4k/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Rynnnzen/tiny-chess-4k/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in under 4,096 bytes of packed Python: a 0x88 board, iterative deepening to depth 12 on a fixed 60,000-node budget, transposition table, null-move pruning, quiescence with delta pruning, and full handling of the 200-ply adjudication, repetition and fifty-move rules. No model calls and no clock in the search — every move is deterministic.

## Run it

```sh
python3 -P -s /bot/main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=3nca7vjq&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
