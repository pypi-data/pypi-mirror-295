from src.Node import Node

class GraphSearch:
    """
    A class able to find a solution with a given search stragies
    """

    def __init__(self, problem, strategy=None):
        self.problem = problem
        self.strategy = strategy
        self.fringe = []
        self.visited = []

    def run(self):
        node = Node(state=self.problem.initial_state,
                    parent=None,
                    action=None,
                    cost=0,
                    depth=0)

        while True:
            # check the goal test
            if self.problem.goal_test(node.state):
                return 'OK', node

            # add node state in a list of visited state
            self.visited.append(node.state)

            # expand the node
            new_states = self.problem.successors(state=node.state)
            new_nodes = [node.expand(new_state=state,
                                     action=action,
                                     cost=self.problem.cost(node.state, action)
                                     ) for state, action in new_states]

            # retain the states not already visited
            new_nodes = [node for node in new_nodes if node.state not in self.visited]

            # update the fringe
            self.fringe = self.fringe + new_nodes
            # select the new node
            self.fringe, node = self.strategy.select(fringe=self.fringe)

            if node is None:
                return 'Fail', []

            # check if is empty
            if len(self.fringe) == 0:
                if self.problem.goal_test(node.state):
                    return 'OK', node
                else:
                    return 'Fail', []
