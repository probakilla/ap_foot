import time
import numpy as np

from geometry import Point, segmentCircleIntersection
from node import *


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

    # 1ère règle de réduction du cours
    def removeEdgeBetweenTwoWhiteNodes (self):
        graphDict = self.graphDict
        haveRemoveNode = False
        for node in graphDict:
            if node.color == WHITE:
                for neighboorNode in graphDict[node]:
                    if neighboorNode.color == WHITE:
                        self.removeEdgeBetweenTwoNodes (node, neighboorNode)
                        haveRemoveNode = True
        return haveRemoveNode

    # 2ème règle de réduction du cours
    def removeWhiteNodeWithBlackNeighboorhood (self):
        graphDict = self.graphDict
        haveRemoveNode = False
        for node in graphDict:
            if node == WHITE:
                blackNeighboorhood = True
                for neighboorNode in graphDict[node]:
                    if neighboorNode == WHITE:
                        blackNeighboorhood = False
                        break
                if blackNeighboorhood:
                    for largeNeighboorNode in graphDict[node][0]:
                        youpi = True
                        for neighboorNode in graphDict[node]:
                            if largeNeighboorNode not in graphDict[neighboorNode]:
                                youpi = False
                                break
                        if youpi:
                            self.removeNode (node)
                            haveRemoveNode = True
                            break
        return haveRemoveNode
    
    # 3ème règle de réduction du cours
    def R3 (self, nbDef):
        graphDict = self.graphDict
        removedNodes = []
        for node in graphDict:
            if nbDef <= 0:
                return removedNodes
            if node.color == BLACK and len(graphDict[node]) == 1:
                neighboorNode = graphDict[node][0]
                if neighboorNode.color == BLACK and isinstance (neighboorNode, DefNode):
                    nbDef -= 1
                    self.removeNodeAndWhiteColorNeighboor (neighboorNode)
                    removedNodes.append (neighboorNode)
        return removedNodes

    def removeNodeAndWhiteColorNeighboor (self, node):
        for neighboorNode in self.graphDict[node]:
            neighboorNode.color = WHITE
        self.removeNode (node)


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
        for t in np.arange(0.0, 360.0, problem.theta_step):
            for g in problem.goals:
                goal_intersection = g.kickResult(o, t)
                if goal_intersection is not None:
                    oNode = AtkNode(Point(o[0], o[1]), t)
                    graph.addNode(oNode)
                    for n in nodes:
                        if g.kickResult(n, t) is not None:
                            node_intersection = segmentCircleIntersection(o, goal_intersection, n, problem.robot_radius)
                            if node_intersection is not None:
                                dNode = DefNode(Point(n[0], n[1]))
                                graph.addNode(dNode)
                                graph.addEdge(oNode, dNode)
    print("--- %s seconds ---" % (time.time() - start_time))
    return graph
