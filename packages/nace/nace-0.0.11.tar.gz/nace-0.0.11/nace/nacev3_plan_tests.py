import color_codes
from agent_module import Agent
from nace_v3 import _plan
from world_module import left, right, up, down
from world_module_numpy import NPWorld


def get_xy_delta_for_action_list(action_list):
    # ignores walls etc.
    x = 0
    y = 0
    for action in action_list:
        if action == down:
            y += 1
        if action == up:
            y -= 1
        if action == left:
            x -= 1
        if action == right:
            x += 1
    return x, y


def get_time_and_board_at_destination(list_of_xy: list, world: NPWorld):
    x = sum([r[0] for r in list_of_xy])
    y = sum([r[1] for r in list_of_xy])
    return world.times[y][x], world.board[y][x]


def t1_plan_will_go_for_food_short():
    """
    Check a known world, that we will go for the food over short distance.

    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o f x  o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,12.0,',
                               '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,13.0,12.0,']]
    rules = {((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),

             ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             }
    actions = [left, right, up, down]
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent = Agent((8, 1), 0, ())

    world = NPWorld.from_string_list(world_str_list)

    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
        _plan(
              world,
              rules,
              actions,
              focus_set,
              agent))

    dt1 = get_xy_delta_for_action_list(lowest_conf_actions)
    dt2 = get_xy_delta_for_action_list(
        [left, left])
    assert dt1 == dt2
    assert lowest_conf_achieves_goal


def t1_plan_no_food_full_observation():
    """
    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,12.0,',
                               '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,13.0,12.0,']]
    #                                                              Score
    #                                                              Delta
    rules = {((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),

             ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),

             ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),

             ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             }
    actions = [right, left, up, down]
    focus_set = {'f': 1, 'u': 1, 'x': 5}
    agent = Agent((8, 1), 0, ())

    world = NPWorld.from_string_list(world_str_list, view_dist_x=100, view_dist_y=100)
    world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
        _plan(
              world,
              rules,
              actions,
              focus_set,
              agent))

    dxdy_best_actions = get_xy_delta_for_action_list(lowest_conf_actions)
    dxdy_best_revisit = get_xy_delta_for_action_list(oldest_age_actions)

    assert dxdy_best_actions == (1, 0)  # first in actions list
    assert dxdy_best_revisit == (2, 4)  # square furthest away (and oldest?)
    assert lowest_AIRIS_confidence == 1.0


def t1_plan_no_food_partial_observation():
    """
    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,12.0,',
                               '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,13.0,12.0,']]
    #                                                              Score
    #                                                              Delta
    rules = {((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),

             ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),

             ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),

             ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             }
    actions = [right, left, up, down]
    focus_set = {'f': 1, 'u': 1, 'x': 5}
    agent = Agent((8, 1), 0, ())

    world = NPWorld.from_string_list(world_str_list, view_dist_x=4, view_dist_y=4)
    world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

    # lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, oldest_age_actions, oldest_age, oldest_age_achieves_goal, debug_values
    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason =  (
        _plan(
              world,
              rules,
              actions,
              focus_set,
              agent))

    dxdy_best_actions = get_xy_delta_for_action_list(lowest_conf_actions)
    dxdy_best_revisit = get_xy_delta_for_action_list(oldest_age_actions)
    assert dxdy_best_actions == (-5, 1)  # nearest un observed cell
    assert lowest_AIRIS_confidence == 0.5


def t1_plan_will_go_for_food():
    """
    Check a known world, that we will go for the food over reasonably long distance.

    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o      f   o',
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,12.0,',
                               '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,13.0,12.0,']]
    rules = {((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,)))}
    actions = [left, right, up, down]
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent = Agent((8, 1), 0, ())

    world = NPWorld.from_string_list(world_str_list, view_dist_x=12, view_dist_y=5)
    world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
        _plan(
              world,
              rules,
              actions,
              focus_set,
              agent))

    dt1 = get_xy_delta_for_action_list(lowest_conf_actions)
    dt2 = get_xy_delta_for_action_list(
        [down, left, left, left, left, left, down, down, right, right, right, right, down])
    assert dt1 == dt2

    dt1 = get_xy_delta_for_action_list(oldest_age_actions)
    dt2 = get_xy_delta_for_action_list(
        [down, left, left, left, left, left, down, down, right, right, right, right, down])
    assert dt1 == dt2
    assert lowest_conf_achieves_goal
    assert oldest_age_achieves_goal
    assert oldest_age == float(10.0)
    assert lowest_AIRIS_confidence == float('-inf')  # this has been split into a new flag and line could be removed.


