from graph.graph import GraphWithDict
import copy
import itertools


def minDominatingSet(graph, maxDominatingSetLength):
    ''' Find the minimum dominating set for a given set max length '''
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

def isDominatingSet(graph, dominatingSet):
    dominatedNodeList = set()
    for node in dominatingSet:
        for neighboorNode in graph.graphDict[node]:
            if neighboorNode.isAtk():
                dominatedNodeList.add(neighboorNode)
    for atkNode in graph.getAttacks():
        if atkNode not in dominatedNodeList:
            return False
    return True


def minDominationSetOkan(graph, k):
    attacks = graph.getAttacks()
    defenders = graph.getDefenders()

    for nbdefender in range(1, k + 1):
        for bits in itertools.combinations(range(len(defenders)), nbdefender):

            attacks_tmp = attacks.copy()

            for defIdx in bits:
                defender = defenders[defIdx]
                shotsStopped = graph.graphDict[defender]

                if nbdefender == 1 and len(shotsStopped) == len(attacks):
                    return {defender}
                else:
                    for shot in shotsStopped:
                        if shot in attacks_tmp:
                            attacks_tmp.remove(shot)

            if len(attacks_tmp) == 0:
                dominatingSet = set()
                for defIdx in bits:
                    dominatingSet.add(defenders[defIdx])
                return dominatingSet
