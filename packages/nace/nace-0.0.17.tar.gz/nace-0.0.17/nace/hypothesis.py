"""
 * The MIT License
 *
 * Copyright (c) 2024 Patrick Hammer
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 * """

import random
import sys
from copy import deepcopy

from numba import jit

from nace.prettyprint import Prettyprint_rule


def Hypothesis_UseMovementOpAssumptions(
        leftOp, rightOp, upOp, downOp, dropOp, DisableOpSymmetryAssumptionFlag
):
    """

    Register operations in case Euclidean space operation alignment assumptions should be exploited which helps data
    efficiency

    @param leftOp:
    @param rightOp:
    @param upOp:
    @param downOp:
    @param dropOp:
    @param DisableOpSymmetryAssumptionFlag:
    @return:
    """
    global left, right, up, down, drop, DisableOpSymmetryAssumption
    left, right, up, down, drop, DisableOpSymmetryAssumption = (
        leftOp,
        rightOp,
        upOp,
        downOp,
        dropOp,
        DisableOpSymmetryAssumptionFlag,
    )


@jit(nopython=True)
def Hypothesis_TruthValue(wpn):
    """
    # The truth value of a hypothesis can be obtained directly from the positive and negative evidence counter

    @param wpn:
    @return:
    """
    (wp, wn) = wpn
    frequency = wp / (wp + wn)
    confidence = (wp + wn) / (wp + wn + 1)
    return frequency, confidence


@jit(nopython=True)
def Hypothesis_TruthExpectation(tv):
    """
    # The truth expectation calculation based on the truth value (frequency, confidence) tuple

    @param tv: truth value made up from frequency and confidence
    @return:
    """
    (f, c) = tv
    return c * (f - 0.5) + 0.5


def Hypothesis_Choice(rule_evidence, rule1, rule2):
    """
    # When two hypotheses predict a different outcome for the same conditions, the higher truth exp one is chosen

    @param rule_evidence:
    @param rule1:
    @param rule2:
    @return:
    """
    if rule1 in rule_evidence and rule2 not in rule_evidence:  # dv added (no longer triggered)
        return rule1
    if rule1 not in rule_evidence and rule2 in rule_evidence:  # dv added (no longer triggered)
        return rule2
    if rule1 not in rule_evidence and rule2 not in rule_evidence:  # dv added (no longer triggered)
        # panic
        print("ERROR this suggests a logic error in calling code.")
        return rule2

    t1 = Hypothesis_TruthValue(rule_evidence[rule1])
    t2 = Hypothesis_TruthValue(rule_evidence[rule2])
    if Hypothesis_TruthExpectation(t1) > Hypothesis_TruthExpectation(t2):
        return rule1
    return rule2


def Hypothesis_Contradicted(rule_evidence, ruleset, negruleset, rule):  # this mutates returned copy of rule_evidence
    """
    # Negative evidence was found for the hypothesis/rule

    @param rule_evidence:
    @param ruleset:
    @param negruleset:
    @param rule:
    @return:
    """
    rule_evidence = _AddEvidence(rule_evidence, rule, False)  # mutates returned copy of rule_evidence
    if "silent" not in sys.argv:
        print("Neg. revised: ", end="")
        Prettyprint_rule(rule_evidence, Hypothesis_TruthValue, rule)
        # in a deterministic setting this would have sufficed however
        # simply excluding rules does not work in non-deterministic ones
        # if rule in ruleset:
        #    print("RULE REMOVAL: ", end=""); Prettyprint_rule(rule_evidence, Hypothesis_TruthValue, rule)
        #    ruleset.remove(rule)
        # negruleset.add(rule)
    return rule_evidence, ruleset, negruleset