def t2_plan_closer_unknown_value():
    """
    If unknown value introduced nearer the agent than the known food,
    best_actions still goes for the food, but best_action_combination_for_revisit will go for the unobserved spot.

    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o     q    o',
         'o   oooooooo',
         'o       u  o',
         'o      f   o',
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,12.0,',
                               '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,13.0,12.0,']]
    rules = {((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),

             ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             }
    actions = [left, right, up, down]
    focus_set = {'f': 1, 'u': 1, 'x': 9, 'q': 1}
    agent = Agent((8, 1), 0, ())
    world = NPWorld.from_string_list(world_str_list, view_dist_x=12, view_dist_y=5)
    world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
        _plan(
              world,
              rules,
              actions,
              focus_set,
              agent))

    dxdy_revist = get_xy_delta_for_action_list(oldest_age_actions)
    dxdy_best = get_xy_delta_for_action_list(lowest_conf_actions)

    assert dxdy_best == (-1, 4)  # goes for  feather

    assert dxdy_revist == (-2, 1)  # goes to unknown,
    assert oldest_age == float(11)
    assert lowest_conf_achieves_goal


def t3_go_for_unobserved():
    """
    If no food and unobserved introduced near (time == -inf), go for unobserved.
    best_actions == best_action_combination_for_revisit

    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o     .    o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,-inf,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,12.0,',
                               '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,13.0,12.0,']]
    rules = {((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),

             ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             }
    actions = [left, right, up, down]
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent = Agent((8, 1), 0, ())

    world = NPWorld.from_string_list(world_str_list)

    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
        _plan(
              world,
              rules,
              actions,
              focus_set,
              agent))

    dt1 = get_xy_delta_for_action_list(oldest_age_actions)
    assert dt1 == (-2, 1)

    dt1 = get_xy_delta_for_action_list(lowest_conf_actions)
    assert dt1 == (-2, 1)


def t4_no_food_go_for_oldest_observed():
    """
    If no food and unobserved  nearby,

    best_action_combination_for_revisit ==  go for
    furthest point on board, even if something else was
    observed longer ago.

    best_actions == first action in list (is this optimal?)

    Is this optimal?

    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (),
        ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
         '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
         '20.0,21.0,22.0,23.0,24.0,26.0,26,26.0,26.0,26.0,26.0,26.0,',
         '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
         '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
         '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,12.0,',
         '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,13.0,12.0,']]
    rules = {
        ((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
        ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
        ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
        ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
        ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
        ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
        ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
        ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
        ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
        ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
        ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),

        ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
        ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
        ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
        ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
        ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
        ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),
        ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
        ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
        ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),

        ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
        ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
        ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
        ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
        ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
        ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
        ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
        ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
    }
    actions = [left, right, up, down, ]
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent_initial_xy_loc = (8, 1)
    agent = Agent(agent_initial_xy_loc, 0, ())

    world = NPWorld.from_string_list(world_str_list, view_dist_x=12, view_dist_y=5)
    world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
        _plan(
              world,
              rules,
              actions,
              focus_set,
              agent))

    xy_dt_bc = get_xy_delta_for_action_list(oldest_age_actions)
    xy_dt_ba = get_xy_delta_for_action_list(lowest_conf_actions)

    time_at_destination, board_value = get_time_and_board_at_destination([agent_initial_xy_loc, xy_dt_bc], world)
    assert time_at_destination == 13  # cant walk into walls


def t5_equal_distance_food():
    """

    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o      f f o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (),
        ['25,25,25,23,24,26,26,26,26,26,26,26,',
         '25,25,25,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,9999,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,25,25,25,25,25,25,25,',
         '19,19,19,19,19,19,19,16,15,14,13,12,',
         '18,18,18,18,18,18,18,16,15,14,13,12,']]
    rules = {((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),

             ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             }
    actions = [left, right, up, down, ]
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent = Agent((8, 1), 0, ())

    world = NPWorld.from_string_list(world_str_list, view_dist_x=12, view_dist_y=5)
    world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
        _plan(
              world,
              rules,
              actions,
              focus_set,
              agent))

    xy_dt2 = get_xy_delta_for_action_list(lowest_conf_actions)

    assert xy_dt2 == (-1, 1)  # go for left food (depends on action order?)
    assert lowest_conf_achieves_goal


