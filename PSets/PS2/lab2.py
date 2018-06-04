# SEARCH FOR "MY_CODE" COMMENT TO FIND MY CONTRIBUTIONS
# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph



# MY_CODE
# Decided to try and implement the broadest sense of a search algorithm
def search(graph, start, goal, max_agenda_size=-1,
           flag_extended_set=False, data_struct_type=0,
           pqueue_sort_key=None, flag_full_breadth=False):
    """
    data_struct_type=0: queue (think BFS)
    data_struct_type=1: stack (think DFS)
    data_struct_type=2: priority queue (think B&B) (requires pqueue_sort_key be defined)
    :param graph:
    :param start:
    :param goal:
    :param max_agenda_size:
    :param flag_extended_set:
    :param data_struct_type:
    :param pqueue_sort_key:
    :return:
    """
    agenda = [[start]]
    if flag_extended_set:
        extended_set = set()
    while agenda:
        condition = True
        new_paths = []
        while condition or (flag_full_breadth and agenda):
            condition = False
            partial_path = agenda.pop(0)
            node_to_extend = partial_path[-1]
            if node_to_extend == goal:
                return partial_path
            if flag_extended_set:
                extended_set.add(node_to_extend)
            for extension in graph.get_connected_nodes(node_to_extend):
                if extension not in partial_path:
                    if (not flag_extended_set) or (extension not in extended_set):
                        new_paths.append([*partial_path, extension])
        if pqueue_sort_key is not None:
            new_paths.sort(key=pqueue_sort_key)
        if 0 == data_struct_type:
            for path in new_paths:
                agenda.append(path)
        elif 1 == data_struct_type:
            new_paths.reverse()
            for path in new_paths:
                agenda.insert(0, path)
        elif 2 == data_struct_type:
            agenda = my_merge(agenda, new_paths, pqueue_sort_key)
        if -1 != max_agenda_size:
            if len(agenda) > max_agenda_size:
                agenda = agenda[:max_agenda_size]
    return []






## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    # MY_CODE
    return search(graph, start, goal, flag_extended_set=True,
                  data_struct_type=0, flag_full_breadth=False)
    # # MY_CODE
    # # Iterative------------------------------------------------------
    # agenda = [[start]]
    # while agenda:
    #     cur_path_to_goal = agenda.pop(0)
    #     node_to_extend = cur_path_to_goal[-1]
    #     if node_to_extend == goal:
    #         return cur_path_to_goal
    #     for extension in graph.get_connected_nodes(node_to_extend):
    #         if extension not in cur_path_to_goal:
    #             # We won't break ties. We won't observe lexographical order.
    #             #  We don't care.
    #             agenda.append([*cur_path_to_goal[:], extension])
    # return []
    # Iterative w/ extended list----------------------------------------
    # MY_CODE
    agenda = [[start]]
    extended_list = [start]
    while agenda:
        cur_path_to_goal = agenda.pop(0)
        node_to_extend = cur_path_to_goal[-1]
        if node_to_extend == goal:
            return cur_path_to_goal
        extended_list.append(node_to_extend)
        for extension in graph.get_connected_nodes(node_to_extend):
            #if extension not in cur_path_to_goal and extension not in extended_list:
            # If extension not in extended_list, extension is guaranteed to
            # not be in cur_path_to_goal, so we'll use only the stronger
            # condition
            if extension not in extended_list:
                # We won't break ties. We won't observe lexographical order.
                #  We don't care.
                agenda.append([*cur_path_to_goal[:], extension])
    return []


## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    # MY_CODE
    return search(graph, start, goal, flag_extended_set=True,
                  data_struct_type=1)
    def dfs_iterative_backtracking(graph, start, goal, to_print=False):
        # MY_CODE
        # Iterative w/ backtracking-------------------------------------------
        # diagnostics
        DIAG_EXT = 0
        DIAG_AG_SZ = 0
        DIAG_MODS = 0
        agenda = [[start]]
        while agenda:
            DIAG_AG_SZ = max(sum([len(elem) for elem in agenda]), DIAG_AG_SZ)
            cur_path_to_goal = agenda.pop(0)
            node_to_extend = cur_path_to_goal[-1]
            if node_to_extend == goal:
                if to_print:
                    print('DFS Iterative w/ backtracking: Path found')
                    print('Total number of extensions made:', DIAG_EXT)
                    print('Largest number of nested elements in agenda:', DIAG_AG_SZ)
                    print('Total number of agenda modifications made:', DIAG_MODS)
                return cur_path_to_goal
            DIAG_EXT += 1
            for extension in graph.get_connected_nodes(node_to_extend):
                if extension not in cur_path_to_goal:
                    # We won't break ties. We won't observe lexographical order.
                    #  We don't care.
                    agenda.insert(0, [*cur_path_to_goal[:], extension])
                    DIAG_MODS += 1
        if to_print:
            print('DFS Iterative w/ backtracking: No path found')
            print('Total number of extensions made:', DIAG_EXT)
            print('Largest number of nested elements in agenda:', DIAG_AG_SZ)
            print('Total number of agenda modifications made:', DIAG_MODS)
        return []

    def dfs_recursive_backtracking(graph, start, goal, to_print=False):
        # MY_CODE
        # Recursive w/ backtracking--------------------------------------------
        # DFS can be recursive because it uses a stack, not a queue (BFS uses a
        # queue)
        # diagnostics
        DIAG_EXT = 0
        DIAG_MODS = 0
        def do_dfs(graph, cur_path_to_goal, goal, DIAGs):
            node_to_extend = cur_path_to_goal[-1]
            if node_to_extend == goal:
                return cur_path_to_goal
            DIAGs[0] += 1
            for extension in graph.get_connected_nodes(node_to_extend):
                if extension not in cur_path_to_goal:
                    # We won't break ties. We won't observe lexographical order.
                    #  We don't care.
                    # agenda.insert(0, [*cur_path_to_goal[:], extension])
                    final_path = do_dfs(graph, [*cur_path_to_goal[:], extension],
                                        goal, DIAGs)
                    DIAGs[1] += 1
                    if final_path:
                        return final_path
            return []
        # MY_CODE
        DIAGs = [DIAG_EXT, DIAG_MODS]
        ans = do_dfs(graph, [start], goal, DIAGs)
        DIAG_EXT, DIAG_MODS = DIAGs
        if to_print:
            if ans:
                print('DFS Recursive w/ backtracking: Path found')
            else:
                print('DFS Recursive w/ backtracking: No path found')
            print('Total number of extensions made:', DIAG_EXT)
            print('Total number of "agenda modifications" made:', DIAG_MODS)
        return ans

    def dfs_iterative_backtracking_extensions_list(graph, start, goal,
                                                   to_print=False):
        # MY_CODE
        # Iterative w/ Extensions list-----------------------------------------
        # diagnostics
        DIAG_EXT = 0
        DIAG_AG_SZ = 0
        DIAG_MODS = 0
        agenda = [[start]]
        extended_list = [start]
        while agenda:
            DIAG_AG_SZ = max(sum([len(elem) for elem in agenda]), DIAG_AG_SZ)
            cur_path_to_goal = agenda.pop(0)
            node_to_extend = cur_path_to_goal[-1]
            if node_to_extend == goal:
                if to_print:
                    print('DFS Iterative w/ backtracking & extensions: Path found')
                    print('Total number of extensions made:', DIAG_EXT)
                    print('Largest number of nested elements in agenda:', DIAG_AG_SZ)
                    print('Total number of agenda modifications made:', DIAG_MODS)
                return cur_path_to_goal
            extended_list.append(node_to_extend)
            DIAG_EXT += 1
            for extension in graph.get_connected_nodes(node_to_extend):
                #if extension not in cur_path_to_goal and extension not in extended_list:
                # If extension not in extended_list, extension is guaranteed to
                # not be in cur_path_to_goal, so we'll use only the stronger
                # condition
                if extension not in extended_list:
                    # We won't break ties. We won't observe lexographical order.
                    #  We don't care.
                    agenda.insert(0, [*cur_path_to_goal[:], extension])
                    DIAG_MODS += 1
        if to_print:
            print('DFS Iterative w/ backtracking & extensions: No path found')
            print('Total number of extensions made:', DIAG_EXT)
            print('Largest number of nested elements in agenda:', DIAG_AG_SZ)
            print('Total number of agenda modifications made:', DIAG_MODS)
        return []
    # MY_CODE
    dfs_iterative_backtracking(graph, start, goal)
    dfs_recursive_backtracking(graph, start, goal)
    return dfs_iterative_backtracking_extensions_list(graph, start, goal)



