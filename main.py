import sys
from graph import buildGraph


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR : NEED A JSON CONFIGURATION FILE!", file=sys.stderr)
        sys.exit()
    graph = buildGraph(sys.argv[1])
