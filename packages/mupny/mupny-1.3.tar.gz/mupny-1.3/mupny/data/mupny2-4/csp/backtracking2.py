from problem import CSP

def mrv(problem:CSP, state):

    return variable

class BackTrcking:

    def __init__(self, problem: CSP, var_criterion=None, value_criterion=None):
        self.var_criterion = mrv if var_criterion is None else var_criterion
        self.value_criterion = lcv if value_criterion is None else value_criterion
        self.problem = problem

    def run(self, state):
        # check if the state is the goal state
        if self.problem.goal_test(state):
            return state

        # chose the next variable to be assigned
        variable = self.var_criterion(problem=self.problem, state=state)

        # if there is no variable to be assigned, the search fail
        if variable is None:
            return False

        # for all the values
        for value in values:
            # order the value and reach a new state
            new_state = self.problem.assign(state=state,
                                            variable=variable,
                                            value=value)

            # check if the new state is consistent
            if self.problem.consistent(state=new_state):
                state = dict(new_state)

                # run the search on the new state
                result = self.run(dict(state))

                if result:
                    return result
                else:
                    state = self.problem.rollback(state, variable)

        # if there is no possible value return failure
        return False


