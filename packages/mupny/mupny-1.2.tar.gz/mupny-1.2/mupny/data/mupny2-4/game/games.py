import itertools
import random

class Game:
    def __init__(self, initial_state, player):
        self.initial_state = initial_state
        self.player = player

    def actions(self, state):
        """
        Given a state return the list of possible actions
        @param state: a state of the game
        @return: a list
        """
        return []

    def result(self, state, action):
        """
        Given a state and an action returns the reached state
        @param state: a state of the game
        @param action: a possible action in the state
        @return: a new state
        """
        return []

    def successors(self, state):
        """
        Given a state returns the reachable states with the respective actions
        :param state: actual state
        :return: list of successor states and actions
        """
        possible_actions = self.actions(state)
        return [(self.result(state, a), a) for a in possible_actions]

    def terminal_test(self, state):
        """
        Returns True if the state is a final state (the game is over), False otherwise
        @param state: a state of the game
        @return: True or False
        """
        return False

    def utility(self, state):
        """
        Given a state returns its utility
        @param state: a state of the game
        @return: a utility value
        """
        return 0

    def player_utility(self, state):
        """
        Given a state, returns the utility of the state from the view of the MAX or the MIN player
        @param state: a state
        @return: a utility value
        """
        if self.player == 'MAX':
            # for MAX player
            return self.utility(state)
        elif self.player == 'MIN':
            # for MIN player
            return -self.utility(state)
        else:
            raise ValueError

    def next_player(self):
        """
        Return the next player to move
        @return: MAX or MIN
        """
        if self.player == 'MAX':
            return 'MIN'
        else:
            return 'MAX'

