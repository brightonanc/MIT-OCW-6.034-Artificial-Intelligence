
# SEARCH FOR "MY_CODE" COMMENT TO FIND MY CONTRIBUTIONS

from classify import *
import math

# MY_CODE
import matplotlib.pyplot as plt

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False, cur_var_data=None):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    # Now that we've run basic_constraint_checker, we know that all assigned
    #  variables are valid. This means we only need to worry about domains
    # in the next step; no need to concern ourselves with the validity of
    # values.
    if not basic:
        return False
    if 0 > state.variable_index:
        return True
    # MY_CODE
    if cur_var_data is None:
        # This default setting is used when this method alone is used for
        # checking
        cur_var = state.get_current_variable()
        # Guaranteed to have an assigned value because it's the current
        # variable in the state object.
        cur_var_value = cur_var.get_assigned_value()
    else:
        # This alternate setting is used when this method is used as a
        # helper to forward_checking_prop_singleton()
        cur_var, cur_var_value = cur_var_data
    neighbor_constraints = state.get_constraints_by_name(cur_var.get_name())
    for constraint in neighbor_constraints:
        neighbor = state.get_variable_by_name(constraint.get_variable_j_name())
        # BEWARE: This domain is not a reference to the actual domain; it is
        #  a copy! One must call the reduce_domain() function to alter the
        # domain
        neighbor_domain = neighbor.get_domain()
        for domain_possibility in neighbor_domain:
            if not constraint.check(state,
                                    value_i=cur_var_value,
                                    value_j=domain_possibility):
                neighbor.reduce_domain(domain_possibility)
        if not neighbor.get_domain():
            return False
    return True


# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False
    # MY_CODE
    if 0 > state.variable_index:
        return True
    cur_var = state.get_current_variable()
    # Guaranteed to have an assigned value because it's the current
    # variable in the state object.s
    cur_var_value = cur_var.get_assigned_value()
    agenda = [(cur_var, cur_var_value)]
    visited_singletons = set()
    while agenda:
        # Var_data holds the data of a singleton
        # On the first run of this loop, it may not technically be a
        # singleton (domain size may be larger than 1), but we have given it an
        # assigned value so we may treat it as one in this routine.
        var_data = agenda.pop(0)
        visited_singletons.add(var_data[0].get_name())
        if not forward_checking(state, verbose, cur_var_data=var_data):
            return False
        neighbor_constraints = \
                state.get_constraints_by_name(var_data[0].get_name())
        neighbors = \
                [state.get_variable_by_name(constraint.get_variable_j_name())
                 for constraint in neighbor_constraints]
        for neighbor in neighbors:
            is_singleton = lambda var: 1 == len(var.get_domain())
            if is_singleton(neighbor) and \
                    neighbor.get_name() not in visited_singletons:
                # Doesn't matter whether we do a BFS or DFS here, so I'll
                # just choose BFS (append for BFS, insert at 0 for DFS)
                agenda.append((neighbor, neighbor.get_domain()[0]))
    return True


## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
# print('Hamming distance results:')
# evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # MY_CODE
    assert len(list1) == len(list2), 'Lists must be equal length'
    dist = 0
    for i in range(len(list1)):
        dist += (list1[i] - list2[i]) ** 2
    dist **= 0.5
    return dist


#Once you have implemented euclidean_distance, you can check the results:
# print('Euclidean distance results:')
# evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1,
#          senate_group2, verbose=True)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

# MY_CODE
my_classifier = nearest_neighbors(euclidean_distance, 5)
# evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
# print(CongressIDTree(senate_people, senate_votes, homogeneous_disorder))

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    # MY_CODE
    # disorder = 0
    # if yes:
    #     total = len(yes)
    #     occ = max([yes.count(e) for e in set(yes)]) / total
    #     disorder += -total * math.log2(1 - ((occ * (1 - occ)) ** 0.5))
    # if no:
    #     total = len(no)
    #     occ = max([no.count(e) for e in set(no)]) / total
    #     disorder += -total * math.log2(1 - ((occ * (1 - occ)) ** 0.5))
    # return disorder / (len(yes) + len(no))
    disorder = 0
    if yes:
        total = len(yes)
        occ = max([yes.count(e) for e in set(yes)]) / total
        if occ != 1:
            disorder += -total * (occ * math.log2(occ) +
                                  (1 - occ) * math.log2(1 - occ))
    if no:
        total = len(no)
        occ = max([no.count(e) for e in set(no)]) / total
        if occ != 1:
            disorder += -total * (occ * math.log2(occ) +
                                  (1 - occ) * math.log2(1 - occ))
    return disorder / (len(yes) + len(no))

# print(CongressIDTree(senate_people, senate_votes, information_disorder))
# evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1,
#          senate_group2, verbose=True)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print("ID tree for first group:")
        print(CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder))
        print()
        print("ID tree for second group:")
        print(CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder))
        print()

    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)


## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 44
rep_classified = limited_house_classifier(house_people, house_votes, N_1)

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 67
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)


# MY_CODE
# Automate the N_x parameter search and discovery
# def classifier_1(N_x: int):
#     return limited_house_classifier(house_people, house_votes, N_x)
# def classifier_2(N_x: int):
#     return limited_house_classifier(senate_people, senate_votes, N_x)
# def classifier_3(N_x: int):
#     return limited_house_classifier(last_senate_people, last_senate_votes, N_x)

# for params in ((classifier_1, 430), (classifier_2, 90), (classifier_3, 95)):
#     classifier = params[0]
#     criteria = params[1]
#     # Assume 1000 is large enough
#     for N_x in range(1, 1000):
#         if classifier(N_x) > criteria:
#             print(N_x)
#             break

# ls = []
# for i in range(1, 100):
#     ls.append(classifier_3(i))
# plt.plot(ls)
# plt.show()

# for params in ((classifier_1, 430), (classifier_2, 90), (classifier_3, 90)):
#     classifier = params[0]
#     criteria = params[1]
#     lower_bound = 1
#     upper_bound = 500
#     lower_bound_val = None
#     upper_bound_val = classifier(upper_bound)
#     while criteria > upper_bound_val:
#         lower_bound = upper_bound
#         lower_bound_val = upper_bound_val
#         upper_bound += 200
#         upper_bound_val = classifier(upper_bound)
#     iteration_ct = 1
#     while abs(upper_bound - lower_bound) > 1:
#         if lower_bound_val is None:
#             lower_bound_val = classifier(lower_bound)
#         if upper_bound_val is None:
#             upper_bound_val = classifier(upper_bound)
#         mid_bound = (lower_bound + upper_bound) // 2
#         mid_bound_val = classifier(mid_bound)
#         if mid_bound_val < criteria:
#             lower_bound = mid_bound
#             lower_bound_val = None
#         else:
#             upper_bound = mid_bound
#             upper_bound_val = None
#         print('    completing iteration {}'.format(iteration_ct))
#         iteration_ct += 1
#     print('Minimum passing N_x: {}'.format(upper_bound))


## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception("Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn)