def Hypothesis_Confirmed(  # this mutates the returned rule_evidence and ruleset
        FocusSet, rule_evidence, ruleset, negruleset, rule
):
    """
    # Positive evidence was found for the hypothesis/rule
    # Confirm rule against +ve and -ve evidence, add variants (i.e. transforms) to newrules

    @param FocusSet:
    @param rule_evidence: dict[rule:(+ve evidence, -ve evidence)]
    @param ruleset:
    @param negruleset:
    @param rule:
    @return:
    """

    rule_evidence = deepcopy(rule_evidence)  # dv added this line
    ruleset = deepcopy(ruleset)  # dv added this line
    # try location symmetry
    variants = _Variants(FocusSet, rule)
    for i, r in enumerate(variants):
        if i > 0:  # abduced hypotheses
            if r in rule_evidence:  # this derived hypothesis already exists
                continue
        rule_evidence = _AddEvidence(rule_evidence, r, True)  # mutates returned copy of rule_evidence
        if "silent" not in sys.argv:
            print("Pos. revised: ", end="")
            Prettyprint_rule(rule_evidence, Hypothesis_TruthValue, r)
        if r not in negruleset:
            if r not in ruleset:
                # print("RULE ADDITION: ", end=""); Prettyprint_rule(rule)
                ruleset.add(r)
    return rule_evidence, ruleset


def Hypothesis_ValidCondition(cond):
    """
    # Valid condition predicate defining the accepted neighbourhood between conclusion and condition cells
    # restrict to neighbours (CA assumption)
    # If 0,1, or 2 in distance in any direction, return True, else False

    @param cond:
    @return:
    """
    (y, x, v) = cond
    if y == 0 and x == 0:  # self
        return True
    if y == 0 and (x == -1 or x == -2):  # left
        return True
    if (y == -1 or y == -2) and x == 0:  # up
        return True
    if y == 0 and (x == 1 or x == 2):  # right
        return True
    if (y == 1 or y == 2) and x == 0:  # down
        return True
    return False


def Hypothesis_BestSelection(rules, rulesExcluded, rule_evidence,
                             stayed_the_same):  # mutates returned rules, rulesExcluded
    """

    We exclude rules which have more negative evidence than positive, and choose the highest truth-exp ones whenever
    a different outcome would be predicted for the same conditions

    @param rules:
    @param rulesExcluded:
    @param rule_evidence:
    @param stayed_the_same: World stayed the same when last ground truth copied in
    @return:
    """
    rulesin = deepcopy(rules)
    for i, rule1 in enumerate(rulesin):
        # if Hypothesis_TruthExpectation(Hypothesis_TruthValue(rule_evidence[rule1])) <= 0.5: #exclude rules which
        # are not better than exp (only 0.5+ makes sense here)
        if rule1 in rule_evidence:  # dv 8/jul/24 added to stop key not found which hadn't happened before
            if Hypothesis_TruthExpectation(
                    Hypothesis_TruthValue(rule_evidence[rule1])
            ) <= 0.5 or (
                    stayed_the_same
                    and random.random()
                    > Hypothesis_TruthExpectation(Hypothesis_TruthValue(rule_evidence[rule1]))
            ):
                if rule1 in rules:
                    rulesExcluded.add(rule1)
                    rules.remove(rule1)
    rulesin = deepcopy(rules)
    for i, rule1 in enumerate(rulesin):
        for j, rule2 in enumerate(rulesin):
            if (
                    i != j
            ):  # exclude rules of same precondition which are worse by truth value
                if rule1[0] == rule2[0]:
                    rulex = Hypothesis_Choice(rule_evidence, rule1, rule2)
                    if rulex == rule1:
                        if rule2 in rules:
                            rulesExcluded.add(rule2)
                            rules.remove(rule2)
                            # print("excluded ", end=''); Prettyprint_rule(rule2)
                    else:
                        if rule1 in rules:
                            rulesExcluded.add(rule1)
                            rules.remove(rule1)
                            # print("excluded", end=''); Prettyprint_rule(rule1)
    return rules, rulesExcluded


def _OpRotate(op):
    """
    # Rotate the operation in Euclidean space if Euclidean op assumptions are allowed to be used

    @param op:
    @return:
    """
    if op == right:
        return down
    if op == down:
        return left
    if op == left:
        return up
    if op == up:
        return right


