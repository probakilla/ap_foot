''' Entry point of the program '''

import json
import sys
import time
from algo.buildGraph import buildGraph, ADJACENCY
from inputOutput.display import Display, DISPLAY_FIELD
from inputOutput.problem import Problem

def main(argv):
    ''' Entry point of the program '''
    if len(argv) != 2:
        sys.stderr.write("ERROR : NEED A JSON CONFIGURATION FILE!\n")
        sys.exit()

    problemPath = sys.argv[1]
    with open(problemPath) as problemFile:
        problem = Problem(json.load(problemFile))

    startTime = time.time()
    graph = buildGraph(problem, ADJACENCY)
    print("Taille du graphe : ", len(graph.listNode))
    print("--- Build graph with dict V1 in %s seconds ---" %
          (time.time() - startTime))

    display = Display(graph, problem)
    display.run(DISPLAY_FIELD, True)
    return True


if __name__ == "__main__":
    main(sys.argv)
