#!/bin/bash
for i in `seq 1 6`;
do
	python ./go.py -a astar -t manhattan -d worst
	python ./go.py -a astar -t displaced -d worst
	python ./go.py -a astar -t max -d worst
	python ./go.py -a astar -t linear -d worst
	python ./go.py -a astar -t invalid -d worst
	python ./go.py -a best -t manhattan -d worst
	python ./go.py -a best -t displaced -d worst
	python ./go.py -a best -t max -d worst
	python ./go.py -a best -t linear -d worst
	python ./go.py -a best -t invalid -d worst
	python ./go.py -a dfs -d worst
	python ./go.py -a bfs -d worst
done

# Include path to goal (verbose)
# python ./go.py -a astar -t manahattan -d worst -v
