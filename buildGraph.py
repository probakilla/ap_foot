import numpy as np

from geometry import Point, segmentCircleIntersection, getDistance
from graph import GraphWithDict, GraphWithAdjencyMatrix
from node import Node

def buildGraphWithDict(problem):
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] - problem.getFieldWidth() / 2), problem.getFieldWidth(), problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] - problem.getFieldHeight() / 2), problem.getFieldHeight(), problem.pos_step):
            nodes.append([i, j])

    graph = GraphWithDict()

    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)

        for g in problem.goals:
            shootings = []
            for t in np.arange(0.0, 360.0, problem.theta_step):
                goalIntersection = g.kickResult(ofender, t)
                if goalIntersection is not None:
                    atkNode = Node(Point(ofender[0], ofender[1]), t)
                    shootings.append(
                        {"atk": atkNode, "intersect": goalIntersection})

            for s in shootings:
                graph.addNode(s["atk"])
                for node in nodes:
                    if getDistance(node, s["intersect"]) < getDistance(ofender, s["intersect"]):
                        shoot_intersection = segmentCircleIntersection(
                            ofender, s["intersect"], node, problem.robot_radius)
                        if shoot_intersection is not None:
                            defNode = Node(Point(node[0], node[1]))
                            graph.addNode(defNode)
                            graph.addEdge(s["atk"], defNode)
    print("Taille du graphe : ", len(graph.graphDict))
    return graph


def buildGraphWithDictV2(problem):
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] - problem.getFieldWidth() / 2), problem.getFieldWidth(),
                       problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] - problem.getFieldHeight() / 2), problem.getFieldHeight(),
                           problem.pos_step):
            nodes.append([i, j])

    graph = GraphWithDict()

    shootings = []
    for i in range(problem.getNbOpponents()):
        ofender = problem.getOpponent(i)

        for g in problem.goals:
            for theta in np.arange(0.0, 360.0, problem.theta_step):
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

    print("Taille du graphe : ", len(graph.graphDict))
    return graph

def buildGraphWithAdjacenyMatrix(problem):
    nodes = []
    for i in np.arange((problem.getFieldCenter()[0] - problem.getFieldWidth() / 2), problem.getFieldWidth(), problem.pos_step):
        for j in np.arange((problem.getFieldCenter()[1] - problem.getFieldHeight() / 2), problem.getFieldHeight(), problem.pos_step):
            nodes.append([i, j])

    graph = GraphWithAdjencyMatrix()

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
    return graph