import collections
import copy
import random
from collections import deque
from typing import Type

import nace.color_codes
import nace.world_module
from nace.agent_module import Agent
# from nace.hypothesis import *
from nace.hypothesis import Hypothesis_BestSelection, Hypothesis_ValidCondition, Hypothesis_Confirmed, Hypothesis_Contradicted
from nace.prettyprint import Prettyprint_Plan
from nace.world_module_numpy import NPWorld


# See nace.py for type and data structure descriptions


def _plan(world: Type[NPWorld], rules, actions, focus_set,
          agent: Type[Agent], max_num_actions: int = 100,
          max_queue_len: int = 2000, custom_goal=None,
          continue_planning_threshold=0.99):
    """
    Plan forward searching for situations of highest reward or lowest AIRIS confidence or oldest age.

    Returns:
    - lowest_conf_actions: List of actions leading to the lowest AIRIS confidence
    - lowest_AIRIS_confidence: The lowest AIRIS confidence score (highest reward for exploring)
    - oldest_age_actions: Actions leading to the oldest world state
    - oldest_age: Age of the oldest world state encountered
    """
    queue = deque([(world, agent.get_values_inc_score(), [], 0, "na 1")])  # (world_state, actions, depth, debug_data)
    encountered = {}  # used to short-circuit search
    evaluation_count = 0

    lowest_conf_actions = []
    lowest_AIRIS_confidence = float("inf")  # smaller is better
    lowest_conf_predicted_score_delta = 0.0
    lowest_conf_stopping_reason = "na 2"

    oldest_age_actions = []
    oldest_age = 0  # if we see an age (time difference) greater than this, we store it.
    oldest_age_predicted_score_delta = 0.0
    oldest_age_stopping_reason = "na 3"

    dead_plans = []

    if agent.get_score() >= 1:
        pass

    while queue and len(queue) <= max_queue_len:  # queue size = number of actions * roll out length
        (current_world, current_agent_values, planned_actions, depth, stopping_reason) = queue.popleft()

        # need to store agent values on the queue as well, and add the values delta to them.

        if depth > max_num_actions:
            print(f"Max depth of {max_num_actions} reached, stopping search.")
            stopping_reason = "Max depth"
            dead_plans.append((planned_actions, stopping_reason))
            continue

        world_state = tuple([current_world.get_board_hashcode()] + current_agent_values[1:])

        if _should_skip_state(world_state, encountered, depth):
            # skip states already evaluated (optimisation)
            # print(f"Skipping state")
            stopping_reason = "Skipping state"
            dead_plans.append((planned_actions, stopping_reason))
            continue

        # store that we have been here, in order to prune the search space and avoid loops
        encountered[world_state] = depth

        for action in actions:  # check each action in turn from a known state
            new_world, new_AIRIS_confidence, new_age, agent_values_delta, predicted_score_delta = (
                _predict_next_world_state(
                    focus_set, current_world, action, rules, agent, custom_goal
                ))
            if agent_values_delta[0] != 0:
                pass  # code to place breakpoint on
            # if predicted_score_delta > 0.0:
            #     print("goal found") # code to place breakpoint on

            if (new_world.get_board_hashcode() == current_world.get_board_hashcode()):  # no effect (e.g. hit a wall )
                stopping_reason = "action triggered no change"
                dead_plans.append((planned_actions + [action], stopping_reason))
                continue  # no need to continue evaluating (optimisation)

            if (new_AIRIS_confidence == float("inf")):  # something bad happens, avoid.
                stopping_reason = "something bad happens (-ve score)"
                dead_plans.append((planned_actions + [action], stopping_reason))
                continue  # no need to continue evaluating (optimisation)

            new_planned_actions = planned_actions + [action]

            if _is_lower_airis_confidence(new_AIRIS_confidence, lowest_AIRIS_confidence, new_planned_actions,
                                          lowest_conf_actions):  # lower or equal confidence and fewer actions
                lowest_conf_actions = new_planned_actions
                lowest_AIRIS_confidence = new_AIRIS_confidence
                lowest_conf_predicted_score_delta = predicted_score_delta
                lowest_conf_stopping_reason = stopping_reason

            if _is_older_age(new_age, oldest_age, new_planned_actions, oldest_age_actions):
                oldest_age_actions = new_planned_actions
                oldest_age = new_age
                oldest_age_predicted_score_delta = predicted_score_delta
                oldest_age_stopping_reason = stopping_reason

            if new_AIRIS_confidence >= continue_planning_threshold:
                # calc value deltas together
                agent_values = list(copy.deepcopy(current_agent_values))
                for i, v in enumerate(agent_values_delta):
                    if i < len(agent_values):
                        agent_values[i] += v
                # add this to the queue to have extra steps added (confidence of 1 means certain, so keep planning)
                queue.append((new_world, agent_values, new_planned_actions, depth + 1, stopping_reason))
            else:
                # do not add this result to the queue, so it stops being explored further
                stopping_reason = "AIRIS confidence dropped below 1.0"
                dead_plans.append((planned_actions + [action], stopping_reason))

            evaluation_count += 1

            if new_AIRIS_confidence == float("-inf") and predicted_score_delta <= 0.0:
                print("logic error")
            if new_AIRIS_confidence > float("-inf") and predicted_score_delta > 0.0:
                print("logic error")

            if predicted_score_delta > 0.0:  # new_AIRIS_confidence == float("-inf"):
                # goal found?
                assert new_AIRIS_confidence == lowest_AIRIS_confidence
                assert predicted_score_delta > 0.0  # can we 'correct' the 'if' above to use score?
                assert lowest_conf_predicted_score_delta > 0.0 or oldest_age_predicted_score_delta > 0.0
                return (lowest_conf_actions,
                        lowest_AIRIS_confidence,
                        lowest_conf_predicted_score_delta,
                        lowest_conf_stopping_reason,
                        oldest_age_actions,
                        oldest_age,
                        oldest_age_predicted_score_delta,
                        oldest_age_stopping_reason)

    return (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_predicted_score_delta, lowest_conf_stopping_reason,
            oldest_age_actions, oldest_age, oldest_age_predicted_score_delta, oldest_age_stopping_reason)


