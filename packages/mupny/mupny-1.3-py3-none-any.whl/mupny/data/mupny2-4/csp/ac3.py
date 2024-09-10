from .problem import CSP

class AC3:
    def __init__(self, csp: CSP):
        self.csp = csp

    def all_arcs(self):
        # return all the arc constraints of the problem (2 degree)
        return [ cons for cons in self.csp.constraints if cons.degree == 2 ]

    def add_neighbours(self, queue, arc):
        x_i, _ = arc.variables
        neighbours = [arc for arc in self.all_arcs() if arc.variables[1] == x_i]
        queue.extend(neighbours)

    def run(self, state):
        # initial queue with all the arcs in the problem
        queue = self.all_arcs()

        # while the queue is not empty
        while queue:
            # select an arc from the queue
            arc = queue.pop()
            # items() return dict as tuple in a list
            # stopping condition: there is at least one variable with no assignables values
            if 0 in [ len(v) for k, v in self.csp.domains.items() ]:
                return False

            if self.csp.remove_inconsistent_values(arc=arc, actual_state=state):
                self.add_neighbours(queue, arc)
        return True
