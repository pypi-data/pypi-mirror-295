from input.roads import *
from src.Problems import *
from src.strategies import *
from src.TreeSearch import TreeSearch
from src.GraphSearch import GraphSearch

streets = Roads(streets=roads_small, coordinates=roads_small_coords)

initial_state = 'Andria'
goal_state = 'Bari'
map_problem = StreetProblem(
    environment=streets,
    goal_state=goal_state,
    initial_state=initial_state)

# TreeSearch / GraphSearch
# strategy = AStar(problem=map_problem) / DepthLimitedSearch(limit=3)
search = TreeSearch(problem=map_problem, strategy=AStar(problem=map_problem))
result, node = search.run()
print(result)
print(node.path())
print(node.cost)