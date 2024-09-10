import random
from .problem import CSP

# ======= VARIABLE ASSIGNMENT ========
def random_variable(problem: CSP, state):
    """
    Given a state returns a random assignable variable
    @param problem: a CSP problem
    @param state: a state
    @return: a random assignable variable
    """
    assignable_vars = problem.assignable_variables(state)
    random.shuffle(assignable_vars)
    return assignable_vars.pop()

def minimum_remaining_values(problem: CSP, state):
    """
    Choose the variable with the fewest legal values
    @param problem: a CSP problem
    @param state: a state
    @return: a variable
    """
    assignable_vars = problem.assignable_variables(state)
    # return min([len(problem.assignable_values(state, var)) for var in assignable_vars])
    return min(assignable_vars, key=lambda var: len(problem.assignable_values(state, var)))

def degree_heuristic(problem: CSP, state):
    """
    Choose the variable with the most constraints on remaining variables
    @param problem: a CSP problem
    @param state: a state
    @return: a variable
    """
    assignable_vars = problem.assignable_variables(state)
    return max(assignable_vars, key=lambda var: problem.remaining_constraints(state, var))

# ======= VALUE ASSIGNMENT ========

def random_assignment(problem: CSP, state, variable):
    """
    Return a random value to be assigned to the variable
    @param problem: a CSP problem
    @param state: a state
    @param variable: a variable
    @return: a possible values for the variable
    """
    possible_values = problem.domains[variable]
    random.shuffle(possible_values)
    return possible_values


def least_constraining_value(problem: CSP, state, variable):
    """
    Given a variable, choose the least constraining value
    Per scegliere il valore da assegnare ad una variabile,
    scegliamo il valore che vincola di meno il dominio delle altre variabili.
    @param problem: a CSP problem
    @param state: a state
    @param variable: an assignable variable
    @return: a list of assignable values
    """
    assignable_values = problem.assignable_values(state, variable)

    return sorted(assignable_values,
                  key=lambda val: sum([
                      len(problem.assignable_values(state=problem.assign(state, variable, val), variable=var_to_check))
                      for var_to_check in problem.assignable_variables(state=problem.assign(state, variable, val))
                  ]), reverse=True)

class BackTracking:

    def __init__(self, problem: CSP, var_criterion=None, value_criterion=None):
        self.var_criterion = random_variable if var_criterion is None else var_criterion
        self.value_criterion = random_assignment if value_criterion is None else value_criterion
        self.problem = problem

    def run(self, state):
        # check if the state is the goal state
        if self.problem.goal_test(state):
            return state

        # choose the next variable to be assigned
        variable = self.var_criterion(problem=self.problem, state=state)
        # if there is no variable to be assigned, the search fail
        if variable is None:
            return False

        # order the values with a desired order
        values = self.value_criterion(self.problem, state, variable)

        # for all the values
        for value in values:

            # assign the value and reach a new state
            new_state = self.problem.assign(state=state, variable=variable, value=value)

            # check if the new state is consistent
            if self.problem.consistent(state=new_state):
                state = dict(new_state)

                # run the search on the new state
                result = self.run(dict(state))

                # if succeeds return the solution
                if result:
                    return result
                else:
                    # if the result is a failure cancel the assignment
                    state = self.problem.rollback(state, variable)

        # if there is no possible value return failure
        return False

    def forward_checking(self, state, domains):
        new_domains = dict(domains)
        # per ogni variabile nel problema calcolo i valori assegnabili (legali)
        # e popolo la nuova mappa dei domini
        for var in self.problem.variables:
            new_domains[var] = self.problem.assignable_values(state, var)
        return new_domains

    def run_with_forward_checking(self, state, domains):
        """
        nel forward checkign è come se i domini diventassero parte dello stato
        perchè per ogni stato, dobbiamo tenere tracia dei domini delle altre variabili
        visto che il forward checking li modifica ad ogni assegnazione
        """
        # check if the state is goal state
        if self.problem.goal_test(state):
            return state

        # check for domain failure with forward checking
        if [] in domains.values():
            return False

        # choose the next variable to be assigned
        variable = self.var_criterion(self.problem, state)
        # if there is no variable to be assigned, the search fail
        if variable is None:
            return False

        # order the value and reach a new state
        values = self.value_criterion(problem=self.problem, state=state, variable=variable)

        # for all the values
        for value in values:

            # assign the value and reach a new state
            new_state = self.problem.assign(state=state,
                                            variable=variable,
                                            value=value)

            # check if the new state is consistent
            if self.problem.consistent(state=new_state):
                state = dict(new_state)

                # apply forward checking
                # (propagare l'assegnazione verso i domini delle altre variabili)
                new_domains = self.forward_checking(state, domains)
                del new_domains[variable]

                # run the search on the new state
                result = self.run_with_forward_checking(dict(state), new_domains)

                # if succeeds return the solution
                if result:
                    return result
                else:
                    # if the result is a failure cancel the assignment
                    state = self.problem.rollback(state, variable)

        # if there is no possible value a failure
        return False
