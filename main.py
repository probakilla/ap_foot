import sys

from graph import buildGraph, searchDominatingSet


def main(argv):
    if len(sys.argv) != 2:
        print("ERROR : NEED A JSON CONFIGURATION FILE!", file=sys.stderr)
        sys.exit()
    g = buildGraph(argv[1])
    print (searchDominatingSet(g, 3))
    print(g)
    return True


if __name__ == "__main__":
    main(sys.argv)
