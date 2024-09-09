import copy

import numpy as np

import nace.color_codes

UNOBSERVED_BOARD_VALUE = '.'


class NPWorld():

    def __init__(self, with_observed_time, name, width=None, height=None, initial_value=ord(UNOBSERVED_BOARD_VALUE),
                 view_dist_x=3, view_dist_y=2):
        self.name = name
        if width is None or height is None:
            self.board = np.zeros((0, 0), dtype=int)
        else:
            self.board = np.zeros((width, height), dtype=int)
            self.board[:] = initial_value

        self.initial_value = initial_value
        self.with_observed_time = with_observed_time

        self.times = np.zeros((0, 0), dtype=np.float16)  # this seems expensive in space, a float16 for each cell. hmmm
        self.times[:] = float('-inf')
        self.agent_location_column = -1
        self.agent_location_row = -1
        self.view_dist_x = view_dist_x
        self.view_dist_y = view_dist_y
        self.debug_board = ""

    def get_char_at(self, row, col):
        return chr(self.board[row, col])

    def set_char_at(self, row, col, c, location_indicator_char='x'):
        self.board[row, col] = ord(c)
        if c == location_indicator_char:
            self.agent_location_column = col
            self.agent_location_row = row

    def get_time_at(self, row, col):
        return self.times[row, col]

    def get_newest_time(self):
        """
        @return: the must recent, up-to-date time stored in the world.
        """
        if self.with_observed_time:
            if self.times.shape[0] > 0:
                return self.times.max()
        return 0

    def get_board_line(self, row_number, color):
        if self.with_observed_time and self.times.size > 0:
            oldest_time = self.times.min().item()
        else:
            oldest_time = float('-inf')
        line = ""
        color_count = 0
        if row_number < self.board.shape[0]:
            for col in range(self.board.shape[1]):
                if self.with_observed_time and self.times[row_number][col] == oldest_time:
                    line += nace.color_codes.color_code_black_on_white
                    color_count += 1
                line += chr(self.board[row_number, col])

                if self.with_observed_time and self.times[row_number][col] == oldest_time:
                    if color != None:
                        line += color
        return line, self.board.shape[1]

    def get_in_nace_board_format(self):
        board = []
        for row in range(self.board.shape[0]):
            line = []
            for col in range(self.board.shape[1]):
                line.append(chr(self.board[row, col]))
            board.append(line)
        return board

    def _reset_non_board(self):
        # set the times and other values to the default
        if self.with_observed_time:
            self.times = np.zeros(self.board.shape, dtype=np.float16)  # this seems expensive in space. hmmm
            self.times[:] = float('-inf')
        self.agent_location_column = -1
        self.agent_location_row = -1

    def update_world_from_ground_truth_gymnasium_format(
            self,
            gym_world: str,
            strip_blanks=True,
            location_indicator_char='x',
            add_surrounding_walls=True,
            wall_code='W',
            time_counter: float = float('-inf')):
        """

        Convert a world in gym format, into a numpy one (via the nace format)

        @param gym_world: str , each \n indicates a new row, white space is stripped. agent location indicated by  location_indicator_char
        @param strip_blanks:
        @param location_indicator_char:  char representing the agent
        @param last_world: if not none, state and times seen copied from this world
        @param add_walls_right_and_bottom:
        @param wall_code:
        @return: the location of last agent seen
        """
        list_of_list_of_str = []  # list of rows. Each row is a list of char.
        for row_number, row_str in enumerate(gym_world.split("\n")):
            if len(row_str.strip()) > 0:
                if strip_blanks:
                    list_of_list_of_str.append([c for c in list(row_str) if c != " "])
                else:
                    list_of_list_of_str.append(list(row_str))

        if add_surrounding_walls:
            for row in list_of_list_of_str:
                row.append(wall_code)
                row.insert(0, wall_code)
            extra_line = [wall_code for _ in row]
            list_of_list_of_str.append(extra_line)
            list_of_list_of_str.insert(0, extra_line)

        # check the sizes are correct, and see where location marker is
        for row_number in range(len(list_of_list_of_str)):
            if row_number > 0:
                assert len(list_of_list_of_str[0]) == len(list_of_list_of_str[row_number])

        # the next line returns the xy location of last agent seen, modified count, and pre-action world
        return self.update_world_from_ground_truth_nace_format(list_of_list_of_str, time_counter=time_counter,
                                                               location_indicator_char=location_indicator_char)

    def _set_board_size(self, height, width):
        prior_board_shape = self.board.shape
        size_changed = False
        if prior_board_shape == (0, 0):
            # we need to reset all other values
            self.board = np.zeros((height, width), dtype=int)
            self.board[:] = self.initial_value
            self._reset_non_board()
            size_changed = True

        return prior_board_shape, size_changed

    def update_world_from_ground_truth_nace_format(
            self,
            nace_format_world_list_of_list_of_str,  # just the board
            location_indicator_char='x',
            time_counter=float('-inf'),
            times_list_of_str=None
    ):
        """
        Update the board with the values passed in when the passed in value is not the unobserved marker
        The time the update happened is written to the times array.

        @param nace_format_world_list_of_list_of_str:
        @param location_indicator_char:
        @param unobserved_indicator_char:
        @param time_counter:
        @return:
        """

        prior_board_shape, size_changed = self._set_board_size(
            height=len(nace_format_world_list_of_list_of_str),
            width=len(nace_format_world_list_of_list_of_str[0]))

        pre_update_world = copy.deepcopy(self)

        location_column = None
        location_row = None
        modified_count = 0

        # find the agents location (assumes only one agent)
        for row_number in range(len(nace_format_world_list_of_list_of_str)):
            for col_number in range(len(nace_format_world_list_of_list_of_str[row_number])):
                c = nace_format_world_list_of_list_of_str[row_number][col_number]
                if c == location_indicator_char:
                    location_column = col_number
                    location_row = row_number

        # iterate only over the observable rows and columns,
        # updating board and times if they are inside the view distance
        for y_delta in range(self.view_dist_y * 2 + 1):
            row_number = location_row + y_delta - self.view_dist_y
            if row_number >= 0 and row_number < self.board.shape[0]:
                for x_delta in range(self.view_dist_x * 2 + 1):
                    col_number = location_column + x_delta - self.view_dist_x
                    if col_number >= 0 and col_number < self.board.shape[1]:
                        c = nace_format_world_list_of_list_of_str[row_number][col_number]
                        if ord(c) != self.initial_value:
                            if self.board[row_number][col_number] != ord(c):
                                self.board[row_number][col_number] = ord(c)
                                modified_count += 1
                            if self.with_observed_time:
                                self.times[row_number][col_number] = float(time_counter)
                        else:  # unobserved
                            pass  # leave the observed time, and board value as they are.

        if self.with_observed_time:
            if times_list_of_str is not None:
                # set the times even though assumed to be only for testing
                print("WARN: setting observation times. This code path should only be triggered in unit tests")
                for row_number in range(len(times_list_of_str)):
                    times = times_list_of_str[row_number].split(",")
                    for col_number in range(len(times)):
                        s = times[col_number].strip()
                        if s != '':
                            self.times[row_number][col_number] = float(s)

        if prior_board_shape != (0, 0):
            if prior_board_shape != self.board.shape:
                raise Exception("Changing board size/shape in flight not yet supported.")
        if location_column is not None and location_row is not None:
            self.agent_location_column = location_column
            self.agent_location_row = location_row

        self.debug_board = self.board_as_string()

        return (location_column, location_row), modified_count, pre_update_world

    def update_world_from_ground_truth(self, time_counter, external_ground_truth_world_model, xy_locations,
                                       location_indicator_char='x'):

        # todo should we pass xy_loc in here? or calculate it? or use the stored version?
        height = external_ground_truth_world_model.board.shape[0]
        width = external_ground_truth_world_model.board.shape[1]

        self._set_board_size(
            height=height,
            width=width)

        pre_action_internal_world = copy.deepcopy(self)

        # for Y in range(height): this was present in the old code
        #     for X in range(width):
        #         if observed_world[TIMES][Y][X] == Time:
        #             observed_world[TIMES][Y][
        #                 X] = Time - 1  # WHY can this ever happen??? DEBUG! it can happen if this routine is called twice in a row.
        modified_count = 0
        for y_delta in range(self.view_dist_y * 2 + 1):
            for x_delta in range(self.view_dist_x * 2 + 1):
                for xy_loc in xy_locations:
                    y = xy_loc[1] + y_delta - self.view_dist_y
                    x = xy_loc[0] + x_delta - self.view_dist_x
                    if y >= 0 and y < height and \
                            x >= 0 and x < width:
                        if external_ground_truth_world_model.board[y][x] != ord(UNOBSERVED_BOARD_VALUE):
                            if self.board[y][x] != external_ground_truth_world_model.board[y][x]:
                                self.board[y][x] = external_ground_truth_world_model.board[y][x]
                                modified_count += 1

                            if self.with_observed_time:
                                self.times[y][x] = time_counter
                        if chr(self.board[y][x]) == location_indicator_char:
                            self.agent_location_column = x
                            self.agent_location_row = y

        if modified_count == 0:
            pass
        self.debug_board = self.board_as_string()
        return modified_count, pre_action_internal_world

    def get_agent_xy_location(self):  # note there may be more than 1 agent at some stage.
        return (self.agent_location_column, self.agent_location_row)

    def get_list_of_differences(self, world2):
        differences = self.board != world2.board
        (row_indexes, column_indexes) = np.nonzero(
            differences)  # return 2 vectors, with all the y values in one, and x in the other
        return row_indexes, column_indexes

    def get_board_hashcode(self):
        """
        Note this may return different hashes on different runs. To Be Checked
        @return:
        """
        return hash(bytes(self.board.data))

    def get_height_width(self):
        return self.board.shape[0], self.board.shape[1]

    def get_board_char_counts(self):
        result = {}
        unique_values = np.unique(self.board)
        for v in unique_values:
            s = np.sum(self.board == v)
            result[chr(v)] = s.item()
        return result

    def multiworld_print(self, list_of_records, pad_length=30):
        """
        Print a number of worlds in coloured text, left to right across the screen
        @param list_of_worlds: dict e.g. [{"World":list[list[char]], "Caption":str, "Color":color code}]
        @return:
        """
        height = [record["World"].get_height_width()[0] for record in list_of_records]
        max_lines = max(height)

        for caption_line in range(3):
            line = ""
            for world_index in range(len(list_of_records)):
                caption = ""
                if "Caption" in list_of_records[world_index]:
                    caption_list = list_of_records[world_index]["Caption"].split("\n")
                    caption_list.extend(["", "", ""])
                    caption = caption_list[caption_line]
                line += caption.ljust(pad_length, " ")
            print(line)

        for line_num in range(max_lines):
            line = ""
            for world_index in range(len(list_of_records)):
                pass
                # Set the color
                color = None
                if "Color" in list_of_records[world_index]:
                    color = list_of_records[world_index]["Color"]
                    line += color
                map_line, row_length = list_of_records[world_index]["World"].get_board_line(line_num, color)
                line += map_line
                line += nace.color_codes.color_code_black_on_white

                padding = "".join([" "] * (pad_length - row_length))
                line += padding
                # line += map_line.ljust(pad_length, " ")[len(map_line):]
            print(line)
        pass

    def board_as_string(self):
        result = ""
        for row_number in range(self.board.shape[0]):
            for col_number in range(self.board.shape[1]):
                result += chr(self.board[row_number, col_number])
            result += "\n"
        return result

    def to_string_list(self):
        board_lines = []
        time_lines = []
        for row_number in range(self.board.shape[0]):
            board_line = ""
            time_line = ""
            for col_number in range(self.board.shape[1]):
                c = chr(self.board[row_number][col_number])
                board_line += c
                t = self.times[row_number][col_number]
                if t == float("-inf"):
                    time_line += "-inf,"
                else:
                    time_line += str(t) + ","
            board_lines.append(board_line)
            time_lines.append(time_line)
        return ([board_lines, (), time_lines])

    @staticmethod
    def from_string_list(str_list: str, location_indicator_char="x", unobserved_indicator_char='.', view_dist_x=3,
                         view_dist_y=2):
        world = NPWorld(with_observed_time=True, name="from_string()", initial_value=ord(unobserved_indicator_char),
                        view_dist_x=view_dist_x, view_dist_y=view_dist_y)
        board_list_of_str = str_list[0]
        times_list_of_str = str_list[2]
        world.update_world_from_ground_truth_nace_format(
            board_list_of_str,
            time_counter=float('-inf'),  # -inf == never seen
            location_indicator_char=location_indicator_char,
            times_list_of_str=times_list_of_str)

        return world
