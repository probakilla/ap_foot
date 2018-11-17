from graph import GraphWithDict
import copy

def minDominatingSet(graph, maxDominatingSetLength):
    markedNodes = set()
    removedNodes = set()
    queue = [(markedNodes, removedNodes)]
    removedNodesChecked = list()
    while len(queue) != 0:
        markedAndRemovedNodes = queue.pop(0)
        markedNodes = markedAndRemovedNodes[0]
        removedNodes = markedAndRemovedNodes[1]
        for currentNode in graph.graphDict:
            if currentNode not in markedNodes and not currentNode.isAtk():
                currentRemovedNodes = removedNodes.copy()
                currentMarkedNodes = markedNodes.copy() 
                lenCurrentRemovedNodes = len(currentRemovedNodes)
                if lenCurrentRemovedNodes == maxDominatingSetLength:
                    break
                if lenCurrentRemovedNodes > maxDominatingSetLength:
                    return None
                currentMarkedNodes.add(currentNode)
                currentRemovedNodes.add(currentNode)
                for neighboorNode in graph.graphDict[currentNode]:
                    currentMarkedNodes.add(neighboorNode)
                if not remainsUndominatedAttacker(graph, currentMarkedNodes):
                    return currentRemovedNodes
                if currentRemovedNodes not in removedNodesChecked:
                    removedNodesChecked.append(currentRemovedNodes)
                    queue.append((currentMarkedNodes, currentRemovedNodes))
    return None

def remainsUndominatedAttacker(graph, dominatedNode):
    for node in graph.graphDict:
        if node.isAtk() and node not in dominatedNode:
            return True
    return False
