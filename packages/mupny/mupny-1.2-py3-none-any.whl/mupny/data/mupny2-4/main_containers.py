from csp.problem import Container
from csp.backtracking import BackTracking
from csp.constraints import MaxCapacity

# =========== CSP =============

csp_problem = Container()
csp_search = BackTracking(csp_problem)

result = csp_search.run({})
print(result)
print(csp_problem.consistent(result))

containers = [ result[var] for var in result ]
map_result = { container: [var for var in result.keys() if result[var] == container] for container in set(containers) }
print('Variabili raggruppate nei container:')
print(map_result)
print('Capacità dei containers:')
print({ k: len(v) for k, v in map_result.items() })

# =========== LOCAL SEARCH =============
print('======== Local Search ==========')
from src.Problems import Containers
from src.local_search import *
import random

variables = csp_problem.variables
random.shuffle(variables)
environment = { "variables": list(variables),
                "max_capacity": 6,
                "constraints": csp_problem.constraints }
ls_problem = Containers(environment)
# HillClimbing / SimulatedAnnealing
ls_search = HillClimbing(ls_problem)
print(ls_problem.conflicts( ((), (), (), ('fz3', 'fz1')) ))
print(ls_problem.conflicts( ((), (), ('fz2',), ('fz3',)) ))

result = ls_search.run()
print(result)

