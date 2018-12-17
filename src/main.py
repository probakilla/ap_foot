''' Entry point of the program '''

import json
import sys
import time
import getopt
import os
from algo.buildGraph import buildGraph, ADJACENCY, DICT
from inputOutput.display import Display, DISPLAY_FIELD, DISPLAY_GRAPH
from inputOutput.problem import Problem

DISPLAY_MODES = ["FIELD", "GRAPH"]
GRAPH_TYPES = ["ADJ", "DICT"]


def usage():
    """
        Display the usage of the program, specifying the arguments
    """
    print("USAGE: python main.py -f <CONFIG_FILE> -d <DISPLAY_TYPE> -g <GRAPH_TYPE>")
    print("Note: Options are not case sensitive.")
    print("-d, --display=DISPLAY_TYPE")
    print("  The display type of the graph, DISPLAY_TYPE possible values"
          " are: ", DISPLAY_MODES)
    print("-f, --file=CONFIG_FILE")
    print("  The path to the configuration file (json format).")
    print("-g, --graph=GRAPH_TYPE")
    print("  The type of the graph, possible values are: ", GRAPH_TYPES)
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
    res = -1
    if displayArgument == "FIELD":
        res = DISPLAY_FIELD
    elif displayArgument == "GRAPH":
        res = DISPLAY_GRAPH
    return res


def graphArgParse(graphArgument):
    """
        Tranforms the argument string into a vakue for the graph building
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


def main(filePath, displayType, graphType):
    ''' Entry point of the program '''

    problemPath = filePath
    with open(problemPath) as problemFile:
        problem = Problem(json.load(problemFile))

    startTime = time.time()
    graph = buildGraph(problem, graphType)
    print("Taille du graphe : ", graph.size())
    print("--- Build graph with dict V1 in %s seconds ---" %
          (time.time() - startTime))

    display = Display(graph, problem)
    display.run(displayType, True)
    return True


if __name__ == "__main__":

    fileArg = None
    displayArg = None
    graphArg = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:f:g:h",
                                   ["display=", "file=", "graph=", "help"])
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
        else:
            assert False, "Unhandled option!"

    if fileArg is None:
        print("ERROR: Need a file!")
        usage()
        sys.exit()
    if displayArg is None:
        print("ERROR: Need a display option!")
        usage()
        sys.exit()
    if graphArg is None:
        print("ERROR: Need a graph type!")
        usage()
        sys.exit()

    main(fileArg, displayArg, graphArg)
