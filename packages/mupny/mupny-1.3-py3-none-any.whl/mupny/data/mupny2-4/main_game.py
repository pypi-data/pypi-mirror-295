from game.games import DummyGame
from game.search import *

game = DummyGame('A')

actions = game.actions('A')

print(actions)

for action in actions:
    result = game.result('A', action=action)
    print(result)
    print(game.actions(result))
print(game.result('D', 'd3'))
print(game.player_utility('D2'))

search = Minimax(game=game)
print("=================")
move = search.next_move(game.initial_state)
print(move)