def t6_oldest_age_and_goal_same_square():
    """

    oldest age and goal are in the same square, how / what does the code return?

    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o     xo',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o         fo',
         'oooooooooooo'], (),
        ['25,25,25,23,24,26,26,26,26,26,26,26,',
         '25,25,25,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,25,25,25,25,25,25,25,',
         '19,19,19,19,19,19,19,16,15,14,13,12,',
         '18,18,18,18,18,18,18,16,15,14,13,12,']]
    rules = {((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),

             ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             }
    actions = [left, right, up, down, ]
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent = Agent((8, 1), 0, ())

    world = NPWorld.from_string_list(world_str_list, view_dist_x=12, view_dist_y=5)
    world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
        _plan(
              world,
              rules,
              actions,
              focus_set,
              agent))

    xy_lowest_conf = get_xy_delta_for_action_list(lowest_conf_actions)
    xy_oldest = get_xy_delta_for_action_list(oldest_age_actions)

    assert xy_lowest_conf == (0, 4)
    assert xy_oldest == (0, 4)

    assert lowest_conf_achieves_goal


def t7_fully_known_world_and_rules_but_no_score_increasing_target():
    """
    Oldest age is far away. there is no food.  Does the code behave?
    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'o   o     xo',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (),
        ['25,25,25,23,24,26,26,26,26,26,26,26,',
         '25,25,25,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,25,25,25,25,25,25,25,',
         '19,19,19,19,19,19,19,16,15,14,13,12,',
         '18,18,18,18,18,18,18,16,15,14,13,12,']]
    rules = {((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),

             ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             }
    actions = [left, right, up, down, ]
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent = Agent((8, 1), 0, ())

    world = NPWorld.from_string_list(world_str_list, view_dist_x=12, view_dist_y=5)
    world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
        _plan(
              world,
              rules,
              actions,
              focus_set,
              agent))

    xy_lowest_conf = get_xy_delta_for_action_list(lowest_conf_actions)
    xy_oldest = get_xy_delta_for_action_list(oldest_age_actions)

    assert xy_lowest_conf == (-1, 0)  # could this move?
    assert xy_oldest == (0, 4)
    assert oldest_age == (26.0-13.0)
    assert lowest_AIRIS_confidence == 1.0  # the rules are fully known, and may well to world.


