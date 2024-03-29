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
    minDistance = 2 * problem.robot_radius

    shootings = list()
    for ofenderIdx in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(ofenderIdx)
        for goal in problem.goals:
            for theta in np.arange(0.0, 2 * np.pi, problem.theta_step):
                goalIntersection = goal.kickResult(ofender, theta)
                if goalIntersection is not None:
                    atkNode = Node(ofender, theta)
                    graph.addNode(atkNode)
                    shootings.append({"atk": atkNode, "intersect": goalIntersection})

    for defender in nodes:
        added = None
        for shoot in shootings:
            if getDistance(shoot["atk"].pos, defender) > minDistance:
                shootInterception = segmentCircleIntersection(shoot["atk"].pos, shoot["intersect"], defender, problem.robot_radius)
                if shootInterception is not None:
                    if added is None:
                        added = Node(defender)
                        graph.addNode(added)
                    graph.addEdge(shoot["atk"], added)
    return graph