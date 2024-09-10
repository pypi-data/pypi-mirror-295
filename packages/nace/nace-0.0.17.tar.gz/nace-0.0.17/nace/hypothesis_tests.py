import sys

import world_module
from hypothesis import (Hypothesis_BestSelection, Hypothesis_Confirmed,
                        Hypothesis_UseMovementOpAssumptions)


def t1():
    rules = {((world_module.down, (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0, 0))),
             ((world_module.up, (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0, 0))),
             ((world_module.left, (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))),
             ((world_module.right, (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))),
             ((world_module.right, (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0, 0))),
             ((world_module.left, (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0))),
             ((world_module.down, (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))),
             ((world_module.up, (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0)))}
    rules_excluded = set()
    rule_evidence = {((world_module.right, (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0, 0))): (1, 0),
                     ((world_module.down, (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0, 0))): (1, 0),
                     ((world_module.left, (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))): (1, 0),
                     ((world_module.up, (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))): (1, 0),
                     ((world_module.right, (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))): (1, 0),
                     ((world_module.down, (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))): (1, 0),
                     ((world_module.left, (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0))): (1, 0),
                     ((world_module.up, (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0, 0))): (1, 0)}
    stayed_the_same = False

    new_rules, rules_excluded = Hypothesis_BestSelection(rules, rules_excluded, rule_evidence, stayed_the_same)
    pass


def t2():
    focus_set = {'x': 1}
    negruleset = set()
    rule = ((world_module.left, (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0)))
    rule_evidence = {}
    rule_set = set()

    Hypothesis_Confirmed(focus_set, rule_evidence, rule_set, negruleset, rule)


if __name__ == "__main__":
    # Configure hypotheses to use Euclidean space properties if desired
    Hypothesis_UseMovementOpAssumptions(
        world_module.left,
        world_module.right,
        world_module.up,
        world_module.down,
        world_module.drop,
        "DisableOpSymmetryAssumption" in sys.argv,
    )

    t1()
    t2()