def _should_skip_state(world_state, encountered, depth):
    return world_state in encountered and depth >= encountered[world_state]


def _is_lower_airis_confidence(new_score, best_score, new_actions, best_actions):
    return (new_score < best_score or
            (new_score == best_score and len(new_actions) < len(best_actions)))


def _is_older_age(new_age, oldest_age, new_actions, best_actions):
    """
    Ages are the difference in the time counter. 1 is 1 time ago. -inf is the start of time.
    @param new_age:
    @param oldest_age:
    @param new_actions:
    @param best_actions:
    @return:
    """
    return (new_age > oldest_age or
            (new_age == oldest_age and len(new_actions) < len(best_actions)))


def _print_score(score):
    """
    Print score value taking its semantics regarding its value range semantics for planning into account

    @param score:
    @return:
    """
    if 0.0 <= score <= 1.0:
        print("certainty:", score)
    else:
        print("desired: True")


def nacev3_get_next_action(
        time_counter,
        focus_set,
        rule_evidence,
        xy_loc,
        internal_world_model: Type[NPWorld],
        rules_in,
        external_ground_truth_world_model: Type[NPWorld],
        print_debug_info,
        stayed_the_same: bool,
        agent: Type[Agent],
        available_actions: list  # used during babling
):
    """
    Determine the next action for the NACE agent based on current observations and rules.

    Steps:
    1. Limit the agent's field of view (partial observability)
    2. Refine rules based on evidence
    3. Plan forward to calculate favored actions and scores

    :param time_counter: Current time
    :param focus_set: Used in subroutine
    :param rule_evidence: Evidence for rules
    :param xy_loc: Tuple(x, y) of agent's location (0,0 is top left)
    :param internal_world_model: Agent's view of the world (mutated)
    :param rules_in: Input rules
    :param external_ground_truth_world_model: Current world state (mutated)
    :param  print_debug_info,
    :param stayed_the_same: bool,
    :param agent,
    :return: Tuple(plan, action, rules_excluded, behavior)


    Notes
        The number of state values that the agent stores, and the number of value delta in the rules must match.
    """
    rules_excluded = set()
    rules = copy.deepcopy(rules_in)

    # Step 1: Update agent's field of view
    # world_module.World_FieldOfView(time_counter, xy_loc, internal_world_model, external_ground_truth_world_model)
    if external_ground_truth_world_model is not None:
        modified_count, _ = internal_world_model.update_world_from_ground_truth(
            time_counter,
            external_ground_truth_world_model, xy_locations=[xy_loc])
        if print_debug_info:
            internal_world_model.multiworld_print([{"Caption": f"Internal:",
                                                    "World": internal_world_model,
                                                    "Color": nace.color_codes.color_code_white_on_black},
                                                   ]
                                                  )

    # Step 2: Refine rules based on evidence
    rules, rules_excluded = Hypothesis_BestSelection(
        rules,
        rules_excluded,
        rule_evidence,
        stayed_the_same)
    if agent.get_score() >= 1.0:
        pass

    # Step 3: Plan forward
    (lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_predicted_score_delta, lowest_conf_stopping_reason,
     oldest_age_actions, oldest_age, oldest_age_predicted_score_delta, oldest_age_stopping_reason) = (
        _plan(
            internal_world_model,
            rules,
            nace.world_module.get_full_action_list(),
            focus_set,
            agent=agent,
            custom_goal=nace.world_module.World_GetObjective()
        ))

    # Determine available actions
    remaining_actions = _get_remaining_actions(rules)
    all_actions_tried = len(remaining_actions) == 0

    # Determine behavior and action
    behavior, action, plan = _determine_behavior_and_action(
        lowest_AIRIS_confidence, lowest_conf_actions, lowest_conf_predicted_score_delta, lowest_conf_stopping_reason,
        oldest_age_actions, oldest_age, oldest_age_predicted_score_delta, oldest_age_stopping_reason,
        all_actions_tried,
        available_actions=available_actions,
        print_debug_info=print_debug_info
    )

    return plan, action, rules_excluded, behavior


def _get_remaining_actions(rules):
    action_list = nace.world_module.get_full_action_list()
    for rule in rules:
        precondition, _ = rule
        action = precondition[0]
        if action in action_list:
            action_list.remove(action)
    return action_list


# def _determine_behavior_and_action_old(airis_score, favored_actions, favored_actions_for_revisit, oldest_age,
#                                        all_actions_tried: bool, board_value_transition: tuple,
#                                        print_debug_info: bool = False):
#     """
#
#     Indeterministic if all_actions_tried == FALSE
#
#     @param airis_score:
#     @param favored_actions:
#     @param favored_actions_for_revisit:
#     @param oldest_age: oldest observed age (smaller == older)
#     @param all_actions_tried: True if all possible actions were in the set of applicable rules
#     @param babbling_rates: dict of rates e.g. : {'curiosity': 0.5, 'exploit': 1.0, 'explore': 0.5}
#     @param board_value_transition: tuple ( char, char) from to values of a board transition.
#     @param print_debug_info:
#     @return:
#     """
#
#     if all_actions_tried or airis_score == float("-inf"):
#         exploit_babble = False
#     else:
#         exploit_babble = random.random() > 0.5
#
#     if all_actions_tried:  # if all_actions_tried evaluates to False, else False 50% of time
#         explore_babble = False
#     else:
#         explore_babble = random.random() > 0.5
#
#     if airis_score >= 0.9 or exploit_babble or len(favored_actions) == 0:
#         # EXPLORE or BABBLE
#         if (not exploit_babble and not explore_babble and oldest_age > 0.0 and
#                 airis_score == 1.0 and
#                 len(favored_actions_for_revisit) != 0):
#             behavior = "EXPLORE"
#             print(behavior, Prettyprint_Plan(favored_actions_for_revisit), "oldest_age:", oldest_age)
#             action = favored_actions_for_revisit[0]
#             plan = favored_actions_for_revisit
#         else:
#             behavior = "BABBLE"
#             action = _choose_babble_action(available_actions=world_module.get_full_action_list())
#             plan = []
#     else:  # airis_score must be < 0.9
#         # ACHIEVE or CURIOUS
#         behavior = "ACHIEVE" if airis_score == float("-inf") else "CURIOUS"
#         print(behavior, Prettyprint_Plan(favored_actions), end=" ")
#         _print_score(airis_score)
#         action = favored_actions[0]
#         plan = favored_actions
#
#     if print_debug_info:
#         print("behavior", behavior,
#               "airis_score", airis_score,
#               "favored_actions", favored_actions,
#               "favored_actions_for_revisit", favored_actions_for_revisit, "oldest_age>0", (oldest_age > 0.0),
#               "board_value_transition", board_value_transition)
#
#     return behavior, action, plan
#

