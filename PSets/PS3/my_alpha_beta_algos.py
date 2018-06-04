# MY_CODE
# Module for various alpha beta algorithms
from connectfour import ConnectFourBoard
from basicplayer import basic_evaluate, get_all_next_moves, is_terminal


INFINITY = float('inf')
NEG_INFINITY = float('-inf')

def alpha_beta_search_recursive(board: ConnectFourBoard, depth, eval_fn,
        # NOTE: You should use get_next_moves_fn when generating
        # next board configurations, and is_terminal_fn when
        # checking game termination.
        # The default functions set here will work
        # for connect_four.
        get_next_moves_fn=get_all_next_moves,
        is_terminal_fn=is_terminal):
    def do_alpha_beta_search(board: ConnectFourBoard, depth: int, ab,
                             is_maximizer: bool, parent_ab,
                             max_depth: int, eval_fn, get_next_moves_fn,
                             is_terminal_fn):
        if is_terminal_fn(max_depth - depth, board):
            player_val = eval_fn(board)
            if not is_maximizer:
                player_val *= -1
            return (player_val, None)
        if parent_ab is None:
            if is_maximizer:
                def_child_ab = INFINITY
            else:
                def_child_ab = NEG_INFINITY
        else:
            def_child_ab = parent_ab
        best_move = None
        for child_move, child_board in get_next_moves_fn(board):
            child_eval = do_alpha_beta_search(child_board, depth+1,
                    def_child_ab, not is_maximizer, ab, max_depth,
                    eval_fn, get_next_moves_fn, is_terminal_fn)
            if child_eval is None:
                continue
            child_ab = child_eval[0]
            if is_maximizer:
                if child_ab > ab:
                    ab = child_ab
                    best_move = child_move
                    if parent_ab is not None and parent_ab <= ab:
                        # Get disowned
                        return None
                else:
                    continue
            else:
                if child_ab < ab:
                    ab = child_ab
                    best_move = child_move
                    if parent_ab is not None and parent_ab >= ab:
                        # Get disowned
                        return None
                else:
                    continue
        return (ab, best_move)


    return do_alpha_beta_search(board, 0, NEG_INFINITY, True, None, depth,
                                eval_fn, get_next_moves_fn, is_terminal_fn)[1]


class AB_node:
    def __init__(self, board, moves_func, parent=None, move=None):
        self.board = board
        self.moves_generator = moves_func(board)
        # For some tests in the assignment tester.py, the moves_func returns
        #  a list, not a generator. This is to compensate for that, and any
        # other non-generator functions
        self.moves_generator = iter(self.moves_generator)
        self.best_move = None
        self.hide_children = False
        if parent is None:
            self.parent = None
            self.move = None
            self.depth = 0
            self.ab = NEG_INFINITY
        else:
            self.parent = parent
            self.move = move
            self.depth = parent.depth + 1
            if parent.parent is None:
                self.ab = INFINITY
            else:
                self.ab = parent.parent.ab
    # def __init__(self, board, moves_func):
    #     # Constructor for root node
    #     self.parent = None
    #     self.move = None
    #     self.depth = 0
    #     self.board = board
    #     self.ab = NEG_INFINITY
    #     self.moves_generator = moves_func(board)
    #     self.best_move = None
    #     self.hide_children = False
    # def child_constructor(self, parent, move, board, moves_func):
    #     # The inefficiencies of Python's lack of multiple constructors
    #     self.parent = parent
    #     self.move = move
    #     self.depth = parent.depth + 1
    #     self.board = board
    #     if parent.parent is None:
    #         self.ab = INFINITY
    #     else:
    #         self.ab = parent.parent.ab
    #     self.moves_generator = moves_func(board)
    #     self.best_move = None
    #     self.hide_children = False
    #     return self
    def is_maximizer(self):
        return 0 == (self.depth % 2)
    def next_child(self, move_func):
        if self.hide_children:
            return None
        try:
            next_move, next_board = next(self.moves_generator)
            return AB_node(next_board, move_func, self, next_move)
        except StopIteration:
            return None



