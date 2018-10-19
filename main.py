import sys
from graph import buildGraph, rotate
from node import Point

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR : NEED A JSON CONFIGURATION FILE!", file=sys.stderr)
        sys.exit()

    graph = buildGraph(sys.argv[1])

print(rotate(Point(0, 0), Point(0, 5), 90))