def _determine_behavior_and_action(lowest_AIRIS_conf,
                                   lowest_AIRIS_conf_actions,
                                   lowest_conf_predicted_score_delta:float,
                                   lowest_AIRIS_conf_stopping_reason: str,
                                   oldest_actions,
                                   oldest_age,
                                   oldest_age_predicted_score_delta:float,
                                   oldest_age_stopping_reason: str,
                                   all_actions_tried: bool,
                                   available_actions: list,
                                   print_debug_info: bool = False):
    """

    Nondeterministic if all_actions_tried == FALSE

    @param lowest_AIRIS_conf:
    @param lowest_AIRIS_conf_actions:
    @param oldest_actions:
    @param oldest_age: oldest observed age (smaller == older)
    @param all_actions_tried: True if all possible actions were in the set of applicable rules
    @param babbling_rates: dict of rates e.g. : {'curiosity': 0.5, 'exploit': 1.0, 'explore': 0.5}
    @param print_debug_info:
    @return:
    """

    # Calculate babbling rates, some are 0.5 if not all actions tried
    explore_curiosity_modulator = 1.0 if all_actions_tried else 0.5
    babbling_rates = {
        'curiosity': explore_curiosity_modulator,
        'exploit': 1.0,
        'explore': explore_curiosity_modulator
    }

    if lowest_AIRIS_conf == float("-inf"):
        exploit_babble = random.random() > babbling_rates['exploit']  # must always evaluate to false

    else:
        if all_actions_tried:
            exploit_babble = False
        else:
            exploit_babble = random.random() > 0.5

    if all_actions_tried:
        explore_babble = False
    else:
        # if all_actions_tried evaluates to False, else False 50% of time
        explore_babble = random.random() > 0.5

    code_path = "?"

    if lowest_conf_predicted_score_delta > 0.0:
        behavior = "ACHIEVE"
        action = lowest_AIRIS_conf_actions[0]
        plan = lowest_AIRIS_conf_actions
        code_path = "Score via Lowest AIRIS conf."
    elif oldest_age_predicted_score_delta > 0.0:
        behavior = "ACHIEVE"
        action = oldest_actions[0]
        plan = oldest_actions
        code_path = "Score via oldest age"
    else:
        if (lowest_AIRIS_conf >= 0.99 # we think we model the world fully
                or exploit_babble or len(lowest_AIRIS_conf_actions) == 0):
            # EXPLORE or BABBLE
            if (not exploit_babble and not explore_babble and oldest_age > 0.0 and
                    lowest_AIRIS_conf == 1.0 and
                    len(oldest_actions) != 0):
                behavior = "EXPLORE"
                code_path = "OLDEST_CELLS"
                action = oldest_actions[0]
                plan = oldest_actions
            else:
                behavior = "BABBLE"
                action = _choose_babble_action(available_actions=available_actions)
                code_path = "RANDOM_ACTION"
                plan = []
        else:  # lowest_AIRIS_conf must be < 0.99
            # ACHIEVE or CURIOUS
            # the oscillation path on world 2 runs through here always selecting lowest_AIRIS_conf_actions
            behavior = "ACHIEVE" if lowest_AIRIS_conf == float("-inf") else "CURIOUS"
            action = lowest_AIRIS_conf_actions[0]
            plan = lowest_AIRIS_conf_actions
            code_path = "Lowest AIRIS conf."




    if print_debug_info:
        print("behavior", behavior,
              "airis_score", lowest_AIRIS_conf,
              "favored_actions", lowest_AIRIS_conf_actions,
              "favored_actions_for_revisit", oldest_actions, "oldest_age>0", (oldest_age > 0.0),
              )

    print(behavior, nace.prettyprint.Prettyprint_AllActions(plan), "oldest_age:", oldest_age, "AIRIS Conf.:", lowest_AIRIS_conf, "Path:",code_path,
          "Lowest age reason:", lowest_AIRIS_conf_stopping_reason, "oldest_age_stopping_reason",
          oldest_age_stopping_reason)
    return behavior, action, plan


def _choose_babble_action(available_actions):
    if nace.world_module.drop in available_actions:
        available_actions += [nace.world_module.drop, nace.world_module.drop]
    return random.choice(available_actions)


def _create_explanation_graphs():
    """
    Hold some things constant, then produce graphs to try an explain how airis score based on synthetic inputs
    e.g.: all_actions_tried, age etc relate to each other
    @return:
    """
    # Calculate babbling rates
    all_results = {}
    num_repeats = 100
    number_airis_bins = 20
    description = ""

    for oldest_age in [10]:
        for all_actions_tried in [True, False]:
            results = []
            for i in range(number_airis_bins + 1):
                airis_score = i / float(number_airis_bins)
                action_type_counts = collections.defaultdict(int)
                behavior_counts = collections.defaultdict(int)

                for run in range(num_repeats):
                    # Determine behavior and action
                    behavior, action, plan = _determine_behavior_and_action(
                        airis_score,
                        lowest_AIRIS_conf_actions=["FA[0]", "FA[1]"],
                        oldest_actions=["FAFR[0]", "FAFR[1]"],
                        oldest_age=oldest_age,
                        available_actions=["FA[0]", "FA[1]", "FAFR[0]", "FAFR[1]"],
                        all_actions_tried=all_actions_tried,
                    )
                    behavior_counts[behavior] += 1
                    if action.find("FAFR[") > -1:
                        action_type_counts["favored_actions_for_revisit"] += 1
                    elif action.find("FA[") > -1:
                        action_type_counts["favored_actions"] += 1

                description = "oldest_age:" + str(oldest_age) + " all_actions_tried:" + str(all_actions_tried)
                results.append({"airis_score": airis_score,
                                "CURIOUS": behavior_counts["CURIOUS"],
                                "ACHIEVE": behavior_counts["ACHIEVE"],
                                "BABBLE": behavior_counts["BABBLE"],
                                "EXPLORE": behavior_counts["EXPLORE"],
                                "favored_actions_for_revisit": action_type_counts["favored_actions_for_revisit"],
                                "favored_actions": action_type_counts["favored_actions"],
                                "description": description,
                                'all_actions_tried': all_actions_tried,
                                'oldest_age': oldest_age
                                })
            print("________________ results:")
            print(results)
            all_results[description] = results
    print("________________ all results:")
    print(all_results)
    # return plan, action, rules_excluded, behavior


