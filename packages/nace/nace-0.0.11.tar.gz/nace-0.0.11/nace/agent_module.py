import copy


class Agent():
    """
    Holds the state of the agent, including location, and 'internal' arbitrary values (num keys held)
    """

    def __init__(self, xy_loc, score, values_exc_score):
        self.xy_loc = xy_loc
        self.values = [score] + list(values_exc_score)

    def set_xy_loc(self, xy_loc):
        self.xy_loc = xy_loc

    def get_xy_loc(self):
        return copy.deepcopy(self.xy_loc)

    def set_score(self, score):
        self.values[0] = score

    def get_score(self):
        return self.values[0]

    def get_values_exc_score(self):
        # adding anything here may explode the size of the planning space.
        return copy.deepcopy(self.values[1:])

    def get_values_inc_score(self):
        # extending the length of the values may explode the size of the planning space.
        return copy.deepcopy(self.values)

    def set_values_inc_score(self, values):
        self.values = list(copy.deepcopy(values))

    def increment_values_including_score(self, values):
        for i in range(len(values)):
            if i < len(self.values):
                if values[i] > 0:
                    pass
                self.values[i] += values[i]
