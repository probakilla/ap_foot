import time

from geometry import Point, segmentCircleIntersection
import copy
from node import *
import numpy as np


class Goal:
    def __init__(self, leftPost, rightPost, direction):
        self.leftPost = leftPost
        self.rightPost = rightPost
        self.direction = direction


class Graph:
    def __init__(self, graphDict=None):
        if graphDict is None:
            graphDict = {}
        self.graphDict = graphDict

    def __str__(self):
        return self.graphDict.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def addNode(self, node):
        if node not in self.graphDict:
            self.graphDict[node] = []

    def addEdge(self, node1, node2):
        self.addEdgeBetweenNodes(node1, node2)
        self.addEdgeBetweenNodes(node2, node1)

    def addEdgeBetweenNodes(self, node1, node2):
        if node1 in self.graphDict:
            if node2 not in self.graphDict[node1]:
                self.graphDict[node1].append(node2)
        else:
            self.graphDict[node1] = [node2]

    def listNodes(self):
        return list(self.graphDict.keys())

    def listEdges(self):
        listEdges = []
        for node in self.graphDict:
            for edge in self.graphDict[node]:
                listEdges.append((node, edge))
        return listEdges

    def removeEdgeBetweenTwoNodes(self, node1, node2):
        self.graphDict[node1].remove(node2)
        self.graphDict[node2].remove(node1)

    def removeNode(self, node):
        listNeighboorNode = self.graphDict[node].copy()
        for neighboorNode in listNeighboorNode:
            self.removeEdgeBetweenTwoNodes(node, neighboorNode)
        del self.graphDict[node]


def buildGraph(problem):
    start_time = time.time()
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] - problem.getFieldWidth() / 2), problem.getFieldWidth(),
                       problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] - problem.getFieldHeight() / 2), problem.getFieldHeight(),
                           problem.pos_step):
            nodes.append([i, j])

    graph = Graph()
    for i in range(problem.getNbOpponents()):
        o = problem.getOpponent(i)
        oNode = AtkNode(Point(o[0], o[1]))
        graph.addNode(oNode)
        for t in np.arange(0.0, 360.0, problem.theta_step):
            for g in problem.goals:
                goal_intersection = g.kickResult(o, t)
                if goal_intersection is not None:
                    for n in nodes:
                        if g.kickResult(n, t) is not None:
                            node_intersection = segmentCircleIntersection(o, goal_intersection, n, problem.robot_radius)
                            if node_intersection is not None:
                                dNode = DefNode(Point(n[0], n[1]))
                                graph.addNode(dNode)
                                graph.addEdge(oNode, dNode)
    print("--- %s seconds ---" % (time.time() - start_time))

    return graph


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
