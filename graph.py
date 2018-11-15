import time
import numpy as np

from geometry import Point, segmentCircleIntersection, getDistance
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
        res = ""
        for node in self.graphDict:
            strNode = node.__str__()
            strNode += ": ["
            for neighboorNode in self.graphDict[node]:
                strNode += neighboorNode.__str__()
                strNode += ", "
            strNode += "]\n"
            res += strNode
        return res

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def addNode(self, node):
        #     if node in self.graphDict:
        #         raise ValueError("NODE %s ALREADY IN GRAPH !!" % (node))
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

    def getAtkNodes(self):
        atkNodes = []
        for node in self.graphDict:
            if isinstance(node, AtkNode):
                atkNodes.append(node)
        return atkNodes

    def getDefNodes(self):
        defNodes = []
        for node in self.graphDict:
            if isinstance(node, DefNode):
                defNodes.append(node)
        return defNodes

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
    def removeEdgeBetweenTwoWhiteNodes(self):
        graphDict = self.graphDict
        haveRemoveNode = False
        for node in graphDict:
            if node.color == WHITE:
                for neighboorNode in graphDict[node]:
                    if neighboorNode.color == WHITE:
                        self.removeEdgeBetweenTwoNodes(node, neighboorNode)
                        haveRemoveNode = True
        return haveRemoveNode

    # 2ème règle de réduction du cours
    def removeWhiteNodeWithBlackNeighboorhood(self):
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
                            self.removeNode(node)
                            haveRemoveNode = True
                            break
        return haveRemoveNode

    # 3ème règle de réduction du cours
    def R3(self, nbDef):
        graphDict = self.graphDict
        removedNodes = []
        for node in list(graphDict):
            if node in removedNodes:
                break
            if nbDef <= 0:
                return removedNodes
            if node.color == BLACK and len(graphDict[node]) == 1:
                neighboorNode = graphDict[node][0]
                if neighboorNode.color == BLACK and isinstance(neighboorNode, DefNode):
                    nbDef -= 1
                    self.removeNodeAndWhiteColorNeighboor(neighboorNode)
                    removedNodes.append(neighboorNode)
        return removedNodes

    def removeNodeAndWhiteColorNeighboor(self, node):
        for neighboorNode in self.graphDict[node]:
            neighboorNode.color = WHITE
        self.removeNode(node)

    def removeNode(self, node):
        listNeighboorNode = self.graphDict[node].copy()
        for neighboorNode in listNeighboorNode:
            self.removeEdgeBetweenTwoNodes(node, neighboorNode)
        del self.graphDict[node]


def buildGraph(problem):
    startTime = time.time()
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] - problem.getFieldWidth() / 2), problem.getFieldWidth(), problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] - problem.getFieldHeight() / 2), problem.getFieldHeight(), problem.pos_step):
            nodes.append([i, j])

    graph = Graph()

    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)

        for g in problem.goals:
            shootings = []
            for t in np.arange(0.0, 360.0, problem.theta_step):
                goalIntersection = g.kickResult(ofender, t)
                if goalIntersection is not None:
                    atkNode = AtkNode(Point(ofender[0], ofender[1]), t)
                    shootings.append(
                        {"atk": atkNode, "intersect": goalIntersection})

            for s in shootings:
                graph.addNode(s["atk"])
                for node in nodes:
                    if getDistance(node, s["intersect"]) < getDistance(ofender, s["intersect"]):
                        shoot_intersection = segmentCircleIntersection(
                            ofender, s["intersect"], node, problem.robot_radius)
                        if shoot_intersection is not None:
                            defNode = DefNode(Point(node[0], node[1]))
                            graph.addNode(defNode)
                            graph.addEdge(s["atk"], defNode)

    print("Taille du graphe : ", len(graph.graphDict))
    print("--- %s seconds ---" % (time.time() - startTime))
    return graph


def buildGraphV2(problem):
    startTime = time.time()
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] - problem.getFieldWidth() / 2), problem.getFieldWidth(),
                       problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] - problem.getFieldHeight() / 2), problem.getFieldHeight(),
                           problem.pos_step):
            nodes.append([i, j])

    graph = Graph()

    shootings = []
    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)

        for g in problem.goals:
            for theta in np.arange(0.0, 360.0, problem.theta_step):
                goalIntersection = g.kickResult(ofender, theta)
                if goalIntersection is not None:
                    atkNode = AtkNode(Point(ofender[0], ofender[1]), theta)
                    shootings.append(
                        {"atk": atkNode, "intersect": goalIntersection})

    for defender in nodes:
        listInterceptedShoot = []
        for shoot in shootings:
            shootInterception = segmentCircleIntersection(
                ofender, shoot["intersect"], defender, problem.robot_radius)
            if shootInterception is not None:
                listInterceptedShoot += [shoot]
        if len(listInterceptedShoot) > 0:
            defNode = DefNode(Point(defender[0], defender[1]))
            graph.addNode(defNode)
            for interceptedShoot in listInterceptedShoot:
                graph.addEdge(interceptedShoot["atk"], defNode)

    print("Taille du graphe : ", len(graph.graphDict))
    print("--- %s seconds ---" % (time.time() - startTime))
    return graph
