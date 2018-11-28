import json
import sys
import cProfile
import time
from algo.buildGraph import buildGraph, ADJACENCY, DICT, DICT_OLD
from inputOutput.display import Display, DISPLAY_GRAPH, DISPLAY_FIELD
from inputOutput.problem import Problem
from algo.algo import minDominatingSetGuillaume, minDominatingSetOkan, isDominatingSet


def main(argv):
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR : NEED A JSON CONFIGURATION FILE!\n")
        sys.exit()

    problem_path = sys.argv[1]
    with open(problem_path) as problem_file:
        problem = Problem(json.load(problem_file))

    startTime = time.time()

    # gAdj = buildGraph(problem, ADJACENCY)
    # print("Taille du graphe : ", len(gAdj.getListNode()))
    # print("--- Build graph Adjacency in %s seconds ---" % (time.time() - startTime))

    # g = buildGraphWithDict(problem)
    # print("Taille du graphe : ", len(g.graphDict))
    # print("--- Build graph with dict V1 in %s seconds ---" % (time.time() - startTime))

    g = buildGraph(problem, DICT)
    print("Taille du graphe : ", len(g.graphDict))
    print("--- Build graph with dict in %s seconds ---" % (time.time() - startTime))

    startTime = time.time()
    dominatingSetGuillaume = minDominatingSetGuillaume(g, 5)
    print("--- Find dominating set Guillaume in %s seconds ---" % (time.time() - startTime))
    startTime = time.time()
    dominatingSetOkan = minDominatingSetOkan(g, 5)
    print("--- Find dominating Okan set in %s seconds ---" % (time.time() - startTime))
    print("il faut ", len(dominatingSetGuillaume) ," defenseurs d'apres Guillaume")
    print("il faut ", len(dominatingSetOkan) ," defenseurs d'apres Okan")
    displayGuillaume = Display(g, problem, dominatingSetGuillaume)
    # DISPLAY_FIELD OR DISPLAY_GRAPH
    displayGuillaume.run(DISPLAY_FIELD)
    displayOkan = Display(g, problem, dominatingSetOkan)
    displayOkan.run(DISPLAY_FIELD)

    return True


if __name__ == "__main__":
    main(sys.argv)