def t8_plan_no_food_partial_observation_best_for_revisit():
    """
    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o   x  o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o          o',
         'oooooooooooo'], (), ['25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '25.0,25.0,25.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,26.0,26.0,26.0,26.0,26.0,26.0,26.0,',
                               '20.0,21.0,22.0,23.0,24.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,',
                               '19.0,19.0,19.0,19.0,19.0,19.0,19.0,16.0,15.0,14.0,13.0,12.0,',
                               '18.0,18.0,18.0,18.0,18.0,18.0,18.0,16.0,15.0,14.0,13.0,12.0,']]
    #                                                              Score
    #                                                              Delta
    rules = {((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),

             ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),

             ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),

             ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             }
    actions = [right, left, up, down]
    focus_set = {'f': 1, 'u': 1, 'x': 5}
    agent = Agent((8, 1), 0, ())

    for i in range(1):  # seems stable, I thought it wasn't

        world = NPWorld.from_string_list(world_str_list, view_dist_x=4, view_dist_y=4)
        world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

        lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
            _plan(
                  world,
                  rules,
                  actions,
                  focus_set,
                  agent))

        dxdy_best_revisit = get_xy_delta_for_action_list(oldest_age_actions)

        print("dxdy best for revist", dxdy_best_revisit)
        assert dxdy_best_revisit in [(-3, 1), (-4, 2), (-3, 2), (-5, 1), (
            -4, 1)]  # loops back on ourselves at end, why?, on restart can be unstable why? -4,2, or -3,1
        assert lowest_AIRIS_confidence == 0.5


def t9_actual_example_where_we_fail_1():
    """
    @return:
    """
    time = 26
    world_str_list = [
        ['oooooooooooo',
         'o   o      o',
         'o       x  o',
         'o   oooooooo',
         'o       u  o',
         'o     ......',
         '............'], (),
    
    [
        '7,   8,  10,  11,  12,  14,  14,  14,  14,  14,  14,  14,',
         '7,   8,  10,  11,  12,  14,  14,  14,  14,  14,  14,  14,',
         '7,   8,  10,  11,  12,  14,  14,  14,  14,  14,  14,  14,',
         '7,   8,  10,  11,  12,  14,  14,  14,  14,  14,  14,  14,',
         '7,   8,   9,   9,   9,  14,  14,  14,  14,  14,  14,  14,',
         '5,   5,   5,   5,   5,   5, -inf, -inf, -inf, -inf, -inf, -inf,',
         '0,   0,   0,   0,   0,   0, -inf, -inf, -inf, -inf, -inf, -inf,'
    ],
    
    
    ]
    #                                                              Score
    #                                                              Delta
    rules = {((up, (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0, 0))),
             ((left, (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))),
             ((up, (0,), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1, 0))),
             ((left, (0,), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1, 0))),
             ((down, (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))),
             ((up, (0,), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1, 0))),
             ((right, (0,), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1, 0))),
             ((down, (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))),
             ((right, (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0, 0))),
             ((left, (0,), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1, 0))),
             ((down, (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0, 0))),
             ((down, (0,), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1, 0))),
             ((right, (0,), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1, 0))),
             ((right, (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))),
             ((up, (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))),
             ((left, (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0))),
             ((down, (0,), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1, 0))),
             ((right, (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))),
             ((up, (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0, 0))),
             ((left, (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0, 0)))}

    actions = [right, left, up, down]
    focus_set = {'f': 1, 'x': 11}
    agent = Agent((8, 2), 0, ())

    for i in range(1):  # seems stable, I thought it wasn't

        world = NPWorld.from_string_list(world_str_list, view_dist_x=30, view_dist_y=20)
        world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

        lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
            _plan(
                  world,
                  rules,
                  actions,
                  focus_set,
                  agent))

        dxdy_best_revisit = get_xy_delta_for_action_list(oldest_age_actions)

        print("dxdy best for revist", dxdy_best_revisit)
        assert dxdy_best_revisit in [(-2, 3)]  # nearest unexplored cell
        assert lowest_AIRIS_confidence == 0.5


def t9_actual_example_where_we_oscilate_1():
    # this happens in the cups on table challenge.
    # if the cup is on row 4, the agent has not learnt it can move the cup up and down (i guess)
    # possibility 2: when we find the score increasing action, we do not exit the search at that stage.
    time = 79
    world_str_list = [
        [   'oooooooooooo',
            'o          o',
            'o          o',
            'o     ooooTo',
            'o ux       o',
            'o          o',
            'oooooooooooo'], (),
        [
                '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,', 
                '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,', 
                '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,', 
                '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,', 
                '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,', 
                '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,', 
                '78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78,'
        ],

    ]
    #                                                              Score
    #                                                              Delta
    rules_a = {((down, (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))), ((down, (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))), ((down, (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0, 0))), ((right, (0,), (0, 0, 'x'), (0, 1, 'T')), (0, 0, 'x', (0, 0))), ((up, (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0, 0))), ((left, (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))), ((right, (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0, 0))), ((left, (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0, 0))), ((right, (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))), ((up, (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0, 0))), ((down, (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))), ((down, (0,), (-1, 0, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))), ((down, (0,), (0, 0, 'x'), (1, 0, 'T')), (0, 0, 'x', (0, 0))), ((right, (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))), ((right, (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0, 0))), ((down, (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0, 0))), ((left, (0,), (0, -1, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))), ((left, (0,), (0, 0, 'T'), (0, 1, 'x')), (0, 0, 'T', (0, 0))), ((down, (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))), ((up, (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))), ((right, (0,), (0, -1, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))), ((up, (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0, 0))), ((up, (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))), ((up, (0,), (0, 0, 'T'), (1, 0, 'x')), (0, 0, 'T', (0, 0))), ((up, (0,), (-1, 0, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))), ((right, (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))), ((right, (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))), ((left, (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))), ((up, (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0, 0))), ((left, (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0)))}

    actions = [right, left, up, down]
    focus_set = {'T': 0, 'u': 31, 'x': 76}
    agent = Agent((3,4), 2, (0,))


    world = NPWorld.from_string_list(world_str_list, view_dist_x=30, view_dist_y=20)
    world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
        _plan(
              world,
              rules_a,
              actions,
              focus_set,
              agent))

    # lowest_conf_actions == left, lowest_AIRIS_confidence==0.5, lowest_conf_stopping_reason= 'na 1'


    time_b = 80
    world_str_list_b = [
        [   'oooooooooooo',
            'o          o',
            'o          o',
            'o     ooooTo',
            'o xu       o',
            'o          o',
            'oooooooooooo'], (),
        [
                '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,', 
                '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,', 
                '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,', 
                '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,', 
                '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,', 
                '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,', 
                '79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,'
        ],

    ]

    world_b = NPWorld.from_string_list(world_str_list_b, view_dist_x=30, view_dist_y=20)
    world_b.multiworld_print([{"World": world_b, "Color": color_codes.color_code_white_on_blue}])


    rules_b = {((down, (0,), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))), ((down, (0,), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))), ((down, (0,), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0, 0))), ((right, (0,), (0, 0, 'x'), (0, 1, 'T')), (0, 0, 'x', (0, 0))), ((up, (0,), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0, 0))), ((left, (0,), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))), ((right, (0,), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0, 0))), ((left, (0,), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0, 0))), ((right, (0,), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0, 0))), ((up, (0,), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0, 0))), ((down, (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))), ((down, (0,), (-1, 0, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))), ((down, (0,), (0, 0, 'x'), (1, 0, 'T')), (0, 0, 'x', (0, 0))), ((right, (0,), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0, 0))), ((right, (0,), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0, 0))), ((down, (0,), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0, 0))), ((left, (0,), (0, -1, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))), ((left, (0,), (0, 0, 'T'), (0, 1, 'x')), (0, 0, 'T', (0, 0))), ((down, (0,), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))), ((up, (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))), ((right, (0,), (0, -1, 'x'), (0, 0, 'T')), (0, 0, 'T', (0, 0))), ((up, (0,), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0, 0))), ((up, (0,), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0, 0))), ((up, (0,), (0, 0, 'T'), (1, 0, 'x')), (0, 0, 'T', (0, 0))), ((up, (0,), (-1, 0, 'T'), (0, 0, 'x')), (0, 0, 'x', (0, 0))), ((right, (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))), ((right, (0,), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0, 0))), ((left, (0,), (0, 0, 'u'), (1, 0, 'T')), (0, 0, ' ', (0, 0))), ((up, (0,), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0, 0))), ((left, (0,), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0, 0)))}

    actions_b = [right, left, up, down]
    focus_set_b = {'T': 0, 'u': 32, 'x': 77}
    agent_b = Agent((2,4), 2, (0,))


    lowest_conf_actions_b, lowest_AIRIS_confidence_b, lowest_conf_achieves_goal_b, lowest_conf_stopping_reason_b, oldest_age_actions_b, oldest_age_b, oldest_age_achieves_goal_b, oldest_age_stopping_reason_b = (
        _plan(
              world_b,
              rules_b,
              actions_b,
              focus_set_b,
              agent_b))
    pass
    # lowest_conf_actions == left, lowest_AIRIS_confidence==0.5, lowest_conf_stopping_reason= 'na 1'



    dxdy_best_revisit = get_xy_delta_for_action_list(oldest_age_actions)

    print("dxdy best for revist", dxdy_best_revisit)
    assert dxdy_best_revisit in [(-2, 3)]  # nearest unexplored cell
    assert lowest_AIRIS_confidence == 0.5



def t10_fully_known_rules_does_the_agent_always_go_for_score_increasing_target():
    """
    @return:
    """
    world_str_list = [
        ['oooooooooooo',
         'of  o      o',
         'o          o',
         'o   oooooooo',
         'o       u  o',
         'o      x   o',
         'oooooooooooo'], (),
        ['25,25,25,23,24,26,26,26,26,26,26,26,',
         '25,25,25,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,26,26,26,26,26,26,26,',
         '20,21,22,23,24,25,25,25,25,25,25,25,',
         '19,19,19,19,19,19,19,16,15,14,13,12,',
         '18,18,18,18,18,18,18,16,15,14,13,12,']]
    rules = {((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'u'), (0, 1, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (0, 0, 'o'), (1, 0, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, ' ')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, ' '), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'u')), (0, 0, 'u', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'u')), (0, 0, 'x', (0,))),
             ((right, (), (0, -1, 'x'), (0, 0, ' ')), (0, 0, 'x', (0,))),
             ((left, (), (0, 0, 'o'), (0, 1, 'x')), (0, 0, 'o', (0,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'o')), (0, 0, 'o', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'u')), (0, 0, 'u', (0,))),
             ((right, (), (0, 0, 'x'), (0, 1, ' ')), (0, 0, ' ', (0,))),
             ((left, (), (0, -1, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),
             ((left, (), (0, -1, ' '), (0, 0, 'x')), (0, 0, ' ', (0,))),
             ((up, (), (0, 0, 'u'), (1, 0, 'x')), (0, 0, 'x', (0,))),
             ((up, (), (-1, 0, 'u'), (0, 0, 'x')), (0, 0, 'u', (0,))),

             ((left, (), (0, 0, 'f'), (0, 1, 'x')), (0, 0, 'x', (1,))),
             ((left, (), (0, -1, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((up, (), (0, 0, 'f'), (1, 0, 'x')), (0, 0, 'x', (1,))),
             ((up, (), (-1, 0, 'f'), (0, 0, 'x')), (0, 0, ' ', (1,))),
             ((down, (), (0, 0, 'x'), (1, 0, 'f')), (0, 0, ' ', (1,))),
             ((down, (), (-1, 0, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1,))),
             ((right, (), (0, 0, 'x'), (0, 1, 'f')), (0, 0, ' ', (1,))),
             }
    actions = [left, right, up, down, ]
    focus_set = {'f': 1, 'u': 1, 'x': 9}
    agent = Agent((8, 1), 0, ())

    world = NPWorld.from_string_list(world_str_list, view_dist_x=12, view_dist_y=5)
    world.multiworld_print([{"World": world, "Color": color_codes.color_code_white_on_blue}])

    lowest_conf_actions, lowest_AIRIS_confidence, lowest_conf_achieves_goal, lowest_conf_stopping_reason, oldest_age_actions, oldest_age, oldest_age_achieves_goal, oldest_age_stopping_reason = (
        _plan(
              world,
              rules,
              actions,
              focus_set,
              agent))

    xy_lowest_conf = get_xy_delta_for_action_list(lowest_conf_actions)
    xy_oldest = get_xy_delta_for_action_list(oldest_age_actions)

    assert xy_lowest_conf == (-1, 0)  # could this move?
    assert xy_oldest == (0, 4)
    assert oldest_age == (26.0-13.0)
    assert lowest_AIRIS_confidence == 1.0  # the rules are fully known, and may well to world.



if __name__ == "__main__":
    t10_fully_known_rules_does_the_agent_always_go_for_score_increasing_target()

    # t9_actual_example_where_we_oscilate_1()


    t1_plan_no_food_partial_observation()  # passes
    t1_plan_no_food_full_observation()  # passes
    t1_plan_will_go_for_food_short()  # passes
    t1_plan_will_go_for_food()  # passes
    t2_plan_closer_unknown_value()  # passes, but finds odd values
    t3_go_for_unobserved()  # passes
    t4_no_food_go_for_oldest_observed()  # passes
    t5_equal_distance_food()  # passes
    t8_plan_no_food_partial_observation_best_for_revisit()  # passes , but shows odd behaviour
    t7_fully_known_world_and_rules_but_no_score_increasing_target()
    t6_oldest_age_and_goal_same_square()
    # t9_actual_example_where_we_fail_1() # fails index out of bounds
