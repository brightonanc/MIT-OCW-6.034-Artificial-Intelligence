# MY_CODE
# Some sanity checks to ensure my best-first search implementation in
# CSP.solve_optimal() works

import sys
from csp import CSP, Variable, BinaryConstraint, solve_csp_problem_optimally, \
    basic_constraint_checker, CSPState


def my_csp_problem_1():
    # Defined in notebook

    constraints = []

    variables = []
    variables.append(Variable("1", ['R', 'G', 'B', 'Y']))
    variables.append(Variable("2", ['R', 'G', 'B', 'Y']))
    variables.append(Variable("3", ['R', 'G', 'B', 'Y']))
    variables.append(Variable("4", ['R', 'G', 'B', 'Y']))
    variables.append(Variable("5", ['R', 'G', 'B', 'Y']))

    # these are all variable pairing of adjacent slots
    adjacent_pairs = [("1", "2"), ("1", "5"),
                      ("2", "1"), ("2", "3"), ("2", "5"),
                      ("3", "2"), ("3", "4"), ("3", "5"),
                      ("4", "3"), ("4", "5"),
                      ("5", "1"), ("5", "2"), ("5", "3"), ("5", "4")
                      ]

    # No same neighbor colors
    def base_rule(val_a, val_b, name_a, name_b):
        if val_a == val_b:
            return False
        return True

    for pair in adjacent_pairs:
        constraints.append(BinaryConstraint(pair[0], pair[1], base_rule,
                                            "No same color neighbors"))

    return CSP(constraints, variables)

def prob_1_obj_func_1(state: CSPState):
    cost = 0
    for var_name in ('1', '2', '3', '4', '5'):
        var_val = state.get_variable_by_name(var_name).get_assigned_value()
        if var_val is None:
            cost += 0
        elif var_name == '1' and var_val == 'B':
            cost -= 1
        elif var_name == '2' and var_val == 'Y':
            cost -= 1
        elif var_name == '3' and var_val == 'B':
            cost -= 1
        elif var_name == '4' and var_val == 'G':
            cost -= 1
        elif var_name == '5' and var_val == 'R':
            cost -= 1
        else:
            cost += 1
    return cost

def prob_1_obj_func_2(state: CSPState):
    cost = 0
    # Shouldn't matter to not check for None's; they wouldn't pass the
    # solution criteria anyway
    if state.get_variable_by_name('1').get_assigned_value() == \
            state.get_variable_by_name('3').get_assigned_value():
        cost -= 1
    else:
        cost += 1
    if state.get_variable_by_name('2').get_assigned_value() == 'Y':
        cost -= 1
    else:
        cost += 1
    return cost


def my_csp_problem_2():
    # Defined in notebook

    constraints = []

    variables = []
    colors = ['R', 'O', 'Y', 'G', 'B']
    variables.append(Variable("1", colors.copy()))
    variables.append(Variable("2", colors.copy()))
    variables.append(Variable("3", colors.copy()))
    variables.append(Variable("4", colors.copy()))
    variables.append(Variable("5", colors.copy()))
    variables.append(Variable("6", colors.copy()))
    variables.append(Variable("7", colors.copy()))
    variables.append(Variable("8", colors.copy()))
    variables.append(Variable("9", colors.copy()))
    variables.append(Variable("10", colors.copy()))

    # these are all variable pairing of adjacent slots
    adjacent_pairs = [("1", "2"), ("1", "10"), ("10", "9"), ("10", "1")]

    for i in range(1, 9):
        adjacent_pairs.append((variables[i].get_name(),
                               variables[i-1].get_name()))
        adjacent_pairs.append((variables[i].get_name(),
                               variables[i+1].get_name()))


    # No same neighbor colors
    def base_rule(val_a, val_b, name_a, name_b):
        if val_a == val_b:
            return False
        return True

    for pair in adjacent_pairs:
        constraints.append(BinaryConstraint(pair[0], pair[1], base_rule,
                                            "No same color neighbors"))

    return CSP(constraints, variables)

def prob_2_obj_func_1(state: CSPState):
    sought_use = 2
    bins = len(state.get_all_variables()) // sought_use
    color_dict = {}
    free_ct = 0
    for v in state.get_all_variables():
        color = v.get_assigned_value()
        if color is not None:
            if color in color_dict:
                color_dict[color] += 1
            else:
                color_dict[color] = 1
        else:
            free_ct += 1
    color_bins = list(color_dict.values())
    while len(color_bins) < bins:
        color_bins.append(0)
    while free_ct > 0:
        color_bins.sort()
        color_bins[0] += 1
        free_ct -= 1
        # develops evenly
    return sum([(use - sought_use) ** 2 for use in color_bins])


