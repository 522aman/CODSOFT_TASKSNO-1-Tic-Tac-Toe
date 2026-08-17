"""
Automated tests / demo for tictactoe.py

Run with: python test_tictactoe.py

Checks:
1. AI vs AI always ends in a draw (both play optimally).
2. AI never loses against a random-move opponent, across many games.
3. Prints node-evaluation counts to show alpha-beta pruning is working.
"""

import random
from tictactoe import TicTacToe, MinimaxAI, HUMAN, AI


def play_ai_vs_ai():
    game = TicTacToe()
    ai_o = MinimaxAI(player=AI, opponent=HUMAN)
    ai_x = MinimaxAI(player=HUMAN, opponent=AI)  # plays optimally as X too
    turn = HUMAN

    while not game.is_game_over():
        if turn == HUMAN:
            move = ai_x.best_move(game)
            game.make_move(move, HUMAN)
            turn = AI
        else:
            move = ai_o.best_move(game)
            game.make_move(move, AI)
            turn = HUMAN

    return game.winner()


def play_ai_vs_random(ai_starts):
    game = TicTacToe()
    ai = MinimaxAI(player=AI, opponent=HUMAN)
    turn = AI if ai_starts else HUMAN

    while not game.is_game_over():
        if turn == AI:
            move = ai.best_move(game)
            game.make_move(move, AI)
            turn = HUMAN
        else:
            move = random.choice(game.available_moves())
            game.make_move(move, HUMAN)
            turn = AI

    return game.winner()


def test_ai_vs_ai_is_always_draw(trials=5):
    print(f"Running {trials} AI-vs-AI games (both optimal)...")
    for i in range(trials):
        result = play_ai_vs_ai()
        assert result == "Draw", f"Expected a draw, got {result}"
    print("  PASS: all AI-vs-AI games ended in a draw.\n")


def test_ai_never_loses_to_random(trials=200):
    print(f"Running {trials} AI-vs-random games...")
    losses = 0
    wins = 0
    draws = 0
    for i in range(trials):
        ai_starts = i % 2 == 0
        result = play_ai_vs_random(ai_starts)
        if result == AI:
            wins += 1
        elif result == "Draw":
            draws += 1
        else:
            losses += 1

    print(f"  AI wins: {wins}, Draws: {draws}, AI losses: {losses}")
    assert losses == 0, "AI should never lose!"
    print("  PASS: AI never lost a single game.\n")


def demo_single_move_pruning():
    print("Demonstrating alpha-beta pruning efficiency on an empty board:")
    game = TicTacToe()
    ai = MinimaxAI(player=AI, opponent=HUMAN)
    move = ai.best_move(game)
    print(f"  AI's opening move: {move}")
    print(f"  Positions evaluated with alpha-beta pruning: {ai.nodes_evaluated}")
    print("  (Without pruning, minimax would evaluate up to 9! = 362,880 leaf paths)\n")


if __name__ == "__main__":
    test_ai_vs_ai_is_always_draw()
    test_ai_never_loses_to_random()
    demo_single_move_pruning()
    print("All tests passed!")
