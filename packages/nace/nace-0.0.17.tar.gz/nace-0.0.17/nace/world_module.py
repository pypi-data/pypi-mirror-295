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
 *
 """
import copy
import random
import sys
from copy import deepcopy

import nace.color_codes
import nace.world_module_numpy
import nace.world_module

# _challenge_input = ""
# for arg in sys.argv:
#     if arg.startswith("world="):
#         _challenge_input = arg.split("world=")[1]
# # Description for world choice
# if "manual" in sys.argv:
#     if _challenge_input == "":
#         print("Enter one of 1-9 to try a world:")
# elif "no_world" in sys.argv:
#     _challenge_input = "0"
# else:
#     print(
#         'Food collecting (1), cup on table challenge (2), doors and keys (3), food collecting with moving object (4), pong (5), bring eggs to chicken (6), soccer (7), shock world (8), interactive world (9), input "1", "2", "3", "4", "5", "6", or "7":')
# if _challenge_input == "":
#     _challenge = input()
# else:
#     _challenge = _challenge_input

# print('Slippery ground y/n (n default)? Causes the chosen action to have the consequence of another action in 10% of cases.')
_slippery = "slippery" in sys.argv
_isWorld5 = False
_isWorld9 = False


def getIsWorld9():
    return _isWorld9


def set_world(_challenge_number):
    global _challenge
    _challenge = _challenge_number


def get_height_width(world):
    """ return the height and width of the board, so that callers do not need to know it's internal structure"""
    if len(world[BOARD]) > 0:
        height, width = (len(world[BOARD]), len(world[BOARD][0]))
    else:
        height, width = (0, 0)
    return height, width


def is_location_on_board(world, xy_loc):
    location_col, location_row = xy_loc
    height, width = (len(world[BOARD]), len(world[BOARD][0]))
    return location_row >= 0 and location_row < height and location_col >= 0 and location_col < width


# Whether there is a cup on the table (user-given goal demo)
def World_CupIsOnTable(world):
    if type(world) is nace.world_module_numpy.NPWorld:
        world_list = world.to_string_list()
    else:
        world_list = world

    height, width = get_height_width(world_list)
    for x in range(width):
        for y in range(height - 1):
            if world_list[BOARD][y + 1][x] == 'T' and world_list[BOARD][y][x] == 'u':
                return True
    return False


World_objective = None
# World states:

env = None
dir_right = 0
dir_down = 1
dir_left = 2
dir_up = 3
action_left = 0
action_right = 1
action_forward = 2
action_pick = 3
action_drop = 4
action_toggle = 5
lastimage = None

gwv_location_xy = (2, 4)  # never used in this file?
gwv_direction = None  # never assigned from main.py
gwv_last_reward = None
gwv_has_reset = 0
gwv_reset_score = 0
gwv_accumulated_score = 0
gwv_step = 0
gwv_episode_id = 0

run_id = -1
episodes = -1
max_steps = 1000

for arg in sys.argv:
    if arg.startswith("runid="):
        run_id = int(arg.split("runid=")[1])
    if arg.startswith("episodes="):
        episodes = int(arg.split("episodes=")[1])


def minigrid_digest(state):
    global gwv_direction, loc, lastimage, gwv_last_reward, gwv_step
    gwv_step += 1
    # print(state[0]["direction"]); exit(0)
    gwv_direction = state[0]["direction"]
    # print(state[0]['image'].shape); exit(0)
    loc = env.agent_pos
    lastimage = state[0]["image"]
    if len(state) == 5 and (gwv_last_reward == 0 or gwv_last_reward == None) and state[1] != 0:
        gwv_last_reward = state[1]
        reward = state[1]


VIEWDISTX, VIEWDISTY = (3, 2)
COFFEEMACHINE, WALL, ROBOT, CUP, FOOD, BATTERY, FREE, TABLE, GOAL, KEY, DOOR, ARROW_DOWN, ARROW_UP, BALL, EGG, EGGPLACE, CHICKEN, SBALL, SHOCK = \
    ('G', 'o', 'x', 'u', 'f', 'b', ' ', 'T', 'H', 'k', 'D', 'v', '^', 'c', 'O', '_', '4', '0', 'z')


