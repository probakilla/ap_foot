import json
import sys

from graph import buildGraphV2, Graph
from display import Display
from problem import Problem
from algo import DSAP
from node import AtkNode, DefNode
from geometry import Point


def main(argv):
    if len(sys.argv) != 2:
        print("ERROR : NEED A JSON CONFIGURATION FILE!", file=sys.stderr)
        sys.exit()

    problem_path = sys.argv[1]
    with open(problem_path) as problem_file:
        problem = Problem(json.load(problem_file))

    g = buildGraphV2(problem)
    print(DSAP(g, 10))

    display = Display(g, True, problem)
    display.run(True)
    return True


if __name__ == "__main__":
    main(sys.argv)
