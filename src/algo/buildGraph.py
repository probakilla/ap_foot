''' Different algorithms for building graph from a given problem '''
import numpy as np
from algo.geometry import segmentCircleIntersection
from algo.generateDefender import generateDefenders, generateDefendersTriangle
from algo.geometry import getDistance
from graph.node import Node
from graph.graphAdjacency import GraphAdjacency
from graph.graphDict import GraphDict

ADJACENCY = 0
DICT = 1

TRIANGLE_DEF = 0
CLASSIC_DEF = 1


def buildGraph(problem, buildWith=ADJACENCY, defenderBuild=TRIANGLE_DEF):
    """
    Build a graph designed for the problem
        :param problem: An instance of the Problem class
        :param buildWith=ADJACENCY: Tells if the graph generated is with
            an adjacency matrix or not
        :param defenderBuild=TRIANGLE_DEF: Tell witch algorithm to use for
            generating the defenders
    """
    nodes = generateDefendersTriangle(problem) if defenderBuild == TRIANGLE_DEF else generateDefenders(problem)
    graph = GraphDict() if buildWith == DICT else GraphAdjacency()

    nodeIdx = 0

    for ofenderIdx in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(ofenderIdx)
        shootings = list()
        for goal in problem.goals:
            for theta in np.arange(0.0, 2 * np.pi, problem.theta_step):
                goalIntersection = goal.kickResult(ofender, theta)
                if goalIntersection is not None:
                    atkNode = Node(nodeIdx, ofender, theta)
                    nodeIdx += 1
                    graph.addNode(atkNode)
                    shootings.append(
                        {"atk": atkNode, "intersect": goalIntersection})

        listInterceptedShoot = list()
        for defender in nodes:
            if getDistance(ofender, defender) > problem.robot_radius:
                for shoot in shootings:
                    shootInterception = segmentCircleIntersection(
                        ofender, shoot["intersect"],
                        defender, problem.robot_radius)
                    if shootInterception is not None:
                        listInterceptedShoot.append((shoot["atk"], Node(nodeIdx, defender)))
                        nodeIdx += 1
        if listInterceptedShoot:
            for interceptedShoot in listInterceptedShoot:
                graph.addNode(interceptedShoot[1])
                graph.addEdge(interceptedShoot[0], interceptedShoot[1])

    addColision(graph, problem.robot_radius * 2)
    return graph


def addColision(graph, minDistance):
    defenderList = graph.getDefendersList()
    nbDefenders = len(defenderList)
    enumDefender = enumerate(defenderList)
    for i, firstNode in enumDefender:
        for indexSecondNode in range(i, nbDefenders):
            secondNode = defenderList[indexSecondNode]
            if firstNode.id != secondNode.id and getDistance(firstNode.pos, secondNode.pos) <= minDistance:
                graph.addEdge(firstNode, secondNode)