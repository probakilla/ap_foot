import json
import sys
import cProfile
import time
from algo.buildGraph import buildGraph, ADJACENCY, DICT, DICT_OLD
from algo.buildGraph import buildGraphTriangle
from inputOutput.display import Display, DISPLAY_GRAPH, DISPLAY_FIELD
from inputOutput.problem import Problem
from algo.algo import minDominatingSetGuillaume, minDominatingSetOkan, isDominatingSet


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("ERROR : NEED A JSON CONFIGURATION FILE!\n")
        sys.exit()

    problem_path = sys.argv[1]
    with open(problem_path) as problemFile:
        problem = Problem(json.load(problemFile))

    startTime = time.time()
    graph = buildGraphTriangle(problem)
    print("Taille du graphe : ", len(graph.graphDict))
    print("--- Build graph with dict V1 in %s seconds ---" %
          (time.time() - startTime))

    startTime = time.time()
    dominatingSet = minDominatingSetGuillaume(graph, 10)
    print("--- Find dominating set in %s seconds ---" %
          (time.time() - startTime))
    print("il faut", len(dominatingSet), "défenseurs")
    display = Display(graph, problem)

    # DISPLAY_FIELD OR DISPLAY_GRAPH
    display.run(DISPLAY_FIELD, True)

    return True


if __name__ == "__main__":
    main(sys.argv)
