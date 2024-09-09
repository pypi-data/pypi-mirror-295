import numpy as np

from world_module_numpy import NPWorld


def run_1():
    # test a known grid world renders correctly and the robot is in the correct place.
    gym_world = 'o  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  o  o  o  o  o  o\nx  C  C  C  C  C  C  C  C  C  C  T\n\n'
    world = NPWorld(with_observed_time=True, name="")
    world.update_world_from_ground_truth_gymnasium_format(gym_world=gym_world)
    world_as_string = world.board_as_string()
    assert world_as_string[61] == 'x'
    print(world_as_string)


def run_2_differences():
    gym_world1 = 'o  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  x  o  o  o  o  o\no  C  C  C  C  C  C  C  C  C  C  T\n\n'
    world1 = NPWorld(with_observed_time=True, name="")
    world1.update_world_from_ground_truth_gymnasium_format(gym_world=gym_world1)

    gym_world2 = 'o  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  o  o  o  o  o  o\nx  C  C  C  C  C  C  C  C  C  C  T\n\n'
    world2 = NPWorld(with_observed_time=True, name="")
    world2.update_world_from_ground_truth_gymnasium_format(gym_world=gym_world2)

    row_indexes, column_indexes = world1.get_list_of_differences(world2)

    print("World 1")
    print(world1.board_as_string())
    print("World 2")
    print(world2.board_as_string())

    print("differences. rows:", row_indexes, "columns:", column_indexes)
    assert world1.board[row_indexes[0], column_indexes[0]] != world2.board[row_indexes[0], column_indexes[0]]
    assert world1.board[row_indexes[1], column_indexes[1]] != world2.board[row_indexes[1], column_indexes[1]]


def run_3_hashcodes():
    gym_world1 = 'o  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  x  o  o  o  o  o\no  C  C  C  C  C  C  C  C  C  C  T\n\n'
    gym_world2 = 'o  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  o  o  o  o  o  o\nx  C  C  C  C  C  C  C  C  C  C  T\n\n'
    #                                                                                                       ^diff             ^diff

    for with_observed_time in [True, False]:
        for (view_dist_x, view_dist_y) in [(3, 2), (10, 10), (100, 100)]:
            world1 = NPWorld(with_observed_time=with_observed_time, name="", view_dist_x=view_dist_x,
                             view_dist_y=view_dist_y)
            world1.update_world_from_ground_truth_gymnasium_format(gym_world=gym_world1)

            world2 = NPWorld(with_observed_time=with_observed_time, name="", view_dist_x=view_dist_x,
                             view_dist_y=view_dist_y)
            world2.update_world_from_ground_truth_gymnasium_format(gym_world=gym_world2)

            world1_duplicate = NPWorld(with_observed_time=with_observed_time, name="", view_dist_x=view_dist_x,
                                       view_dist_y=view_dist_y)
            world1_duplicate.update_world_from_ground_truth_gymnasium_format(gym_world=gym_world1)

            assert world1.get_board_hashcode() != world2.get_board_hashcode()
            assert world1.get_board_hashcode() == world1_duplicate.get_board_hashcode()

            world1_duplicate.set_char_at(2, 2, 'p')
            assert world1.get_board_hashcode() != world1_duplicate.get_board_hashcode()


def run_4_to_from_string():
    gym_world1 = 'o  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  o  o  o  o  o  o\no  o  o  o  o  o  x  o  o  o  o  o\no  C  C  C  C  C  C  C  C  C  C  T\n\n'
    world1 = NPWorld(with_observed_time=True, name="unittest")
    world1.update_world_from_ground_truth_gymnasium_format(gym_world=gym_world1)

    intermediate_fmt = world1.to_string_list()

    rebuilt = NPWorld.from_string_list(intermediate_fmt)
    assert np.array_equal(world1.times, rebuilt.times)
    assert np.array_equal(world1.board, rebuilt.board)


if __name__ == "__main__":
    run_1()
    run_2_differences()
    run_3_hashcodes()
    run_4_to_from_string()