def get_world_str(_challenge, max_steps=1000):
    global world_str

    global _isWorld9
    global _isWorld5
    global isMinigridWorld
    global World_objective

    World_objective = None

    # The worlds:
    world_str = """
    oooooooooooo
    o   o   f  o
    o          o
    o   oooooooo
    o x        o
    o       u  o
    oooooooooooo
    """
    _world2 = """
    oooooooooooo
    o          o
    o   u      o
    o     ooooTo
    o x        o
    o          o
    oooooooooooo
    """
    _world3 = """
    oooooooooooo
    o   k o   ko
    o     D b  o
    o     oooooo
    o x   D b  o
    o     o   ko
    oooooooooooo
    """
    _world4 = """
    oooooooooooo
    o  vo   f  o
    o          o
    o   oooooooo
    o x        o
    o       u  o
    oooooooooooo
    """
    _world5 = """
    oooooooooooo
    oo          
    oo          
    oo         c
    oox         
    oo          
    oooooooooooo
    """
    _world6 = """
    oooooooooooo
    o O  4  O  o
    o          o
    o          o
    o x  O  O  o
    o          o
    oooooooooooo
    """
    _world7 = """
    oooooooooooo
    o          o
    o  0 0     o
    o       H  o
    o x0 0     o
    o          o
    oooooooooooo
    """
    _world8 = """
    oooooooooooo
    o     zzzzzo
    o f z z    o
    o   z z zz o
    o x z z z  o
    o   z   z  o
    oooooooooooo
    """
    _world9 = """
    oooooooooooo
    o          o
    o     u    o
    o  T     G o
    o x   H    o
    o          o
    oooooooooooo
    """
    _world_empty = """











    """
    world_test_1 = """
    oooooo
    o   fo
    ox   o
    oooooo
    """

    if "t1" == _challenge:
        world_str = world_test_1
    if "2" == _challenge:
        world_str = _world2
        World_objective = World_CupIsOnTable
    if "3" == _challenge:
        world_str = _world3
    if "4" == _challenge:
        world_str = _world4
    if "5" == _challenge:
        world_str = _world5
        _isWorld5 = True
        global VIEWDISTX
        global VIEWDISTY
        VIEWDISTX, VIEWDISTY = (4, 3)

    if "6" == _challenge:
        world_str = _world6
    if "7" == _challenge:
        world_str = _world7
    if "8" == _challenge:
        world_str = _world8
    if "9" == _challenge:
        world_str = _world9
        _isWorld9 = True

    worldstr = "MiniGrid-DoorKey-8x8-v0"
    if "10" == _challenge:
        worldstr = "MiniGrid-Empty-8x8-v0"
    if "11" == _challenge:
        worldstr = "BabyAI-GoToRedBallNoDists-v0"
    if "12" == _challenge:
        worldstr = "MiniGrid-DistShift2-v0"
    if "13" == _challenge:
        worldstr = "MiniGrid-LavaGapS7-v0"
    if "14" == _challenge:
        worldstr = "MiniGrid-SimpleCrossingS11N5-v0"
    if "15" == _challenge:
        worldstr = "MiniGrid-LavaCrossingS11N5-v0"
    if "16" == _challenge:
        worldstr = "MiniGrid-Unlock-v0"
    if "17" == _challenge:
        worldstr = "MiniGrid-DoorKey-8x8-v0"
    if "18" == _challenge:
        worldstr = "MiniGrid-UnlockPickup-v0"
    if "19" == _challenge:
        worldstr = "MiniGrid-BlockedUnlockPickup-v0"

    isMinigridWorld = _challenge.isdigit() and int(_challenge) >= 10  # Minigrid challenges start at that index
    # if isMinigridWorld:  # "9" in _challenge:
    #     from minigrid.wrappers import *
    #
    #     _isWorld5 = False  # TODO
    #     if "nominigrid" not in sys.argv:
    #         env = gym.make(worldstr, render_mode='human', max_steps=max_steps)
    #     else:
    #         env = gym.make(worldstr, max_steps=max_steps)
    #     observation_reward_and_whatever = env.reset()
    #     minigrid_digest(observation_reward_and_whatever)
    #     print("Observation:", observation_reward_and_whatever)
    #     if "nominigrid" not in sys.argv:
    #         env.render()
    #     world_str = _world_empty
    #     loc = env.agent_pos

    if _isWorld5:
        set_full_action_list(list(set([up, down, right])))
    if isMinigridWorld and int(_challenge) >= 16:
        set_full_action_list(list(set([left, right, up, down, drop, pick, drop, toggle])))

    # strip leading and trailing spaces that were introduced by python tabs.
    t_world_str = world_str.split("\n")
    t_world_str_list = [s.strip() for s in t_world_str if len(s.strip()) > 0]

    if _isWorld5:
        t_world_str_list = [t.ljust(len(t_world_str_list[0]), " ") for t in t_world_str_list]

    for i, str in enumerate(t_world_str_list):
        assert len(str) == len(t_world_str_list[0])

    world_str = "\n".join(t_world_str_list)
    return world_str


#
# World is a tuple:
# (
#   Array of char that is a map,
#   tuple : ( Score?, Value? )
#   Array of int, how long ago the map was observed at that location, (if never observed -inf)
# )


