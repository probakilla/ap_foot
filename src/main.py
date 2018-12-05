import json
import sys
import cProfile
import time
from algo.buildGraph import buildGraph, ADJACENCY, DICT, DICT_OLD, buildGraphTriangles
from inputOutput.display import Display, DISPLAY_GRAPH, DISPLAY_FIELD
from inputOutput.problem import Problem
from algo.algo import minDominatingSetGuillaume, minDominatingSetOkan, isDominatingSet, greedyMinDominatingSet


def main(argv):
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR : NEED A JSON CONFIGURATION FILE!\n")
        sys.exit()

    problem_path = sys.argv[1]
    with open(problem_path) as problem_file:
        problem = Problem(json.load(problem_file))

    startTime = time.time()
    g = buildGraphTriangles(problem)
    print("Taille du graphe : ", len(g.graphDict))
    print("--- Build graph with dict in %s seconds ---" % (time.time() - startTime))
    
    startTime = time.time()
    greedyDominatingSet = greedyMinDominatingSet(g, 3)
    print("--- Find dominating set with greedy in %s seconds ---" % (time.time() - startTime))
    print("il faut ", len(greedyDominatingSet) ," defenseurs d'apres greedy")
    displayGreedy = Display(g, problem, greedyDominatingSet)
    # DISPLAY_FIELD OR DISPLAY_GRAPH
    displayGreedy.run(DISPLAY_FIELD)

    return True


if __name__ == "__main__":
    main(sys.argv)
