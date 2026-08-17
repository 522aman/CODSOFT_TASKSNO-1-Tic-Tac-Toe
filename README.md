# Tic-Tac-Toe AI (Minimax + Alpha-Beta Pruning)

A command-line Tic-Tac-Toe game where you play against an **unbeatable**
AI. The AI uses the **Minimax algorithm** with **Alpha-Beta Pruning** to
search the entire game tree and always pick the optimal move — it will
never lose, and best case for you is a draw.

## Files

- `tictactoe.py` – game logic, the Minimax/Alpha-Beta AI, and an
  interactive CLI you can play against.
- `test_tictactoe.py` – automated tests proving the AI is unbeatable:
  - AI vs AI always ends in a draw.
  - AI vs a random-move opponent never loses (across 200 games).
  - Prints how many positions alpha-beta pruning evaluates vs. the
    theoretical worst case, to illustrate the speed-up.

## How it works

### The board
The board is a flat list of 9 cells (indices `0`-`8`):

```
 0 | 1 | 2
---+---+---
 3 | 4 | 5
---+---+---
 6 | 7 | 8
```

### Minimax
Minimax explores every possible sequence of future moves. The AI
("maximizing" player) tries to pick moves that lead to the best
possible outcome *assuming the opponent ("minimizing" player) always
plays their best counter-move too*. Terminal positions are scored:

- `+10 - depth` if the AI wins (winning sooner scores higher)
- `depth - 10` if the human wins (losing later is less bad)
- `0` for a draw

### Alpha-Beta Pruning
Plain minimax on Tic-Tac-Toe evaluates hundreds of thousands of board
states from the opening move. Alpha-beta pruning cuts off branches of
the search tree that can't possibly affect the final decision,
tracking:

- **alpha** – the best score the maximizer can guarantee so far
- **beta** – the best score the minimizer can guarantee so far

Whenever `beta <= alpha`, the remaining branches at that node are
skipped, since a rational opponent would never let the game reach
them. This makes the search dramatically faster while producing the
exact same optimal move as plain minimax.

### Tie-breaking
When several moves are equally optimal, the AI picks randomly among
them so it doesn't always play in a robotic, predictable pattern.

## Running it

Play interactively in your terminal:

```bash
python tictactoe.py
```

You'll be asked whether you want to move first. Enter a number `0-8`
on your turn to place your mark. Try your best — you won't be able to
beat it, but you can force a draw with perfect play!

Run the automated test suite / demo:

```bash
python test_tictactoe.py
```

## Extending it

- **Adjustable difficulty**: make the AI occasionally pick a
  non-optimal move at random (e.g. 20% of the time) to create an
  easier difficulty setting.
- **Larger boards**: generalize `WIN_LINES` and the board size to
  play on 4x4 or 5x5 variants (note: minimax gets expensive fast on
  bigger boards without more aggressive pruning or heuristics).
- **GUI**: swap out the CLI in `play()` for a Tkinter, Pygame, or web
  front-end that calls the same `TicTacToe` / `MinimaxAI` classes.

## Requirements

Python 3.7+ (standard library only: `math`, `random`).
