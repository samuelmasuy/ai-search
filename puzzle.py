"""
State definition, and specific puzzle definition for 8-Puzzle.
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
            self.heuristic = parent.heuristic
        else:
            self.heuristic = heuristic

    def neighbors(self):
        """Find all neighbors of a state."""
        pass

    def h(self, goal):
        """Compute heuristic of state from the goal"""
        pass


class State_Puzzle(State):
    """
    8-Puzzle specific state. Defines rules of 8-Puzzle, and some heuristics.
    """

    def __init__(self, values, parent, heuristic=None):
        super(State_Puzzle, self).__init__(values, parent, heuristic)
        # add heuristic here.
        if self.heuristic == "manhattan":
            self.h = self.manhattan_heuristic
        elif self.heuristic == "hamming":
            self.h = self.hamming_heuristic
        elif self.heuristic == "invalid":
            self.h = self.invalid_heuristic
        elif self.heuristic == "max":
            self.h = self.max_heuristic

    def h(self, goal):
        return 0

    def neighbors(self):
        """
        Return children states where a valid move is possible.
        Note: The child state includes the move.
        """
        res = []
        ind = self.values.index(0)
        if not self.is_top(ind):
            res.append(State_Puzzle(self._move_up(self.values, ind), self))
        if not self.is_bottom(ind):
            res.append(State_Puzzle(self._move_down(self.values, ind), self))
        if not self.is_left(ind):
            res.append(State_Puzzle(self._move_left(self.values, ind), self))
        if not self.is_right(ind):
            res.append(State_Puzzle(self._move_right(self.values, ind), self))
        return res

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
        The Manhattan Distance is the distance between two points measured along axes at right angles.
        """
        return sum(abs(a - b) for a, b in zip(self.values, goal))

    def hamming_heuristic(self, goal):
        """
        Compute hamming heuristic (Misplaced tiles).
        Number of tiles that are not in the final position (not counting the blank)
        """
        return sum(c1 != c2 for c1, c2 in zip(self.values, goal))

    def invalid_heuristic(self, goal):
        """
        Multiplying an admissible heuristic by a large enough constant K will
        make a heuristic inadmissible. For example, making K approach infinity
        will result in A* acting like greedy search. The performance will thus
        be better every time greedy search works better than A*. An example
        is where there are many proofs of equal length, where there appears
        to be no initial headway. In this case, greedy will find a solution
        fast (sometimes even an optimal solution), while A* can take a very
        long time!

        Also, in this case the heuristic is inadmissible because h(goal) != 0
        """
        K = 8888888
        return self.hamming_heuristic(goal) + K * K

    def max_heuristic(self, goal):
        """
        Compute max between the manhattan heuristic and the hamming heuristic.
        Combining heuristics can achieve higher accuracy.
        """
        return max(
            self.manhattan_heuristic(goal), self.hamming_heuristic(goal))

    #####################################################################
    # The following private methods (starting with _) are an adaptation #
    # from: http://stackoverflow.com/a/25956328                         #
    # The purpose of this code is to define the rules of a 8*8 grid.    #
    # I borrowed this code to have a more efficient way and quicker     #
    # way to check the neighbors in a grid using the python's tuple     #
    # data structure.                                                   #
    # My original consisted of making the tuple representing the grid   #
    # a 2-D array, checking if the move is valid, make the move,        #
    # convert it back to 1-D array and then transforming the array to a #
    # tuple.                                                            #
    # Instead this solution is only focusing on the index of the tuple. #
    #####################################################################
    def is_top(self, ind):
        return ind < 3

    def is_bottom(self, ind):
        return ind > 5

    def is_left(self, ind):
        return ind in [0, 3, 6]

    def is_right(self, ind):
        return ind in [2, 5, 8]

    def _move_up(self, p, ind):
        """exchange blank position with the tile above """
        _p = list(p)
        _p[ind], _p[ind - 3] = _p[ind - 3], _p[ind]
        return tuple(_p)

    def _move_down(self, p, ind):
        """exchange blank position with the tile below"""
        _p = list(p)
        _p[ind], _p[ind + 3] = _p[ind + 3], _p[ind]
        return tuple(_p)

    def _move_left(self, p, ind):
        """exchange blank position with the tile on the left"""
        _p = list(p)
        _p[ind], _p[ind - 1] = _p[ind - 1], _p[ind]
        return tuple(_p)

    def _move_right(self, p, ind):
        """exchange blank position with the tile on the right"""
        _p = list(p)
        _p[ind], _p[ind + 1] = _p[ind + 1], _p[ind]
        return tuple(_p)