def _match_hypotheses(focus_set, oldworld, action, rules, old_agent: Type[Agent]):
    """
    Match hypotheses (rules) preconditions to the world, calculating how AIRIS-confident the prediction would be:
    ( called _MatchHypotheses in old system)

    @param focus_set:
    @param oldworld:
    @param action:
    @param rules:
    @return:
    """
    positionscores = dict([])
    highesthighscore = 0.0
    AttendPositions = set([])

    height, width = oldworld.get_height_width()
    for y in range(height):
        for x in range(width):
            if oldworld.get_char_at(y, x) in focus_set:
                # if oldworld[world_module.BOARD][y][x] in focus_set:
                AttendPositions.add((y, x))
                for rule in rules:
                    (precondition, consequence) = rule
                    action_score_and_preconditions = list(precondition)
                    for y_rel, x_rel, requiredstate in action_score_and_preconditions[
                                                       2:
                                                       ]:
                        AttendPositions.add((y + y_rel, x + x_rel))
    for y in range(height):
        for x in range(width):
            if (y, x) not in AttendPositions:
                continue
            scores = dict([])
            positionscores[(y, x)] = scores
            highscore = 0.0
            highscorerule = None
            for rule in rules:
                (precondition, consequence) = rule
                action_score_and_preconditions = list(precondition)
                values = action_score_and_preconditions[1]
                if action_score_and_preconditions[0] == action:
                    scores[rule] = 0.0
                else:
                    continue
                CONTINUE = False
                for i in range(len(values)):
                    if values[i] != old_agent.get_values_exc_score()[
                        i]:  # hmm should be doable? # 15th Aug, changed to be inclusive of score.
                        # 30 aug changed to be exlusive of score
                        CONTINUE = True
                if CONTINUE:
                    continue
                for y_rel, x_rel, requiredstate in action_score_and_preconditions[2:]:
                    if (
                            y + y_rel >= height
                            or y + y_rel < 0
                            or x + x_rel >= width
                            or x + x_rel < 0
                    ):
                        CONTINUE = True
                        break
                    if oldworld.get_char_at(y + y_rel, x + x_rel) == requiredstate:
                        scores[rule] += 1.0  # n matched_conds
                if CONTINUE:
                    continue
                scores[rule] /= len(precondition) - 2  # Q(r,c) - Match Quotient
                if scores[rule] > 0.0 and (
                        scores[rule] > highscore
                        or (
                                scores[rule] == highscore
                                and highscorerule is not None
                                and len(rule[0]) > len(highscorerule[0])
                        )
                ):
                    highscore = scores.get(rule, 0.0)
                    highscorerule = rule
            positionscores[(y, x)] = (scores, highscore, highscorerule)
            if highscore > highesthighscore:
                highesthighscore = highscore
    return (positionscores, highesthighscore)


def _rule_applicable(scores, highscore, highesthighscore, rule):  # called _RuleApplicable in old system
    """
    # Whether a rule is applicable: only if it matches better than not at all, and as well as the best matching rule

    @param scores:
    @param highscore:
    @param highesthighscore:
    @param rule:
    @return:
    """
    if highscore > 0.0 and scores.get(rule, 0.0) == highesthighscore:
        return True
    return False


def _predict_next_world_state(focus_set, oldworld, action, rules,
                              agent,
                              customGoal=None):  # called NACE_Predict in old system
    """
    Returns the world as predicted after 'action' is applied to 'oldWorld'.
    It does this by applying rules that have been previously learnt.

    How: Apply the move to the predicted world model whereby we use the learned rules to decide how grid elements might
    most likely change.

    :param focus_set: - Note: NOT updated by this routine.
    :param oldworld:
    :param action:
    :param rules:
    :param customGoal:
    :return:
    """
    newworld = copy.deepcopy(oldworld)
    newagent = copy.deepcopy(agent)
    used_rules_sumscore = 0.0
    used_rules_amount = 0
    score_delta = 0.0
    # score : the AIRIS confidence of the prediction
    (positionscores, highesthighscore) = _match_hypotheses(
        focus_set, oldworld, action, rules, agent
    )
    max_focus = None
    if len(focus_set) > 0:
        max_focus = max(focus_set, key=lambda k: focus_set[k])
    age = 0
    height, width = oldworld.get_height_width()
    for y in range(height):
        for x in range(width):
            if (y, x) not in positionscores:
                continue
            scores, highscore, rule = positionscores[(y, x)]
            # for rule in rules:
            if _rule_applicable(scores, highscore, highesthighscore, rule):
                # newworld[world_module.VALUES] = rule[1][3]    # values including score?
                newagent.set_values_inc_score(rule[1][3])  # new agent score should be considered delta
                newworld.set_char_at(y, x, rule[1][2])
                used_rules_sumscore += scores.get(rule, 0.0)
                used_rules_amount += 1
    current_time = newworld.get_newest_time()
    for y in range(height):
        for x in range(width):
            if (y, x) not in positionscores:
                continue
            if (
                    max_focus
                    and newworld.get_char_at(y, x) in focus_set
                    and newworld.get_char_at(y, x) == max_focus
            ):
                age = max(age, (current_time - newworld.get_time_at(y, x)))
    AIRIS_confidence = (
        used_rules_sumscore / used_rules_amount if used_rules_amount > 0 else 1.0
    )  # AIRIS confidence
    if AIRIS_confidence < 1.0:
        pass  # noop for breakpoint placement

    # but if the certainty predicted world has higher value, then set prediction score to the best it can be
    if (newagent.get_score() > 0.0 and AIRIS_confidence == 1.0):  # newagent score should be considered as a delta here
        AIRIS_confidence = float("-inf")  # set this to be where we would explore
        score_delta = newagent.get_score()

    # while if the certainty predicted world has lower value, set prediction score to the worst it can be
    if (newagent.get_score() < 0.0 and AIRIS_confidence == 1.0):
        AIRIS_confidence = float("inf")  # i.e. Flag to tell calling code avoid! avoid! # needs to be re-worked
        score_delta = newagent.get_score()  # newagent score should be considered as a delta here

    if (customGoal and customGoal(newworld)):
        AIRIS_confidence = float("-inf")  # set this to be where we would explore
        score_delta = 1.0
        newagent.set_score(score_delta)  # newagent score should be considered as a delta here

    # l = max(len(agent.get_values_inc_score()), len(newagent.get_values_inc_score()))
    # value_deltas = [0] * l
    # for i in range(l):
    #     value_deltas[i] = newagent.get_values_inc_score()[i] - agent.get_values_inc_score()[i]

    return (newworld,
            AIRIS_confidence,
            age,
            newagent.get_values_inc_score(),  # delta of all values including score
            score_delta)


