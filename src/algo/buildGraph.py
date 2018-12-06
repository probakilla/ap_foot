''' Different algorithms for building graph from a given problem '''

import numpy as np
from matplotlib.patches import Circle
from algo.geometry import Point
from algo.geometry import segmentCircleIntersection
from graph.graphDict import GraphWithDict
from graph.graphAdjacency import GraphWithAdjacencyMatrix
from graph.node import Node
from algo.generateDefender import generateDefenders
from algo.generateDefender import generateDefendersTriangle

ADJACENCY = 1
DICT = 2

TRIANGLE_DEF = 1
CLASSI_DEF = 2


def buildGraph(problem, buildWith=ADJACENCY, defenderBuild=TRIANGLE_DEF):
    """
    Build a graph designed for the problem
        :param problem: An instance of the Problem class
        :param buildWith=ADJACENCY: Tells if the graph generated is with
            an adjacency matrix or not
        :param defenderBuild=TRIANGLE_DEF: Tell witch algorithm to use for
            generating the defenders
    """
    nodes = generateDefendersTriangle(problem) \
        if defenderBuild == TRIANGLE_DEF else generateDefenders(problem)
    graph = GraphWithDict() \
        if buildWith == DICT else GraphWithAdjacencyMatrix()

    for ofender in problem.opponents:
        shootings = list()
        for goal in problem.goals:
            for theta in np.arange(0.0, 2 * np.pi, problem.theta_step):
                goalIntersection = goal.kickResult(ofender, theta)
                if goalIntersection is not None:
                    atkNode = Node(Point(ofender[0], ofender[1]), theta)
                    graph.addNode(atkNode)
                    shootings.append(
                        {"atk": atkNode, "intersect": goalIntersection})

        ofenderCircle = Circle(ofender, problem.robot_radius)
        for defender in nodes:
            if not ofenderCircle.contains_point(defender):
                listInterceptedShoot = []
                for shoot in shootings:
                    shootInterception = segmentCircleIntersection(
                        ofender, shoot["intersect"],
                        defender, problem.robot_radius)
                    if shootInterception is not None:
                        listInterceptedShoot += [shoot]
                if not listInterceptedShoot:
                    defNode = Node(Point(defender[0], defender[1]))
                    graph.addNode(defNode)
                    for interceptedShoot in listInterceptedShoot:
                        graph.addEdge(interceptedShoot["atk"], defNode)
    return graph
