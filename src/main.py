''' Entry point of the program '''

import json
import sys
import time
import getopt
import os
import cProfile
from algo.algo import greedyMinDominatingSet
from algo.buildGraph import buildGraph, ADJACENCY, DICT
from inputOutput.display import Display, DISPLAY_FIELD, DISPLAY_GRAPH
from inputOutput.problem import Problem

DISPLAY_MODES = ["FIELD", "GRAPH", None]
GRAPH_TYPES = ["ADJ", "DICT"]
K = 3


def usage():
    """
        Display the usage of the program, specifying the arguments
    """
    print("USAGE: python main.py -f <CONFIG_FILE> -d <DISPLAY_TYPE> -g <GRAPH_TYPE> -k <NB_DEF>")
    print("Note: Options are not case sensitive.")
    print("-d, --display=DISPLAY_TYPE")
    print("  The display type of the graph, DISPLAY_TYPE possible values"
          " are: ", DISPLAY_MODES)
    print("-f, --file=CONFIG_FILE")
    print("  The path to the configuration file (json format).")
    print("-g, --graph=GRAPH_TYPE")
    print("  The type of the graph, possible values are: ", GRAPH_TYPES)
    print("-k")
    print("  The maximum number of defender for the dominating. Value need to be an integer. By default, k=3")
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

def main(filePath, displayType, graphType, profiling):
    ''' Entry point of the program '''

    problemPath = filePath
    with open(problemPath) as problemFile:
        problem = Problem(json.load(problemFile))

    profile = None
    if profiling:
        profile = cProfile.Profile()
        profile.enable()
    startTime = time.time()
    graph = buildGraph(problem, graphType)
    if profiling:
        profile.disable()
        print("Profiling results:")
        profile.print_stats("time")
    print("Taille du graphe : ", graph.size())
    print("--- Build graph in %s seconds ---" %
          (time.time() - startTime))

    startTime = time.time()
    domSet = greedyMinDominatingSet(graph, K)
    if domSet is None:
        print("Can't find position for %s defenders" % K)
    else:
        print("Need %s defender " % len(domSet))
    print("--- Min dominating set found in %s seconds ---" %
          (time.time() - startTime))

    if not displayType is None:
        if domSet is None:
            display = Display(graph, problem)
        else:
            display = Display(graph, problem, domSet)
        display.run(displayType, True)

    return True


if __name__ == "__main__":

    fileArg = None
    displayArg = None
    graphArg = None
    profilingArg = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:f:g:hpk:",
                                   ["display=", "file=", "graph=",
                                    "help", "profile"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--display"):
            displayArg = displayArgParse(arg.upper())
        elif opt in ("-f", "--file"):
            if not os.path.isfile(arg):
                print("ERROR: %s does not exists !" % arg)
                sys.exit(4)
            fileArg = arg
        elif opt in ("-g", "--graph"):
            graphArg = graphArgParse(arg.upper())
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-p", "--profile"):
            profilingArg = True
        elif opt in ("-k"):
            try:
                K = int(arg)
            except: 
                print("ERROR: Wrong k type value!")
                usage()
                sys.exit(5)
        else:
            assert False, "Unhandled option!"

    if fileArg is None:
        print("ERROR: Need a file!")
        usage()
        sys.exit()
    if graphArg is None:
        print("ERROR: Need a graph option!")
        usage()
        sys.exit()

    main(fileArg, displayArg, graphArg, profilingArg)
