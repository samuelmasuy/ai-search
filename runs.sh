python ./go.py -a astar -t manahattan -d worst
python ./go.py -a astar -t displaced -d worst
python ./go.py -a astar -t max -d worst
python ./go.py -a astar -t linear -d worst
python ./go.py -a astar -t invalid -d worst
python ./go.py -a best -t manahattan -d worst
python ./go.py -a best -t displaced -d worst
python ./go.py -a best -t max -d worst
python ./go.py -a best -t linear -d worst
python ./go.py -a best -t invalid -d worst
python ./go.py -a dfs -d worst
python ./go.py -a bfs -d worst

# Include path to goal (verbose)
python ./go.py -a astar -t manahattan -d worst -v
