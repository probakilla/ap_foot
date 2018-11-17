import json
import sys
import cProfile
from buildGraph import buildGraphWithDictV2, buildGraphWithAdjacenyMatrix, buildGraphWithDict
from display import Display
from problem import Problem
from algo import minDominatingSet


def main(argv):
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR : NEED A JSON CONFIGURATION FILE!\n")
        sys.exit()

    problem_path = sys.argv[1]
    with open(problem_path) as problem_file:
        problem = Problem(json.load(problem_file))

    pr = cProfile.Profile()
    pr.enable()
    g = buildGraphWithDictV2(problem)
    pr.disable()
    pr.print_stats("time")
    #print(minDominatingSet(g, 10))

    # display = Display(g, True, problem)
    # display.run(True)
    return True


if __name__ == "__main__":
    main(sys.argv)
