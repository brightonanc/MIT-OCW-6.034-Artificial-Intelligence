# MY_CODE
# Some sanity checks to ensure my best-first search implementation in
# CSP.solve_optimal() works

import sys
from csp import CSP, Variable, BinaryConstraint, solve_csp_problem_optimally, \
    basic_constraint_checker, CSPState


def my_csp_problem():
    # Defined in notebook

    constraints = []

    # We start with the reduced domain.
    # So the constraint that McCain must sit in seat 1 is already
    # covered.
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
    # def obj_func(state: CSPState):
    #     cost = 0
    #     for var_name in ('1', '2', '3', '4', '5'):
    #         var_val = state.get_variable_by_name(var_name).get_assigned_value()
    #         if var_val is None:
    #             cost += 0
    #         elif var_name == '1' and var_val == 'B':
    #             cost -= 1
    #         elif var_name == '2' and var_val == 'Y':
    #             cost -= 1
    #         elif var_name == '3' and var_val == 'B':
    #             cost -= 1
    #         elif var_name == '4' and var_val == 'G':
    #             cost -= 1
    #         elif var_name == '5' and var_val == 'R':
    #             cost -= 1
    #         else:
    #             cost += 1
    #     return cost

    def obj_func(state: CSPState):
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

    solve_csp_problem_optimally(my_csp_problem, checker, obj_func,
                                verbose=True)