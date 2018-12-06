import json
import sys
import cProfile
import time
<<<<<<< HEAD
from algo.buildGraph import buildGraph, ADJACENCY, DICT, DICT_OLD
from algo.buildGraph import buildGraphTriangles
from inputOutput.display import Display, DISPLAY_GRAPH, DISPLAY_FIELD
from inputOutput.problem import Problem
from algo.algo import minDominatingSetGuillaume, minDominatingSetOkan
from algo.algo import isDominatingSet, buildGraphWithDict
=======
from algo.buildGraph import buildGraph, ADJACENCY, DICT, DICT_OLD, buildGraphTriangles
from inputOutput.display import Display, DISPLAY_GRAPH, DISPLAY_FIELD
from inputOutput.problem import Problem
from algo.algo import minDominatingSetGuillaume, minDominatingSetOkan, isDominatingSet, greedyMinDominatingSet
>>>>>>> 7238f1c2b531e0417ca96e7ebd56807d927d63c2


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("ERROR : NEED A JSON CONFIGURATION FILE!\n")
        sys.exit()

    problem_path = sys.argv[1]
<<<<<<< HEAD
    with open(problem_path) as problemFile:
        problem = Problem(json.load(problemFile))

    startTime = time.time()
    graph = buildGraphWithDict(problem)
    print("Taille du graphe : ", len(graph.graphDict))
    print("--- Build graph with dict V1 in %s seconds ---" %
          (time.time() - startTime))

    startTime = time.time()
    dominatingSet = minDominatingSetGuillaume(graph, 10)
    print("--- Find dominating set in %s seconds ---" %
          (time.time() - startTime))
    print("il faut", len(dominatingSet), "défenseurs")
=======
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
>>>>>>> 7238f1c2b531e0417ca96e7ebd56807d927d63c2

    display = Display(graph, problem)
    display.run(DISPLAY_FIELD, True)
    return True


if __name__ == "__main__":
    main(sys.argv)
