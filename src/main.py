import json
import sys
import cProfile
import time
from algo.buildGraph import buildGraphWithAdjacencyMatrix, buildGraphWithDict, buildGraphWithDictV2
from inputOutput.display import Display, DISPLAY_GRAPH, DISPLAY_FIELD
from inputOutput.problem import Problem
from algo.algo import minDominatingSet


def main(argv):
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR : NEED A JSON CONFIGURATION FILE!\n")
        sys.exit()

    problem_path = sys.argv[1]
    with open(problem_path) as problem_file:
        problem = Problem(json.load(problem_file))

    startTime = time.time()

    gAdj = buildGraphWithAdjacencyMatrix(problem)
    print("Taille du graphe : ", len(gAdj.getListNode()))
    print("--- Build graph Adjacency in %s seconds ---" % (time.time() - startTime))

    # g = buildGraphWithDict(problem)
    # print("Taille du graphe : ", len(g.graphDict))
    # print("--- Build graph with dict V1 in %s seconds ---" % (time.time() - startTime))

    g = buildGraphWithDictV2(problem)
    print("Taille du graphe : ", len(g.graphDict))
    print("--- Build graph with dict V1 in %s seconds ---" % (time.time() - startTime))

    startTime = time.time()
    # print(minDominatingSet(g, 10))
    # print("--- Find dominating set in %s seconds ---" % (time.time() - startTime))

    display = Display(gAdj, problem)
    #DISPLAY_FIELD OR DISPLAY_GRAPH
    display.run(DISPLAY_GRAPH)

    return True


if __name__ == "__main__":
    main(sys.argv)
