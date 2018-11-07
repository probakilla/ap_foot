import copy

from node import BLACK, WHITE, AtkNode, DefNode
from graph import Graph

def DSAP (graph, k, removedNodes = []):
    graphCpy = copy.deepcopy (graph)
    cont = True
    while k > 0 and cont:
        tmp = False
        tmp = graphCpy.removeEdgeBetweenTwoWhiteNodes () or tmp
        tmp = graphCpy.removeWhiteNodeWithBlackNeighboorhood () or tmp
        tmp2 = graphCpy.R3 (k)
        if tmp2 != []:
            tmp = True
            removedNodes += tmp2
        cont = tmp
    if not remainsUndominateAttacker (graphCpy.graphDict):
        return removedNodes
    if k == 0:
        return None
    for node in graphCpy.graphDict:
        if node.color == BLACK and isinstance (node, DefNode) and len (graphCpy.graphDict[node]) <= 7:
            graphWithoutNode = copy.deepcopy (graphCpy)
            graphWithoutNode.removeNodeAndWhiteColorNeighboor (node)
            currentRemovedNodes = copy.deepcopy (removedNodes)
            currentRemovedNodes.append (node)
            dominatingSet = DSAP (graphWithoutNode, k-1, currentRemovedNodes)
            if dominatingSet is not None:
                return dominatingSet
            for neighboorNode in graphCpy.graphDict[node]:
                if neighboorNode.color == BLACK and isinstance (neighboorNode, DefNode):
                    currentRemovedNodes = copy.deepcopy (removedNodes)
                    currentRemovedNodes.append (neighboorNode)
                    graphWithoutNode = copy.deepcopy (graphCpy)
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