BOARD, VALUES, TIMES = (0, 1, 2)


def build_initial_world_object(_challenge, unobserved_code):
    world_str = get_world_str(_challenge)
    world_obj = [[[*x] for x in world_str.split("\n")], tuple([0, 0])]
    _height, _width = get_height_width(world_obj)
    world_obj.append([[float("-inf") for i in range(_width)] for j in range(_height)])

    observed_world = [
        [[unobserved_code for x in world_obj[BOARD][i]] for i in
         range(len(world_obj[BOARD]))],
        world_obj[VALUES],
        world_obj[TIMES],
    ]
    return world_obj, observed_world, _height, _width


def build_blank_world_surrounded_by_wall(height, width, wall_char="\u2588", free_char='_', agent_char='x', agent_col=1,
                                         agent_row=1):
    result = ""
    for c in range(height):
        line = ""
        for r in range(width):
            if r == agent_row and c == agent_col:
                line += agent_char
            else:
                if r in [0, width - 1] or c in [0, height - 1]:
                    line += wall_char
                else:
                    line += free_char
        result += line + "\n"
    return result


def extract_agent_location_from_board(board, location_indicator_char='x'):
    """
    Extrat the location of an item on the board. Assumes uniqueness
    @param board:
    @param location_indicator_char:
    @return:
    """
    location_row = 0
    location_column = 0
    # check the sizes are correct, and see where location marker is
    for row_number in range(len(board)):
        if row_number > 0:
            assert len(board[0]) == len(board[row_number])
        # check for location marker
        if location_indicator_char in board[row_number]:
            location_row = row_number
            location_column = board[row_number].index(location_indicator_char)
    return (location_column, location_row)


def convert_gymnasium_world_to_nace(gym_world: str, strip_blanks=True, location_indicator_char='x', state_source=None,
                                    add_surrounding_walls=True, wall_code='W'):
    """

    @param gym_world: str , each \n indicates a new row, white space is stripped. agent location indicated by  location_indicator_char
    @param strip_blanks:
    @param location_indicator_char:  char representing the agent
    @param last_world: if not none, state and times seen copied from this world
    @param add_walls_right_and_bottom:
    @param wall_code:
    @return:
    """
    board = []  # list of rows. Each row is a list of char.
    for row_number, row_str in enumerate(gym_world.split("\n")):
        if len(row_str.strip()) > 0:
            if strip_blanks:
                board.append([c for c in list(row_str) if c != " "])
            else:
                board.append(list(row_str))
    if add_surrounding_walls:
        for row in board:
            row.append(wall_code)
            row.insert(0, wall_code)
        extra_line = [wall_code for _ in row]
        board.append(extra_line)
        board.insert(0, extra_line)

    BOARD, VALUES, TIMES = (0, 1, 2)

    if state_source is None:
        world_state = tuple([0, 0])
        height, width = (len(board), len(board[0]))
        world_observed_at = [[float("-inf") for i in range(width)] for j in range(height)]
    else:
        world_state = copy.deepcopy(state_source[VALUES])
        world_observed_at = copy.deepcopy(
            state_source[TIMES])  # this should never be used, here to speed conversion of code.

    nace_world = [board, world_state, world_observed_at]

    xy_location = extract_agent_location_from_board(board, location_indicator_char=location_indicator_char)

    return nace_world, xy_location  # NOTE location is xy format


# Move operations to move the agent in the world:
def left(loc):
    return (loc[0] - 1, loc[1])


def right(loc):
    if _isWorld5:
        return loc
    return (loc[0] + 1, loc[1])


def up(loc):
    return (loc[0], loc[1] - 1)


def down(loc):
    return (loc[0], loc[1] + 1)


def pick(loc):
    return loc


def drop(loc):
    return loc


def toggle(loc):
    return loc


gwv_lastseen = set([])


def help(action):
    if action != drop:
        minigrid_digest(env.step(action_toggle))
        minigrid_digest(env.step(action_pick))


def cntEntry(world, VAL):
    cnt = 0
    height, width = get_height_width(world)
    for y in range(height):
        for x in range(width):
            if world[BOARD][y][x] == VAL:
                cnt += 1
    return cnt


