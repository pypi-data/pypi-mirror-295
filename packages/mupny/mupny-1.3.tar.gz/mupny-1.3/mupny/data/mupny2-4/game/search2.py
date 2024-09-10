import numpy as np

class MiniMax:
    def __init__(self, game):
        self.game = game


    def min_value(self, state):
        if self.game.terminal_test(state):
            return self.game.utility(state)
        values = [ self.max_value(state) for state, action in self.game.successors(state) ]
        return min(values)

    def max_value(self, state):
        if self.game.terminal_test(state):
            return self.game.player_utility(state)
        values = [ self.min_value(state) for state, action in self.game.successors(state)]
        return max(values)

    def next_move(self, state):
        # recupero le azioni possibili
        moves = self.game.actions(state)
        return max(moves, key=lambda move: self.min_value(self.game.result(move)))

class AlphaBeta:
    # ALPHA viene aggiornato da MAX
    # BETA viene aggiornato da MIN
    # MIN vede alpha che gli passa MAX
    # MAX vede BETA che gli passa MIN
    from .games import Game

    def __init__(self, game: Game):
        self.game = game

    def min_value(self, state, alpha, beta):
        if self.game.terminal_test(state):
            return self.game.utility(state)
        best_value = np.inf
        for state, action in self.game.successors(state):
            value = self.max_value(state, alpha, beta)
            best_value = min(best_value, value)
            if best_value < alpha:
                return best_value
            beta = min(beta, best_value)
        return best_value

    def next_move(self, state):
        alpha = -np.inf
        beta = np.inf

        best_move = None

        for state, action in self.game.successors(state):
            value = self.min_value(state, alpha, beta)
            if value > alpha:
                alpha = value
                best_move = move
        return best_move