## Now we're going to add some heuristics into the search.
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    # MY_CODE
    sort_key = lambda path: graph.get_heuristic(path[-1], goal)
    return search(graph, start, goal, data_struct_type=1,
                  pqueue_sort_key=sort_key, )
    agenda = [[start]]
    while agenda:
        partial_path = agenda.pop(0)
        node_to_extend = partial_path[-1]
        if node_to_extend == goal:
            return partial_path
        extensions = []
        for extension in graph.get_connected_nodes(node_to_extend):
            if extension not in partial_path:
                extensions.append(extension)
        extensions.sort(key=(lambda x: graph.get_heuristic(x, goal)))
        extensions.reverse()
        for extension in extensions:
            agenda.insert(0, [*partial_path, extension])
    return []


## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    # MY_CODE
    sort_key = lambda path: graph.get_heuristic(path[-1], goal)
    return search(graph, start, goal, max_agenda_size=beam_width,
                  data_struct_type=2, pqueue_sort_key=sort_key,
                  flag_full_breadth=True)
    agenda = [[start]]
    while agenda:
        new_agenda = []
        for partial_path in agenda:
            node_to_expand = partial_path[-1]
            if node_to_expand == goal:
                return partial_path
            for expansion in graph.get_connected_nodes(node_to_expand):
                if expansion not in partial_path:
                    new_agenda.append([*partial_path, expansion])
        # For each partial path, get the heuristic between the terminating
        # node and the goal node
        sorting_lambda = lambda path: graph.get_heuristic(path[-1], goal)
        new_agenda.sort(key=sorting_lambda)
        if len(new_agenda) > beam_width:
            agenda = new_agenda[:beam_width]
        else:
            agenda = new_agenda
    return []


## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    # MY_CODE
    total_length = 0
    for i in range(len(node_names)-1):
        total_length += graph.get_edge(node_names[i], node_names[i+1]).length
    return total_length


def branch_and_bound(graph, start, goal):
    # MY_CODE
    sort_key = lambda path: path_length(graph, path)
    return search(graph, start, goal, data_struct_type=2,
                  pqueue_sort_key=sort_key)
    agenda = [[start]]
    while agenda:
        partial_path = agenda.pop(0)
        node_to_expand = partial_path[-1]
        if node_to_expand == goal:
            return partial_path
        new_paths = []
        for expansion in graph.get_connected_nodes(node_to_expand):
            if expansion not in partial_path:
                new_paths.append([*partial_path, expansion])
        # Sort by path length
        sorting_lambda = lambda path: path_length(graph, path)
        new_paths.sort(key=sorting_lambda)
        agenda = my_merge(agenda, new_paths, sorting_lambda)
    return []

# MY_CODE
def my_merge(list_1, list_2, key=lambda x: x):
    """ Quick function to improve the performance of branch_and_bound
    Uses the mergesort algorithm to save the headache of resorting the
    entire agenda every time we modify it.

    Given two sorted lists and a key, we merge them into one sorted list and
    return the answer. Preference is given to the elements of the first list
    in the cases of ties
    """
    list_res = []
    while list_1 and list_2:
        if key(list_1[0]) <= key(list_2[0]):
            list_res.append(list_1.pop(0))
        else:
            list_res.append(list_2.pop(0))
    if list_1:
        [list_res.append(elem) for elem in list_1]
    elif list_2:
        [list_res.append(elem) for elem in list_2]
    return list_res


