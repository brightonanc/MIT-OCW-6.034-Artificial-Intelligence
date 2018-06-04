# MY_CODE
# Quick tester
from my_alpha_beta_algos import alpha_beta_iterative_w_objects


my_board = 'A'
my_board_graph = {'A': ('B', 'C', 'D'),
                  'B': ('E', 'F'),
                  'C': ('G', 'H'),
                  'D': ('I', 'J'),
                  'E': 2,
                  'F': ('K', 'L'),
                  'G': ('M', 'N'),
                  'H': 6,
                  'I': 1,
                  'J': ('O', 'P'),
                  'K': -3,
                  'L': -0,
                  'M': ('Q', 'R'),
                  'N': -7,
                  'O': -2,
                  'P': -20,
                  'Q': 1,
                  'R': 10,
                  }


def my_next_tree_move(board):
    for next in my_board_graph[board]:
        yield (next, next)

def my_is_terminal(depth, board):
    return isinstance(my_board_graph[board], int)

def my_eval_fn(board):
    return my_board_graph[board]

res = alpha_beta_iterative_w_objects(my_board, 10, my_eval_fn,
                                    my_next_tree_move, my_is_terminal)
print(res)
