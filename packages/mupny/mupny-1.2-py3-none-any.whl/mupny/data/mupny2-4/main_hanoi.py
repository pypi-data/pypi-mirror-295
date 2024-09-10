from src.Problems import HanoiTower
from src.GraphSearch import *
from src.strategies import *

initial_state = {
    'A': [3, 2, 1],
    'B': [],
    'C': []
}

goal_state = {
    'A': [],
    'B': [],
    'C': [3, 2, 1]
}

problem = HanoiTower(initial_state, goal_state)
search = GraphSearch(problem=problem, strategy=AStar(problem))
result, node = search.run()
print(result)
print(node)
print(node.path())


