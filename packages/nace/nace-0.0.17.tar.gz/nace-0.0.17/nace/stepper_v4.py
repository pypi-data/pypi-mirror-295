"""
 * The MIT License
 *
 * Copyright (c) 2024 Dwane van der Sluis
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
import copy
import random
import sys
import time
from typing import Type

from nace.agent_module import Agent
from nace.nace_v3 import nacev3_get_next_action, nacev3_predict_and_observe
from nace.world_module_numpy import NPWorld


def _get_expected_deltas(nace_action_name):
    expected_directions = {
        "^left": (-1, 0),
        "^right": (1, 0),
        "^up": (0, -1),
        "^down": (0, 1)
    }
    expected_column_delta, expected_row_delta = expected_directions.get(nace_action_name, (0, 0))
    return expected_row_delta, expected_column_delta


class StepperV4():
    def __init__(self, seed_value=1, unobserved_code='.'):
        # The world is held externally.
        # The state of the agent (score number of keys held etc.) is held externally
        # Actions are performed on that world externally
        # this class wraps code and expectations that allow it to take one of the passed in worlds and predict forward.
        # partial observation (if it occurs) happens outside this code.

        # This module hole

        # variables set to specific values and passed in
        self.current_behavior = "BABBLE"
        random.seed(seed_value)

        # variables set to empty sets, or lists before the first call of this routine

        # these 4 var are global in the original implementation
        self.focus_set = dict([])
        self.rule_evidence = dict([])
        self.rules = set()
        self.negrules = set()
        self.plan = []
        self.time_counter = -1
        self.unobserved_code = unobserved_code  # indicates we have not seen the maps true value

        self.anamestr = "1234"

        # variables NOT set before the first call of this routine (in original implementation)
        self.used_rules = None
        self.debuginput = None

        self.rules_excluded = None
        self.stayed_the_same = False  # when last time the new ground truth is copied over it.

        self.post_action_agent = None
        self.pre_action_agent = None

        self.lastplanworld = None  # outputed
        self.planworld = None  # outputed
        self.internal_world = None  # working copy

        self.internal_preaction_world = None  # updated each time a best action is predicted
        self.action = None  # predicted best action

    def set_agent_ground_truth_state(self, xy_loc, score, values_exc_score):

        if self.post_action_agent is None:
            self.pre_action_agent = Agent(xy_loc, score, [0 for _ in values_exc_score])
            self.post_action_agent = Agent(xy_loc, score,
                                           values_exc_score=values_exc_score)
        else:
            self.pre_action_agent = copy.deepcopy(self.post_action_agent)
            self.post_action_agent.set_xy_loc(xy_loc)
            self.post_action_agent.set_values_inc_score([score] + list(values_exc_score))
        # Possible feature: try and reverse engineer rules that change each value into the description for that value
        # 'kx',left -> 'x ', v[1]+=1   --> pick up k
        result = {}
        for i, v in enumerate(self.post_action_agent.values):
            if i == 0:
                result["score"] = {"v": v}
            else:
                result["v" + str(i)] = {"v": v}
        return result

    def set_world_ground_truth_state(self, ground_truth_external_world: Type[NPWorld], new_xy_loc, time_counter):
        # Step 1: Update agent's field of view
        # world_module.World_FieldOfView(time_counter, xy_loc, internal_world_model, external_ground_truth_world_model)
        if ground_truth_external_world is not None:
            modified_count, _ = self.internal_world.update_world_from_ground_truth(
                time_counter,
                ground_truth_external_world, xy_locations=[new_xy_loc])

    def get_next_action(self, ground_truth_external_world: Type[NPWorld], new_xy_loc, print_debug_info,
                        time_delay_sec=0.0, available_actions=tuple([]), view_dist_x=3, view_dist_y=2):

        if self.pre_action_agent is None:
            self.pre_action_agent = Agent(new_xy_loc, score=0, values_exc_score=(0,))
        if self.internal_world is None:
            self.internal_world = NPWorld(with_observed_time=True, name="self.internal_world", view_dist_x=view_dist_x,
                                          view_dist_y=view_dist_y)

        start_time = time.time()
        self.time_counter += 1
        agent = self.post_action_agent if self.post_action_agent is not None else self.pre_action_agent

        self.plan, self.action, self.rules_excluded, self.current_behavior = nacev3_get_next_action(
            self.time_counter,
            self.focus_set,
            self.rule_evidence,  # can be mutated
            agent.get_xy_loc(),  #
            self.internal_world,  # passed in, has updates from external world applied to it.
            self.rules,
            ground_truth_external_world,  # used to update internal world
            print_debug_info=print_debug_info,
            stayed_the_same=self.stayed_the_same,
            agent=agent,
            available_actions=available_actions
        )

        # Store a copy after the external updates are copied in, i.e. the world use to predict on
        self.internal_preaction_world = copy.deepcopy(self.internal_world)

        end_time = time.time()
        if "manual" in sys.argv:
            print(self.current_behavior)
        else:
            if print_debug_info:
                print("get_next_action()", "focus=" + str(self.focus_set), self.current_behavior, "next_action=",
                      str(self.action))
        elapsed_time = end_time - start_time
        if (
                elapsed_time < time_delay_sec
                and "nosleep" not in sys.argv
                and "debug" not in sys.argv
                and "manual" not in sys.argv
        ):
            time.sleep(time_delay_sec - elapsed_time)

        return self.action, self.current_behavior

    def predict_and_observe(self,
                            object_count_threshold=1,
                            print_out_world_and_plan=True
                            ):
        """
        Possibly a new main entry point when the world does not need to be
        modeled in a way that actions can occur on it.
        @param object_count_threshold: how many new instances can be seen , and be considered, more are ignored
        @return:
        """
        (
            self.used_rules,
            self.focus_set,
            self.rule_evidence,
            predicted_world,  # self.t_minus_1_partially_observed_world,
            self.rules,
            self.negrules,
            values,
            self.lastplanworld,
            self.planworld,
            self.stayed_the_same
        ) = nacev3_predict_and_observe(
            self.time_counter,
            self.focus_set,
            self.rule_evidence,
            self.pre_action_agent.get_xy_loc(),
            copy.deepcopy(self.internal_preaction_world),  # pre action world (with times)
            self.rules,  # used in part1 and part2
            self.negrules,
            self.plan,
            self.action,
            self.rules_excluded,
            copy.deepcopy(self.internal_world),
            # post action world, can be internal or external, differences are copied in
            pre_action_agent=self.pre_action_agent,  # pre action agent
            ground_truth_post_action_agent=self.post_action_agent,  # post action agent
            unobserved_code=self.unobserved_code,
            object_count_threshold=object_count_threshold,
            print_out_world_and_plan=print_out_world_and_plan,
        )
