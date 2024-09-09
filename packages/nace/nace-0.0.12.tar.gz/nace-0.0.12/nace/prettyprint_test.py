from hypothesis import Hypothesis_TruthValue
from prettyprint import Prettyprint_rule
from world_module import right

if __name__ == "__main__":
    rule_evidence = {((right, (0,), (0, 0, 'x'), (0, 1, 'o')), (0, 0, ' ', (-1, 0))): (1, 0)}
    rule = ((right, (0,), (0, 0, 'x'), (0, 1, 'o')), (0, 0, ' ', (-1, 0)))

    Prettyprint_rule(rule_evidence, Hypothesis_TruthValue, rule)
