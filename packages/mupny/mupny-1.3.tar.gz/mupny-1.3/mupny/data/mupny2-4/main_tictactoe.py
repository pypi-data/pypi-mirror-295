from game.games import TicTacToe
from game.search import *

initial_state = (1, 0, -1, 0, 0, 0, 0, 0, 0)
problem = TicTacToe(player='MAX')
actions = problem.actions(initial_state)
print(actions)
for action in actions:
    print(f'action : {action}')
    print(problem.result(initial_state, action))

print(f'utiity of {initial_state} : {problem.utility(initial_state)}')
print(problem.successors(initial_state))
print(f'terminal test: {problem.terminal_test(initial_state)}')


search = Minimax(game=problem)
move = search.next_move(initial_state)
print(move)