def _add_to_adjacent_set(adjacent_change_sets: list, newEntry: tuple, MaxCapacity: int, CanCreateNewSet: bool,
                         maximum_distance: int = 1):  # called _AddToAdjacentSet in the old system
    """


    If there are no entries in the adjacent_change_sets create a new one with the new point.
    If the new point if not adjacent to any of the existing sets create a new set containing it.
    If the new point is adjacent to a point in the existing sets, add it to that set if
              there are less than 3 points in it.

    @param adjacent_change_sets:
    @param newEntry:
    @param MaxCapacity:
    @param CanCreateNewSet:
    @param maximum_distance:
    @return:
    """
    (y, x) = newEntry
    AdjacentToAnySet = False
    for consideredSet in adjacent_change_sets:
        consideredSetFrozen = copy.deepcopy(consideredSet)
        for ys, xs in consideredSetFrozen:
            if abs(y - ys) + abs(x - xs) <= maximum_distance:
                if len(consideredSet) < MaxCapacity:
                    consideredSet.add(newEntry)
                AdjacentToAnySet = True
    if not AdjacentToAnySet and CanCreateNewSet:
        adjacent_change_sets.append({newEntry})


def _is_presently_observed(Time, world, y, x):
    """
    # Whether the grid cell has been observed now (not all have been, due to partial observability)

    @param Time:
    @param world:
    @param y:
    @param x:
    @return:
    """
    diff = Time - world.times[y][x]
    return diff == 0  # TODO this logic should be in world object


