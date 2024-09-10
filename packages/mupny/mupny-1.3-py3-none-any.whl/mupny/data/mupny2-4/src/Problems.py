import math
import random
import copy

class StreetProblem:

    def __init__(self, initial_state, goal_state, environment):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.environment = environment

    def successors(self, state):
        possible_actions = self.actions(state)
        return [(self.result(state, action), action) for action in possible_actions]

    def actions(self, state):
        """
        Given a state returns the list of possible actions
        :param state: actual state
        :return: a list of actions
        """
        return self.environment.streets[state]

    def result(self, state, action):
        """
        Given a state and an action returns the reached state
        :param state: actual state
        :param action: chosen action
        :return: reached state
        """
        return action

    def goal_test(self, state):
        """
        Checks if the goal condition has been reached
        :param state: actual state
        :return: True if the goal condition is matched, False otherwise
        """
        return state == self.goal_state

    def cost(self, state, action):
        reached_state = self.result(state, action)
        return self.environment.distance(state, reached_state)

    def heuristic(self, state):
        """
        Given a state returns the heuristic value of the state
        :param state: a state
        :return: the heuristic value of the state
        """
        return self.environment.distance(state, self.goal_state)


class EightQueensProblem:
    """
    the initial environment is an emtpy matrix, so from an implementation pov, we don't need to instanciate that.
    the model is -> (1, 1, 5, 4, 6, 7, 8, 3)
    queen 1 = (1,1)
    queen 2 = (1,2)
    queen 3 = (5,3)
    """

    def __init__(self, initial_state=None):
        self.initial_state = self.random() if initial_state is None else initial_state
        self.max_conflicts = sum([i for i in range(1, 8)])

    @staticmethod
    def random():
        chess = [random.randrange(0, 8) for _ in range(8)]
        return tuple(chess)  # tupla is immutable array

    def successors(self, state):
        possible_actions = self.actions(state=state)
        return [(self.result(state, action), action) for action in possible_actions]

    @staticmethod
    def actions(state):
        actions = []
        for col, row in enumerate(state):
            squares = list(range(0, 8))
            squares.remove(row)
            new_actions = list(zip([col] * len(squares), squares))
            actions.extend(new_actions)
        return actions

    @staticmethod
    def result(state, action):
        new_state = list(state)
        col, new_row = action
        new_state[col] = new_row
        return tuple(new_state)

    def goal_test(self, state):
        return self.conflicts(state) == 0

    @staticmethod
    def cost():
        """
        Returns the cost of an action. In this problem the cost is always unitary.
        :param state: a state
        :param action: an action
        :return: a cost
        """
        return 1

    @staticmethod
    def conflicts(state):
        conflicts = 0
        for col in range(8):
            queen_row = state[col]
            for col1 in range(col + 1, 8):
                queen_row1 = state[col1]
                if queen_row == queen_row1:
                    conflicts += 1
                # diagonale
                if abs(queen_row - col) == abs(queen_row1 - col1) or queen_row+col == queen_row1+col1:
                    conflicts += 1
        return conflicts

    def value(self, state):
        """
        Returns the value of a state. This function is used for evaluating a state in the local search.
        (The higher the better)
        :param state: a state
        :return: the value of a state
        """
        return self.max_conflicts - self.conflicts(state)


# ============ esercizio svolto a lezione 10. 05-04-2023 ============

"""
LOCAL SEARCH 
SI funzione obiettivo, NO euristica 
Per modellare un local search devo pormi queste domande:
- Quali sono le azioni (qui si mette info sul numero lettere)
- Quali sono i risultati
- Quali sono i possibili stati
- Quando uno stato è più vicino alla soluzione di un altro
"""
class Cruciverba:
    def __init__(self, words):
        self.initial_state = tuple()
        self.words = words

    def actions(self, state):
        """
        Given a state returns the list of possible actions
        :param state: actual state
        :return: a list of actions
        """
        match len(state):
            case 0:
                return [word for word in self.words if len(word) == 6]
            case 1:
                return [word for word in self.words if len(word) == 7]
            case 2:
                return [word for word in self.words if len(word) == 3]
            case 3:
                return []

    @staticmethod
    def result(state, action):
        """
        Given a state and an action returns the reached state
        :param state: actual state
        :param action: chosen action
        :return: reached state
        """
        new_state = list(state)
        new_state.append(action)
        return tuple(new_state)

    def successors(self, state):
        """
        Given a state returns the reachable states with the respective actions
        :param state: actual state
        :return: list of successor states and actions
        """
        possible_actions = self.actions(state)
        return [ tuple( (self.result(state, action), action) ) for action in possible_actions ]

    @staticmethod
    def conflicts(state):
        """
        Given a state return the number of conflicts
        :param state: a state
        :return: number of conflicting words
        """
        count = 0
        if len(state) >= 2:
            if state[0][4] != state[1][1]:
                count += 1
            if len(state) == 3:
                if state[1][5] != state[2][0]:
                    count += 1
        return count

    def goal_test(self, state):
        """
        Checks if the goal condition has been reached
        :param state: actual state
        :return: True if the goal condition is matched, False otherwise
        """
        return len(state) == 3 and self.conflicts(state) == 0

    def value(self, state):
        """
        Returns the value of a state. This function is used for evaluating a state in the local search.
        (The higher the better)
        :param state: a state
        :return: the value of a state
        """
        return len(state) - self.conflicts(state)


