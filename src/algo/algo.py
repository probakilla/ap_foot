import itertools
from algo.geometry import getDistance

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

def greedyMinDominatingSet(graph, k, minDistance):
    '''
    Retrieves the minimum dominating set lower than k for graph.
    Return None if there isn't such dominating set
    It use a greedy algo.
    '''
    dominatingSet = set()
    markedNodes = set()
    i = 0
    while i < k:
        i += 1
        if (len(graph.getDefendersList()) == 0):
            return None
        nodeMaxDegree = graph.getDefenderMaxDegree(markedNodes)
        if nodeMaxDegree is None:
            return None
        markedNodes.add(nodeMaxDegree)
        # If the node collide with a node in the set we doesn't choose it.
        if checkCollision(dominatingSet, nodeMaxDegree, minDistance):
            i = i-1
            continue
        dominatingSet.add(nodeMaxDegree)
        for neighbourNode in graph.getNeighbourhood(nodeMaxDegree):
            markedNodes.add(neighbourNode)
        if isDominatingSet(graph, dominatingSet):
            return dominatingSet
    return None


def bruteForceMinDominatingSet(graph, k, minDistance):
    '''
    Retrieves the minimum dominating set lower than k for graph, by brute force.
    Return None if there isn't such dominating set
    '''
    listDefender = graph.getDefendersList()
    for nbdefender in range(1, k+1):
        for defenderCombination in itertools.combinations(listDefender, nbdefender):
            if isDominatingSet(graph, defenderCombination):
                # Check if a node in defenderComination collide with an another node of this
                # set. If there is one the combination is invalid. 
                for node in defenderCombination:
                    if checkCollision(defenderCombination, node, minDistance):
                        continue
                return defenderCombination
    return None

def checkCollision(nodeSet, nodeToCheck, minDistance):
    '''
    Check if nodeToCheck is at a distance lower than minDistance from a node
    from nodeSet.
    Return True in case of collision.
    '''
    for node in nodeSet:
        if node != nodeToCheck and getDistance(nodeToCheck.pos, node.pos) < minDistance:
            return True
    return False