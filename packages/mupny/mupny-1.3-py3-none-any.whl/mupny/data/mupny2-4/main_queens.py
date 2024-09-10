from src.Problems import EightQueensProblem
from src.local_search import *

# formulate the problem
problem = EightQueensProblem()

# HillClimbing / SimulatedAnnealing
search = SimulatedAnnealing(problem=problem)

result, state = search.run()

print(result)
print(problem.value(state))
print(state)