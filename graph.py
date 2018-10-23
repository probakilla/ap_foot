from geometry import rotate, line, intersection, Point, newPointFromDistance, getDistance
from inputOutput import parseFile
import copy
from node import *


class Goal:
    def __init__(self, leftPost, rightPost, direction):
        self.leftPost = leftPost
        self.rightPost = rightPost
        self.direction = direction


class Graph:
    def __init__(self, graphDict=None):
        if graphDict == None:
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


'''
TODO
* IMPORTANT : gerer la direction des 'goals'
* performance : trouver l'intersection avec l'équation plutot que la fonction 'intersection()
'''


def buildGraph(file):
    jsonData = parseFile(file)

    jsongoals = jsonData["goals"][0]["posts"]
    gp1 = Point(jsongoals[0][0], jsongoals[0][1])
    gp2 = Point(jsongoals[1][0], jsongoals[1][1])
    goal_line = line(gp2, gp1)

    theta_step = jsonData["theta_step"]
    pos_step = jsonData["pos_step"]

    nodes = []

    for o in jsonData["opponents"]:
        opos = Point(o[0], o[1])
        g = Point(gp2.x, gp2.y)
        while g.y > gp1.y:
            g = rotate(opos, g, theta_step)
            p = intersection(line(opos, g), goal_line)  # plus tard, utiliser l'equation
            # verifier ici que ca ne depasse pas les cages
            node = p
            while ((node.x - opos.x) + (node.y - opos.y)) > 0:
                nodes.append(node)
                node = newPointFromDistance(node, opos, pos_step)

    k = 0
    while k < len(nodes):
        tmparr = nodes[:k + 1]
        for i in range(k + 1, len(nodes)):
            if getDistance(nodes[k], nodes[i]) > pos_step:
                tmparr.append(nodes[i])
        nodes = tmparr
        k = k + 1

    for n in nodes:
        print(str(n), end=",")

    return False


def searchDominatingSet(graph):
    queue = []
    queue.append((copy.deepcopy(graph), []))
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
                for neighboorNode in currentGraphDict[node]:
                    neighboorNode.color = WHITE
                graphWithoutNode = Graph(currentGraphDict)
                graphWithoutNode.removeNode(node)
                currentRemovedNodes = copy.deepcopy(removedNodes)
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
