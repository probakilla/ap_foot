import sys
from graph import buildGraph


def main(argv):
    if len(sys.argv) != 2:
        print("ERROR : NEED A JSON CONFIGURATION FILE!", file=sys.stderr)
        sys.exit()
    graph = buildGraph(argv[1])
    print(graph)
    return True


if __name__ == "__main__":
    main(sys.argv)
