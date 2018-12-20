''' Entry point of the program '''

import json
import sys
import time
import getopt
import os
import cProfile
from algo.algo import greedyMinDominatingSet, bruteForceMinDominatingSet
from algo.buildGraph import buildGraph, ADJACENCY, DICT
from inputOutput.display import Display, DISPLAY_FIELD, DISPLAY_GRAPH
from inputOutput.problem import Problem

DISPLAY_MODES = ["FIELD", "GRAPH", None]
GRAPH_TYPES = ["ADJ", "DICT"]
ALGO_TYPE = ["GREEDY", "BRUTE"]
K = 3


def usage():
    """
        Display the usage of the program, specifying the arguments
    """
    print("USAGE: python main.py -f <CONFIG_FILE> -d <DISPLAY_TYPE> -g"
          "GRAPH_TYPE> -k <NB_DEF>")
    print("Note: Options are not case sensitive.")
    print("-a, --algo=ALGO_TYPE")
    print("  The algorithm to use for the dominating set. Possible values are"
          " {}".format(ALGO_TYPE))
    print("-d, --display=DISPLAY_TYPE")
    print("  The display type of the graph, DISPLAY_TYPE possible values"
          " are {}, default value is GREEDY".format(DISPLAY_MODES))
    print("-f, --file=CONFIG_FILE")
    print("  The path to the configuration file (json format).")
    print("-g, --graph=GRAPH_TYPE")
    print("  The type of the graph, possible values are {}".format(GRAPH_TYPES))
    print("-k")
    print("  The maximum number of defender for the dominating. Value need to"
          " be an integer. By default, k=3")
    print("-h, --help")
    print("  Display the help for this program.")


def displayArgParse(displayArgument):
    """
        Transforms the argument string into a value for the display function.
        Also checks if the argument is a valid value.
        :param displayArgument: The argument to transform
    """
    if not displayArgument in DISPLAY_MODES:
        print("ERROR: Wrong display type value!")
        usage()
        sys.exit(3)
    res = displayArgument
    if displayArgument == "FIELD":
        res = DISPLAY_FIELD
    elif displayArgument == "GRAPH":
        res = DISPLAY_GRAPH
    return res


def graphArgParse(graphArgument):
    """
        Tranforms the argument string into a value for the graph building
        function. Also checks if the argument is a valid value.
        :param graphArgument: The argument to transform
    """
    if not graphArgument in GRAPH_TYPES:
        print("ERROR: Wrong graph type value!")
        usage()
        sys.exit(5)
    res = -1
    if graphArgument == "ADJ":
        res = ADJACENCY
    elif graphArgument == "DICT":
        res = DICT
    return res


if __name__ == "__main__":

    FILE_ARG = None
    DISPLAY_ARG = None
    GRAPH_ARG = None
    ALGO_ARG = "GREEDY"
    PROFILING_ARG = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:d:f:g:hpk:",
                                   ["algo=", "display=", "file=", "graph=",
                                    "help", "profile"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-a", "--algo"):
            if not arg.upper() in ALGO_TYPE:
                print("ERROR: Wrong algorithm type!")
                usage()
                sys.exit(7)
            ALGO_ARG = arg.upper()
        elif opt in ("-d", "--display"):
            DISPLAY_ARG = displayArgParse(arg.upper())
        elif opt in ("-f", "--file"):
            if not os.path.isfile(arg):
                print("ERROR: %s does not exists !" % arg)
                sys.exit(4)
            FILE_ARG = arg
        elif opt in ("-g", "--graph"):
            GRAPH_ARG = graphArgParse(arg.upper())
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-p", "--profile"):
            PROFILING_ARG = True
        elif opt in ("-k"):
            try:
                K = int(arg)
            except:
                print("ERROR: Wrong k type value!")
                usage()
                sys.exit(5)
        else:
            assert False, "Unhandled option!"

    if FILE_ARG is None:
        print("ERROR: Need a file!")
        usage()
        sys.exit()
    if GRAPH_ARG is None:
        print("ERROR: Need a graph option!")
        usage()
        sys.exit()

    with open(FILE_ARG) as problemFile:
        problem = Problem(json.load(problemFile))

    profile = None
    if PROFILING_ARG:
        profile = cProfile.Profile()
        profile.enable()
    startTime = time.time()
    graph = buildGraph(problem, GRAPH_ARG)
    if PROFILING_ARG:
        profile.disable()
        print("Profiling results:")
        profile.print_stats("time")
    print("Taille du graphe : ", graph.size())
    print("--- Build graph in %s seconds ---" %
          (time.time() - startTime))

    startTime = time.time()
    domSet = None
    if ALGO_ARG == "BRUTE":
        domSet = bruteForceMinDominatingSet(graph, K)
    elif ALGO_ARG == "GREEDY":
        domSet = greedyMinDominatingSet(graph, K)

    if domSet is None:
        print("Can't find position for %s defenders" % K)
    else:
        print("Need %s defender " % len(domSet))
    print("--- Min dominating set found in %s seconds ---" %
          (time.time() - startTime))

    if not DISPLAY_ARG is None:
        if domSet is None:
            display = Display(graph, problem)
        else:
            display = Display(graph, problem, domSet)
        display.run(DISPLAY_ARG, True)
