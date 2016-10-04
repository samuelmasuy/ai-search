"""
Main program, and generic search.
"""
import argparse
import time

from fringe import AStarFringe, BestFringe, DFSFringe, BFSFringe
from puzzle import State_Puzzle

DEFAULT_GOAL = (1, 2, 3, 8, 0, 4, 7, 6, 5)
DIFFICULTY_GOAL = (1, 2, 3, 8, 4, 0, 7, 6, 5)
DIFFICULTY_START = {
        "easy": (1, 3, 4, 8, 6, 2, 7, 5, 0),
        "medium": (2, 8, 1, 4, 3, 0, 7, 6, 5),
        "hard": (2, 8, 1, 4, 6, 3, 7, 5, 0),
        "worst": (5, 6, 7, 4, 8, 0, 3, 2, 1)
}


class Solver(object):
    def __init__(self, start, goal, algorithm):
        self.visited = set() # closed list
        # set fringe according to the algorithm chosen
        if algorithm == "astar":
            self.fringe = AStarFringe(start, goal)
        elif algorithm == "best":
            self.fringe = BestFringe(start, goal)
        elif algorithm == "bfs":
            self.fringe = BFSFringe(start, goal)
        elif algorithm == "dfs":
            self.fringe = DFSFringe(start, goal)

    def solve(self):
        """Implement generic search algorithm."""
        while (self.fringe.is_not_empty()):
            current = self.fringe.get()

            if self.fringe.is_goal(current):
                return current, len(self.visited)

            for n in current.neighbors():
                if n.values not in self.visited:
                    self.visited.add(n.values)
                    self.fringe.put(current, n)
        raise Exception("Goal not reachable")


def reconstruct_path(node):
    """Reconstruct path from the solution node to its parent."""
    while True:
        if not node:
            break
        yield node
        node = node.parent


def parse_start_state(start):
    """Helper function to parse the input start state from user."""
    if len(start) != len(set(start)):
        raise argparse.ArgumentTypeError("No duplicates are allowed in the start state.")
    parsed_start = []
    for p in start:
        if p.isdigit() and int(p) > 0 and int(p) < 9:
            parsed_start.append(int(p))
        elif p == 'B':
            parsed_start.append(0)
        else:
            raise argparse.ArgumentTypeError('Values have to be be integers between 1 and 8, blank is represented with B.')
    return tuple(parsed_start)


def get_cmd_args():
    """Helper function to get argument passed to this program."""
    parser = argparse.ArgumentParser(description='8-Puzzle Solver')

    parser.add_argument('-a', action="store", dest="algorithm", default="astar", choices=["astar", "best", "bfs", "dfs"],
                        help="Select the algorithm you want to run. Chose between astar, best, bfs or dfs.")
    parser.add_argument('-t', action="store", dest="heuristic", default="manhattan", choices=["manhattan", "hamming", "invalid", "max"],
                        help="Select the heuristic you want to apply. Chose between manhattan, hamming, invalid or max.")
    parser.add_argument('--start', nargs=9, default=['1', '2', '3', '4', 'B', '5', '7', '6', '8'],
                        help="Write the 8-Puzzle start state you would like to solve. Integers between 1 and 8, blank represented with B.")
    parser.add_argument('-d', action="store", dest="difficulty", choices=["easy", "medium", "hard", "worst"],
                        help="Select a predifined start state with specific difficulty. Chose between easy, medium, hard or worst.")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity. Will show the path to the goal.", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_cmd_args()

    if args.difficulty:
        start = DIFFICULTY_START[args.difficulty]
        goal = DIFFICULTY_GOAL
    else:
        start = parse_start_state(args.start)
        goal = DEFAULT_GOAL
    print "Solving using: {algo} ".format(algo=args.algorithm)

    # define start state node
    if args.algorithm == 'astar' or args.algorithm == 'best':
        print "Using Heuristic: {heuristic}".format(heuristic=args.heuristic)
        start_state = State_Puzzle(start, None, args.heuristic)
    else:
        start_state = State_Puzzle(start, None, None)

    print "Start state is: {start}".format(start=start)
    print "Goal state is: {goal}".format(goal=goal)
    print "-------------------------------------\n"

    # define solver, and solve the puzzle
    solver = Solver(start_state, goal, args.algorithm)
    start = time.time()
    solution_node, visited_nodes_len = solver.solve()
    elapsed = (time.time() - start)

    print "{algo} - Solved in {elapsed:.4f} seconds\n".format(algo=args.algorithm, elapsed=elapsed)

    for count, node in enumerate(reconstruct_path(solution_node), 1):
        if args.verbose:
            print "-------------------------------------"
            print count
            print "-------------------------------------"
            print node
            if args.algorithm == 'astar':
                print "cost: {} total_cost: {}".format(node.cost, node.total_cost)
            if args.algorithm == 'best':
                print "cost: {}".format(node.cost)
    print "\n-------------------------------------"

    print "Total nodes to goal: {}".format(count)
    print "Total nodes visited: {}\n".format(visited_nodes_len)
