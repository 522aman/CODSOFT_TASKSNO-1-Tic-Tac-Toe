"""
Tic-Tac-Toe AI
--------------
A command-line Tic-Tac-Toe game where the human plays against an
unbeatable AI powered by the Minimax algorithm with Alpha-Beta Pruning.

Run it with:
    python tictactoe.py
"""

import math
import random

HUMAN = "X"
AI = "O"
EMPTY = " "

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]


class TicTacToe:
    """Board state and game rules for Tic-Tac-Toe."""

    def __init__(self):
        self.board = [EMPTY] * 9

    def available_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == EMPTY]

    def make_move(self, index, player):
        self.board[index] = player

    def undo_move(self, index):
        self.board[index] = EMPTY

    def winner(self):
        """Return HUMAN, AI, 'Draw', or None if the game isn't over."""
        for a, b, c in WIN_LINES:
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if EMPTY not in self.board:
            return "Draw"
        return None

    def is_game_over(self):
        return self.winner() is not None

    def print_board(self):
        cells = [c if c != EMPTY else str(i) for i, c in enumerate(self.board)]
        rows = [cells[0:3], cells[3:6], cells[6:9]]
        print()
        print("  " + " | ".join(rows[0]))
        print(" ---+---+---")
        print("  " + " | ".join(rows[1]))
        print(" ---+---+---")
        print("  " + " | ".join(rows[2]))
        print()


class MinimaxAI:
    """AI player that chooses optimal moves via Minimax + Alpha-Beta Pruning."""

    def __init__(self, player=AI, opponent=HUMAN):
        self.player = player
        self.opponent = opponent
        self.nodes_evaluated = 0

    def score(self, winner, depth):
        """Higher score = better for AI. Prefer faster wins, slower losses."""
        if winner == self.player:
            return 10 - depth
        elif winner == self.opponent:
            return depth - 10
        return 0

    def minimax(self, game: TicTacToe, depth, alpha, beta, maximizing):
        self.nodes_evaluated += 1
        winner = game.winner()
        if winner is not None:
            return self.score(winner, depth)

        if maximizing:
            best = -math.inf
            for move in game.available_moves():
                game.make_move(move, self.player)
                value = self.minimax(game, depth + 1, alpha, beta, False)
                game.undo_move(move)
                best = max(best, value)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break  # beta cutoff (prune)
            return best
        else:
            best = math.inf
            for move in game.available_moves():
                game.make_move(move, self.opponent)
                value = self.minimax(game, depth + 1, alpha, beta, True)
                game.undo_move(move)
                best = min(best, value)
                beta = min(beta, best)
                if beta <= alpha:
                    break  # alpha cutoff (prune)
            return best

    def best_move(self, game: TicTacToe):
        self.nodes_evaluated = 0
        best_score = -math.inf
        best_moves = []

        for move in game.available_moves():
            game.make_move(move, self.player)
            move_score = self.minimax(game, 0, -math.inf, math.inf, False)
            game.undo_move(move)

            if move_score > best_score:
                best_score = move_score
                best_moves = [move]
            elif move_score == best_score:
                best_moves.append(move)

        # Randomize among equally-good moves so the AI isn't predictable.
        return random.choice(best_moves)


def get_human_move(game: TicTacToe):
    while True:
        raw = input("Your move (0-8): ").strip()
        if not raw.isdigit():
            print("Please enter a number between 0 and 8.")
            continue
        move = int(raw)
        if move not in range(9):
            print("Please enter a number between 0 and 8.")
            continue
        if move not in game.available_moves():
            print("That cell is already taken. Try again.")
            continue
        return move


def choose_starting_player():
    while True:
        choice = input("Do you want to go first? (y/n): ").strip().lower()
        if choice in ("y", "yes"):
            return HUMAN
        if choice in ("n", "no"):
            return AI
        print("Please answer 'y' or 'n'.")


def play():
    print("=== Tic-Tac-Toe: You (X) vs AI (O) ===")
    print("Cell positions are numbered 0-8 like this:")
    ref = TicTacToe()
    ref.print_board()

    game = TicTacToe()
    ai = MinimaxAI(player=AI, opponent=HUMAN)
    turn = choose_starting_player()

    game.print_board()

    while not game.is_game_over():
        if turn == HUMAN:
            move = get_human_move(game)
            game.make_move(move, HUMAN)
            turn = AI
        else:
            print("AI is thinking...")
            move = ai.best_move(game)
            game.make_move(move, AI)
            print(f"AI plays at {move} (evaluated {ai.nodes_evaluated} positions).")
            turn = HUMAN

        game.print_board()

    result = game.winner()
    if result == "Draw":
        print("It's a draw!")
    elif result == HUMAN:
        print("Congratulations, you win! (That shouldn't happen against a perfect AI...)")
    else:
        print("The AI wins!")


if __name__ == "__main__":
    while True:
        play()
        again = input("Play again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Thanks for playing!")
            break