def _build_change_sets(
        focus_set,
        oldworld,
        action,
        newworld,
        predictedworld,
        unobserved_code,
        object_count_threshold=1
):
    """
    calc value_counts : counts each board value has been seen

    @param focus_set:
    @param oldworld:
    @param action:
    @param newworld:
    @param predictedworld:
    @param object_count_threshold:
    @return:
    """
    # Keep track of cell type counts - count of each cell type
    # in world keyed by the chars in the world map
    value_counts = dict([])
    height, width = oldworld.get_height_width()
    for y in range(height):
        for x in range(width):
            val = oldworld.get_char_at(y, x)
            if val not in value_counts:
                value_counts[val] = 1
            else:
                value_counts[val] += 1
    # Update focus_set based on unique values and unique changing values.
    # focus_set : keyed by the char in a map location.
    #         Value == the number of time steps this value has been one that has changed (and there was only 1 of them)
    # if the world is huge, is this realistic, or work out from current location till N are found ...
    #
    pass
    # only consider cells that were observed in both newworld and oldworld in the most recent upadate of each,
    # if there is only 1 cell of this type (why?) add this, or increment this in the focus set.
    # Optimisation : Code could be changed to pull this set of locations from the worlds utilizing fast np operations.
    current_time = newworld.get_newest_time()
    for y in range(height):
        for x in range(width):
            # skip unobserved cells
            if not _is_presently_observed(
                    current_time, newworld, y, x
            ) and not _is_presently_observed(current_time - 1, newworld, y, x):
                continue
            val = oldworld.get_char_at(y, x)  # value in the map
            if val == "O":
                pass
            # if val in value_counts.keys() and val not in focus_set:  # if 'val' is new, init focus set
            #     focus_set[val] = 0
            # if oldworld.get_char_at(y, x) != newworld.get_char_at(y, x):  # this cell changed away from value 'val'
            #     # used to check for uniquiness - was this just an oversight? - why check for uniqueness? this makes no sense. # dv-5/Aug # Patrick Why
            #     if val not in focus_set:
            #         focus_set[val] = 1
            #     else:
            #         focus_set[val] += 1  # == the number of times this cell type has been seen to change
            #
            #
            # if 1 <= value_counts[
            #     val] <= object_count_threshold and val not in focus_set:  # if this map type is unique and not in focus set # Patrick Why
            #     focus_set[val] = 0
            if value_counts[val] == 1 and val not in focus_set:  # if 'val' is new, init focus set
                focus_set[val] = 0
            if oldworld.get_char_at(y, x) != newworld.get_char_at(y, x):  # only when it comes into view first time
                if 1 <= value_counts[val] <= object_count_threshold:  # unique - why check for uniqueness?
                    # this makes no sense. # dv-5/Aug # Patrick said implementation detail, it meant that it would only
                    # trigger if there was 1 new value within visible window
                    focus_set[val] += 1  # can happen when already set to 0, or over multiple time steps.
                    # because we may focus over multiple time frames?

    # create adjacent change sets
    adjacent_change_sets = []
    for y in range(height):
        for x in range(width):
            # skip cells not observed in either this, or the last times step.
            if _is_presently_observed(
                    current_time, newworld, y, x
            ) and _is_presently_observed(current_time - 1, newworld, y, x):
                if (  # if different and not observed code
                        oldworld.get_char_at(y, x) != newworld.get_char_at(y, x)
                        and oldworld.get_char_at(y, x) != unobserved_code
                ):
                    # moving into the cliff or off the edge of the board makes no change, so this code does not detect it.
                    if oldworld.get_char_at(y,
                                            x) == 'C':
                        pass  # debugging breakpoint
                    # mutate changesets adding values to it.
                    _add_to_adjacent_set(
                        adjacent_change_sets, (y, x), MaxCapacity=3, CanCreateNewSet=True, maximum_distance=1
                        # MaxCapacity=3 as 3 things need to have changed for more complex rules to be induced.
                        # TODO 3 and 1 are magic numbers.
                    )
    changesetslen = len(adjacent_change_sets)  # the length of change set only
    changeset0len = 0  # length of changeset 0 (the first changeset) Possibly this should be the max changeset length?
    if changesetslen > 0:
        changeset0len = len(
            adjacent_change_sets[0]
        )  # temporary fix: 3 things need to have changed at least to allow for the more complex rules to be induced
    # Add prediction mismatch entries to adjacent change set entry (using newworld for observation times)
    pass
    for y in range(height):
        for x in range(width):
            # skip unobserved cells
            if not _is_presently_observed(
                    current_time, newworld, y, x
            ) and not _is_presently_observed(current_time - 1, newworld, y, x):
                continue
            if (
                    predictedworld
                    and predictedworld.get_char_at(y, x) != newworld.get_char_at(y, x)
                    and oldworld.get_char_at(y, x) != unobserved_code
            ):
                _add_to_adjacent_set(
                    adjacent_change_sets, (y, x), MaxCapacity=2, CanCreateNewSet=True, maximum_distance=1
                    # MaxCapacity is one less than it was. hmmm...
                )
    # if there was a change next to a focus set element (spatial dependency) add it to the changeSet
    chgsets = copy.deepcopy(adjacent_change_sets)
    for changeset in chgsets:
        for y, x in changeset:
            if (
                    (action == nace.world_module.left or action == nace.world_module.right)
                    and x > 0  # assumes there will be a wall round the board
                    and newworld.get_char_at(y, x - 1) in focus_set
                    and oldworld.get_char_at(y, x - 1) != unobserved_code
            ):
                _add_to_adjacent_set(
                    adjacent_change_sets, (y, x - 1), MaxCapacity=3, CanCreateNewSet=False, maximum_distance=1
                )
            if (
                    (action == nace.world_module.left or action == nace.world_module.right)
                    and x < width - 1  # assumes there will be a wall round the board
                    and newworld.get_char_at(y, x + 1) in focus_set
                    and oldworld.get_char_at(y, x + 1) != unobserved_code
            ):
                _add_to_adjacent_set(
                    adjacent_change_sets, (y, x + 1), MaxCapacity=3, CanCreateNewSet=False, maximum_distance=1
                )
            if (
                    (action == nace.world_module.up or action == nace.world_module.down or action == nace.world_module.drop)
                    and y > 0  # assumes there will be a wall round the board
                    and newworld.get_char_at(y - 1, x) in focus_set
                    and oldworld.get_char_at(y - 1, x) != unobserved_code
            ):
                _add_to_adjacent_set(
                    adjacent_change_sets, (y - 1, x), MaxCapacity=3, CanCreateNewSet=False, maximum_distance=1
                )
            if (
                    (action == nace.world_module.up or action == nace.world_module.down)
                    and y < height - 1  # assumes there will be a wall round the board
                    and newworld.get_char_at(y + 1, x) in focus_set
                    and oldworld.get_char_at(y + 1, x) != unobserved_code
            ):
                _add_to_adjacent_set(
                    adjacent_change_sets, (y + 1, x), MaxCapacity=3, CanCreateNewSet=False, maximum_distance=1
                )
    # Change sets are now built ready to be used.
    print("Adjacent change sets have been built:", adjacent_change_sets)
    return focus_set, adjacent_change_sets, changeset0len