def World_Move(local_location, world, action, external_reward_for_last_action, annomate_arrows_prob=0.25):
    """

    Applies the effect of the movement operations, considering how different grid cell types interact with each other.
    Contains specific, hard coded logic, that the agent is expected to learn, or work around.

    @param local_location: assume xy location?
    @param world:
    @param action:
    @return:
    """
    global gwv_lastseen  # does not seem to need to be global
    global gwv_last_reward, gwv_has_reset, gwv_reset_score, gwv_accumulated_score, gwv_step, gwv_episode_id
    gwv_lastseen = set([])
    gwv_last_reward = 0

    height, width = get_height_width(world)

    if env is not None:
        """if action == pick:
            minigrid_digest(env.step(action_pick))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_pick))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_pick))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_pick))
            minigrid_digest(env.step(action_right))
        if action == drop:
            minigrid_digest(env.step(action_drop))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_drop))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_drop))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_drop))
            minigrid_digest(env.step(action_right))
        if action == toggle:
            minigrid_digest(env.step(action_toggle))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_toggle))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_toggle))
            minigrid_digest(env.step(action_right))
            minigrid_digest(env.step(action_toggle))
            minigrid_digest(env.step(action_right))"""

        if action == drop:  # drop below always
            if gwv_direction == dir_down:
                help(action);
                minigrid_digest(env.step(action_drop))
            elif gwv_direction == dir_left:
                minigrid_digest(env.step(action_left))
                help(action);
                minigrid_digest(env.step(action_drop))
            elif gwv_direction == dir_right:
                minigrid_digest(env.step(action_right))
                help(action);
                minigrid_digest(env.step(action_drop))
            elif gwv_direction == dir_up:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                help(action);
                minigrid_digest(env.step(action_drop))
        if action == left:
            if gwv_direction == dir_left:
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_down:
                minigrid_digest(env.step(action_right))
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_up:
                minigrid_digest(env.step(action_left))
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_right:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                help(action);
                minigrid_digest(env.step(action_forward))
            """if lastActionIsPick:
                minigrid_digest(env.step(action_pick))
            if lastActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if lastActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        if action == right:
            if gwv_direction == dir_right:
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_down:
                minigrid_digest(env.step(action_left))
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_up:
                minigrid_digest(env.step(action_right))
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_left:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                help(action);
                minigrid_digest(env.step(action_forward))
            """if lastActionIsPick:
                minigrid_digest(env.step(action_pick))
            if lastActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if lastActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        if action == up:
            if gwv_direction == dir_up:
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_right:
                minigrid_digest(env.step(action_left))
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_left:
                minigrid_digest(env.step(action_right))
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_down:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                help(action);
                minigrid_digest(env.step(action_forward))
            """if lastActionIsPick:
                minigrid_digest(env.step(action_pick))
            if lastActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if lastActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        if action == down:
            if gwv_direction == dir_down:
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_right:
                minigrid_digest(env.step(action_right))
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_left:
                minigrid_digest(env.step(action_left))
                help(action);
                minigrid_digest(env.step(action_forward))
            if gwv_direction == dir_up:
                minigrid_digest(env.step(action_right))
                minigrid_digest(env.step(action_right))
                help(action);
                minigrid_digest(env.step(action_forward))
            """if lastActionIsPick:
                minigrid_digest(env.step(action_pick))
            if lastActionIsDrop:
                minigrid_digest(env.step(action_drop))
            if lastActionIsToggle:
                minigrid_digest(env.step(action_toggle))"""
        # help(action)
        newloc = env.agent_pos  # a breakpoint placed here is never triggered from any of my flows.
        oldworld = deepcopy(world)

        M = {(1, 0): FREE, (2, 0): WALL, (4, 0): FREE, (4, 1): FREE, (4, 2): DOOR, (5, 0): KEY, (6, 0): BALL,
             (7, 0): TABLE, (8, 0): GOAL, (9, 0): SHOCK}
        for i in range(7):
            for j in reversed(range(7)):
                if lastimage[i, j][0] == 0:
                    break
                if gwv_direction == dir_right:
                    X = newloc[0] + (7 - (j + 1))
                    Y = newloc[1] + i - 3
                    gwv_lastseen.add((Y, X))
                    # print(lastimage); exit(0)
                    V = (lastimage[i, j][0], lastimage[i, j][2])
                    if V[0] != 0 and Y >= 0 and X >= 0 and Y < height and X < width:
                        # print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]
                if gwv_direction == dir_left:
                    X = newloc[0] - (7 - (j + 1))
                    Y = newloc[1] - i + 3
                    # print(lastimage); exit(0)
                    gwv_lastseen.add((Y, X))
                    V = (lastimage[i, j][0], lastimage[i, j][2])
                    if V[0] != 0 and Y >= 0 and X >= 0 and Y < height and X < width:
                        # print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]

                if gwv_direction == dir_up:
                    Y = newloc[1] - (7 - (j + 1))
                    X = newloc[0] + i - 3
                    # print(lastimage); exit(0)
                    gwv_lastseen.add((Y, X))
                    V = (lastimage[i, j][0], lastimage[i, j][2])
                    if V[0] != 0 and Y >= 0 and X >= 0 and Y < height and X < width:
                        # print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]
                if gwv_direction == dir_down:
                    Y = newloc[1] + (7 - (j + 1))
                    X = newloc[0] - i + 3
                    # print(lastimage); exit(0)
                    gwv_lastseen.add((Y, X))
                    V = (lastimage[i, j][0], lastimage[i, j][2])
                    if V[0] != 0 and Y >= 0 and X >= 0 and Y < height and X < width:
                        # print("!!!", (X,Y), (i,j), V)
                        world[BOARD][Y][X] = M[V]

        world[BOARD][local_location[1]][local_location[0]] = gwv_traversable_board_values[
            0]  # set to first free value from transversable set
        world[BOARD][newloc[1]][newloc[0]] = ROBOT
        local_location = newloc
        i_inventory = 3
        j_inventory = 6
        V_inventory = lastimage[i_inventory, j_inventory][0]
        if (cntEntry(oldworld, TABLE) > cntEntry(world, TABLE)) or \
                (cntEntry(oldworld, GOAL) > cntEntry(world, GOAL)) or \
                (cntEntry(oldworld, SHOCK) > cntEntry(world, SHOCK)) or gwv_last_reward != 0:
            gwv_episode_id += 1
            if gwv_last_reward > 0 or (cntEntry(oldworld, TABLE) > cntEntry(world, TABLE)) or (
                    cntEntry(oldworld, GOAL) > cntEntry(world, GOAL)):
                gwv_last_reward = 1  # minigrid is not giving so we provide own reward
            else:
                gwv_last_reward = -1
            gwv_accumulated_score += gwv_last_reward
            world[VALUES] = (gwv_accumulated_score, V_inventory)
            gwv_has_reset = 2  # ugly double reset hack is needed
            gwv_reset_score = world[VALUES][0]
            minigrid_digest(env.reset())
            if run_id != -1:
                reward = 1 - 0.9 * (gwv_step / max_steps)
                if gwv_episode_id < episodes:
                    with open("run_world" + str(_challenge_input) + "_" + str(run_id) + ".run", "a") as f:
                        f.write(f"{gwv_episode_id} {reward}\n")
                if episodes != -1 and gwv_episode_id >= episodes:
                    exit(0)
                gwv_step = 0
        else:
            gwv_accumulated_score += gwv_last_reward
            world[VALUES] = (gwv_accumulated_score, V_inventory)
        return local_location, [world[BOARD], world[VALUES], world[TIMES]]
    if _slippery and random.random() > 0.9:  # agent still believes it did the proper action
        action = random.choice(gwv_full_action_list)  # but the world is slippery!
    newloc = action(local_location)  # the bounding is checked just below

    if newloc[0] < 0:
        newloc = (0, newloc[1])
    if newloc[1] < 0:
        newloc = (newloc[0], 0)
    if newloc[0] >= width:
        newloc = (width - 1, newloc[1])
    if newloc[1] >= height:
        newloc = (newloc[0], height - 1)

    oldworld = deepcopy(world)
    # ROBOT MOVEMENT ON FREE SPACE
    movedAgent = False
    if oldworld[BOARD][newloc[1]][newloc[
        0]] in get_traversable_board_values():  # TODO the list of objects the agent can move onto should be learned
        world[BOARD][local_location[1]][local_location[0]] = gwv_traversable_board_values[
            0]  # set to first free value from transversable set  # TODO after the agent moved off a spot, replace it with the last observed in that location? or free, and let outside model correct it?
        world[BOARD][newloc[1]][newloc[0]] = ROBOT
        movedAgent = local_location != newloc
        local_location = newloc
    oldoldworld = deepcopy(oldworld)
    oldworld = deepcopy(world)

    annomate_arrows = random.random() < annomate_arrows_prob

    for y in range(height):
        for x in range(width):
            if oldworld[BOARD][y][x] == BALL and world[BOARD][y][x - 1] in gwv_traversable_board_values and \
                    oldoldworld[BOARD][y][
                        x - 1] in gwv_traversable_board_values:
                world[BOARD][y][x - 1] = BALL
                world[BOARD][y][x] = gwv_traversable_board_values[0]  # set to first free value from transversable set
            if oldworld[BOARD][y][x] == BALL and oldworld[BOARD][y][x - 1] == WALL:
                world[BOARD][y][x] = gwv_traversable_board_values[0]  # set to first free value from transversable set
                world[BOARD][random.choice(range(1, height - 1))][width - 1] = BALL
            if oldworld[BOARD][y][x] == BALL and oldoldworld[BOARD][y][x - 1] == ROBOT:
                world[BOARD][y][x] = gwv_traversable_board_values[0]  # set to first free value from transversable set
                world[BOARD][random.choice(range(1, height - 1))][width - 1] = BALL
                if not movedAgent:
                    world[VALUES] = tuple(
                        [world[VALUES][0] + 1] + list(world[VALUES][1:]))  # the first value +1 and the rest stays

            if annomate_arrows and oldworld[BOARD][y][x] == ARROW_DOWN and oldworld[BOARD][y + 1][
                x] in gwv_traversable_board_values:
                world[BOARD][y + 1][x] = ARROW_DOWN
                world[BOARD][y][x] = gwv_traversable_board_values[0]  # set to first free value from transversable set
            if annomate_arrows and oldworld[BOARD][y][x] == ARROW_UP and oldworld[BOARD][y - 1][
                x] in gwv_traversable_board_values:
                world[BOARD][y - 1][x] = ARROW_UP
                world[BOARD][y][x] = gwv_traversable_board_values[0]  # set to first free value from transversable set
            if annomate_arrows and oldworld[BOARD][y][x] == ARROW_DOWN and oldworld[BOARD][y + 1][x] in [WALL, ROBOT,
                                                                                                         FOOD]:
                world[BOARD][y][x] = ARROW_UP
            if annomate_arrows and oldworld[BOARD][y][x] == ARROW_UP and oldworld[BOARD][y - 1][x] in [WALL, ROBOT,
                                                                                                       FOOD]:
                world[BOARD][y][x] = ARROW_DOWN
            if oldworld[BOARD][y][x] == CUP and oldworld[BOARD][y + 1][x] == TABLE:
                if not _isWorld9:
                    world[BOARD][y][x] = gwv_traversable_board_values[
                        0]  # set to first free value from transversable set
                    while True:
                        xr, yr = (random.randint(0, width - 1), random.randint(0, height - 1))
                        if oldworld[BOARD][yr][xr] in gwv_traversable_board_values:
                            world[BOARD][yr][xr] = CUP
                            break
    # CUP
    if world[BOARD][newloc[1]][newloc[0]] == CUP:  # an object the system could shift around
        world[BOARD][local_location[1]][local_location[0]] = CUP
        local_location = newloc
        world[BOARD][local_location[1]][local_location[0]] = ROBOT
    # KEY
    if world[BOARD][newloc[1]][newloc[0]] == KEY:
        world[BOARD][local_location[1]][local_location[0]] = gwv_traversable_board_values[
            0]  # set to first free value from transversable set
        local_location = newloc
        world[BOARD][local_location[1]][local_location[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] + 1] + list(
            world[VALUES][2:]))  # the second value +1 and the rest stays. (we picked up a key)
    # DOOR
    if world[BOARD][newloc[1]][newloc[0]] == DOOR and world[VALUES][1] > 0:
        world[BOARD][local_location[1]][local_location[0]] = gwv_traversable_board_values[
            0]  # set to first free value from transversable set
        local_location = newloc
        world[BOARD][local_location[1]][local_location[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] - 1] + list(
            world[VALUES][2:]))  # the second value -1 and the rest stays (we used the key on the door)
    # BATTERY
    if world[BOARD][newloc[1]][newloc[0]] == BATTERY:
        world[BOARD][local_location[1]][local_location[0]] = gwv_traversable_board_values[
            0]  # set to first free value from transversable set
        local_location = newloc
        world[BOARD][local_location[1]][local_location[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:]))  # the first value +1 and the rest stays
    # SHOCK
    if world[BOARD][newloc[1]][newloc[0]] == SHOCK:
        world[BOARD][local_location[1]][local_location[0]] = gwv_traversable_board_values[
            0]  # set to first free value from transversable set
        local_location = newloc
        world[BOARD][local_location[1]][local_location[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0] - 1] + list(world[VALUES][1:]))  # the first value -1 and the rest stays
    # FOOD
    if world[BOARD][newloc[1]][newloc[0]] == FOOD:
        world[BOARD][local_location[1]][local_location[0]] = gwv_traversable_board_values[
            0]  # set to first free value from transversable set
        local_location = newloc
        world[BOARD][local_location[1]][local_location[0]] = ROBOT
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:]))  # the first value +1 and the rest stays

        new_food_placed = False
        for poss_xy_location in [(8, 1), (8, 5), (9, 5), (7, 5)]:
            x, y = poss_xy_location
            if world[BOARD][y][x] in gwv_traversable_board_values:
                world[BOARD][y][x] = FOOD
                new_food_placed = True
                break
        if not new_food_placed:
            while True:
                x, y = (random.randint(0, width - 1), random.randint(0, height - 1))
                if world[BOARD][y][x] in gwv_traversable_board_values:
                    world[BOARD][y][x] = FOOD
                    break

    # EGG
    if world[BOARD][newloc[1]][newloc[0]] == EGG and world[VALUES][1] == 0:  # can only carry 1
        world[BOARD][newloc[1]][newloc[0]] = EGGPLACE  # EGGPLACE - where an egg was.
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] + 1] + list(world[VALUES][2:]))
    elif world[BOARD][newloc[1]][newloc[0]] == EGGPLACE and world[VALUES][1] > 0:
        world[BOARD][newloc[1]][newloc[0]] = EGG
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] - 1] + list(world[VALUES][2:]))
    elif world[BOARD][newloc[1]][newloc[0]] == CHICKEN and world[VALUES][1] > 0:
        world[VALUES] = tuple([world[VALUES][0]] + [world[VALUES][1] - 1] + list(world[VALUES][2:]))
        world[VALUES] = tuple([world[VALUES][0] + 1] + list(world[VALUES][1:]))  # 1 food
    # Football
    crateloc = action(newloc)
    if crateloc[1] < height and crateloc[0] < width and crateloc[1] >= 0 and crateloc[0] >= 0:
        if world[BOARD][crateloc[1]][crateloc[0]] in gwv_traversable_board_values:
            if world[BOARD][newloc[1]][newloc[0]] == SBALL:
                world[BOARD][local_location[1]][local_location[0]] = gwv_traversable_board_values[
                    0]  # set to first free value from transversable set
                local_location = newloc
                world[BOARD][local_location[1]][local_location[0]] = ROBOT
                world[BOARD][crateloc[1]][crateloc[0]] = SBALL
        if world[BOARD][crateloc[1]][crateloc[0]] == GOAL and world[BOARD][newloc[1]][newloc[0]] == SBALL:
            world[BOARD][local_location[1]][local_location[0]] = gwv_traversable_board_values[
                0]  # set to first free value from transversable set
            local_location = newloc
            world[BOARD][newloc[1]][newloc[0]] = ROBOT
            world[VALUES] = tuple(
                [world[VALUES][0] + 1] + list(world[VALUES][1:]))  # the first value +1 and the rest stays
            while True:
                xr, yr = (random.randint(0, width - 1), random.randint(0, height - 1))
                if oldworld[BOARD][yr][
                    xr] in gwv_traversable_board_values and xr > 1 and yr > 1 and xr < width - 2 and yr < height - 2 and \
                        oldworld[BOARD][yr + 1][xr] in gwv_traversable_board_values and oldworld[BOARD][yr - 1][
                    xr] in gwv_traversable_board_values and \
                        oldworld[BOARD][yr][xr + 1] in gwv_traversable_board_values and oldworld[BOARD][yr][
                    xr - 1] in gwv_traversable_board_values:
                    world[BOARD][yr][xr] = SBALL
                    break

    if external_reward_for_last_action is not None:
        world[VALUES] = tuple(
            [world[VALUES][0] + external_reward_for_last_action] + list(
                world[VALUES][1:]))  # the first value += external_reward_for_last_action and the rest stays

    if World_GetObjective() is not None:
        if World_GetObjective()(world):
            l = list(world[VALUES])
            world[VALUES] = tuple([l[0] + 1] + l[1:])

    return local_location, [world[BOARD], world[VALUES], world[TIMES]]


def World_Criteria(world):
    return World_objective(world)


def World_SetObjective(func):
    global World_objective
    World_objective = func


def World_GetObjective():
    return World_objective


# Print the world into the terminal
def World_Print(world):
    for line in world[BOARD]:
        print("".join(line))


def Multiple_World_Print(list_of_worlds, pad_length=30):
    """
    Print a number of worlds in coloured text, left to right across the screen
    @param list_of_worlds: dict e.g. [{"World":list[list[char]], "Caption":str, "Color":color code}]
    @return:
    """
    max_lines = max([len(record["World"][BOARD]) for record in list_of_worlds])

    line = ""
    for world_index in range(len(list_of_worlds)):
        line += list_of_worlds[world_index]["Caption"].ljust(pad_length, " ")

    print(line)

    for line_num in range(max_lines):
        line = ""
        for world_index in range(len(list_of_worlds)):
            pass
            # Set the color
            if "Color" in list_of_worlds[world_index]:
                line += list_of_worlds[world_index]["Color"]
            map_line = "".join(list_of_worlds[world_index]["World"][BOARD][line_num])
            line += map_line
            line += nace.color_codes.color_code_black_on_white
            line += map_line.ljust(pad_length, " ")[len(map_line):]
        print(line)
    pass


def World_FieldOfView(Time, local_xy_location, observed_world, external_world):
    """
    The limited field of view the agent can observe dependent on view distance (partial observability)
    Does this by merging parts of the full visibility world with the last known partially observed world.
    State is held in the observed world. New visible portions of 'world' are copied into observed world.

    This mutates the observed_world passed in (updated time) and returns it, but assignment of the return value to the same variable
    can overwrite these changes.

    @param Time:
    @param local_xy_location:
    @param observed_world:
    @param external_world:
    @return:
    """
    global gwv_has_reset

    height, width = (len(external_world[BOARD]), len(external_world[BOARD][0]))

    for Y in range(height):
        for X in range(width):
            if observed_world[TIMES][Y][X] == Time:
                observed_world[TIMES][Y][
                    X] = Time - 1  # WHY can this ever happen??? DEBUG! it can happen if this routine is called twice in a row.
    if env is None:  # usual case. This will 'move' the robot in the process of freshening the observed world.
        for y in range(VIEWDISTY * 2 + 1):
            for x in range(VIEWDISTX * 2 + 1):
                Y = local_xy_location[1] + y - VIEWDISTY
                X = local_xy_location[0] + x - VIEWDISTX
                if Y >= 0 and Y < height and \
                        X >= 0 and X < width:
                    observed_world[BOARD][Y][X] = external_world[BOARD][Y][X]
                    observed_world[TIMES][Y][X] = Time
    else:
        if gwv_has_reset > 0:
            external_world[VALUES] = (gwv_reset_score, 0)
            for y in range(height):
                for x in range(width):
                    observed_world[BOARD][y][x] = '.'
                    external_world[BOARD][y][x] = gwv_traversable_board_values[
                        0]  # set to first free value from transversable set
                    observed_world[TIMES][y][x] = Time - 1000
            observed_world[VALUES] = (gwv_reset_score, 0)
            external_world[VALUES] = (gwv_reset_score, 0)
            gwv_has_reset -= 1
            # PRINT("RESET!!!!!!!!!!!!")
        for Y in range(height):
            for X in range(width):
                if observed_world[BOARD][Y][X] == ROBOT:
                    observed_world[BOARD][Y][X] = gwv_traversable_board_values[
                        0]  # set to first free value from transversable set
        for Y in range(height):
            for X in range(width):
                if (Y, X) in gwv_lastseen:
                    if Y >= 0 and Y < height and \
                            X >= 0 and X < width:
                        observed_world[BOARD][Y][X] = external_world[BOARD][Y][X]
                        observed_world[TIMES][Y][X] = Time
    observed_world[VALUES] = deepcopy(external_world[VALUES])  # copy the values across (NOT the times or board)


def World_AsTuple(worldpart):
    """
    @param worldpart:
    @return: The world component represented as an immutable tuple
    """
    return tuple(World_AsTuple(i) if isinstance(i, list) else i for i in worldpart)


def World_Num5():
    return _isWorld5


# The actions the agent can take dependent on the chosen world:
gwv_full_action_list = [left, right, up, down]  # was called actions


def get_full_action_list():
    """
    @return: a list of all the known/valid actions for the world
    """
    global gwv_full_action_list

    # if (gwv_full_action_list[0] != left or
    #         gwv_full_action_list[1] != right or
    #         gwv_full_action_list[2] != up or
    #         gwv_full_action_list[3] != down
    # ):
    #     print("WARN: Actions are stored in a different order")

    return copy.deepcopy(gwv_full_action_list)


def add_to_full_action_list(new_action):
    """
    Adds an action to this list of existing actions if not already part of the list.
    @param new_action:
    @return: nothing
    """
    global gwv_full_action_list
    if new_action not in gwv_full_action_list:
        gwv_full_action_list.append(new_action)


def set_full_action_list(action_list):
    """
    sets in the list of passed in actions as the possible action that can be taken. Conserves order.
    @param new_action:
    @return: nothing
    """
    global gwv_full_action_list
    gwv_full_action_list.clear()
    gwv_full_action_list.extend(action_list)


# The board values that the agent can move onto. Use getters and setters for access
gwv_traversable_board_values = list(set([FREE]))


def add_traversable_board_value(value: str):
    global gwv_traversable_board_values
    gwv_traversable_board_values.add(value)


def set_traversable_board_value(value: str):
    global gwv_traversable_board_values
    gwv_traversable_board_values = list(set([value]))


def get_traversable_board_values():
    global gwv_traversable_board_values
    return deepcopy(gwv_traversable_board_values)



def _act(
        xy_loc, fully_observed_pre_action_world, action, inject_key, external_reward_for_last_action):
    # move the agent on the map, and upload location
    xy_loc, fully_observed_post_action_world = nace.world_module.World_Move(xy_loc,
                                                                       deepcopy(fully_observed_pre_action_world),
                                                                       action,
                                                                       None if external_reward_for_last_action == 0 else external_reward_for_last_action)
    return xy_loc, fully_observed_post_action_world, "na"
