import time
import numpy as np
from node import Node
from geometry import Point, getDistance, segmentCircleIntersection


class GraphV2:
    def __init__(self):
        self.listNode = list()
        self.listIndexAtk = list()
        self.adjacencyMatrix = list(list())

    def __str__(self):
        strNode = ""
        for indexNode in range(len(self.listNode)):
            strNode += self.listNode[indexNode].__str__()
            strNode += ": ["
            for indexNeighboor in range(len(self.adjacencyMatrix[indexNode])):
                if self.adjacencyMatrix[indexNode][indexNeighboor]:
                    strNode += self.listNode[indexNeighboor].__str__()
            strNode += "]\n"
        return strNode

    def getListNode(self):
        return self.listNode

    def getAdjacencyMatrix(self):
        return self.adjacencyMatrix

    def getListAtkNodes(self):
        res = list()
        for i in self.listIndexAtk:
            res.append(self.listNode[i])
        return res

    def getListDefNodes(self):
        res = self.listNode
        for i in self.listIndexAtk:
            del res[i]
        return res

    def addAtk(self, node):
        self.listIndexAtk.append(len(self.listNode))
        self.addNode(node)

    def addNode(self, node):
        self.listNode.append(node)
        for i in self.adjacencyMatrix:
            i.append(False)
        boolList = [False] * (len(self.adjacencyMatrix) + 1)
        self.adjacencyMatrix.append(boolList)

    def addEdge(self, node1, node2):
        indexNode1 = self.listNode.index(node1)
        indexNode2 = self.listNode.index(node2)
        self.adjacencyMatrix[indexNode1][indexNode2] = True


def buildGraph(problem):
    startTime = time.time()
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] - problem.getFieldWidth() / 2), problem.getFieldWidth(), problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] - problem.getFieldHeight() / 2), problem.getFieldHeight(), problem.pos_step):
            nodes.append([i, j])

    graph = GraphV2()

    for indexOpp in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(indexOpp)

        for goal in problem.goals:
            shootings = []
            for theta in np.arange(0.0, 360.0, problem.theta_step):
                goalIntersection = goal.kickResult(ofender, theta)
                if goalIntersection is not None:
                    atkNode = Node(Point(ofender[0], ofender[1]), theta)
                    shootings.append(
                        {"atk": atkNode, "intersect": goalIntersection})
                    graph.addAtk(atkNode)

    for defender in nodes:
        listInterceptedShoot = []
        for shoot in shootings:
            shootInterception = segmentCircleIntersection(
                ofender, shoot["intersect"], defender, problem.robot_radius)
            if shootInterception is not None:
                listInterceptedShoot += [shoot]
        if len(listInterceptedShoot) > 0:
            defNode = Node(Point(defender[0], defender[1]))
            graph.addNode(defNode)
            for interceptedShoot in listInterceptedShoot:
                graph.addEdge(interceptedShoot["atk"], defNode)

    print("Taille du graphe : ", len(graph.getListNode()))
    print("--- %s seconds ---" % (time.time() - startTime))
    return graph