def _observe(
        focus_set,
        rule_evidence,
        oldworld,
        action,
        newworld,
        oldrules,
        oldnegrules,
        predictedworld,
        pre_action_agent,
        ground_truth_post_action_agent,
        unobserved_code,
        object_count_threshold,
):
    """
    Extract new rules from the observations by looking only for observed changes and prediction-observation mismatches

    @param focus_set: Set of focus points
    @param rule_evidence:  dict[rule:(+ve evidence, -ve evidence)]
    @param oldworld: State of the world before the action
    @param action: Action taken
    @param newworld: State of the world after the action
    @param oldrules: Existing rules
    @param oldnegrules: Existing negative rules
    @param predictedworld: Predicted state of the world after the action
    @param pre_action_agent: Agent state before the action
    @param ground_truth_post_action_agent: Ground truth agent state after the action
    @param unobserved_code: Code representing unobserved states
    @param object_count_threshold: Threshold for object count
    @return: Updated focus_set, rule_evidence, new_rules, new_negrules
    """
    new_rules = copy.deepcopy(oldrules)
    new_negrules = copy.deepcopy(oldnegrules)

    if ground_truth_post_action_agent.get_score() >= 1:
        pass  # used to place breakpoint for debugging. TODO remove

    focus_set, adjacent_change_sets, changeset0len = _build_change_sets(
        focus_set,
        oldworld,
        action,
        newworld,
        predictedworld,
        unobserved_code,
        object_count_threshold=object_count_threshold
    )

    # Build rules based on changes and prediction-observation mismatches
    # Algo: Compare all to all others,
    #
    for changeset in adjacent_change_sets:
        for y1_abs, x1_abs in changeset:
            action_values_precondition = [action,
                                          tuple(pre_action_agent.get_values_exc_score())]  # values excluding score
            preconditions = []
            CONTINUE = False
            for y2_abs, x2_abs in changeset:
                (y2_rel, x2_rel) = (y2_abs - y1_abs, x2_abs - x1_abs)  # relative to changeset 1
                condition = (y2_rel, x2_rel, oldworld.get_char_at(y2_abs, x2_abs))
                if (
                        oldworld.get_char_at(y2_abs, x2_abs) == unobserved_code
                ):  # NECESSARY FOR EPISODE RESET ONLY
                    CONTINUE = True  # old world at this location was unobserved. So no info here, skip?
                    break
                if Hypothesis_ValidCondition(condition):  # close by (0-2 in distance)
                    preconditions.append(condition)
                    # if current location in old_board has the same object on it in the newworld, we can skip forward
                    if y2_rel == 0 and x2_rel == 0:
                        if (oldworld.get_char_at(y2_abs, x2_abs)
                                == newworld.get_char_at(y1_abs, x1_abs)):
                            #
                            CONTINUE = True
                            break
            if CONTINUE:
                continue  # skip forward to next record
            preconditions = sorted(preconditions)
            for pr in preconditions:
                action_values_precondition.append(pr)
            rule = (
                tuple(action_values_precondition),
                (
                    0,
                    0,
                    newworld.get_char_at(y1_abs, x1_abs),
                    tuple(
                        [post_v - pre_v for (post_v, pre_v) in (
                            zip(ground_truth_post_action_agent.get_values_inc_score(),
                                pre_action_agent.get_values_inc_score()))]  # get the delta of each value inc score
                    ),
                ),
            )
            if len(preconditions) >= 2 and (
                    changeset0len == 3 or len(preconditions) <= 2
            ):
                rule_evidence, new_rules = Hypothesis_Confirmed(  # Mutates returned copy of rule_evidence and ruleset
                    focus_set, rule_evidence, new_rules, new_negrules, rule
                    # note newrules can be mutated in this routine.
                )
        break  # speedup (dv-this looks odd, why have the outer loop if we always break?)
        # hmm, related to the continue flag.

    # if rule conditions are only partly met or the predicted outcome is different from observed,
    # build a specialized rule which has the precondition and conclusion corrected!
    max_focus = None
    if len(focus_set) > 0:
        max_focus = max(focus_set, key=lambda m: focus_set[m])
    (positionscores, highesthighscore) = _match_hypotheses(  # scores == Match Quotient
        focus_set, oldworld, action, new_rules, pre_action_agent
    )

    height, width = oldworld.get_height_width()
    current_time = newworld.get_newest_time()

    for y in range(height):
        for x in range(width):
            if (y, x) not in positionscores:
                continue
            if (
                    not _is_presently_observed(current_time, newworld, y, x)
                    and oldworld.get_char_at(y, x) != max_focus
                    and not (
                    newworld.get_char_at(y, x) == unobserved_code and oldworld.get_char_at(y, x) != unobserved_code)
            ):
                continue
            scores, highscore, rule = positionscores[(y, x)]
            # for rule in oldrules:
            if _rule_applicable(scores, highscore, highesthighscore, rule):
                if rule[1][2] != newworld.get_char_at(y, x):
                    (precondition, consequence) = rule
                    action_score_and_preconditions = list(precondition)
                    # values = action_score_and_preconditions[1]  # dv commented out as not used 3/aug/2024
                    corrected_preconditions = []
                    CONTINUE = False
                    has_focus_set_condition = False  # TODO!!!
                    for y_rel, x_rel, requiredstate in action_score_and_preconditions[
                                                       2:
                                                       ]:
                        if (
                                y + y_rel >= height
                                or y + y_rel < 0
                                or x + x_rel >= width
                                or x + x_rel < 0
                        ):
                            CONTINUE = True
                            break
                        if oldworld.get_char_at(y + y_rel, x + x_rel) == max_focus:
                            has_focus_set_condition = True
                        if oldworld.get_char_at(y + y_rel, x + x_rel) == unobserved_code:
                            CONTINUE = True
                            break
                        corrected_preconditions.append(
                            (y_rel, x_rel, oldworld.get_char_at(y + y_rel, x + x_rel))
                        )
                    corrected_preconditions = sorted(corrected_preconditions)
                    if CONTINUE or not has_focus_set_condition:
                        continue
                    rule_new = (
                        tuple(
                            [
                                action_score_and_preconditions[0],
                                action_score_and_preconditions[1],
                            ]
                            + corrected_preconditions
                        ),
                        tuple(
                            [
                                rule[1][0],
                                rule[1][1],
                                newworld.get_char_at(y, x),
                                tuple(
                                    [post_v - pre_v for (post_v, pre_v) in (
                                        zip(ground_truth_post_action_agent.get_values_inc_score(),
                                            pre_action_agent.get_values_inc_score()))]
                                    # get the delta of each value inc score
                                ),
                            ]
                        ),
                    )
                    # print("RULE CORRECTION ", y, x, xy_loc, worldchange);
                    # Prettyprint_rule(rule);
                    # Prettyprint_rule(rule_new)
                    rule_evidence, new_rules = Hypothesis_Confirmed(
                        # Mutates returned copy of rule_evidence and ruleset
                        focus_set, rule_evidence, new_rules, new_negrules, rule_new
                    )
                    break
    # Crisp match: Add negative evidence for rules which prediction contradicts observation (in a classical AIRIS
    # implementation restricted to deterministic worlds: this part would remove contradicting rules from the
    # rule set and would ensure they can't be re-induced)
    for y in range(height):
        for x in range(width):
            if (
                    not _is_presently_observed(current_time, newworld, y, x)
                    and oldworld.get_char_at(y, x) != max_focus
                    and not (
                    newworld.get_char_at(y, x) == unobserved_code and oldworld.get_char_at(y, x) != unobserved_code)
            ):
                continue
            for (
                    rule
            ) in (
                    oldrules
            ):  # find rules which don't work, and add negative evidence for them (classical AIRIS:
                # remove them and add them to newnegrules)
                (precondition, consequence) = rule
                action_valsExScore_and_preconditions = list(precondition)
                valsExScore = action_valsExScore_and_preconditions[1]
                CONTINUE = False
                if action_valsExScore_and_preconditions[0] != action:  # rule did not apply
                    continue
                for i in range(len(valsExScore)):
                    if (
                            valsExScore[i] != pre_action_agent.get_values_exc_score()[i]  #
                    ):  # value didn't match, rule did not apply
                        CONTINUE = True
                        break
                for y_rel, x_rel, requiredstate in action_valsExScore_and_preconditions[2:]:
                    if (
                            y + y_rel >= height
                            or y + y_rel < 0
                            or x + x_rel >= width
                            or x + x_rel < 0
                    ):
                        CONTINUE = True
                        break
                    if oldworld.get_char_at(y + y_rel, x + x_rel) != requiredstate:
                        CONTINUE = True
                        break
                if CONTINUE:
                    continue
                if rule[1][3][0] != ground_truth_post_action_agent.get_score() - pre_action_agent.get_score():
                    rule_evidence, new_rules, new_negrules = Hypothesis_Contradicted(
                        # Mutates returned copy of rule_evidence
                        rule_evidence, new_rules, new_negrules, rule
                    )  # score increase did not happen
                    continue
                num_values = max(len(rule[1][3]), len(ground_truth_post_action_agent.get_values_inc_score()))
                for k in range(1, num_values):  # wrong value (not score) prediction (we start at index 1)
                    agent_value_k = ground_truth_post_action_agent.get_values_inc_score()[k]
                    rule_value_k = rule[1][3][k]
                    if rule_value_k != agent_value_k:
                        rule_evidence, new_rules, new_negrules = Hypothesis_Contradicted(
                            # Mutates returned copy of rule_evidence
                            rule_evidence, new_rules, new_negrules, rule
                        )
                        CONTINUE = True
                        break
                if CONTINUE:
                    continue
                if rule[1][2] != newworld.get_char_at(y, x):
                    rule_evidence, new_rules, new_negrules = Hypothesis_Contradicted(
                        # Mutates returned copy of rule_evidence
                        rule_evidence, new_rules, new_negrules, rule
                    )
    return focus_set, rule_evidence, new_rules, new_negrules


