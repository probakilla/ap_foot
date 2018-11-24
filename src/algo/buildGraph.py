''' Different algorithms for building graph from a given problem '''

import numpy as np
from algo.geometry import Point
from algo.geometry import segmentCircleIntersection
from algo.geometry import getDistance
from algo.geometry import moveInLine
from algo.geometry import getDistancePts
from graph.graph import GraphWithDict
from graph.graph import GraphWithAdjacencyMatrix
from graph.node import Node


def buildGraphWithDict(problem):
    ''' First version of the graph building algorithm build an instance
    of GraphWithDict '''
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] - problem.getFieldWidth() / 2), problem.getFieldWidth(), problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] - problem.getFieldHeight() / 2), problem.getFieldHeight(), problem.pos_step):
            nodes.append([i, j])

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
                            ofender, shooting["intersect"], node, problem.robot_radius)
                        if shootIntersection is not None:
                            defNode = Node(Point(node[0], node[1]))
                            graph.addNode(defNode)
                            graph.addEdge(shooting["atk"], defNode)

    return graph


def buildGraphWithDictV2(problem):
    ''' Second version of graph building, retrieves an instance of
    GraphWithDict '''
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] - problem.getFieldWidth() / 2), problem.getFieldWidth(),
                       problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] - problem.getFieldHeight() / 2), problem.getFieldHeight(),
                           problem.pos_step):
            nodes.append([i, j])

    graph = GraphWithDict()

    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)

        shootings = []
        for g in problem.goals:
            for theta in np.arange(0.0, 2 * np.pi, problem.theta_step):
                goalIntersection = g.kickResult(ofender, theta)
                if goalIntersection is not None:
                    atkNode = Node(Point(ofender[0], ofender[1]), theta)
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
                defNode = Node(Point(defender[0], defender[1]))
                graph.addNode(defNode)
                for interceptedShoot in listInterceptedShoot:
                    graph.addEdge(interceptedShoot["atk"], defNode)
    return graph


def buildGraphWithAdjacencyMatrix(problem):
    ''' Build an instance of GraphWithAdjacencyMatrix for a given problem '''
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] - problem.getFieldWidth() / 2), problem.getFieldWidth(), problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] - problem.getFieldHeight() / 2), problem.getFieldHeight(), problem.pos_step):
            nodes.append([i, j])

    graph = GraphWithAdjacencyMatrix()

    for indexOpp in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(indexOpp)

        shootings = []
        for goal in problem.goals:
            for theta in np.arange(0.0, 2 * np.pi, problem.theta_step):
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
    return graph
