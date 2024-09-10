from csp.problem import *
from csp.backtracking import *
from input.words import words

# ==================== CSP ====================
problem = Cruciverba(words)

search = BackTracking(problem=problem,
                      var_criterion=random_variable,
                      value_criterion=random_assignment)
initial_state = {}
result = search.run(state=initial_state)
print(result)


# ==================== LOCAL SEARCH ====================
from src.Problems import Cruciverba as Cruciverba_ls
from src.local_search import *

ls_problem = Cruciverba_ls(words)

local_search = HillClimbing(ls_problem)

ls_result = local_search.run()
print(ls_result)