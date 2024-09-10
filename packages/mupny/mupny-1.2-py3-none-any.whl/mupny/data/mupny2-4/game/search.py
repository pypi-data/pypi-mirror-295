import numpy as np

class Minimax:
    def __init__(self, game):
        self.game = game

    def min_value(self, state):
        """
        A function that computes the value given by the player MIN to a node
        """
        if self.game.terminal_test(state):
            return self.game.player_utility(state)
        values = [ self.max_value(state) for state, action in self.game.successors(state) ]
        return min(values)

    def max_value(self, state):
        """
        A function that computes the value given by the player MAX to a node
        """
        if self.game.terminal_test(state):
            return self.game.player_utility(state)
        values = [ self.min_value(state) for state, action in self.game.successors(state) ]
        return max(values)

    def next_move(self, state):
        """
        Compute the final move suggested to the player MAX
        @param state: a state
        @return: a move
        """
        moves = self.game.actions(state)
        for move in moves:
            print(move, self.min_value(self.game.result(state, move)))
        print("final move: ")
        return max(moves, key=lambda move: self.min_value(self.game.result(state, move)))

class AlphaBeta:
    # alpha viene aggiornato da MAX
    # beta viene aggiornato da MIN
    # MIN vede alpha che gli passa MAX
    # MAX vede beta che gli passa MIN

    def __init__(self, game):
        self.game = game

    def max_value(self, state, alpha, beta):
        """
        A function that computes the value given by player MIN to a node
        @param state: a state
        @param alpha:
        @param beta:
        @return: the value associated by max to the node
        """
        if self.game.terminal_test(state):
            return self.game.player_utility(state)

        best_value = -np.inf
        for state, action in self.game.successors(state):
            value = self.min_value(state, alpha, beta)
            best_value = min(best_value, value)
            # beta test (if MAX choice will never be the choice of MIN, stop searching)
            if best_value > beta:
                return best_value
            # update the best_value for MIN
            alpha = max(alpha, best_value)
        return best_value

    def min_value(self, state, alpha, beta):
        """
        A function that computes the value given by player MIN to a node
        @param state: a state
        @param alpha:
        @param beta:
        @return: the value associated by max to the node
        """
        if self.game.terminal_test(state):
            return self.game.player_utility(state)

        best_value = np.inf
        for state, action in self.game.successors(state):
            value = self.max_value(state, alpha, beta)
            best_value = min(best_value, value)
            # beta test (if MIN choice will never be the choice of MAX, stop searching)
            if best_value < alpha:
                return best_value
            # update the best_value for MIN
            beta = min(beta, best_value)
        return best_value

    def next_move(self, state):
        """
        Compute the final move suggested to the player MAX
        @param state: a state
        @return: a move
        """
        alpha = -np.inf
        beta = np.inf

        best_move = None

        for state, move in self.game.successors(state):
            value = self.min_value(state, alpha, beta)
            print(value, alpha)
            if value > alpha:
                # update the best value for MAX
                alpha = value
                best_move = move
        return best_move


class LimitedAlphaBeta:

    def __init__(self, game, limit=1000000000):
        self.game = game
        self.limit = limit

    def max_value(self, state, alpha, beta, limit):
        """
        A function that computes the value given by player MAX to a node
        @param state: a state
        @param alpha:
        @param beta:
        @param limit:
        @return: the value associated by max to the node
        """

        # game end check
        if self.game.terminal_test(state) or limit == 0:
            return self.game.player_utility(state)
        best_value = -np.inf
        for s, a in self.game.successors(state):
            value = self.min_value(s, alpha, beta, limit-1)
            best_value = max(best_value, value)
            # beta test (if MAX choice will never be the choice of MIN, stop searching)
            if best_value > beta:
                return best_value
            # update the best value for MAX
            alpha = max(alpha, best_value)
        return best_value

    def min_value(self, state, alpha, beta, limit):
        """
        A function that computes the value given by player MIN to a node
        @param state: a state
        @param alpha:
        @param beta:
        @param limit:
        @return: the value associated by max to the node
        """

        # game end check
        if self.game.terminal_test(state) or limit == 0:
            return self.game.player_utility(state)
        best_value = np.inf
        for s, a in self.game.successors(state):
            value = self.max_value(s, alpha, beta, limit-1)
            best_value = min(best_value, value)
            # beta test (if MIN choice will never be the choice of MAX, stop searching)
            if best_value < alpha:
                return best_value
            # update the best value for MIN
            beta = min(beta, best_value)
        return best_value

    def next_move(self, state):
        """
        Compute the final move suggested to the player MAX
        @param state: a state
        @return: a move
        """

        alpha = -np.inf
        beta = np.inf

        best_move = None

        for s, move in self.game.successors(state):
            value = self.min_value(s, alpha, beta, self.limit)
            if value > alpha:
                # update the best value for MAX
                alpha = value
                best_move = move
        return best_move