def a_star(graph, start, goal):
    # MY_CODE
    sort_key = lambda path: \
                graph.get_heuristic(path[-1], goal) + path_length(graph, path)
    return search(graph, start, goal, flag_extended_set=True,
                  data_struct_type=2, pqueue_sort_key=sort_key)
    agenda = [[start]]
    extended_set = {start}  # This is a set, NOT A DICT
    while agenda:
        partial_path = agenda.pop(0)
        node_to_extend = partial_path[-1]
        if node_to_extend == goal:
            return partial_path
        new_paths = []
        extended_set.add(node_to_extend)
        for extension in graph.get_connected_nodes(node_to_extend):
            #if extension not in partial_path and extension not in extended_set:
            # Just use the stronger conditional only (if extension not in
            # extended_set, then extension is guaranteed to not be in
            # partial_path because partial path is composed of a subset of
            # nodes in extended_set)
            if extension not in extended_set:
                new_paths.append([*partial_path, extension])
        sorting_lambda = lambda path: \
                graph.get_heuristic(path[-1], goal) + path_length(graph, path)
        new_paths.sort(key=sorting_lambda)
        agenda = my_merge(agenda, new_paths, sorting_lambda)
    return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    # MY_CODE
    # assert 0 == graph.get_heuristic(goal, goal), \
    #         "This path is distance 0. Assuming all paths will have positive " \
    #         "weights, 0 is the only permissible heuristic for goal-goal pair."
    if 0 != graph.get_heuristic(goal, goal):
        return False
    agenda = [[goal]]
    extended_set = {goal}
    while agenda:
        partial_path = agenda.pop(0)
        node_to_extend = partial_path[-1]
        extended_set.add(node_to_extend)
        for extension in graph.get_connected_nodes(node_to_extend):
            if extension not in extended_set:
                new_path = [*partial_path, extension]
                if graph.get_heuristic(extension, goal) \
                        > path_length(graph, new_path):
                    return False
    # for node in graph.nodes:
    #     if node not in extended_set:
    #         # Heuristic could reasonably be anything because this node is
    #         # unreachable from goal (assuming undirected graphs). So long as
    #         # heuristic is >= 0, that is
    return True


def is_consistent(graph, goal):
    # MY_CODE
    for edge in graph.edges:
        if edge.length < abs(graph.get_heuristic(edge.node1, goal) -
                             graph.get_heuristic(edge.node2, goal)):
            return False
    return True


HOW_MANY_HOURS_THIS_PSET_TOOK = '5'
WHAT_I_FOUND_INTERESTING = 'Most'
WHAT_I_FOUND_BORING = 'None'



# MY_CODE
def dijkstra(graph, start, goal):
    # MY_CODE
    agenda_nodes = [start]
    ancestors = {}
    distances = {start: 0}
    extended_set = set()
    while agenda_nodes:
        node_to_extend = agenda_nodes.pop(0)
        if node_to_extend == goal:
            # construct the path
            path = [goal]
            while path[0] != start:
                path.insert(0, ancestors[path[0]])
            return path
        extended_set.add(node_to_extend)
        new_agenda_nodes = []
        for extension in graph.get_connected_nodes(node_to_extend):
            if (extension not in extended_set) \
                    and (extension not in agenda_nodes):
                new_agenda_nodes.append(extension)
            edge_length = graph.get_edge(node_to_extend, extension).length
            total_extension_path_length = \
                    distances[node_to_extend] + edge_length
            if (extension not in distances) or \
                    total_extension_path_length < distances[extension]:
                ancestors[extension] = node_to_extend
                distances[extension] = total_extension_path_length
        sort_key = lambda node: distances[node]
        new_agenda_nodes.sort(key=sort_key)
        agenda_nodes = my_merge(agenda_nodes, new_agenda_nodes, sort_key)
    return []

# MY_CODE
if __name__ == '__main__':
    from search import NAME, VAL, NODE1, NODE2
    MY_GRAPH = Graph(edgesdict=[
        {NAME: '1', VAL: 10, NODE1: 'S', NODE2: 'A'},
        {NAME: '2', VAL: 8, NODE1: 'S', NODE2: 'C'},
        {NAME: '3', VAL: 3, NODE1: 'S', NODE2: 'B'},
        {NAME: '4', VAL: 3, NODE1: 'A', NODE2: 'C'},
        {NAME: '5', VAL: 3, NODE1: 'B', NODE2: 'C'},
        {NAME: '6', VAL: 3, NODE1: 'C', NODE2: 'D'},
        {NAME: '7', VAL: 12, NODE1: 'C', NODE2: 'G'},
        {NAME: '8', VAL: 4, NODE1: 'C', NODE2: 'E'},
        {NAME: '9', VAL: 10, NODE1: 'D', NODE2: 'G'},
        {NAME: '10', VAL: 4, NODE1: 'E', NODE2: 'G'}],
                    # Heuristic is not admissible nor consistent
                    heuristic={'G': {
                        'S': 0,
                        'A': 5,
                        'B': 10,
                        'C': 7,
                        'D': 0,
                        'E': 9,
                        'G': 0
                    }})
    print(a_star(MY_GRAPH, 'S', 'G'))
