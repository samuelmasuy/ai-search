"""
Fringe defintion and Fringe specific definition for each algorithm.
"""
from collections import deque
from Queue import PriorityQueue


class Fringe(object):
    """Define base operation of the fringe"""

    def __init__(self, goal, fringe):
        self.fringe = fringe
        self.goal = goal

    def is_not_empty(self):
        """Check if the fringe is not empty"""
        pass

    def get(self):
        """Get first element of the fringe."""
        pass

    def put(self, parent, child):
        """Add element to the fringe."""
        pass

    def is_goal(self, n):
        """Check if n is the goal state."""
        return n.values == self.goal


class AStarFringe(Fringe):
    """
    Define fringe for a* algorithm.
    We use a PriorityQueue as the fringe data structure.
    """

    def __init__(self, start, goal):
        super(AStarFringe, self).__init__(goal, PriorityQueue())
        start.cost = start.h(self.goal)
        start.total_cost = 0
        self.fringe.put((start.cost, start))

    def is_not_empty(self):
        return self.fringe.qsize() != 0

    def get(self):
        return self.fringe.get()[1]

    def put(self, parent, child):
        # get heuristic value
        child.cost = child.h(self.goal)
        child.total_cost = child.cost + child.parent.total_cost
        self.fringe.put((child.total_cost, child))


class BestFringe(Fringe):
    """
    Define fringe for best first search algorithm.
    We use a PriorityQueue as the fringe data structure.
    """

    def __init__(self, start, goal):
        super(BestFringe, self).__init__(goal, PriorityQueue())
        start.cost = start.h(self.goal)
        self.fringe.put((start.cost, start))

    def is_not_empty(self):
        return self.fringe.qsize() != 0

    def get(self):
        return self.fringe.get()[1]

    def put(self, parent, child):
        child.cost = child.h(self.goal)
        self.fringe.put((child.cost, child))


class DFSFringe(Fringe):
    """
    Define fringe for depth first search algorithm.
    We use a deque as the fringe data structure.
    """

    def __init__(self, start, goal):
        super(DFSFringe, self).__init__(goal, deque())
        self.fringe.append(start)

    def is_not_empty(self):
        return len(self.fringe) != 0

    def get(self):
        return self.fringe.popleft()

    def put(self, parent, child):
        self.fringe.appendleft(child)  # prepend element to the deque.


class BFSFringe(Fringe):
    """
    Define fringe for breath first search algorithm.
    We use a deque as the fringe data structure.
    """

    def __init__(self, start, goal):
        super(BFSFringe, self).__init__(goal, deque())
        self.fringe.append(start)

    def is_not_empty(self):
        return len(self.fringe) != 0

    def get(self):
        return self.fringe.popleft()

    def put(self, parent, child):
        self.fringe.append(child)
