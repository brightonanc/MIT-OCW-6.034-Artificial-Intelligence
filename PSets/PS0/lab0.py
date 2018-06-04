# SEARCH FOR "MY_CODE" COMMENT TO FIND MY CONTRIBUTIONS
# This is the file you'll use to submit most of Lab 0.

# Certain problems may ask you to modify other files to accomplish a certain
# task. There are also various other files that make the problem set work, and
# generally you will _not_ be expected to modify or even understand this code.
# Don't get bogged down with unnecessary work.


# Section 1: Problem set logistics ___________________________________________

# This is a multiple choice question. You answer by replacing
# the symbol 'fill-me-in' with a number, corresponding to your answer.

# You get to check multiple choice answers using the tester before you
# submit them! So there's no reason to worry about getting them wrong.
# Often, multiple-choice questions will be intended to make sure you have the
# right ideas going into the problem set. Run the tester right after you
# answer them, so that you can make sure you have the right answers.

# What version of Python do we *recommend* (not "require") for this course?
#   1. Python v2.3
#   2. Python v2.5 or Python v2.6
#   3. Python v3.0
# Fill in your answer in the next line of code ("1", "2", or "3"):

ANSWER_1 = '2'


# Section 2: Programming warmup _____________________________________________

# Problem 2.1: Warm-Up Stretch

def cube(x):
    # MY_CODE
    return x ** 3

def factorial(x):
    # MY_CODE
    assert x >= 0 and type(x) == int, "x must be non-negative int"
    if 0 == x:
        return 1
    else:
        return x * factorial(x-1)


def count_pattern(pattern, lst):
    # MY_CODE
    # Much simpler implementation:
    # (I did the below for fun/challenge)
    # matches = 0
    # for i in range(len(lst)-len(pattern)+1):
    #     if all([pattern[j] == lst[i+j] for j in range(len(pattern))]):
    #         matches += 1
    # return matches

    # Turns out they might give lists as symbols, so I have to ensure
    # everything is hashable (tuples) for the dictionary implementation below:
    pattern = [tuple(p) if isinstance(p, list) else p for p in pattern]
    lst = [tuple(l) if isinstance(l, list) else l for l in lst]

    # MY_CODE
    def build_state_machine(pattern, overlapping = True):
        """ Builds a state machine to detect the pattern
        The state machine is represented as a list of dicts.
        Each element in the list is a state.
        The dict at each entry in the list has keys that represent next
        values in the sequence. These keys map to the index in the list for
        the next state.
        """
        # Not a fully optimized algorithm, but was fun to make nonetheless
        states_list = []
        zeroth_symbol = pattern[0]
        state_transit_dict = {zeroth_symbol: 1}
        states_list += [state_transit_dict]
        return_routes = []
        for i in range(len(pattern) - 1):
            next_symbol = pattern[i + 1]
            state_transit_dict = {next_symbol: i + 2}
            for route in return_routes:
                if pattern[route] not in state_transit_dict:
                    state_transit_dict[pattern[route]] = route + 1
            if zeroth_symbol not in state_transit_dict:
                state_transit_dict[zeroth_symbol] = 1
            states_list += [state_transit_dict]
            return_routes_remove_list = []
            for j in range(len(return_routes)):
                route = return_routes[j]
                if next_symbol == pattern[route]:
                    return_routes[j] += 1
                else:
                    return_routes_remove_list += [return_routes[j]]
            [return_routes.remove(elem) for elem in return_routes_remove_list]
            if next_symbol == zeroth_symbol:
                return_routes += [1]
        if overlapping:
            state_transit_dict = {}
            for route in return_routes:
                if pattern[route] not in state_transit_dict:
                    state_transit_dict[pattern[route]] = route + 1
            if zeroth_symbol not in state_transit_dict:
                state_transit_dict[zeroth_symbol] = 1
            states_list += [state_transit_dict]
        return states_list
    # MY_CODE
    states_list = build_state_machine(pattern)
    state = states_list[0]
    matches = 0
    for symbol in lst:
        if symbol in state:
            next_state_ind = state[symbol]
            # I know I SHOULD do greater than or equal to, but should never
            # be greater than so equal to SHOULD suffice
            if next_state_ind == (len(states_list) - 1):
                matches += 1
            state = states_list[next_state_ind]
        else:
            state = states_list[0]
    return matches

# Problem 2.2: Expression depth

def depth(expr):
    # MY_CODE
    if not isinstance(expr, (list, tuple)):
        return 0
    else:
        return 1 + max([depth(x) for x in expr])


# Problem 2.3: Tree indexing

def tree_ref(tree, index):
    # MY_CODE
    if 1 == len(index):
        return tree[index[0]]
    else:
        return tree_ref(tree, index[:-1])[index[-1]]


# Section 3: Symbolic algebra

# Your solution to this problem doesn't go in this file.
# Instead, you need to modify 'algebra.py' to complete the distributer.

from algebra import Sum, Product, simplify_if_possible
from algebra_utils import distribution, encode_sumprod, decode_sumprod

# Section 4: Survey _________________________________________________________

# Please answer these questions inside the double quotes.

# When did you take 6.01?
WHEN_DID_YOU_TAKE_601 = ""

# How many hours did you spend per 6.01 lab?
HOURS_PER_601_LAB = ""

# How well did you learn 6.01?
HOW_WELL_I_LEARNED_601 = ""

# How many hours did this lab take?
HOURS = ""
