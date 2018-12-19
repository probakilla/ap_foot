import copy
import itertools


def remainsUndominatedAttacker(graph, dominatedNode):
    for node in graph.graphDict:
        if node.isAtk() and node not in dominatedNode:
            return True
    return False


def isDominatingSet(graph, dominatingSet):
    dominatedNodeList = set()
    for node in dominatingSet:
        for neighbourNode in graph.getNeighbourhood(node):
            if neighbourNode.isAtk():
                dominatedNodeList.add(neighbourNode)
    for atkNode in graph.getAttacksList():
        if atkNode not in dominatedNodeList:
            return False
    return True

def greedyMinDominatingSet(graph, k):
    '''
    Retrieves the minimum dominating set lower than k for graph.
    Return None if there isn't such dominating set
    It use a greedy algo.
    '''
    dominatingSet = set()
    markedNodes = set()
    for _ in range(k):
        if (len(graph.getDefendersList()) == 0):
            return None
        nodeMaxDegree = graph.getDefenderMaxDegree(markedNodes)
        dominatingSet.add(nodeMaxDegree)
        markedNodes.add(nodeMaxDegree)
        for neighbourNode in graph.getNeighbourhood(nodeMaxDegree):
            markedNodes.add(neighbourNode)
        if isDominatingSet(graph, dominatingSet):
            return dominatingSet
    return None


def bruteForceMinDominatingSet(graph, k):
    '''
    Retrieves the minimum dominating set lower than k for graph, by brute force.
    Return None if there isn't such dominating set
    '''
    listDefender = graph.getDefendersList()
    for nbdefender in range(1, k+1):
        for defenderCombination in itertools.combinations(listDefender, nbdefender):
            if isDominatingSet(graph, defenderCombination):
                return defenderCombination
    return None
