import json
import sys

from graph import buildGraph
from display import Display
from problem import Problem


def main(argv):
    if len(sys.argv) != 2:
        print("ERROR : NEED A JSON CONFIGURATION FILE!", file=sys.stderr)
        sys.exit()

    problem_path = sys.argv[1]
    with open(problem_path) as problem_file:
        problem = Problem(json.load(problem_file))

    g = buildGraph(problem)

    display = Display(g, True, argv[1])
    display.run()

    return True


if __name__ == "__main__":
    main(sys.argv)