def alpha_beta_recursive_w_objects(board: ConnectFourBoard, depth, eval_fn,
        # NOTE: You should use get_next_moves_fn when generating
        # next board configurations, and is_terminal_fn when
        # checking game termination.
        # The default functions set here will work
        # for connect_four.
        get_next_moves_fn=get_all_next_moves,
        is_terminal_fn=is_terminal):
    """
    Returns the best ab and the best move
    :param board:
    :param depth:
    :param eval_fn:
    :param get_next_moves_fn:
    :param is_terminal_fn:
    :return:
    """
    def do_alpha_beta_search(node: AB_node, my_eval_fn, get_next_moves_fn,
                             my_is_terminal_fn):
        if my_is_terminal_fn(node):
            player_val = my_eval_fn(node)
            if not node.is_maximizer():
                player_val *= -1
            node.ab = player_val
            return (node.ab, None)
        best_move = None
        child = node.next_child(get_next_moves_fn)
        while child is not None:
            child_eval = do_alpha_beta_search(child, my_eval_fn,
                    get_next_moves_fn, my_is_terminal_fn)
            if child_eval is not None:
                if node.is_maximizer():
                    if child.ab > node.ab:
                        node.ab = child.ab
                        best_move = child.move
                        if node.parent is not None and node.parent.ab <= node.ab:
                            # Get disowned
                            return None
                else:
                    if child.ab < node.ab:
                        node.ab = child.ab
                        best_move = child.move
                        if node.parent is not None and node.parent.ab >= node.ab:
                            # Get disowned
                            return None
            child = node.next_child(get_next_moves_fn)
        return (node.ab, best_move)

    my_eval_fn = lambda node: eval_fn(node.board)
    my_is_terminal_fn = lambda node: \
            is_terminal_fn(depth - node.depth, node.board)
    root = AB_node(board, get_next_moves_fn)
    return do_alpha_beta_search(root, my_eval_fn, get_next_moves_fn,
                                my_is_terminal_fn)[1]


def alpha_beta_recursive_flipped_w_objects(board: ConnectFourBoard, depth,
                                        eval_fn,
        # NOTE: You should use get_next_moves_fn when generating
        # next board configurations, and is_terminal_fn when
        # checking game termination.
        # The default functions set here will work
        # for connect_four.
        get_next_moves_fn=get_all_next_moves,
        is_terminal_fn=is_terminal):
    """
    Returns the best ab and the best move
    :param board:
    :param depth:
    :param eval_fn:
    :param get_next_moves_fn:
    :param is_terminal_fn:
    :return:
    """
    def do_alpha_beta_search(node: AB_node, my_eval_fn, get_next_moves_fn,
                             my_is_terminal_fn):
        if my_is_terminal_fn(node):
            player_val = my_eval_fn(node)
            if not node.is_maximizer():
                player_val *= -1
            node.ab = player_val
            return (node.ab, None)
        node.best_move = None
        child = node.next_child(get_next_moves_fn)
        while child is not None:
            child_eval = do_alpha_beta_search(child, my_eval_fn,
                    get_next_moves_fn, my_is_terminal_fn)
            if child_eval is not None:
                if node.is_maximizer():
                    if child.ab > node.ab:
                        node.ab = child.ab
                        node.best_move = child.move
                        if node.parent is not None and node.parent.ab <= node.ab:
                            # Get disowned
                            return None
                else:
                    if child.ab < node.ab:
                        node.ab = child.ab
                        node.best_move = child.move
                        if node.parent is not None and node.parent.ab >= node.ab:
                            # Get disowned
                            return None
            child = node.next_child(get_next_moves_fn)
        return (node.ab, node.best_move)

    my_eval_fn = lambda node: eval_fn(node.board)
    my_is_terminal_fn = lambda node: \
            is_terminal_fn(depth - node.depth, node.board)
    root = AB_node(board, get_next_moves_fn)
    return do_alpha_beta_search(root, my_eval_fn, get_next_moves_fn,
                                my_is_terminal_fn)[1]


