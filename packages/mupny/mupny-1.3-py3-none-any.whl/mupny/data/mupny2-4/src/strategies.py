import random

class Random:

    @staticmethod
    def select(self, fringe):
        random.shuffle(fringe)
        node = fringe.pop()
        return fringe, node

class BreathFirst:

    @staticmethod
    def select(self, fringe):
        # FIFO
        node = fringe.pop(0)
        return fringe, node

class DepthFirst:

    @staticmethod
    def select(fringe):
        # LIFO
        node = fringe.pop()
        return fringe, node

class DepthLimitedSearch:
    def __init__(self, limit):
        self.limit = limit

    def select(self, fringe):
        fringe = [node for node in fringe if node.depth <= self.limit]
        try:
            node = fringe.pop()
        except IndexError:
            return [], None
        return fringe, node

class UniformCostSearh:

    @staticmethod
    def select(self, fringe):
        fringe = sorted(fringe, key=lambda x: x.cost)
        node = fringe.pop(0)
        return fringe, node

class Greedy:

    def __init__(self, problem):
        self.problem = problem

    def select(self, fringe):
        # sorted in base all'heuristic function
        fringe = sorted(fringe, key=lambda x: self.problem.heuristic(x.state))
        node = fringe.pop(0)
        return fringe, node

class AStar:

    def __init__(self, problem):
        self.problem = problem

    def select(self, fringe):
        fringe = sorted(fringe, key=lambda node: self.problem.heuristic(node.state)+node.cost)
        node = fringe.pop(0)
        return fringe, node
