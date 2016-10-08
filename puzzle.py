"""
State definition, and specific puzzle state definition for 8-Puzzle
articularly. Definition of heuristics for 8-puzzle.
"""
import math


class State(object):
    """
    Base state, that defines heuristic use and the method that a State
    need to implement.
    """

    def __init__(self, values, parent, heuristic=None):
        self.parent = parent
        self.values = values
        self.cost = None
        self.total_cost = None
        if parent:
            # make sure the heuristic propagates to the child
            self.heuristic = parent.heuristic
        else:
            self.heuristic = heuristic

    def neighbors(self):
        """Generate all neighbors of a state."""
        pass

    def h(self, goal):
        """Compute heuristic of state from the goal"""
        pass


class State8Puzzle(State):
    """
    8-Puzzle specific state. Defines rules of 8-Puzzle, and some heuristics.
    """

    def __init__(self, values, parent, heuristic=None):
        super(State8Puzzle, self).__init__(values, parent, heuristic)
        # add heuristic here.
        if self.heuristic == "manhattan":
            self.h = self.manhattan_heuristic
        elif self.heuristic == "displaced":
            self.h = self.displaced_heuristic
        elif self.heuristic == "invalid":
            self.h = self.invalid_heuristic
        elif self.heuristic == "max":
            self.h = self.max_heuristic
        elif self.heuristic == "linear":
            self.h = self.linear_conflict

    def h(self, goal):
        return 0

    def neighbors(self):
        """
        Generator that generates the children states where a valid move is possible.
        Note: The child state includes the move.
        """
        index = self.values.index(0)
        if not _is_top(index):
            yield State8Puzzle(_move_up(self.values, index), self)
        if not _is_bottom(index):
            yield State8Puzzle(_move_down(self.values, index), self)
        if not _is_left(index):
            yield State8Puzzle(_move_left(self.values, index), self)
        if not _is_right(index):
            yield State8Puzzle(_move_right(self.values, index), self)

    def __str__(self):
        """
        Define the representation (string) of a state.
        We chose to representate the state, as it would look in real life.
        """
        ret = ""
        cells = int(math.sqrt(len(self.values)))
        for count, val in enumerate(self.values):
            if val == 0:
                val = "B"
            if (count + 1) % cells > 0:
                ret += " %s |" % val
            else:
                ret += " %s\n" % val
        return ret

    def manhattan_heuristic(self, goal):
        """
        Compute manhattan heuristic.
        The Manhattan Distance is the distance between two points measured
        along axes at right angles.
        """
        return sum(abs(a - b) for a, b in zip(self.values, goal) if a != 0)

    def displaced_heuristic(self, goal):
        """
        Compute displaced tiles heuristic (Hammming distance).
        Number of tiles that are not in the final position (not counting the blank)
        """
        return sum(a != b for a, b in zip(self.values, goal) if a != 0)

    def invalid_heuristic(self, goal):
        """
        Invalid Heuristic: Variant of Nilsson's Sequence Score.
        h(n) = P(n) + kS(n)
        P(n): the Manhattan Distance of each tile from its proper position.
        S(n): the sequence score obtained by checking around the non-central
        (goal blank tile) tiles in turn, allotting 2 for every tile not
        followed by its proper successor and 1 in case that the center is not empty.
        k: constant
        """
        k = 88
        s = 0
        goal_blank_index = goal.index(0)
        start_blank_index = goal.index(0)

        if goal_blank_index != start_blank_index:
            s += 1

        for i in xrange(len(self.values)):
            # Check central square.
            if i == start_blank_index:
                continue

            if i == len(self.values) - 1:
                if self.values[0] != goal[0]:
                    s += 2
                continue

            if self.values[i + 1] != goal[i + 1]:
                s += 2

        return self.manhattan_heuristic(goal) + k * s

    def max_heuristic(self, goal):
        """
        Compute max between the manhattan heuristic and the displaced heuristic.
        Combining heuristics can achieve higher accuracy.
        """
        return max(
            self.manhattan_heuristic(goal), self.displaced_heuristic(goal))

    def linear_conflict(self, goal):
        """
        Linear conflict heuristic, one tile must move up or down to allow the other to
        pass by and then back up add two moves to the manhattan distance.
        """
        return sum(
            self.manhattan_heuristic(goal),
            self._vertical_linear_conflict(goal),
            self._horizontal_linear_conflict(goal))

    def _vertical_linear_conflict(self, goal):
        conflict = 0

        for row in xrange(3):
            max_val = -1
            for column in xrange(3):
                cell_value = _get_cell_value(self.values, row, column)
                # Is the tile in its goal row?
                if cell_value != 0 and cell_value in _get_range_goal_row_values(goal, row):
                    if (cell_value > max_val):
                        max_val = cell_value
                    else:
                        # The linear conflict adds at least two moves to the Manhattan Distance
                        # of the two conflicting tiles, by forcing them to surround one another.
                        conflict += 2
        return conflict

    def _horizontal_linear_conflict(self, goal):
        conflict = 0
        for row in xrange(3):
            max_val = -1
            for column in xrange(3):
                cell_value = _get_cell_value(self.values, row, column)
                # Is the tile in its goal column?
                if cell_value != 0 and _get_range_goal_column_values(goal, column):
                    if (cell_value > max_val):
                        max_val = cell_value
                    else:
                        # The linear conflict adds at least two moves to the Manhattan Distance
                        # of the two conflicting tiles, by forcing them to surround one another.
                        conflict += 2
        return conflict


def _get_cell_value(s, row, column):
    """Helper function to get value in 1-D array (s), given row and column"""
    return s[row * 3 + column]


def _get_range_goal_row_values(goal, row):
    """Helper function to get set of values of row in 1-D array, given a row index"""
    return goal[row * 3:row * 3 + 3]


def _get_range_goal_column_values(goal, column):
    """Helper function to get set of values of row in 1-D array, given a row index"""
    return goal[column:column + 1] + goal[column + 3:column + 4] + goal[column + 6:column + 7]


#############################################################
# The purpose of the following functions is to define the   #
# rules of a 8Puzzle grid.                                  #
# This solution is only focusing on the index of the tuple, #
# and therefore not applicable to other kind of grid.       #
#############################################################
def _is_top(index):
    return index < 3


def _is_bottom(index):
    return index > 5


def _is_left(index):
    return index in (0, 3, 6)


def _is_right(index):
    return index in (2, 5, 8)


def _move_up(p, index):
    """exchange blank position with the tile above """
    _p = list(p)
    _p[index], _p[index - 3] = _p[index - 3], _p[index]
    return tuple(_p)


def _move_down(p, index):
    """exchange blank position with the tile below"""
    _p = list(p)
    _p[index], _p[index + 3] = _p[index + 3], _p[index]
    return tuple(_p)


def _move_left(p, index):
    """exchange blank position with the tile on the left"""
    _p = list(p)
    _p[index], _p[index - 1] = _p[index - 1], _p[index]
    return tuple(_p)


def _move_right(p, index):
    """exchange blank position with the tile on the right"""
    _p = list(p)
    _p[index], _p[index + 1] = _p[index + 1], _p[index]
    return tuple(_p)
