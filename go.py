#!/usr/bin/env python
"""
Main program, and generic search.
"""
import argparse
import time
from collections import defaultdict

from fringe import AStarFringe, BestFringe, DFSFringe, BFSFringe
from puzzle import State8Puzzle

DEFAULT_GOAL = (1, 2, 3, 8, 0, 4, 7, 6, 5)
DIFFICULTY_GOAL = (1, 2, 3, 8, 4, 0, 7, 6, 5)
DIFFICULTY_START = {
    "easy": (1, 3, 4, 8, 6, 2, 7, 5, 0),
    "medium": (2, 8, 1, 4, 3, 0, 7, 6, 5),
    "hard": (2, 8, 1, 4, 6, 3, 7, 5, 0),
    "worst": (5, 6, 7, 4, 8, 0, 3, 2, 1)
}
ALL_HEURISTICS = ["manhattan", "displaced", "invalid", "max", "linear"]
ALL_ALGORITHMS = ["astar", "best", "bfs", "dfs"]


def get_fringe(start, goal, algorithm):
    """Get fringe according to the algorithm chosen"""
    if algorithm == "astar":
        fringe = AStarFringe(start, goal)
    elif algorithm == "best":
        fringe = BestFringe(start, goal)
    elif algorithm == "bfs":
        fringe = BFSFringe(start, goal)
    elif algorithm == "dfs":
        fringe = DFSFringe(start, goal)
    else:
        raise Exception("Chosen algorithm is not implemented.")
    return fringe



def search(start, goal, algorithm):
    """Implement generic search algorithm."""
    fringe = get_fringe(start, goal, algorithm)  # open list
    visited = set()  # closed list
    while (fringe.is_not_empty()):
        current = fringe.get()

        if current.values == goal:
            return current, len(visited)

        for n in current.neighbors():
            if n.values not in visited:
                visited.add(n.values)
                fringe.put(current, n)
    raise Exception("Goal not reachable")



def reconstruct_path(node):
    """Generator to reconstruct path from the solution node to its parent."""
    while True:
        if not node:
            break
        yield node
        node = node.parent


def solve_puzzle(start_state, goal, algo):
    start = time.time()
    solution_node, visited_nodes_len = search(start_state, goal, algo)
    elapsed = (time.time() - start)
    return elapsed, list(reconstruct_path(solution_node)), visited_nodes_len


def avg(l):
    return sum(l) / len(l)


def parse_start_state(start):
    """Helper function to parse the input start state from user."""
    if len(start) != len(set(start)):
        raise argparse.ArgumentTypeError(
            "No duplicates are allowed in the start state.")
    parsed_start = []
    for p in start:
        if p.isdigit() and int(p) > 0 and int(p) < 9:
            parsed_start.append(int(p))
        elif p == 'B':
            parsed_start.append(0)
        else:
            raise argparse.ArgumentTypeError(
                'Values have to be be integers between 1 and 8, blank is represented with B.'
            )
    return tuple(parsed_start)


def get_cmd_args():
    """Helper function to get argument passed to this program."""
    parser = argparse.ArgumentParser(description='8-Puzzle Solver')

    parser.add_argument(
        '-a',
        action="store",
        dest="algorithm",
        default="astar",
        choices=ALL_ALGORITHMS,
        help="Select the algorithm you want to run. Chose between astar, best, bfs or dfs."
    )
    parser.add_argument(
        '-t',
        action="store",
        dest="heuristic",
        default="manhattan",
        choices=ALL_HEURISTICS,
        help="Select the heuristic you want to apply. Chose between manhattan, displaced, invalid, linear or max."
    )
    parser.add_argument(
        '--start',
        nargs=9,
        default=['1', '2', '3', '4', 'B', '5', '7', '6', '8'],
        help="Write the 8-Puzzle start state you would like to solve. Integers between 1 and 8, blank represented with B."
    )
    parser.add_argument(
        '-d',
        action="store",
        dest="difficulty",
        choices=["easy", "medium", "hard", "worst"],
        help="Select a predifined start state with specific difficulty. Chose between easy, medium, hard or worst."
    )
    parser.add_argument(
        "-b",
        "--benchmark",
        type=int,
        help="Select the number of loops, you want to average on. It will run all algorithms, and output results to a file.",
        action="store")
    parser.add_argument(
        "-v",
        "--verbose",
        help="Increase output verbosity. Will show the path to the goal.",
        action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_cmd_args()

    if not args.benchmark:
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
            start_state = State8Puzzle(start, None, args.heuristic)
        else:
            start_state = State8Puzzle(start, None, None)

        print "Start state is: {start}".format(start=start)
        print "Goal state is: {goal}".format(goal=goal)
        print "-------------------------------------\n"

        # Solve the puzzle
        elapsed, path, visited_nodes_len = solve_puzzle(start_state, goal, args.algorithm)

        print "{algo} - Solved in {elapsed:.4f} seconds\n".format(
            algo=args.algorithm, elapsed=elapsed)

        for count, node in enumerate(reversed(path), 1):
            if args.verbose:
                print "-------------------------------------"
                print count
                print "-------------------------------------"
                print node
                if args.algorithm == 'astar':
                    print "cost: {} total_cost: {}".format(node.cost,
                                                           node.total_cost)
                if args.algorithm == 'best':
                    print "cost: {}".format(node.cost)
        print "\n-------------------------------------"

        print "Total nodes to goal: {}".format(count)
        print "Total nodes visited: {}\n".format(visited_nodes_len)
    else:
        total_start = time.time()

        bench = defaultdict(set) # holds all results
        if args.difficulty:
            start = DIFFICULTY_START[args.difficulty]
        else:
            start = DIFFICULTY_START["worst"]
        goal = DIFFICULTY_GOAL

        for _ in xrange(args.benchmark):
            for a in ALL_ALGORITHMS:
                if a == 'astar' or a == 'best':
                    for h in ALL_HEURISTICS:
                        start_state = State8Puzzle(start, None, h)
                        elapsed, path, visited_nodes_len = solve_puzzle(start_state, goal, a)
                        bench["{}-{}".format(a, h)].add((elapsed, len(path), visited_nodes_len))
                else:
                    start_state = State8Puzzle(start, None, None)
                    elapsed, path, visited_nodes_len = solve_puzzle(start_state, goal, a)
                    bench["{}-N/A".format(a)].add((elapsed, len(path), visited_nodes_len))

        total_elapsed = (time.time() - total_start)

        with open('./benchmark_result-{}.txt'.format(time.strftime("%Y%m%d-%H%M%S")), 'w+') as f:
            f.write("Executed {} loops in {:.4f} seconds.\n".format(args.benchmark, total_elapsed))

            for k, v in sorted(bench.iteritems()):
                f.write("{}\n".format(k))
                f.write("Average time: {:.4f}\n".format(avg([x[0] for x in v])))
                f.write("Total nodes to goal: {}\n".format(avg([x[1] for x in v])))
                f.write("Total nodes visited: {}\n".format(avg([x[2] for x in v])))
