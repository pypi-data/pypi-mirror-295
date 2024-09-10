from .constraints import *
class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.initial_state = dict()

    def consistent(self, state):
        """
        Given a state checks if it is admissable
        ovvero per ogni constraint passa lo stato e vedi se viola quel constraint.
        Se lo stato in input non viola nessun constraint allora ritorna True
        """
        return all([c.check(state) for c in self.constraints])

    def complete(self, state):
        # return all([ var in state.keys() for var in self.variables])
        return len(state) == len(self.variables)

    def goal_test(self, state):
        return self.complete(state) and self.consistent(state)

    def assign(self, state, variable, value):
        if variable in self.variables and value in self.domains[variable]:
            new_state = dict(state)
            new_state[variable] = value
            return new_state
        raise ValueError

    def rollback(self, state, variable):
        if variable in self.variables:
            new_state = dict(state)
            del new_state[variable]
            return new_state
        raise ValueError

    def assignable_variables(self, state):
        # ritorna le variabili che non sono ancora state assegnate
        return [var for var in self.variables if var not in state]

    def assignable_values(self, state, variable):
        """
        Given a state and a variable returns the list of possible assignments
        @param state: a state
        @param variable: a variable of the problem
        @return: a list of the legal values
        """
        return [ value for value in self.domains[variable] if self.consistent(self.assign(state, variable, value)) ]

    def remaining_constraints(self, state, variable):
        """
        Given a state and a variable returns the sum of constraints between the variable and all the other variables
        @param state: a state
        @param variable: a variable
        @return: a number of constraints
        """
        remaining_variables = [var for var in self.assignable_variables(state) if var != variable]
        if remaining_variables:
            return len(
                [ constraint.variables
                  for constraint in self.constraints
                  if variable == constraint.variables[0]
                    and constraint.variables[1] in remaining_variables ]
            )
        else:
            return 0

    def remove_inconsistent_values(self, arc, actual_state):
        """
        Given an arc constraint over the variables x_i, x_j check that the values of x_i have at least one value
        in x_j that satisfies the constraint, otherwise remove that value of x_i from its domain
        @param arc: an arc constraint
        @param actual_state: the problem state
        @return: True if some value of x_i has been removed, False otherwise
        """
        # variables of the arc x_i => x_j (arc is constraint, list of 2 variables)
        x_i, x_j = arc.variables

        # variable that checks if some value has been removed
        removed = False
        # iterate for all the possible assignments of x_i
        for value_i in self.domains[x_i]:
            # assign the value to x_i
            state = self.assign(state=actual_state,
                                variable=x_i,
                                value=value_i)
            # check the constraint validity for all the possible values of x_j
            assignments = [ arc.check(self.assign(state=state,
                                                  variable=x_j,
                                                  value=value_j)) for value_j in self.domains[x_j] ]
            # if there are no possible assignments
            if not any(assignments):
                # remove the value from the domain of x_i
                self.domains[x_i].remove(value_i)
                print(f'removing {value_i} from {x_i}')
                removed = True
        return removed

class MapColors(CSP):
    def __init__(self):
        self.variables = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
        # nel caso in cui le variabili abbiano domini diversi bisogna definire esplicitamente per ogni variabile il suo dominio
        self.domains = { var: ['green', 'red', 'blue'] for var in self.variables }
        self.constraints = [
            DifferentValues(['WA', 'NT']),
            DifferentValues(['NT', 'WA']),
            DifferentValues(['WA', 'SA']),
            DifferentValues(['SA', 'WA']),
            DifferentValues(['SA', 'NT']),
            DifferentValues(['NT', 'SA']),
            DifferentValues(['SA', 'Q']),
            DifferentValues(['Q', 'SA']),
            DifferentValues(['SA', 'NSW']),
            DifferentValues(['NSW', 'SA']),
            DifferentValues(['SA', 'V']),
            DifferentValues(['V', 'SA']),
            DifferentValues(['Q', 'NT']),
            DifferentValues(['NT', 'Q']),
            DifferentValues(['NSW', 'Q']),
            DifferentValues(['Q', 'NSW']),
            DifferentValues(['V', 'NSW']),
            DifferentValues(['NSW', 'V'])
        ]

# ============ esercizio svolto a lezione 10. 05-04-2023 ============
class Cruciverba(CSP):
    def __init__(self, words):
        self.variables = ['W1', 'W2']
        self.domains = {
            'W1': [w for w in words if len(w) == 6],
            'W2': [w for w in words if len(w) == 3]
        }
        self.constraints = [
            LetterConstraint('W1', 'l', 4),
            LetterConstraint('W2', 't', 0)
        ]


# ============ esercizio CSP container https://github.com/sisinflab/Agent-Based-Artificial-Intelligence/blob/main/exercises/CSP_Containers_challenge_19-20.pdf ============

class Container(CSP):
    def __init__(self):
        self.variables = ['t1', 't2', 't3', 't4', 't5', 'f1', 'f2', 'f3', 'e1', 'e2', 'fz1', 'fz2', 'fz3', 'fs1']
        self.domains = { var: ['C1', 'C2', 'C3', 'C4']
                         for var in self.variables }
        self.constraints = [
            DifferentContainer(['e1', 'e2']),
            DifferentContainer(['e2', 'e1']),
            DifferentContainer(['t1', 'f1']),
            DifferentContainer(['t1', 'f2']),
            DifferentContainer(['t1', 'f3']),
            DifferentContainer(['t2', 'f1']),
            DifferentContainer(['t2', 'f2']),
            DifferentContainer(['t2', 'f3']),
            DifferentContainer(['t3', 'f1']),
            DifferentContainer(['t3', 'f2']),
            DifferentContainer(['t3', 'f3']),
            DifferentContainer(['t4', 'f1']),
            DifferentContainer(['t4', 'f2']),
            DifferentContainer(['t4', 'f3']),
            DifferentContainer(['t5', 'f1']),
            DifferentContainer(['t5', 'f2']),
            DifferentContainer(['t5', 'f3']),
            SameContainer(['fz1', 'fz2', 'fz3']),
            DifferentContainer(['fs1', 'fz1']),
            DifferentContainer(['fs1', 'fz2']),
            DifferentContainer(['fs1', 'fz3']),
            MaxCapacity(max_capacity=6),
        ]

# ============ esercizio CSP container https://github.com/sisinflab/Agent-Based-Artificial-Intelligence/blob/main/exercises/CSP_Containers_challenge_19-20.pdf ============