def nacev3_predict_and_observe(  # called _predict_and_observe in v1
        time_counter,
        focus_set,
        rule_evidence,
        xy_loc,  # pre action agent location note (0,0) is top left
        pre_action_world,  # pre action internal world model (partially observed) before last_action is applied
        rulesin,  # used in part1 and part2
        negrules,
        plan,
        last_action,
        rulesExcluded,
        post_action_ground_truth_world,  # i.e. this is the post action world model
        pre_action_agent,  # pre action agent
        ground_truth_post_action_agent,  # post action agent
        unobserved_code,  # value which indicates we can not see the true value of the cell
        object_count_threshold=1,  # how unique values must be before they are considered. was 1, i.e. unique
        print_out_world_and_plan=True):
    """
    Find difference between the actual world, and the predicted world.

    @param time_counter:
    @param focus_set:
    @param rule_evidence:
    @param xy_loc:
    @param pre_action_world:
    @param rulesin:
    @param negrules:
    @param plan:
    @param last_action:
    @param rulesExcluded:
    @param post_action_ground_truth_world:
    @param pre_action_agent
    @param ground_truth_post_action_agent
    @param print_out_world_and_plan:
    @return:
    """
    if print_out_world_and_plan:
        print("-- Predict and Observe Start ---")
    rules = copy.deepcopy(rulesin)
    simulated_world_original = copy.deepcopy(pre_action_world)
    simulated_world_post_action = copy.deepcopy(pre_action_world)
    xy_location_t_minus_1 = simulated_world_original.get_agent_xy_location()
    modified_count, _ = simulated_world_post_action.update_world_from_ground_truth(
        time_counter,
        post_action_ground_truth_world,
        [xy_loc, xy_location_t_minus_1]
    )

    r = simulated_world_post_action.get_board_char_counts()
    if "x" in r:
        if r["x"] != 1:
            pass

    stayed_the_same = modified_count == 0

    rules, rulesExcluded = Hypothesis_BestSelection(
        rules,
        rulesExcluded,
        rule_evidence,
        stayed_the_same)  # Step 2 # Mutates rules and rulesExcluded by adding and removing items

    rules = copy.deepcopy(rulesin)
    predicted_world, _, __, values, predicted_score_delta = _predict_next_world_state(
        focus_set, copy.deepcopy(simulated_world_original), last_action, rules, pre_action_agent
    )

    # Extract new rules from the observations by looking only for observed changes and prediction-observation mismatches
    focus_set, rule_evidence, newrules, newnegrules = _observe(
        focus_set,
        rule_evidence,
        simulated_world_original,
        last_action,
        simulated_world_post_action,
        rules,
        negrules,
        predicted_world,
        pre_action_agent,
        ground_truth_post_action_agent,
        unobserved_code,
        object_count_threshold
    )
    used_rules = copy.deepcopy(newrules)
    for rule in rulesExcluded:  # add again so we won't lose them
        newrules.add(rule)

    lastplanworld = copy.deepcopy(simulated_world_original)
    planworld = copy.deepcopy(predicted_world)
    for i in range(1, len(plan)):
        lastplanworld = copy.deepcopy(planworld)
        planworld, _, __, ___, ____ = _predict_next_world_state(
            focus_set, copy.deepcopy(planworld), plan[i], rules, pre_action_agent
        )

    if print_out_world_and_plan:
        post_action_ground_truth_world.multiworld_print(
            [
                {"Caption": "Internal model:\ndt=-1",
                 "World": simulated_world_original,
                 "Color": nace.color_codes.color_code_white_on_blue},

                {"Caption": "Predicted\ndt=0\n==GT?",
                 "World": predicted_world,
                 "Color": nace.color_codes.color_code_white_on_blue},

                {"Caption": f"Ground Truth \ndt=0\nt={time_counter} beliefs={len(rules)}:",
                 "World": post_action_ground_truth_world,
                 "Color": nace.color_codes.color_code_white_on_black},

                {"Caption": "End Prediction\nsteps=" + str(len(plan)) + "\n" + str(Prettyprint_Plan(plan)),
                 "World": planworld,
                 "Color": nace.color_codes.color_code_white_on_red},
            ]
        )
    if print_out_world_and_plan:
        print("-- Predict and Observe END ---")

    return (
        used_rules,
        focus_set,
        rule_evidence,
        simulated_world_post_action,
        newrules,
        newnegrules,
        values,
        lastplanworld,
        planworld,
        stayed_the_same
    )

    # return plan, action, rulesExcluded, behavior, simulated_world_staued_the_same_last_time_new_data_copied_in


if __name__ == "__main__":
    _create_explanation_graphs()
