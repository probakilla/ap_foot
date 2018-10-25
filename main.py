import sys

from graph import buildGraph, searchDominatingSet
from inputOutput import graphToJson
from display import Display


def main(argv):
    if len(sys.argv) != 2:
        print("ERROR : NEED A JSON CONFIGURATION FILE!", file=sys.stderr)
        sys.exit()
    g = buildGraph(argv[1])

    display = Display(g, 0.2, True, argv[1])
    display.run()
    return True


if __name__ == "__main__":
    main(sys.argv)