# let's populate the skeleton with our dummy game
class DummyGame(Game):
    def __init__(self, initial_state=None, player='MAX'):
        if initial_state is None:
            initial_state = 'A'
        super(DummyGame, self).__init__(initial_state, player)
        self.initial_state = initial_state
        self.player = player

    def actions(self, state):
        """
        Given a state return the list of possible actions
        @param state: a state of the game
        @return: a list
        """
        actions = {
            'A': ['a1', 'a2', 'a3'],
            'B': ['b1', 'b2', 'b3'],
            'C': ['c1', 'c2', 'c3'],
            'D': ['d1', 'd2', 'd3'],
        }
        if state in actions:
            return actions[state]
        else:
            return []

    def result(self, state, action):
        """
        Given a state and an action returns the reached state
        @param state: a state of the game
        @param action: a possible action in the state
        @return: a new state
        """
        result = {
            'A': {
                'a1': 'B',
                'a2': 'C',
                'a3': 'D'},
            'B': {
                'b1': 'B1',
                'b2': 'B2',
                'b3': 'B3'},
            'C': {
                'c1': 'C1',
                'c2': 'C2',
                'c3': 'C3'},
            'D': {
                'd1': 'D1',
                'd2': 'D2',
                'd3': 'D3'},
        }
        return result[state][action]

    def terminal_test(self, state):
        """
        Returns True if the state is a final state (the game is over), False otherwise
        @param state: a state of the game
        @return: True or False
        """
        if state in ('B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'D1', 'D2', 'D3'):
            return True
        else:
            return False

    def utility(self, state):
        """
        Given a state returns its utility
        @param state: a state of the game
        @return: a utility value (integer)
        """
        utility = {'B1': 3,
                   'B2': 12,
                   'B3': 8,
                   'C1': 2,
                   'C2': 4,
                   'C3': 6,
                   'D1': 14,
                   'D2': 5,
                   'D3': 2}
        return utility[state]

class TicTacToe(Game):  # Tris
    def __init__(self, initial_state=None, player='MAX'):
        super().__init__(initial_state, player)
        self.empty = 0
        self.MAX = 1
        self.MIN = -1
        self.initial_state = tuple([ self.empty for i in range(0,8)]) if initial_state is None else initial_state
        self.player = player

    def actions(self, state):
        # Given a state, return the possible actions
        # 1 -> MAX
        # -1 -> MIN
        # if the sum is 0 the next move is to self.player
        if all([ cell != 0 for cell in state]):
            return []
        next_action = getattr(self, self.player) if sum(state) == 0 else -1
        return [ (next_action, i) for i, cell in enumerate(state) if cell == 0 ]

    def result(self, state, action):
        move, cell = action
        new_state = list(state)
        new_state[cell] = move
        return new_state

    def terminal_test(self, state):
        # stato terminale quando è stato raggiunto un tris (utilità diversa da zero)
        # oppure
        # stato terminale quando al tupla contiene tutti valori diversi da zero
        if self.utility(state) != 0 or all([ move != 0 for move in state ]):
            return True
        else:
            return False

    def utility(self, state):
        # horizontal check
        for i in [3, 6, 9]:
            if all([ move == self.MAX for move in state[:i] ]):
                return self.MAX
            elif all([ move == self.MIN for move in state[:i] ]):
                return self.MIN

        # vertical check
        for i in [0, 1, 2]:
            if all([ move == self.MAX for move in state[i:i+7:3] ]):
                return self.MAX
            elif all([ move == self.MIN for move in state[i:i+7:3] ]):
                return self.MIN

        # diagonal check
        for diagonal in [[*range(0, 9, 4)], [*range(2, 7, 2)] ]:
            diagonal_move = [ state[i] for i in range(0, 9) if i in diagonal ]
            if all([ move == self.MAX for move in diagonal_move ]):
                return self.MAX
            elif all([ move == self.MIN for move in diagonal_move ]):
                return self.MIN

        return 0

class PacmanGame(Game):
    def __init__(self, initial_state=None, player='MAX', board=4):
        self.board = board
        if initial_state is None:
            initial_state = self.init_state()
        super(PacmanGame, self).__init__(initial_state, player)
        self.initial_state = initial_state
        self.player = player
        self.to_eat = len(initial_state['specials'])
        self.min = 'MIN'
        self.max = 'MAX'
        self.empty = '.'
        self.special = '*'
        self.met = 'X'

    def init_state(self):
        temp_specials = list(itertools.permutations(range(self.board-1), 2))
        random.shuffle(temp_specials)
        state = {
            'max_pos': (0, 0),
            'min_pos': (self.board-1, self.board-1),
            'specials': temp_specials[: round(self.board ** 2 / 4)],
            'to_move': 'MAX'
        }

        return state

    def actions(self, state):
        """
        Given a state return the list of possible actions
        @param state: a state of the game
        @return: a list
        """
        action_list = ['Up', 'Down', 'Right', 'Left']
        if state['to_move'] == 'MAX':
            pos = state['max_pos']
        elif state['to_move'] == 'MIN':
            pos = state['min_pos']
        else:
            raise ValueError

        if pos[0] == 0:
            action_list.remove("Up")
        if pos[0] == self.board - 1:
            action_list.remove("Down")
        if pos[1] == 0:
            action_list.remove("Left")
        if pos[1] == self.board - 1:
            action_list.remove("Right")
        return action_list

    def result(self, state, action):
        if state['to_move'] == 'MAX':
            pos = state['max_pos']
            reached_pos = self.compute_reached_pos(action, pos)
            specials = [sp_pos for sp_pos in state['specials'] if sp_pos != reached_pos]
            reached_state = {
                'max_pos': reached_pos,
                'min_pos': state['min_pos'],
                'specials': specials,
                'to_move': 'MIN'
            }
            return reached_state

        elif state['to_move'] == 'MIN':
            pos = state['min_pos']
            reached_pos = self.compute_reached_pos(action, pos)
            reached_state = {
                'max_pos': state['max_pos'],
                'min_pos': reached_pos,
                'specials': state['specials'],
                'to_move': 'MAX'
            }
            return reached_state
        else:
            raise ValueError

    @staticmethod
    def compute_reached_pos(action, pos):
        if action == 'Up':
            reached_pos = (pos[0] - 1, pos[1])
        if action == 'Down':
            reached_pos = (pos[0] + 1, pos[1])
        if action == 'Left':
            reached_pos = (pos[0], pos[1] - 1)
        if action == 'Right':
            reached_pos = (pos[0], pos[1] + 1)
        return reached_pos

    def terminal_test(self, state):
        """
        Returns True if the state is a final state (the game is over), False otherwise
        @param state: a state of the game
        @return: True or False
        """
        if state['max_pos'] == state['min_pos'] or len(state['specials']) == 0:
            return True
        else:
            return False

    def utility(self, state):
        """
        Given a state returns its utility
        @param state: a state of the game
        @return: a utility value (integer)
        """
        manhattan = abs(state['max_pos'][0] - state['min_pos'][0]) + abs(state['max_pos'][1] - state['min_pos'][1])
        food = self.to_eat - len(state['specials'])
        return manhattan + food

    def play(self, player_one, player_two):
        """
        A function that simulates the game between two players
        @param player_one: function that models the first player
        @param player_two:  function that models the second player
        """
        state = self.initial_state
        print("----- THE GAME STARTS! -----\n\n")
        self.draw_board(self.initial_state)
        players = [player_one, player_two]
        moves = []
        while True:
            for player in players:
                if self.terminal_test(state):
                    print('----- GAME OVER -----\n\n')
                    return moves
                else:
                    print(f'{self.player} plays!')
                move = player.next_move(state)
                state = self.result(state, move)
                self.draw_board(state)
                moves.append((move, self.player))
                self.player = self.next_player()
                print('_____________________')

    def display(self, state):
        print('_____________________')
        if self.player == 'MAX':
            print(self.player, 'in ', state['max_pos'], self.player_utility(state))
        elif self.player == 'MIN':
            print(self.player, 'in ', state['min_pos'], self.player_utility(state))
        else:
            raise ValueError

    def display_move(self, state, move):
        print(self.player, f'--{move}--> ', state)

    def draw_board(self, state):
        # print header
        print('\t', end='')
        for column in range(0, self.board):
            print(column, '\t\t', end='')
        print()

        for i in range(0, self.board):
            print(i, end='')
            for j in range(0, self.board):
                if (i, j) == state['min_pos'] == state['max_pos']:
                    print('\t{}\t|'.format(self.met), end=" ")
                elif (i, j) == state['min_pos']:
                    print('\t{}\t|'.format(self.min), end=" ")
                elif (i, j) == state['max_pos']:
                    print('\t{}\t|'.format(self.max), end=" ")
                elif (i, j) in state['specials']:
                    print('\t{}\t|'.format(self.special), end=" ")

                else:
                    print('\t{}\t|'.format(self.empty), end=" ")
            print()
        print()
