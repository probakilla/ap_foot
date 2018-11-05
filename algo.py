import copy

from node import BLACK, WHITE, AtkNode, DefNode
from graph import Graph

def DSAP (graph, k, removedNodes = []):
    cont = True
    while k > 0 and cont:
        tmp = False
        tmp = graph.removeEdgeBetweenTwoWhiteNodes () or tmp
        tmp = graph.removeWhiteNodeWithBlackNeighboorhood () or tmp
        tmp2 = graph.R3 (k)
        if tmp2 != []:
            tmp = True
            removedNodes += tmp2
        cont = tmp
    if not remainsUndominateAttacker (graph.graphDict):
        return removedNodes
    if k == 0:
        return None
    for node in graph.graphDict:
        if node.color == BLACK and isinstance (node, DefNode) and len (graph.graphDict[node]) <= 7:
            graphWithoutNode = copy.deepcopy (graph)
            graphWithoutNode.removeNodeAndWhiteColorNeighboor (node)
            currentRemovedNodes = copy.deepcopy (removedNodes)
            currentRemovedNodes.append (node)
            dominatingSet = DSAP (graphWithoutNode, k-1, currentRemovedNodes)
            if dominatingSet is not None:
                return dominatingSet
            for neighboorNode in graph.graphDict[node]:
                if neighboorNode.color == BLACK and isinstance (neighboorNode, DefNode):
                    currentRemovedNodes = copy.deepcopy (removedNodes)
                    currentRemovedNodes.append (neighboorNode)
                    graphWithoutNode = copy.deepcopy (graph)
                    graphWithoutNode.removeNodeAndWhiteColorNeighboor (neighboorNode)
                    dominatingSet = DSAP (graphWithoutNode, k-1, removedNodes)
                    if dominatingSet is not None:
                        return dominatingSet
            return None
    return None

    

def remainsUndominateAttacker(graph):
    for node in graph:
        if isinstance(node, AtkNode):
            if node.color == BLACK:
                return True
    return False
