# SEARCH FOR "MY_CODE" COMMENT TO FIND MY CONTRIBUTIONS
# 6.034 Fall 2010 Lab 3: Games
# Name: Brighton Ancelin
# Email: <Your Email>

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
##
## Uncomment this line to play a game as white:
# run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board: ConnectFourBoard):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """
    # MY_CODE
    # To my understanding, this is a pretty arbitrary function.
    if board.is_win():
        # Other player won
        return -1000
    elif board.is_tie():
        return 0
    else:
        chains = board.chain_cells(board.get_current_player_id())
        inst_of_size = {}
        for chain in chains:
            size = len(chain)
            if size in inst_of_size:
                inst_of_size[size] += 1
            else:
                inst_of_size[size] = 1
        return sum([size * inst for size, inst in inst_of_size.items()])


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

# MY_CODE
from my_alpha_beta_algos import alpha_beta_iterative_w_objects

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alpha_beta_search(board: ConnectFourBoard, depth, eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		              is_terminal_fn=is_terminal):
    # MY_CODE
    root = alpha_beta_iterative_w_objects(board, depth, eval_fn,
            get_next_moves_fn, is_terminal_fn)
    # if isinstance(board, ConnectFourBoard):
    #     before_rating = eval_fn(board)
    #     after_rating = -eval_fn(board.do_move(root.best_move))
    #     print('Ratings for player {} making move {} at depth {}:'.format(
    #             board.get_current_player_id(), root.best_move, depth))
    #     print('Before:', before_rating)
    #     print('After:', after_rating)
    return root.best_move
    # def do_alpha_beta_search(board: ConnectFourBoard, depth: int, ab,
    #                          is_maximizer: bool, parent_ab,
    #                          max_depth: int, eval_fn, get_next_moves_fn,
    #                          is_terminal_fn):
    #     if is_terminal_fn(max_depth - depth, board):
    #         player_val = eval_fn(board)
    #         if not is_maximizer:
    #             player_val *= -1
    #         return (player_val, None)
    #     if parent_ab is None:
    #         if is_maximizer:
    #             def_child_ab = INFINITY
    #         else:
    #             def_child_ab = NEG_INFINITY
    #     else:
    #         def_child_ab = parent_ab
    #     best_move = None
    #     for child_move, child_board in get_next_moves_fn(board):
    #         child_eval = do_alpha_beta_search(child_board, depth+1,
    #                 def_child_ab, not is_maximizer, ab, max_depth,
    #                 eval_fn, get_next_moves_fn, is_terminal_fn)
    #         if child_eval is None:
    #             continue
    #         child_ab = child_eval[0]
    #         if is_maximizer:
    #             if child_ab > ab:
    #                 ab = child_ab
    #                 best_move = child_move
    #                 if parent_ab is not None and parent_ab <= ab:
    #                     # Get disowned
    #                     return None
    #             else:
    #                 continue
    #         else:
    #             if child_ab < ab:
    #                 ab = child_ab
    #                 best_move = child_move
    #                 if parent_ab is not None and parent_ab >= ab:
    #                     # Get disowned
    #                     return None
    #             else:
    #                 continue
    #     return (ab, best_move)
    #
    #
    # return do_alpha_beta_search(board, 0, NEG_INFINITY, True, None, depth,
    #                             eval_fn, get_next_moves_fn, is_terminal_fn)[1]

    # class AB_node:
    #     def __init__(self,
    #                  parent: AB_node,
    #                  move: int,
    #                  board: ConnectFourBoard):
    #         self.parent = parent
    #         self.children = []
    #         self.move = move  # Move that led to this node's board state
    #         self.board = board
    #         if self.parent is None:
    #             # Root Maximizer
    #             self.is_maximizer = True
    #             self.alpha_or_beta = NEG_INFINITY
    #             self.depth = 0
    #         elif self.parent.parent is None:
    #             # Depth-1 Minimizers
    #             self.is_maximizer = False
    #             self.alpha_or_beta = INFINITY
    #             self.depth = 1
    #         else:
    #             self.is_maximizer = not parent.is_maximizer
    #             # Alpha for maximizers, beta for minimizers
    #             self.alpha_or_beta = parent.inherit_alpha_or_beta(
    #                 self.is_maximizer)
    #             self.depth = parent.depth + 1
    #     def inherit_alpha_or_beta(self, child_is_maximizer: bool):
    #         if self.is_maximizer == child_is_maximizer:
    #             return self.alpha_or_beta
    #         elif self.parent is not None:
    #             # Should only go up one level
    #             return self.parent.inherit_alpha_or_beta(child_is_maximizer)
    #     def populate_children(self, get_next_moves_fn):
    #         for move, new_board in get_next_moves_fn(self.board):
    #             self.add_child(move, new_board)
    #     def add_child(self, move: int, board: ConnectFourBoard):
    #         child = AB_node(self, move, board)
    #         self.children.append(child)
    #         return child
    #     def has_children(self):
    #         return 1 <= len(self.children)
    #     def pop_next_child(self):
    #         return self.children.pop(0)
    #     def set_ab_and_update_parent(self, alpha_or_beta):
    #         self.alpha_or_beta = alpha_or_beta
    #         self.parent.update_from_child(self)
    #     def update_from_child(self, child: AB_node):
    #         if self.is_maximizer:
    #             if child.alpha_or_beta > self.alpha_or_beta:
    #                 self.set_ab_and_update_parent(child.alpha_or_beta)
    #             else:
    #                 # Unnecessary?
    #                 self.children.remove(child)
    #         else:
    #             if child.alpha_or_beta < self.alpha_or_beta:
    #                 self.set_ab_and_update_parent(child.alpha_or_beta)
    #             else:
    #                 # Unnecessary?
    #                 self.children.remove(child)
    #
    #
    # root = AB_node(None, None, board)
    # node = root
    # while :
    #     if is_terminal_fn(depth - node.depth, node.board):
    #         val = eval_fn(node.board)
    #         node.set_ab_and_update_parent(val)
    #     node.populate_children(get_next_moves_fn)
    #     node = node.pop_next_child()
    #
    # return []





## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

def better_evaluate(board: ConnectFourBoard):
    # MY_CODE
    if board.is_win():
        # Other player won
        return -1000
    elif board.is_tie():
        return -100
    else:
        cur_chains = board.chain_cells(board.get_current_player_id())
        adv_chains = board.chain_cells(board.get_other_player_id())
        cur_inst_of_size = {}
        adv_inst_of_size = {}
        for chain in cur_chains:
            size = len(chain)
            if size in cur_inst_of_size:
                cur_inst_of_size[size] += 1
            else:
                cur_inst_of_size[size] = 1
        for chain in adv_chains:
            size = len(chain)
            if size in adv_inst_of_size:
                adv_inst_of_size[size] += 1
            else:
                adv_inst_of_size[size] = 1

        choice_adjustment = 0
        # for i in range(7):
        #     if 0 != board.get_cell(0, i):
        #         choice_adjustment -= 10
        cur_score = [inst * (size ** 2) for size, inst in
                     cur_inst_of_size.items()]
        adv_score = [inst * (size ** 2) for size, inst in
                     adv_inst_of_size.items()]
        return sum(cur_score) - sum(adv_score) + choice_adjustment

    # if board.is_win():
    #     # Other player won
    #     return -1000
    # elif board.is_tie():
    #     return -100
    # else:
    #     score = 0
    #     board_arr = board.get_board_array()
    #     height = len(board_arr)
    #     width = len(board_arr[0])
    #     cur_id = board.get_current_player_id()
    #     can_index = lambda row, col: 0 <= row < height and 0 <= col < width
    #     for r in range(height):
    #         for c in range(width):
    #             id = board_arr[r][c]
    #             if 0 == id:
    #                 continue
    #             for elem in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),
    #                          (1, -1), (1, 0), (1, 1)):
    #                 d_r, d_c = elem
    #                 row = r + d_r
    #                 col = c + d_c
    #                 if can_index(row, col):
    #                     neighbor_id = board_arr[row][col]
    #                     if 0 == neighbor_id:
    #                         if id == cur_id:
    #                             score += 10
    #                         else:
    #                             score -= 10
    #                         break
    #     return score


    # else:
    #     ID = board.get_current_player_id()
    #     net_value = 0
    #     board_arr = board.get_board_array()
    #     height = len(board_arr)
    #     width = len(board_arr[0])
    #     for col in range(width):
    #         for row in range(height):
    #             top_id = board_arr[row][col]
    #             if (0 != top_id) or (height-1 == row):
    #                 if 0 == row:
    #                     break
    #                 elif 0 != top_id:
    #                     row -= 1
    #                 if ID == top_id:
    #                     chain_len = 1
    #                     new_row = row + 2
    #                     can_index = lambda r: r < height
    #                     while can_index(new_row):
    #                         if ID == board_arr[new_row][col]:
    #                             chain_len += 1
    #                             new_row += 1
    #                         else:
    #                             break
    #                     if chain_len + row + 1 >= 4:
    #                         if 1 == chain_len:
    #                             net_value += 1
    #                         elif 2 == chain_len:
    #                             net_value += 10
    #                         elif 3 == chain_len:
    #                             return 999
    #
    #                 d_c = 1
    #                 for d_r in (1, 0, -1):
    #                     row_coords = [row, -1, -1, -1]
    #                     col_coords = [col, -1, -1, -1]
    #                     chain_def = [True, False, False, False]
    #                     chain = [0, 0, 0, 0]
    #                     can_index = lambda r, c: \
    #                             0 <= r < height and 0 <= c < width
    #                     for i in range(1, 4):
    #                         row_coords[i] = row + (i * d_r)
    #                         col_coords[i] = col + (i * d_c)
    #                         if can_index(row_coords[i], col_coords[i]):
    #                             id = board_arr[row_coords[i]][col_coords[i]]
    #                             if ID == id or 0 == id:
    #                                 chain_def[i] = True
    #                                 chain[i] = id
    #                             else:
    #                                 break
    #                         else:
    #                             break
    #
    #                     best_chain_len = 0
    #                     for conv in range(4):
    #                         chain_len = 0
    #                         avail_len = 0
    #                         if all(chain_def):
    #                             for i in range(4):
    #                                 if chain_def[i]:
    #                                     if ID == chain[i]:
    #                                         chain_len += 1
    #                                     elif 0 == chain[i]:
    #                                         avail_len += 1
    #                                     else:
    #                                         # Should never run
    #                                         print('Should never run')
    #                                         break
    #                                 else:
    #                                     break
    #                             # Should be impossible to ever exceed 4
    #                             if 4 == chain_len + avail_len:
    #                                 if 3 == chain_len:
    #                                     for j in range(4):
    #                                         if 0 == chain[j]:
    #                                             ch_r = row_coords[j] + 1
    #                                             ch_c = col_coords[j]
    #                                             cond_1 = not can_index(ch_r, ch_c)
    #                                             if cond_1 or 0 != board_arr[ch_r][ch_c]:
    #                                                 return 999
    #                                             break
    #                                     net_value += 100
    #                                     break
    #                                 elif chain_len > best_chain_len:
    #                                     best_chain_len = chain_len
    #                         if conv < 3:
    #                             row_coords[1:] = row_coords[:3]
    #                             row_coords[0] = row_coords[1] - d_r
    #                             col_coords[1:] = col_coords[:3]
    #                             col_coords[0] = col_coords[1] - d_c
    #                             if can_index(row_coords[0], col_coords[0]):
    #                                 id = board_arr[row_coords[0]][col_coords[0]]
    #                                 if ID == id or 0 == id:
    #                                     chain_def[1:] = chain_def[:3]
    #                                     chain_def[0] = True
    #                                     chain[1:] = chain[:3]
    #                                     chain[0] = id
    #                                 else:
    #                                     break
    #                             else:
    #                                 break
    #                     # best_chain_len could equal 0
    #                     if 1 == best_chain_len:
    #                         net_value += 1
    #                     elif 2 == best_chain_len:
    #                         net_value += 10
    #                     elif 3 == best_chain_len:
    #                         return 999
    #                 break
    #     return net_value

        # my_score = 0
        # board_arr = board.get_board_array()
        # height = len(board_arr)
        # width = len(board_arr[0])
        # for row in range(height):
        #     for col in range(width):
        #         player_id = board_arr[row][col]
        #         if 0 != board_arr[row][col]:
        #             for d_r in (-1, 0, 1):
        #                 for d_c in (-1, 0, 1):
        #                     if 0 == d_r and 0 == d_c:
        #                         continue
        #                     elif 0 == row and -1 == d_r:
        #                         continue
        #                     elif height-1 == row and 1 == d_r:
        #                         continue
        #                     elif 0 == col and -1 == d_c:
        #                         continue
        #                     elif width-1 == col and 1 == d_c:
        #                         continue
        #                     else:
        #                         d_id = board_arr[row+d_r][col+d_c]
        #                         if 0 == d_id:
        #                             continue
        #                         elif d_id == player_id:
        #                             my_score += 1
        #                         else:
        #                             my_score -= 2
        # return my_score

        # board_arr = board.get_board_array()
        # height = len(board_arr)
        # width = len(board_arr[0])
        # my_score = 0
        # tops = [-1] * width
        # for col in range(width):
        #     for row in range(height):
        #         player_id = board_arr[row][col]
        #         if 0 != player_id:
        #             if 0 != row:
        #                 tops[col] = row - 1
        #                 if 1 == player_id:
        #                     my_score += 2
        #                 else:
        #                     my_score -= 2
        # if -1 != tops[0] and tops[0] >= tops[1]:
        #     for dr in (1, 0, -1):
        #         player_id = board_arr[tops[0]+dr][1]
        #         if 0 == player_id:
        #             break
        #         elif 1 == player_id:
        #             my_score += 1
        #         else:
        #             my_score -= 1
        # if -1 != tops[-1] and tops[-1] >= tops[-2]:
        #     for dr in (1, 0, -1):
        #         player_id = board_arr[tops[-1]+dr][-2]
        #         if 0 == player_id:
        #             break
        #         elif 1 == player_id:
        #             my_score += 1
        #         else:
        #             my_score -= 1
        # for col in range(1, width-1):
        #     if -1 != tops[col]:
        #         if tops[col] >= tops[col + 1]:
        #             for dr in (1, 0, -1):
        #                 player_id = board_arr[tops[col] + dr][col + 1]
        #                 if 0 == player_id:
        #                     break
        #                 elif 1 == player_id:
        #                     my_score += 3
        #                 else:
        #                     my_score -= 3
        #         if tops[col] >= tops[col - 1]:
        #             for dr in (1, 0, -1):
        #                 player_id = board_arr[tops[col] + dr][col - 1]
        #                 if 0 == player_id:
        #                     break
        #                 elif 1 == player_id:
        #                     my_score += 3
        #                 else:
        #                     my_score -= 3
        # # Scaling doesn't matter; it's all relative
        # return my_score





# Comment this line after you've fully implemented better_evaluate
# better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 1,0,1,2,2,0,0 ),
                    ( 1,0,2,2,1,0,0 ),
                    ( 2,0,1,1,2,0,0 ),
                    ( 1,0,2,2,1,2,0 ),
                    ( 1,0,1,2,2,1,0 ),
                    ( 1,0,1,2,2,1,2 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print('Xs: perspective:')
    print("%s => %s" %(test_board_1, better_evaluate(test_board_1)))
    # better evaluate from player 2
    print('\n\n')
    print('Os perspective:')
    print("%s => %s" %(test_board_2, better_evaluate(test_board_2)))

    print('BE 1:', basic_evaluate(test_board_1))
    print('BE 2:', basic_evaluate(test_board_2))


## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
# run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
# run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])

def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)

## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = False

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "I"
WHAT_I_FOUND_INTERESTING = "Do"
WHAT_I_FOUND_BORING = "Not"
NAME = "Want"
EMAIL = "To Answer These"

# MY_CODE
h_player = lambda board: run_search_function(board,
        search_fn=alpha_beta_search, eval_fn=memoize(focused_evaluate),
        timeout=5)

# MY_CODE
run_game(human_player, h_player)
