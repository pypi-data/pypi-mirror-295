from csp.problem import *
from csp.backtracking import *
from csp.ac3 import AC3

austr_problem = MapColors()
initial_state = {}

print('Example 1')
problem = CSP(variables=austr_problem.variables,
              domains=austr_problem.domains,
              constraints=austr_problem.constraints)
state = problem.initial_state
optimizer = AC3(csp=problem)
optimizer.run(state)
print(problem.domains)

print('Example 2')
problem = CSP(variables=austr_problem.variables,
              domains=austr_problem.domains,
              constraints=austr_problem.constraints)
act_state = {'WA': 'red', 'Q': 'green'}
problem.domains['WA'] = ['red']
problem.domains['Q'] = ['green']
optimizer = AC3(csp=problem)
optimizer.run(state)
print(problem.domains)