def _ConditionRotate(cond):
    """
    # Rotate the conditions as well if Euclidean op assumptions are allowed to be utilized

    @param cond:
    @return:
    """
    (y, x, v) = cond
    if y == 0 and x == -1:  # left
        return (-1, 0, v)  # up
    if y == 0 and x == -2:  # left
        return (-2, 0, v)  # up
    if y == -1 and x == 0:  # up
        return (0, 1, v)  # right
    if y == -2 and x == 0:  # up
        return (0, 2, v)  # right
    if y == 0 and x == 1:  # right
        return (1, 0, v)  # down
    if y == 0 and x == 2:  # right
        return (2, 0, v)  # down
    if y == 1 and x == 0:  # down
        return (0, -1, v)  # left
    if y == 2 and x == 0:  # down
        return (0, -2, v)  # left
    if x == 0 and y == 0:
        return (0, 0, v)


def _Variants(
        focus_set, rule
):
    """
    # The rule variants, including hypothetical abduced variations for different directions based on Euclidean space
    rotation and "operation-independence" hypotheses.
    # Exploits Euclidean space properties (knowledge about World_Movement operations for faster learning)

    """

    global left, right, up, down, drop  # DV added

    action_values_precons = rule[0]
    conditions = action_values_precons[2:]
    action = action_values_precons[0]
    max_focus = None
    max_focus_val = False
    if len(focus_set) > 0:
        max_focus = max(focus_set, key=lambda k: focus_set[k])
    if max_focus is not None:
        for x, y, val in action_values_precons[2:]:
            if val == max_focus or rule[1][2] == max_focus:
                max_focus_val = True
    for y, x, v in conditions:
        if (action == left or action == right) and y != 0:
            return []
        if (action == up or action == down or action == drop) and x != 0:
            return []
    rules = [rule]
    action2 = _OpRotate(action)
    action3 = _OpRotate(action2)
    action4 = _OpRotate(action3)
    if DisableOpSymmetryAssumption:
        return rules
    if not max_focus_val:
        rules.append(
            (tuple([left, action_values_precons[1]] + list(conditions)), rule[1])
        )
        rules.append(
            (tuple([right, action_values_precons[1]] + list(conditions)), rule[1])
        )
        rules.append(
            (tuple([up, action_values_precons[1]] + list(conditions)), rule[1])
        )
        rules.append(
            (tuple([down, action_values_precons[1]] + list(conditions)), rule[1])
        )
    if (
            action != left and action != right and action != down and action != up
    ):  # not such an op where symmetry would apply
        return rules
    conditionlist2 = sorted([_ConditionRotate(x) for x in conditions])
    conditionlist3 = sorted([_ConditionRotate(x) for x in conditionlist2])
    conditionlist4 = sorted([_ConditionRotate(x) for x in conditionlist3])
    if max_focus_val:
        rules.append(
            (tuple([action2, action_values_precons[1]] + conditionlist2), rule[1])
        )
        rules.append(
            (tuple([action3, action_values_precons[1]] + conditionlist3), rule[1])
        )
        rules.append(
            (tuple([action4, action_values_precons[1]] + conditionlist4), rule[1])
        )
    return rules


def _AddEvidence(rule_evidence, rule, positive, w_max=20):  # Mutates a copy of rule_evidence
    """
    Add positive or negative evidence for a rule, with a certain max. amount of evidence so that non-stationary
    environments can be handled too

    @param rule_evidence:
    @param rule:
    @param positive:
    @param w_max:
    @return:
    """
    rule_evidence = deepcopy(rule_evidence)
    if rule not in rule_evidence:
        rule_evidence[rule] = (0, 0)
    (wp, wn) = rule_evidence[rule]
    if positive:
        if wp + wn <= w_max:
            rule_evidence[rule] = (wp + 1, wn)
        else:
            rule_evidence[rule] = (wp, max(0, wn - 1))
    else:
        if wp + wn <= w_max:
            rule_evidence[rule] = (wp, wn + 1)
        else:
            rule_evidence[rule] = (max(0, wp - 1), wn)
    return rule_evidence
