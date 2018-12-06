''' Different algorithms for building graph from a given problem '''

import numpy as np
from algo.geometry import Point
from algo.geometry import segmentCircleIntersection
from algo.geometry import getDistance
from graph.graph import GraphWithDict
from graph.graph import GraphWithAdjacencyMatrix
from graph.node import Node
from matplotlib.patches import Circle
from algo.generateDefender import generateDefenders, generateDefendersTriangle

ADJACENCY = 1
DICT = 2
DICT_OLD = 3


def buildGraph(problem, buildWith):
    if buildWith == DICT_OLD:
        return buildGraphWithDict(problem)

    nodes = generateDefendersTriangle(problem)
    graph = GraphWithDict() if buildWith == DICT else GraphWithAdjacencyMatrix()

    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)

        shootings = []
        for g in problem.goals:
            for theta in np.arange(0.0, 2 * np.pi, problem.theta_step):
                goalIntersection = g.kickResult(ofender, theta)
                if goalIntersection is not None:
                    atkNode = Node(Point(ofender[0], ofender[1]), theta)
                    graph.addNode(atkNode)
                    shootings.append(
                        {"atk": atkNode, "intersect": goalIntersection})

        ofender_circle = Circle(ofender, problem.robot_radius)
        for defender in nodes:
            if not ofender_circle.contains_point(defender):
                listInterceptedShoot = []
                for shoot in shootings:
                    shootInterception = segmentCircleIntersection(
                        ofender, shoot["intersect"],
                        defender, problem.robot_radius)
                    if shootInterception is not None:
                        listInterceptedShoot += [shoot]
                if len(listInterceptedShoot) > 0:
                    defNode = Node(Point(defender[0], defender[1]))
                    graph.addNode(defNode)
                    for interceptedShoot in listInterceptedShoot:
                        graph.addEdge(interceptedShoot["atk"], defNode)
    return graph


def buildGraphWithDict(problem):
    nodes = generateDefendersTriangle(problem)
    graph = GraphWithDict()

    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)

        for goal in problem.goals:
            shootings = []
            for t in np.arange(0.0, 2 * np.pi, problem.theta_step):
                goalIntersection = goal.kickResult(ofender, t)
                if goalIntersection is not None:
                    atkNode = Node(Point(ofender[0], ofender[1]), t)
                    shootings.append(
                        {"atk": atkNode, "intersect": goalIntersection})

            for shooting in shootings:
                graph.addNode(shooting["atk"])
                for node in nodes:
                    if getDistance(node, shooting["intersect"]) < getDistance(ofender, shooting["intersect"]):
                        shootIntersection = segmentCircleIntersection(
                            Point(ofender[0], ofender[1]), shooting["intersect"], node, problem.robot_radius)
                        if shootIntersection is not None:
                            defNode = Node(Point(node[0], node[1]))
                            graph.addNode(defNode)
                            graph.addEdge(defNode, shooting["atk"])

    return graph
