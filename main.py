import sys

from graph import buildGraph, searchDominatingSet


def main(argv):
    if len(sys.argv) != 2:
        print("ERROR : NEED A JSON CONFIGURATION FILE!", file=sys.stderr)
        sys.exit()
    g = buildGraph(argv[1])
    searchDominatingSet(g)
    print(g)
    return True


if __name__ == "__main__":
    main(sys.argv)
