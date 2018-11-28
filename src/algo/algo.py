from graph.graph import GraphWithDict
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
        for neighboorNode in graph.graphDict[node]:
            if neighboorNode.isAtk():
                dominatedNodeList.add(neighboorNode)
    for atkNode in graph.getAttacks():
        if atkNode not in dominatedNodeList:
            return False
    return True

def minDominatingSetGuillaume(graph, k):
    listDefender = graph.getDefenders()
    for nbdefender in range(1, k + 1):
        for defenderCombination in itertools.combinations(listDefender, nbdefender):
            if isDominatingSet(graph, defenderCombination):
                return defenderCombination
    return None

def minDominatingSetOkan(graph, k):
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