# ============ esercizio CSP container https://github.com/sisinflab/Agent-Based-Artificial-Intelligence/blob/main/exercises/CSP_Containers_challenge_19-20.pdf ============
class Containers:
    def __init__(self, environment):
        self.initial_state = tuple( ((), (), (), ()) )
        self.environment = environment

    def actions(self, state):
        """
        Given a state returns the list of possible actions
        :param state: actual state
        :return: a list of actions -> tupla(n° container, item)
        ritorna una lista di tuple, dove una tupla contiene la coppia
        (numero container, elemento da inserire) ma solo se la dimensione del container
        nello stato attuale è minore di 6
        """
        item_in_state = [item for container in state for item in container]
        return [ (n_cont, item)
                 for n_cont in range(0, 4)
                 for item in self.environment["variables"]
                 if len(state[n_cont]) < self.environment["max_capacity"]
                 and item not in item_in_state ]

    @staticmethod
    def result(state, action):
        """
        Given a state and an action returns the reached state
        :param state: actual state
        :param action: chosen action
        :return: reached state
        """
        new_state = list([list(container) for container in state])
        n_container, item = action
        new_state[n_container].append(item)
        return tuple( [tuple(new_container) for new_container in new_state] )

    def successors(self, state):
        """
        Given a state returns the reachable states with the respective actions
        :param state: actual state
        :return: list of successor states and actions
        """
        possible_actions = self.actions(state)
        random.shuffle(possible_actions)
        return [ tuple( (self.result(state, action), action) ) for action in possible_actions]

    def conflicts(self, state):
        """
        Given a state return the number of conflicts
        :param state: a state
        :return: number of conflicting words
        """
        count = 0
        for constraint in self.environment["constraints"]:
            if constraint.scope == 'DifferentContainer':
                for container in state:
                    if sum([ item in constraint.variables for item in container ]) > 1:
                        count += 1
            if constraint.scope == 'SameContainer':
                for container in state:
                    match len(constraint.variables) - sum([ item in constraint.variables for item in container ]):
                        case 1:  # 2 in the same container
                            count -= 1
                        case 0:  # all in the same container
                            count -= 3

        return count

    def value(self, state):
        """
        Returns the value of a state. This function is used for evaluating a state in the local search.
        (The higher the better)
        :param state: a state
        :return: the value of a state
        """
        return len([ item for container in state for item in container ]) - self.conflicts(state)

# ============ esercizio HANOI TOWER https://github.com/sisinflab/Agent-Based-Artificial-Intelligence/blob/main/exercises/FirstMidTerm_Hanoi.pdf ============
class HanoiTower:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    @staticmethod
    def actions(state):
        # given a state return the possible actions
        # tuple( rod di partenza, rod di destinazione )
        source_target = {}
        for rod_source, disks_source in state.items():
            if disks_source:
                rods_target = [ rod_target
                                for rod_target, disks_target in state.items()
                                if rod_target != rod_source
                                and (
                                        (
                                                disks_target
                                                and
                                                disks_source[-1] < disks_target[-1]
                                        )
                                        or ( not disks_target )
                                )]
                source_target[rod_source] = rods_target
        return [(rod_source, rod_target) for rod_source, rods_target in source_target.items()
                for rod_target in rods_target ]

    @staticmethod
    def result(state, action):
        # given a state and an action, return the result
        rod_source, rod_target = action
        new_state = copy.deepcopy(state)
        disk = new_state[rod_source].pop()
        new_state[rod_target].append(disk)
        return new_state

    def successors(self, state):
        # given a state, return the reachable states with the respective actions
        possible_actions = self.actions(state)
        return [ (self.result(state, action), action) for action in possible_actions ]

    def goal_test(self, state):
        return state == self.goal_state

    @staticmethod
    def cost(state, action):
        return 1

    def heuristic(self, state):
        # given a state, return the heuristic value of the state
        # the heuristic is an under estimation of the cost
        return len(self.goal_state) - sum([ len(d_state) == len(d_goal)
                                            for r_state, d_state in state.items()
                                            for r_goal, d_goal in self.goal_state.items()
                                            if r_state == r_goal])

class MonkAI:
    from ..main_monkAI import Environment

    def __init__(self, initial_state, goal_state, environment: Environment):
        self.environment = environment
        self.initial_state = environment.initial_state
        self.goal_state = { 'monk_pos': environment.chest_pos, 'key': True }

    def actions(self, state):
        action_list = ["Up", "Down", "Right", "Left"]
        if state['monk_pos'][0] == 0:
            action_list.remove("Up")
        if state['monk_pos'][0] == self.environment.m-1:
            action_list.remove("Down")
