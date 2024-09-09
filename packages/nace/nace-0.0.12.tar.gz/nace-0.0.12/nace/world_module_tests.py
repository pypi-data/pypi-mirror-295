import world_module


def run1_gym_world_conversion():
    # a gym world contains white space that is not there in reality. Remove it.
    # A gym world may not be surrounded by walls, add the ability to add them.
    # if walls were added the x,y location of the agent needs to be adjusted accordingly
    gym_world = " o  o  o  o  o \n o  o  x  o  o \n o  o  o  o  o"
    nace_world, xy_loc = world_module.convert_gymnasium_world_to_nace(gym_world)
    assert xy_loc == (3, 2)


if __name__ == "__main__":
    run1_gym_world_conversion()
