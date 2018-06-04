# SEARCH FOR "MY_CODE" COMMENT TO FIND MY CONTRIBUTIONS
from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    # MY_CODE
    if isinstance(hypothesis, AND) or isinstance(hypothesis, OR) or \
            isinstance(hypothesis, NOT):
        return hypothesis.__class__(*[backchain_to_goal_tree(rules, inner)
                                     for inner in hypothesis])
    if isinstance(hypothesis, str):
        goal_tree = OR(hypothesis)
    else:
        raise ValueError('Hypothesis must be a str, AND, OR, or NOT')
    # Hypothesis desormais gauranteed to be str (leaf)
    for rule in rules:
        consequent = rule.consequent()
        for inner in consequent:
            bindings = match(inner, hypothesis)
            if bindings is not None:
                antecedent = rule.antecedent()
                if bindings:
                    antecedent = populate(antecedent, bindings)
                goal_tree += [backchain_to_goal_tree(rules, antecedent)]
    return simplify(goal_tree)



# Here's an example of running the backward chainer - uncomment
# it to see it work:
print(backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin'))
