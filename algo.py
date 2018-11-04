import copy

from node import BLACK, WHITE, AtkNode, DefNode
from graph import Graph


def searchDominatingSet(graph, nbDef):
    queue = [(copy.deepcopy(graph), [])]
    graphDone = list()
    while len(queue) != 0:
        graphAndRemovedNodes = queue.pop(0)
        currentGraph = graphAndRemovedNodes[0]
        graphDone.append(copy.deepcopy(currentGraph))
        graphDict = currentGraph.graphDict
        removedNodes = graphAndRemovedNodes[1]
        if not remainsUndominateAttacker(graphDict):
            return removedNodes
        for node in graphDict.copy():
            if node.color == BLACK and isinstance(node, DefNode):
                currentGraphDict = copy.deepcopy(graphDict)
                currentRemovedNodes = copy.deepcopy(removedNodes)
                if len(currentRemovedNodes) >= nbDef:
                    break
                for neighboorNode in currentGraphDict[node]:
                    neighboorNode.color = WHITE
                graphWithoutNode = Graph(currentGraphDict)
                graphWithoutNode.removeNode(node)
                currentRemovedNodes.append(node)
                if graphWithoutNode not in graphDone:
                    queue.append((graphWithoutNode, currentRemovedNodes))
    return None


def remainsUndominateAttacker(graph):
    for node in graph:
        if isinstance(node, AtkNode):
            if node.color == BLACK:
                return True
    return False
