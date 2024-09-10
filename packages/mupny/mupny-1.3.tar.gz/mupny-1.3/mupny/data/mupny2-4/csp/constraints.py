class Constraint:
    def __init__(self, variables):
        self.variables = variables
        self.degree = len(variables)

    def check(self, state):
        return True

class UnaryConstraint(Constraint):
    def __init__(self, variable):
        self.variable = variable
        super(UnaryConstraint, self).__init__(variables=variable)

        def check(self, state):
            return True

class ValueConstraint(UnaryConstraint):
    def __init__(self, variable, accepted_values):
        super(ValueConstraint, self).__init__(variable=variable)
        self.accepted_values = accepted_values

    def check(self, state):
        # la variabile deve essere in uno stato
        if self.variable in state:
            return state[self.variable] in self.accepted_values
        return True

class DifferentValues(Constraint):
    def check(self, state):
        values = [state[var] for var in self.variables if var in state]
        return len(values) == len(set(values))  # set toglie i valori ripetuti

# ============ esercizio svolto a lezione 10. 05-04-2023 ============
class LetterConstraint(UnaryConstraint):
    def __init__(self, variable, letter, position):
        super(LetterConstraint, self).__init__(variable=variable)
        self.letter = letter
        self.position = position

    def check(self, state):
        # un constraint ha senso di essere controllato
        # se quella variabile è stata assegnata
        if self.variable in state:
            return state[self.variable][self.position] == self.letter
        # se la variabile non è nello state il constraint non è violato
        return True


# ============ esercizio CSP container https://github.com/sisinflab/Agent-Based-Artificial-Intelligence/blob/main/exercises/CSP_Containers_challenge_19-20.pdf ============

class DifferentContainer(Constraint):
    def __init__(self, variables):
        super(DifferentContainer, self).__init__(variables)
        self.scope = 'DifferentContainer'

    def check(self, state):
        values = [state[var] for var in self.variables if var in state ]
        return len(values) == len(set(values)) if values else True

class SameContainer(Constraint):
    def __init__(self, variables):
        super(SameContainer, self).__init__(variables)
        self.scope = 'SameContainer'

    def check(self, state):
        values = [ state[var] for var in self.variables if var in state ]
        return len(set(values)) == 1 if values else True

class MaxCapacity:
    def __init__(self, max_capacity):
        self.max_capacity = max_capacity
        self.scope = 'MaxCapacity'

    def check(self, state):
        containers = [ state[var] for var in state ]
        for container in set(containers):
            capacity = len([ c for c in containers if c == container ])
            # print(f'Capacity of {container} = {capacity}')
            if capacity > self.max_capacity:
                return False
        return True
