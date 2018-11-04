import copy

from node import BLACK, WHITE, AtkNode, DefNode
from graph import Graph

def DSAP (graph, k, removedNodes = []):
    # print ("Start")
    # print (k)
    # print (removedNodes)
    cont = True
    while k > 0 and cont:
        cont = graph.removeEdgeBetweenTwoWhiteNodes () or cont
        cont = graph.removeWhiteNodeWithBlackNeighboorhood () or cont
        tmp = graph.R3 (k)
        if tmp == []:
            cont = False
        else:
            cont = True
            removedNodes.append (tmp)
    #         print (removedNodes)
    # print (k)
    if not remainsUndominateAttacker (graph.graphDict):
        # print ("notRemains")
        # print (removedNodes)
        return removedNodes
    if k == 0:
        # print ("None")
        return None
    for node in graph.graphDict:
        if node.color == BLACK and isinstance (node, DefNode) and len (graph.graphDict[node]) <= 7:
            graphWithoutNode = copy.deepcopy (graph)
            graphWithoutNode.removeNodeAndWhiteColorNeighboor (node)
            currentRemovedNodes = copy.deepcopy (removedNodes)
            currentRemovedNodes.append (node)
            dominatingSet = DSAP (graphWithoutNode, k-1, currentRemovedNodes)
            if dominatingSet is not None:
                # print ("notNone")
                # print (dominatingSet)
                return dominatingSet
            for neighboorNode in graph.graphDict[node]:
                if neighboorNode.color == BLACK and isinstance (node, DefNode):
                    currentRemovedNodes = copy.deepcopy (removedNodes)
                    currentRemovedNodes.append (neighboorNode)
                    graphWithoutNode = copy.deepcopy (graph)
                    graphWithoutNode.removeNodeAndWhiteColorNeighboor (neighboorNode)
                    dominatingSet = DSAP (graphWithoutNode, k-1, removedNodes)
                    if dominatingSet is not None:
                        # print ("test")
                        # print (dominatingSet)
                        return dominatingSet
            # print ("None")
            return None
    # print ("None")
    return None

    

def remainsUndominateAttacker(graph):
    for node in graph:
        if isinstance(node, AtkNode):
            if node.color == BLACK:
                return True
    return False