def prob_2_obj_func_2(state: CSPState):
    sought_use = 1
    bins = len(state.get_all_variables()) // sought_use
    color_dict = {}
    free_ct = 0
    for v in state.get_all_variables():
        color = v.get_assigned_value()
        if color is not None:
            if color in color_dict:
                color_dict[color] += 1
            else:
                color_dict[color] = 1
        else:
            free_ct += 1
    color_bins = list(color_dict.values())
    while len(color_bins) < bins:
        color_bins.append(0)
    while free_ct > 0:
        color_bins.sort()
        color_bins[0] += 1
        free_ct -= 1
        # develops evenly
    return sum([(use - sought_use) ** 2 for use in color_bins])

def prob_2_obj_func_3(state: CSPState):
    sought_use = 1
    num_colors = 5
    bins = len(state.get_all_variables()) // sought_use
    bins = min(bins, num_colors)
    color_dict = {}
    free_ct = 0
    for v in state.get_all_variables():
        color = v.get_assigned_value()
        if color is not None:
            if color in color_dict:
                color_dict[color] += 1
            else:
                color_dict[color] = 1
        else:
            free_ct += 1
    color_bins = list(color_dict.values())
    while len(color_bins) < bins:
        color_bins.append(0)
    while free_ct > 0:
        color_bins.sort()
        color_bins[0] += 1
        free_ct -= 1
        # develops evenly
    return sum([(use - sought_use) ** 2 for use in color_bins])

def prob_2_obj_func_4(state: CSPState):
    sought_use = 3
    num_colors = 5
    bins = len(state.get_all_variables()) // sought_use
    bins = min(bins, num_colors)
    color_dict = {}
    free_ct = 0
    for v in state.get_all_variables():
        color = v.get_assigned_value()
        if color is not None:
            if color in color_dict:
                color_dict[color] += 1
            else:
                color_dict[color] = 1
        else:
            free_ct += 1
    color_bins = list(color_dict.values())
    while len(color_bins) < bins:
        color_bins.append(0)
    while free_ct > 0:
        color_bins.sort()
        color_bins[0] += 1
        free_ct -= 1
        # develops evenly
    return sum([(use - sought_use) ** 2 for use in color_bins])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        checker_type = sys.argv[1]
    else:
        checker_type = "dfs"

    if checker_type == "dfs":
        checker = basic_constraint_checker
    elif checker_type == "fc":
        import lab4

        checker = lab4.forward_checking
    elif checker_type == "fcps":
        import lab4

        checker = lab4.forward_checking_prop_singleton
    else:
        checker = basic_constraint_checker

    # WORKED
    # print('Prob 1, Obj_func_1. Expect BYBGR')
    # solve_csp_problem_optimally(my_csp_problem_1, checker,
    #                             prob_1_obj_func_1, verbose=False)

    # WORKED
    # print('Prob 1, Obj_func_2. Expect XYX?? where X is unknowns')
    # solve_csp_problem_optimally(my_csp_problem_1, checker,
    #                             prob_1_obj_func_2, verbose=False)

    # WORKED
    # print('Prob 2, Obj_func_1. Expect each color to be used twice with '
    #       'cost 0')
    # solve_csp_problem_optimally(my_csp_problem_2, checker,
    #                             prob_2_obj_func_1, verbose=False)

    # VERY SLOW
    # In theory should finish.
    # This was an 'impossible' problem, i.e. the minimum possible cost is not
    # 0. I need to somehow inform the search algorithm that error less than
    # 10, the theoretical minimum, is deceptive.
    # Some quick calculations:
    #   * Branching factor: 5
    #   * Tree depth (num choices): 10
    #   * For the first 5 layers, the algo can be lead to believe that the
    # problem is not 'impossible'
    # print('Prob 2, Obj_func_2. Expect each color to be used twice with '
    #       'cost 10')
    # solve_csp_problem_optimally(my_csp_problem_2, checker,
    #                             prob_2_obj_func_2, verbose=False)

    # FINISHED INSTANTLY. WORKED
    # This is effectively the same algo as directly above (
    # prob_2_obj_func_2), with one small modification: it removes the
    # deception that 0 error is achievable. It uses the knowledge of how
    # many colors are allowed to shrink bins down to its feasible size,
    # the max number of colors.
    # print('Prob 2, Obj_func_3. Expect each color to be used twice with '
    #       'cost 5')
    # solve_csp_problem_optimally(my_csp_problem_2, checker,
    #                             prob_2_obj_func_3, verbose=False)

    print('Prob 2, Obj_func_4. Expect each color to be used thrice-ish with '
          'cost 1')
    solve_csp_problem_optimally(my_csp_problem_2, checker,
                                prob_2_obj_func_4, verbose=False)




