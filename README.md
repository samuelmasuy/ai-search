#8-Puzzle Solver

##File structure

In go.py:
	Main program, and generic search.
In fringe.py:
	Fringe defintion and Fringe specific definition for each algorithm.
In puzzle.py:
	State definition, and specific puzzle state definition for 8-Puzzle
	particularly. Definition of heuristics for 8-puzzle.

##Usage

python go.py
             [-h]
			 [-a {astar,best,bfs,dfs}]
             [-t {manhattan,hamming,invalid,max}]
             [--start START START START START START START START START START]
             [-d {easy,medium,hard,worst}] [-v]

optional arguments:
  -h, --help
						show this help message and exit

  -a {astar,best,bfs,dfs}
                        Select the algorithm you want to run. Chose between
                        astar, best, bfs or dfs.

  -t {manhattan,hamming,invalid,max}
                        Select the heuristic you want to apply. Chose between
                        manhattan, hamming, invalid or max.

  -d {easy,medium,hard,worst}
                        Select a predifined start state with specific
                        difficulty. Chose between easy, medium, hard or worst.
						Note: if this option is selected, --start will be
						ignored, also goal state is set to:
						1	2	3
						8	4
						7	6	5

  --start START START START START START START START START START
                        Write the 8-Puzzle start state you would like to
                        solve. Integers between 1 and 8, blank represented
                        with B.

  -v, --verbose
						Increase output verbosity. Will show the path to the
                        goal.

##Default goal state

	1	2	3
	8		4
	7	6	5