def alpha_beta_iterative_w_objects(board: ConnectFourBoard, depth, eval_fn,
        # NOTE: You should use get_next_moves_fn when generating
        # next board configurations, and is_terminal_fn when
        # checking game termination.
        # The default functions set here will work
        # for connect_four.
        get_next_moves_fn=get_all_next_moves,
        is_terminal_fn=is_terminal):

    my_eval_fn = lambda node: eval_fn(node.board)
    my_is_terminal_fn = lambda node: \
            is_terminal_fn(depth - node.depth, node.board)
    root = AB_node(board, get_next_moves_fn)

    node = root
    while node is not None:
        child = node.next_child(get_next_moves_fn)
        if child is not None:
            node = child
            if my_is_terminal_fn(node):
                player_val = my_eval_fn(node)
                if not node.is_maximizer():
                    player_val *= -1
                node.ab = player_val
                node.hide_children = True
                # node has no children now. It's called hide_children
                # because technically, the node may have children, we just
                # don't have time to evaluate them
        else:
            # No more children; parent will now decide if it wants the ab
            child = node
            node = node.parent
            if node is None:
                # root has no more children (and is called child). Return the
                # result
                # This block of code should ALWAYS be reached
                return child
            if node.is_maximizer():
                if child.ab > node.ab:
                    node.ab = child.ab
                    node.best_move = child.move
                    if node.parent is not None and node.parent.ab <= node.ab:
                        # Get disowned
                        node = node.parent
            else:
                if child.ab < node.ab:
                    node.ab = child.ab
                    node.best_move = child.move
                    if node.parent is not None and node.parent.ab >= node.ab:
                        # Get disowned
                        node = node.parent
    raise ValueError("Somewhere something went wrong. "
                     "This shouldn't be reachable")

def get_alpha_beta_root(board, get_next_moves_fn=get_all_next_moves):
    return AB_node(board, get_next_moves_fn)

def alpha_beta_iterative_w_root(root: AB_node, depth, eval_fn,
        # NOTE: You should use get_next_moves_fn when generating
        # next board configurations, and is_terminal_fn when
        # checking game termination.
        # The default functions set here will work
        # for connect_four.
        get_next_moves_fn=get_all_next_moves,
        is_terminal_fn=is_terminal):

    my_eval_fn = lambda node: eval_fn(node.board)
    my_is_terminal_fn = lambda node: \
            is_terminal_fn(depth - node.depth, node.board)

    node = root
    while node is not None:
        child = node.next_child(get_next_moves_fn)
        if child is not None:
            node = child
            if my_is_terminal_fn(node):
                player_val = my_eval_fn(node)
                if not node.is_maximizer():
                    player_val *= -1
                node.ab = player_val
                node.hide_children = True
                # node has no children now. It's called hide_children
                # because technically, the node may have children, we just
                # don't have time to evaluate them
        else:
            # No more children; parent will now decide if it wants the ab
            child = node
            node = node.parent
            if node is None:
                # root has no more children (and is called child). Return the
                # result
                # This block of code should ALWAYS be reached
                return child
            if node.is_maximizer():
                if child.ab > node.ab:
                    node.ab = child.ab
                    node.best_move = child.move
                    if node.parent is not None and node.parent.ab <= node.ab:
                        # Get disowned
                        node = node.parent
            else:
                if child.ab < node.ab:
                    node.ab = child.ab
                    node.best_move = child.move
                    if node.parent is not None and node.parent.ab >= node.ab:
                        # Get disowned
                        node = node.parent
    raise ValueError("Somewhere something went wrong. "
                     "This shouldn't be reachable")
